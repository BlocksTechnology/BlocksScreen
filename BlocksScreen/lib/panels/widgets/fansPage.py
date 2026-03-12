import typing
import re
from lib.utils.icon_button import IconButton
from helper_methods import normalize

from PyQt6 import QtCore, QtGui, QtWidgets

from lib.panels.widgets.optionCardWidget import OptionCard


class FansPage(QtWidgets.QWidget):
    tune_display_buttons: dict = {}
    card_options: dict = {}

    request_slider_page = QtCore.pyqtSignal(
        str, int, "PyQt_PyObject", int, int, name="on_slidePage_request"
    )
    request_back_button = QtCore.pyqtSignal(name="request-back-button")

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super(FansPage, self).__init__(parent)

        self._setup_ui()
        self.fans_back_btn.clicked.connect(self.request_back_button.emit)

        self.path = {
            "fan_cage": QtGui.QPixmap(":/fan_related/media/btn_icons/fan_cage.svg"),
            "blower": QtGui.QPixmap(":/fan_related/media/btn_icons/blower.svg"),
            "fan": QtGui.QPixmap(":/fan_related/media/btn_icons/fan.svg"),
        }

    @QtCore.pyqtSlot(str, str, float, name="on_fan_update")
    @QtCore.pyqtSlot(str, str, int, name="on_fan_update")
    def on_fan_object_update(
        self, name: str, field: str, new_value: int | float
    ) -> None:
        """Slot that receives updates from fan objects.

        Args:
            name (str): Fan object name
            field (str): Field name
            new_value (int | float): New value for the field
        """
        if "speed" not in field:
            return

        fields = name.split()
        first_field = fields[0]
        second_field = fields[1] if len(fields) > 1 else None
        name = second_field.replace("_", " ") if second_field else name

        fan_card = self.tune_display_buttons.get(name)
        if fan_card is None and first_field in (
            "fan",
            "fan_generic",
        ):
            icon = self.path.get("fan")
            if second_field:
                second_field = second_field.lower()
                pattern_blower = r"(?:^|_)(?:blower|auxiliary)(?:_|$)"
                pattern_exhaust = r"(?:^|_)exhaust(?:_|$)"
                if re.search(pattern_blower, second_field):
                    icon = self.path.get("blower")
                elif re.search(pattern_exhaust, second_field):
                    icon = self.path.get("fan_cage")

            card = OptionCard(self, name, str(name), icon)  # type: ignore
            card.setObjectName(str(name))

            # Add card to layout and record reference
            self.card_options[name] = card
            self.fans_content_layout.addWidget(card)

            # If the card doesn't have expected UI properties, discard it
            if not hasattr(card, "continue_clicked"):
                del card
                self.card_options.pop(name, None)
                return

            card.setMode(True)
            card.secondtext.setText(f"{new_value}%")
            card.continue_clicked.connect(
                lambda: self.request_slider_page.emit(
                    str(name),
                    int(card.secondtext.text().replace("%", "")),
                    self.on_slider_change,
                    0,
                    100,
                )
            )

            self.tune_display_buttons[name] = card
            self.update()
            fan_card = card

        if fan_card:
            value_percent = new_value * 100 if new_value <= 1 else new_value
            fan_card.secondtext.setText(f"{value_percent:.0f}%")

    @QtCore.pyqtSlot(str, int, name="on_slider_change")
    def on_slider_change(self, name: str, new_value: int) -> None:
        if "speed" in name.lower():
            self.speed_factor_override = new_value / 100
            self.run_gcode_signal.emit(f"M220 S{new_value}")
        if name.lower() == "fan":
            self.run_gcode_signal.emit(
                f"M106 S{int(round((normalize(float(new_value / 100), 0.0, 1.0, 0, 255))))}"
            )  # [0, 255] Range
        else:
            name = name.replace(" ", "_")
            self.run_gcode_signal.emit(
                f'SET_FAN_SPEED FAN="{name}" SPEED={float(new_value / 100.00)}'
            )  # [0.0, 1.0] Range

    def _setup_ui(self) -> None:
        self.setObjectName("fans_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setGeometry(QtCore.QRect(0, 0, 720, 420))

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        spacerItem9 = QtWidgets.QSpacerItem(
            20,
            24,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.verticalLayout.addItem(spacerItem9)

        self.fans_header_layout = QtWidgets.QHBoxLayout()
        self.fans_header_layout.setObjectName("fans_header_layout")

        spacerItem10 = QtWidgets.QSpacerItem(
            60,
            20,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.fans_header_layout.addItem(spacerItem10)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.fans_title_label = QtWidgets.QLabel(parent=self)
        self.fans_title_label.setSizePolicy(sizePolicy)
        self.fans_title_label.setFont(font)
        self.fans_title_label.setStyleSheet("background: transparent; color: white;")
        self.fans_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fans_title_label.setObjectName("fans_title_label")
        self.fans_header_layout.addWidget(self.fans_title_label)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(20)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.fans_back_btn = IconButton(parent=self)
        self.fans_back_btn.setSizePolicy(sizePolicy)
        self.fans_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.fans_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.fans_back_btn.setFont(font)
        self.fans_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.fans_back_btn.setObjectName("fans_back_btn")

        self.fans_header_layout.addWidget(self.fans_back_btn)
        self.verticalLayout.addLayout(self.fans_header_layout)
        spacerItem11 = QtWidgets.QSpacerItem(
            20,
            111,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        self.verticalLayout.addItem(spacerItem11)

        self.fans_content_layout = QtWidgets.QHBoxLayout()
        self.fans_content_layout.setObjectName("fans_content_layout")
        self.verticalLayout.addLayout(self.fans_content_layout)

        self.verticalLayout.addItem(spacerItem11)

        widget.setLayout(self.verticalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.fans_title_label.setText(_translate("controlStackedWidget", "Fans"))
        self.fans_back_btn.setText(_translate("controlStackedWidget", "Back"))
