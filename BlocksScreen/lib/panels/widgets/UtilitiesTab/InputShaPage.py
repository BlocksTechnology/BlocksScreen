import re
import typing

from lib.panels.widgets.Common.basePopup import BasePopup
from lib.panels.widgets.Common.optionCardWidget import OptionCard
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets


class InputShaperPage(QtWidgets.QStackedWidget):
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    call_load_panel = QtCore.pyqtSignal(bool, str, bool, name="call-load-panel")
    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    def __init__(self, parent=None, logic: bool = False) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()

        # flag that disable all UI usage (headless per say) <- current use on utilities tab
        self.logic: bool = logic

        self.currentItem: ListItem | None = None
        self.type_dict: dict = {}
        self.is_types: dict = {}
        self.is_aut_types: dict = {}
        self.aut: bool = False

        self._is_timeout_timer: QtCore.QTimer = QtCore.QTimer(self)
        self._is_timeout_timer.setSingleShot(True)
        self._is_timeout_timer.setInterval(300_000)  # 5 min: longest plausible IS run
        self._is_timeout_timer.timeout.connect(self._on_is_timeout)

        if self.logic:
            return

        self._setup_ui()

        self.model = EntryListModel()
        self.model.setParent(self.update_buttons_list_widget)
        self.entry_delegate = EntryDelegate()
        self.update_buttons_list_widget.setModel(self.model)
        self.update_buttons_list_widget.setItemDelegate(self.entry_delegate)
        self.entry_delegate.item_selected.connect(self.on_item_clicked)
        self.update_back_btn.clicked.connect(self.reset_view_model)

        self.is_back_btn.clicked.connect(self.request_back_button)

        self.dialog_page = BasePopup(self, dialog=True, floating=True)
        self.addWidget(self.dialog_page)
        self.dialog_page.confirm_button.clicked.connect(
            lambda: self.handle_is("SHAPER_CALIBRATE AXIS=Y")
        )
        self.dialog_page.cancel_button.clicked.connect(
            lambda: self.handle_is("SHAPER_CALIBRATE AXIS=X")
        )

        self.action_btn.clicked.connect(self.handle_ism_confirm)

        self.automatic_card_is = OptionCard(
            self,
            "Automatic\nInput Shaper",
            "Automatic Input Shaper",
            QtGui.QPixmap(":/input_shaper/media/btn_icons/input_shaper_auto.svg"),
        )  # type: ignore
        self.automatic_card_is.setObjectName("Automatic_IS_Card")
        self.is_content_layout.addWidget(
            self.automatic_card_is, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.automatic_card_is.clicked.connect(
            lambda: self.handle_is("SHAPER_CALIBRATE")
        )

        self.manual__card_is = OptionCard(
            self,
            "Manual\nInput Shaper",
            "Manual Input Shaper",
            QtGui.QPixmap(":/input_shaper/media/btn_icons/input_shaper_manual.svg"),
        )  # type: ignore
        self.manual__card_is.setObjectName("Manual_IS_Card")
        self.is_content_layout.addWidget(
            self.manual__card_is, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.manual__card_is.clicked.connect(lambda: self.handle_is(""))

        self.setCurrentIndex(self.indexOf(self.manual_is))

    def handle_gcode_response(self, data: list[str]) -> None:
        """
        Parses a Klipper Input Shaper console message and updates self.is_types.
        """

        if not isinstance(data, list) or len(data) != 1 or not isinstance(data[0], str):
            print(
                f"WARNING: Invalid input format. Expected a list with one string. Received: {data}"
            )
            return

        message = data[0]

        pattern_fitted = re.compile(
            r"Fitted shaper '(?P<name>\w+)' frequency = (?P<freq>[\d\.]+) Hz \(vibrations = (?P<vib>[\d\.]+)%"
        )
        match_fitted = pattern_fitted.search(message)

        if match_fitted:
            name = match_fitted.group("name")
            freq = float(match_fitted.group("freq"))
            vib = float(match_fitted.group("vib"))
            current_data = self.is_types.get(name, {})
            current_data.update(
                {
                    "frequency": freq,
                    "vibration": vib,
                    "max_accel": current_data.get("max_accel", 0.0),
                }
            )
            self.is_types[name] = current_data

            return
        pattern_accel = re.compile(
            r"To avoid too much smoothing with '(?P<name>\w+)', suggested max_accel <= (?P<accel>[\d\.]+) mm/sec\^2"
        )
        match_accel = pattern_accel.search(message)

        if match_accel:
            name = match_accel.group("name")
            accel = float(match_accel.group("accel"))

            if name in self.is_types and isinstance(self.is_types[name], dict):
                self.is_types[name]["max_accel"] = accel
            else:
                self.is_types[name] = self.is_types.get(name, {})
                self.is_types[name]["max_accel"] = accel
            return

        pattern_recommended = re.compile(
            r"Recommended shaper_type_(?P<axis>[xy]) = (?P<type>\w+), shaper_freq_(?P=axis) = (?P<freq>[\d\.]+) Hz"
        )
        match_recommended = pattern_recommended.search(message)
        if match_recommended:
            axis = match_recommended.group("axis")
            recommended_type = match_recommended.group("type")
            self.is_types["Axis"] = axis
            if self.aut:
                self.is_aut_types[axis] = recommended_type
                if len(self.is_aut_types) == 2:
                    self.run_gcode_signal.emit("SAVE_CONFIG")
                    self._is_timeout_timer.stop()
                    self.call_load_panel.emit(False, "", False)
                    self.aut = False
                    return
                return

            reordered = {}
            if recommended_type in self.is_types:
                reordered[recommended_type] = self.is_types[recommended_type]
            for key, value in self.is_types.items():
                if key not in ("suggested_type", recommended_type, "Axis"):
                    reordered[key] = value

            self.set_type_dictionary(self.is_types)
            first_key = next(iter(reordered.keys()), None)
            for key in reordered:
                if key == first_key:
                    self.add_type_entry(key, "Recommended type")
                else:
                    self.add_type_entry(key)

            self.build_model_list()
            self._is_timeout_timer.stop()
            self.call_load_panel.emit(False, "", False)
            return

    def set_type_dictionary(self, types: dict) -> None:
        """Receives the dictionary of input shaper types from the utilities tab"""
        self.type_dict = types

    def _on_is_timeout(self) -> None:
        self.call_load_panel.emit(False, "", False)

    def handle_is(self, gcode: str) -> None:
        if gcode == "SHAPER_CALIBRATE":
            self.run_gcode_signal.emit("G28\nM400")
            self.aut = True
            self.run_gcode_signal.emit(gcode)
        elif gcode == "":
            # Picking an axis needs the dialog, which logic-only mode never built.
            if self.logic:
                return
            self.dialog_page.confirm_background_color("#dfdfdf")
            self.dialog_page.cancel_background_color("#dfdfdf")
            self.dialog_page.cancel_font_color("#000000")
            self.dialog_page.confirm_font_color("#000000")
            self.dialog_page.cancel_button_text("X axis")
            self.dialog_page.confirm_button_text("Y axis")
            self.dialog_page.set_message(
                "Select the axis you want to execute the input shaper on:"
            )
            self.dialog_page.show()
            return
        else:
            self.run_gcode_signal.emit("G28\nM400")
            self.run_gcode_signal.emit(gcode)
            if not self.logic:
                self.setCurrentIndex(self.indexOf(self.manual_is))

        self._is_timeout_timer.start()
        self.call_load_panel.emit(True, "Running Input Shaper...", False)

    def reset_view_model(self) -> None:
        """Clears items from ListView
        (Resets `QAbstractListModel` by clearing entries)
        """
        if self.logic:
            return
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
        if self.logic:
            return
        self.update_buttons_list_widget.blockSignals(True)
        self.model.setData(self.model.index(0), True, EntryListModel.EnableRole)
        self.on_item_clicked(
            self.model.data(self.model.index(0), QtCore.Qt.ItemDataRole.UserRole)
        )
        self.update_buttons_list_widget.blockSignals(False)

    @QtCore.pyqtSlot(ListItem, name="on-item-clicked")
    def on_item_clicked(self, item: ListItem) -> None:
        """Setup information for the currently clicked list item on the info box.
        Keeps track of the list item
        """
        if self.logic:
            return
        self.currentItem = item
        if not item:
            return
        current_info = self.type_dict.get(item.text, {})
        if not current_info:
            return

        self.vib_label.setText(self._measurement(current_info.get("vibration"), "%"))
        self.sug_accel_label.setText(
            self._measurement(current_info.get("max_accel"), "mm/s²")
        )

        self.action_btn.show()

    @staticmethod
    def _measurement(value: object, unit: str) -> str:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return "N/A"
        return f"{value:.0f}{unit}"

    def handle_ism_confirm(self) -> None:
        """Apply the selected shaper to the axis that was calibrated, and save."""
        if self.logic:
            return
        axis = self.type_dict.get("Axis")
        if self.currentItem is None or axis not in ("x", "y"):
            return

        current_info = self.type_dict.get(self.currentItem.text, {})
        frequency = current_info.get("frequency", "N/A")
        self.run_gcode_signal.emit(
            f"SET_INPUT_SHAPER SHAPER_TYPE_{axis.upper()}={self.currentItem.text} "
            f"SHAPER_FREQ_{axis.upper()}={frequency}"
        )

        self.run_gcode_signal.emit("SAVE_CONFIG")
        self.reset_view_model()
        self.setCurrentIndex(self.indexOf(self.is_page))

    def add_type_entry(self, cli_name: str, recommended: str = "") -> None:
        """Adds a new item to the list model"""
        if self.logic:
            return
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

    def _setup_ui(self) -> None:
        """Setup UI for updatePage"""

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )

        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(720, 420))

        self.is_page = QtWidgets.QWidget()
        self.is_page.setObjectName("is_page")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.is_page)
        self.verticalLayout_13.setObjectName("verticalLayout_13")

        spacerItem14 = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout_13.addItem(spacerItem14)
        self.is_header_layout = QtWidgets.QHBoxLayout()
        self.is_header_layout.setObjectName("is_header_layout")
        spacerItem15 = QtWidgets.QSpacerItem(
            60,
            0,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.is_header_layout.addItem(spacerItem15)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.is_header_title = QtWidgets.QLabel(parent=self.is_page)
        self.is_header_title.setSizePolicy(sizePolicy)
        self.is_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        self.is_header_title.setFont(font)
        self.is_header_title.setStyleSheet("background: transparent; color: white;")
        self.is_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.is_header_layout.addWidget(self.is_header_title)

        self.is_back_btn = IconButton(parent=self.is_page)
        self.is_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.is_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.is_back_btn.setStyleSheet("")
        self.is_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.is_header_layout.addWidget(self.is_back_btn)

        self.verticalLayout_13.addLayout(self.is_header_layout)

        self.is_content_layout = QtWidgets.QHBoxLayout()
        self.is_content_layout.setObjectName("is_content_layout")
        self.verticalLayout_13.addLayout(self.is_content_layout)

        self.addWidget(self.is_page)

        self.is_header_title.setText("Input Shaper")
        self.is_back_btn.setText("Back")

        #  MANUAL INPUT SHAPPER PAGE DOWN HERE DONT TOUCH  . thx :D

        self.manual_is = QtWidgets.QWidget(self)
        self.manual_is.setSizePolicy(sizePolicy)
        self.manual_is.setMinimumSize(QtCore.QSize(710, 400))
        self.manual_is.setMaximumSize(QtCore.QSize(720, 420))

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.update_page_content_layout = QtWidgets.QVBoxLayout(self.manual_is)
        self.update_page_content_layout.setContentsMargins(15, 15, 2, 2)

        self.header_content_layout = QtWidgets.QHBoxLayout(self.manual_is)
        self.header_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.spacer_left = QtWidgets.QLabel(self.manual_is)
        self.spacer_left.setMinimumSize(QtCore.QSize(60, 60))
        self.spacer_left.setMaximumSize(QtCore.QSize(60, 60))
        self.header_content_layout.addWidget(self.spacer_left, 0)

        font = QtGui.QFont()
        font.setPointSize(24)

        self.header_title = QtWidgets.QLabel(self.manual_is)
        self.header_title.setMinimumSize(QtCore.QSize(100, 60))
        self.header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        self.header_title.setFont(font)
        self.header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header_title.setStyleSheet("color:white")
        self.header_title.setText("Input Shaper")
        self.header_content_layout.addWidget(self.header_title, 0)

        self.update_back_btn = IconButton(self.manual_is)
        self.update_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.update_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.update_back_btn.setFlat(True)
        self.update_back_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))

        self.header_content_layout.addWidget(self.update_back_btn, 0)
        self.update_page_content_layout.addLayout(self.header_content_layout, 0)

        self.main_content_layout = QtWidgets.QHBoxLayout(self.manual_is)
        self.main_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.update_buttons_frame = BlocksCustomFrame(self.manual_is)

        self.update_buttons_list_widget = QtWidgets.QListView(self.update_buttons_frame)
        self.update_buttons_list_widget.setMouseTracking(True)
        self.update_buttons_list_widget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.update_buttons_list_widget.setStyleSheet("background-color:transparent")
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

        self.update_buttons_layout = QtWidgets.QVBoxLayout(self.manual_is)
        # self.update_buttons_layout.setContentsMargins(15, 20, 20, 5)
        self.update_buttons_layout.addWidget(self.update_buttons_list_widget, 0)

        self.update_buttons_frame.setLayout(self.update_buttons_layout)

        self.main_content_layout.addWidget(self.update_buttons_frame, 0)

        self.infobox_frame = BlocksCustomFrame(self.manual_is)
        self.infobox_frame.setMaximumWidth(250)

        self.info_box_layout = QtWidgets.QVBoxLayout()
        self.info_box_layout.setContentsMargins(10, 10, 10, 10)

        font = QtGui.QFont()
        font.setPointSize(20)

        self.info_box = QtWidgets.QGridLayout(self.manual_is)
        self.info_box.setContentsMargins(0, 0, 0, 0)

        font.setPointSize(12)

        self.vib_title_label = QtWidgets.QLabel(self.manual_is)
        self.vib_title_label.setText("Vibrations: ")
        self.vib_title_label.setMinimumSize(QtCore.QSize(60, 60))
        self.vib_title_label.setMaximumSize(
            QtCore.QSize(int(self.infobox_frame.size().width() * 0.40), 9999)
        )
        self.vib_title_label.setStyleSheet("color:white")
        self.vib_title_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.vib_title_label.setFont(font)
        self.vib_title_label.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)

        self.vib_label = QtWidgets.QLabel(self.manual_is)
        self.vib_label.setMinimumSize(QtCore.QSize(100, 60))
        self.vib_label.setFont(font)
        self.vib_label.setStyleSheet("color:white")

        self.vib_label.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.vib_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.info_box.addWidget(self.vib_title_label, 0, 0)
        self.info_box.addWidget(self.vib_label, 0, 1)

        self.sug_accel_title_label = QtWidgets.QLabel(self.manual_is)
        self.sug_accel_title_label.setText("Sugested Max\nAcceleration:")
        self.sug_accel_title_label.setMinimumSize(QtCore.QSize(60, 60))
        self.sug_accel_title_label.setMaximumSize(
            QtCore.QSize(int(self.infobox_frame.size().width() * 0.40), 9999)
        )
        self.sug_accel_title_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.sug_accel_title_label.setFont(font)
        self.sug_accel_title_label.setStyleSheet("color:white")

        self.sug_accel_label = QtWidgets.QLabel(self.manual_is)
        self.sug_accel_label.setMinimumSize(QtCore.QSize(100, 60))
        self.sug_accel_label.setMaximumSize(
            QtCore.QSize(int(self.infobox_frame.size().width() * 0.60), 9999)
        )
        self.sug_accel_label.setStyleSheet("color:white")

        self.sug_accel_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sug_accel_label.setFont(font)

        self.info_box.addWidget(self.sug_accel_title_label, 1, 0)
        self.info_box.addWidget(self.sug_accel_label, 1, 1)

        self.info_box_layout.addLayout(self.info_box, 1)

        self.button_box = QtWidgets.QVBoxLayout(self.manual_is)
        self.button_box.setContentsMargins(0, 0, 0, 0)
        self.button_box.addSpacing(-1)

        self.action_btn = BlocksCustomButton(self.manual_is)
        self.action_btn.setMinimumSize(QtCore.QSize(200, 60))
        self.action_btn.setMaximumSize(QtCore.QSize(250, 60))
        self.action_btn.setFont(font)
        self.action_btn.setSizePolicy(sizePolicy)
        self.action_btn.setText("Confirm")
        self.action_btn.setPixmap(QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg"))
        self.action_btn.hide()
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

        self.addWidget(self.manual_is)
