from typing import ClassVar

from lib.panels.widgets.popupDialogWidget import Popup
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets


class NotificationPage(QtWidgets.QWidget):
    """Notification panel, lists moonraker/UI notifications and lets the user clear them"""

    has_new_notification: ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="has-new-notification"
    )

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._ICON_INFO = QtGui.QPixmap(":/ui/media/btn_icons/info.svg")
        self._ICON_WARN = QtGui.QPixmap(":/ui/media/btn_icons/troubleshoot.svg")
        self._ICON_ERROR = QtGui.QPixmap(":/ui/media/btn_icons/error.svg")
        self._setupUI()
        self.selected_item: ListItem | None = None
        self.popup = Popup(self)

        self.model = EntryListModel()
        self.model.setParent(self.notification_list_view)
        self.entry_delegate = EntryDelegate()
        self.notification_list_view.setModel(self.model)
        self.notification_list_view.setItemDelegate(self.entry_delegate)
        self.entry_delegate.item_selected.connect(self.on_item_clicked)
        self.model.rowsInserted.connect(self._on_rows_inserted)

        self.back_btn.clicked.connect(self.hide)
        self.delete_btn.clicked.connect(self.delete_selected_item)
        self.delete_all_btn.clicked.connect(self.reset_view_model)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.hide()

    @QtCore.pyqtSlot(name="call-notification-panel")
    def show_notification_panel(
        self,
    ) -> None:
        """Slot for displaying notification Panel"""
        if not self.parent():
            return
        _parent_size = self.parent().size()  # type: ignore
        self.setGeometry(0, 0, _parent_size.width(), _parent_size.height())
        self.updateGeometry()
        self.update()
        self.show()
        self.raise_()
        self.has_new_notification.emit(False)
        if self.model.entries:
            self._select_row(0)

    def delete_selected_item(self) -> None:
        """Deletes currently selected item from the list view"""
        if self.selected_item is None:
            return
        self.model.remove_item(self.selected_item)
        self.selected_item = None
        if self.model.entries:
            self._select_row(0)
        else:
            self._clear_info_box()

    def reset_view_model(self) -> None:
        """Clears items from ListView
        (Resets `QAbstractListModel` by clearing entries)
        """
        self.model.clear()
        self.entry_delegate.clear()
        self.selected_item = None
        self._clear_info_box()
        self.has_new_notification.emit(False)

    def _clear_info_box(self) -> None:
        """Resets the info box to its empty-list default (no item selected)."""
        self.delete_btn.setEnabled(False)
        self.type_label.setText("N/A")
        self.time_label.setText("N/A")

    def _on_rows_inserted(
        self, _parent: QtCore.QModelIndex, first: int, _last: int
    ) -> None:
        """Keep the delegate's prev_index valid when a notification is prepended above it."""
        if first <= self.entry_delegate.prev_index:
            self.entry_delegate.prev_index += 1

    def _select_row(self, row: int) -> None:
        """Selects *row*, clearing the previous selection and refreshing the info box."""
        index = self.model.index(row)
        if not index.isValid():
            return
        if self.entry_delegate.prev_index != row:
            prev_index = self.model.index(self.entry_delegate.prev_index)
            if prev_index.isValid():
                self.model.setData(prev_index, False, EntryListModel.EnableRole)
            self.entry_delegate.prev_index = row
        self.model.setData(index, True, EntryListModel.EnableRole)
        self.on_item_clicked(index.data(QtCore.Qt.ItemDataRole.UserRole))

    def _ingest_notification(self, message: str, priority: int) -> None:
        """Adds *message* to the model, collapsing a repeat of the last entry (moonraker echo spam)."""
        match priority:
            case 1:
                color, icon = "#1A8FBF", self._ICON_INFO
            case 2:
                color, icon = "#E7E147", self._ICON_WARN
            case 3:
                color, icon = "#CA4949", self._ICON_ERROR
            case _:
                color, icon = "#a4a4a4", self._ICON_INFO

        if self.model.refresh_last_if_duplicate(message, color):
            self._select_row(0)
            return

        self.notification_list_view.blockSignals(True)
        try:
            self._add_notif_entry(message, color, icon)
            self._select_row(0)
        finally:
            self.notification_list_view.blockSignals(False)

    @QtCore.pyqtSlot(ListItem, name="on-item-clicked")
    def on_item_clicked(self, item: ListItem) -> None:
        """Setup information for the currently clicked list item on the info box.
        Keeps track of the list item
        """
        self.delete_btn.setEnabled(True)

        match item.color:
            case "#1A8FBF":
                self.type_label.setText("Info")
            case "#E7E147":
                self.type_label.setText("Warning")
            case "#CA4949":
                self.type_label.setText("Error")
            case _:
                self.type_label.setText("Unknown")

        self.time_label.setText(item._cache.get(-1, "N/A"))
        self.selected_item = item

    @QtCore.pyqtSlot(str, str, int, bool, name="new-notication")
    def new_notication(
        self,
        _origin: str | None = None,
        message: str = "",
        priority: int = 0,
        popup: bool = False,
    ):
        """
        :param message: sets notification message
        :type message: str
        :param priority: sets notification priority from 0 to 3
        :type priority: int
        :param popup: sets if notification should appear as popup
        :type popup: bool
        """
        self._ingest_notification(message, priority)

        if popup:
            match priority:
                case 3:
                    msg_type = Popup.MessageType.ERROR
                case 2:
                    msg_type = Popup.MessageType.WARNING
                case 1:
                    msg_type = Popup.MessageType.INFO
                case _:
                    msg_type = Popup.MessageType.UNKNOWN

            self.popup.new_message(message_type=msg_type, message=message, timeout=3000)

        self.has_new_notification.emit(not self.isVisible())

    def _add_notif_entry(
        self,
        message: str,
        color: str = "#dfdfdf",
        right_icon: QtGui.QPixmap | None = None,
    ) -> None:
        """Adds a new item to the list model"""
        item = ListItem(
            text=message,
            left_icon=right_icon,
            selected=False,
            _lfontsize=17,
            _rfontsize=12,
            color=color,
            height=80,
            allow_expand=True,
            notificate=False,
            color_left_icon=True,
        )
        time = QtCore.QDateTime.currentDateTime().toString("hh:mm:ss")
        item._cache[-1] = time
        self.model.insert_item(0, item)

    def _setupUI(self) -> None:
        """Setup UI for the notification panel"""
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.setSizePolicy(sizePolicy)
        self.setObjectName("notificationPage")
        self.setStyleSheet(
            """#notificationPage {
                background-image: url(:/background/media/1st_background.png);
            }"""
        )
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.content_layout = QtWidgets.QVBoxLayout()
        self.setMinimumSize(800, 480)
        self.content_layout.setContentsMargins(15, 15, 15, 15)

        self.header_content_layout = QtWidgets.QHBoxLayout()
        self.header_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.spacer = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        self.header_content_layout.addItem(self.spacer)

        self.header_title = QtWidgets.QLabel(self)
        self.header_title.setMinimumSize(QtCore.QSize(100, 60))
        self.header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        palette = self.header_title.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.header_title.setFont(font)
        font.setPointSize(15)
        self.header_title.setPalette(palette)
        self.header_title.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.header_title.setObjectName("header-title")
        self.header_title.setText("Notification")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.header_title.setSizePolicy(sizePolicy)
        self.header_content_layout.addWidget(
            self.header_title, alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.back_btn = IconButton(self)
        self.back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.back_btn.setFlat(True)
        self.back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.header_content_layout.addWidget(
            self.back_btn
        )  # alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addLayout(self.header_content_layout, 0)

        self.main_content_layout = QtWidgets.QHBoxLayout()
        self.main_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.list_frame = BlocksCustomFrame(self)

        self.list_frame.setMinimumSize(QtCore.QSize(500, 380))
        self.list_frame.setMaximumSize(QtCore.QSize(560, 500))

        self.notification_list_view = QtWidgets.QListView(self.list_frame)
        self.notification_list_view.setMouseTracking(True)
        self.notification_list_view.setTabletTracking(True)

        self.notification_list_view.setPalette(palette)
        self.notification_list_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.notification_list_view.setStyleSheet("background-color:transparent")
        self.notification_list_view.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.notification_list_view.setMinimumSize(self.list_frame.size())
        self.notification_list_view.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.notification_list_view.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.notification_list_view.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.notification_list_view.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.notification_list_view.setAutoScroll(False)
        self.notification_list_view.setProperty("showDropIndicator", False)
        self.notification_list_view.setDefaultDropAction(
            QtCore.Qt.DropAction.IgnoreAction
        )
        self.notification_list_view.setAlternatingRowColors(False)
        self.notification_list_view.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.NoSelection
        )
        self.notification_list_view.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.notification_list_view.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.notification_list_view.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        QtWidgets.QScroller.grabGesture(
            self.notification_list_view,
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )
        QtWidgets.QScroller.grabGesture(
            self.notification_list_view,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )
        self.list_frame_layout = QtWidgets.QVBoxLayout()
        self.list_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.list_frame_layout.addWidget(self.notification_list_view, 0)
        self.list_frame.setLayout(self.list_frame_layout)

        self.main_content_layout.addWidget(self.list_frame)

        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(5, 5, 5, 5)

        self.info_frame = BlocksCustomFrame()
        self.info_frame.setMinimumSize(QtCore.QSize(200, 150))

        self.info_box_layout = QtWidgets.QGridLayout(self.info_frame)
        self.info_box_layout.setContentsMargins(0, 0, 0, 0)

        self.type_title = QtWidgets.QLabel(self.info_frame)
        self.type_title.setText("Type:")
        self.type_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_box_layout.addWidget(self.type_title, 1, 1)

        self.type_label = QtWidgets.QLabel(self.info_frame)
        self.type_label.setText("N/A")
        self.type_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_box_layout.addWidget(self.type_label, 1, 2)

        self.time_title = QtWidgets.QLabel(self.info_frame)
        self.time_title.setText("Time:")
        self.time_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_box_layout.addWidget(self.time_title, 2, 1)

        self.time_label = QtWidgets.QLabel(self.info_frame)
        self.time_label.setText("N/A")
        self.time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_box_layout.addWidget(self.time_label, 2, 2)

        # Equal stretch keeps the Type/Time gap instead of collapsing it into the padding.
        self.info_box_layout.setColumnStretch(0, 1)
        self.info_box_layout.setColumnStretch(3, 1)
        self.info_box_layout.setRowStretch(0, 1)
        self.info_box_layout.setRowStretch(1, 1)
        self.info_box_layout.setRowStretch(2, 1)
        self.info_box_layout.setRowStretch(3, 1)

        self.type_title.setFont(font)
        self.type_title.setStyleSheet("color:#FFFFFF")

        self.time_title.setFont(font)
        self.time_title.setStyleSheet("color:#FFFFFF")

        self.type_label.setFont(font)
        self.type_label.setStyleSheet("color:#FFFFFF")

        self.time_label.setFont(font)
        self.time_label.setStyleSheet("color:#FFFFFF")

        self.info_frame.setLayout(self.info_box_layout)

        self.buttons_frame = BlocksCustomFrame()
        self.buttons_frame.setMinimumSize(QtCore.QSize(200, 200))
        self.buttons_frame.setMaximumSize(QtCore.QSize(300, 200))

        self.button_box_layout = QtWidgets.QVBoxLayout()
        self.button_box_layout.setContentsMargins(10, 10, 10, 10)
        self.buttons_frame.setLayout(self.button_box_layout)

        self.button_box = QtWidgets.QVBoxLayout()
        self.button_box.setContentsMargins(0, 0, 0, 0)

        self.button_box.addItem(
            QtWidgets.QSpacerItem(
                20,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.delete_btn = BlocksCustomButton()
        self.delete_btn.setMinimumSize(QtCore.QSize(200, 60))
        self.delete_btn.setMaximumSize(QtCore.QSize(300, 60))
        font.setPointSize(15)

        self.delete_btn.setFont(font)
        self.delete_btn.setPalette(palette)
        self.delete_btn.setSizePolicy(sizePolicy)
        self.delete_btn.setText("Delete")
        self.delete_btn.setEnabled(False)
        self.delete_btn.setPixmap(
            QtGui.QPixmap(":/ui/media/btn_icons/garbage-icon.svg")
        )
        self.button_box.addWidget(
            self.delete_btn, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.delete_all_btn = BlocksCustomButton()
        self.delete_all_btn.setMinimumSize(QtCore.QSize(200, 60))
        self.delete_all_btn.setMaximumSize(QtCore.QSize(300, 60))
        font.setPointSize(15)
        self.delete_all_btn.setFont(font)
        self.delete_all_btn.setPalette(palette)
        self.delete_all_btn.setSizePolicy(sizePolicy)
        self.delete_all_btn.setText("Delete all")
        self.delete_all_btn.setPixmap(
            QtGui.QPixmap(":/ui/media/btn_icons/garbage-icon.svg")
        )
        self.button_box.addWidget(
            self.delete_all_btn, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.button_box_layout.addLayout(
            self.button_box,
            0,
        )

        self.vlayout.addWidget(self.info_frame)
        self.vlayout.addWidget(self.buttons_frame)

        self.main_content_layout.addLayout(self.vlayout)
        self.content_layout.addLayout(self.main_content_layout, 1)
        self.setLayout(self.content_layout)
