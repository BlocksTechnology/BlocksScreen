import typing

from lib.utils.icon_button import IconButton
from lib.utils.display_button import DisplayButton
from lib.utils.blocks_button import BlocksCustomButton

from PyQt6 import QtCore, QtGui, QtWidgets


class TemperaturePage(QtWidgets.QWidget):
    request_back = QtCore.pyqtSignal(name="request-back-button")

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    request_numpad: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str,
        int,
        "PyQt_PyObject",
        int,
        int,
        name="request-numpad",
    )

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super(TemperaturePage, self).__init__(parent)

        self._setup_ui()

        self.temp_back_button.clicked.connect(self.request_back.emit)

        self.cooldown_btn.hide()
        self.temperature_cooldown_btn.hide()

        self.extruder_temp_display.clicked.connect(
            lambda: self.request_numpad.emit(
                "Extruder Temperature",
                int(round(float(self.extruder_temp_display.secondary_text))),
                self.on_numpad_change,
                0,
                300,  # TODO: Get this value from printer objects
            )
        )
        self.bed_temp_display.clicked.connect(
            lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
                "Bed Temperature",
                int(round(float(self.bed_temp_display.secondary_text))),
                self.on_numpad_change,
                0,
                120,  # TODO: Get this value from printer objects
            )
        )

    @QtCore.pyqtSlot(str, int, name="on-numpad-change")
    def on_numpad_change(self, name: str, new_value: int) -> None:
        """Handles inputted numpad values"""
        if "bed" in name.lower():
            name = "heater_bed"
        elif "extruder" in name.lower():
            name = "extruder"
        self.run_gcode_signal.emit(
            f"SET_HEATER_TEMPERATURE HEATER={name} TARGET={new_value}"
        )

    @QtCore.pyqtSlot(str, str, float, name="on-extruder-update")
    def on_extruder_update(
        self, extruder_name: str, field: str, new_value: float
    ) -> None:
        """Handles updates from extruder printer object"""
        if extruder_name == "extruder" and field == "temperature":
            self.extruder_temp_display.setText(f"{new_value:.1f}")
        if extruder_name == "extruder" and field == "target":
            self.extruder_temp_display.secondary_text = f"{new_value:.1f}"

    @QtCore.pyqtSlot(str, str, float, name="on-heater-bed-update")
    def on_heater_bed_update(self, name: str, field: str, new_value: float) -> None:
        """Handles updated from heater_bed printer object"""
        if field == "temperature":
            self.bed_temp_display.setText(f"{new_value:.1f}")
        if field == "target":
            self.bed_temp_display.secondary_text = f"{new_value:.1f}"

    def _setup_ui(self) -> None:
        self.setObjectName("fans_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setGeometry(QtCore.QRect(0, 0, 720, 420))
        self.setObjectName("temperature_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout.addItem(spacerItem3)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem4 = QtWidgets.QSpacerItem(
            60,
            20,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem4)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)

        self.temp_header_title = QtWidgets.QLabel(parent=self)
        self.temp_header_title.setSizePolicy(sizePolicy)
        self.temp_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        self.temp_header_title.setFont(font)
        self.temp_header_title.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.temp_header_title.setStyleSheet("background: transparent; color: white;")
        self.temp_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.temp_header_title.setObjectName("temp_header_title")
        self.horizontalLayout.addWidget(self.temp_header_title)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.temp_back_button = IconButton(parent=self)
        self.temp_back_button.setSizePolicy(sizePolicy)
        self.temp_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.temp_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.temp_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.temp_back_button.setObjectName("temp_back_button")

        self.horizontalLayout.addWidget(self.temp_back_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        spacerItem5 = QtWidgets.QSpacerItem(
            20,
            35,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout.addItem(spacerItem5)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")

        self.tp_content_horizontal_layout = QtWidgets.QHBoxLayout()
        self.tp_content_horizontal_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMinimumSize
        )
        self.tp_content_horizontal_layout.setContentsMargins(5, 5, 5, 5)
        self.tp_content_horizontal_layout.setSpacing(5)
        self.tp_content_horizontal_layout.setObjectName("tp_content_horizontal_layout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)

        font = QtGui.QFont()
        font.setPointSize(11)

        self.extruder_temp_display = DisplayButton(parent=self)
        self.extruder_temp_display.setSizePolicy(sizePolicy)
        self.extruder_temp_display.setMinimumSize(QtCore.QSize(200, 60))
        self.extruder_temp_display.setMaximumSize(QtCore.QSize(120, 60))
        self.extruder_temp_display.setFont(font)
        self.extruder_temp_display.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/extruder_related/media/btn_icons/nozzle.svg"),
        )
        self.extruder_temp_display.setObjectName("extruder_temp_display")
        self.tp_content_horizontal_layout.addWidget(self.extruder_temp_display)

        self.bed_temp_display = DisplayButton(parent=self)
        self.bed_temp_display.setSizePolicy(sizePolicy)
        self.bed_temp_display.setMinimumSize(QtCore.QSize(200, 60))
        self.bed_temp_display.setMaximumSize(QtCore.QSize(120, 60))
        self.bed_temp_display.setFont(font)
        self.bed_temp_display.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(
                ":/temperature_related/media/btn_icons/temperature_plate.svg"
            ),
        )
        self.bed_temp_display.setObjectName("bed_temp_display")

        self.tp_content_horizontal_layout.addWidget(self.bed_temp_display)
        self.gridLayout.addLayout(self.tp_content_horizontal_layout, 0, 0, 1, 2)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.cooldown_btn = BlocksCustomButton(parent=self)
        self.cooldown_btn.setSizePolicy(sizePolicy)
        self.cooldown_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.cooldown_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.cooldown_btn.setFont(font)
        self.cooldown_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.cooldown_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/temperature_related/media/btn_icons/cooldown.svg"),
        )
        self.cooldown_btn.setObjectName("cooldown_btn")

        self.gridLayout.addWidget(self.cooldown_btn, 2, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(
            20,
            50,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem6, 1, 0, 1, 2)

        self.temperature_cooldown_btn = BlocksCustomButton(parent=self)
        self.temperature_cooldown_btn.setSizePolicy(sizePolicy)
        self.temperature_cooldown_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.temperature_cooldown_btn.setMaximumSize(QtCore.QSize(250, 80))
        self.temperature_cooldown_btn.setFont(font)
        self.temperature_cooldown_btn.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.temperature_cooldown_btn.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/temperature_related/media/btn_icons/heatsoak_icon.svg"),
        )
        self.temperature_cooldown_btn.setObjectName("temperature_cooldown_btn")
        self.gridLayout.addWidget(self.temperature_cooldown_btn, 2, 0, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem7 = QtWidgets.QSpacerItem(
            20,
            8,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout.addItem(spacerItem7)

        widget.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.temp_header_title.setText(
            _translate("controlStackedWidget", "Temperature")
        )
        self.temp_back_button.setText(_translate("controlStackedWidget", "Back"))
        self.extruder_temp_display.setProperty(
            "button_type", _translate("controlStackedWidget", "secondary_display")
        )
        self.bed_temp_display.setProperty(
            "button_type", _translate("controlStackedWidget", "secondary_display")
        )
        self.cooldown_btn.setText(_translate("controlStackedWidget", "Cooldown"))
        self.temperature_cooldown_btn.setText(
            _translate("controlStackedWidget", "Heatsoak")
        )
