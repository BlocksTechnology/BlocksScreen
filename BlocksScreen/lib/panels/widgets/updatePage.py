import copy
import typing

from lib.panels.widgets.loadPage import LoadScreen
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets


class UpdatePage(QtWidgets.QWidget):
    """Update GUI Page,
    retrieves from moonraker available clients and adds functionality
    for updating or recovering them
    """

    request_update_klipper: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="update-klipper"
    )
    request_update_moonraker: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="update-moonraker"
    )
    request_update_client: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="update-client"
    )
    request_update_system: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="update-system"
    )
    request_full_update: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="update-full"
    )
    request_update_status: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="update-status"
    )
    request_refresh_update: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [], [str], name="update-refresh"
    )
    request_recover_repo: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [str], [str, bool], name="recover-repo"
    )
    request_rollback_update: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="rollback-update"
    )
    update_in_progress: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="update-in-progress"
    )
    update_end: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="update-end"
    )
    update_available: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="update-available"
    )

    def __init__(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self._setupUI()
        self.cli_tracking = {}
        self.selected_item: ListItem | None = None
        self.ongoing_update: bool = False

        self.load_popup: LoadScreen = LoadScreen(self)
        self.repeated_request_status = QtCore.QTimer()
        self.repeated_request_status.setInterval(2000)  # every 2 seconds
        self.model = EntryListModel()
        self.model.setParent(self.update_buttons_list_widget)
        self.entry_delegate = EntryDelegate()
        self.update_buttons_list_widget.setModel(self.model)
        self.update_buttons_list_widget.setItemDelegate(self.entry_delegate)
        self.entry_delegate.item_selected.connect(self.on_item_clicked)
        self.action_btn.clicked.connect(self.on_update_clicked)
        self.update_back_btn.clicked.connect(self.reset_view_model)
        self.update_in_progress.connect(self.handle_ongoing_update)
        self.update_end.connect(self.handle_update_end)
        self.repeated_request_status.timeout.connect(
            lambda: self.request_update_status.emit(False)
        )

    def handle_update_end(self) -> None:
        """Handles update end signal
        (closes loading page, returns to normal operation)
        """
        if self.load_popup.isVisible():
            self.load_popup.close()
        self.repeated_request_status.stop()
        self.request_refresh_update.emit()
        self.build_model_list()

    def handle_ongoing_update(self) -> None:
        """Handled ongoing update signal,
        calls loading page (blocks user interaction)
        """
        self.load_popup.set_status_message("Updating...")
        self.load_popup.show()
        self.repeated_request_status.start(2000)

    def reset_view_model(self) -> None:
        """Clears items from ListView
        (Resets `QAbstractListModel` by clearing entries)
        """
        self.model.clear()
        self.entry_delegate.clear()

    def deleteLater(self) -> None:
        """Schedule the object for deletion, resets the list model first"""
        self.reset_view_model()
        return super().deleteLater()

    def showEvent(self, event: QtGui.QShowEvent | None) -> None:
        """Re-add clients to update list"""
        self.build_model_list()
        return super().showEvent(event)

    def build_model_list(self) -> None:
        """Builds the model list (`self.model`) containing updatable clients"""
        self.update_buttons_list_widget.blockSignals(True)
        self.reset_view_model()
        for cli_name, _cli_info in self.cli_tracking.items():
            if not _cli_info:
                continue
            if "system" in cli_name.lower():
                _updatable = bool(_cli_info.get("package_count", 0))
            else:
                _updatable = bool(_cli_info.get("commits_behind", []))
            self.add_update_entry(cli_name, _updatable)
        self.model.setData(
            self.model.index(0), True, EntryListModel.EnableRole
        )  # Set the first item checked on startup
        self.on_item_clicked(
            self.model.data(self.model.index(0), QtCore.Qt.ItemDataRole.UserRole)
        )  # Bandage solution: simulate click for setting information on infobox
        self.update_buttons_list_widget.blockSignals(False)

    @QtCore.pyqtSlot(name="on-update-clicked")
    def on_update_clicked(self) -> None:
        """Handle `update_btn` clicked event"""
        mode = self.action_btn.text()
        if not self.selected_item:
            return
        cli_name = self.selected_item.text
        if mode == "Update":
            if "system" in cli_name:
                self.request_update_system.emit()
            elif "klipper" in cli_name:
                self.request_update_klipper.emit()
            elif "moonraker" in cli_name:
                self.request_update_moonraker.emit()
            self.request_update_client.emit(cli_name)
            self.load_popup.set_status_message(f"Updating {cli_name}")
        else:
            self.request_recover_repo[str, bool].emit(cli_name, True)
            self.load_popup.set_status_message(f"Recovering {cli_name}")
        self.load_popup.show()
        self.request_update_status.emit(False)

    @QtCore.pyqtSlot(ListItem, name="on-item-clicked")
    def on_item_clicked(self, item: ListItem) -> None:
        """Setup information for the currently clicked list item on the info box.
        Keeps track of the list item
        """
        if not item:
            return
        cli_data = self.cli_tracking.get(item.text, {})
        if not cli_data:
            self.version_tracking_info.setText("Missing, Cannot Update")
        self.selected_item = copy.copy(item)
        if item.text == "system":
            self.remote_version_title.hide()
            self.remote_version_tracking.hide()
            updatable_packages = cli_data.get("package_count", 0)
            if updatable_packages == 0:
                self.version_title.hide()
                self.version_tracking_info.hide()
                self.action_btn.hide()
                self.no_update_placeholder.show()
                return
            self.version_tracking_info.setText(
                f"{updatable_packages} upgradable \n packages"
            )
            self.action_btn.show()
            return
        _remote_version = cli_data.get("remote_version", None)
        if not _remote_version:
            self.remote_version_title.hide()
            self.remote_version_tracking.hide()
        self.remote_version_title.show()
        self.remote_version_tracking.show()
        self.remote_version_tracking.setText(_remote_version)
        _curr_version = cli_data.get("version", None)
        if not _curr_version:
            # There is no version information something is seriously wrong here
            self.action_btn.setText("Recover")
        self.version_title.show()
        self.version_tracking_info.show()
        self.version_tracking_info.setText(_curr_version)
        _updatable = bool(
            not (
                cli_data.get("corrupt", False)
                or cli_data.get("is_dirty", False)
                or cli_data.get("detached", False)
            )
            and (cli_data.get("is_valid", False) and cli_data.get("commits_behind", []))
        )
        _recover = bool(
            cli_data.get("corrupt", False)
            or cli_data.get("is_dirty", False)
            or cli_data.get("detached", False)
        )
        if _updatable and not _recover:
            self.no_update_placeholder.hide()
            self.action_btn.setText("Update")
        elif _recover:
            self.action_btn.setText("Recover")
        else:
            self.no_update_placeholder.show()
            self.action_btn.hide()
            return

        self.no_update_placeholder.hide()
        self.action_btn.show()

    @QtCore.pyqtSlot(dict, name="handle-update-message")
    def handle_update_message(self, message: dict) -> None:
        """Handle receiving current state of each item update.

        Receives updates from moonraker `machine.update.status` request.
        """
        busy = message.get("busy", False)
        if busy:
            self.update_in_progress.emit()
            return
        else:  # todo: this will always fire, and it shouldn't so i need to only send this signal if we were updating before
            self.update_end.emit()
        cli_version_info = message.get("version_info", None)
        if not cli_version_info:
            return
        self.cli_tracking = cli_version_info
        # Signal that updates exist (Used to render red dots)
        _update_avail = any(
            value
            and (
                ("system" in key.lower() and value.get("package_count", 0))
                or (value.get("commits_behind"))
            )
            for key, value in cli_version_info.items()
        )
        self.update_available.emit(_update_avail)

    def add_update_entry(self, cli_name: str, updatable: bool = False) -> None:
        """Adds a new item to the list model"""
        item = ListItem(
            text=cli_name,
            right_icon=QtGui.QPixmap(":/ui/media/btn_icons/info.svg"),
            selected=False,
            _lfontsize=17,
            _rfontsize=12,
            height=60,
            notificate=updatable,
        )
        self.model.add_item(item)

    def _setupUI(self) -> None:
        """Setup UI for updatePage"""
        font_id = QtGui.QFontDatabase.addApplicationFont(
            ":/font/media/fonts for text/Momcake-Bold.ttf"
        )
        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.update_page_content_layout = QtWidgets.QVBoxLayout()
        self.update_page_content_layout.setContentsMargins(15, 15, 2, 2)

        self.header_content_layout = QtWidgets.QHBoxLayout()
        self.header_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.header_title = QtWidgets.QLabel(self)
        self.header_title.setMinimumSize(QtCore.QSize(100, 60))
        self.header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily(font_family)
        font.setPointSize(24)
        palette = self.header_title.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.header_title.setFont(font)
        self.header_title.setPalette(palette)
        self.header_title.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header_title.setObjectName("header-title")
        self.header_title.setText("Update Manager")
        self.header_content_layout.addWidget(self.header_title, 0)
        self.update_back_btn = IconButton(self)
        self.update_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.update_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.update_back_btn.setFlat(True)
        self.update_back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.header_content_layout.addWidget(self.update_back_btn, 0)
        self.update_page_content_layout.addLayout(self.header_content_layout, 0)

        self.main_content_layout = QtWidgets.QHBoxLayout()
        self.main_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.update_buttons_frame = BlocksCustomFrame(self)

        self.update_buttons_frame.setMinimumSize(QtCore.QSize(320, 300))
        self.update_buttons_frame.setMaximumSize(QtCore.QSize(450, 500))

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Button,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Base,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Window,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Highlight,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Link,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Button,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Base,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Window,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Highlight,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Link,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Button,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Base,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Window,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Highlight,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Link,
            brush,
        )
        self.update_buttons_list_widget = QtWidgets.QListView(self.update_buttons_frame)
        self.update_buttons_list_widget.setMouseTracking(True)
        self.update_buttons_list_widget.setTabletTracking(True)

        self.update_buttons_list_widget.setPalette(palette)
        self.update_buttons_list_widget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.update_buttons_list_widget.setStyleSheet("background-color:transparent")
        self.update_buttons_list_widget.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.update_buttons_list_widget.setMinimumSize(self.update_buttons_frame.size())
        self.update_buttons_list_widget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.update_buttons_list_widget.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.update_buttons_list_widget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.update_buttons_list_widget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.update_buttons_list_widget.setAutoScroll(False)
        self.update_buttons_list_widget.setProperty("showDropIndicator", False)
        self.update_buttons_list_widget.setDefaultDropAction(
            QtCore.Qt.DropAction.IgnoreAction
        )
        self.update_buttons_list_widget.setAlternatingRowColors(False)
        self.update_buttons_list_widget.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.NoSelection
        )
        self.update_buttons_list_widget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.update_buttons_list_widget.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.update_buttons_list_widget.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        QtWidgets.QScroller.grabGesture(
            self.update_buttons_list_widget,
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )
        QtWidgets.QScroller.grabGesture(
            self.update_buttons_list_widget,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )
        self.update_buttons_layout = QtWidgets.QVBoxLayout()
        self.update_buttons_layout.setContentsMargins(15, 20, 20, 5)
        self.update_buttons_layout.addWidget(self.update_buttons_list_widget, 0)
        self.update_buttons_frame.setLayout(self.update_buttons_layout)

        self.main_content_layout.addWidget(self.update_buttons_frame, 0)

        self.infobox_frame = BlocksCustomFrame()
        self.infobox_frame.setMinimumSize(QtCore.QSize(250, 300))

        self.info_box_layout = QtWidgets.QVBoxLayout()
        self.info_box_layout.setContentsMargins(10, 0, 10, 0)

        font = QtGui.QFont()
        font.setFamily(font_family)
        font.setPointSize(20)
        self.version_box = QtWidgets.QHBoxLayout()
        self.version_title = QtWidgets.QLabel(self)
        self.version_title.setText("Current Version: ")
        self.version_title.setMinimumSize(QtCore.QSize(60, 60))
        self.version_title.setMaximumSize(
            QtCore.QSize(int(self.infobox_frame.size().width() * 0.40), 60)
        )
        palette = self.version_title.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.version_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.version_title.setFont(font)
        self.version_title.setPalette(palette)
        self.version_title.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.version_tracking_info = QtWidgets.QLabel(self)
        self.version_tracking_info.setMinimumSize(QtCore.QSize(100, 60))
        self.version_tracking_info.setMaximumSize(QtCore.QSize(16777215, 100))
        palette = self.version_tracking_info.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.version_tracking_info.setFont(font)
        self.version_tracking_info.setPalette(palette)
        self.version_tracking_info.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.version_tracking_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.version_tracking_info.setObjectName("version-tracking")
        self.version_box.addWidget(self.version_title, 0)
        self.version_box.addWidget(self.version_tracking_info, 0)
        self.info_box_layout.addLayout(self.version_box, 1)

        self.remote_version_box = QtWidgets.QHBoxLayout()
        self.remote_version_title = QtWidgets.QLabel(self)
        self.remote_version_title.setText("Remote Version: ")
        self.remote_version_title.setMinimumSize(QtCore.QSize(60, 60))
        self.remote_version_title.setMaximumSize(
            QtCore.QSize(int(self.infobox_frame.size().width() * 0.40), 60)
        )
        palette = self.remote_version_title.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.remote_version_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.remote_version_title.setFont(font)
        self.remote_version_title.setPalette(palette)
        self.remote_version_title.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )
        self.remote_version_box.addWidget(self.remote_version_title, 0)

        self.remote_version_tracking = QtWidgets.QLabel(self)
        self.remote_version_tracking.setMinimumSize(QtCore.QSize(100, 60))
        self.remote_version_tracking.setMaximumSize(
            QtCore.QSize(int(self.infobox_frame.size().width() * 0.60), 60)
        )
        palette = self.remote_version_tracking.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.remote_version_tracking.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.remote_version_tracking.setFont(font)
        self.remote_version_tracking.setPalette(palette)
        self.remote_version_box.addWidget(self.remote_version_tracking, 0)
        self.info_box_layout.addLayout(self.remote_version_box, 1)

        self.button_box = QtWidgets.QVBoxLayout()
        self.button_box.setContentsMargins(0, 0, 0, 0)
        self.button_box.addSpacing(-1)

        self.action_btn = BlocksCustomButton()
        self.action_btn.setMinimumSize(QtCore.QSize(200, 60))
        self.action_btn.setMaximumSize(QtCore.QSize(250, 60))
        font.setPointSize(20)
        self.action_btn.setFont(font)
        self.action_btn.setPalette(palette)
        self.action_btn.setSizePolicy(sizePolicy)
        self.action_btn.setText("Update")
        self.button_box.addWidget(
            self.action_btn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.no_update_placeholder = QtWidgets.QLabel(self)
        self.no_update_placeholder.setMinimumSize(QtCore.QSize(200, 60))
        self.no_update_placeholder.setMaximumSize(QtCore.QSize(300, 60))
        font.setPointSize(20)
        self.no_update_placeholder.setFont(font)
        self.no_update_placeholder.setPalette(palette)
        self.no_update_placeholder.setSizePolicy(sizePolicy)
        self.no_update_placeholder.setText("No Updates Available")
        self.no_update_placeholder.setWordWrap(True)
        self.no_update_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_box_layout.addWidget(
            self.no_update_placeholder, 0, QtCore.Qt.AlignmentFlag.AlignBottom
        )

        self.no_update_placeholder.hide()

        self.info_box_layout.addLayout(
            self.button_box,
            0,
        )
        self.infobox_frame.setLayout(self.info_box_layout)
        self.main_content_layout.addWidget(self.infobox_frame, 1)
        self.update_page_content_layout.addLayout(self.main_content_layout, 1)
        self.setLayout(self.update_page_content_layout)
