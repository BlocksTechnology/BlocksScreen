from lib.panels.widgets.loadWidget import LoadingOverlayWidget
from lib.panels.widgets.basePopup import BasePopup
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets

import typing


class InputShaperPage(QtWidgets.QWidget):
    """Update GUI Page,
    retrieves from moonraker available clients and adds functionality
    for updating or recovering them
    """

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )

    def __init__(self, parent=None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()
        self._setupUI()
        self.selected_item: ListItem | None = None
        self.ongoing_update: bool = False
        self.type_dict: dict = {}

        self.loadscreen = BasePopup(self, floating=False, dialog=False)
        self.loadwidget = LoadingOverlayWidget(
            self, LoadingOverlayWidget.AnimationGIF.DEFAULT
        )
        self.loadscreen.add_widget(self.loadwidget)
        self.repeated_request_status = QtCore.QTimer()
        self.repeated_request_status.setInterval(2000)  # every 2 seconds
        self.model = EntryListModel()
        self.model.setParent(self.update_buttons_list_widget)
        self.entry_delegate = EntryDelegate()
        self.update_buttons_list_widget.setModel(self.model)
        self.update_buttons_list_widget.setItemDelegate(self.entry_delegate)
        self.entry_delegate.item_selected.connect(self.on_item_clicked)
        self.update_back_btn.clicked.connect(self.reset_view_model)

        self.action_btn.clicked.connect(self.handle_ism_confirm)

    def handle_update_end(self) -> None:
        """Handles update end signal
        (closes loading page, returns to normal operation)
        """
        if self.load_popup.isVisible():
            self.load_popup.close()
        self.repeated_request_status.stop()
        self.build_model_list()

    def handle_ongoing_update(self) -> None:
        """Handled ongoing update signal,
        calls loading page (blocks user interaction)
        """
        self.loadwidget.set_status_message("Updating...")
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

    def showEvent(self, a0: QtGui.QShowEvent | None) -> None:
        """Re-add clients to update list"""
        return super().showEvent(a0)

    def build_model_list(self) -> None:
        """Builds the model list (`self.model`) containing updatable clients"""
        self.update_buttons_list_widget.blockSignals(True)
        self.model.setData(self.model.index(0), True, EntryListModel.EnableRole)
        self.on_item_clicked(
            self.model.data(self.model.index(0), QtCore.Qt.ItemDataRole.UserRole)
        )
        self.update_buttons_list_widget.blockSignals(False)

    def set_type_dictionary(self, dict) -> None:
        """Receives the dictionary of input shaper types from the utilities tab"""
        self.type_dict = dict
        return

    @QtCore.pyqtSlot(ListItem, name="on-item-clicked")
    def on_item_clicked(self, item: ListItem) -> None:
        """Setup information for the currently clicked list item on the info box.
        Keeps track of the list item
        """
        self.currentItem: ListItem = item
        if not item:
            return
        current_info = self.type_dict.get(self.currentItem.text, {})
        if not current_info:
            return

        self.vib_label.setText(str("%.0f" % current_info.get("vibration", "N/A")) + "%")
        self.sug_accel_label.setText(
            str("%.0f" % current_info.get("max_accel", "N/A")) + "mm/s²"
        )

        self.action_btn.show()

    def handle_ism_confirm(self) -> None:
        current_info = self.type_dict.get(self.currentItem.text, {})
        frequency = current_info.get("frequency", "N/A")
        if self.type_dict["Axis"] == "x":
            self.run_gcode_signal.emit(
                f"SET_INPUT_SHAPER SHAPER_TYPE_X={self.currentItem.text} SHAPER_FREQ_X={frequency}"
            )
        elif self.type_dict["Axis"] == "y":
            self.run_gcode_signal.emit(
                f"SET_INPUT_SHAPER SHAPER_TYPE_Y={self.currentItem.text} SHAPER_FREQ_Y={frequency}"
            )

        self.run_gcode_signal.emit("SAVE_CONFIG")
        self.reset_view_model()

    def add_type_entry(self, cli_name: str, recommended: str = "") -> None:
        """Adds a new item to the list model"""
        item = ListItem(
            text=cli_name,
            right_text=recommended,
            right_icon=QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg"),
            selected=False,
            _lfontsize=17,
            _rfontsize=9,
            height=60,
            allow_check=True,
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
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.update_page_content_layout = QtWidgets.QVBoxLayout()
        self.update_page_content_layout.setContentsMargins(15, 15, 2, 2)

        self.header_content_layout = QtWidgets.QHBoxLayout()
        self.header_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.spacer_left = QtWidgets.QLabel(self)
        self.spacer_left.setMinimumSize(QtCore.QSize(60, 60))
        self.spacer_left.setMaximumSize(QtCore.QSize(60, 60))
        self.header_content_layout.addWidget(self.spacer_left, 0)
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
        self.header_title.setText("Input Shaper")
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

        self.update_buttons_frame.setMinimumSize(QtCore.QSize(300, 300))
        self.update_buttons_frame.setMaximumSize(QtCore.QSize(350, 500))

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
        self.info_box_layout.setContentsMargins(10, 10, 10, 10)

        font = QtGui.QFont()
        font.setFamily(font_family)
        font.setPointSize(20)
        self.info_box = QtWidgets.QGridLayout()
        self.info_box.setContentsMargins(0, 0, 0, 0)

        self.vib_title_label = QtWidgets.QLabel(self)
        self.vib_title_label.setText("Vibrations: ")
        self.vib_title_label.setMinimumSize(QtCore.QSize(60, 60))
        self.vib_title_label.setMaximumSize(
            QtCore.QSize(int(self.infobox_frame.size().width() * 0.40), 9999)
        )
        palette = self.vib_title_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.vib_title_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.vib_title_label.setFont(font)
        self.vib_title_label.setPalette(palette)
        self.vib_title_label.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.vib_label = QtWidgets.QLabel(self)
        self.vib_label.setMinimumSize(QtCore.QSize(100, 60))
        self.vib_label.setMaximumSize(QtCore.QSize(16777215, 9999))
        palette = self.vib_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.vib_label.setFont(font)
        self.vib_label.setPalette(palette)
        self.vib_label.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.vib_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.vib_label.setObjectName("version-tracking")

        self.info_box.addWidget(self.vib_title_label, 0, 0)
        self.info_box.addWidget(self.vib_label, 0, 1)

        self.sug_accel_title_label = QtWidgets.QLabel(self)
        self.sug_accel_title_label.setText("Sugested Max\nAcceleration:")
        self.sug_accel_title_label.setMinimumSize(QtCore.QSize(60, 60))
        self.sug_accel_title_label.setMaximumSize(
            QtCore.QSize(int(self.infobox_frame.size().width() * 0.40), 9999)
        )
        palette = self.sug_accel_title_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.sug_accel_title_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.sug_accel_title_label.setFont(font)
        self.sug_accel_title_label.setPalette(palette)
        self.sug_accel_title_label.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft
        )

        self.sug_accel_label = QtWidgets.QLabel(self)
        self.sug_accel_label.setMinimumSize(QtCore.QSize(100, 60))
        self.sug_accel_label.setMaximumSize(
            QtCore.QSize(int(self.infobox_frame.size().width() * 0.60), 9999)
        )
        palette = self.sug_accel_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.sug_accel_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sug_accel_label.setFont(font)
        self.sug_accel_label.setPalette(palette)

        self.info_box.addWidget(self.sug_accel_title_label, 1, 0)
        self.info_box.addWidget(self.sug_accel_label, 1, 1)

        self.info_box_layout.addLayout(self.info_box, 1)

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
        self.action_btn.setText("Confirm")
        self.action_btn.setPixmap(QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg"))
        self.button_box.addWidget(
            self.action_btn,
            0,
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignBottom,
        )

        self.info_box_layout.addLayout(
            self.button_box,
            0,
        )
        self.infobox_frame.setLayout(self.info_box_layout)
        self.main_content_layout.addWidget(self.infobox_frame, 1)
        self.update_page_content_layout.addLayout(self.main_content_layout, 1)
        self.setLayout(self.update_page_content_layout)
