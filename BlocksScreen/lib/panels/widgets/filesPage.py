import json
import logging
import typing

import helper_methods
from lib.utils.blocks_combobox import BlocksComboBox
from lib.utils.blocks_Scrollbar import CustomScrollBar
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(__name__)


class FilesPage(QtWidgets.QWidget):
    # Signals
    request_back = QtCore.pyqtSignal(name="request_back")
    file_selected = QtCore.pyqtSignal(str, dict, name="file_selected")
    request_dir_info = QtCore.pyqtSignal(
        [], [str], [str, bool], name="api_get_dir_info"
    )

    # Constants
    GCODE_EXTENSION = ".gcode"
    USB_PREFIX = "USB-"
    ITEM_HEIGHT = 80
    LEFT_FONT_SIZE = 17
    RIGHT_FONT_SIZE = 12

    SORTING_TYPES: tuple[str, ...] = (
        "Last Print",
        "Name",
        "Filament",
        "Nozzle Size",
        "Import Order",
    )

    # Icon paths
    ICON_PATHS = {
        "back_folder": ":/ui/media/btn_icons/back_folder.svg",
        "folder": ":/ui/media/btn_icons/folderIcon.svg",
        "right_arrow": ":/arrow_icons/media/btn_icons/right_arrow.svg",
        "usb": ":/ui/media/btn_icons/usb_icon.svg",
        "back": ":/ui/media/btn_icons/back.svg",
        "refresh": ":/ui/media/btn_icons/refresh.svg",
        "sort_desc": ":/arrow_icons/media/btn_icons/down_arrow.svg",
        "sort_asc": ":/arrow_icons/media/btn_icons/up_arrow.svg",
    }

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        self._file_list: list[dict] = []
        self._files_data: dict[str, dict] = {}  # filename -> metadata dict
        self._directories: list[dict] = []
        self._curr_dir: str = ""
        self._pending_action: bool = False
        self._sort_key: str = self.SORTING_TYPES[0]
        self._sort_descending: bool = True
        self._icons: dict[str, QtGui.QPixmap] = {}

        self._model = EntryListModel()
        self._entry_delegate = EntryDelegate()

        self._model.rowsInserted.connect(self._delayed_scrollbar_update)
        self._model.rowsRemoved.connect(self._delayed_scrollbar_update)
        self._model.modelReset.connect(self._delayed_scrollbar_update)

        self._setup_ui()
        self._load_icons()
        self._connect_signals()

        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    @property
    def current_directory(self) -> str:
        """Get current directory path."""
        return self._curr_dir

    @current_directory.setter
    def current_directory(self, value: str) -> None:
        """Set current directory path."""
        self._curr_dir = value

    @QtCore.pyqtSlot(list, name="on_file_list")
    def on_file_list(self, file_list: list) -> None:
        """Handle receiving full files list."""
        self._file_list = file_list.copy() if file_list else []
        logger.debug(f"Received file list with {len(self._file_list)} files")

    @QtCore.pyqtSlot(list, name="on_dirs")
    def on_directories(self, directories_data: list) -> None:
        """Handle receiving full directories list."""
        self._directories = directories_data.copy() if directories_data else []
        # New directory: drop the previous dir's cached metadata (bounds memory).
        self._files_data.clear()
        logger.debug(f"Received {len(self._directories)} directories")

        if self.isVisible():
            self._build_file_list()

    @QtCore.pyqtSlot(dict, name="on_fileinfo")
    def on_fileinfo(self, filedata: dict) -> None:
        """Cache file metadata and refresh the affected row in place."""
        if not filedata:
            return
        filename = filedata.get("filename", "")
        if not filename.lower().endswith(self.GCODE_EXTENSION):
            return
        self._files_data[filename] = filedata
        if self.isVisible():
            self._build_file_list()

    @QtCore.pyqtSlot(str, list, name="on_usb_files_loaded")
    def on_usb_files_loaded(self, usb_path: str, files: list) -> None:
        """Update display when USB files are preloaded."""
        current = self._curr_dir.removeprefix("/")

        # If we're currently in this USB folder, update the file list
        if current == usb_path:
            self._file_list = files.copy()
            if self.isVisible():
                self._build_file_list()
            logger.debug(f"Updated view with preloaded USB files: {usb_path}")

    @QtCore.pyqtSlot(dict, name="on_file_added")
    def on_file_added(self, file_data: dict) -> None:
        """Add a created file to backing data and refresh the current view."""
        path = file_data.get("path", file_data.get("filename", "")).removeprefix("/")
        current = self._curr_dir.removeprefix("/")
        if not path or helper_methods.get_parent_dir(path) != current:
            return
        # Store the bare basename to match the get_directory listing convention.
        name = helper_methods.get_file_name(path)
        if not any(
            helper_methods.get_file_name(f.get("filename", f.get("path", ""))) == name
            for f in self._file_list
        ):
            self._file_list.append(file_data | {"filename": name})
        # Metadata is owned + requested by Files (_handle_file_created); no re-request.
        if self.isVisible():
            self._build_file_list()

    @QtCore.pyqtSlot(str, name="on_file_removed")
    def on_file_removed(self, filepath: str) -> None:
        """Drop a deleted file from backing data/cache and refresh."""
        filepath = filepath.removeprefix("/")
        self._files_data.pop(filepath, None)
        # _file_list holds bare basenames; match on basename to drop the row.
        name = helper_methods.get_file_name(filepath)
        self._file_list = [
            f
            for f in self._file_list
            if helper_methods.get_file_name(f.get("filename", f.get("path", "")))
            != name
        ]
        current = self._curr_dir.removeprefix("/")
        if self.isVisible() and helper_methods.get_parent_dir(filepath) == current:
            self._build_file_list()

    @QtCore.pyqtSlot(dict, name="on_file_modified")
    def on_file_modified(self, file_data: dict) -> None:
        """Handle file modification from Moonraker."""
        path = file_data.get("path", file_data.get("filename", ""))
        if path:
            # Remove old entry and request fresh metadata
            self.on_file_removed(path)
            self.on_file_added(file_data)

    @QtCore.pyqtSlot(dict, name="on_dir_added")
    def on_dir_added(self, dir_data: dict) -> None:
        """Add a created directory to backing data and refresh."""
        path = dir_data.get("path", "").removeprefix("/")
        dirname = dir_data.get("dirname", "") or helper_methods.get_parent_dir(path)
        if not dirname or dirname.startswith("."):
            return
        parent_dir = helper_methods.get_parent_dir(path) if path else ""
        if parent_dir != self._curr_dir.removeprefix("/"):
            return
        if not any(d.get("dirname", "") == dirname for d in self._directories):
            self._directories.append(dir_data | {"dirname": dirname})
        if self.isVisible():
            self._build_file_list()

    @QtCore.pyqtSlot(str, name="on_dir_removed")
    def on_dir_removed(self, dirname_or_path: str) -> None:
        """Remove a directory from backing data, or bail to root if it is current."""
        dirname_or_path = dirname_or_path.removeprefix("/")
        dirname = (
            helper_methods.get_parent_dir(dirname_or_path)
            if "/" in dirname_or_path
            else dirname_or_path
        )
        if not dirname:
            return
        current = self._curr_dir.removeprefix("/")
        if current == dirname or current.startswith(dirname + "/"):
            logger.warning(
                "Current directory '%s' was removed, returning to root", current
            )
            self.on_directory_error()
            return
        self._directories = [
            d for d in self._directories if d.get("dirname", "") != dirname
        ]
        if self.isVisible():
            self._build_file_list()

    @QtCore.pyqtSlot(name="on_full_refresh_needed")
    def on_full_refresh_needed(self) -> None:
        """Refresh display on root update or major changes."""
        logger.info("Full refresh requested")
        self._curr_dir = ""
        self.request_dir_info[str].emit(self._curr_dir)

    @QtCore.pyqtSlot(name="on_directory_error")
    def on_directory_error(self) -> None:
        """Navigate back to the root gcodes folder after a directory error."""
        logger.info("Directory Error - returning to root directory")
        self._curr_dir = ""
        self._pending_action = False

        # Request fresh data for root directory
        self.request_dir_info[str].emit("")

    @QtCore.pyqtSlot(str, name="on_usb_removed")
    def on_usb_removed(self, _device_path: str = "") -> None:
        """Return to the gcodes root when a USB drive is removed while inside its folder."""
        if self._curr_dir.removeprefix("/").startswith(self.USB_PREFIX):
            logger.info("USB removed while inside its folder, returning to root")
            self.on_directory_error()

    @QtCore.pyqtSlot(ListItem, name="on_item_selected")
    def _on_item_selected(self, item: ListItem) -> None:
        """Handle list item selection."""
        if not item.left_icon:
            # File selected (files don't have left icon).
            filename = self._selected_file_path(item.text)
            if filename:
                self._on_file_item_clicked(filename)
        elif item.text == "Go Back":
            # Go back selected
            go_back_path = helper_methods.get_parent_dir(self._curr_dir)
            if go_back_path == "/":
                go_back_path = ""
            self._on_go_back_dir(go_back_path)
        else:
            # Directory selected
            self._on_dir_item_clicked("/" + item.text)

    @QtCore.pyqtSlot(name="reset_dir")
    def reset_dir(self) -> None:
        """Reset to root directory."""
        self._curr_dir = ""
        self.request_dir_info[str].emit(self._curr_dir)

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        """Handle widget becoming visible."""
        # Request fresh data when becoming visible
        self.request_dir_info[str].emit(self._curr_dir)
        super().showEvent(event)

    @staticmethod
    def _item_key(item: ListItem) -> str:
        """Stable identity for reconcile: dirs/back vs files, namespaced by text."""
        return f"{'d' if item.left_icon else 'f'}:{item.text}"

    def _build_file_list(self) -> None:
        """Rebuild the model from backing data via keyed reconcile."""
        self._pending_action = False
        meta = self._metadata_map()
        is_root = not self._curr_dir or self._curr_dir == "/"
        if is_root and not self._file_list and not self._directories:
            self._model.clear()
            self._entry_delegate.clear()
            self._show_placeholder()
            return
        self._hide_placeholder()
        self._model.reconcile(self._desired_items(is_root, meta), self._item_key)

    def _metadata_map(self) -> dict[str, dict | None]:
        """Each file's bare name to its cached metadata, one lookup pass per rebuild."""
        meta: dict[str, dict | None] = {}
        for f in self._file_list:
            name = f.get("filename", f.get("path", ""))
            meta[name] = self._files_data.get(self._build_filepath(name))
        return meta

    def _lookup_meta(self, filename: str, meta: dict | None) -> dict | None:
        """Cached metadata from the prebuilt map, else a direct lookup."""
        if meta is not None and filename in meta:
            return meta[filename]
        return self._files_data.get(self._build_filepath(filename))

    def _desired_items(self, is_root: bool, meta: dict) -> list[ListItem]:
        """Ordered rows: Go Back (subdir), dirs A-Z, then files newest-first."""
        items: list[ListItem] = []
        if not is_root:
            items.append(self._make_back_folder_item())
        items.extend(self._desired_directory_items())
        items.extend(self._desired_file_items(meta))
        return items

    def _desired_directory_items(self) -> list[ListItem]:
        """Directory rows sorted alphabetically, excluding dot-dirs."""
        rows = sorted(self._directories, key=lambda d: d.get("dirname", "").lower())
        return [
            self._make_directory_item(d)
            for d in rows
            if d.get("dirname", "") and not d["dirname"].startswith(".")
        ]

    def _desired_file_items(self, meta: dict) -> list[ListItem]:
        """Gcode file rows ordered by the active sort key and direction."""
        files = [
            f
            for f in self._file_list
            if f.get("filename", f.get("path", ""))
            .lower()
            .endswith(self.GCODE_EXTENSION)
        ]
        if self._sort_key != "Import Order":
            files.sort(
                key=lambda f: self._sort_value(f, meta),
                reverse=self._sort_descending,
            )
        return [
            self._make_file_item(f.get("filename", f.get("path", "")), meta)
            for f in files
        ]

    def _sort_value(self, filedata: dict, meta: dict) -> object:
        """Comparable key for the active sort column (uniform type per column)."""
        name = filedata.get("filename", filedata.get("path", ""))
        if self._sort_key == "Last Print":
            cached = self._lookup_meta(name, meta) or {}
            return cached.get("print_start_time") or 0
        if self._sort_key == "Nozzle Size":
            cached = self._lookup_meta(name, meta) or {}
            nozzle = cached.get("nozzle_diameter", -1.0)
            return nozzle if isinstance(nozzle, (int, float)) else -1.0
        if self._sort_key == "Filament":
            cached = self._lookup_meta(name, meta) or {}
            return self._filament_label(cached.get("filament_type")).lower()
        return name.lower()

    def _on_sort_key_changed(self, sort_key: str) -> None:
        """Apply the selected sort column and rebuild the list."""
        self._sort_key = sort_key or self.SORTING_TYPES[0]
        self._build_file_list()

    def _on_sort_order_toggled(self) -> None:
        """Flip the sort direction, refresh the toggle icon, and rebuild."""
        self._sort_descending = not self._sort_descending
        self._update_sort_order_icon()
        self._build_file_list()

    def _update_sort_order_icon(self) -> None:
        """Point the order-toggle button at the icon for the current direction."""
        key = "sort_desc" if self._sort_descending else "sort_asc"
        self._sort_order_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(self.ICON_PATHS[key])
        )
        self._sort_order_btn.update()

    def _make_back_folder_item(self) -> ListItem:
        """The leading Go Back navigation row."""
        return self._row("Go Back", "", self._icons.get("back_folder"), None)

    def _make_directory_item(self, dir_data: dict) -> ListItem:
        """A directory row; USB mounts at root get the USB icon."""
        name = str(dir_data.get("dirname", ""))
        icon = self._icons.get("folder")
        if not self._curr_dir and helper_methods.is_usb_mount(name):
            icon = self._icons.get("usb")
        return self._row(name, "", icon, None)

    def _make_file_item(self, filename: str, meta: dict | None = None) -> ListItem:
        """A file row from cached metadata, or an Unknown placeholder."""
        cached = self._lookup_meta(filename, meta)
        right = (
            self._format_file_meta(cached)
            if cached
            else "Unknown Filament - Unknown time"
        )
        return self._row(
            self._get_display_name(filename),
            right,
            None,
            self._icons.get("right_arrow"),
        )

    def _row(
        self,
        text: str,
        right_text: str,
        left_icon: typing.Optional[QtGui.QPixmap],
        right_icon: typing.Optional[QtGui.QPixmap],
    ) -> ListItem:
        """ListItem with this page's standard sizing/flags."""
        return ListItem(
            text=text,
            right_text=right_text,
            left_icon=left_icon,
            right_icon=right_icon,
            callback=None,
            selected=False,
            allow_check=False,
            _lfontsize=self.LEFT_FONT_SIZE,
            _rfontsize=self.RIGHT_FONT_SIZE,
            height=self.ITEM_HEIGHT,
            notificate=False,
        )

    def _format_file_meta(self, filedata: dict) -> str:
        """'<filament> - <time>' summary from a metadata dict."""
        est = filedata.get("estimated_time", 0)
        seconds = int(est) if isinstance(est, (int, float)) else 0
        filament = self._filament_label(filedata.get("filament_type"))
        return f"{filament} - {self._format_print_time(seconds)}"

    @staticmethod
    def _parse_materials(filament_type) -> list[str]:
        """filament_type (str/list/JSON/comma) -> ordered list of material names."""
        if isinstance(filament_type, str):
            text = filament_type.strip()
            if text.startswith("[") and text.endswith("]"):
                try:
                    types = json.loads(text)
                except json.JSONDecodeError:
                    types = [text]
            else:
                types = text.split(",")
        elif isinstance(filament_type, list):
            types = filament_type
        else:
            types = [filament_type] if filament_type else []
        return [name for t in types if (name := str(t).strip())]

    @classmethod
    def _filament_label(cls, filament_type) -> str:
        """Normalize filament_type to a comma-joined display label."""
        label = ",".join(dict.fromkeys(cls._parse_materials(filament_type)))
        if not label or label == "Unknown":
            return "Unknown Filament"
        return label

    @classmethod
    def _material_set(cls, filedata: dict) -> set[str]:
        """Distinct printable materials declared in a file's metadata."""
        return {
            m
            for m in cls._parse_materials(filedata.get("filament_type"))
            if m != "Unknown"
        }

    def _delayed_scrollbar_update(self) -> None:
        """Update scrollbar after model changes."""
        QtCore.QTimer.singleShot(10, self._setup_scrollbar)

    def _on_file_item_clicked(self, filename: str) -> None:
        """Handle file item click."""
        clean_filename = filename.removeprefix("/")
        file_data = self._files_data.get(clean_filename, {})
        self.file_selected.emit(clean_filename, file_data)

    def _selected_file_path(self, display_name: str) -> str:
        """Full path of the gcode row whose display name matches (extension-agnostic)."""
        for f in self._file_list:
            name = f.get("filename", f.get("path", ""))
            if name.lower().endswith(self.GCODE_EXTENSION) and (
                self._get_display_name(name) == display_name
            ):
                return self._build_filepath(name)
        return ""

    def _on_dir_item_clicked(self, directory: str) -> None:
        """Handle directory item click."""
        if self._pending_action:
            return

        self._curr_dir = self._curr_dir + directory
        self.request_dir_info[str].emit(self._curr_dir)
        self._pending_action = True

    def _on_go_back_dir(self, directory: str) -> None:
        """Handle go back navigation."""
        self.request_dir_info[str].emit(directory)
        self._curr_dir = directory

    def _show_placeholder(self) -> None:
        """Show the 'No Files found' placeholder."""
        self._scrollbar.hide()
        self._list_widget.hide()
        self._label.show()

    def _hide_placeholder(self) -> None:
        """Hide the placeholder and show the list."""
        self._label.hide()
        self._list_widget.show()

    def _handle_scrollbar_value_changed(self, value: int) -> None:
        """Sync scrollbar with list widget."""
        self._scrollbar.blockSignals(True)
        self._scrollbar.setValue(value)
        self._scrollbar.blockSignals(False)

    def _setup_scrollbar(self) -> None:
        """Configure scrollbar to match list size."""
        list_scrollbar = self._list_widget.verticalScrollBar()
        self._scrollbar.setMinimum(list_scrollbar.minimum())
        self._scrollbar.setMaximum(list_scrollbar.maximum())
        self._scrollbar.setPageStep(list_scrollbar.pageStep())

        if list_scrollbar.maximum() > 0:
            self._scrollbar.show()
        else:
            self._scrollbar.hide()

    def _build_filepath(self, filename: str) -> str:
        """Build full file path from current directory and filename."""
        filename = filename.removeprefix("/")
        if self._curr_dir:
            curr = self._curr_dir.removeprefix("/")
            return f"{curr}/{filename}"
        return filename

    @staticmethod
    def _format_print_time(seconds: int) -> str:
        """Format print time in human-readable form."""
        if seconds <= 0:
            return "Unknown time"
        if seconds < 60:
            return f"{seconds}s"

        days, hours, minutes, _ = helper_methods.estimate_print_time(seconds)

        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    def _get_display_name(self, filename: str) -> str:
        """Get display name from filename (without path and extension)."""
        name = helper_methods.get_file_name(filename)

        # Remove .gcode extension
        if name.lower().endswith(self.GCODE_EXTENSION):
            name = name[:-6]

        return name

    def _load_icons(self) -> None:
        """Load all icons into cache."""
        self._icons = {
            "back_folder": QtGui.QPixmap(self.ICON_PATHS["back_folder"]),
            "folder": QtGui.QPixmap(self.ICON_PATHS["folder"]),
            "right_arrow": QtGui.QPixmap(self.ICON_PATHS["right_arrow"]),
            "usb": QtGui.QPixmap(self.ICON_PATHS["usb"]),
        }

    def _connect_signals(self) -> None:
        """Connect internal signals."""
        # Button connections
        self._reload_button.clicked.connect(
            lambda: self.request_dir_info[str].emit(self._curr_dir)
        )
        self.back_btn.clicked.connect(self.reset_dir)

        # List widget connections
        self._list_widget.verticalScrollBar().valueChanged.connect(
            self._handle_scrollbar_value_changed
        )
        self._scrollbar.valueChanged.connect(self._handle_scrollbar_value_changed)
        self._scrollbar.valueChanged.connect(
            lambda value: self._list_widget.verticalScrollBar().setValue(value)
        )

        # Delegate connections
        self._entry_delegate.item_selected.connect(self._on_item_selected)

    def _setup_ui(self) -> None:
        """Set up the widget UI."""
        # Size policy
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(710, 400))

        # Font
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.setFont(font)

        # Layout direction and style
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.setAutoFillBackground(False)
        self.setStyleSheet("#file_page { background-color: transparent; }")

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setObjectName("main_layout")

        # Header layout
        header_layout = self._create_header_layout()
        main_layout.addLayout(header_layout)

        # Separator line
        line = QtWidgets.QFrame(parent=self)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        # Content layout
        content_layout = self._create_content_layout()
        main_layout.addLayout(content_layout)

    def _create_header_layout(self) -> QtWidgets.QHBoxLayout:
        """Create the header with back and reload buttons."""
        layout = QtWidgets.QHBoxLayout()
        layout.setObjectName("header_layout")

        # Back button
        self.back_btn = IconButton(parent=self)
        self.back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.back_btn.setFlat(True)
        self.back_btn.setProperty("icon_pixmap", QtGui.QPixmap(self.ICON_PATHS["back"]))
        self.back_btn.setObjectName("back_btn")
        layout.addWidget(self.back_btn, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        layout.addStretch(1)

        # Sort order toggle (ascending/descending)
        self._sort_order_btn = IconButton(parent=self)
        self._sort_order_btn.setMinimumSize(QtCore.QSize(60, 60))
        self._sort_order_btn.setMaximumSize(QtCore.QSize(60, 60))
        self._sort_order_btn.setFlat(True)
        self._sort_order_btn.setObjectName("sort_order_btn")
        self._sort_order_btn.clicked.connect(self._on_sort_order_toggled)
        self._update_sort_order_icon()
        layout.addWidget(self._sort_order_btn, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)

        # Sort key selector
        self._sort_combo = BlocksComboBox(parent=self)
        for name in self.SORTING_TYPES:
            self._sort_combo.addItem(name)
        self._sort_combo.currentTextChanged.connect(self._on_sort_key_changed)
        layout.addWidget(self._sort_combo, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)

        layout.addStretch(1)

        # Reload button
        self._reload_button = IconButton(parent=self)
        self._reload_button.setMinimumSize(QtCore.QSize(60, 60))
        self._reload_button.setMaximumSize(QtCore.QSize(60, 60))
        self._reload_button.setFlat(True)
        self._reload_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(self.ICON_PATHS["refresh"])
        )
        self._reload_button.setObjectName("reload_button")
        layout.addWidget(self._reload_button, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        return layout

    def _create_content_layout(self) -> QtWidgets.QHBoxLayout:
        """Create the content area with list and scrollbar."""
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setObjectName("content_layout")

        # Placeholder label
        font = QtGui.QFont()
        font.setPointSize(25)
        self._label = QtWidgets.QLabel("No Files found")
        self._label.setFont(font)
        self._label.setStyleSheet("color: gray;")
        self._label.hide()

        # List widget
        self._list_widget = self._create_list_widget()

        # Scrollbar
        self._scrollbar = CustomScrollBar()
        self._scrollbar.show()

        # Add widgets to layout
        layout.addWidget(
            self._label,
            alignment=(
                QtCore.Qt.AlignmentFlag.AlignHCenter
                | QtCore.Qt.AlignmentFlag.AlignVCenter
            ),
        )
        layout.addWidget(self._list_widget)
        layout.addWidget(self._scrollbar)

        return layout

    def _create_list_widget(self) -> QtWidgets.QListView:
        """Create and configure the list view widget."""
        list_widget = QtWidgets.QListView(parent=self)
        list_widget.setModel(self._model)
        list_widget.setItemDelegate(self._entry_delegate)
        list_widget.setSpacing(5)
        list_widget.setProperty("showDropIndicator", False)
        list_widget.setProperty("selectionMode", "NoSelection")
        list_widget.setStyleSheet("background: transparent;")
        list_widget.setDefaultDropAction(QtCore.Qt.DropAction.IgnoreAction)
        list_widget.setUniformItemSizes(True)
        list_widget.setObjectName("list_widget")
        list_widget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        list_widget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        list_widget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        list_widget.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        list_widget.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        list_widget.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # Enable touch gestures
        QtWidgets.QScroller.grabGesture(
            list_widget,
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )
        QtWidgets.QScroller.grabGesture(
            list_widget,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )

        # Configure scroller properties
        scroller = QtWidgets.QScroller.scroller(list_widget)
        props = scroller.scrollerProperties()
        props.setScrollMetric(
            QtWidgets.QScrollerProperties.ScrollMetric.DragVelocitySmoothingFactor,
            0.05,
        )
        props.setScrollMetric(
            QtWidgets.QScrollerProperties.ScrollMetric.DecelerationFactor,
            0.4,
        )
        scroller.setScrollerProperties(props)

        return list_widget
