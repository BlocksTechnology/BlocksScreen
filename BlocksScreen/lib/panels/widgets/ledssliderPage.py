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

from lib.panels.utilitiesTab import LedState


class LedsSliderPage(QtWidgets.QWidget):

    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super(LedsSliderPage, self).__init__(parent)

        self.leds_w_slider.sliderReleased.connect(self.update_led_values)
        self.request_back_button.connect(self.request_back_button.emit)


        self._setup_ui()


    def update_led_values(self) -> None:
        """Update led state and color values"""
        if not self.current_object:
            return
        self.current_object.white = int(self.leds_w_slider.value() * 255 / 100)
        self.save_led_state()


    def set_slider(self,led_state:LedState,name:str):
        self.leds_w_slider.setValue(led_state.white)
        self.leds_slider_tittle_label.setText(name)
        
        self.led_name = name
        self.current_object = led_state


    def toggle_led_state(self) -> None:
        """Toggle leds"""
        if not self.current_object:
            return
        led_state = self.current_object.state
        if led_state == "off":
            led_state = "on"
            self.toggle_led_button.state = ToggleAnimatedButton.State.ON
        else:
            led_state = "off"
            self.toggle_led_button.state = ToggleAnimatedButton.State.OFF
        self.save_led_state()

    
    def save_led_state(self):
        """Save led state"""
        if self.current_object:
                self.run_gcode_signal.emit(self.current_object.get_gcode(self.led_name))





    def _setup_ui(self) -> None:
        self.setObjectName("leds_slider_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setGeometry(QtCore.QRect(0, 0, 720, 420))
        
        self.toggle_led_button = ToggleAnimatedButton(parent=self)
        self.toggle_led_button.setGeometry(QtCore.QRect(70, 120, 100, 50))
        self.toggle_led_button.setMinimumSize(QtCore.QSize(100, 50))
        self.toggle_led_button.setMaximumSize(QtCore.QSize(100, 16777215))
        self.toggle_led_button.setObjectName("toggle_led_button")

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(11)

        self.label_4 = QtWidgets.QLabel(parent=self)
        self.label_4.setGeometry(QtCore.QRect(170, 150, 31, 16))
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(parent=self)
        self.label_5.setGeometry(QtCore.QRect(40, 150, 31, 16))
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color:white")
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")

        self.layoutWidget = QtWidgets.QWidget(parent=self)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 691, 81))
        self.layoutWidget.setObjectName("layoutWidget")

        self.leds_slider_header_layout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.leds_slider_header_layout.setContentsMargins(0, 0, 0, 0)
        self.leds_slider_header_layout.setObjectName("leds_slider_header_layout")
        spacerItem19 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.leds_slider_header_layout.addItem(spacerItem19)
        
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.leds_slider_tittle_label = QtWidgets.QLabel(parent=self.layoutWidget)
        self.leds_slider_tittle_label.setSizePolicy(sizePolicy)
        self.leds_slider_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.leds_slider_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        self.leds_slider_tittle_label.setFont(font)
        self.leds_slider_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.leds_slider_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.leds_slider_tittle_label.setObjectName("leds_slider_tittle_label")
        self.leds_slider_header_layout.addWidget(self.leds_slider_tittle_label)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(20)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leds_slider_back_btn.sizePolicy().hasHeightForWidth())

        self.leds_slider_back_btn = IconButton(parent=self.layoutWidget)
        self.leds_slider_back_btn.setSizePolicy(sizePolicy)
        self.leds_slider_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.leds_slider_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.leds_slider_back_btn.setFont(font)
        self.leds_slider_back_btn.setProperty("icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.leds_slider_back_btn.setObjectName("leds_slider_back_btn") 
        self.leds_slider_header_layout.addWidget(self.leds_slider_back_btn)

        self.layoutWidget1 = QtWidgets.QWidget(parent=self)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 200, 688, 101))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.leds_w_slider = BlocksSlider(parent=self.layoutWidget1)
        self.leds_w_slider.setSizePolicy(sizePolicy)
        self.leds_w_slider.setMinimumSize(QtCore.QSize(600, 90))
        self.leds_w_slider.setMaximumSize(QtCore.QSize(600, 90))
        self.leds_w_slider.setMaximum(100)
        self.leds_w_slider.setProperty("value", 100)
        self.leds_w_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.leds_w_slider.setObjectName("leds_w_slider")
        self.verticalLayout.addWidget(self.leds_w_slider, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)

        widget.setLayout(self.verticalLayout)

        self.retranslateUi()




    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

