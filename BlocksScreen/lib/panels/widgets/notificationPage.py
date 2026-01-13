from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets
import typing

from collections import deque
from typing import Deque

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

        self.model = EntryListModel()
        self.model.setParent(self.update_buttons_list_widget)
        self.entry_delegate = EntryDelegate()
        self.update_buttons_list_widget.setModel(self.model)
        self.update_buttons_list_widget.setItemDelegate(self.entry_delegate)
        self.entry_delegate.item_selected.connect(self.on_item_clicked)
        self.update_back_btn.clicked.connect(self.hide)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)



    def reset_view_model(self) -> None:
        """Clears items from ListView
        (Resets `QAbstractListModel` by clearing entries)
        """
        ...

    def deleteLater(self) -> None:
        """Schedule the object for deletion, resets the list model first"""
        self.reset_view_model()
        return super().deleteLater()

    def showEvent(self, event: QtGui.QShowEvent | None) -> None:
        """Re-add clients to update list"""
        # self.build_model_list()
        return super().showEvent(event)

    def build_model_list(self) -> None:
        """Builds the model list (`self.model`) containing updatable clients"""
        self.update_buttons_list_widget.blockSignals(True)
        self.reset_view_model()
        message  , origin , priority = self.cli_tracking.popleft()
        match priority:
            case 1:
                self._add_notif_entry(message, "#1A8FBF" , QtGui.QPixmap(":/ui/media/btn_icons/info.svg"))
            case 2:
                self._add_notif_entry(message, "#E7E147", QtGui.QPixmap(":/ui/media/btn_icons/troubleshoot.svg"))
            case 3:
                self._add_notif_entry(message, "#CA4949", QtGui.QPixmap(":/ui/media/btn_icons/error.svg"))
            case _:
                self._add_notif_entry(message, "#a4a4a4", QtGui.QPixmap(":/ui/media/btn_icons/info.svg"))
                

        self.model.setData(
            self.model.index(0), True, EntryListModel.EnableRole
        )
        self.on_item_clicked(
            self.model.data(self.model.index(0), QtCore.Qt.ItemDataRole.UserRole)
        )
        self.update_buttons_list_widget.blockSignals(False)

    @QtCore.pyqtSlot(ListItem, name="on-item-clicked")
    def on_item_clicked(self, item: ListItem) -> None:
        """Setup information for the currently clicked list item on the info box.
        Keeps track of the list item
        """
        ...
    
    @QtCore.pyqtSlot(str, str, int,name = "new-notication")
    def new_notication(self, origin: str | None = None, message: str = "", priority: int = 0):
        """
        :param message: sets notification message
        :type message: str
        :param priority: sets notification priority from 0 to 3
        :type priority: int
        """
        self.cli_tracking.append((message, origin, priority))
        self.build_model_list()


    def _add_notif_entry(self, message: str, color: str = "#dfdfdf", right_icon: QtGui.QPixmap | None = None) -> None:
        """Adds a new item to the list model"""
        item = ListItem(
            text=message,
            right_icon=right_icon,
            selected=False,
            _lfontsize=17,
            _rfontsize=12,
            color=color,
            height=60,
            notificate=False,
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
        self.setObjectName("updatePage")
        self.setStyleSheet(
            """#updatePage {
                background-image: url(:/background/media/1st_background.png);
            }"""
        )
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.update_page_content_layout = QtWidgets.QVBoxLayout()
        self.setMinimumSize(800,480)
        self.update_page_content_layout.setContentsMargins(15, 15, 15, 15)

        self.header_content_layout = QtWidgets.QHBoxLayout()
        self.header_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.reload_btn = IconButton(self)
        self.reload_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.reload_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.reload_btn.setFlat(True)
        self.reload_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/refresh.svg"))
        self.header_content_layout.addWidget(
            self.reload_btn
        )  # alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

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
        self.header_title.setObjectName("header-title")
        self.header_title.setText("Notification Page")
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

        self.update_buttons_frame.setMinimumSize(QtCore.QSize(420, 380))
        self.update_buttons_frame.setMaximumSize(QtCore.QSize(450, 500))

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
        self.update_buttons_layout.setContentsMargins(10, 10, 10, 10)
        self.update_buttons_layout.addWidget(self.update_buttons_list_widget, 0)
        self.update_buttons_frame.setLayout(self.update_buttons_layout)

        self.main_content_layout.addWidget(self.update_buttons_frame, 0)

        self.infobox_frame = BlocksCustomFrame()
        self.info_box_layout = QtWidgets.QVBoxLayout()
        self.info_box_layout.setContentsMargins(10, 10, 10, 10)
        self.infobox_frame.setLayout(self.info_box_layout)

        font = QtGui.QFont()
        font.setFamily(font_family)
        font.setPointSize(20)

        self.button_box = QtWidgets.QVBoxLayout()
        self.button_box.setContentsMargins(0, 0, 0, 0)
        self.button_box.addSpacing(-1)

        self.action_btn = BlocksCustomButton()
        self.action_btn.setMinimumSize(QtCore.QSize(200, 60))
        self.action_btn.setMaximumSize(QtCore.QSize(300, 60))
        font.setPointSize(20)
        self.action_btn.setFont(font)
        self.action_btn.setPalette(palette)
        self.action_btn.setSizePolicy(sizePolicy)
        self.action_btn.setText("Update")
        self.action_btn.setPixmap(
            QtGui.QPixmap(":/system/media/btn_icons/update-software-icon.svg")
        )
        self.button_box.addWidget(
            self.action_btn, 0, QtCore.Qt.AlignmentFlag.AlignCenter
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
            self.no_update_placeholder, 0, QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.info_box_layout.addLayout(
            self.button_box,
            0,
        )
        self.main_content_layout.addWidget(self.infobox_frame, 1)
        self.update_page_content_layout.addLayout(self.main_content_layout, 1)
        self.setLayout(self.update_page_content_layout)