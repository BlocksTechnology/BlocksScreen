from __future__ import annotations

import logging
import typing
from collections import deque
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path

import events
from events import ReceivedFileData
from lib.moonrakerComm import MoonWebSocket
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(__name__)
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


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
        args = [parent, ws]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ__init____mutmut_orig(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_1(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(None)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_2(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = None

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_3(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = None
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_4(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = None
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_5(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = None
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_6(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = None
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_7(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = "XXXX"
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_8(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = None
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_9(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = True
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_10(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = None
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_11(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = Path(None).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_12(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = None
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_13(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = None
        self._usb_preload_queue: deque[str] = deque()

        self._connect_signals()
        self._install_event_filter()

    def xǁFilesǁ__init____mutmut_14(self, parent: QtCore.QObject, ws: MoonWebSocket) -> None:
        super().__init__(parent)
        self.ws = ws

        # Internal state
        self._files: dict[str, dict] = {}
        self._directories: dict[str, dict] = {}
        self._files_metadata: dict[str, FileMetadata] = {}
        self._current_directory: str = ""
        self._initial_load_complete: bool = False
        self.gcode_path = Path(self.GCODE_PATH).expanduser()
        # USB preloaded files cache: usb_path -> list of files
        self._usb_files_cache: dict[str, list[dict]] = {}
        # Track pending USB preload requests (ordered FIFO queue)
        self._pending_usb_preloads: set[str] = set()
        self._usb_preload_queue: deque[str] = None

        self._connect_signals()
        self._install_event_filter()
    
    xǁFilesǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ__init____mutmut_1': xǁFilesǁ__init____mutmut_1, 
        'xǁFilesǁ__init____mutmut_2': xǁFilesǁ__init____mutmut_2, 
        'xǁFilesǁ__init____mutmut_3': xǁFilesǁ__init____mutmut_3, 
        'xǁFilesǁ__init____mutmut_4': xǁFilesǁ__init____mutmut_4, 
        'xǁFilesǁ__init____mutmut_5': xǁFilesǁ__init____mutmut_5, 
        'xǁFilesǁ__init____mutmut_6': xǁFilesǁ__init____mutmut_6, 
        'xǁFilesǁ__init____mutmut_7': xǁFilesǁ__init____mutmut_7, 
        'xǁFilesǁ__init____mutmut_8': xǁFilesǁ__init____mutmut_8, 
        'xǁFilesǁ__init____mutmut_9': xǁFilesǁ__init____mutmut_9, 
        'xǁFilesǁ__init____mutmut_10': xǁFilesǁ__init____mutmut_10, 
        'xǁFilesǁ__init____mutmut_11': xǁFilesǁ__init____mutmut_11, 
        'xǁFilesǁ__init____mutmut_12': xǁFilesǁ__init____mutmut_12, 
        'xǁFilesǁ__init____mutmut_13': xǁFilesǁ__init____mutmut_13, 
        'xǁFilesǁ__init____mutmut_14': xǁFilesǁ__init____mutmut_14
    }
    xǁFilesǁ__init____mutmut_orig.__name__ = 'xǁFilesǁ__init__'

    def _connect_signals(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_connect_signals__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_connect_signals__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_connect_signals__mutmut_orig(self) -> None:
        """Connect internal signals to websocket API."""
        self.request_file_list.connect(self.ws.api.get_file_list)
        self.request_file_list[str].connect(self.ws.api.get_file_list)
        self.request_dir_info.connect(self.ws.api.get_dir_information)
        self.request_dir_info[str, bool].connect(self.ws.api.get_dir_information)
        self.request_dir_info[str].connect(self.ws.api.get_dir_information)
        self.request_file_metadata.connect(self.ws.api.get_gcode_metadata)

    def xǁFilesǁ_connect_signals__mutmut_1(self) -> None:
        """Connect internal signals to websocket API."""
        self.request_file_list.connect(None)
        self.request_file_list[str].connect(self.ws.api.get_file_list)
        self.request_dir_info.connect(self.ws.api.get_dir_information)
        self.request_dir_info[str, bool].connect(self.ws.api.get_dir_information)
        self.request_dir_info[str].connect(self.ws.api.get_dir_information)
        self.request_file_metadata.connect(self.ws.api.get_gcode_metadata)

    def xǁFilesǁ_connect_signals__mutmut_2(self) -> None:
        """Connect internal signals to websocket API."""
        self.request_file_list.connect(self.ws.api.get_file_list)
        self.request_file_list[str].connect(None)
        self.request_dir_info.connect(self.ws.api.get_dir_information)
        self.request_dir_info[str, bool].connect(self.ws.api.get_dir_information)
        self.request_dir_info[str].connect(self.ws.api.get_dir_information)
        self.request_file_metadata.connect(self.ws.api.get_gcode_metadata)

    def xǁFilesǁ_connect_signals__mutmut_3(self) -> None:
        """Connect internal signals to websocket API."""
        self.request_file_list.connect(self.ws.api.get_file_list)
        self.request_file_list[str].connect(self.ws.api.get_file_list)
        self.request_dir_info.connect(None)
        self.request_dir_info[str, bool].connect(self.ws.api.get_dir_information)
        self.request_dir_info[str].connect(self.ws.api.get_dir_information)
        self.request_file_metadata.connect(self.ws.api.get_gcode_metadata)

    def xǁFilesǁ_connect_signals__mutmut_4(self) -> None:
        """Connect internal signals to websocket API."""
        self.request_file_list.connect(self.ws.api.get_file_list)
        self.request_file_list[str].connect(self.ws.api.get_file_list)
        self.request_dir_info.connect(self.ws.api.get_dir_information)
        self.request_dir_info[str, bool].connect(None)
        self.request_dir_info[str].connect(self.ws.api.get_dir_information)
        self.request_file_metadata.connect(self.ws.api.get_gcode_metadata)

    def xǁFilesǁ_connect_signals__mutmut_5(self) -> None:
        """Connect internal signals to websocket API."""
        self.request_file_list.connect(self.ws.api.get_file_list)
        self.request_file_list[str].connect(self.ws.api.get_file_list)
        self.request_dir_info.connect(self.ws.api.get_dir_information)
        self.request_dir_info[str, bool].connect(self.ws.api.get_dir_information)
        self.request_dir_info[str].connect(None)
        self.request_file_metadata.connect(self.ws.api.get_gcode_metadata)

    def xǁFilesǁ_connect_signals__mutmut_6(self) -> None:
        """Connect internal signals to websocket API."""
        self.request_file_list.connect(self.ws.api.get_file_list)
        self.request_file_list[str].connect(self.ws.api.get_file_list)
        self.request_dir_info.connect(self.ws.api.get_dir_information)
        self.request_dir_info[str, bool].connect(self.ws.api.get_dir_information)
        self.request_dir_info[str].connect(self.ws.api.get_dir_information)
        self.request_file_metadata.connect(None)
    
    xǁFilesǁ_connect_signals__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_connect_signals__mutmut_1': xǁFilesǁ_connect_signals__mutmut_1, 
        'xǁFilesǁ_connect_signals__mutmut_2': xǁFilesǁ_connect_signals__mutmut_2, 
        'xǁFilesǁ_connect_signals__mutmut_3': xǁFilesǁ_connect_signals__mutmut_3, 
        'xǁFilesǁ_connect_signals__mutmut_4': xǁFilesǁ_connect_signals__mutmut_4, 
        'xǁFilesǁ_connect_signals__mutmut_5': xǁFilesǁ_connect_signals__mutmut_5, 
        'xǁFilesǁ_connect_signals__mutmut_6': xǁFilesǁ_connect_signals__mutmut_6
    }
    xǁFilesǁ_connect_signals__mutmut_orig.__name__ = 'xǁFilesǁ_connect_signals'

    def _install_event_filter(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_install_event_filter__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_install_event_filter__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_install_event_filter__mutmut_orig(self) -> None:
        """Install event filter on application instance."""
        app = QtWidgets.QApplication.instance()
        if app:
            app.installEventFilter(self)

    def xǁFilesǁ_install_event_filter__mutmut_1(self) -> None:
        """Install event filter on application instance."""
        app = None
        if app:
            app.installEventFilter(self)

    def xǁFilesǁ_install_event_filter__mutmut_2(self) -> None:
        """Install event filter on application instance."""
        app = QtWidgets.QApplication.instance()
        if app:
            app.installEventFilter(None)
    
    xǁFilesǁ_install_event_filter__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_install_event_filter__mutmut_1': xǁFilesǁ_install_event_filter__mutmut_1, 
        'xǁFilesǁ_install_event_filter__mutmut_2': xǁFilesǁ_install_event_filter__mutmut_2
    }
    xǁFilesǁ_install_event_filter__mutmut_orig.__name__ = 'xǁFilesǁ_install_event_filter'

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
        args = [filename]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁget_file_metadata__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁget_file_metadata__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁget_file_metadata__mutmut_orig(self, filename: str) -> typing.Optional[FileMetadata]:
        """Get cached metadata for a file."""
        return self._files_metadata.get(filename.removeprefix("/"))

    def xǁFilesǁget_file_metadata__mutmut_1(self, filename: str) -> typing.Optional[FileMetadata]:
        """Get cached metadata for a file."""
        return self._files_metadata.get(None)

    def xǁFilesǁget_file_metadata__mutmut_2(self, filename: str) -> typing.Optional[FileMetadata]:
        """Get cached metadata for a file."""
        return self._files_metadata.get(filename.removeprefix(None))

    def xǁFilesǁget_file_metadata__mutmut_3(self, filename: str) -> typing.Optional[FileMetadata]:
        """Get cached metadata for a file."""
        return self._files_metadata.get(filename.removesuffix("/"))

    def xǁFilesǁget_file_metadata__mutmut_4(self, filename: str) -> typing.Optional[FileMetadata]:
        """Get cached metadata for a file."""
        return self._files_metadata.get(filename.removeprefix("XX/XX"))
    
    xǁFilesǁget_file_metadata__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁget_file_metadata__mutmut_1': xǁFilesǁget_file_metadata__mutmut_1, 
        'xǁFilesǁget_file_metadata__mutmut_2': xǁFilesǁget_file_metadata__mutmut_2, 
        'xǁFilesǁget_file_metadata__mutmut_3': xǁFilesǁget_file_metadata__mutmut_3, 
        'xǁFilesǁget_file_metadata__mutmut_4': xǁFilesǁget_file_metadata__mutmut_4
    }
    xǁFilesǁget_file_metadata__mutmut_orig.__name__ = 'xǁFilesǁget_file_metadata'

    def get_file_data(self, filename: str) -> dict:
        args = [filename]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁget_file_data__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁget_file_data__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁget_file_data__mutmut_orig(self, filename: str) -> dict:
        """Get cached file data dict for a file."""
        clean_name = filename.removeprefix("/")
        metadata = self._files_metadata.get(clean_name)
        if metadata:
            return metadata.to_dict()
        return {}

    def xǁFilesǁget_file_data__mutmut_1(self, filename: str) -> dict:
        """Get cached file data dict for a file."""
        clean_name = None
        metadata = self._files_metadata.get(clean_name)
        if metadata:
            return metadata.to_dict()
        return {}

    def xǁFilesǁget_file_data__mutmut_2(self, filename: str) -> dict:
        """Get cached file data dict for a file."""
        clean_name = filename.removeprefix(None)
        metadata = self._files_metadata.get(clean_name)
        if metadata:
            return metadata.to_dict()
        return {}

    def xǁFilesǁget_file_data__mutmut_3(self, filename: str) -> dict:
        """Get cached file data dict for a file."""
        clean_name = filename.removesuffix("/")
        metadata = self._files_metadata.get(clean_name)
        if metadata:
            return metadata.to_dict()
        return {}

    def xǁFilesǁget_file_data__mutmut_4(self, filename: str) -> dict:
        """Get cached file data dict for a file."""
        clean_name = filename.removeprefix("XX/XX")
        metadata = self._files_metadata.get(clean_name)
        if metadata:
            return metadata.to_dict()
        return {}

    def xǁFilesǁget_file_data__mutmut_5(self, filename: str) -> dict:
        """Get cached file data dict for a file."""
        clean_name = filename.removeprefix("/")
        metadata = None
        if metadata:
            return metadata.to_dict()
        return {}

    def xǁFilesǁget_file_data__mutmut_6(self, filename: str) -> dict:
        """Get cached file data dict for a file."""
        clean_name = filename.removeprefix("/")
        metadata = self._files_metadata.get(None)
        if metadata:
            return metadata.to_dict()
        return {}
    
    xǁFilesǁget_file_data__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁget_file_data__mutmut_1': xǁFilesǁget_file_data__mutmut_1, 
        'xǁFilesǁget_file_data__mutmut_2': xǁFilesǁget_file_data__mutmut_2, 
        'xǁFilesǁget_file_data__mutmut_3': xǁFilesǁget_file_data__mutmut_3, 
        'xǁFilesǁget_file_data__mutmut_4': xǁFilesǁget_file_data__mutmut_4, 
        'xǁFilesǁget_file_data__mutmut_5': xǁFilesǁget_file_data__mutmut_5, 
        'xǁFilesǁget_file_data__mutmut_6': xǁFilesǁget_file_data__mutmut_6
    }
    xǁFilesǁget_file_data__mutmut_orig.__name__ = 'xǁFilesǁget_file_data'

    def refresh_directory(self, directory: str = "") -> None:
        args = [directory]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁrefresh_directory__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁrefresh_directory__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁrefresh_directory__mutmut_orig(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory or 'root'}")
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(directory, True)

    def xǁFilesǁrefresh_directory__mutmut_1(self, directory: str = "XXXX") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory or 'root'}")
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(directory, True)

    def xǁFilesǁrefresh_directory__mutmut_2(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(None)
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(directory, True)

    def xǁFilesǁrefresh_directory__mutmut_3(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory and 'root'}")
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(directory, True)

    def xǁFilesǁrefresh_directory__mutmut_4(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory or 'XXrootXX'}")
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(directory, True)

    def xǁFilesǁrefresh_directory__mutmut_5(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory or 'ROOT'}")
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(directory, True)

    def xǁFilesǁrefresh_directory__mutmut_6(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory or 'root'}")
        self._current_directory = None
        self.request_dir_info[str, bool].emit(directory, True)

    def xǁFilesǁrefresh_directory__mutmut_7(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory or 'root'}")
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(None, True)

    def xǁFilesǁrefresh_directory__mutmut_8(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory or 'root'}")
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(directory, None)

    def xǁFilesǁrefresh_directory__mutmut_9(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory or 'root'}")
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(True)

    def xǁFilesǁrefresh_directory__mutmut_10(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory or 'root'}")
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(directory, )

    def xǁFilesǁrefresh_directory__mutmut_11(self, directory: str = "") -> None:
        """Force refresh of a specific directory."""
        logger.debug(f"Refreshing directory: {directory or 'root'}")
        self._current_directory = directory
        self.request_dir_info[str, bool].emit(directory, False)
    
    xǁFilesǁrefresh_directory__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁrefresh_directory__mutmut_1': xǁFilesǁrefresh_directory__mutmut_1, 
        'xǁFilesǁrefresh_directory__mutmut_2': xǁFilesǁrefresh_directory__mutmut_2, 
        'xǁFilesǁrefresh_directory__mutmut_3': xǁFilesǁrefresh_directory__mutmut_3, 
        'xǁFilesǁrefresh_directory__mutmut_4': xǁFilesǁrefresh_directory__mutmut_4, 
        'xǁFilesǁrefresh_directory__mutmut_5': xǁFilesǁrefresh_directory__mutmut_5, 
        'xǁFilesǁrefresh_directory__mutmut_6': xǁFilesǁrefresh_directory__mutmut_6, 
        'xǁFilesǁrefresh_directory__mutmut_7': xǁFilesǁrefresh_directory__mutmut_7, 
        'xǁFilesǁrefresh_directory__mutmut_8': xǁFilesǁrefresh_directory__mutmut_8, 
        'xǁFilesǁrefresh_directory__mutmut_9': xǁFilesǁrefresh_directory__mutmut_9, 
        'xǁFilesǁrefresh_directory__mutmut_10': xǁFilesǁrefresh_directory__mutmut_10, 
        'xǁFilesǁrefresh_directory__mutmut_11': xǁFilesǁrefresh_directory__mutmut_11
    }
    xǁFilesǁrefresh_directory__mutmut_orig.__name__ = 'xǁFilesǁrefresh_directory'

    def initial_load(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁinitial_load__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁinitial_load__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁinitial_load__mutmut_orig(self) -> None:
        """Perform initial load of file list."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("", True)

    def xǁFilesǁinitial_load__mutmut_1(self) -> None:
        """Perform initial load of file list."""
        logger.info(None)
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("", True)

    def xǁFilesǁinitial_load__mutmut_2(self) -> None:
        """Perform initial load of file list."""
        logger.info("XXPerforming initial file list loadXX")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("", True)

    def xǁFilesǁinitial_load__mutmut_3(self) -> None:
        """Perform initial load of file list."""
        logger.info("performing initial file list load")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("", True)

    def xǁFilesǁinitial_load__mutmut_4(self) -> None:
        """Perform initial load of file list."""
        logger.info("PERFORMING INITIAL FILE LIST LOAD")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("", True)

    def xǁFilesǁinitial_load__mutmut_5(self) -> None:
        """Perform initial load of file list."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = None
        self.request_dir_info[str, bool].emit("", True)

    def xǁFilesǁinitial_load__mutmut_6(self) -> None:
        """Perform initial load of file list."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = True
        self.request_dir_info[str, bool].emit("", True)

    def xǁFilesǁinitial_load__mutmut_7(self) -> None:
        """Perform initial load of file list."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit(None, True)

    def xǁFilesǁinitial_load__mutmut_8(self) -> None:
        """Perform initial load of file list."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("", None)

    def xǁFilesǁinitial_load__mutmut_9(self) -> None:
        """Perform initial load of file list."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit(True)

    def xǁFilesǁinitial_load__mutmut_10(self) -> None:
        """Perform initial load of file list."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("", )

    def xǁFilesǁinitial_load__mutmut_11(self) -> None:
        """Perform initial load of file list."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("XXXX", True)

    def xǁFilesǁinitial_load__mutmut_12(self) -> None:
        """Perform initial load of file list."""
        logger.info("Performing initial file list load")
        self._initial_load_complete = False
        self.request_dir_info[str, bool].emit("", False)
    
    xǁFilesǁinitial_load__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁinitial_load__mutmut_1': xǁFilesǁinitial_load__mutmut_1, 
        'xǁFilesǁinitial_load__mutmut_2': xǁFilesǁinitial_load__mutmut_2, 
        'xǁFilesǁinitial_load__mutmut_3': xǁFilesǁinitial_load__mutmut_3, 
        'xǁFilesǁinitial_load__mutmut_4': xǁFilesǁinitial_load__mutmut_4, 
        'xǁFilesǁinitial_load__mutmut_5': xǁFilesǁinitial_load__mutmut_5, 
        'xǁFilesǁinitial_load__mutmut_6': xǁFilesǁinitial_load__mutmut_6, 
        'xǁFilesǁinitial_load__mutmut_7': xǁFilesǁinitial_load__mutmut_7, 
        'xǁFilesǁinitial_load__mutmut_8': xǁFilesǁinitial_load__mutmut_8, 
        'xǁFilesǁinitial_load__mutmut_9': xǁFilesǁinitial_load__mutmut_9, 
        'xǁFilesǁinitial_load__mutmut_10': xǁFilesǁinitial_load__mutmut_10, 
        'xǁFilesǁinitial_load__mutmut_11': xǁFilesǁinitial_load__mutmut_11, 
        'xǁFilesǁinitial_load__mutmut_12': xǁFilesǁinitial_load__mutmut_12
    }
    xǁFilesǁinitial_load__mutmut_orig.__name__ = 'xǁFilesǁinitial_load'

    def handle_filelist_changed(self, data: typing.Union[dict, list]) -> None:
        args = [data]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁhandle_filelist_changed__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁhandle_filelist_changed__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁhandle_filelist_changed__mutmut_orig(self, data: typing.Union[dict, list]) -> None:
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

    def xǁFilesǁhandle_filelist_changed__mutmut_1(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) or "params" in data:
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

    def xǁFilesǁhandle_filelist_changed__mutmut_2(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "XXparamsXX" in data:
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

    def xǁFilesǁhandle_filelist_changed__mutmut_3(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "PARAMS" in data:
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

    def xǁFilesǁhandle_filelist_changed__mutmut_4(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" not in data:
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

    def xǁFilesǁhandle_filelist_changed__mutmut_5(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = None

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

    def xǁFilesǁhandle_filelist_changed__mutmut_6(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get(None, [])

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

    def xǁFilesǁhandle_filelist_changed__mutmut_7(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get("params", None)

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

    def xǁFilesǁhandle_filelist_changed__mutmut_8(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get([])

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

    def xǁFilesǁhandle_filelist_changed__mutmut_9(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get("params", )

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

    def xǁFilesǁhandle_filelist_changed__mutmut_10(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get("XXparamsXX", [])

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

    def xǁFilesǁhandle_filelist_changed__mutmut_11(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get("PARAMS", [])

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

    def xǁFilesǁhandle_filelist_changed__mutmut_12(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get("params", [])

        if isinstance(data, list):
            if len(data) >= 0:
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

    def xǁFilesǁhandle_filelist_changed__mutmut_13(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get("params", [])

        if isinstance(data, list):
            if len(data) > 1:
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

    def xǁFilesǁhandle_filelist_changed__mutmut_14(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get("params", [])

        if isinstance(data, list):
            if len(data) > 0:
                data = None
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

    def xǁFilesǁhandle_filelist_changed__mutmut_15(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get("params", [])

        if isinstance(data, list):
            if len(data) > 0:
                data = data[1]
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

    def xǁFilesǁhandle_filelist_changed__mutmut_16(self, data: typing.Union[dict, list]) -> None:
        """Handle notify_filelist_changed from Moonraker."""
        if isinstance(data, dict) and "params" in data:
            data = data.get("params", [])

        if isinstance(data, list):
            if len(data) > 0:
                data = data[0]
            else:
                return

        if isinstance(data, dict):
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

    def xǁFilesǁhandle_filelist_changed__mutmut_17(self, data: typing.Union[dict, list]) -> None:
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

        action_str = None
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

    def xǁFilesǁhandle_filelist_changed__mutmut_18(self, data: typing.Union[dict, list]) -> None:
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

        action_str = data.get(None, "")
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

    def xǁFilesǁhandle_filelist_changed__mutmut_19(self, data: typing.Union[dict, list]) -> None:
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

        action_str = data.get("action", None)
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

    def xǁFilesǁhandle_filelist_changed__mutmut_20(self, data: typing.Union[dict, list]) -> None:
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

        action_str = data.get("")
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

    def xǁFilesǁhandle_filelist_changed__mutmut_21(self, data: typing.Union[dict, list]) -> None:
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

        action_str = data.get("action", )
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

    def xǁFilesǁhandle_filelist_changed__mutmut_22(self, data: typing.Union[dict, list]) -> None:
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

        action_str = data.get("XXactionXX", "")
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

    def xǁFilesǁhandle_filelist_changed__mutmut_23(self, data: typing.Union[dict, list]) -> None:
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

        action_str = data.get("ACTION", "")
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

    def xǁFilesǁhandle_filelist_changed__mutmut_24(self, data: typing.Union[dict, list]) -> None:
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

        action_str = data.get("action", "XXXX")
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

    def xǁFilesǁhandle_filelist_changed__mutmut_25(self, data: typing.Union[dict, list]) -> None:
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
        action = None
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

    def xǁFilesǁhandle_filelist_changed__mutmut_26(self, data: typing.Union[dict, list]) -> None:
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
        action = FileAction.from_string(None)
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

    def xǁFilesǁhandle_filelist_changed__mutmut_27(self, data: typing.Union[dict, list]) -> None:
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
        item = None
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

    def xǁFilesǁhandle_filelist_changed__mutmut_28(self, data: typing.Union[dict, list]) -> None:
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
        item = data.get(None, {})
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

    def xǁFilesǁhandle_filelist_changed__mutmut_29(self, data: typing.Union[dict, list]) -> None:
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
        item = data.get("item", None)
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

    def xǁFilesǁhandle_filelist_changed__mutmut_30(self, data: typing.Union[dict, list]) -> None:
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
        item = data.get({})
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

    def xǁFilesǁhandle_filelist_changed__mutmut_31(self, data: typing.Union[dict, list]) -> None:
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
        item = data.get("item", )
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

    def xǁFilesǁhandle_filelist_changed__mutmut_32(self, data: typing.Union[dict, list]) -> None:
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
        item = data.get("XXitemXX", {})
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

    def xǁFilesǁhandle_filelist_changed__mutmut_33(self, data: typing.Union[dict, list]) -> None:
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
        item = data.get("ITEM", {})
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

    def xǁFilesǁhandle_filelist_changed__mutmut_34(self, data: typing.Union[dict, list]) -> None:
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
        source_item = None

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

    def xǁFilesǁhandle_filelist_changed__mutmut_35(self, data: typing.Union[dict, list]) -> None:
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
        source_item = data.get(None, {})

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

    def xǁFilesǁhandle_filelist_changed__mutmut_36(self, data: typing.Union[dict, list]) -> None:
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
        source_item = data.get("source_item", None)

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

    def xǁFilesǁhandle_filelist_changed__mutmut_37(self, data: typing.Union[dict, list]) -> None:
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
        source_item = data.get({})

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

    def xǁFilesǁhandle_filelist_changed__mutmut_38(self, data: typing.Union[dict, list]) -> None:
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
        source_item = data.get("source_item", )

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

    def xǁFilesǁhandle_filelist_changed__mutmut_39(self, data: typing.Union[dict, list]) -> None:
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
        source_item = data.get("XXsource_itemXX", {})

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

    def xǁFilesǁhandle_filelist_changed__mutmut_40(self, data: typing.Union[dict, list]) -> None:
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
        source_item = data.get("SOURCE_ITEM", {})

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

    def xǁFilesǁhandle_filelist_changed__mutmut_41(self, data: typing.Union[dict, list]) -> None:
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

        logger.debug(None)

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

    def xǁFilesǁhandle_filelist_changed__mutmut_42(self, data: typing.Union[dict, list]) -> None:
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

        handlers = None

        handler = handlers.get(action)
        if handler:
            handler(item, source_item)

    def xǁFilesǁhandle_filelist_changed__mutmut_43(self, data: typing.Union[dict, list]) -> None:
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

        handler = None
        if handler:
            handler(item, source_item)

    def xǁFilesǁhandle_filelist_changed__mutmut_44(self, data: typing.Union[dict, list]) -> None:
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

        handler = handlers.get(None)
        if handler:
            handler(item, source_item)

    def xǁFilesǁhandle_filelist_changed__mutmut_45(self, data: typing.Union[dict, list]) -> None:
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
            handler(None, source_item)

    def xǁFilesǁhandle_filelist_changed__mutmut_46(self, data: typing.Union[dict, list]) -> None:
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
            handler(item, None)

    def xǁFilesǁhandle_filelist_changed__mutmut_47(self, data: typing.Union[dict, list]) -> None:
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
            handler(source_item)

    def xǁFilesǁhandle_filelist_changed__mutmut_48(self, data: typing.Union[dict, list]) -> None:
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
            handler(item, )
    
    xǁFilesǁhandle_filelist_changed__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁhandle_filelist_changed__mutmut_1': xǁFilesǁhandle_filelist_changed__mutmut_1, 
        'xǁFilesǁhandle_filelist_changed__mutmut_2': xǁFilesǁhandle_filelist_changed__mutmut_2, 
        'xǁFilesǁhandle_filelist_changed__mutmut_3': xǁFilesǁhandle_filelist_changed__mutmut_3, 
        'xǁFilesǁhandle_filelist_changed__mutmut_4': xǁFilesǁhandle_filelist_changed__mutmut_4, 
        'xǁFilesǁhandle_filelist_changed__mutmut_5': xǁFilesǁhandle_filelist_changed__mutmut_5, 
        'xǁFilesǁhandle_filelist_changed__mutmut_6': xǁFilesǁhandle_filelist_changed__mutmut_6, 
        'xǁFilesǁhandle_filelist_changed__mutmut_7': xǁFilesǁhandle_filelist_changed__mutmut_7, 
        'xǁFilesǁhandle_filelist_changed__mutmut_8': xǁFilesǁhandle_filelist_changed__mutmut_8, 
        'xǁFilesǁhandle_filelist_changed__mutmut_9': xǁFilesǁhandle_filelist_changed__mutmut_9, 
        'xǁFilesǁhandle_filelist_changed__mutmut_10': xǁFilesǁhandle_filelist_changed__mutmut_10, 
        'xǁFilesǁhandle_filelist_changed__mutmut_11': xǁFilesǁhandle_filelist_changed__mutmut_11, 
        'xǁFilesǁhandle_filelist_changed__mutmut_12': xǁFilesǁhandle_filelist_changed__mutmut_12, 
        'xǁFilesǁhandle_filelist_changed__mutmut_13': xǁFilesǁhandle_filelist_changed__mutmut_13, 
        'xǁFilesǁhandle_filelist_changed__mutmut_14': xǁFilesǁhandle_filelist_changed__mutmut_14, 
        'xǁFilesǁhandle_filelist_changed__mutmut_15': xǁFilesǁhandle_filelist_changed__mutmut_15, 
        'xǁFilesǁhandle_filelist_changed__mutmut_16': xǁFilesǁhandle_filelist_changed__mutmut_16, 
        'xǁFilesǁhandle_filelist_changed__mutmut_17': xǁFilesǁhandle_filelist_changed__mutmut_17, 
        'xǁFilesǁhandle_filelist_changed__mutmut_18': xǁFilesǁhandle_filelist_changed__mutmut_18, 
        'xǁFilesǁhandle_filelist_changed__mutmut_19': xǁFilesǁhandle_filelist_changed__mutmut_19, 
        'xǁFilesǁhandle_filelist_changed__mutmut_20': xǁFilesǁhandle_filelist_changed__mutmut_20, 
        'xǁFilesǁhandle_filelist_changed__mutmut_21': xǁFilesǁhandle_filelist_changed__mutmut_21, 
        'xǁFilesǁhandle_filelist_changed__mutmut_22': xǁFilesǁhandle_filelist_changed__mutmut_22, 
        'xǁFilesǁhandle_filelist_changed__mutmut_23': xǁFilesǁhandle_filelist_changed__mutmut_23, 
        'xǁFilesǁhandle_filelist_changed__mutmut_24': xǁFilesǁhandle_filelist_changed__mutmut_24, 
        'xǁFilesǁhandle_filelist_changed__mutmut_25': xǁFilesǁhandle_filelist_changed__mutmut_25, 
        'xǁFilesǁhandle_filelist_changed__mutmut_26': xǁFilesǁhandle_filelist_changed__mutmut_26, 
        'xǁFilesǁhandle_filelist_changed__mutmut_27': xǁFilesǁhandle_filelist_changed__mutmut_27, 
        'xǁFilesǁhandle_filelist_changed__mutmut_28': xǁFilesǁhandle_filelist_changed__mutmut_28, 
        'xǁFilesǁhandle_filelist_changed__mutmut_29': xǁFilesǁhandle_filelist_changed__mutmut_29, 
        'xǁFilesǁhandle_filelist_changed__mutmut_30': xǁFilesǁhandle_filelist_changed__mutmut_30, 
        'xǁFilesǁhandle_filelist_changed__mutmut_31': xǁFilesǁhandle_filelist_changed__mutmut_31, 
        'xǁFilesǁhandle_filelist_changed__mutmut_32': xǁFilesǁhandle_filelist_changed__mutmut_32, 
        'xǁFilesǁhandle_filelist_changed__mutmut_33': xǁFilesǁhandle_filelist_changed__mutmut_33, 
        'xǁFilesǁhandle_filelist_changed__mutmut_34': xǁFilesǁhandle_filelist_changed__mutmut_34, 
        'xǁFilesǁhandle_filelist_changed__mutmut_35': xǁFilesǁhandle_filelist_changed__mutmut_35, 
        'xǁFilesǁhandle_filelist_changed__mutmut_36': xǁFilesǁhandle_filelist_changed__mutmut_36, 
        'xǁFilesǁhandle_filelist_changed__mutmut_37': xǁFilesǁhandle_filelist_changed__mutmut_37, 
        'xǁFilesǁhandle_filelist_changed__mutmut_38': xǁFilesǁhandle_filelist_changed__mutmut_38, 
        'xǁFilesǁhandle_filelist_changed__mutmut_39': xǁFilesǁhandle_filelist_changed__mutmut_39, 
        'xǁFilesǁhandle_filelist_changed__mutmut_40': xǁFilesǁhandle_filelist_changed__mutmut_40, 
        'xǁFilesǁhandle_filelist_changed__mutmut_41': xǁFilesǁhandle_filelist_changed__mutmut_41, 
        'xǁFilesǁhandle_filelist_changed__mutmut_42': xǁFilesǁhandle_filelist_changed__mutmut_42, 
        'xǁFilesǁhandle_filelist_changed__mutmut_43': xǁFilesǁhandle_filelist_changed__mutmut_43, 
        'xǁFilesǁhandle_filelist_changed__mutmut_44': xǁFilesǁhandle_filelist_changed__mutmut_44, 
        'xǁFilesǁhandle_filelist_changed__mutmut_45': xǁFilesǁhandle_filelist_changed__mutmut_45, 
        'xǁFilesǁhandle_filelist_changed__mutmut_46': xǁFilesǁhandle_filelist_changed__mutmut_46, 
        'xǁFilesǁhandle_filelist_changed__mutmut_47': xǁFilesǁhandle_filelist_changed__mutmut_47, 
        'xǁFilesǁhandle_filelist_changed__mutmut_48': xǁFilesǁhandle_filelist_changed__mutmut_48
    }
    xǁFilesǁhandle_filelist_changed__mutmut_orig.__name__ = 'xǁFilesǁhandle_filelist_changed'

    def _handle_file_created(self, item: dict, _: dict) -> None:
        args = [item, _]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_handle_file_created__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_handle_file_created__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_handle_file_created__mutmut_orig(self, item: dict, _: dict) -> None:
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

    def xǁFilesǁ_handle_file_created__mutmut_1(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = None
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

    def xǁFilesǁ_handle_file_created__mutmut_2(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get(None, "")
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

    def xǁFilesǁ_handle_file_created__mutmut_3(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", None)
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

    def xǁFilesǁ_handle_file_created__mutmut_4(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("")
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

    def xǁFilesǁ_handle_file_created__mutmut_5(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", )
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

    def xǁFilesǁ_handle_file_created__mutmut_6(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("XXpathXX", "")
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

    def xǁFilesǁ_handle_file_created__mutmut_7(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("PATH", "")
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

    def xǁFilesǁ_handle_file_created__mutmut_8(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "XXXX")
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

    def xǁFilesǁ_handle_file_created__mutmut_9(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if path:
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

    def xǁFilesǁ_handle_file_created__mutmut_10(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(None):
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

    def xǁFilesǁ_handle_file_created__mutmut_11(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = None
            self._handle_dir_created(item, {})
            return

        if not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_12(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["XXdirnameXX"] = path
            self._handle_dir_created(item, {})
            return

        if not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_13(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["DIRNAME"] = path
            self._handle_dir_created(item, {})
            return

        if not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_14(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_created(None, {})
            return

        if not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_15(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_created(item, None)
            return

        if not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_16(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_created({})
            return

        if not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_17(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_created(item, )
            return

        if not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_18(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_created(item, {})
            return

        if path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_19(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_created(item, {})
            return

        if not path.lower().endswith(None):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_20(self, item: dict, _: dict) -> None:
        """Handle new file creation."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_created(item, {})
            return

        if not path.upper().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_21(self, item: dict, _: dict) -> None:
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

        self._files[path] = None
        self.file_added.emit(item)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_22(self, item: dict, _: dict) -> None:
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
        self.file_added.emit(None)

        # Request metadata (will update later)
        self.request_file_metadata.emit(path.removeprefix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_23(self, item: dict, _: dict) -> None:
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
        self.request_file_metadata.emit(None)
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_24(self, item: dict, _: dict) -> None:
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
        self.request_file_metadata.emit(path.removeprefix(None))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_25(self, item: dict, _: dict) -> None:
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
        self.request_file_metadata.emit(path.removesuffix("/"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_26(self, item: dict, _: dict) -> None:
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
        self.request_file_metadata.emit(path.removeprefix("XX/XX"))
        logger.info(f"File created: {path}")

    def xǁFilesǁ_handle_file_created__mutmut_27(self, item: dict, _: dict) -> None:
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
        logger.info(None)
    
    xǁFilesǁ_handle_file_created__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_handle_file_created__mutmut_1': xǁFilesǁ_handle_file_created__mutmut_1, 
        'xǁFilesǁ_handle_file_created__mutmut_2': xǁFilesǁ_handle_file_created__mutmut_2, 
        'xǁFilesǁ_handle_file_created__mutmut_3': xǁFilesǁ_handle_file_created__mutmut_3, 
        'xǁFilesǁ_handle_file_created__mutmut_4': xǁFilesǁ_handle_file_created__mutmut_4, 
        'xǁFilesǁ_handle_file_created__mutmut_5': xǁFilesǁ_handle_file_created__mutmut_5, 
        'xǁFilesǁ_handle_file_created__mutmut_6': xǁFilesǁ_handle_file_created__mutmut_6, 
        'xǁFilesǁ_handle_file_created__mutmut_7': xǁFilesǁ_handle_file_created__mutmut_7, 
        'xǁFilesǁ_handle_file_created__mutmut_8': xǁFilesǁ_handle_file_created__mutmut_8, 
        'xǁFilesǁ_handle_file_created__mutmut_9': xǁFilesǁ_handle_file_created__mutmut_9, 
        'xǁFilesǁ_handle_file_created__mutmut_10': xǁFilesǁ_handle_file_created__mutmut_10, 
        'xǁFilesǁ_handle_file_created__mutmut_11': xǁFilesǁ_handle_file_created__mutmut_11, 
        'xǁFilesǁ_handle_file_created__mutmut_12': xǁFilesǁ_handle_file_created__mutmut_12, 
        'xǁFilesǁ_handle_file_created__mutmut_13': xǁFilesǁ_handle_file_created__mutmut_13, 
        'xǁFilesǁ_handle_file_created__mutmut_14': xǁFilesǁ_handle_file_created__mutmut_14, 
        'xǁFilesǁ_handle_file_created__mutmut_15': xǁFilesǁ_handle_file_created__mutmut_15, 
        'xǁFilesǁ_handle_file_created__mutmut_16': xǁFilesǁ_handle_file_created__mutmut_16, 
        'xǁFilesǁ_handle_file_created__mutmut_17': xǁFilesǁ_handle_file_created__mutmut_17, 
        'xǁFilesǁ_handle_file_created__mutmut_18': xǁFilesǁ_handle_file_created__mutmut_18, 
        'xǁFilesǁ_handle_file_created__mutmut_19': xǁFilesǁ_handle_file_created__mutmut_19, 
        'xǁFilesǁ_handle_file_created__mutmut_20': xǁFilesǁ_handle_file_created__mutmut_20, 
        'xǁFilesǁ_handle_file_created__mutmut_21': xǁFilesǁ_handle_file_created__mutmut_21, 
        'xǁFilesǁ_handle_file_created__mutmut_22': xǁFilesǁ_handle_file_created__mutmut_22, 
        'xǁFilesǁ_handle_file_created__mutmut_23': xǁFilesǁ_handle_file_created__mutmut_23, 
        'xǁFilesǁ_handle_file_created__mutmut_24': xǁFilesǁ_handle_file_created__mutmut_24, 
        'xǁFilesǁ_handle_file_created__mutmut_25': xǁFilesǁ_handle_file_created__mutmut_25, 
        'xǁFilesǁ_handle_file_created__mutmut_26': xǁFilesǁ_handle_file_created__mutmut_26, 
        'xǁFilesǁ_handle_file_created__mutmut_27': xǁFilesǁ_handle_file_created__mutmut_27
    }
    xǁFilesǁ_handle_file_created__mutmut_orig.__name__ = 'xǁFilesǁ_handle_file_created'

    def _handle_file_deleted(self, item: dict, _: dict) -> None:
        args = [item, _]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_handle_file_deleted__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_handle_file_deleted__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_handle_file_deleted__mutmut_orig(self, item: dict, _: dict) -> None:
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

    def xǁFilesǁ_handle_file_deleted__mutmut_1(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = None
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

    def xǁFilesǁ_handle_file_deleted__mutmut_2(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get(None, "")
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

    def xǁFilesǁ_handle_file_deleted__mutmut_3(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", None)
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

    def xǁFilesǁ_handle_file_deleted__mutmut_4(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("")
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

    def xǁFilesǁ_handle_file_deleted__mutmut_5(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", )
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

    def xǁFilesǁ_handle_file_deleted__mutmut_6(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("XXpathXX", "")
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

    def xǁFilesǁ_handle_file_deleted__mutmut_7(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("PATH", "")
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

    def xǁFilesǁ_handle_file_deleted__mutmut_8(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "XXXX")
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

    def xǁFilesǁ_handle_file_deleted__mutmut_9(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_10(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(None):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_11(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = None
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_12(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["XXdirnameXX"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_13(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["DIRNAME"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_14(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(None, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_15(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, None)
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_16(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted({})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_17(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, )
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_18(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(None, None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_19(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(None)
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_20(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, )
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_21(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(None, None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_22(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_23(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("/"), )

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_24(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix(None), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_25(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removesuffix("/"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_26(self, item: dict, _: dict) -> None:
        """Handle file deletion."""
        path = item.get("path", "")
        if not path:
            return

        if self._is_usb_mount(path):
            item["dirname"] = path
            self._handle_dir_deleted(item, {})
            return

        self._files.pop(path, None)
        self._files_metadata.pop(path.removeprefix("XX/XX"), None)

        self.file_removed.emit(path)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_27(self, item: dict, _: dict) -> None:
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

        self.file_removed.emit(None)
        logger.info(f"File deleted: {path}")

    def xǁFilesǁ_handle_file_deleted__mutmut_28(self, item: dict, _: dict) -> None:
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
        logger.info(None)
    
    xǁFilesǁ_handle_file_deleted__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_handle_file_deleted__mutmut_1': xǁFilesǁ_handle_file_deleted__mutmut_1, 
        'xǁFilesǁ_handle_file_deleted__mutmut_2': xǁFilesǁ_handle_file_deleted__mutmut_2, 
        'xǁFilesǁ_handle_file_deleted__mutmut_3': xǁFilesǁ_handle_file_deleted__mutmut_3, 
        'xǁFilesǁ_handle_file_deleted__mutmut_4': xǁFilesǁ_handle_file_deleted__mutmut_4, 
        'xǁFilesǁ_handle_file_deleted__mutmut_5': xǁFilesǁ_handle_file_deleted__mutmut_5, 
        'xǁFilesǁ_handle_file_deleted__mutmut_6': xǁFilesǁ_handle_file_deleted__mutmut_6, 
        'xǁFilesǁ_handle_file_deleted__mutmut_7': xǁFilesǁ_handle_file_deleted__mutmut_7, 
        'xǁFilesǁ_handle_file_deleted__mutmut_8': xǁFilesǁ_handle_file_deleted__mutmut_8, 
        'xǁFilesǁ_handle_file_deleted__mutmut_9': xǁFilesǁ_handle_file_deleted__mutmut_9, 
        'xǁFilesǁ_handle_file_deleted__mutmut_10': xǁFilesǁ_handle_file_deleted__mutmut_10, 
        'xǁFilesǁ_handle_file_deleted__mutmut_11': xǁFilesǁ_handle_file_deleted__mutmut_11, 
        'xǁFilesǁ_handle_file_deleted__mutmut_12': xǁFilesǁ_handle_file_deleted__mutmut_12, 
        'xǁFilesǁ_handle_file_deleted__mutmut_13': xǁFilesǁ_handle_file_deleted__mutmut_13, 
        'xǁFilesǁ_handle_file_deleted__mutmut_14': xǁFilesǁ_handle_file_deleted__mutmut_14, 
        'xǁFilesǁ_handle_file_deleted__mutmut_15': xǁFilesǁ_handle_file_deleted__mutmut_15, 
        'xǁFilesǁ_handle_file_deleted__mutmut_16': xǁFilesǁ_handle_file_deleted__mutmut_16, 
        'xǁFilesǁ_handle_file_deleted__mutmut_17': xǁFilesǁ_handle_file_deleted__mutmut_17, 
        'xǁFilesǁ_handle_file_deleted__mutmut_18': xǁFilesǁ_handle_file_deleted__mutmut_18, 
        'xǁFilesǁ_handle_file_deleted__mutmut_19': xǁFilesǁ_handle_file_deleted__mutmut_19, 
        'xǁFilesǁ_handle_file_deleted__mutmut_20': xǁFilesǁ_handle_file_deleted__mutmut_20, 
        'xǁFilesǁ_handle_file_deleted__mutmut_21': xǁFilesǁ_handle_file_deleted__mutmut_21, 
        'xǁFilesǁ_handle_file_deleted__mutmut_22': xǁFilesǁ_handle_file_deleted__mutmut_22, 
        'xǁFilesǁ_handle_file_deleted__mutmut_23': xǁFilesǁ_handle_file_deleted__mutmut_23, 
        'xǁFilesǁ_handle_file_deleted__mutmut_24': xǁFilesǁ_handle_file_deleted__mutmut_24, 
        'xǁFilesǁ_handle_file_deleted__mutmut_25': xǁFilesǁ_handle_file_deleted__mutmut_25, 
        'xǁFilesǁ_handle_file_deleted__mutmut_26': xǁFilesǁ_handle_file_deleted__mutmut_26, 
        'xǁFilesǁ_handle_file_deleted__mutmut_27': xǁFilesǁ_handle_file_deleted__mutmut_27, 
        'xǁFilesǁ_handle_file_deleted__mutmut_28': xǁFilesǁ_handle_file_deleted__mutmut_28
    }
    xǁFilesǁ_handle_file_deleted__mutmut_orig.__name__ = 'xǁFilesǁ_handle_file_deleted'

    def _handle_file_modified(self, item: dict, _: dict) -> None:
        args = [item, _]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_handle_file_modified__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_handle_file_modified__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_handle_file_modified__mutmut_orig(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_1(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = None
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_2(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get(None, "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_3(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", None)
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_4(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_5(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", )
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_6(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("XXpathXX", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_7(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("PATH", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_8(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "XXXX")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_9(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path and not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_10(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_11(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_12(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(None):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_13(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.upper().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_14(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = None
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_15(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(None, None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_16(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_17(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), )

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_18(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix(None), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_19(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removesuffix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_20(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("XX/XX"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_21(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(None)
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_22(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix(None))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_23(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removesuffix("/"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_24(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("XX/XX"))
        self.file_modified.emit(item)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_25(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(None)
        logger.info(f"File modified: {path}")

    def xǁFilesǁ_handle_file_modified__mutmut_26(self, item: dict, _: dict) -> None:
        """Handle file modification."""
        path = item.get("path", "")
        if not path or not path.lower().endswith(self.GCODE_EXTENSION):
            return

        self._files[path] = item
        self._files_metadata.pop(path.removeprefix("/"), None)

        self.request_file_metadata.emit(path.removeprefix("/"))
        self.file_modified.emit(item)
        logger.info(None)
    
    xǁFilesǁ_handle_file_modified__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_handle_file_modified__mutmut_1': xǁFilesǁ_handle_file_modified__mutmut_1, 
        'xǁFilesǁ_handle_file_modified__mutmut_2': xǁFilesǁ_handle_file_modified__mutmut_2, 
        'xǁFilesǁ_handle_file_modified__mutmut_3': xǁFilesǁ_handle_file_modified__mutmut_3, 
        'xǁFilesǁ_handle_file_modified__mutmut_4': xǁFilesǁ_handle_file_modified__mutmut_4, 
        'xǁFilesǁ_handle_file_modified__mutmut_5': xǁFilesǁ_handle_file_modified__mutmut_5, 
        'xǁFilesǁ_handle_file_modified__mutmut_6': xǁFilesǁ_handle_file_modified__mutmut_6, 
        'xǁFilesǁ_handle_file_modified__mutmut_7': xǁFilesǁ_handle_file_modified__mutmut_7, 
        'xǁFilesǁ_handle_file_modified__mutmut_8': xǁFilesǁ_handle_file_modified__mutmut_8, 
        'xǁFilesǁ_handle_file_modified__mutmut_9': xǁFilesǁ_handle_file_modified__mutmut_9, 
        'xǁFilesǁ_handle_file_modified__mutmut_10': xǁFilesǁ_handle_file_modified__mutmut_10, 
        'xǁFilesǁ_handle_file_modified__mutmut_11': xǁFilesǁ_handle_file_modified__mutmut_11, 
        'xǁFilesǁ_handle_file_modified__mutmut_12': xǁFilesǁ_handle_file_modified__mutmut_12, 
        'xǁFilesǁ_handle_file_modified__mutmut_13': xǁFilesǁ_handle_file_modified__mutmut_13, 
        'xǁFilesǁ_handle_file_modified__mutmut_14': xǁFilesǁ_handle_file_modified__mutmut_14, 
        'xǁFilesǁ_handle_file_modified__mutmut_15': xǁFilesǁ_handle_file_modified__mutmut_15, 
        'xǁFilesǁ_handle_file_modified__mutmut_16': xǁFilesǁ_handle_file_modified__mutmut_16, 
        'xǁFilesǁ_handle_file_modified__mutmut_17': xǁFilesǁ_handle_file_modified__mutmut_17, 
        'xǁFilesǁ_handle_file_modified__mutmut_18': xǁFilesǁ_handle_file_modified__mutmut_18, 
        'xǁFilesǁ_handle_file_modified__mutmut_19': xǁFilesǁ_handle_file_modified__mutmut_19, 
        'xǁFilesǁ_handle_file_modified__mutmut_20': xǁFilesǁ_handle_file_modified__mutmut_20, 
        'xǁFilesǁ_handle_file_modified__mutmut_21': xǁFilesǁ_handle_file_modified__mutmut_21, 
        'xǁFilesǁ_handle_file_modified__mutmut_22': xǁFilesǁ_handle_file_modified__mutmut_22, 
        'xǁFilesǁ_handle_file_modified__mutmut_23': xǁFilesǁ_handle_file_modified__mutmut_23, 
        'xǁFilesǁ_handle_file_modified__mutmut_24': xǁFilesǁ_handle_file_modified__mutmut_24, 
        'xǁFilesǁ_handle_file_modified__mutmut_25': xǁFilesǁ_handle_file_modified__mutmut_25, 
        'xǁFilesǁ_handle_file_modified__mutmut_26': xǁFilesǁ_handle_file_modified__mutmut_26
    }
    xǁFilesǁ_handle_file_modified__mutmut_orig.__name__ = 'xǁFilesǁ_handle_file_modified'

    def _handle_file_moved(self, item: dict, source_item: dict) -> None:
        args = [item, source_item]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_handle_file_moved__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_handle_file_moved__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_handle_file_moved__mutmut_orig(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_1(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = None
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_2(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get(None, "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_3(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", None)
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_4(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_5(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", )
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_6(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("XXpathXX", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_7(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("PATH", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_8(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "XXXX")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_9(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = None

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_10(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get(None, "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_11(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", None)

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_12(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_13(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", )

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_14(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("XXpathXX", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_15(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("PATH", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_16(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "XXXX")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_17(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(None, {})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_18(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, None)
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_19(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted({})
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_20(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, )
        if new_path:
            self._handle_file_created(item, {})

    def xǁFilesǁ_handle_file_moved__mutmut_21(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(None, {})

    def xǁFilesǁ_handle_file_moved__mutmut_22(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, None)

    def xǁFilesǁ_handle_file_moved__mutmut_23(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created({})

    def xǁFilesǁ_handle_file_moved__mutmut_24(self, item: dict, source_item: dict) -> None:
        """Handle file move/rename."""
        old_path = source_item.get("path", "")
        new_path = item.get("path", "")

        if old_path:
            self._handle_file_deleted(source_item, {})
        if new_path:
            self._handle_file_created(item, )
    
    xǁFilesǁ_handle_file_moved__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_handle_file_moved__mutmut_1': xǁFilesǁ_handle_file_moved__mutmut_1, 
        'xǁFilesǁ_handle_file_moved__mutmut_2': xǁFilesǁ_handle_file_moved__mutmut_2, 
        'xǁFilesǁ_handle_file_moved__mutmut_3': xǁFilesǁ_handle_file_moved__mutmut_3, 
        'xǁFilesǁ_handle_file_moved__mutmut_4': xǁFilesǁ_handle_file_moved__mutmut_4, 
        'xǁFilesǁ_handle_file_moved__mutmut_5': xǁFilesǁ_handle_file_moved__mutmut_5, 
        'xǁFilesǁ_handle_file_moved__mutmut_6': xǁFilesǁ_handle_file_moved__mutmut_6, 
        'xǁFilesǁ_handle_file_moved__mutmut_7': xǁFilesǁ_handle_file_moved__mutmut_7, 
        'xǁFilesǁ_handle_file_moved__mutmut_8': xǁFilesǁ_handle_file_moved__mutmut_8, 
        'xǁFilesǁ_handle_file_moved__mutmut_9': xǁFilesǁ_handle_file_moved__mutmut_9, 
        'xǁFilesǁ_handle_file_moved__mutmut_10': xǁFilesǁ_handle_file_moved__mutmut_10, 
        'xǁFilesǁ_handle_file_moved__mutmut_11': xǁFilesǁ_handle_file_moved__mutmut_11, 
        'xǁFilesǁ_handle_file_moved__mutmut_12': xǁFilesǁ_handle_file_moved__mutmut_12, 
        'xǁFilesǁ_handle_file_moved__mutmut_13': xǁFilesǁ_handle_file_moved__mutmut_13, 
        'xǁFilesǁ_handle_file_moved__mutmut_14': xǁFilesǁ_handle_file_moved__mutmut_14, 
        'xǁFilesǁ_handle_file_moved__mutmut_15': xǁFilesǁ_handle_file_moved__mutmut_15, 
        'xǁFilesǁ_handle_file_moved__mutmut_16': xǁFilesǁ_handle_file_moved__mutmut_16, 
        'xǁFilesǁ_handle_file_moved__mutmut_17': xǁFilesǁ_handle_file_moved__mutmut_17, 
        'xǁFilesǁ_handle_file_moved__mutmut_18': xǁFilesǁ_handle_file_moved__mutmut_18, 
        'xǁFilesǁ_handle_file_moved__mutmut_19': xǁFilesǁ_handle_file_moved__mutmut_19, 
        'xǁFilesǁ_handle_file_moved__mutmut_20': xǁFilesǁ_handle_file_moved__mutmut_20, 
        'xǁFilesǁ_handle_file_moved__mutmut_21': xǁFilesǁ_handle_file_moved__mutmut_21, 
        'xǁFilesǁ_handle_file_moved__mutmut_22': xǁFilesǁ_handle_file_moved__mutmut_22, 
        'xǁFilesǁ_handle_file_moved__mutmut_23': xǁFilesǁ_handle_file_moved__mutmut_23, 
        'xǁFilesǁ_handle_file_moved__mutmut_24': xǁFilesǁ_handle_file_moved__mutmut_24
    }
    xǁFilesǁ_handle_file_moved__mutmut_orig.__name__ = 'xǁFilesǁ_handle_file_moved'

    def _handle_dir_created(self, item: dict, _: dict) -> None:
        args = [item, _]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_handle_dir_created__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_handle_dir_created__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_handle_dir_created__mutmut_orig(self, item: dict, _: dict) -> None:
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

    def xǁFilesǁ_handle_dir_created__mutmut_1(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = None
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

    def xǁFilesǁ_handle_dir_created__mutmut_2(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get(None, "")
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

    def xǁFilesǁ_handle_dir_created__mutmut_3(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", None)
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

    def xǁFilesǁ_handle_dir_created__mutmut_4(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("")
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

    def xǁFilesǁ_handle_dir_created__mutmut_5(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", )
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

    def xǁFilesǁ_handle_dir_created__mutmut_6(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("XXpathXX", "")
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

    def xǁFilesǁ_handle_dir_created__mutmut_7(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("PATH", "")
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

    def xǁFilesǁ_handle_dir_created__mutmut_8(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "XXXX")
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

    def xǁFilesǁ_handle_dir_created__mutmut_9(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = None

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

    def xǁFilesǁ_handle_dir_created__mutmut_10(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get(None, "")

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

    def xǁFilesǁ_handle_dir_created__mutmut_11(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", None)

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

    def xǁFilesǁ_handle_dir_created__mutmut_12(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("")

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

    def xǁFilesǁ_handle_dir_created__mutmut_13(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", )

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

    def xǁFilesǁ_handle_dir_created__mutmut_14(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("XXdirnameXX", "")

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

    def xǁFilesǁ_handle_dir_created__mutmut_15(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("DIRNAME", "")

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

    def xǁFilesǁ_handle_dir_created__mutmut_16(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "XXXX")

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

    def xǁFilesǁ_handle_dir_created__mutmut_17(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname or path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_18(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_19(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = None

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_20(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split(None)[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_21(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip(None).split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_22(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.lstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_23(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("XX/XX").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_24(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("XX/XX")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_25(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[+1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_26(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-2]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_27(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname and dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_28(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_29(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith(None):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_30(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("XX.XX"):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_31(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = None
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_32(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["XXdirnameXX"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_33(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["DIRNAME"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_34(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = None
        self.dir_added.emit(item)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_35(self, item: dict, _: dict) -> None:
        """Handle directory creation."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname or dirname.startswith("."):
            return

        item["dirname"] = dirname
        self._directories[dirname] = item
        self.dir_added.emit(None)
        logger.info(f"Directory created: {dirname}")

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_36(self, item: dict, _: dict) -> None:
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
        logger.info(None)

        if self._is_usb_mount(dirname):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_37(self, item: dict, _: dict) -> None:
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

        if self._is_usb_mount(None):
            self._preload_usb_contents(dirname)

    def xǁFilesǁ_handle_dir_created__mutmut_38(self, item: dict, _: dict) -> None:
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
            self._preload_usb_contents(None)
    
    xǁFilesǁ_handle_dir_created__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_handle_dir_created__mutmut_1': xǁFilesǁ_handle_dir_created__mutmut_1, 
        'xǁFilesǁ_handle_dir_created__mutmut_2': xǁFilesǁ_handle_dir_created__mutmut_2, 
        'xǁFilesǁ_handle_dir_created__mutmut_3': xǁFilesǁ_handle_dir_created__mutmut_3, 
        'xǁFilesǁ_handle_dir_created__mutmut_4': xǁFilesǁ_handle_dir_created__mutmut_4, 
        'xǁFilesǁ_handle_dir_created__mutmut_5': xǁFilesǁ_handle_dir_created__mutmut_5, 
        'xǁFilesǁ_handle_dir_created__mutmut_6': xǁFilesǁ_handle_dir_created__mutmut_6, 
        'xǁFilesǁ_handle_dir_created__mutmut_7': xǁFilesǁ_handle_dir_created__mutmut_7, 
        'xǁFilesǁ_handle_dir_created__mutmut_8': xǁFilesǁ_handle_dir_created__mutmut_8, 
        'xǁFilesǁ_handle_dir_created__mutmut_9': xǁFilesǁ_handle_dir_created__mutmut_9, 
        'xǁFilesǁ_handle_dir_created__mutmut_10': xǁFilesǁ_handle_dir_created__mutmut_10, 
        'xǁFilesǁ_handle_dir_created__mutmut_11': xǁFilesǁ_handle_dir_created__mutmut_11, 
        'xǁFilesǁ_handle_dir_created__mutmut_12': xǁFilesǁ_handle_dir_created__mutmut_12, 
        'xǁFilesǁ_handle_dir_created__mutmut_13': xǁFilesǁ_handle_dir_created__mutmut_13, 
        'xǁFilesǁ_handle_dir_created__mutmut_14': xǁFilesǁ_handle_dir_created__mutmut_14, 
        'xǁFilesǁ_handle_dir_created__mutmut_15': xǁFilesǁ_handle_dir_created__mutmut_15, 
        'xǁFilesǁ_handle_dir_created__mutmut_16': xǁFilesǁ_handle_dir_created__mutmut_16, 
        'xǁFilesǁ_handle_dir_created__mutmut_17': xǁFilesǁ_handle_dir_created__mutmut_17, 
        'xǁFilesǁ_handle_dir_created__mutmut_18': xǁFilesǁ_handle_dir_created__mutmut_18, 
        'xǁFilesǁ_handle_dir_created__mutmut_19': xǁFilesǁ_handle_dir_created__mutmut_19, 
        'xǁFilesǁ_handle_dir_created__mutmut_20': xǁFilesǁ_handle_dir_created__mutmut_20, 
        'xǁFilesǁ_handle_dir_created__mutmut_21': xǁFilesǁ_handle_dir_created__mutmut_21, 
        'xǁFilesǁ_handle_dir_created__mutmut_22': xǁFilesǁ_handle_dir_created__mutmut_22, 
        'xǁFilesǁ_handle_dir_created__mutmut_23': xǁFilesǁ_handle_dir_created__mutmut_23, 
        'xǁFilesǁ_handle_dir_created__mutmut_24': xǁFilesǁ_handle_dir_created__mutmut_24, 
        'xǁFilesǁ_handle_dir_created__mutmut_25': xǁFilesǁ_handle_dir_created__mutmut_25, 
        'xǁFilesǁ_handle_dir_created__mutmut_26': xǁFilesǁ_handle_dir_created__mutmut_26, 
        'xǁFilesǁ_handle_dir_created__mutmut_27': xǁFilesǁ_handle_dir_created__mutmut_27, 
        'xǁFilesǁ_handle_dir_created__mutmut_28': xǁFilesǁ_handle_dir_created__mutmut_28, 
        'xǁFilesǁ_handle_dir_created__mutmut_29': xǁFilesǁ_handle_dir_created__mutmut_29, 
        'xǁFilesǁ_handle_dir_created__mutmut_30': xǁFilesǁ_handle_dir_created__mutmut_30, 
        'xǁFilesǁ_handle_dir_created__mutmut_31': xǁFilesǁ_handle_dir_created__mutmut_31, 
        'xǁFilesǁ_handle_dir_created__mutmut_32': xǁFilesǁ_handle_dir_created__mutmut_32, 
        'xǁFilesǁ_handle_dir_created__mutmut_33': xǁFilesǁ_handle_dir_created__mutmut_33, 
        'xǁFilesǁ_handle_dir_created__mutmut_34': xǁFilesǁ_handle_dir_created__mutmut_34, 
        'xǁFilesǁ_handle_dir_created__mutmut_35': xǁFilesǁ_handle_dir_created__mutmut_35, 
        'xǁFilesǁ_handle_dir_created__mutmut_36': xǁFilesǁ_handle_dir_created__mutmut_36, 
        'xǁFilesǁ_handle_dir_created__mutmut_37': xǁFilesǁ_handle_dir_created__mutmut_37, 
        'xǁFilesǁ_handle_dir_created__mutmut_38': xǁFilesǁ_handle_dir_created__mutmut_38
    }
    xǁFilesǁ_handle_dir_created__mutmut_orig.__name__ = 'xǁFilesǁ_handle_dir_created'

    def _handle_dir_deleted(self, item: dict, _: dict) -> None:
        args = [item, _]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_handle_dir_deleted__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_handle_dir_deleted__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_handle_dir_deleted__mutmut_orig(self, item: dict, _: dict) -> None:
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_1(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = None
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_2(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get(None, "")
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_3(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", None)
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_4(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("")
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_5(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", )
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_6(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("XXpathXX", "")
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_7(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("PATH", "")
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_8(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "XXXX")
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_9(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = None

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_10(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get(None, "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_11(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", None)

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_12(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_13(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", )

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_14(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("XXdirnameXX", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_15(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("DIRNAME", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_16(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "XXXX")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_17(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname or path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_18(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_19(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = None

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_20(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split(None)[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_21(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip(None).split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_22(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.lstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_23(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("XX/XX").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_24(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("XX/XX")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_25(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[+1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_26(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-2]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_27(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_28(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(None, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_29(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_30(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, )

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(dirname):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_31(self, item: dict, _: dict) -> None:
        """Handle directory deletion."""
        path = item.get("path", "")
        dirname = item.get("dirname", "")

        if not dirname and path:
            dirname = path.rstrip("/").split("/")[-1]

        if not dirname:
            return

        self._directories.pop(dirname, None)

        # Clear USB cache if this was a USB mount
        if self._is_usb_mount(None):
            self._usb_files_cache.pop(dirname, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_32(self, item: dict, _: dict) -> None:
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
            self._usb_files_cache.pop(None, None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_33(self, item: dict, _: dict) -> None:
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
            self._usb_files_cache.pop(None)
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_34(self, item: dict, _: dict) -> None:
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
            self._usb_files_cache.pop(dirname, )
            self._pending_usb_preloads.discard(dirname)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_35(self, item: dict, _: dict) -> None:
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
            self._pending_usb_preloads.discard(None)
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_36(self, item: dict, _: dict) -> None:
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
            if dirname not in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_37(self, item: dict, _: dict) -> None:
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(None)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_38(self, item: dict, _: dict) -> None:
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(None)

        self.dir_removed.emit(dirname)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_39(self, item: dict, _: dict) -> None:
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(None)
        logger.info(f"Directory deleted: {dirname}")

    def xǁFilesǁ_handle_dir_deleted__mutmut_40(self, item: dict, _: dict) -> None:
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
            if dirname in self._usb_preload_queue:
                self._usb_preload_queue.remove(dirname)
            logger.info(f"Cleared USB cache for: {dirname}")

        self.dir_removed.emit(dirname)
        logger.info(None)
    
    xǁFilesǁ_handle_dir_deleted__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_handle_dir_deleted__mutmut_1': xǁFilesǁ_handle_dir_deleted__mutmut_1, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_2': xǁFilesǁ_handle_dir_deleted__mutmut_2, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_3': xǁFilesǁ_handle_dir_deleted__mutmut_3, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_4': xǁFilesǁ_handle_dir_deleted__mutmut_4, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_5': xǁFilesǁ_handle_dir_deleted__mutmut_5, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_6': xǁFilesǁ_handle_dir_deleted__mutmut_6, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_7': xǁFilesǁ_handle_dir_deleted__mutmut_7, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_8': xǁFilesǁ_handle_dir_deleted__mutmut_8, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_9': xǁFilesǁ_handle_dir_deleted__mutmut_9, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_10': xǁFilesǁ_handle_dir_deleted__mutmut_10, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_11': xǁFilesǁ_handle_dir_deleted__mutmut_11, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_12': xǁFilesǁ_handle_dir_deleted__mutmut_12, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_13': xǁFilesǁ_handle_dir_deleted__mutmut_13, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_14': xǁFilesǁ_handle_dir_deleted__mutmut_14, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_15': xǁFilesǁ_handle_dir_deleted__mutmut_15, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_16': xǁFilesǁ_handle_dir_deleted__mutmut_16, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_17': xǁFilesǁ_handle_dir_deleted__mutmut_17, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_18': xǁFilesǁ_handle_dir_deleted__mutmut_18, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_19': xǁFilesǁ_handle_dir_deleted__mutmut_19, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_20': xǁFilesǁ_handle_dir_deleted__mutmut_20, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_21': xǁFilesǁ_handle_dir_deleted__mutmut_21, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_22': xǁFilesǁ_handle_dir_deleted__mutmut_22, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_23': xǁFilesǁ_handle_dir_deleted__mutmut_23, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_24': xǁFilesǁ_handle_dir_deleted__mutmut_24, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_25': xǁFilesǁ_handle_dir_deleted__mutmut_25, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_26': xǁFilesǁ_handle_dir_deleted__mutmut_26, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_27': xǁFilesǁ_handle_dir_deleted__mutmut_27, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_28': xǁFilesǁ_handle_dir_deleted__mutmut_28, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_29': xǁFilesǁ_handle_dir_deleted__mutmut_29, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_30': xǁFilesǁ_handle_dir_deleted__mutmut_30, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_31': xǁFilesǁ_handle_dir_deleted__mutmut_31, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_32': xǁFilesǁ_handle_dir_deleted__mutmut_32, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_33': xǁFilesǁ_handle_dir_deleted__mutmut_33, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_34': xǁFilesǁ_handle_dir_deleted__mutmut_34, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_35': xǁFilesǁ_handle_dir_deleted__mutmut_35, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_36': xǁFilesǁ_handle_dir_deleted__mutmut_36, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_37': xǁFilesǁ_handle_dir_deleted__mutmut_37, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_38': xǁFilesǁ_handle_dir_deleted__mutmut_38, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_39': xǁFilesǁ_handle_dir_deleted__mutmut_39, 
        'xǁFilesǁ_handle_dir_deleted__mutmut_40': xǁFilesǁ_handle_dir_deleted__mutmut_40
    }
    xǁFilesǁ_handle_dir_deleted__mutmut_orig.__name__ = 'xǁFilesǁ_handle_dir_deleted'

    def _handle_dir_moved(self, item: dict, source_item: dict) -> None:
        args = [item, source_item]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_handle_dir_moved__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_handle_dir_moved__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_handle_dir_moved__mutmut_orig(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        self._handle_dir_deleted(source_item, {})
        self._handle_dir_created(item, {})

    def xǁFilesǁ_handle_dir_moved__mutmut_1(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        self._handle_dir_deleted(None, {})
        self._handle_dir_created(item, {})

    def xǁFilesǁ_handle_dir_moved__mutmut_2(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        self._handle_dir_deleted(source_item, None)
        self._handle_dir_created(item, {})

    def xǁFilesǁ_handle_dir_moved__mutmut_3(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        self._handle_dir_deleted({})
        self._handle_dir_created(item, {})

    def xǁFilesǁ_handle_dir_moved__mutmut_4(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        self._handle_dir_deleted(source_item, )
        self._handle_dir_created(item, {})

    def xǁFilesǁ_handle_dir_moved__mutmut_5(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        self._handle_dir_deleted(source_item, {})
        self._handle_dir_created(None, {})

    def xǁFilesǁ_handle_dir_moved__mutmut_6(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        self._handle_dir_deleted(source_item, {})
        self._handle_dir_created(item, None)

    def xǁFilesǁ_handle_dir_moved__mutmut_7(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        self._handle_dir_deleted(source_item, {})
        self._handle_dir_created({})

    def xǁFilesǁ_handle_dir_moved__mutmut_8(self, item: dict, source_item: dict) -> None:
        """Handle directory move/rename."""
        self._handle_dir_deleted(source_item, {})
        self._handle_dir_created(item, )
    
    xǁFilesǁ_handle_dir_moved__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_handle_dir_moved__mutmut_1': xǁFilesǁ_handle_dir_moved__mutmut_1, 
        'xǁFilesǁ_handle_dir_moved__mutmut_2': xǁFilesǁ_handle_dir_moved__mutmut_2, 
        'xǁFilesǁ_handle_dir_moved__mutmut_3': xǁFilesǁ_handle_dir_moved__mutmut_3, 
        'xǁFilesǁ_handle_dir_moved__mutmut_4': xǁFilesǁ_handle_dir_moved__mutmut_4, 
        'xǁFilesǁ_handle_dir_moved__mutmut_5': xǁFilesǁ_handle_dir_moved__mutmut_5, 
        'xǁFilesǁ_handle_dir_moved__mutmut_6': xǁFilesǁ_handle_dir_moved__mutmut_6, 
        'xǁFilesǁ_handle_dir_moved__mutmut_7': xǁFilesǁ_handle_dir_moved__mutmut_7, 
        'xǁFilesǁ_handle_dir_moved__mutmut_8': xǁFilesǁ_handle_dir_moved__mutmut_8
    }
    xǁFilesǁ_handle_dir_moved__mutmut_orig.__name__ = 'xǁFilesǁ_handle_dir_moved'

    def _handle_root_update(self, _: dict, __: dict) -> None:
        args = [_, __]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_handle_root_update__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_handle_root_update__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_handle_root_update__mutmut_orig(self, _: dict, __: dict) -> None:
        """Handle root update."""
        logger.info("Root update detected, requesting full refresh")
        self.full_refresh_needed.emit()
        self.initial_load()

    def xǁFilesǁ_handle_root_update__mutmut_1(self, _: dict, __: dict) -> None:
        """Handle root update."""
        logger.info(None)
        self.full_refresh_needed.emit()
        self.initial_load()

    def xǁFilesǁ_handle_root_update__mutmut_2(self, _: dict, __: dict) -> None:
        """Handle root update."""
        logger.info("XXRoot update detected, requesting full refreshXX")
        self.full_refresh_needed.emit()
        self.initial_load()

    def xǁFilesǁ_handle_root_update__mutmut_3(self, _: dict, __: dict) -> None:
        """Handle root update."""
        logger.info("root update detected, requesting full refresh")
        self.full_refresh_needed.emit()
        self.initial_load()

    def xǁFilesǁ_handle_root_update__mutmut_4(self, _: dict, __: dict) -> None:
        """Handle root update."""
        logger.info("ROOT UPDATE DETECTED, REQUESTING FULL REFRESH")
        self.full_refresh_needed.emit()
        self.initial_load()
    
    xǁFilesǁ_handle_root_update__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_handle_root_update__mutmut_1': xǁFilesǁ_handle_root_update__mutmut_1, 
        'xǁFilesǁ_handle_root_update__mutmut_2': xǁFilesǁ_handle_root_update__mutmut_2, 
        'xǁFilesǁ_handle_root_update__mutmut_3': xǁFilesǁ_handle_root_update__mutmut_3, 
        'xǁFilesǁ_handle_root_update__mutmut_4': xǁFilesǁ_handle_root_update__mutmut_4
    }
    xǁFilesǁ_handle_root_update__mutmut_orig.__name__ = 'xǁFilesǁ_handle_root_update'

    @staticmethod
    def _is_usb_mount(path: str) -> bool:
        """Check if a path is a USB mount point."""
        path = path.removeprefix("/")
        return "/" not in path and path.startswith("USB-")

    def handle_message_received(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        args = [method, data, params]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁhandle_message_received__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁhandle_message_received__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁhandle_message_received__mutmut_orig(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" in method:
            self._process_file_list(data)
        elif "server.files.metadata" in method:
            self._process_metadata(data)
        elif "server.files.get_directory" in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_1(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "XXserver.files.listXX" in method:
            self._process_file_list(data)
        elif "server.files.metadata" in method:
            self._process_metadata(data)
        elif "server.files.get_directory" in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_2(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "SERVER.FILES.LIST" in method:
            self._process_file_list(data)
        elif "server.files.metadata" in method:
            self._process_metadata(data)
        elif "server.files.get_directory" in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_3(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" not in method:
            self._process_file_list(data)
        elif "server.files.metadata" in method:
            self._process_metadata(data)
        elif "server.files.get_directory" in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_4(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" in method:
            self._process_file_list(None)
        elif "server.files.metadata" in method:
            self._process_metadata(data)
        elif "server.files.get_directory" in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_5(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" in method:
            self._process_file_list(data)
        elif "XXserver.files.metadataXX" in method:
            self._process_metadata(data)
        elif "server.files.get_directory" in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_6(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" in method:
            self._process_file_list(data)
        elif "SERVER.FILES.METADATA" in method:
            self._process_metadata(data)
        elif "server.files.get_directory" in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_7(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" in method:
            self._process_file_list(data)
        elif "server.files.metadata" not in method:
            self._process_metadata(data)
        elif "server.files.get_directory" in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_8(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" in method:
            self._process_file_list(data)
        elif "server.files.metadata" in method:
            self._process_metadata(None)
        elif "server.files.get_directory" in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_9(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" in method:
            self._process_file_list(data)
        elif "server.files.metadata" in method:
            self._process_metadata(data)
        elif "XXserver.files.get_directoryXX" in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_10(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" in method:
            self._process_file_list(data)
        elif "server.files.metadata" in method:
            self._process_metadata(data)
        elif "SERVER.FILES.GET_DIRECTORY" in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_11(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" in method:
            self._process_file_list(data)
        elif "server.files.metadata" in method:
            self._process_metadata(data)
        elif "server.files.get_directory" not in method:
            self._process_directory_info(data)

    def xǁFilesǁhandle_message_received__mutmut_12(
        self, method: str, data: typing.Any, params: dict
    ) -> None:
        """Handle file-related messages received from Moonraker."""
        if "server.files.list" in method:
            self._process_file_list(data)
        elif "server.files.metadata" in method:
            self._process_metadata(data)
        elif "server.files.get_directory" in method:
            self._process_directory_info(None)
    
    xǁFilesǁhandle_message_received__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁhandle_message_received__mutmut_1': xǁFilesǁhandle_message_received__mutmut_1, 
        'xǁFilesǁhandle_message_received__mutmut_2': xǁFilesǁhandle_message_received__mutmut_2, 
        'xǁFilesǁhandle_message_received__mutmut_3': xǁFilesǁhandle_message_received__mutmut_3, 
        'xǁFilesǁhandle_message_received__mutmut_4': xǁFilesǁhandle_message_received__mutmut_4, 
        'xǁFilesǁhandle_message_received__mutmut_5': xǁFilesǁhandle_message_received__mutmut_5, 
        'xǁFilesǁhandle_message_received__mutmut_6': xǁFilesǁhandle_message_received__mutmut_6, 
        'xǁFilesǁhandle_message_received__mutmut_7': xǁFilesǁhandle_message_received__mutmut_7, 
        'xǁFilesǁhandle_message_received__mutmut_8': xǁFilesǁhandle_message_received__mutmut_8, 
        'xǁFilesǁhandle_message_received__mutmut_9': xǁFilesǁhandle_message_received__mutmut_9, 
        'xǁFilesǁhandle_message_received__mutmut_10': xǁFilesǁhandle_message_received__mutmut_10, 
        'xǁFilesǁhandle_message_received__mutmut_11': xǁFilesǁhandle_message_received__mutmut_11, 
        'xǁFilesǁhandle_message_received__mutmut_12': xǁFilesǁhandle_message_received__mutmut_12
    }
    xǁFilesǁhandle_message_received__mutmut_orig.__name__ = 'xǁFilesǁhandle_message_received'

    def _process_file_list(self, data: list) -> None:
        args = [data]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_process_file_list__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_process_file_list__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_process_file_list__mutmut_orig(self, data: list) -> None:
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

    def xǁFilesǁ_process_file_list__mutmut_1(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = None
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_2(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get(None, item.get("filename", ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_3(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", None)
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_4(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get(item.get("filename", ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_5(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", )
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_6(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("XXpathXX", item.get("filename", ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_7(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("PATH", item.get("filename", ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_8(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get(None, ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_9(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get("filename", None))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_10(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get(""))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_11(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get("filename", ))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_12(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get("XXfilenameXX", ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_13(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get("FILENAME", ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_14(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get("filename", "XXXX"))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_15(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get("filename", ""))
            if path:
                self._files[path] = None

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_16(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get("filename", ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = None
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_17(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get("filename", ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = False
        self.on_file_list.emit(self.file_list)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_18(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get("filename", ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(None)
        logger.info(f"Loaded {len(self._files)} files")
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_19(self, data: list) -> None:
        """Process full file list response."""
        self._files.clear()

        for item in data:
            path = item.get("path", item.get("filename", ""))
            if path:
                self._files[path] = item

        self._initial_load_complete = True
        self.on_file_list.emit(self.file_list)
        logger.info(None)
        # Request metadata only for gcode files (async update)
        for path in self._files:
            if path.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_20(self, data: list) -> None:
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
            if path.lower().endswith(None):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_21(self, data: list) -> None:
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
            if path.upper().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(path.removeprefix("/"))

    def xǁFilesǁ_process_file_list__mutmut_22(self, data: list) -> None:
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
                self.request_file_metadata.emit(None)

    def xǁFilesǁ_process_file_list__mutmut_23(self, data: list) -> None:
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
                self.request_file_metadata.emit(path.removeprefix(None))

    def xǁFilesǁ_process_file_list__mutmut_24(self, data: list) -> None:
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
                self.request_file_metadata.emit(path.removesuffix("/"))

    def xǁFilesǁ_process_file_list__mutmut_25(self, data: list) -> None:
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
                self.request_file_metadata.emit(path.removeprefix("XX/XX"))
    
    xǁFilesǁ_process_file_list__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_process_file_list__mutmut_1': xǁFilesǁ_process_file_list__mutmut_1, 
        'xǁFilesǁ_process_file_list__mutmut_2': xǁFilesǁ_process_file_list__mutmut_2, 
        'xǁFilesǁ_process_file_list__mutmut_3': xǁFilesǁ_process_file_list__mutmut_3, 
        'xǁFilesǁ_process_file_list__mutmut_4': xǁFilesǁ_process_file_list__mutmut_4, 
        'xǁFilesǁ_process_file_list__mutmut_5': xǁFilesǁ_process_file_list__mutmut_5, 
        'xǁFilesǁ_process_file_list__mutmut_6': xǁFilesǁ_process_file_list__mutmut_6, 
        'xǁFilesǁ_process_file_list__mutmut_7': xǁFilesǁ_process_file_list__mutmut_7, 
        'xǁFilesǁ_process_file_list__mutmut_8': xǁFilesǁ_process_file_list__mutmut_8, 
        'xǁFilesǁ_process_file_list__mutmut_9': xǁFilesǁ_process_file_list__mutmut_9, 
        'xǁFilesǁ_process_file_list__mutmut_10': xǁFilesǁ_process_file_list__mutmut_10, 
        'xǁFilesǁ_process_file_list__mutmut_11': xǁFilesǁ_process_file_list__mutmut_11, 
        'xǁFilesǁ_process_file_list__mutmut_12': xǁFilesǁ_process_file_list__mutmut_12, 
        'xǁFilesǁ_process_file_list__mutmut_13': xǁFilesǁ_process_file_list__mutmut_13, 
        'xǁFilesǁ_process_file_list__mutmut_14': xǁFilesǁ_process_file_list__mutmut_14, 
        'xǁFilesǁ_process_file_list__mutmut_15': xǁFilesǁ_process_file_list__mutmut_15, 
        'xǁFilesǁ_process_file_list__mutmut_16': xǁFilesǁ_process_file_list__mutmut_16, 
        'xǁFilesǁ_process_file_list__mutmut_17': xǁFilesǁ_process_file_list__mutmut_17, 
        'xǁFilesǁ_process_file_list__mutmut_18': xǁFilesǁ_process_file_list__mutmut_18, 
        'xǁFilesǁ_process_file_list__mutmut_19': xǁFilesǁ_process_file_list__mutmut_19, 
        'xǁFilesǁ_process_file_list__mutmut_20': xǁFilesǁ_process_file_list__mutmut_20, 
        'xǁFilesǁ_process_file_list__mutmut_21': xǁFilesǁ_process_file_list__mutmut_21, 
        'xǁFilesǁ_process_file_list__mutmut_22': xǁFilesǁ_process_file_list__mutmut_22, 
        'xǁFilesǁ_process_file_list__mutmut_23': xǁFilesǁ_process_file_list__mutmut_23, 
        'xǁFilesǁ_process_file_list__mutmut_24': xǁFilesǁ_process_file_list__mutmut_24, 
        'xǁFilesǁ_process_file_list__mutmut_25': xǁFilesǁ_process_file_list__mutmut_25
    }
    xǁFilesǁ_process_file_list__mutmut_orig.__name__ = 'xǁFilesǁ_process_file_list'

    def _process_metadata(self, data: dict) -> None:
        args = [data]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_process_metadata__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_process_metadata__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_process_metadata__mutmut_orig(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_1(self, data: dict) -> None:
        """Process file metadata response."""
        filename = None
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_2(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get(None)
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_3(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("XXfilenameXX")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_4(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("FILENAME")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_5(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_6(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = None
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_7(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get(None, [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_8(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", None)
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_9(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get([])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_10(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", )
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_11(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("XXthumbnailsXX", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_12(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("THUMBNAILS", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_13(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = None
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_14(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path * filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_15(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = None

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

    def xǁFilesǁ_process_metadata__mutmut_16(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(None)
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

    def xǁFilesǁ_process_metadata__mutmut_17(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir * t.get("relative_path", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_18(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get(None, ""))
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

    def xǁFilesǁ_process_metadata__mutmut_19(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", None))
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

    def xǁFilesǁ_process_metadata__mutmut_20(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get(""))
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

    def xǁFilesǁ_process_metadata__mutmut_21(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ))
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

    def xǁFilesǁ_process_metadata__mutmut_22(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("XXrelative_pathXX", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_23(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("RELATIVE_PATH", ""))
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

    def xǁFilesǁ_process_metadata__mutmut_24(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", "XXXX"))
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

    def xǁFilesǁ_process_metadata__mutmut_25(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) or t["relative_path"]
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

    def xǁFilesǁ_process_metadata__mutmut_26(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["XXrelative_pathXX"]
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

    def xǁFilesǁ_process_metadata__mutmut_27(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["RELATIVE_PATH"]
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

    def xǁFilesǁ_process_metadata__mutmut_28(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["relative_path"]
        ]

        # Load images, filtering out invalid files
        thumbnail_images = None
        for path in thumbnail_paths:
            image = QtGui.QImage(path)
            if not image.isNull():  # skip loading errors
                thumbnail_images.append(image)

        metadata = FileMetadata.from_dict(data, thumbnail_images)
        self._files_metadata[filename] = metadata

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_29(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["relative_path"]
        ]

        # Load images, filtering out invalid files
        thumbnail_images = []
        for path in thumbnail_paths:
            image = None
            if not image.isNull():  # skip loading errors
                thumbnail_images.append(image)

        metadata = FileMetadata.from_dict(data, thumbnail_images)
        self._files_metadata[filename] = metadata

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_30(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["relative_path"]
        ]

        # Load images, filtering out invalid files
        thumbnail_images = []
        for path in thumbnail_paths:
            image = QtGui.QImage(None)
            if not image.isNull():  # skip loading errors
                thumbnail_images.append(image)

        metadata = FileMetadata.from_dict(data, thumbnail_images)
        self._files_metadata[filename] = metadata

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_31(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["relative_path"]
        ]

        # Load images, filtering out invalid files
        thumbnail_images = []
        for path in thumbnail_paths:
            image = QtGui.QImage(path)
            if image.isNull():  # skip loading errors
                thumbnail_images.append(image)

        metadata = FileMetadata.from_dict(data, thumbnail_images)
        self._files_metadata[filename] = metadata

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_32(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["relative_path"]
        ]

        # Load images, filtering out invalid files
        thumbnail_images = []
        for path in thumbnail_paths:
            image = QtGui.QImage(path)
            if not image.isNull():  # skip loading errors
                thumbnail_images.append(None)

        metadata = FileMetadata.from_dict(data, thumbnail_images)
        self._files_metadata[filename] = metadata

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_33(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["relative_path"]
        ]

        # Load images, filtering out invalid files
        thumbnail_images = []
        for path in thumbnail_paths:
            image = QtGui.QImage(path)
            if not image.isNull():  # skip loading errors
                thumbnail_images.append(image)

        metadata = None
        self._files_metadata[filename] = metadata

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_34(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["relative_path"]
        ]

        # Load images, filtering out invalid files
        thumbnail_images = []
        for path in thumbnail_paths:
            image = QtGui.QImage(path)
            if not image.isNull():  # skip loading errors
                thumbnail_images.append(image)

        metadata = FileMetadata.from_dict(None, thumbnail_images)
        self._files_metadata[filename] = metadata

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_35(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["relative_path"]
        ]

        # Load images, filtering out invalid files
        thumbnail_images = []
        for path in thumbnail_paths:
            image = QtGui.QImage(path)
            if not image.isNull():  # skip loading errors
                thumbnail_images.append(image)

        metadata = FileMetadata.from_dict(data, None)
        self._files_metadata[filename] = metadata

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_36(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["relative_path"]
        ]

        # Load images, filtering out invalid files
        thumbnail_images = []
        for path in thumbnail_paths:
            image = QtGui.QImage(path)
            if not image.isNull():  # skip loading errors
                thumbnail_images.append(image)

        metadata = FileMetadata.from_dict(thumbnail_images)
        self._files_metadata[filename] = metadata

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_37(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
            for t in thumbnails
            if isinstance(t.get("relative_path", None), str) and t["relative_path"]
        ]

        # Load images, filtering out invalid files
        thumbnail_images = []
        for path in thumbnail_paths:
            image = QtGui.QImage(path)
            if not image.isNull():  # skip loading errors
                thumbnail_images.append(image)

        metadata = FileMetadata.from_dict(data, )
        self._files_metadata[filename] = metadata

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_38(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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
        self._files_metadata[filename] = None

        # Emit updated fileinfo
        self.fileinfo.emit(metadata.to_dict())
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_39(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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
        self.fileinfo.emit(None)
        logger.debug(f"Metadata loaded for: {filename}")

    def xǁFilesǁ_process_metadata__mutmut_40(self, data: dict) -> None:
        """Process file metadata response."""
        filename = data.get("filename")
        if not filename:
            return

        thumbnails = data.get("thumbnails", [])
        base_dir = (self.gcode_path / filename).parent
        thumbnail_paths = [
            str(base_dir / t.get("relative_path", ""))
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
        logger.debug(None)
    
    xǁFilesǁ_process_metadata__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_process_metadata__mutmut_1': xǁFilesǁ_process_metadata__mutmut_1, 
        'xǁFilesǁ_process_metadata__mutmut_2': xǁFilesǁ_process_metadata__mutmut_2, 
        'xǁFilesǁ_process_metadata__mutmut_3': xǁFilesǁ_process_metadata__mutmut_3, 
        'xǁFilesǁ_process_metadata__mutmut_4': xǁFilesǁ_process_metadata__mutmut_4, 
        'xǁFilesǁ_process_metadata__mutmut_5': xǁFilesǁ_process_metadata__mutmut_5, 
        'xǁFilesǁ_process_metadata__mutmut_6': xǁFilesǁ_process_metadata__mutmut_6, 
        'xǁFilesǁ_process_metadata__mutmut_7': xǁFilesǁ_process_metadata__mutmut_7, 
        'xǁFilesǁ_process_metadata__mutmut_8': xǁFilesǁ_process_metadata__mutmut_8, 
        'xǁFilesǁ_process_metadata__mutmut_9': xǁFilesǁ_process_metadata__mutmut_9, 
        'xǁFilesǁ_process_metadata__mutmut_10': xǁFilesǁ_process_metadata__mutmut_10, 
        'xǁFilesǁ_process_metadata__mutmut_11': xǁFilesǁ_process_metadata__mutmut_11, 
        'xǁFilesǁ_process_metadata__mutmut_12': xǁFilesǁ_process_metadata__mutmut_12, 
        'xǁFilesǁ_process_metadata__mutmut_13': xǁFilesǁ_process_metadata__mutmut_13, 
        'xǁFilesǁ_process_metadata__mutmut_14': xǁFilesǁ_process_metadata__mutmut_14, 
        'xǁFilesǁ_process_metadata__mutmut_15': xǁFilesǁ_process_metadata__mutmut_15, 
        'xǁFilesǁ_process_metadata__mutmut_16': xǁFilesǁ_process_metadata__mutmut_16, 
        'xǁFilesǁ_process_metadata__mutmut_17': xǁFilesǁ_process_metadata__mutmut_17, 
        'xǁFilesǁ_process_metadata__mutmut_18': xǁFilesǁ_process_metadata__mutmut_18, 
        'xǁFilesǁ_process_metadata__mutmut_19': xǁFilesǁ_process_metadata__mutmut_19, 
        'xǁFilesǁ_process_metadata__mutmut_20': xǁFilesǁ_process_metadata__mutmut_20, 
        'xǁFilesǁ_process_metadata__mutmut_21': xǁFilesǁ_process_metadata__mutmut_21, 
        'xǁFilesǁ_process_metadata__mutmut_22': xǁFilesǁ_process_metadata__mutmut_22, 
        'xǁFilesǁ_process_metadata__mutmut_23': xǁFilesǁ_process_metadata__mutmut_23, 
        'xǁFilesǁ_process_metadata__mutmut_24': xǁFilesǁ_process_metadata__mutmut_24, 
        'xǁFilesǁ_process_metadata__mutmut_25': xǁFilesǁ_process_metadata__mutmut_25, 
        'xǁFilesǁ_process_metadata__mutmut_26': xǁFilesǁ_process_metadata__mutmut_26, 
        'xǁFilesǁ_process_metadata__mutmut_27': xǁFilesǁ_process_metadata__mutmut_27, 
        'xǁFilesǁ_process_metadata__mutmut_28': xǁFilesǁ_process_metadata__mutmut_28, 
        'xǁFilesǁ_process_metadata__mutmut_29': xǁFilesǁ_process_metadata__mutmut_29, 
        'xǁFilesǁ_process_metadata__mutmut_30': xǁFilesǁ_process_metadata__mutmut_30, 
        'xǁFilesǁ_process_metadata__mutmut_31': xǁFilesǁ_process_metadata__mutmut_31, 
        'xǁFilesǁ_process_metadata__mutmut_32': xǁFilesǁ_process_metadata__mutmut_32, 
        'xǁFilesǁ_process_metadata__mutmut_33': xǁFilesǁ_process_metadata__mutmut_33, 
        'xǁFilesǁ_process_metadata__mutmut_34': xǁFilesǁ_process_metadata__mutmut_34, 
        'xǁFilesǁ_process_metadata__mutmut_35': xǁFilesǁ_process_metadata__mutmut_35, 
        'xǁFilesǁ_process_metadata__mutmut_36': xǁFilesǁ_process_metadata__mutmut_36, 
        'xǁFilesǁ_process_metadata__mutmut_37': xǁFilesǁ_process_metadata__mutmut_37, 
        'xǁFilesǁ_process_metadata__mutmut_38': xǁFilesǁ_process_metadata__mutmut_38, 
        'xǁFilesǁ_process_metadata__mutmut_39': xǁFilesǁ_process_metadata__mutmut_39, 
        'xǁFilesǁ_process_metadata__mutmut_40': xǁFilesǁ_process_metadata__mutmut_40
    }
    xǁFilesǁ_process_metadata__mutmut_orig.__name__ = 'xǁFilesǁ_process_metadata'

    def handle_metadata_error(self, error_data: typing.Union[str, dict]) -> None:
        args = [error_data]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁhandle_metadata_error__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁhandle_metadata_error__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁhandle_metadata_error__mutmut_orig(self, error_data: typing.Union[str, dict]) -> None:
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

    def xǁFilesǁhandle_metadata_error__mutmut_1(self, error_data: typing.Union[str, dict]) -> None:
        """
        Handle metadata request error from Moonraker.

        Parses the filename from the error message and emits metadata_error signal.
        Called directly from MainWindow error handler.

        Args:
            error_data: The error message string or dict from Moonraker
        """
        if error_data:
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

    def xǁFilesǁhandle_metadata_error__mutmut_2(self, error_data: typing.Union[str, dict]) -> None:
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
            text = None
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

    def xǁFilesǁhandle_metadata_error__mutmut_3(self, error_data: typing.Union[str, dict]) -> None:
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
            text = error_data.get(None, str(error_data))
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

    def xǁFilesǁhandle_metadata_error__mutmut_4(self, error_data: typing.Union[str, dict]) -> None:
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
            text = error_data.get("message", None)
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

    def xǁFilesǁhandle_metadata_error__mutmut_5(self, error_data: typing.Union[str, dict]) -> None:
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
            text = error_data.get(str(error_data))
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

    def xǁFilesǁhandle_metadata_error__mutmut_6(self, error_data: typing.Union[str, dict]) -> None:
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
            text = error_data.get("message", )
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

    def xǁFilesǁhandle_metadata_error__mutmut_7(self, error_data: typing.Union[str, dict]) -> None:
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
            text = error_data.get("XXmessageXX", str(error_data))
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

    def xǁFilesǁhandle_metadata_error__mutmut_8(self, error_data: typing.Union[str, dict]) -> None:
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
            text = error_data.get("MESSAGE", str(error_data))
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

    def xǁFilesǁhandle_metadata_error__mutmut_9(self, error_data: typing.Union[str, dict]) -> None:
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
            text = error_data.get("message", str(None))
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

    def xǁFilesǁhandle_metadata_error__mutmut_10(self, error_data: typing.Union[str, dict]) -> None:
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
            text = None

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

    def xǁFilesǁhandle_metadata_error__mutmut_11(self, error_data: typing.Union[str, dict]) -> None:
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
            text = str(None)

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

    def xǁFilesǁhandle_metadata_error__mutmut_12(self, error_data: typing.Union[str, dict]) -> None:
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

        if "XXmetadataXX" not in text.lower():
            return

        # Parse filename from error message (format: <filename>)
        start = text.find("<") + 1
        end = text.find(">", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_13(self, error_data: typing.Union[str, dict]) -> None:
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

        if "METADATA" not in text.lower():
            return

        # Parse filename from error message (format: <filename>)
        start = text.find("<") + 1
        end = text.find(">", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_14(self, error_data: typing.Union[str, dict]) -> None:
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

        if "metadata" in text.lower():
            return

        # Parse filename from error message (format: <filename>)
        start = text.find("<") + 1
        end = text.find(">", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_15(self, error_data: typing.Union[str, dict]) -> None:
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

        if "metadata" not in text.upper():
            return

        # Parse filename from error message (format: <filename>)
        start = text.find("<") + 1
        end = text.find(">", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_16(self, error_data: typing.Union[str, dict]) -> None:
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
        start = None
        end = text.find(">", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_17(self, error_data: typing.Union[str, dict]) -> None:
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
        start = text.find("<") - 1
        end = text.find(">", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_18(self, error_data: typing.Union[str, dict]) -> None:
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
        start = text.find(None) + 1
        end = text.find(">", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_19(self, error_data: typing.Union[str, dict]) -> None:
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
        start = text.rfind("<") + 1
        end = text.find(">", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_20(self, error_data: typing.Union[str, dict]) -> None:
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
        start = text.find("XX<XX") + 1
        end = text.find(">", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_21(self, error_data: typing.Union[str, dict]) -> None:
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
        start = text.find("<") + 2
        end = text.find(">", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_22(self, error_data: typing.Union[str, dict]) -> None:
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
        end = None

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_23(self, error_data: typing.Union[str, dict]) -> None:
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
        end = text.find(None, start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_24(self, error_data: typing.Union[str, dict]) -> None:
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
        end = text.find(">", None)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_25(self, error_data: typing.Union[str, dict]) -> None:
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
        end = text.find(start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_26(self, error_data: typing.Union[str, dict]) -> None:
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
        end = text.find(">", )

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_27(self, error_data: typing.Union[str, dict]) -> None:
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
        end = text.rfind(">", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_28(self, error_data: typing.Union[str, dict]) -> None:
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
        end = text.find("XX>XX", start)

        if start > 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_29(self, error_data: typing.Union[str, dict]) -> None:
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

        if start > 0 or end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_30(self, error_data: typing.Union[str, dict]) -> None:
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

        if start >= 0 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_31(self, error_data: typing.Union[str, dict]) -> None:
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

        if start > 1 and end > start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_32(self, error_data: typing.Union[str, dict]) -> None:
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

        if start > 0 and end >= start:
            filename = text[start:end]
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_33(self, error_data: typing.Union[str, dict]) -> None:
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
            filename = None
            clean_filename = filename.removeprefix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_34(self, error_data: typing.Union[str, dict]) -> None:
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
            clean_filename = None
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_35(self, error_data: typing.Union[str, dict]) -> None:
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
            clean_filename = filename.removeprefix(None)
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_36(self, error_data: typing.Union[str, dict]) -> None:
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
            clean_filename = filename.removesuffix("/")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_37(self, error_data: typing.Union[str, dict]) -> None:
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
            clean_filename = filename.removeprefix("XX/XX")
            self.metadata_error.emit(clean_filename)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_38(self, error_data: typing.Union[str, dict]) -> None:
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
            self.metadata_error.emit(None)
            logger.debug(f"Metadata error for: {clean_filename}")

    def xǁFilesǁhandle_metadata_error__mutmut_39(self, error_data: typing.Union[str, dict]) -> None:
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
            logger.debug(None)
    
    xǁFilesǁhandle_metadata_error__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁhandle_metadata_error__mutmut_1': xǁFilesǁhandle_metadata_error__mutmut_1, 
        'xǁFilesǁhandle_metadata_error__mutmut_2': xǁFilesǁhandle_metadata_error__mutmut_2, 
        'xǁFilesǁhandle_metadata_error__mutmut_3': xǁFilesǁhandle_metadata_error__mutmut_3, 
        'xǁFilesǁhandle_metadata_error__mutmut_4': xǁFilesǁhandle_metadata_error__mutmut_4, 
        'xǁFilesǁhandle_metadata_error__mutmut_5': xǁFilesǁhandle_metadata_error__mutmut_5, 
        'xǁFilesǁhandle_metadata_error__mutmut_6': xǁFilesǁhandle_metadata_error__mutmut_6, 
        'xǁFilesǁhandle_metadata_error__mutmut_7': xǁFilesǁhandle_metadata_error__mutmut_7, 
        'xǁFilesǁhandle_metadata_error__mutmut_8': xǁFilesǁhandle_metadata_error__mutmut_8, 
        'xǁFilesǁhandle_metadata_error__mutmut_9': xǁFilesǁhandle_metadata_error__mutmut_9, 
        'xǁFilesǁhandle_metadata_error__mutmut_10': xǁFilesǁhandle_metadata_error__mutmut_10, 
        'xǁFilesǁhandle_metadata_error__mutmut_11': xǁFilesǁhandle_metadata_error__mutmut_11, 
        'xǁFilesǁhandle_metadata_error__mutmut_12': xǁFilesǁhandle_metadata_error__mutmut_12, 
        'xǁFilesǁhandle_metadata_error__mutmut_13': xǁFilesǁhandle_metadata_error__mutmut_13, 
        'xǁFilesǁhandle_metadata_error__mutmut_14': xǁFilesǁhandle_metadata_error__mutmut_14, 
        'xǁFilesǁhandle_metadata_error__mutmut_15': xǁFilesǁhandle_metadata_error__mutmut_15, 
        'xǁFilesǁhandle_metadata_error__mutmut_16': xǁFilesǁhandle_metadata_error__mutmut_16, 
        'xǁFilesǁhandle_metadata_error__mutmut_17': xǁFilesǁhandle_metadata_error__mutmut_17, 
        'xǁFilesǁhandle_metadata_error__mutmut_18': xǁFilesǁhandle_metadata_error__mutmut_18, 
        'xǁFilesǁhandle_metadata_error__mutmut_19': xǁFilesǁhandle_metadata_error__mutmut_19, 
        'xǁFilesǁhandle_metadata_error__mutmut_20': xǁFilesǁhandle_metadata_error__mutmut_20, 
        'xǁFilesǁhandle_metadata_error__mutmut_21': xǁFilesǁhandle_metadata_error__mutmut_21, 
        'xǁFilesǁhandle_metadata_error__mutmut_22': xǁFilesǁhandle_metadata_error__mutmut_22, 
        'xǁFilesǁhandle_metadata_error__mutmut_23': xǁFilesǁhandle_metadata_error__mutmut_23, 
        'xǁFilesǁhandle_metadata_error__mutmut_24': xǁFilesǁhandle_metadata_error__mutmut_24, 
        'xǁFilesǁhandle_metadata_error__mutmut_25': xǁFilesǁhandle_metadata_error__mutmut_25, 
        'xǁFilesǁhandle_metadata_error__mutmut_26': xǁFilesǁhandle_metadata_error__mutmut_26, 
        'xǁFilesǁhandle_metadata_error__mutmut_27': xǁFilesǁhandle_metadata_error__mutmut_27, 
        'xǁFilesǁhandle_metadata_error__mutmut_28': xǁFilesǁhandle_metadata_error__mutmut_28, 
        'xǁFilesǁhandle_metadata_error__mutmut_29': xǁFilesǁhandle_metadata_error__mutmut_29, 
        'xǁFilesǁhandle_metadata_error__mutmut_30': xǁFilesǁhandle_metadata_error__mutmut_30, 
        'xǁFilesǁhandle_metadata_error__mutmut_31': xǁFilesǁhandle_metadata_error__mutmut_31, 
        'xǁFilesǁhandle_metadata_error__mutmut_32': xǁFilesǁhandle_metadata_error__mutmut_32, 
        'xǁFilesǁhandle_metadata_error__mutmut_33': xǁFilesǁhandle_metadata_error__mutmut_33, 
        'xǁFilesǁhandle_metadata_error__mutmut_34': xǁFilesǁhandle_metadata_error__mutmut_34, 
        'xǁFilesǁhandle_metadata_error__mutmut_35': xǁFilesǁhandle_metadata_error__mutmut_35, 
        'xǁFilesǁhandle_metadata_error__mutmut_36': xǁFilesǁhandle_metadata_error__mutmut_36, 
        'xǁFilesǁhandle_metadata_error__mutmut_37': xǁFilesǁhandle_metadata_error__mutmut_37, 
        'xǁFilesǁhandle_metadata_error__mutmut_38': xǁFilesǁhandle_metadata_error__mutmut_38, 
        'xǁFilesǁhandle_metadata_error__mutmut_39': xǁFilesǁhandle_metadata_error__mutmut_39
    }
    xǁFilesǁhandle_metadata_error__mutmut_orig.__name__ = 'xǁFilesǁhandle_metadata_error'

    def _preload_usb_contents(self, usb_path: str) -> None:
        args = [usb_path]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_preload_usb_contents__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_preload_usb_contents__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_preload_usb_contents__mutmut_orig(self, usb_path: str) -> None:
        """
        Preload USB contents when USB is inserted.

        Requests directory info for the USB mount so files are ready
        when user navigates to it.

        Args:
            usb_path: The USB mount path (e.g., "USB-sda1")
        """
        logger.info(f"Preloading USB contents: {usb_path}")
        self._pending_usb_preloads.add(usb_path)
        self._usb_preload_queue.append(usb_path)
        self.ws.api.get_dir_information(usb_path, True)

    def xǁFilesǁ_preload_usb_contents__mutmut_1(self, usb_path: str) -> None:
        """
        Preload USB contents when USB is inserted.

        Requests directory info for the USB mount so files are ready
        when user navigates to it.

        Args:
            usb_path: The USB mount path (e.g., "USB-sda1")
        """
        logger.info(None)
        self._pending_usb_preloads.add(usb_path)
        self._usb_preload_queue.append(usb_path)
        self.ws.api.get_dir_information(usb_path, True)

    def xǁFilesǁ_preload_usb_contents__mutmut_2(self, usb_path: str) -> None:
        """
        Preload USB contents when USB is inserted.

        Requests directory info for the USB mount so files are ready
        when user navigates to it.

        Args:
            usb_path: The USB mount path (e.g., "USB-sda1")
        """
        logger.info(f"Preloading USB contents: {usb_path}")
        self._pending_usb_preloads.add(None)
        self._usb_preload_queue.append(usb_path)
        self.ws.api.get_dir_information(usb_path, True)

    def xǁFilesǁ_preload_usb_contents__mutmut_3(self, usb_path: str) -> None:
        """
        Preload USB contents when USB is inserted.

        Requests directory info for the USB mount so files are ready
        when user navigates to it.

        Args:
            usb_path: The USB mount path (e.g., "USB-sda1")
        """
        logger.info(f"Preloading USB contents: {usb_path}")
        self._pending_usb_preloads.add(usb_path)
        self._usb_preload_queue.append(None)
        self.ws.api.get_dir_information(usb_path, True)

    def xǁFilesǁ_preload_usb_contents__mutmut_4(self, usb_path: str) -> None:
        """
        Preload USB contents when USB is inserted.

        Requests directory info for the USB mount so files are ready
        when user navigates to it.

        Args:
            usb_path: The USB mount path (e.g., "USB-sda1")
        """
        logger.info(f"Preloading USB contents: {usb_path}")
        self._pending_usb_preloads.add(usb_path)
        self._usb_preload_queue.append(usb_path)
        self.ws.api.get_dir_information(None, True)

    def xǁFilesǁ_preload_usb_contents__mutmut_5(self, usb_path: str) -> None:
        """
        Preload USB contents when USB is inserted.

        Requests directory info for the USB mount so files are ready
        when user navigates to it.

        Args:
            usb_path: The USB mount path (e.g., "USB-sda1")
        """
        logger.info(f"Preloading USB contents: {usb_path}")
        self._pending_usb_preloads.add(usb_path)
        self._usb_preload_queue.append(usb_path)
        self.ws.api.get_dir_information(usb_path, None)

    def xǁFilesǁ_preload_usb_contents__mutmut_6(self, usb_path: str) -> None:
        """
        Preload USB contents when USB is inserted.

        Requests directory info for the USB mount so files are ready
        when user navigates to it.

        Args:
            usb_path: The USB mount path (e.g., "USB-sda1")
        """
        logger.info(f"Preloading USB contents: {usb_path}")
        self._pending_usb_preloads.add(usb_path)
        self._usb_preload_queue.append(usb_path)
        self.ws.api.get_dir_information(True)

    def xǁFilesǁ_preload_usb_contents__mutmut_7(self, usb_path: str) -> None:
        """
        Preload USB contents when USB is inserted.

        Requests directory info for the USB mount so files are ready
        when user navigates to it.

        Args:
            usb_path: The USB mount path (e.g., "USB-sda1")
        """
        logger.info(f"Preloading USB contents: {usb_path}")
        self._pending_usb_preloads.add(usb_path)
        self._usb_preload_queue.append(usb_path)
        self.ws.api.get_dir_information(usb_path, )

    def xǁFilesǁ_preload_usb_contents__mutmut_8(self, usb_path: str) -> None:
        """
        Preload USB contents when USB is inserted.

        Requests directory info for the USB mount so files are ready
        when user navigates to it.

        Args:
            usb_path: The USB mount path (e.g., "USB-sda1")
        """
        logger.info(f"Preloading USB contents: {usb_path}")
        self._pending_usb_preloads.add(usb_path)
        self._usb_preload_queue.append(usb_path)
        self.ws.api.get_dir_information(usb_path, False)
    
    xǁFilesǁ_preload_usb_contents__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_preload_usb_contents__mutmut_1': xǁFilesǁ_preload_usb_contents__mutmut_1, 
        'xǁFilesǁ_preload_usb_contents__mutmut_2': xǁFilesǁ_preload_usb_contents__mutmut_2, 
        'xǁFilesǁ_preload_usb_contents__mutmut_3': xǁFilesǁ_preload_usb_contents__mutmut_3, 
        'xǁFilesǁ_preload_usb_contents__mutmut_4': xǁFilesǁ_preload_usb_contents__mutmut_4, 
        'xǁFilesǁ_preload_usb_contents__mutmut_5': xǁFilesǁ_preload_usb_contents__mutmut_5, 
        'xǁFilesǁ_preload_usb_contents__mutmut_6': xǁFilesǁ_preload_usb_contents__mutmut_6, 
        'xǁFilesǁ_preload_usb_contents__mutmut_7': xǁFilesǁ_preload_usb_contents__mutmut_7, 
        'xǁFilesǁ_preload_usb_contents__mutmut_8': xǁFilesǁ_preload_usb_contents__mutmut_8
    }
    xǁFilesǁ_preload_usb_contents__mutmut_orig.__name__ = 'xǁFilesǁ_preload_usb_contents'

    def get_cached_usb_files(self, usb_path: str) -> typing.Optional[list[dict]]:
        args = [usb_path]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁget_cached_usb_files__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁget_cached_usb_files__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁget_cached_usb_files__mutmut_orig(self, usb_path: str) -> typing.Optional[list[dict]]:
        """
        Get cached files for a USB path if available.

        Args:
            usb_path: The USB mount path

        Returns:
            List of file dicts if cached, None otherwise
        """
        return self._usb_files_cache.get(usb_path.removeprefix("/"))

    def xǁFilesǁget_cached_usb_files__mutmut_1(self, usb_path: str) -> typing.Optional[list[dict]]:
        """
        Get cached files for a USB path if available.

        Args:
            usb_path: The USB mount path

        Returns:
            List of file dicts if cached, None otherwise
        """
        return self._usb_files_cache.get(None)

    def xǁFilesǁget_cached_usb_files__mutmut_2(self, usb_path: str) -> typing.Optional[list[dict]]:
        """
        Get cached files for a USB path if available.

        Args:
            usb_path: The USB mount path

        Returns:
            List of file dicts if cached, None otherwise
        """
        return self._usb_files_cache.get(usb_path.removeprefix(None))

    def xǁFilesǁget_cached_usb_files__mutmut_3(self, usb_path: str) -> typing.Optional[list[dict]]:
        """
        Get cached files for a USB path if available.

        Args:
            usb_path: The USB mount path

        Returns:
            List of file dicts if cached, None otherwise
        """
        return self._usb_files_cache.get(usb_path.removesuffix("/"))

    def xǁFilesǁget_cached_usb_files__mutmut_4(self, usb_path: str) -> typing.Optional[list[dict]]:
        """
        Get cached files for a USB path if available.

        Args:
            usb_path: The USB mount path

        Returns:
            List of file dicts if cached, None otherwise
        """
        return self._usb_files_cache.get(usb_path.removeprefix("XX/XX"))
    
    xǁFilesǁget_cached_usb_files__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁget_cached_usb_files__mutmut_1': xǁFilesǁget_cached_usb_files__mutmut_1, 
        'xǁFilesǁget_cached_usb_files__mutmut_2': xǁFilesǁget_cached_usb_files__mutmut_2, 
        'xǁFilesǁget_cached_usb_files__mutmut_3': xǁFilesǁget_cached_usb_files__mutmut_3, 
        'xǁFilesǁget_cached_usb_files__mutmut_4': xǁFilesǁget_cached_usb_files__mutmut_4
    }
    xǁFilesǁget_cached_usb_files__mutmut_orig.__name__ = 'xǁFilesǁget_cached_usb_files'

    def _process_usb_directory_info(self, usb_path: str, data: dict) -> None:
        args = [usb_path, data]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_process_usb_directory_info__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_process_usb_directory_info__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_process_usb_directory_info__mutmut_orig(self, usb_path: str, data: dict) -> None:
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

    def xǁFilesǁ_process_usb_directory_info__mutmut_1(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = None
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

    def xǁFilesǁ_process_usb_directory_info__mutmut_2(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get(None, []):
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

    def xǁFilesǁ_process_usb_directory_info__mutmut_3(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", None):
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

    def xǁFilesǁ_process_usb_directory_info__mutmut_4(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get([]):
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

    def xǁFilesǁ_process_usb_directory_info__mutmut_5(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", ):
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

    def xǁFilesǁ_process_usb_directory_info__mutmut_6(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("XXfilesXX", []):
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

    def xǁFilesǁ_process_usb_directory_info__mutmut_7(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("FILES", []):
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

    def xǁFilesǁ_process_usb_directory_info__mutmut_8(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = None
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_9(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get(None, file_data.get("path", ""))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_10(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("filename", None)
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_11(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get(file_data.get("path", ""))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_12(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("filename", )
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_13(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("XXfilenameXX", file_data.get("path", ""))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_14(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("FILENAME", file_data.get("path", ""))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_15(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get(None, ""))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_16(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get("path", None))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_17(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get(""))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_18(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get("path", ))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_19(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get("XXpathXX", ""))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_20(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get("PATH", ""))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_21(self, usb_path: str, data: dict) -> None:
        """
        Process preloaded USB directory info.

        Caches the files and requests metadata for gcode files.

        Args:
            usb_path: The USB mount path
            data: Directory info response from Moonraker
        """
        files = []
        for file_data in data.get("files", []):
            filename = file_data.get("filename", file_data.get("path", "XXXX"))
            if filename:
                files.append(file_data)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_22(self, usb_path: str, data: dict) -> None:
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
                files.append(None)

                full_path = f"{usb_path}/{filename}"
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_23(self, usb_path: str, data: dict) -> None:
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

                full_path = None
                if filename.lower().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_24(self, usb_path: str, data: dict) -> None:
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
                if filename.lower().endswith(None):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_25(self, usb_path: str, data: dict) -> None:
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
                if filename.upper().endswith(self.GCODE_EXTENSION):
                    self.request_file_metadata.emit(full_path)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_26(self, usb_path: str, data: dict) -> None:
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
                    self.request_file_metadata.emit(None)

        # Cache the files
        self._usb_files_cache[usb_path] = files
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_27(self, usb_path: str, data: dict) -> None:
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
        self._usb_files_cache[usb_path] = None
        self.usb_files_loaded.emit(usb_path, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_28(self, usb_path: str, data: dict) -> None:
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
        self.usb_files_loaded.emit(None, files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_29(self, usb_path: str, data: dict) -> None:
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
        self.usb_files_loaded.emit(usb_path, None)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_30(self, usb_path: str, data: dict) -> None:
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
        self.usb_files_loaded.emit(files)
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_31(self, usb_path: str, data: dict) -> None:
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
        self.usb_files_loaded.emit(usb_path, )
        logger.info(f"Preloaded {len(files)} files from USB: {usb_path}")

    def xǁFilesǁ_process_usb_directory_info__mutmut_32(self, usb_path: str, data: dict) -> None:
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
        logger.info(None)
    
    xǁFilesǁ_process_usb_directory_info__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_process_usb_directory_info__mutmut_1': xǁFilesǁ_process_usb_directory_info__mutmut_1, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_2': xǁFilesǁ_process_usb_directory_info__mutmut_2, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_3': xǁFilesǁ_process_usb_directory_info__mutmut_3, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_4': xǁFilesǁ_process_usb_directory_info__mutmut_4, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_5': xǁFilesǁ_process_usb_directory_info__mutmut_5, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_6': xǁFilesǁ_process_usb_directory_info__mutmut_6, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_7': xǁFilesǁ_process_usb_directory_info__mutmut_7, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_8': xǁFilesǁ_process_usb_directory_info__mutmut_8, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_9': xǁFilesǁ_process_usb_directory_info__mutmut_9, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_10': xǁFilesǁ_process_usb_directory_info__mutmut_10, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_11': xǁFilesǁ_process_usb_directory_info__mutmut_11, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_12': xǁFilesǁ_process_usb_directory_info__mutmut_12, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_13': xǁFilesǁ_process_usb_directory_info__mutmut_13, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_14': xǁFilesǁ_process_usb_directory_info__mutmut_14, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_15': xǁFilesǁ_process_usb_directory_info__mutmut_15, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_16': xǁFilesǁ_process_usb_directory_info__mutmut_16, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_17': xǁFilesǁ_process_usb_directory_info__mutmut_17, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_18': xǁFilesǁ_process_usb_directory_info__mutmut_18, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_19': xǁFilesǁ_process_usb_directory_info__mutmut_19, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_20': xǁFilesǁ_process_usb_directory_info__mutmut_20, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_21': xǁFilesǁ_process_usb_directory_info__mutmut_21, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_22': xǁFilesǁ_process_usb_directory_info__mutmut_22, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_23': xǁFilesǁ_process_usb_directory_info__mutmut_23, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_24': xǁFilesǁ_process_usb_directory_info__mutmut_24, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_25': xǁFilesǁ_process_usb_directory_info__mutmut_25, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_26': xǁFilesǁ_process_usb_directory_info__mutmut_26, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_27': xǁFilesǁ_process_usb_directory_info__mutmut_27, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_28': xǁFilesǁ_process_usb_directory_info__mutmut_28, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_29': xǁFilesǁ_process_usb_directory_info__mutmut_29, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_30': xǁFilesǁ_process_usb_directory_info__mutmut_30, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_31': xǁFilesǁ_process_usb_directory_info__mutmut_31, 
        'xǁFilesǁ_process_usb_directory_info__mutmut_32': xǁFilesǁ_process_usb_directory_info__mutmut_32
    }
    xǁFilesǁ_process_usb_directory_info__mutmut_orig.__name__ = 'xǁFilesǁ_process_usb_directory_info'

    def _process_directory_info(self, data: dict) -> None:
        args = [data]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_process_directory_info__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_process_directory_info__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_process_directory_info__mutmut_orig(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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

    def xǁFilesǁ_process_directory_info__mutmut_1(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = ""

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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

    def xǁFilesǁ_process_directory_info__mutmut_2(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = None
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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

    def xǁFilesǁ_process_directory_info__mutmut_3(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate not in self._pending_usb_preloads:
                matched_usb = candidate

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

    def xǁFilesǁ_process_directory_info__mutmut_4(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = None

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

    def xǁFilesǁ_process_directory_info__mutmut_5(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(None)
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

    def xǁFilesǁ_process_directory_info__mutmut_6(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(None, data)
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

    def xǁFilesǁ_process_directory_info__mutmut_7(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, None)
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

    def xǁFilesǁ_process_directory_info__mutmut_8(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(data)
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

    def xǁFilesǁ_process_directory_info__mutmut_9(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, )
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

    def xǁFilesǁ_process_directory_info__mutmut_10(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get(None, []):
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

    def xǁFilesǁ_process_directory_info__mutmut_11(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", None):
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

    def xǁFilesǁ_process_directory_info__mutmut_12(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get([]):
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

    def xǁFilesǁ_process_directory_info__mutmut_13(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", ):
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

    def xǁFilesǁ_process_directory_info__mutmut_14(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("XXdirsXX", []):
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

    def xǁFilesǁ_process_directory_info__mutmut_15(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("DIRS", []):
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

    def xǁFilesǁ_process_directory_info__mutmut_16(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = None
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

    def xǁFilesǁ_process_directory_info__mutmut_17(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get(None, "")
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

    def xǁFilesǁ_process_directory_info__mutmut_18(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("dirname", None)
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

    def xǁFilesǁ_process_directory_info__mutmut_19(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("")
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

    def xǁFilesǁ_process_directory_info__mutmut_20(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("dirname", )
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

    def xǁFilesǁ_process_directory_info__mutmut_21(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("XXdirnameXX", "")
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

    def xǁFilesǁ_process_directory_info__mutmut_22(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("DIRNAME", "")
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

    def xǁFilesǁ_process_directory_info__mutmut_23(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("dirname", "XXXX")
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

    def xǁFilesǁ_process_directory_info__mutmut_24(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("dirname", "")
            if dirname or not dirname.startswith("."):
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

    def xǁFilesǁ_process_directory_info__mutmut_25(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("dirname", "")
            if dirname and dirname.startswith("."):
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

    def xǁFilesǁ_process_directory_info__mutmut_26(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("dirname", "")
            if dirname and not dirname.startswith(None):
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

    def xǁFilesǁ_process_directory_info__mutmut_27(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("dirname", "")
            if dirname and not dirname.startswith("XX.XX"):
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

    def xǁFilesǁ_process_directory_info__mutmut_28(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

        if matched_usb:
            self._pending_usb_preloads.discard(matched_usb)
            self._process_usb_directory_info(matched_usb, data)
            return

        self._directories.clear()
        self._files.clear()

        for dir_data in data.get("dirs", []):
            dirname = dir_data.get("dirname", "")
            if dirname and not dirname.startswith("."):
                self._directories[dirname] = None

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

    def xǁFilesǁ_process_directory_info__mutmut_29(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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

        for file_data in data.get(None, []):
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

    def xǁFilesǁ_process_directory_info__mutmut_30(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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

        for file_data in data.get("files", None):
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

    def xǁFilesǁ_process_directory_info__mutmut_31(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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

        for file_data in data.get([]):
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

    def xǁFilesǁ_process_directory_info__mutmut_32(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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

        for file_data in data.get("files", ):
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

    def xǁFilesǁ_process_directory_info__mutmut_33(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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

        for file_data in data.get("XXfilesXX", []):
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

    def xǁFilesǁ_process_directory_info__mutmut_34(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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

        for file_data in data.get("FILES", []):
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

    def xǁFilesǁ_process_directory_info__mutmut_35(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = None
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

    def xǁFilesǁ_process_directory_info__mutmut_36(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get(None, file_data.get("path", ""))
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

    def xǁFilesǁ_process_directory_info__mutmut_37(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get("filename", None)
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

    def xǁFilesǁ_process_directory_info__mutmut_38(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get(file_data.get("path", ""))
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

    def xǁFilesǁ_process_directory_info__mutmut_39(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get("filename", )
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

    def xǁFilesǁ_process_directory_info__mutmut_40(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get("XXfilenameXX", file_data.get("path", ""))
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

    def xǁFilesǁ_process_directory_info__mutmut_41(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get("FILENAME", file_data.get("path", ""))
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

    def xǁFilesǁ_process_directory_info__mutmut_42(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get("filename", file_data.get(None, ""))
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

    def xǁFilesǁ_process_directory_info__mutmut_43(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get("filename", file_data.get("path", None))
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

    def xǁFilesǁ_process_directory_info__mutmut_44(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get("filename", file_data.get(""))
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

    def xǁFilesǁ_process_directory_info__mutmut_45(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get("filename", file_data.get("path", ))
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

    def xǁFilesǁ_process_directory_info__mutmut_46(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get("filename", file_data.get("XXpathXX", ""))
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

    def xǁFilesǁ_process_directory_info__mutmut_47(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get("filename", file_data.get("PATH", ""))
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

    def xǁFilesǁ_process_directory_info__mutmut_48(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            filename = file_data.get("filename", file_data.get("path", "XXXX"))
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

    def xǁFilesǁ_process_directory_info__mutmut_49(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
                self._files[filename] = None

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

    def xǁFilesǁ_process_directory_info__mutmut_50(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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

        self.on_file_list.emit(None)
        self.on_dirs.emit(self.directories)
        self._initial_load_complete = True

        logger.info(
            f"Directory loaded: {len(self._directories)} dirs, {len(self._files)} files"
        )

        # Request metadata only for gcode files (async update)
        for filename in self._files:
            if filename.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(filename.removeprefix("/"))

    def xǁFilesǁ_process_directory_info__mutmut_51(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
        self.on_dirs.emit(None)
        self._initial_load_complete = True

        logger.info(
            f"Directory loaded: {len(self._directories)} dirs, {len(self._files)} files"
        )

        # Request metadata only for gcode files (async update)
        for filename in self._files:
            if filename.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(filename.removeprefix("/"))

    def xǁFilesǁ_process_directory_info__mutmut_52(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
        self._initial_load_complete = None

        logger.info(
            f"Directory loaded: {len(self._directories)} dirs, {len(self._files)} files"
        )

        # Request metadata only for gcode files (async update)
        for filename in self._files:
            if filename.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(filename.removeprefix("/"))

    def xǁFilesǁ_process_directory_info__mutmut_53(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
        self._initial_load_complete = False

        logger.info(
            f"Directory loaded: {len(self._directories)} dirs, {len(self._files)} files"
        )

        # Request metadata only for gcode files (async update)
        for filename in self._files:
            if filename.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(filename.removeprefix("/"))

    def xǁFilesǁ_process_directory_info__mutmut_54(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            None
        )

        # Request metadata only for gcode files (async update)
        for filename in self._files:
            if filename.lower().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(filename.removeprefix("/"))

    def xǁFilesǁ_process_directory_info__mutmut_55(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            if filename.lower().endswith(None):
                self.request_file_metadata.emit(filename.removeprefix("/"))

    def xǁFilesǁ_process_directory_info__mutmut_56(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
            if filename.upper().endswith(self.GCODE_EXTENSION):
                self.request_file_metadata.emit(filename.removeprefix("/"))

    def xǁFilesǁ_process_directory_info__mutmut_57(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
                self.request_file_metadata.emit(None)

    def xǁFilesǁ_process_directory_info__mutmut_58(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
                self.request_file_metadata.emit(filename.removeprefix(None))

    def xǁFilesǁ_process_directory_info__mutmut_59(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
                self.request_file_metadata.emit(filename.removesuffix("/"))

    def xǁFilesǁ_process_directory_info__mutmut_60(self, data: dict) -> None:
        """Process directory info response."""
        # Check if this is a USB preload response.
        # Match by FIFO queue — Moonraker responds to get_dir_information in order.
        matched_usb = None

        if self._usb_preload_queue:
            candidate = self._usb_preload_queue.popleft()
            if candidate in self._pending_usb_preloads:
                matched_usb = candidate

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
                self.request_file_metadata.emit(filename.removeprefix("XX/XX"))
    
    xǁFilesǁ_process_directory_info__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_process_directory_info__mutmut_1': xǁFilesǁ_process_directory_info__mutmut_1, 
        'xǁFilesǁ_process_directory_info__mutmut_2': xǁFilesǁ_process_directory_info__mutmut_2, 
        'xǁFilesǁ_process_directory_info__mutmut_3': xǁFilesǁ_process_directory_info__mutmut_3, 
        'xǁFilesǁ_process_directory_info__mutmut_4': xǁFilesǁ_process_directory_info__mutmut_4, 
        'xǁFilesǁ_process_directory_info__mutmut_5': xǁFilesǁ_process_directory_info__mutmut_5, 
        'xǁFilesǁ_process_directory_info__mutmut_6': xǁFilesǁ_process_directory_info__mutmut_6, 
        'xǁFilesǁ_process_directory_info__mutmut_7': xǁFilesǁ_process_directory_info__mutmut_7, 
        'xǁFilesǁ_process_directory_info__mutmut_8': xǁFilesǁ_process_directory_info__mutmut_8, 
        'xǁFilesǁ_process_directory_info__mutmut_9': xǁFilesǁ_process_directory_info__mutmut_9, 
        'xǁFilesǁ_process_directory_info__mutmut_10': xǁFilesǁ_process_directory_info__mutmut_10, 
        'xǁFilesǁ_process_directory_info__mutmut_11': xǁFilesǁ_process_directory_info__mutmut_11, 
        'xǁFilesǁ_process_directory_info__mutmut_12': xǁFilesǁ_process_directory_info__mutmut_12, 
        'xǁFilesǁ_process_directory_info__mutmut_13': xǁFilesǁ_process_directory_info__mutmut_13, 
        'xǁFilesǁ_process_directory_info__mutmut_14': xǁFilesǁ_process_directory_info__mutmut_14, 
        'xǁFilesǁ_process_directory_info__mutmut_15': xǁFilesǁ_process_directory_info__mutmut_15, 
        'xǁFilesǁ_process_directory_info__mutmut_16': xǁFilesǁ_process_directory_info__mutmut_16, 
        'xǁFilesǁ_process_directory_info__mutmut_17': xǁFilesǁ_process_directory_info__mutmut_17, 
        'xǁFilesǁ_process_directory_info__mutmut_18': xǁFilesǁ_process_directory_info__mutmut_18, 
        'xǁFilesǁ_process_directory_info__mutmut_19': xǁFilesǁ_process_directory_info__mutmut_19, 
        'xǁFilesǁ_process_directory_info__mutmut_20': xǁFilesǁ_process_directory_info__mutmut_20, 
        'xǁFilesǁ_process_directory_info__mutmut_21': xǁFilesǁ_process_directory_info__mutmut_21, 
        'xǁFilesǁ_process_directory_info__mutmut_22': xǁFilesǁ_process_directory_info__mutmut_22, 
        'xǁFilesǁ_process_directory_info__mutmut_23': xǁFilesǁ_process_directory_info__mutmut_23, 
        'xǁFilesǁ_process_directory_info__mutmut_24': xǁFilesǁ_process_directory_info__mutmut_24, 
        'xǁFilesǁ_process_directory_info__mutmut_25': xǁFilesǁ_process_directory_info__mutmut_25, 
        'xǁFilesǁ_process_directory_info__mutmut_26': xǁFilesǁ_process_directory_info__mutmut_26, 
        'xǁFilesǁ_process_directory_info__mutmut_27': xǁFilesǁ_process_directory_info__mutmut_27, 
        'xǁFilesǁ_process_directory_info__mutmut_28': xǁFilesǁ_process_directory_info__mutmut_28, 
        'xǁFilesǁ_process_directory_info__mutmut_29': xǁFilesǁ_process_directory_info__mutmut_29, 
        'xǁFilesǁ_process_directory_info__mutmut_30': xǁFilesǁ_process_directory_info__mutmut_30, 
        'xǁFilesǁ_process_directory_info__mutmut_31': xǁFilesǁ_process_directory_info__mutmut_31, 
        'xǁFilesǁ_process_directory_info__mutmut_32': xǁFilesǁ_process_directory_info__mutmut_32, 
        'xǁFilesǁ_process_directory_info__mutmut_33': xǁFilesǁ_process_directory_info__mutmut_33, 
        'xǁFilesǁ_process_directory_info__mutmut_34': xǁFilesǁ_process_directory_info__mutmut_34, 
        'xǁFilesǁ_process_directory_info__mutmut_35': xǁFilesǁ_process_directory_info__mutmut_35, 
        'xǁFilesǁ_process_directory_info__mutmut_36': xǁFilesǁ_process_directory_info__mutmut_36, 
        'xǁFilesǁ_process_directory_info__mutmut_37': xǁFilesǁ_process_directory_info__mutmut_37, 
        'xǁFilesǁ_process_directory_info__mutmut_38': xǁFilesǁ_process_directory_info__mutmut_38, 
        'xǁFilesǁ_process_directory_info__mutmut_39': xǁFilesǁ_process_directory_info__mutmut_39, 
        'xǁFilesǁ_process_directory_info__mutmut_40': xǁFilesǁ_process_directory_info__mutmut_40, 
        'xǁFilesǁ_process_directory_info__mutmut_41': xǁFilesǁ_process_directory_info__mutmut_41, 
        'xǁFilesǁ_process_directory_info__mutmut_42': xǁFilesǁ_process_directory_info__mutmut_42, 
        'xǁFilesǁ_process_directory_info__mutmut_43': xǁFilesǁ_process_directory_info__mutmut_43, 
        'xǁFilesǁ_process_directory_info__mutmut_44': xǁFilesǁ_process_directory_info__mutmut_44, 
        'xǁFilesǁ_process_directory_info__mutmut_45': xǁFilesǁ_process_directory_info__mutmut_45, 
        'xǁFilesǁ_process_directory_info__mutmut_46': xǁFilesǁ_process_directory_info__mutmut_46, 
        'xǁFilesǁ_process_directory_info__mutmut_47': xǁFilesǁ_process_directory_info__mutmut_47, 
        'xǁFilesǁ_process_directory_info__mutmut_48': xǁFilesǁ_process_directory_info__mutmut_48, 
        'xǁFilesǁ_process_directory_info__mutmut_49': xǁFilesǁ_process_directory_info__mutmut_49, 
        'xǁFilesǁ_process_directory_info__mutmut_50': xǁFilesǁ_process_directory_info__mutmut_50, 
        'xǁFilesǁ_process_directory_info__mutmut_51': xǁFilesǁ_process_directory_info__mutmut_51, 
        'xǁFilesǁ_process_directory_info__mutmut_52': xǁFilesǁ_process_directory_info__mutmut_52, 
        'xǁFilesǁ_process_directory_info__mutmut_53': xǁFilesǁ_process_directory_info__mutmut_53, 
        'xǁFilesǁ_process_directory_info__mutmut_54': xǁFilesǁ_process_directory_info__mutmut_54, 
        'xǁFilesǁ_process_directory_info__mutmut_55': xǁFilesǁ_process_directory_info__mutmut_55, 
        'xǁFilesǁ_process_directory_info__mutmut_56': xǁFilesǁ_process_directory_info__mutmut_56, 
        'xǁFilesǁ_process_directory_info__mutmut_57': xǁFilesǁ_process_directory_info__mutmut_57, 
        'xǁFilesǁ_process_directory_info__mutmut_58': xǁFilesǁ_process_directory_info__mutmut_58, 
        'xǁFilesǁ_process_directory_info__mutmut_59': xǁFilesǁ_process_directory_info__mutmut_59, 
        'xǁFilesǁ_process_directory_info__mutmut_60': xǁFilesǁ_process_directory_info__mutmut_60
    }
    xǁFilesǁ_process_directory_info__mutmut_orig.__name__ = 'xǁFilesǁ_process_directory_info'

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
        args = [obj, event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁeventFilter__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁeventFilter__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁeventFilter__mutmut_orig(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Handle application-level events."""
        if event.type() == events.WebSocketOpen.type():
            self.initial_load()
            return False

        if event.type() == events.KlippyDisconnected.type():
            self._clear_all_data()
            return False

        return super().eventFilter(obj, event)

    def xǁFilesǁeventFilter__mutmut_1(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Handle application-level events."""
        if event.type() != events.WebSocketOpen.type():
            self.initial_load()
            return False

        if event.type() == events.KlippyDisconnected.type():
            self._clear_all_data()
            return False

        return super().eventFilter(obj, event)

    def xǁFilesǁeventFilter__mutmut_2(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Handle application-level events."""
        if event.type() == events.WebSocketOpen.type():
            self.initial_load()
            return True

        if event.type() == events.KlippyDisconnected.type():
            self._clear_all_data()
            return False

        return super().eventFilter(obj, event)

    def xǁFilesǁeventFilter__mutmut_3(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Handle application-level events."""
        if event.type() == events.WebSocketOpen.type():
            self.initial_load()
            return False

        if event.type() != events.KlippyDisconnected.type():
            self._clear_all_data()
            return False

        return super().eventFilter(obj, event)

    def xǁFilesǁeventFilter__mutmut_4(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Handle application-level events."""
        if event.type() == events.WebSocketOpen.type():
            self.initial_load()
            return False

        if event.type() == events.KlippyDisconnected.type():
            self._clear_all_data()
            return True

        return super().eventFilter(obj, event)

    def xǁFilesǁeventFilter__mutmut_5(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Handle application-level events."""
        if event.type() == events.WebSocketOpen.type():
            self.initial_load()
            return False

        if event.type() == events.KlippyDisconnected.type():
            self._clear_all_data()
            return False

        return super().eventFilter(None, event)

    def xǁFilesǁeventFilter__mutmut_6(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Handle application-level events."""
        if event.type() == events.WebSocketOpen.type():
            self.initial_load()
            return False

        if event.type() == events.KlippyDisconnected.type():
            self._clear_all_data()
            return False

        return super().eventFilter(obj, None)

    def xǁFilesǁeventFilter__mutmut_7(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Handle application-level events."""
        if event.type() == events.WebSocketOpen.type():
            self.initial_load()
            return False

        if event.type() == events.KlippyDisconnected.type():
            self._clear_all_data()
            return False

        return super().eventFilter(event)

    def xǁFilesǁeventFilter__mutmut_8(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Handle application-level events."""
        if event.type() == events.WebSocketOpen.type():
            self.initial_load()
            return False

        if event.type() == events.KlippyDisconnected.type():
            self._clear_all_data()
            return False

        return super().eventFilter(obj, )
    
    xǁFilesǁeventFilter__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁeventFilter__mutmut_1': xǁFilesǁeventFilter__mutmut_1, 
        'xǁFilesǁeventFilter__mutmut_2': xǁFilesǁeventFilter__mutmut_2, 
        'xǁFilesǁeventFilter__mutmut_3': xǁFilesǁeventFilter__mutmut_3, 
        'xǁFilesǁeventFilter__mutmut_4': xǁFilesǁeventFilter__mutmut_4, 
        'xǁFilesǁeventFilter__mutmut_5': xǁFilesǁeventFilter__mutmut_5, 
        'xǁFilesǁeventFilter__mutmut_6': xǁFilesǁeventFilter__mutmut_6, 
        'xǁFilesǁeventFilter__mutmut_7': xǁFilesǁeventFilter__mutmut_7, 
        'xǁFilesǁeventFilter__mutmut_8': xǁFilesǁeventFilter__mutmut_8
    }
    xǁFilesǁeventFilter__mutmut_orig.__name__ = 'xǁFilesǁeventFilter'

    def event(self, event: QtCore.QEvent) -> bool:
        args = [event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁevent__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁevent__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁevent__mutmut_orig(self, event: QtCore.QEvent) -> bool:
        """Handle object-level events."""
        if event.type() == ReceivedFileData.type():
            if isinstance(event, ReceivedFileData):
                self.handle_message_received(event.method, event.data, event.params)
                return True
        return super().event(event)

    def xǁFilesǁevent__mutmut_1(self, event: QtCore.QEvent) -> bool:
        """Handle object-level events."""
        if event.type() != ReceivedFileData.type():
            if isinstance(event, ReceivedFileData):
                self.handle_message_received(event.method, event.data, event.params)
                return True
        return super().event(event)

    def xǁFilesǁevent__mutmut_2(self, event: QtCore.QEvent) -> bool:
        """Handle object-level events."""
        if event.type() == ReceivedFileData.type():
            if isinstance(event, ReceivedFileData):
                self.handle_message_received(None, event.data, event.params)
                return True
        return super().event(event)

    def xǁFilesǁevent__mutmut_3(self, event: QtCore.QEvent) -> bool:
        """Handle object-level events."""
        if event.type() == ReceivedFileData.type():
            if isinstance(event, ReceivedFileData):
                self.handle_message_received(event.method, None, event.params)
                return True
        return super().event(event)

    def xǁFilesǁevent__mutmut_4(self, event: QtCore.QEvent) -> bool:
        """Handle object-level events."""
        if event.type() == ReceivedFileData.type():
            if isinstance(event, ReceivedFileData):
                self.handle_message_received(event.method, event.data, None)
                return True
        return super().event(event)

    def xǁFilesǁevent__mutmut_5(self, event: QtCore.QEvent) -> bool:
        """Handle object-level events."""
        if event.type() == ReceivedFileData.type():
            if isinstance(event, ReceivedFileData):
                self.handle_message_received(event.data, event.params)
                return True
        return super().event(event)

    def xǁFilesǁevent__mutmut_6(self, event: QtCore.QEvent) -> bool:
        """Handle object-level events."""
        if event.type() == ReceivedFileData.type():
            if isinstance(event, ReceivedFileData):
                self.handle_message_received(event.method, event.params)
                return True
        return super().event(event)

    def xǁFilesǁevent__mutmut_7(self, event: QtCore.QEvent) -> bool:
        """Handle object-level events."""
        if event.type() == ReceivedFileData.type():
            if isinstance(event, ReceivedFileData):
                self.handle_message_received(event.method, event.data, )
                return True
        return super().event(event)

    def xǁFilesǁevent__mutmut_8(self, event: QtCore.QEvent) -> bool:
        """Handle object-level events."""
        if event.type() == ReceivedFileData.type():
            if isinstance(event, ReceivedFileData):
                self.handle_message_received(event.method, event.data, event.params)
                return False
        return super().event(event)

    def xǁFilesǁevent__mutmut_9(self, event: QtCore.QEvent) -> bool:
        """Handle object-level events."""
        if event.type() == ReceivedFileData.type():
            if isinstance(event, ReceivedFileData):
                self.handle_message_received(event.method, event.data, event.params)
                return True
        return super().event(None)
    
    xǁFilesǁevent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁevent__mutmut_1': xǁFilesǁevent__mutmut_1, 
        'xǁFilesǁevent__mutmut_2': xǁFilesǁevent__mutmut_2, 
        'xǁFilesǁevent__mutmut_3': xǁFilesǁevent__mutmut_3, 
        'xǁFilesǁevent__mutmut_4': xǁFilesǁevent__mutmut_4, 
        'xǁFilesǁevent__mutmut_5': xǁFilesǁevent__mutmut_5, 
        'xǁFilesǁevent__mutmut_6': xǁFilesǁevent__mutmut_6, 
        'xǁFilesǁevent__mutmut_7': xǁFilesǁevent__mutmut_7, 
        'xǁFilesǁevent__mutmut_8': xǁFilesǁevent__mutmut_8, 
        'xǁFilesǁevent__mutmut_9': xǁFilesǁevent__mutmut_9
    }
    xǁFilesǁevent__mutmut_orig.__name__ = 'xǁFilesǁevent'

    def _clear_all_data(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilesǁ_clear_all_data__mutmut_orig'), object.__getattribute__(self, 'xǁFilesǁ_clear_all_data__mutmut_mutants'), args, kwargs, self)

    def xǁFilesǁ_clear_all_data__mutmut_orig(self) -> None:
        """Clear all cached data."""
        self._files.clear()
        self._directories.clear()
        self._files_metadata.clear()
        self._usb_files_cache.clear()
        self._pending_usb_preloads.clear()
        self._usb_preload_queue.clear()
        self._initial_load_complete = False
        logger.info("All file data cleared")

    def xǁFilesǁ_clear_all_data__mutmut_1(self) -> None:
        """Clear all cached data."""
        self._files.clear()
        self._directories.clear()
        self._files_metadata.clear()
        self._usb_files_cache.clear()
        self._pending_usb_preloads.clear()
        self._usb_preload_queue.clear()
        self._initial_load_complete = None
        logger.info("All file data cleared")

    def xǁFilesǁ_clear_all_data__mutmut_2(self) -> None:
        """Clear all cached data."""
        self._files.clear()
        self._directories.clear()
        self._files_metadata.clear()
        self._usb_files_cache.clear()
        self._pending_usb_preloads.clear()
        self._usb_preload_queue.clear()
        self._initial_load_complete = True
        logger.info("All file data cleared")

    def xǁFilesǁ_clear_all_data__mutmut_3(self) -> None:
        """Clear all cached data."""
        self._files.clear()
        self._directories.clear()
        self._files_metadata.clear()
        self._usb_files_cache.clear()
        self._pending_usb_preloads.clear()
        self._usb_preload_queue.clear()
        self._initial_load_complete = False
        logger.info(None)

    def xǁFilesǁ_clear_all_data__mutmut_4(self) -> None:
        """Clear all cached data."""
        self._files.clear()
        self._directories.clear()
        self._files_metadata.clear()
        self._usb_files_cache.clear()
        self._pending_usb_preloads.clear()
        self._usb_preload_queue.clear()
        self._initial_load_complete = False
        logger.info("XXAll file data clearedXX")

    def xǁFilesǁ_clear_all_data__mutmut_5(self) -> None:
        """Clear all cached data."""
        self._files.clear()
        self._directories.clear()
        self._files_metadata.clear()
        self._usb_files_cache.clear()
        self._pending_usb_preloads.clear()
        self._usb_preload_queue.clear()
        self._initial_load_complete = False
        logger.info("all file data cleared")

    def xǁFilesǁ_clear_all_data__mutmut_6(self) -> None:
        """Clear all cached data."""
        self._files.clear()
        self._directories.clear()
        self._files_metadata.clear()
        self._usb_files_cache.clear()
        self._pending_usb_preloads.clear()
        self._usb_preload_queue.clear()
        self._initial_load_complete = False
        logger.info("ALL FILE DATA CLEARED")
    
    xǁFilesǁ_clear_all_data__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilesǁ_clear_all_data__mutmut_1': xǁFilesǁ_clear_all_data__mutmut_1, 
        'xǁFilesǁ_clear_all_data__mutmut_2': xǁFilesǁ_clear_all_data__mutmut_2, 
        'xǁFilesǁ_clear_all_data__mutmut_3': xǁFilesǁ_clear_all_data__mutmut_3, 
        'xǁFilesǁ_clear_all_data__mutmut_4': xǁFilesǁ_clear_all_data__mutmut_4, 
        'xǁFilesǁ_clear_all_data__mutmut_5': xǁFilesǁ_clear_all_data__mutmut_5, 
        'xǁFilesǁ_clear_all_data__mutmut_6': xǁFilesǁ_clear_all_data__mutmut_6
    }
    xǁFilesǁ_clear_all_data__mutmut_orig.__name__ = 'xǁFilesǁ_clear_all_data'
