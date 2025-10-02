import typing
from dataclasses import dataclass

from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


@dataclass
class ListItem:
    text: str
    right_text: str | None = None
    icon: QtGui.QPixmap | None = None
    callback: callable = None
    selected: bool = False
    allow_check: bool = True
    _lfontsize: int = 0
    _rfontsize: int = 0


class UpdatePage(QtWidgets.QWidget):
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
        str, name="update-refresh"
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

    def __init__(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self._setupUI()
        self.cli_tracking = {}
        self.model = EntryListModel()
        self.model.setParent(self.update_buttons_list_widget)
        self.entry_delegate = EntryDelegate()
        self.update_buttons_list_widget.setModel(self.model)
        self.entry_delegate.item_selected.connect(self.on_item_clicked)
        self.update_btn.clicked.connect(self.on_update_clicked)
        self.recover_btn.clicked.connect(self.on_recover_clicked)
        self.update_back_btn.clicked.connect(self.reset_view_model)

        self.update_buttons_list_widget.setModel(self.model)
        self.update_buttons_list_widget.setItemDelegate(self.entry_delegate)

    def reset_view_model(self) -> None:
        """Clears items from ListView (Resets `QAbstractListModel` by clearing entries)"""
        self.model.clear()
        self.entry_delegate.clear()
        self.update_buttons_list_widget.selectionModel().clear()
        self.request_update_status.emit(True)

    def deleteLater(self) -> None:
        self.reset_view_model()
        return super().deleteLater()

    def showEvent(self, a0: QtGui.QShowEvent | None) -> None:
        """Re-add clients to update list"""
        self.update_buttons_list_widget.blockSignals(True)
        for cli_name in self.cli_tracking.keys():
            self.add_update_entry(cli_name)
        self.model.setData(
            self.model.index(0), True, EntryListModel.EnableRole
        )  # Set the first item checked on startup
        self.update_buttons_list_widget.blockSignals(False)
        return super().showEvent(a0)

    def hide(self) -> None:
        return super().hide()

    @QtCore.pyqtSlot(name="on-recover-clicked")
    def on_recover_clicked(self) -> None:
        """Handle `recover_btn` clicked event"""
        ...

    @QtCore.pyqtSlot(name="on-update-clicked")
    def on_update_clicked(self) -> None:
        """Handle `update_btn` clicked event"""
        ...

    @QtCore.pyqtSlot(str, name="on-item-clicked")
    def on_item_clicked(self, name: str) -> None:
        """Setup information for the currently clicked list item on the info box. Keeps track of the list item"""
        cli_data = self.cli_tracking.get(name, {})
        if not cli_data:
            self.version_tracking_info.setText("Missing, Cannot Update")
        if name == "system":
            updatable_packages = cli_data.get("package_count", 0)
            self.recover_btn.hide()
            if updatable_packages == 0:
                self.version_tracking_info.setText("No updates")
                self.update_btn.hide()
                self.remote_version_title.hide()
                self.remote_version_tracking.hide()
                self.version_tracking_info.setWordWrap(True)
                return
            self.version_tracking_info.setText(
                f"{updatable_packages} upgradable \n packages"
            )
            self.update_btn.show()
            return
        self.update_btn.show()
        self.recover_btn.show()
        self.remote_version_title.show()
        self.remote_version_tracking.show()
        self.version_tracking_info.setText(cli_data.get("version", "Missing"))

    @QtCore.pyqtSlot(dict, name="handle-update-message")
    def handle_update_message(self, message: dict) -> None:
        """Handle receiving current state of each item update.

        Receives updates from moonraker `machine.update.status` request.
        """
        busy = message.get("busy", False)
        if busy:
            self.update_in_progress.emit()
        cli_version_info = message.get("version_info", None)
        if not cli_version_info:
            return
        self.cli_tracking = cli_version_info

    def add_update_entry(self, cli_name: str) -> None:
        item = ListItem(
            text=cli_name,
            icon=QtGui.QPixmap(":/ui/media/btn_icons/info.svg"),
            callback=self.on_item_clicked,
            selected=False,
            right_text=None,
            _lfontsize=17,
            _rfontsize=12,
        )
        self.model.add_item(item)

    def _setupUI(self) -> None:
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
        self.remote_version_tracking.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.remote_version_tracking.setFont(font)
        self.remote_version_tracking.setPalette(palette)
        self.remote_version_box.addWidget(self.remote_version_tracking, 0)
        self.info_box_layout.addLayout(self.remote_version_box, 1)

        self.button_box = QtWidgets.QVBoxLayout()
        self.button_box.setContentsMargins(0, 0, 0, 0)
        self.button_box.addSpacing(-1)

        self.update_btn = BlocksCustomButton()
        self.update_btn.setMinimumSize(QtCore.QSize(200, 60))
        self.update_btn.setMaximumSize(QtCore.QSize(250, 60))
        font.setPointSize(20)
        self.update_btn.setFont(font)
        self.update_btn.setPalette(palette)
        self.update_btn.setSizePolicy(sizePolicy)
        self.update_btn.text
        self.update_btn.setText("Update")
        self.button_box.addWidget(
            self.update_btn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.recover_btn = BlocksCustomButton()
        self.recover_btn.setMinimumSize(QtCore.QSize(200, 60))
        self.recover_btn.setMaximumSize(QtCore.QSize(250, 60))
        font.setPointSize(20)
        self.recover_btn.setFont(font)
        self.recover_btn.setPalette(palette)
        self.recover_btn.setSizePolicy(sizePolicy)
        self.recover_btn.text
        self.recover_btn.setText("Recover")
        self.button_box.addWidget(
            self.recover_btn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.info_box_layout.addLayout(
            self.button_box,
            0,
        )
        self.infobox_frame.setLayout(self.info_box_layout)
        self.main_content_layout.addWidget(self.infobox_frame, 1)
        self.update_page_content_layout.addLayout(self.main_content_layout, 1)
        self.setLayout(self.update_page_content_layout)


class EntryListModel(QtCore.QAbstractListModel):
    EnableRole = QtCore.Qt.ItemDataRole.UserRole + 1

    def __init__(self, entries=None) -> None:
        super().__init__()
        self.entries = entries or []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.entries)

    def deleteLater(self) -> None:
        return super().deleteLater()

    def clear(self) -> None:
        self.beginResetModel()
        self.entries.clear()
        self.endResetModel()

    def add_item(self, item: ListItem) -> None:
        self.beginInsertRows(
            QtCore.QModelIndex(),
            self.rowCount(),
            self.rowCount(),
        )
        self.entries.append(item)
        self.endInsertRows()

    def flags(self, index):
        item = self.entries[index.row()]
        flags = QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable
        if item.allow_check:
            flags |= QtCore.Qt.ItemFlag.ItemIsUserCheckable
        return flags

    def setData(
        self, index: QtCore.QModelIndex, value: typing.Any, role: int = ...
    ) -> bool:
        if not index.isValid():
            return False
        if role == EntryListModel.EnableRole:
            item = self.entries[index.row()]
            item.selected = value
            self.dataChanged.emit(index, index, [EntryListModel.EnableRole])
            return True
        if role == QtCore.Qt.ItemDataRole.UserRole:
            self.dataChanged.emit(index, index, [QtCore.Qt.ItemDataRole.UserRole])
            return True
        return False

    def data(self, index: QtCore.QModelIndex, role: int):
        if not index.isValid():
            return
        item: ListItem = self.entries[index.row()]
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return item
        if role == EntryListModel.EnableRole:
            return item.selected


class EntryDelegate(QtWidgets.QStyledItemDelegate):
    item_selected: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="item-selected"
    )

    def __init__(self) -> None:
        super().__init__()
        self.prev_index: int = 0

    def clear(self) -> None:
        self.prev_index = 0

    def sizeHint(self, option, index):
        base = super().sizeHint(option, index)
        return QtCore.QSize(base.width(), base.height() + 55)

    def paint(self, painter: QtGui.QPainter, option, index):
        item = index.data(QtCore.Qt.ItemDataRole.UserRole)
        painter.save()
        rect = option.rect
        rect.setHeight(60)
        button = QtWidgets.QStyleOptionButton()
        style = QtWidgets.QApplication.style()
        if not style:
            return
        style.drawControl(
            QtWidgets.QStyle.ControlElement.CE_PushButton, button, painter
        )
        button.rect = rect
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform, True)
        radius = rect.height() / 5.0

        # Main rounded rectangle path (using the adjusted rect)
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(rect), radius, radius)

        # Ellipse ("hole") for the icon on the right
        ellipse_margin = rect.height() * 0.05
        ellipse_size = rect.height() * 0.90
        ellipse_rect = QtCore.QRectF(
            rect.right() - ellipse_margin - ellipse_size,
            rect.top() + ellipse_margin,
            ellipse_size,
            ellipse_size,
        )
        ellipse_path = QtGui.QPainterPath()
        ellipse_path.addEllipse(ellipse_rect)

        # Ellipse ("hole") for the icon on the left (only if present)
        left_icon_margin = rect.height() * 0.05
        left_icon_size = rect.height() * 0.50
        left_icon_rect = QtCore.QRectF(
            rect.left() + left_icon_margin,
            rect.top() + left_icon_margin,
            left_icon_size,
            left_icon_size,
        )
        left_margin = 10  # default left margin

        # Gradient background (left to right)
        if not item.selected:
            pressed_color = QtGui.QColor("#1A8FBF")
            pressed_color.setAlpha(20)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(pressed_color)
            painter.fillPath(path, pressed_color)
        else:
            pressed_color = QtGui.QColor("#1A8FBF")
            pressed_color.setAlpha(90)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(pressed_color)
            painter.fillPath(path, pressed_color)

        # Draw icon inside the ellipse "hole" (on the right)
        if not item.icon.isNull():
            icon_margin = ellipse_size * 0.10
            icon_rect = QtCore.QRectF(
                ellipse_rect.left() + icon_margin / 2,
                ellipse_rect.top() + icon_margin / 2,
                ellipse_rect.width() - icon_margin,
                ellipse_rect.height() - icon_margin,
            )
            icon_scaled = item.icon.scaled(
                icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            # Center the icon in the ellipse
            adjusted_x = icon_rect.x() + (icon_rect.width() - icon_scaled.width()) / 2.0
            adjusted_y = (
                icon_rect.y() + (icon_rect.height() - icon_scaled.height()) / 2.0
            )
            adjusted_icon_rect = QtCore.QRectF(
                adjusted_x,
                adjusted_y,
                icon_scaled.width(),
                icon_scaled.height(),
            )
            painter.drawPixmap(
                adjusted_icon_rect, icon_scaled, icon_scaled.rect().toRectF()
            )

        # Draw text, area before the ellipse (adjusted for left icon)
        text_margin = int(
            rect.right() - ellipse_size - ellipse_margin - rect.height() * 0.10
        )
        text_rect = QtCore.QRectF(
            rect.left() + left_margin,
            rect.top(),
            text_margin - rect.left() - left_margin,
            rect.height(),
        )

        # Draw main text (left-aligned)
        painter.setPen(QtGui.QColor(255, 255, 255))
        _font = painter.font()
        _font.setPointSize(item._lfontsize)
        painter.setFont(_font)
        metrics = QtGui.QFontMetrics(_font)
        main_text_height = metrics.height()

        # Vertically center text
        text_y = rect.top() + (rect.height() + main_text_height) / 2 - metrics.descent()

        # Calculate where to start the right text: just left of the right icon ellipse
        gap = 10  # gap between right text and icon ellipse
        right_font = QtGui.QFont(_font)
        right_font.setPointSize(item._rfontsize)
        right_metrics = QtGui.QFontMetrics(right_font)
        right_text_width = right_metrics.horizontalAdvance(item.right_text)

        # The right text should end at ellipse_rect.left() - gap
        right_text_x = ellipse_rect.left() - gap - right_text_width

        # Draw main text (left-aligned, but don't overlap right text)
        max_main_text_width = (
            right_text_x - text_rect.left() - 10
        )  # 10px gap between main and right text
        elided_main_text = metrics.elidedText(
            item.text,
            QtCore.Qt.TextElideMode.ElideRight,
            int(max_main_text_width),
        )

        painter.setFont(_font)
        painter.drawText(
            int(text_rect.left()),
            int(text_y),
            elided_main_text,
        )

        # Draw right text (smaller, grey, just left of the icon)
        if item.right_text:
            painter.setFont(right_font)
            painter.setPen(QtGui.QColor(160, 160, 160))  # grey color
            right_text_height = right_metrics.height()
            right_text_y = (
                rect.top()
                + (rect.height() + right_text_height) / 2
                - right_metrics.descent()
            )
            painter.drawText(
                int(right_text_x),
                int(right_text_y),
                item.right_text,
            )
        painter.restore()

    def editorEvent(
        self,
        event: QtCore.QEvent,
        model: EntryListModel,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):
        item = index.data(QtCore.Qt.ItemDataRole.UserRole)
        if item.selected:
            self.item_selected.emit(item.text)
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            item.callback("Can call callback")
            if self.prev_index is None:
                return False
            if self.prev_index != index.row():
                prev_index: QtCore.QModelIndex = model.index(self.prev_index)
                model.setData(prev_index, False, EntryListModel.EnableRole)
                self.prev_index = index.row()
            model.setData(index, True, EntryListModel.EnableRole)
            self.item_selected.emit(item.text)
            return True
        return False
