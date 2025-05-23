import typing

from PyQt6 import QtCore, QtGui, QtWidgets
from utils.blocks_slider import BlocksSlider
from utils.icon_button import IconButton


class SliderPage(QtWidgets.QWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    run_gcode: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.name: str = ""
        self.gcode_command: str = ""
        self.accept_gcode_command: str = ""

        self.increase_button_icon = QtGui.QPixmap(
            ":/arrow_icons/media/btn_icons/right_arrow.svg"
        )
        self.decrease_button_icon = QtGui.QPixmap(
            ":/arrow_icons/media/btn_icons/left_arrow.svg"
        )
        self.background = QtGui.QPixmap(
            ":/ui/background/media/1st_background.png"
        )
        self.setStyleSheet(
            "#SliderPage{background-image: url(:/background/media/1st_background.png);}\n"
        )
        self.setObjectName("SliderPage")
        self.setupUI()
        self.back_button.clicked.connect(self.request_back.emit)
        self.slider.sliderReleased.connect(self.on_slider_value_change)
        self.increase_button.pressed.connect(
            lambda: (
                self.slider.setSliderPosition(self.slider.sliderPosition() + 5)
                and self.on_slider_value_change()
            )
        )
        self.decrease_button.pressed.connect(
            lambda: (
                self.slider.setSliderPosition(self.slider.sliderPosition() - 5)
                and self.on_slider_value_change()
            )
        )

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

    def set_name(self, name: str) -> None:
        """Sets the header name for the page"""
        self.name = name
        self.update()

    def send_gcode_command(self) -> None:
        """Sends a gcode command to the printer"""
        if self.gcode_command:
            self.run_gcode.emit(f"{self.gcode_command}")

    def set_slider_pos(self, value) -> None:
        """Set slider position from value, updates the widget"""
        if not isinstance(value, int | float):
            return

        self.slider.setSliderPosition(int(round(value)))
        self.update()
        self.repaint()

    @QtCore.pyqtSlot(name="sliderReleased")
    def on_slider_value_change(self) -> None:
        """Handles slider position changes"""
        print("Slider released can send gcode")
        ...
        # self.current_value_label.setText(f"{self.slider.sliderPosition()}%")

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Custom painting for the widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)
        painter.setRenderHint(painter.RenderHint.TextAntialiasing)
        painter.drawPixmap(self.rect(), self.background, self.rect())
        self.current_value_label.setText(f"{self.slider.sliderPosition()}%")
        self.object_name_label.setText(f"{self.name}")

        if "speed" in self.name.lower():
            if (
                self.slider.maximum() <= 500
                and self.slider.sliderPosition() + 10 >= self.slider.maximum()
            ):
                self.slider.setMaximum(int(int(self.slider.maximum()) + 100))
            elif self.slider.maximum() <= 100:
                self.slider.setMaximum(100)

        painter.end()

    def setupUI(self) -> None:
        """Setup the components for the widget"""
        self.setMinimumSize(QtCore.QSize(700, 410))
        self.setMaximumSize(QtCore.QSize(720, 420))

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setContentsMargins(10, 10, 10, 10)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setWindowOpacity(1.0)
        self.setAutoFillBackground(False)
        self.setBackgroundRole(QtGui.QPalette.ColorRole.Window)

        self.main_verticalLayout_1 = QtWidgets.QVBoxLayout(self)
        self.main_verticalLayout_1.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.main_verticalLayout_1.setContentsMargins(10, 10, 10, 10)
        self.main_verticalLayout_1.setSpacing(6)
        self.main_verticalLayout_1.setObjectName("main_verticalLayout_1")

        self.header_horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.header_horizontalLayoutWidget.setMinimumHeight(80)
        self.header_horizontalLayoutWidget.setMaximumHeight(80)
        self.header_horizontalLayout = QtWidgets.QHBoxLayout(
            self.header_horizontalLayoutWidget
        )

        palette = QtGui.QPalette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText,
            QtGui.QColor(QtCore.Qt.GlobalColor.white),
        )
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(22)
        self.object_name_label = QtWidgets.QLabel(
            self.header_horizontalLayoutWidget
        )
        self.object_name_label.setFont(font)
        self.object_name_label.setPalette(palette)
        self.object_name_label.setMinimumSize(QtCore.QSize(self.width(), 80))
        self.object_name_label.setMaximumSize(QtCore.QSize(self.width(), 80))
        self.object_name_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        self.back_button = IconButton(self.header_horizontalLayoutWidget)
        self.back_button.setIconPixmap(
            QtGui.QPixmap(":ui/media/btn_icons/back.svg")
        )
        self.back_button.has_text = False
        self.back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.back_button.setMaximumSize(QtCore.QSize(60, 60))

        # self.main_verticalLayout_1.addWidget(
        self.header_horizontalLayout.addWidget(
            # self.object_name_label,
            self.object_name_label,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.header_horizontalLayout.addWidget(
            self.back_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.main_verticalLayout_1.addWidget(
            self.header_horizontalLayoutWidget,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.current_value_label = QtWidgets.QLabel(self)
        self.current_value_label.setFont(font)
        self.current_value_label.setPalette(palette)
        self.current_value_label.setMinimumSize(QtCore.QSize(self.width(), 80))
        self.current_value_label.setMaximumSize(
            QtCore.QSize(self.width(), 200)
        )
        self.current_value_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        self.main_verticalLayout_1.addWidget(
            # self.header_horizontalLayout.addWidget(
            self.current_value_label,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        # self.main_verticalLayout_1.addWidget(
        #     self.header_horizontalLayoutWidget,
        #     0,
        #     QtCore.Qt.AlignmentFlag.AlignHCenter
        #     | QtCore.Qt.AlignmentFlag.AlignVCenter,
        # )
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()

        self.decrease_button = IconButton(self)
        self.decrease_button.setMinimumSize(QtCore.QSize(80, 80))
        self.decrease_button.setMaximumSize(QtCore.QSize(80, 80))
        self.decrease_button.setProperty(
            name="icon_pixmap", value=self.decrease_button_icon
        )
        self.horizontalLayout_1.addWidget(
            self.decrease_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignVCenter
            | QtCore.Qt.AlignmentFlag.AlignHCenter,
        )
        self.slider = BlocksSlider(self)
        self.slider.setMinimumSize(QtCore.QSize(self.width() - 100 * 2, 100))
        self.horizontalLayout_1.addWidget(
            self.slider,
            0,
            QtCore.Qt.AlignmentFlag.AlignVCenter
            | QtCore.Qt.AlignmentFlag.AlignHCenter,
        )
        self.increase_button = IconButton(self)
        self.increase_button.setProperty(
            name="icon_pixmap", value=self.increase_button_icon
        )
        self.increase_button.setMinimumSize(QtCore.QSize(80, 80))
        self.increase_button.setMaximumSize(QtCore.QSize(80, 80))

        self.horizontalLayout_1.addWidget(
            self.increase_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignVCenter
            | QtCore.Qt.AlignmentFlag.AlignHCenter,
        )
        self.main_verticalLayout_1.addLayout(self.horizontalLayout_1)
