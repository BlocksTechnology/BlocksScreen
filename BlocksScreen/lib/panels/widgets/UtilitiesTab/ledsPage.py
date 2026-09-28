import typing
from dataclasses import dataclass
from functools import partial

from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_slider import BlocksSlider
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


@dataclass
class LedState:
    """Represents the state of an LED light."""

    led_type: str
    red: int = 0
    green: int = 0
    blue: int = 0
    white: int = 255
    state: bool = True

    def get_gcode(self, name: str) -> str:
        """Generates the G-code command for the current state."""
        if not self.state:
            return f"SET_LED LED={name} RED=0 GREEN=0 BLUE=0 WHITE=0"
        if self.led_type == "white":
            return f"SET_LED LED={name} WHITE={self.white / 255:.2f}"
        return (
            f"SET_LED LED={name} RED={self.red / 255:.2f} "
            f"GREEN={self.green / 255:.2f} BLUE={self.blue / 255:.2f} "
            f"WHITE={self.white / 255:.2f}"
        )


class LedsPage(QtWidgets.QStackedWidget):
    """Leds page of the utilities tab."""

    _LED_TYPES: frozenset[str] = frozenset({"led", "neopixel", "dotstar"})

    request_back_button = QtCore.pyqtSignal(name="request-back-button")
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super().__init__(parent)

        self.singleled: bool = False
        self.leds: dict[str, LedState] = {}
        self.current_led: str | None = None

        self._led_pixmap = QtGui.QPixmap(":/ui/media/btn_icons/LEDs.svg")

        self._setup_ui()
        self.leds_back_btn.clicked.connect(self.request_back_button.emit)

        self.leds_w_slider.sliderReleased.connect(self.update_led_values)
        self.leds_slider_back_btn.clicked.connect(self._slider_back)
        self.leds_on_btn.clicked.connect(partial(self.set_led_state, True))
        self.leds_off_btn.clicked.connect(partial(self.set_led_state, False))

    def showEvent(self, a0: QtGui.QShowEvent | None) -> None:
        if self.singleled and self.leds:
            self.handle_led_button(next(iter(self.leds)))
        else:
            self.setCurrentIndex(self.indexOf(self.main_page))

        return super().showEvent(a0)

    def _slider_back(self) -> None:
        if self.singleled:
            self.request_back_button.emit()
        else:
            self.setCurrentIndex(self.indexOf(self.main_page))

    def update_led_values(self) -> None:
        """Update led state and color values"""
        led_state: LedState = self.leds[str(self.current_led)]
        led_state.white = int(self.leds_w_slider.value() * 255 / 100)
        self.save_led_state()

    def on_object_list(self, config_file) -> bool:
        layout = self.leds_content_layout
        cg = config_file

        while layout.count():
            if (child := layout.takeAt(0)) and child.widget():
                child.widget().deleteLater()  # type: ignore

        led_names = []
        self.leds.clear()

        for obj in cg:
            parts = obj.split()
            if len(parts) >= 2 and parts[0] in self._LED_TYPES:
                name = parts[1]
                led_names.append(name)
                self.leds[name] = LedState(led_type="white")

        max_columns = 3
        self.singleled = len(led_names) == 1

        for i, name in enumerate(led_names):
            button = BlocksCustomButton()
            button.setFixedSize(250, 80)
            button.setText(name)
            button.setProperty("class", "menu_btn")
            button.setPixmap(self._led_pixmap)
            row, col = divmod(i, max_columns)
            layout.addWidget(button, row, col, QtCore.Qt.AlignmentFlag.AlignCenter)
            button.clicked.connect(partial(self.handle_led_button, name))

        return True

    def handle_led_button(self, name: str):
        self.current_led = name
        led_state = self.leds.get(name)
        if not led_state:
            return
        is_rgb = led_state.led_type == "rgb"
        self.leds_w_slider.setVisible(not is_rgb)
        self.leds_w_slider.setValue(round(led_state.white * 100 / 255))
        self._sync_state_buttons(led_state.state)
        self.leds_slider_tittle_label.setText(name.replace("_", " "))
        self.setCurrentIndex(self.indexOf(self.leds_slider_page))

    def set_led_state(self, state: bool) -> None:
        """Turn the current led on or off"""
        led_state = self.leds.get(str(self.current_led))
        if not led_state or led_state.state == state:
            return
        led_state.state = state
        self._sync_state_buttons(state)
        self.save_led_state()

    def _sync_state_buttons(self, state: bool) -> None:
        # Whichever button matches the state the led is already in has nothing
        # left to do, so it is the one that greys out.
        self.leds_on_btn.setEnabled(not state)
        self.leds_off_btn.setEnabled(state)

    def save_led_state(self):
        """Save led state"""
        if self.current_led and self.current_led in self.leds:
            led_state: LedState = self.leds[self.current_led]
            self.run_gcode_signal.emit(led_state.get_gcode(self.current_led))

    def _setup_ui(self) -> None:
        self.setObjectName("leds_page")

        self.main_page = QtWidgets.QWidget()
        self.main_page.setObjectName("leds_main_page")
        spacerItem3 = QtWidgets.QSpacerItem(
            60,
            20,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        spacerItem2 = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )

        spacerItem4 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        spacerItem5 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.main_page)
        self.verticalLayout_4.addItem(spacerItem2)

        self.leds_header_layout = QtWidgets.QHBoxLayout()
        self.leds_header_layout.setContentsMargins(0, 0, 0, 0)
        self.leds_header_layout.setObjectName("leds_header_layout")
        self.leds_header_layout.addItem(spacerItem3)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        self.leds_title_label = QtWidgets.QLabel(parent=self.main_page)
        self.leds_title_label.setSizePolicy(sizePolicy)
        self.leds_title_label.setFont(font)
        self.leds_title_label.setStyleSheet("background: transparent; color: white;")
        self.leds_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.leds_title_label.setFixedHeight(60)
        self.leds_header_layout.addWidget(self.leds_title_label)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )

        self.leds_back_btn = IconButton(parent=self.main_page)
        self.leds_back_btn.setSizePolicy(sizePolicy)
        self.leds_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.leds_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.leds_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.leds_header_layout.addWidget(self.leds_back_btn)

        self.verticalLayout_4.addLayout(self.leds_header_layout)
        self.verticalLayout_4.addItem(spacerItem4)

        self.leds_content_layout = QtWidgets.QGridLayout()
        self.leds_content_layout.setObjectName("leds_content_layout")

        self.verticalLayout_4.addLayout(self.leds_content_layout)
        self.verticalLayout_4.addItem(spacerItem5)

        self.addWidget(self.main_page)

        # --- LED slider page -------------------------------------------------

        self.leds_slider_page = QtWidgets.QWidget()
        self.leds_slider_page.setObjectName("leds_slider_page")

        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.leds_slider_page)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(10, 30, 9, 9)
        self.verticalLayout_12.setSpacing(0)

        self.leds_slider_header_layout = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout.setObjectName("leds_slider_header_layout")
        self.leds_slider_header_layout.setContentsMargins(0, 10, 0, 11)
        self.leds_slider_header_layout.setSpacing(6)
        self.leds_slider_header_layout.addItem(
            QtWidgets.QSpacerItem(
                60,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        self.leds_slider_tittle_label = QtWidgets.QLabel(parent=self.leds_slider_page)
        self.leds_slider_tittle_label.setSizePolicy(sizePolicy)
        self.leds_slider_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.leds_slider_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        self.leds_slider_tittle_label.setFont(font)
        self.leds_slider_tittle_label.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.leds_slider_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.leds_slider_tittle_label.setObjectName("leds_slider_tittle_label")
        self.leds_slider_header_layout.addWidget(self.leds_slider_tittle_label)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )

        self.leds_slider_back_btn = IconButton(parent=self.leds_slider_page)
        self.leds_slider_back_btn.setSizePolicy(sizePolicy)
        self.leds_slider_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.leds_slider_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.leds_slider_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.leds_slider_back_btn.setObjectName("leds_slider_back_btn")
        self.leds_slider_header_layout.addWidget(self.leds_slider_back_btn)

        self.verticalLayout_12.addLayout(self.leds_slider_header_layout)

        self.verticalLayout_12.addSpacing(50)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )

        self.leds_slider_content_layout = QtWidgets.QVBoxLayout()
        self.leds_slider_content_layout.setObjectName("leds_slider_content_layout")
        self.leds_slider_content_layout.setContentsMargins(0, 5, 0, 30)

        self.leds_w_slider = BlocksSlider(parent=self.leds_slider_page)
        self.leds_w_slider.setSizePolicy(sizePolicy)
        self.leds_w_slider.setMinimumSize(QtCore.QSize(600, 90))
        self.leds_w_slider.setMaximumSize(QtCore.QSize(600, 90))
        self.leds_w_slider.setMaximum(100)
        self.leds_w_slider.setProperty("value", 100)
        self.leds_w_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.leds_slider_content_layout.addWidget(
            self.leds_w_slider, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.verticalLayout_12.addLayout(self.leds_slider_content_layout)
        self.verticalLayout_12.addSpacing(20)

        # The on/off pair that replaced the toggle. Only one of them is ever
        # enabled -- see _sync_state_buttons.
        self.leds_buttons_layout = QtWidgets.QHBoxLayout()
        self.leds_buttons_layout.setObjectName("leds_buttons_layout")
        self.leds_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.leds_buttons_layout.setSpacing(50)
        self.leds_buttons_layout.addStretch(1)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)

        self.leds_on_btn = BlocksCustomButton(parent=self.leds_slider_page)
        self.leds_on_btn.setFixedSize(QtCore.QSize(250, 80))
        self.leds_on_btn.setFont(font)
        self.leds_on_btn.setProperty("class", "menu_btn")
        self.leds_on_btn.setPixmap(self._led_pixmap)
        self.leds_on_btn.setObjectName("leds_on_btn")
        self.leds_on_btn.setText("ON")
        self.leds_buttons_layout.addWidget(self.leds_on_btn)

        self.leds_off_btn = BlocksCustomButton(parent=self.leds_slider_page)
        self.leds_off_btn.setFixedSize(QtCore.QSize(250, 80))
        self.leds_off_btn.setFont(font)
        self.leds_off_btn.setProperty("class", "menu_btn")
        self.leds_off_btn.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/LEDs_off.svg"))
        self.leds_off_btn.setObjectName("leds_off_btn")
        self.leds_off_btn.setText("OFF")
        self.leds_buttons_layout.addWidget(self.leds_off_btn)

        self.leds_buttons_layout.addStretch(1)

        # LedState defaults to on, and so does the pair until a led is opened.
        self._sync_state_buttons(True)

        self.verticalLayout_12.addLayout(self.leds_buttons_layout)
        self.verticalLayout_12.addStretch(1)

        self.addWidget(self.leds_slider_page)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        _translate = QtCore.QCoreApplication.translate

        self.leds_title_label.setText(_translate("self", "LED's"))
        self.leds_back_btn.setText(_translate("self", "Back"))
        self.leds_slider_back_btn.setText(_translate("self", "Back"))
        self.leds_slider_tittle_label.setText(_translate("self", "LED's"))
