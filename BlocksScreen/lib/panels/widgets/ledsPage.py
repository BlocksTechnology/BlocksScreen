import typing
import re
from lib.utils.icon_button import IconButton
from helper_methods import normalize

from PyQt6 import QtCore, QtGui, QtWidgets

from lib.panels.widgets.optionCardWidget import OptionCard


from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_slider import BlocksSlider
from lib.utils.check_button import BlocksCustomCheckButton
from lib.utils.icon_button import IconButton
from lib.utils.toggleAnimatedButton import ToggleAnimatedButton

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
    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:a
        super(LedsPage, self).__init__(parent)

        self.leds = {}

        self._setup_ui()

    @QtCore.pyqtSlot(list, name="on_object_list")
    def on_object_list(self, object_list: list) -> None:
        """Handle receiving printer object list"""
        self._update_leds_from_config(object_list)



    def _update_leds_from_config(self,config:list):
        layout = self.leds_content_layout

        while layout.count():
            if (child := layout.takeAt(0)) and child.widget():
                child.widget().deleteLater()  # type: ignore

        led_names = []
        if not config:
            return

        # Collect LED names
        for obj in config:
            if "led" in obj:
                try:
                    name = obj.split()[1]
                    led_names.append(name)
                    self.leds[name] = LedState(led_type="white")
                except IndexError:
                    pass

        max_columns = 3
        buttons = []  # store references to created buttons

        # Create LED buttons
        for i, name in enumerate(led_names):
            if self.leds_widget:
                button = BlocksCustomButton()
                button.setFixedSize(200, 70)
                button.setText(name)
                button.setProperty("class", "menu_btn")
                button.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/LEDs.svg"))
                row, col = divmod(i, max_columns)
                layout.addWidget(button, row, col)
                button.clicked.connect(lambda:self.handle_led_button(name))
                buttons.append(button)

        if len(buttons) == 1:
            ...
            # self.panel.utilities_leds_btn.clicked.connect(
            #     partial(self.handle_led_button, led_names[0])
            # )
        else:
            ...
            # self._connect_page_change(
            #     self.panel.utilities_leds_btn, self.panel.leds_page
            # )

    def handle_led_button(self, name: str) -> None:
        """Handle led button clicked"""
        self.current_object = name
        led_state: LedState = self.leds.get(name)
        if not led_state:
            return
        #TODO: finish setting up buttons


        # self.change_page(self.indexOf(self.panel.leds_slider_page))

    def _setup_ui(self) -> None:

        self.setObjectName("fans_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setGeometry(QtCore.QRect(0, 0, 720, 420))

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(20, 24, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        self.leds_header_layout = QtWidgets.QHBoxLayout()
        self.leds_header_layout.setObjectName("leds_header_layout")
        spacerItem3 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.leds_header_layout.addItem(spacerItem3)
        self.leds_title_label = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leds_title_label.sizePolicy().hasHeightForWidth())
        self.leds_title_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.leds_title_label.setFont(font)
        self.leds_title_label.setStyleSheet("background: transparent; color: white;")
        self.leds_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.leds_title_label.setObjectName("leds_title_label")
        self.leds_header_layout.addWidget(self.leds_title_label)
        self.leds_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leds_back_btn.sizePolicy().hasHeightForWidth())
        self.leds_back_btn.setSizePolicy(sizePolicy)
        self.leds_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.leds_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(20)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.leds_back_btn.setFont(font)
        self.leds_back_btn.setMouseTracking(False)
        self.leds_back_btn.setTabletTracking(True)
        self.leds_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.leds_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.leds_back_btn.setStyleSheet("")
        self.leds_back_btn.setAutoDefault(False)
        self.leds_back_btn.setFlat(True)
        self.leds_back_btn.setProperty("icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.leds_back_btn.setObjectName("leds_back_btn")
        self.leds_header_layout.addWidget(self.leds_back_btn)
        self.verticalLayout.addLayout(self.leds_header_layout)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.verticalScrollBar = QtWidgets.QScrollBar(parent=self)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.verticalLayout.addWidget(self.verticalScrollBar)
        self.leds_content_layout = QtWidgets.QGridLayout()
        self.leds_content_layout.setObjectName("leds_content_layout")
        self.leds_widget = QtWidgets.QWidget(parent=self)
        self.leds_widget.setObjectName("leds_widget")
        self.leds_content_layout.addWidget(self.leds_widget, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.leds_content_layout)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem5)

        widget.setLayout(self.verticalLayout)
        self.retranslateUi()
        ...


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

