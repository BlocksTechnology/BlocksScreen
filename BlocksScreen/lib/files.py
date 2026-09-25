from __future__ import annotations

import logging
import typing
from collections import deque
from dataclasses import asdict, dataclass, field, replace
from enum import StrEnum, auto
from pathlib import Path

import events
import helper_methods
from lib.moonrakerComm import MoonWebSocket
from lib.utils import gcode_loader
from PyQt6 import QtCore, QtWidgets

logger = logging.getLogger(__name__)


class FileAction(StrEnum):
    """Enumeration of possible file actions from Moonraker notifications."""

    CREATE_FILE = auto()
    DELETE_FILE = auto()
    MOVE_FILE = auto()
    MODIFY_FILE = auto()
    CREATE_DIR = auto()
    DELETE_DIR = auto()
    MOVE_DIR = auto()
    ROOT_UPDATE = auto()
    UNKNOWN = auto()

    @classmethod
    def from_string(cls, action: str) -> FileAction:
        """Convert Moonraker action string to enum."""
        try:
            return cls(action.lower())
        except ValueError:
            return cls.UNKNOWN


@dataclass(frozen=True, slots=True)
class FileMetadata:
    """Gcode file metadata; thumbnails as filesystem paths."""

    filename: str = ""
    thumbnail_paths: list[str] = field(default_factory=list)
    filament_total: dict | str | float = field(default_factory=dict)
    estimated_time: int = 0
    layer_count: int = -1
    total_layer: int = -1
    object_height: float = -1.0
    size: int = 0
    modified: float = 0.0
    filament_type: str = "Unknown"
    filament_weight_total: float = -1.0
    layer_height: float = -1.0
    first_layer_height: float = -1.0
    first_layer_extr_temp: float = -1.0
    first_layer_bed_temp: float = -1.0
    filament_name: str = "Unknown"
    nozzle_diameter: float = -1.0
    slicer: str = "Unknown"
    slicer_version: str = "Unknown"
    gcode_start_byte: int = 0
    gcode_end_byte: int = 0
    print_start_time: float | None = None
    job_id: str | None = None
    print_duration: float | None = None

    def to_dict(self) -> dict:
        """Plain dict for signals, containers deep-copied."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict, thumbnail_paths: list[str]) -> FileMetadata:
        """Create FileMetadata from Moonraker API response."""
        filename = data.get("filename", "")

        # Helper to safely get values with fallback
        def safe_get(key: str, default: typing.Any) -> typing.Any:
            value = data.get(key, default)
            if value is None or value == -1.0:
                return default
            return value

        return cls(
            filename=filename,
            thumbnail_paths=thumbnail_paths,
            filament_total=safe_get("filament_total", {}),
            estimated_time=int(safe_get("estimated_time", 0)),
            layer_count=safe_get("layer_count", -1),
            total_layer=safe_get("total_layer", -1),
            object_height=safe_get("object_height", -1.0),
            size=safe_get("size", 0),
            modified=safe_get("modified", 0.0),
            filament_type=safe_get("filament_type", "Unknown") or "Unknown",
            filament_weight_total=safe_get("filament_weight_total", -1.0),
            layer_height=safe_get("layer_height", -1.0),
            first_layer_height=safe_get("first_layer_height", -1.0),
            first_layer_extr_temp=safe_get("first_layer_extr_temp", -1.0),
            first_layer_bed_temp=safe_get("first_layer_bed_temp", -1.0),
            filament_name=safe_get("filament_name", "Unknown") or "Unknown",
            nozzle_diameter=safe_get("nozzle_diameter", -1.0),
            slicer=safe_get("slicer", "Unknown") or "Unknown",
            slicer_version=safe_get("slicer_version", "Unknown") or "Unknown",
            gcode_start_byte=safe_get("gcode_start_byte", 0),
            gcode_end_byte=safe_get("gcode_end_byte", 0),
            print_start_time=data.get("print_start_time"),
            job_id=data.get("job_id"),
            print_duration=data.get("print_duration"),
        )


class Files(QtCore.QObject):
    """Gcode file and dir state, synced from Moonraker notifications."""

    # Signals for API requests
    request_dir_info = QtCore.pyqtSignal(
        [], [str], [str, bool], name="api_get_dir_info"
    )
    request_file_metadata = QtCore.pyqtSignal(str, name="get_file_metadata")
    request_scan_metadata = QtCore.pyqtSignal(str, name="scan_file_metadata")

    # Signals for UI updates
    on_dirs = QtCore.pyqtSignal(list, name="on_dirs")
    on_file_list = QtCore.pyqtSignal(list, name="on_file_list")
    fileinfo = QtCore.pyqtSignal(dict, name="fileinfo")
    metadata_error = QtCore.pyqtSignal(
        str, name="metadata_error"
    )  # filename when metadata fails

    # Signals for incremental updates
    file_added = QtCore.pyqtSignal(dict, name="file_added")
    file_removed = QtCore.pyqtSignal(str, name="file_removed")
    file_modified = QtCore.pyqtSignal(dict, name="file_modified")
    dir_added = QtCore.pyqtSignal(dict, name="dir_added")
    dir_removed = QtCore.pyqtSignal(str, name="dir_removed")
    full_refresh_needed = QtCore.pyqtSignal(name="full_refresh_needed")
    # Hops history replies from the websocket thread to the Qt thread.
    _history_job = QtCore.pyqtSignal(str, str, dict, name="history_job")

    # Signal for preloaded USB files
    usb_files_loaded = QtCore.pyqtSignal(
        str, list, name="usb_files_loaded"
    )  # (usb_path, files)
    GCODE_EXTENSION = ".gcode"
    GCODE_PATH = "~/printer_data/gcodes"

    def __init__(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._metadata_retry_count: dict[str, int] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()
        # USB metadata: per-path size/modified, plus the lazy loader.
        self._usb_meta_base: dict[str, dict] = {}
        self._meta_loader: gcode_loader.GcodeMetadataLoader | None = None
        # job_id -> completed duration; None = asked or unusable, never re-ask.
        self._job_durations: dict[str, float | None] = {}

        self._connect_signals()
        self._install_event_filter()

    def _connect_signals(self) -> None:
        """Connect internal signals to websocket API."""
        self.request_dir_info.connect(self.ws.api.get_dir_information)
        self.request_dir_info[str, bool].connect(self.ws.api.get_dir_information)
        self.request_dir_info[str].connect(self.ws.api.get_dir_information)
        self.request_file_metadata.connect(self.ws.api.get_gcode_metadata)
        self.request_scan_metadata.connect(self.ws.api.scan_gcode_metadata)
        self._history_job.connect(self._on_history_job)

    def _install_event_filter(self) -> None:
        """Install event filter on application instance."""
        app = QtWidgets.QApplication.instance()
        if app:
            app.installEventFilter(self)

    @property
    def file_list(self) -> list[dict]:
        """Get list of files in current directory."""
        return list(self._files.values())

    @property
    def directories(self) -> list[dict]:
        """Get list of directories in current directory."""
        return list(self._directories.values())

    @property
    def current_directory(self) -> str:
        """Get current directory path."""
        return self._current_directory

    @current_directory.setter
    def current_directory(self, value: str) -> None:
        """Set current directory path."""
        self._current_directory = value

    def initial_load(self) -> None:
        """Perform initial load of file list."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("", True)

    def handle_filelist_changed(self, data: dict | list) -> None:
        """Handle notify_filelist_changed; params may batch entries."""
        if isinstance(data, dict) and "params" in data:
            data = data.get("params", [])
        entries = data if isinstance(data, list) else [data]
        for entry in entries:
            if isinstance(entry, dict):
                self._apply_filelist_change(entry)

    def _apply_filelist_change(self, data: dict) -> None:
        """Route one filelist entry to its handler."""
        action_str = data.get("action", "")
        action = FileAction.from_string(action_str)
        item = data.get("item", {})
        source_item = data.get("source_item", {})
        if not (self._in_gcodes(item) or self._in_gcodes(source_item)):
            return

        logger.debug(f"File list changed: action={action_str}, item={item}")

        handlers = {
            FileAction.CREATE_FILE: self._handle_file_created,
            FileAction.DELETE_FILE: self._handle_file_deleted,
            FileAction.MODIFY_FILE: self._handle_file_modified,
            FileAction.MOVE_FILE: self._handle_file_moved,
            FileAction.CREATE_DIR: self._handle_dir_created,
            FileAction.DELETE_DIR: self._handle_dir_deleted,
            FileAction.MOVE_DIR: self._handle_dir_moved,
            FileAction.ROOT_UPDATE: self._handle_root_update,
        }

        handler = handlers.get(action)
        if handler:
            handler(item, source_item)

    @staticmethod
    def _in_gcodes(item: dict) -> bool:
        """True for a gcodes-root item; config/logs roots notify too."""
        return bool(item) and item.get("root", "gcodes") == "gcodes"

    def _handle_file_created(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if helper_methods.is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_created(item, {})
            return

        if not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self._request_gcode_metadata(path.removeprefix("/"), item)
        logger.info(f"File created: {path}")

    def _handle_file_deleted(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if helper_methods.is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._forget_cached(path.removeprefix("/"))

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def _handle_file_modified(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path:
            return

        # Moonraker reports a root USB symlink as a file event.
        if helper_methods.is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_created(item, {})
            return

        if not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        # A same-name re-upload must not show the old parse.
        self._forget_cached(path.removeprefix("/"))
        # Before the request: the page drops its copy on this signal.
        self.file_modified.emit(item)
        self._request_gcode_metadata(path.removeprefix("/"), item)
        logger.info(f"File modified: {path}")

    def _handle_file_moved(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        # A cross-root move is only a delete or a create here.
        if self._in_gcodes(source_item):
            self._handle_file_deleted(source_item, {})
        if self._in_gcodes(item):
            self._handle_file_created(item, {})

    def _handle_dir_created(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "").strip("/")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        # Full path: a subdir folder named USB-* is not a mount.
        if helper_methods.is_usb_mount(path or dirname):
            self._preload_usb_contents(dirname)

    def _handle_dir_deleted(self, item: dict, _: dict) -> None:
        """Handle a deleted dir; emits its gcodes-relative path."""
        path = item.get("path", "").strip("/")
        dirname = item.get("dirname", "").strip("/")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)
        # A reinserted drive or recreated dir may hold different files.
        self._forget_cached(path or dirname)

        # Clear USB cache if this was a USB mount
        if helper_methods.is_usb_mount(path or dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        # Full path, so sub/x is not mistaken for a root x.
        self.dir_removed.emit(path or dirname)
        logger.info("Directory deleted: %s", path or dirname)

    def _forget_cached(self, path: str) -> None:
        """Drop cached metadata and loader payloads at or under *path*."""
        root = f"{path}/"
        for cache in (self._files_metadata, self._usb_meta_base):
            for key in [k for k in cache if f"{k}/".startswith(root)]:
                del cache[key]
        for loader in (gcode_loader.get_loader(), gcode_loader.get_metadata_loader()):
            if loader is not None:
                loader.forget(path)

    def _handle_dir_moved(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        if self._in_gcodes(source_item):
            self._handle_dir_deleted(source_item, {})
        if self._in_gcodes(item):
            self._handle_dir_created(item, {})

    def _handle_root_update(self, _: dict, __: dict) -> None:
        """Handle root update."""
        logger.info("Root update detected, requesting full refresh")
        self.full_refresh_needed.emit()
        self.initial_load()

    def handle_message_received(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.metadata" in method:
            self._process_metadata(data)
        elif "server.files.get_directory" in method:
            requested_dir = self._requested_dir_from_params(params)
            self._process_directory_info(data, requested_dir)

    def _requested_dir_from_params(self, params: typing.Any) -> str:
        """Dir asked for by a [method, params, callback] entry."""
        try:
            path = params[1].get("path", "")
        except (IndexError, TypeError, AttributeError):
            return ""
        return path.removeprefix("gcodes/").strip("/")

    def _full_gcode_path(self, filename: str, directory: str) -> str:
        """Gcodes-relative path of a bare listing filename."""
        bare = filename.removeprefix("/")
        parent = directory.removeprefix("/").strip("/")
        return f"{parent}/{bare}" if parent else bare

    def _process_metadata(self, data: dict, full_path: str | None = None) -> None:
        """Build FileMetadata and emit fileinfo."""
        if full_path:
            data = data | {"filename": full_path}
        filename = data.get("filename") or data.get("path")
        if not filename:
            return
        thumbs = [
            t
            for t in data.get("thumbnails") or []
            if isinstance(t, dict) and isinstance(t.get("relative_path"), str)
        ]
        # Consumers take [-1] as largest, as in KlipperScreen.
        thumbs.sort(key=lambda t: t.get("size") or 0)
        thumbnail_paths = [
            str(
                helper_methods.resolve_thumbnail_path(
                    self.gcode_path, filename, t["relative_path"]
                )
            )
            for t in thumbs
            if t["relative_path"]
        ]
        metadata = FileMetadata.from_dict(data, thumbnail_paths)
        duration = self._job_durations.get(str(metadata.job_id))
        if metadata.print_duration is None and duration is not None:
            metadata = replace(metadata, print_duration=duration)
        self._files_metadata[filename] = metadata
        self._metadata_retry_count.pop(filename.removeprefix("/"), None)
        self.fileinfo.emit(metadata.to_dict())
        logger.debug("Metadata loaded: %s", filename)

    @QtCore.pyqtSlot(str, name="request_print_duration")
    def request_print_duration(self, filename: str) -> None:
        """Fetch the file's last job duration from history, once."""
        filename = filename.removeprefix("/")
        metadata = self._files_metadata.get(filename)
        if metadata is None or not metadata.job_id:
            return
        job_id = str(metadata.job_id)
        if job_id in self._job_durations:
            return
        # Mark before sending: error replies skip the callback.
        self._job_durations[job_id] = None
        self.ws.api.history_get_job(
            job_id,
            lambda result, name=filename, uid=job_id: self._history_job.emit(
                name, uid, result or {}
            ),
        )

    @QtCore.pyqtSlot(str, str, dict, name="on_history_job")
    def _on_history_job(self, filename: str, job_id: str, result: dict) -> None:
        """Cache a completed job's duration and re-emit fileinfo."""
        job = result.get("job") or {}
        status = job.get("status")
        if status == "in_progress":
            self._job_durations.pop(job_id, None)
            return
        duration = job.get("print_duration")
        # Cancelled/errored runs stopped early; their time misleads.
        if status != "completed" or not isinstance(duration, (int, float)):
            return
        if duration <= 0:
            return
        self._job_durations[job_id] = float(duration)
        metadata = self._files_metadata.get(filename)
        if metadata is None or str(metadata.job_id) != job_id:
            return
        updated = replace(metadata, print_duration=float(duration))
        self._files_metadata[filename] = updated
        self.fileinfo.emit(updated.to_dict())

    @staticmethod
    def _has_inline_metadata(file_data: dict) -> bool:
        """True if a dir entry has real metadata, not only thumbnails."""
        return "estimated_time" in file_data

    def _is_cached(self, path: str, file_data: dict) -> bool:
        """True if *path* is cached at this entry's size and mtime."""
        cached = self._files_metadata.get(path)
        # Moonraker's own freshness test (FileManager._has_valid_data).
        return cached is not None and (cached.size, cached.modified) == (
            file_data.get("size"),
            file_data.get("modified"),
        )

    def _usb_metadata_loader(self) -> gcode_loader.GcodeMetadataLoader:
        """Create and wire the USB metadata loader on first use."""
        if self._meta_loader is None:
            loader = (
                gcode_loader.get_metadata_loader()
                or gcode_loader.configure_metadata(self.ws._moonRest)
            )
            loader.ready.connect(self._on_usb_metadata_ready)
            self._meta_loader = loader
        return self._meta_loader

    def _request_gcode_metadata(
        self, full_path: str, file_data: dict | None = None
    ) -> None:
        """Ask Moonraker, or parse USB gcodes locally (it can't scan them)."""
        if not helper_methods.is_usb_path(full_path):
            self.request_file_metadata.emit(full_path)
            return
        rel = full_path.removeprefix("/")
        if file_data:
            self._usb_meta_base[rel] = {
                "size": file_data.get("size", 0),
                "modified": file_data.get("modified", 0.0),
            }
        self._usb_metadata_loader().request(rel)

    @QtCore.pyqtSlot(str, dict)
    def _on_usb_metadata_ready(self, full_path: str, meta: dict) -> None:
        """Feed parsed USB metadata into the normal pipeline."""
        base = self._usb_meta_base.pop(full_path, {})
        self._process_metadata(base | meta, full_path)

    def handle_metadata_error(self, error_data: str | dict) -> None:
        """Retry the metadata scan named in a Moonraker error."""
        if not error_data:
            return

        if isinstance(error_data, dict):
            text = error_data.get("message", str(error_data))
        else:
            text = str(error_data)

        if "metadata" not in text.lower():
            return

        # Parse filename from error message (format: <filename>)
        start = text.find("<") + 1
        end = text.find(">", start)

        if start > 0 and end > start:
            self._retry_metadata_scan(text[start:end].removeprefix("/"))

    def _retry_metadata_scan(self, clean_filename: str) -> None:
        """Force a metadata rescan up to 3 times, then give up."""
        if not clean_filename.lower().endswith(self.GCODE_EXTENSION):
            return
        count = self._metadata_retry_count.get(clean_filename, 0)
        if count >= 3:
            self._metadata_retry_count.pop(clean_filename, None)
            self.metadata_error.emit(clean_filename)
            logger.debug("Metadata retry limit reached: %s", clean_filename)
            return
        self._metadata_retry_count[clean_filename] = count + 1
        self.request_scan_metadata.emit(clean_filename)
        logger.debug("Metadata rescan attempt %d: %s", count + 1, clean_filename)

    def _preload_usb_contents(self, usb_path: str) -> None:
        """Preload USB directory info when USB is inserted."""
        if usb_path in self._pending_usb_preloads:
            return  # a second reply would be taken as the shown listing
        logger.info(f"Preloading USB contents: {usb_path}")
        self._pending_usb_preloads.add(usb_path)
        self._usb_preload_queue.append(usb_path)
        self.ws.api.get_dir_information(usb_path, True)

    def _process_usb_directory_info(self, usb_path: str, data: dict) -> None:
        """Cache preloaded USB directory info and request metadata."""
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get("path", ""))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(
                    self.GCODE_EXTENSION
                ) and not self._is_cached(full_path, file_data):
                    self._request_gcode_metadata(full_path, file_data)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def _process_directory_info(self, data: dict, requested_dir: str = "") -> None:
        """Publish a directory listing and dispatch its gcode metadata."""
        matched_usb = self._match_usb_preload(requested_dir)
        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return
        self._populate_directory(data)
        self.on_file_list.emit(self.file_list)
        self.on_dirs.emit(self.directories)
        self._initial_load_complete = True
        logger.info(
            "Directory loaded: %d dirs, %d files",
            len(self._directories),
            len(self._files),
        )
        self._dispatch_metadata(requested_dir)

    def _match_usb_preload(self, requested_dir: str) -> str | None:
        """Pending USB preload matching this response, else None."""
        if not requested_dir or requested_dir not in self._pending_usb_preloads:
            return None
        if requested_dir in self._usb_preload_queue:
            self._usb_preload_queue.remove(requested_dir)
        return requested_dir

    def _populate_directory(self, data: dict) -> None:
        """Replace backing dir/file maps from a directory response."""
        self._directories.clear()
        self._files.clear()
        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("dirname", "")
            if dirname and not dirname.startswith("."):
                self._directories[dirname] = dir_data
        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get("path", ""))
            if not filename:
                continue
            # Moonraker lists USB symlinks as files; show them as dirs.
            if helper_methods.is_usb_mount(filename):
                self._directories[filename] = file_data | {"dirname": filename}
                continue
            self._files[filename] = file_data

    def _dispatch_metadata(self, requested_dir: str = "") -> None:
        """Process each new or changed gcode once; the page keeps the rest."""
        for filename, file_data in self._files.items():
            if not filename.lower().endswith(self.GCODE_EXTENSION):
                continue
            full = self._full_gcode_path(filename, requested_dir)
            if self._is_cached(full, file_data):
                continue
            if self._has_inline_metadata(file_data):
                self._process_metadata(file_data, full)
            else:
                self._request_gcode_metadata(full, file_data)

    @QtCore.pyqtSlot(str, str, name="on_request_delete_file")
    def on_request_delete_file(self, filename: str, directory: str = "gcodes") -> None:
        """Request deletion of a file."""
        if not filename:
            return

        if directory:
            self.ws.api.delete_file(filename, directory)
        else:
            self.ws.api.delete_file(filename)

        logger.info(f"Requested deletion of: {filename}")

    @QtCore.pyqtSlot(str, name="on_request_fileinfo")
    def on_request_fileinfo(self, filename: str) -> None:
        """Request and emit metadata for a file."""
        clean_filename = filename.removeprefix("/")
        cached = self._files_metadata.get(clean_filename)

        if cached:
            self.fileinfo.emit(cached.to_dict())
        else:
            self._request_gcode_metadata(clean_filename)

    @QtCore.pyqtSlot(name="get_dir_info")
    @QtCore.pyqtSlot(str, name="get_dir_info")
    @QtCore.pyqtSlot(str, bool, name="get_dir_info")
    def get_dir_information(
        self, directory: str = "", extended: bool = True
    ) -> typing.Any:
        """Get directory information."""
        self._current_directory = directory

        if not extended and self._initial_load_complete:
            return self.directories

        return self.ws.api.get_dir_information(directory, extended)

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Handle application-level events."""
        if event.type() == events.WebSocketOpen.type():
            self.initial_load()
            return False

        if event.type() == events.KlippyDisconnected.type():
            self._clear_all_data()
            return False

        return super().eventFilter(obj, event)

    def event(self, event: QtCore.QEvent) -> bool:
        """Handle object-level events."""
        if event.type() == events.ReceivedFileData.type():
            if isinstance(event, events.ReceivedFileData):
                self.handle_message_received(event.method, event.data, event.params)
                return True
        return super().event(event)

    def _clear_all_data(self) -> None:
        """Clear all cached data."""
        self._files.clear()
        self._directories.clear()
        self._files_metadata.clear()
        self._usb_files_cache.clear()
        self._pending_usb_preloads.clear()
        self._usb_preload_queue.clear()
        self._job_durations.clear()
        self._initial_load_complete = False
        logger.info("All file data cleared")
