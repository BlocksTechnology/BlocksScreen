import typing

from lib.utils.blocks_slider import BlocksSlider
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class SliderPage(QtWidgets.QWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    run_gcode: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )
    value_selected: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, int, name="value_selected"
    )
    min_value = 0
    max_value = 100

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.name: str = ""
        self.increase_button_icon = QtGui.QPixmap(
            ":/arrow_icons/media/btn_icons/right_arrow.svg"
        )
        self.decrease_button_icon = QtGui.QPixmap(
            ":/arrow_icons/media/btn_icons/left_arrow.svg"
        )
        self.background = QtGui.QPixmap(":/ui/background/media/1st_background.png")
        self.setStyleSheet(
            "#SliderPage{background-image: url(:/background/media/1st_background.png);}\n"
        )
        self.setObjectName("SliderPage")
        self._setupUI()
        self.back_button.clicked.connect(self.request_back.emit)
        self.back_button.clicked.connect(self.value_selected.disconnect)
        self.slider.valueChanged.connect(self.on_slider_value_change)
        self.increase_button.pressed.connect(
            lambda: (self.slider.setSliderPosition(self.slider.sliderPosition() + 5))
        )
        self.decrease_button.pressed.connect(
            lambda: (self.slider.setSliderPosition(self.slider.sliderPosition() - 5))
        )
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

    @QtCore.pyqtSlot(int, name="valueChanged")
    def on_slider_value_change(self, value) -> None:
        """Handles slider position changes"""
        self.value_selected.emit(self.name, value)

    def set_name(self, name: str) -> None:
        """Sets the header name for the page"""
        self.name = name

    def set_slider_position(self, value: int) -> None:
        """Set slider position from value, updates the widget"""
        self.slider.setSliderPosition(int(value))

    def set_slider_minimum(self, value: int) -> None:
        """Set slider minimum value"""
        self.slider.setMinimum(value)

    def set_slider_maximum(self, value: int) -> None:
        """Set slider maximum value"""
        self.slider.setMaximum(value)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Custom painting for the widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)
        painter.setRenderHint(painter.RenderHint.TextAntialiasing)
        painter.drawPixmap(self.rect(), self.background, self.rect())
        self.current_value_label.setText(str(self.slider.value()) + " " + "%")
        self.object_name_label.setText(str(self.name))
        painter.end()

    def _setupUI(self) -> None:
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

        self.main_verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.main_verticalLayout_1.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.main_verticalLayout_1.setContentsMargins(10, 10, 10, 10)
        self.main_verticalLayout_1.setSpacing(6)
        self.main_verticalLayout_1.setObjectName("main_verticalLayout_1")

        self.header_horizontalLayout = QtWidgets.QHBoxLayout()

        palette = QtGui.QPalette()
        palette.setColor(
            QtGui.QPalette.ColorRole.WindowText,
            QtGui.QColor(QtCore.Qt.GlobalColor.white),
        )
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(22)
        self.object_name_label = QtWidgets.QLabel(self)
        self.object_name_label.setFont(font)
        self.object_name_label.setPalette(palette)
        self.object_name_label.setMinimumSize(QtCore.QSize(self.width(), 60))
        self.object_name_label.setMaximumSize(QtCore.QSize(self.width() - 60, 60))
        self.object_name_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        self.back_button = IconButton(self)
        self.back_button.setPixmap(QtGui.QPixmap(":ui/media/btn_icons/back.svg"))
        self.back_button.has_text = False
        self.back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.header_horizontalLayout.addWidget(
            self.object_name_label,
            0,
        )
        self.header_horizontalLayout.addWidget(
            self.back_button,
            0,
        )
        self.main_verticalLayout_1.addLayout(self.header_horizontalLayout)
        self.middle_content_layout = QtWidgets.QHBoxLayout()
        self.current_value_label = QtWidgets.QLabel(self)
        self.current_value_label.setFont(font)
        self.current_value_label.setPalette(palette)
        self.current_value_label.setMinimumSize(QtCore.QSize(self.width(), 80))
        self.current_value_label.setMaximumSize(QtCore.QSize(self.width(), 300))
        self.current_value_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.middle_content_layout.addWidget(
            self.current_value_label,
            1,
        )
        self.middle_content_layout.setStretch(0, 1)
        self.main_verticalLayout_1.addLayout(self.middle_content_layout)
        self.slider_layout = QtWidgets.QHBoxLayout()
        self.decrease_button = IconButton(self)
        self.decrease_button.setMinimumSize(QtCore.QSize(80, 80))
        self.decrease_button.setMaximumSize(QtCore.QSize(80, 80))
        self.decrease_button.setProperty(
            name="icon_pixmap", value=self.decrease_button_icon
        )
        self.slider_layout.addWidget(
            self.decrease_button,
            0,
        )
        self.slider = BlocksSlider(self)
        self.slider.setMinimumSize(QtCore.QSize(self.width() - 100 * 2, 100))
        self.slider_layout.addWidget(
            self.slider,
            0,
            QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter,
        )
        self.increase_button = IconButton(self)
        self.increase_button.setProperty(
            name="icon_pixmap", value=self.increase_button_icon
        )
        self.increase_button.setMinimumSize(QtCore.QSize(80, 80))
        self.increase_button.setMaximumSize(QtCore.QSize(80, 80))

        self.slider_layout.addWidget(
            self.increase_button,
            0,
        )
        self.main_verticalLayout_1.addLayout(self.slider_layout)
        self.setLayout(self.main_verticalLayout_1)
