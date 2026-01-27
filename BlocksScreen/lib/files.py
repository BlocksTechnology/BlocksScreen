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
    `Data class for file metadata.`

    All data comes from Moonraker API - no local filesystem access.
    Thumbnails are stored as ThumbnailInfo objects with paths that can
    be fetched via Moonraker's /server/files/gcodes/<path> endpoint.
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
    `Manages gcode files with event-driven updates.`

    Architecture:
    1. On WebSocket connection: requests full file list once via initial_load()
    2. On notify_filelist_changed: updates internal state incrementally
    3. Emits signals for UI components to react to changes

    Signals emitted:
    - on_dirs: Full directory list (for initial load)
    - on_file_list: Full file list (for initial load)
    - fileinfo: Single file metadata (when metadata is received)
    - file_added: Single file was added
    - file_removed: Single file was removed
    - file_modified: Single file was modified
    - dir_added: Single directory was added
    - dir_removed: Single directory was removed
    - full_refresh_needed: Root changed, need complete refresh
    """

    # Signals for API requests (to Moonraker)
    request_file_list = QtCore.pyqtSignal([], [str], name="api_get_files_list")
    request_dir_info = QtCore.pyqtSignal(
        [], [str], [str, bool], name="api_get_dir_info"
    )
    request_file_metadata = QtCore.pyqtSignal(str, name="get_file_metadata")
    request_thumbnail = QtCore.pyqtSignal(str, name="request_thumbnail")
    request_file_download = QtCore.pyqtSignal(str, str, name="file_download")

    # Signals for UI updates (full refresh)
    on_dirs = QtCore.pyqtSignal(list, name="on_dirs")
    on_file_list = QtCore.pyqtSignal(list, name="on_file_list")
    fileinfo = QtCore.pyqtSignal(dict, name="fileinfo")

    # Signals for incremental updates (event-driven)
    file_added = QtCore.pyqtSignal(dict, name="file_added")
    file_removed = QtCore.pyqtSignal(str, name="file_removed")
    file_modified = QtCore.pyqtSignal(dict, name="file_modified")
    dir_added = QtCore.pyqtSignal(dict, name="dir_added")
    dir_removed = QtCore.pyqtSignal(str, name="dir_removed")
    full_refresh_needed = QtCore.pyqtSignal(name="full_refresh_needed")

    # Constants
    GCODE_EXTENSION = ".gcode"
    GCODE_PATH = "~/printer_data/gcodes"

    def __init__(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state - use instance variables, not class variables!
        self._files: dict[str, dict] = {}  # filename -> file data
        self._directories: dict[str, dict] = {}  # dirname -> dir data
        self._files_metadata: dict[str, FileMetadata] = {}  # filename -> metadata
        self._current_directory: str = ""
        self._initial_load_complete: bool = False

        self.gcode_path = os.path.expanduser("~/printer_data/gcodes")

        self._connect_signals()
        QtWidgets.QApplication.instance().installEventFilter(self)  # type: ignore

    def _connect_signals(self) -> None:
        """Connect internal signals to websocket API."""
        self.request_file_list.connect(self.ws.api.get_file_list)
        self.request_file_list[str].connect(self.ws.api.get_file_list)
        self.request_dir_info.connect(self.ws.api.get_dir_information)
        self.request_dir_info[str, bool].connect(self.ws.api.get_dir_information)
        self.request_dir_info[str].connect(self.ws.api.get_dir_information)
        self.request_file_metadata.connect(self.ws.api.get_gcode_metadata)
        self.request_thumbnail.connect(self.ws.api.get_gcode_thumbnail)
        self.request_file_download.connect(self.ws.api.download_file)

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
        return self._files_metadata.get(filename)

    def get_file_data(self, filename: str) -> dict:
        """Get cached file data dict for a file."""
        clean_name = filename.removeprefix("/")
        metadata = self._files_metadata.get(clean_name)
        if metadata:
            return metadata.to_dict()
        return {}

    def refresh_directory(self, directory: str = "") -> None:
        """
        Force refresh of a specific directory.
        Use sparingly - prefer event-driven updates.
        """
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(directory, True)

    def initial_load(self) -> None:
        """Perform initial load of file list. Call once on connection."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("", True)

    def handle_filelist_changed(self, data: typing.Union[dict, list]) -> None:
        """
        Handle notify_filelist_changed from Moonraker.

        This is the main entry point for event-driven updates.
        Called from your websocket message handler when receiving
        'notify_filelist_changed' notifications.

        Args:
            data: The notification data from Moonraker (various formats supported).
        """
        # Handle nested "params" key (full JSON-RPC envelope)
        if isinstance(data, dict) and "params" in data:
            data = data.get("params", [])

        # Handle list format
        if isinstance(data, list):
            if len(data) > 0:
                data = data[0]
            else:
                logger.warning("Received empty list in filelist_changed")
                return

        # Validate we have a dict
        if not isinstance(data, dict):
            logger.warning(
                "Unexpected data type in filelist_changed: %s", type(data).__name__
            )
            return

        action_str = data.get("action", "")
        action = FileAction.from_string(action_str)
        item = data.get("item", {})
        source_item = data.get("source_item", {})

        logger.debug("File list changed: action=%s, item=%s", action_str, item)

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
        else:
            logger.warning("Unknown file action: %s", action_str)

    def _handle_file_created(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        # Check if this is actually a USB mount (Moonraker reports USB as files)
        # USB mounts: path like "USB-sda1" with no extension, at root level
        if self._is_usb_mount(path):
            # Treat as directory instead
            item["dirname"] = path
            self._handle_dir_created(item, {})
            return

        # Only process gcode files
        if not path.lower().endswith(self.GCODE_EXTENSION):
            return

        # Add to internal state
        self._files[path] = item

        # Emit signal for UI and request metadata
        self.file_added.emit(item)
        self.request_file_metadata.emit(path.removeprefix("/"))

        logger.info("File created: %s", path)

    def _handle_file_deleted(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        # Check if this is actually a USB mount being removed
        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        # Remove from internal state
        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        # Emit signal for UI
        self.file_removed.emit(path)
        logger.info("File deleted: %s", path)

    def _handle_file_modified(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        # Update internal state
        self._files[path] = item

        # Clear cached metadata and request fresh
        self._files_metadata.pop(path.removeprefix("/"), None)

        # Emit signal and request new metadata
        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info("File modified: %s", path)

    def _handle_file_moved(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "")

        # Remove from old location
        if old_path:
            self._handle_file_deleted(source_item, {})

        # Add to new location
        if new_path:
            self._handle_file_created(item, {})

        logger.info("File moved: %s -> %s", old_path, new_path)

    def _handle_dir_created(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        # Extract dirname from path if not provided
        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        # Ensure dirname is in item for UI
        item["dirname"] = dirname

        # Add to internal state
        self._directories[dirname] = item

        # Emit signal for UI
        self.dir_added.emit(item)
        logger.info("Directory created: %s", dirname)

    def _handle_dir_deleted(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        # Extract dirname from path if not provided
        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        # Remove from internal state
        self._directories.pop(dirname, None)

        # Emit signal for UI
        self.dir_removed.emit(dirname)
        logger.info("Directory deleted: %s", dirname)

    def _handle_dir_moved(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        self._handle_dir_deleted(source_item, {})
        self._handle_dir_created(item, {})

    def _handle_root_update(self, _: dict, __: dict) -> None:
        """Handle root update - requires full refresh."""
        logger.info("Root update detected, requesting full refresh")
        self.full_refresh_needed.emit()
        self.initial_load()

    @staticmethod
    def _is_usb_mount(path: str) -> bool:
        """
        Check if a path is a USB mount point.

        Moonraker incorrectly reports USB mounts as files with create_file/delete_file.
        USB mounts have paths like "USB-sda1" - starting with "USB-" and at root level.

        Args:
            path: The file path to check

        Returns:
            True if this appears to be a USB mount point
        """
        path = path.removeprefix("/")
        # USB mounts are at root level (no slashes) and start with "USB-"
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
                # Request metadata for each file
                self.request_file_metadata.emit(path.removeprefix("/"))

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info("Loaded %d files", len(self._files))

    def _process_metadata(self, data: dict) -> None:
        """Process file metadata response from Moonraker."""
        filename = data.get("filename")
        if not filename:
            return

        # Create metadata from Moonraker response (no local filesystem access)
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
        self.fileinfo.emit(metadata.to_dict())

    def _process_directory_info(self, data: dict) -> None:
        """Process directory info response."""
        self._directories.clear()
        self._files.clear()

        # Process directories
        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("dirname", "")
            if dirname and not dirname.startswith("."):
                self._directories[dirname] = dir_data

        # Process files
        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get("path", ""))
            if filename:
                self._files[filename] = file_data

        # Emit signals for UI
        self.on_file_list.emit(self.file_list)
        self.on_dirs.emit(self.directories)
        self._initial_load_complete = True

        logger.info(
            "Directory loaded: %d dirs, %d files",
            len(self._directories),
            len(self._files),
        )

    @QtCore.pyqtSlot(str, str, name="on_request_delete_file")
    def on_request_delete_file(self, filename: str, directory: str = "gcodes") -> None:
        """Request deletion of a file."""
        if not filename:
            logger.warning("Attempted to delete file with empty filename")
            return

        if directory:
            self.ws.api.delete_file(filename, directory)
        else:
            self.ws.api.delete_file(filename)

        logger.info("Requested deletion of: %s", filename)

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
        """Get directory information - from cache or request from Moonraker."""
        self._current_directory = directory

        if not extended and self._initial_load_complete:
            # Return cached data if available and extended info not needed
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
        self._initial_load_complete = False
        logger.info("All file data cleared")
