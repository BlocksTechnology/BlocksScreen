from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets
import typing

from collections import deque
from typing import Deque


from lib.panels.widgets.popupDialogWidget import Popup


class NotificationPage(QtWidgets.QWidget):
    """Update GUI Page,
    retrieves from moonraker available clients and adds functionality
    for updating or recovering them
    """

    on_update_message: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="on-update-message"
    )

    def __init__(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self._setupUI()
        self.cli_tracking: Deque = deque()
        self.selected_item: ListItem | None = None
        self.ongoing_update: bool = False
        self.popup = Popup(self)

        self.model = EntryListModel()
        self.model.setParent(self.update_buttons_list_widget)
        self.entry_delegate = EntryDelegate()
        self.update_buttons_list_widget.setModel(self.model)
        self.update_buttons_list_widget.setItemDelegate(self.entry_delegate)
        self.entry_delegate.item_selected.connect(self.on_item_clicked)

        self.update_back_btn.clicked.connect(self.hide)
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

    def delete_selected_item(self) -> None:
        """Deletes currently selected item from the list view"""
        if self.selected_item is None:
            return
        self.model.remove_item(self.selected_item)
        self.delete_btn.setEnabled(False)
        self.selected_item = None

    def reset_view_model(self) -> None:
        """Clears items from ListView
        (Resets `QAbstractListModel` by clearing entries)
        """
        self.model.clear()
        self.entry_delegate.clear()

    def build_model_list(self) -> None:
        """Builds the model list (`self.model`) containing updatable clients"""
        self.update_buttons_list_widget.blockSignals(True)
        message, origin, priority = self.cli_tracking.popleft()
        match priority:
            case 1:
                self._add_notif_entry(
                    message, "#1A8FBF", QtGui.QPixmap(":/ui/media/btn_icons/info.svg")
                )
            case 2:
                self._add_notif_entry(
                    message,
                    "#E7E147",
                    QtGui.QPixmap(":/ui/media/btn_icons/troubleshoot.svg"),
                )
            case 3:
                self._add_notif_entry(
                    message, "#CA4949", QtGui.QPixmap(":/ui/media/btn_icons/error.svg")
                )
            case _:
                self._add_notif_entry(
                    message, "#a4a4a4", QtGui.QPixmap(":/ui/media/btn_icons/info.svg")
                )

        self.model.setData(self.model.index(0), True, EntryListModel.EnableRole)
        self.update_buttons_list_widget.blockSignals(False)

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
        self, origin: str | None = None, message: str = "", priority: int = 0 , popup: bool = False
    ):
        """
        :param message: sets notification message
        :type message: str
        :param priority: sets notification priority from 0 to 3
        :type priority: int
        :param popup: sets if notification should appear as popup
        :type popup: bool
        """
        self.cli_tracking.append((message, origin, priority))
        self.model.delete_duplicates()

        if popup:
            ui = False
            match priority:
                case 3:
                    type = Popup.MessageType.ERROR
                    ui = True
                case 2:
                    type = Popup.MessageType.WARNING
                case 1:
                    type = Popup.MessageType.INFO
                case _:
                    type = Popup.MessageType.UNKNOWN
                
            self.popup.new_message(
                message_type=type, message=message , userInput=ui
            )

        self.build_model_list()

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
        )
        time = QtCore.QDateTime.currentDateTime().toString("hh:mm:ss")
        item._cache[-1] = time
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
        font = QtGui.QFont()
        font.setPointSize(20)
        self.setSizePolicy(sizePolicy)
        self.setObjectName("updatePage")
        self.setStyleSheet(
            """#updatePage {
                background-image: url(:/background/media/1st_background.png);
            }"""
        )
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.update_page_content_layout = QtWidgets.QVBoxLayout()
        self.setMinimumSize(800, 480)
        self.update_page_content_layout.setContentsMargins(15, 15, 15, 15)

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
        self.update_back_btn = IconButton(self)
        self.update_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.update_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.update_back_btn.setFlat(True)
        self.update_back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.header_content_layout.addWidget(
            self.update_back_btn
        )  # alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.update_page_content_layout.addLayout(self.header_content_layout, 0)

        self.main_content_layout = QtWidgets.QHBoxLayout()
        self.main_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.update_buttons_frame = BlocksCustomFrame(self)

        self.update_buttons_frame.setMinimumSize(QtCore.QSize(500, 380))
        self.update_buttons_frame.setMaximumSize(QtCore.QSize(560, 500))

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
        self.update_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.update_buttons_layout.addWidget(self.update_buttons_list_widget, 0)
        self.update_buttons_frame.setLayout(self.update_buttons_layout)

        self.main_content_layout.addWidget(self.update_buttons_frame)

        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(5, 5, 5, 5)

        self.info_frame = BlocksCustomFrame()
        self.info_frame.setMinimumSize(QtCore.QSize(200, 150))

        self.spacer_item = QtWidgets.QSpacerItem(
            20,
            20,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        self.info_box_layout = QtWidgets.QGridLayout(self.info_frame)
        self.info_box_layout.setContentsMargins(0, 0, 0, 0)

        self.info_box_layout.addItem(self.spacer_item, 0, 0)

        self.type_title = QtWidgets.QLabel(self.info_frame)
        self.type_title.setText("Type:")
        self.type_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_box_layout.addWidget(self.type_title, 1, 0)

        self.type_label = QtWidgets.QLabel(self.info_frame)
        self.type_label.setText("N/A")
        self.type_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_box_layout.addWidget(self.type_label, 1, 1)

        self.time_title = QtWidgets.QLabel(self.info_frame)
        self.time_title.setText("Time:")
        self.time_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_box_layout.addWidget(self.time_title, 2, 0)

        self.time_label = QtWidgets.QLabel(self.info_frame)
        self.time_label.setText("N/A")
        self.time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_box_layout.addWidget(self.time_label, 2, 1)

        self.type_title.setFont(font)
        self.type_title.setStyleSheet("color:#FFFFFF")

        self.time_title.setFont(font)
        self.time_title.setStyleSheet("color:#FFFFFF")

        self.time_title.setFont(font)
        self.type_label.setStyleSheet("color:#FFFFFF")

        self.time_title.setFont(font)
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
        self.button_box.addSpacing(-1)

        self.button_box.addItem(self.spacer_item)

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
        self.update_page_content_layout.addLayout(self.main_content_layout, 1)
        self.setLayout(self.update_page_content_layout)
