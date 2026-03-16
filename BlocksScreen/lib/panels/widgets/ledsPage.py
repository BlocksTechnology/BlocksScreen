import typing
from lib.utils.icon_button import IconButton

from PyQt6 import QtCore, QtGui, QtWidgets


from lib.utils.blocks_button import BlocksCustomButton


class LedState:
    """Represents the state of an LED light."""

    led_type: str
    red: int = 0
    green: int = 0
    blue: int = 0
    white: int = 255
    state: str = "on"

    def get_gcode(self, name: str) -> str:
        """Generates the G-code command for the current state."""
        if self.state == "off":
            return f"SET_LED LED={name} RED=0 GREEN=0 BLUE=0 WHITE=0"
        if self.led_type == "white":
            return f"SET_LED LED={name} WHITE={self.white / 255:.2f}"
        # Default to RGB
        return (
            f"SET_LED LED={name} RED={self.red / 255:.2f} "
            f"GREEN={self.green / 255:.2f} BLUE={self.blue / 255:.2f} "
            f"WHITE={self.white / 255:.2f}"
        )


class LedsPage(QtWidgets.QWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    request_ledslider_page = QtCore.pyqtSignal(
        LedState, str, bool, name="request-ledslider-page"
    )

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super(LedsPage, self).__init__(parent)

        self._setup_ui()
        self.leds = {}
        self.leds_back_btn.clicked.connect(self.request_back)

    def showEvent(self, a0: QtGui.QShowEvent | None) -> None:
        if self.singleLed:
            self.handle_led_button(self.singleLed)
        return super().showEvent(a0)

    @QtCore.pyqtSlot(list, name="on_object_list")
    def on_object_list(self, object_list: list) -> None:
        """Handle receiving printer object list"""

        layout = self.leds_content_layout

        while layout.count():
            if (child := layout.takeAt(0)) and child.widget():
                child.widget().deleteLater()  # type: ignore

        led_names = []
        if not object_list:
            return

        # Collect LED names
        for obj in object_list:
            if "led" in obj:
                try:
                    name = obj.split()[1]
                    led_names.append(name)
                    self.leds[name] = LedState()
                    self.leds[name].led_type = "white"
                except IndexError:
                    pass

        max_columns = 3
        buttons = []

        # Create LED buttons
        for i, name in enumerate(led_names):
            if self.leds_widget:
                button = BlocksCustomButton()
                button.setFixedSize(200, 70)
                button.setText(name)
                button.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/LEDs.svg"))
                row, col = divmod(i, max_columns)
                layout.addWidget(button, row, col)
                button.clicked.connect(lambda: self.handle_led_button(name))
                buttons.append(button)

        if len(buttons) == 1:
            self.singleLed = name
        else:
            self.singleLed = None

    def handle_led_button(self, name: str) -> None:
        """Handle led button clicked"""
        self.current_object = name
        led_state: LedState = self.leds.get(name)
        if not led_state:
            return

        self.request_ledslider_page.emit(
            led_state, name, True if self.singleLed else False
        )

    def _setup_ui(self) -> None:

        self.setObjectName("fans_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setGeometry(QtCore.QRect(0, 0, 720, 420))

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout.addItem(spacerItem2)
        self.leds_header_layout = QtWidgets.QHBoxLayout()
        self.leds_header_layout.setObjectName("leds_header_layout")
        spacerItem3 = QtWidgets.QSpacerItem(
            60,
            20,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_header_layout.addItem(spacerItem3)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        self.leds_title_label = QtWidgets.QLabel(parent=self)
        self.leds_title_label.setSizePolicy(sizePolicy)
        self.leds_title_label.setFont(font)
        self.leds_title_label.setStyleSheet("background: transparent; color: white;")
        self.leds_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.leds_title_label.setObjectName("leds_title_label")
        self.leds_header_layout.addWidget(self.leds_title_label)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.leds_back_btn = IconButton(parent=self)
        self.leds_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.leds_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.leds_back_btn.setFont(font)
        self.leds_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.leds_back_btn.setObjectName("leds_back_btn")

        self.leds_header_layout.addWidget(self.leds_back_btn)

        self.verticalLayout.addLayout(self.leds_header_layout)
        spacerItem4 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.verticalLayout.addItem(spacerItem4)
        self.leds_content_layout = QtWidgets.QGridLayout()
        self.leds_content_layout.setObjectName("leds_content_layout")

        self.leds_widget = QtWidgets.QWidget(parent=self)
        self.leds_widget.setObjectName("leds_widget")
        self.leds_content_layout.addWidget(self.leds_widget, 0, 0, 1, 1)

        self.verticalLayout.addLayout(self.leds_content_layout)
        self.verticalLayout.addItem(spacerItem4)

        widget.setLayout(self.verticalLayout)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.leds_title_label.setText(_translate("utilitiesStackedWidget", "LED's"))
        self.leds_back_btn.setText(_translate("utilitiesStackedWidget", "Back"))
