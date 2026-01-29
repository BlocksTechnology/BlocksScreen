from __future__ import annotations

import logging
import os
import typing
from dataclasses import dataclass, field
from enum import Enum, auto

import events
from events import ReceivedFileData
from lib.moonrakerComm import MoonWebSocket
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(__name__)


class FileAction(Enum):
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
    def from_string(cls, action: str) -> "FileAction":
        """Convert Moonraker action string to enum."""
        mapping = {
            "create_file": cls.CREATE_FILE,
            "delete_file": cls.DELETE_FILE,
            "move_file": cls.MOVE_FILE,
            "modify_file": cls.MODIFY_FILE,
            "create_dir": cls.CREATE_DIR,
            "delete_dir": cls.DELETE_DIR,
            "move_dir": cls.MOVE_DIR,
            "root_update": cls.ROOT_UPDATE,
        }
        return mapping.get(action.lower(), cls.UNKNOWN)


@dataclass
class FileMetadata:
    """
    Data class for file metadata.

    Thumbnails are stored as QImage objects when available.
    """

    filename: str = ""
    thumbnail_images: list[QtGui.QImage] = field(default_factory=list)
    filament_total: typing.Union[dict, str, float] = field(default_factory=dict)
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
    first_layer_extruder_temp: float = -1.0
    first_layer_bed_temp: float = -1.0
    chamber_temp: float = -1.0
    filament_name: str = "Unknown"
    nozzle_diameter: float = -1.0
    slicer: str = "Unknown"
    slicer_version: str = "Unknown"
    gcode_start_byte: int = 0
    gcode_end_byte: int = 0
    print_start_time: typing.Optional[float] = None
    job_id: typing.Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for signal emission."""
        return {
            "filename": self.filename,
            "thumbnail_images": self.thumbnail_images,
            "filament_total": self.filament_total,
            "estimated_time": self.estimated_time,
            "layer_count": self.layer_count,
            "total_layer": self.total_layer,
            "object_height": self.object_height,
            "size": self.size,
            "modified": self.modified,
            "filament_type": self.filament_type,
            "filament_weight_total": self.filament_weight_total,
            "layer_height": self.layer_height,
            "first_layer_height": self.first_layer_height,
            "first_layer_extruder_temp": self.first_layer_extruder_temp,
            "first_layer_bed_temp": self.first_layer_bed_temp,
            "chamber_temp": self.chamber_temp,
            "filament_name": self.filament_name,
            "nozzle_diameter": self.nozzle_diameter,
            "slicer": self.slicer,
            "slicer_version": self.slicer_version,
            "gcode_start_byte": self.gcode_start_byte,
            "gcode_end_byte": self.gcode_end_byte,
            "print_start_time": self.print_start_time,
            "job_id": self.job_id,
        }

    @classmethod
    def from_dict(
        cls, data: dict, thumbnail_images: list[QtGui.QImage]
    ) -> "FileMetadata":
        """
        `Create FileMetadata from Moonraker API response.`

        All data comes directly from Moonraker - no local filesystem access.
        """
        filename = data.get("filename", "")

        # Helper to safely get values with fallback
        def safe_get(key: str, default: typing.Any) -> typing.Any:
            value = data.get(key, default)
            if value is None or value == -1.0:
                return default
            return value

        return cls(
            filename=filename,
            thumbnail_images=thumbnail_images,
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
            first_layer_extruder_temp=safe_get("first_layer_extruder_temp", -1.0),
            first_layer_bed_temp=safe_get("first_layer_bed_temp", -1.0),
            chamber_temp=safe_get("chamber_temp", -1.0),
            filament_name=safe_get("filament_name", "Unknown") or "Unknown",
            nozzle_diameter=safe_get("nozzle_diameter", -1.0),
            slicer=safe_get("slicer", "Unknown") or "Unknown",
            slicer_version=safe_get("slicer_version", "Unknown") or "Unknown",
            gcode_start_byte=safe_get("gcode_start_byte", 0),
            gcode_end_byte=safe_get("gcode_end_byte", 0),
            print_start_time=data.get("print_start_time"),
            job_id=data.get("job_id"),
        )


class Files(QtCore.QObject):
    """
        Manages gcode files with event-driven updates.
    E
        Signals emitted:
        - on_dirs: Full directory list
        - on_file_list: Full file list
        - fileinfo: Single file metadata update
        - file_added/removed/modified: Incremental updates
        - dir_added/removed: Directory updates
        - full_refresh_needed: Root changed
    """

    # Signals for API requests
    request_file_list = QtCore.pyqtSignal([], [str], name="api_get_files_list")
    request_dir_info = QtCore.pyqtSignal(
        [], [str], [str, bool], name="api_get_dir_info"
    )
    request_file_metadata = QtCore.pyqtSignal(str, name="get_file_metadata")

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
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = os.path.expanduser(self.GCODE_PATH)
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests
        self._pending_usb_preloads: set[str] = set()
        # Track the last USB preload request for response matching
        self._last_usb_preload_request: str = ""

        self._connect_signals()
        self._install_event_filter()

    def _connect_signals(self) -> None:
        """Connect internal signals to websocket API."""
        self.request_file_list.connect(self.ws.api.get_file_list)
        self.request_file_list[str].connect(self.ws.api.get_file_list)
        self.request_dir_info.connect(self.ws.api.get_dir_information)
        self.request_dir_info[str, bool].connect(self.ws.api.get_dir_information)
        self.request_dir_info[str].connect(self.ws.api.get_dir_information)
        self.request_file_metadata.connect(self.ws.api.get_gcode_metadata)

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

    @property
    def is_loaded(self) -> bool:
        """Check if initial load is complete."""
        return self._initial_load_complete

    def get_file_metadata(self, filename: str) -> typing.Optional[FileMetadata]:
        """Get cached metadata for a file."""
        return self._files_metadata.get(filename.removeprefix("/"))

    def get_file_data(self, filename: str) -> dict:
        """Get cached file data dict for a file."""
        clean_name = filename.removeprefix("/")
        metadata = self._files_metadata.get(clean_name)
        if metadata:
            return metadata.to_dict()
        return {}

    def refresh_directory(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory or 'root'}")
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(directory, True)

    def initial_load(self) -> None:
        """Perform initial load of file list."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("", True)

    def handle_filelist_changed(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get("params", [])

        if isinstance(data, list):
            if len(data) > 0:
                data = data[0]
            else:
                return

        if not isinstance(data, dict):
            return

        action_str = data.get("action", "")
        action = FileAction.from_string(action_str)
        item = data.get("item", {})
        source_item = data.get("source_item", {})

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

    def _handle_file_created(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_created(item, {})
            return

        if not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def _handle_file_deleted(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def _handle_file_modified(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def _handle_file_moved(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def _handle_dir_created(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def _handle_dir_deleted(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def _handle_dir_moved(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        self._handle_dir_deleted(source_item, {})
        self._handle_dir_created(item, {})

    def _handle_root_update(self, _: dict, __: dict) -> None:
        """Handle root update."""
        logger.info("Root update detected, requesting full refresh")
        self.full_refresh_needed.emit()
        self.initial_load()

    @staticmethod
    def _is_usb_mount(path: str) -> bool:
        """Check if a path is a USB mount point."""
        path = path.removeprefix("/")
        return "/" not in path and path.startswith("USB-")

    def handle_message_received(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" in method:
            self._process_file_list(data)
        elif "server.files.metadata" in method:
            self._process_metadata(data)
        elif "server.files.get_directory" in method:
            self._process_directory_info(data)

    def _process_file_list(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get("filename", ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def _process_metadata(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = os.path.dirname(os.path.join(self.gcode_path, filename))
        thumbnail_paths = [
            os.path.join(base_dir, t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["relative_path"]
        ]

        # Load images, filtering out invalid files
        thumbnail_images = []
        for path in thumbnail_paths:
            image = QtGui.QImage(path)
            if not image.isNull():  # skip loading errors
                thumbnail_images.append(image)

        metadata = FileMetadata.from_dict(data, thumbnail_images)
        self._files_metadata[filename] = metadata

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def handle_metadata_error(self, error_data: typing.Union[str, dict]) -> None:
        """
        Handle metadata request error from Moonraker.

        Parses the filename from the error message and emits metadata_error signal.
        Called directly from MainWindow error handler.

        Args:
            error_data: The error message string or dict from Moonraker
        """
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
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def _preload_usb_contents(self, usb_path: str) -> None:
        """
        Preload USB contents when USB is inserted.

        Requests directory info for the USB mount so files are ready
        when user navigates to it.

        Args:
            usb_path: The USB mount path (e.g., "USB-sda1")
        """
        logger.info(f"Preloading USB contents: {usb_path}")
        self._pending_usb_preloads.add(usb_path)
        # Store which USB we're preloading (for response matching)
        self._last_usb_preload_request = usb_path
        self.ws.api.get_dir_information(usb_path, True)

    def get_cached_usb_files(self, usb_path: str) -> typing.Optional[list[dict]]:
        """
        Get cached files for a USB path if available.

        Args:
            usb_path: The USB mount path

        Returns:
            List of file dicts if cached, None otherwise
        """
        return self._usb_files_cache.get(usb_path.removeprefix("/"))

    def _process_usb_directory_info(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get("path", ""))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def _process_directory_info(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response
        matched_usb = None

        if self._pending_usb_preloads:
            # Check if this response matches last USB preload request
            if self._last_usb_preload_request in self._pending_usb_preloads:
                matched_usb = self._last_usb_preload_request
                self._last_usb_preload_request = ""
            else:
                # Fallback: check root_info for USB marker
                root_info = data.get("root_info", {})
                root_name = root_info.get("name", "")
                for usb_path in list(self._pending_usb_preloads):
                    if root_name.startswith("USB-") or usb_path in root_name:
                        matched_usb = usb_path
                        break

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("dirname", "")
            if dirname and not dirname.startswith("."):
                self._directories[dirname] = dir_data

        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get("path", ""))
            if filename:
                self._files[filename] = file_data

        self.on_file_list.emit(self.file_list)
        self.on_dirs.emit(self.directories)
        self._initial_load_complete = True

        logger.info(
            f"Directory loaded: {len(self._directories)} dirs, {len(self._files)} files"
        )

        # Request metadata only for gcode files (async update)
        for filename in self._files:
            if filename.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(filename.removeprefix("/"))

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
            self.request_file_metadata.emit(clean_filename)

    @QtCore.pyqtSlot(name="get_dir_info")
    @QtCore.pyqtSlot(str, name="get_dir_info")
    @QtCore.pyqtSlot(str, bool, name="get_dir_info")
    def get_dir_information(
        self, directory: str = "", extended: bool = True
    ) -> typing.Optional[list]:
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
        if event.type() == ReceivedFileData.type():
            if isinstance(event, ReceivedFileData):
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
        self._last_usb_preload_request = ""
        self._initial_load_complete = False
        logger.info("All file data cleared")
