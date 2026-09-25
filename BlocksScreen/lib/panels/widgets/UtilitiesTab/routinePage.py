import math
import typing
from dataclasses import dataclass, replace

from lib.panels.widgets.Common.basePopup import BasePopup
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class RoutineCheckPage(QtWidgets.QWidget):
    """Routine check page of the utilities tab."""

    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-back"
    )
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )
    call_load_panel: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, str, bool, name="call-load-panel"
    )
    request_tb_page: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-tb-page"
    )
    subscribe_config: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [list, "PyQt_PyObject"],
        [str, "PyQt_PyObject"],
        name="on-subscribe-config",
    )

    HOMED_AXES = frozenset("xyz")

    @dataclass(frozen=True)
    class Step:
        label: str
        prompt: str
        gcode: str
        cleanup: str = ""

    @dataclass(frozen=True)
    class AxisLimits:
        """Travel range of one stepper, as reported by the printer config."""

        min: float
        max: float
        homes_at_min: bool

        @property
        def span(self) -> float:
            """How far the axis can travel end to end."""
            return self.max - self.min

    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
    ) -> None:
        super().__init__(parent)
        self._setup_ui()

        self.fans: list[str] = []
        self.axis_limits: dict[str, RoutineCheckPage.AxisLimits] = {}

        self._steps: list[RoutineCheckPage.Step] = []
        self._index: int = -1
        self._awaiting: bool = False

        self._homing: bool = False
        self._home_dropped: bool = False
        self._pending: RoutineCheckPage.Step | None = None

        self._home_settle: QtCore.QTimer = QtCore.QTimer(self)
        self._home_settle.setSingleShot(True)
        self._home_settle.setInterval(10_000)
        self._home_settle.timeout.connect(self._home_finished)

        self._home_guard: QtCore.QTimer = QtCore.QTimer(self)
        self._home_guard.setSingleShot(True)
        self._home_guard.setInterval(180_000)
        self._home_guard.timeout.connect(self._home_finished)

        self.answerPopup: BasePopup = BasePopup(self)
        self.answerPopup.accepted.connect(lambda: self.on_answer(True))
        self.answerPopup.rejected.connect(lambda: self.on_answer(False))

        self.rp_button_1.clicked.connect(self.start_fan)
        self.rp_button_2.clicked.connect(self.start_axis)
        self.rp_button_3.clicked.connect(self.start_extruder)
        self.rp_button_4.clicked.connect(self.start_bed)
        self.back_button.clicked.connect(self.abort)
        self.back_button.clicked.connect(self.request_back)

    def on_object_list(self, object_list: list):
        """Collect the fans this printer reports, dropping any earlier list."""
        self.fans = []
        for obj in object_list:
            base_name = obj.split()[0]

            if base_name == "fan_generic" or base_name == "fan":
                self.fans.append(obj.removeprefix(base_name + " "))

    @QtCore.pyqtSlot(dict, name="on_object_config")
    @QtCore.pyqtSlot(list, name="on_object_config")
    def on_object_config(self, config: dict | list) -> None:
        """Handle receiving printer object configurations"""
        if not config:
            return
        self.axis_limits.update(self.parse_axis_limits(config))

    def on_printer_config_received(self, config: dict) -> None:
        """Handle printer configuration"""
        for axis in ("x", "y", "z"):
            self.subscribe_config[str, "PyQt_PyObject"].emit(
                f"stepper_{axis}", self.on_object_config
            )

    @QtCore.pyqtSlot(str, str, name="on_toolhead_update")
    def on_toolhead_update(self, field: str, value: str) -> None:
        """Watch homed_axes so the homing screen knows when to come down."""
        if field != "homed_axes" or not self._homing:
            return

        if not self.HOMED_AXES <= set(str(value).lower()):
            self._home_dropped = True
            return

        if self._home_dropped and not self._home_settle.isActive():
            self._home_settle.start()

    def start_fan(self) -> None:
        """Check every fan this printer reports, one at a time."""
        self.start_routine(self.fan_steps(self.fans))

    def start_axis(self) -> None:
        """Home, then move each axis out and back so the user can watch it."""
        self.start_routine(self.axis_steps(self.axis_limits))

    def start_extruder(self) -> None:
        """Check the extruder heater."""
        self.start_routine(self.heater_steps(["extruder"]))

    def start_bed(self) -> None:
        """Check the bed heater."""
        self.start_routine(self.heater_steps(["heater_bed"]))

    def start_routine(self, steps: list[Step]) -> None:
        """Begin a routine, asking about each step in turn."""
        self.abort()
        self._steps = steps
        self._index = -1
        self.next_step()

    def next_step(self) -> None:
        """Advance to the next step, or finish when they have all been checked."""
        self._index += 1
        if self._index >= len(self._steps):
            self._reset()
            return
        self._awaiting = True
        step = self._steps[self._index]
        self.send_gcode(step.gcode)
        if self._homing:
            self._pending = step
        else:
            self._ask(step)

    def on_answer(self, ok: bool) -> None:
        """Continue to the next step, or hand over to troubleshoot on a no."""
        if not self._awaiting:
            return
        self._awaiting = False
        cleanup = self._steps[self._index].cleanup
        if cleanup:
            self.send_gcode(cleanup)
        if ok:
            self.next_step()
            return
        self._reset()
        self.request_tb_page.emit()

    def abort(self) -> None:
        """Cancel a running routine and undo anything it left running."""
        if not self._steps:
            return
        self.answerPopup.hide()

        seen: set[str] = set()
        for step in self._steps:
            if step.cleanup and step.cleanup not in seen:
                seen.add(step.cleanup)
                self.send_gcode(step.cleanup)

        self._reset()

    def _reset(self) -> None:
        self._steps = []
        self._index = -1
        self._awaiting = False
        self._pending = None

    def send_gcode(self, gcode: str) -> None:
        """Run a g-code block, raising the homing screen if it homes."""
        if "G28" in gcode:
            self._await_home()
        self.run_gcode_signal.emit(gcode)

    def _await_home(self) -> None:
        self._homing = True
        self._home_dropped = False
        self._home_settle.stop()
        self._home_guard.start()
        self.answerPopup.hide()
        self.call_load_panel.emit(True, "Homing...\nPlease wait", False)

    def _home_finished(self) -> None:
        self._home_settle.stop()
        self._home_guard.stop()
        self._homing = False
        self._home_dropped = False
        self.call_load_panel.emit(False, "", False)

        step, self._pending = self._pending, None
        if step is not None:
            self._ask(step)

    def _ask(self, step: Step) -> None:
        self.answerPopup.set_message(step.prompt)
        self.answerPopup.show()

    @classmethod
    def fan_steps(cls, fans: list[str]) -> list[Step]:
        steps = []
        for fan in fans:
            if fan == "fan":
                label = "part cooling fan"
                on, off = "M106 S255", "M107"
            else:
                label = fan
                on = f"SET_FAN_SPEED FAN={fan} SPEED=0.8"
                off = f"SET_FAN_SPEED FAN={fan} SPEED=0"
            steps.append(
                cls.Step(
                    label=label,
                    prompt=f"Please check if the {label} is spinning.",
                    gcode=f"{on}\nM400",
                    cleanup=off,
                )
            )
        return steps

    @classmethod
    def heater_steps(cls, heaters: list[str]) -> list[Step]:
        """Build one check step per heater, warming each to 60 degrees."""
        steps = []
        for heater in heaters:
            label = "bed heater" if heater == "heater_bed" else heater
            steps.append(
                cls.Step(
                    label=label,
                    prompt=(
                        f"Please check if the {label} reaches 60ºC.\n"
                        "It may take a few moments."
                    ),
                    gcode=f"SET_HEATER_TEMPERATURE HEATER={heater} TARGET=60\nM400",
                    cleanup="TURN_OFF_HEATERS",
                )
            )
        return steps

    @classmethod
    def parse_axis_limits(
        cls,
        config: dict | list | None,
    ) -> dict[str, AxisLimits]:
        """Pull the travel range of every stepper out of a printer config reply."""
        if not config:
            return {}

        limits = {}
        for item in [config] if isinstance(config, dict) else config:
            for key, value in item.items():
                if not key.startswith("stepper_") or not isinstance(value, dict):
                    continue

                pos_min = value.get("position_min")
                pos_max = value.get("position_max")
                if pos_min is None and pos_max is None:
                    continue

                low = float(pos_min) if pos_min is not None else -math.inf
                high = float(pos_max) if pos_max is not None else math.inf

                endstop_raw = value.get("position_endstop")
                endstop = float(endstop_raw) if endstop_raw is not None else 0.0
                homes_at_min = abs(endstop - low) <= abs(endstop - high)

                limits[key.removeprefix("stepper_")] = cls.AxisLimits(
                    min=low, max=high, homes_at_min=homes_at_min
                )
        return limits

    @staticmethod
    def axis_move_gcode(
        axis: str,
        limits: AxisLimits,
        margin: float = 70.0,
        park: float | None = None,
    ) -> str:
        """Move the axis most of the way out and back, in absolute coordinates."""
        span = limits.span
        if not math.isfinite(span) or span <= 0:
            return ""

        if span - (2 * margin) <= 0:
            margin = span * 0.1

        far = limits.max - margin if limits.homes_at_min else limits.min + margin
        middle = (limits.min + limits.max) / 2

        name = axis.upper()
        moves = [
            "G90",
            f"G1 {name}{far:.2f} F{6000}",
            f"G1 {name}{middle:.2f} F{6000}",
        ]
        if park is not None:
            parked = min(max(park, limits.min), limits.max)
            if abs(parked - middle) >= 0.01:
                moves.append(f"G1 {name}{parked:.2f} F{6000}")

        return "\n".join(moves)

    @classmethod
    def axis_steps(
        cls,
        limits: dict[str, AxisLimits],
        axes: typing.Sequence[str] = ("x", "y", "z"),
    ) -> list[Step]:
        """Build one check step per axis, homing once before the first of them."""
        y = limits.get("y")
        park_x = (
            (y.min + y.max) / 2 if y is not None and math.isfinite(y.span) else None
        )

        steps = []
        for axis in ["x", "y", "z"]:
            limit = limits.get(axis)
            if limit is None:
                continue

            moves = cls.axis_move_gcode(
                axis, limit, park=park_x if axis == "x" else None
            )
            if not moves:
                continue

            prologue = "" if steps else "G28\nM400\n"
            steps.append(
                cls.Step(
                    label=f"{axis.upper()} axis",
                    prompt=f"Please ensure the {axis.upper()} axis moves correctly.",
                    gcode=f"{prologue}{moves}\nM400",
                )
            )

        if steps:
            steps[-1] = replace(steps[-1], cleanup="G28")
        return steps

    def _setup_ui(self) -> None:

        self.blank = QtWidgets.QWidget()
        self.blank.setMinimumSize(QtCore.QSize(250, 80))
        self.blank.setMaximumSize(QtCore.QSize(250, 80))

        self.Hblank = QtWidgets.QWidget()
        self.Hblank.setMinimumSize(QtCore.QSize(60, 60))
        self.Hblank.setMaximumSize(QtCore.QSize(60, 60))

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.rp_header_layout = QtWidgets.QHBoxLayout()
        self.rp_header_layout.setObjectName("rp_header_layout")

        self.rp_header_layout.addWidget(self.Hblank)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.rp_header_title = QtWidgets.QLabel(parent=self)
        self.rp_header_title.setSizePolicy(sizePolicy)
        self.rp_header_title.setMinimumSize(QtCore.QSize(0, 60))
        self.rp_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        self.rp_header_title.setFont(font)
        self.rp_header_title.setStyleSheet("background: transparent; color: white;")
        self.rp_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.rp_header_layout.addWidget(self.rp_header_title)

        self.back_button = IconButton(parent=self)
        self.back_button.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.rp_header_layout.addWidget(self.back_button)

        self.verticalLayout.addLayout(self.rp_header_layout)

        self.rp_content_layout = QtWidgets.QGridLayout()
        self.rp_content_layout.setObjectName("rp_content_layout")

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(19)

        self.rp_button_1 = BlocksCustomButton(parent=self)
        self.rp_button_1.setSizePolicy(sizePolicy)
        self.rp_button_1.setMinimumSize(QtCore.QSize(250, 80))
        self.rp_button_1.setMaximumSize(QtCore.QSize(250, 80))
        self.rp_button_1.setFont(font)
        self.rp_button_1.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/fan_related/media/btn_icons/fan_cage.svg"),
        )
        self.rp_content_layout.addWidget(self.rp_button_1, 0, 0, 1, 1)

        self.rp_button_2 = BlocksCustomButton(parent=self)
        self.rp_button_2.setSizePolicy(sizePolicy)
        self.rp_button_2.setMinimumSize(QtCore.QSize(250, 80))
        self.rp_button_2.setMaximumSize(QtCore.QSize(250, 80))
        self.rp_button_2.setFont(font)
        self.rp_button_2.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/motion/media/btn_icons/axis_maintenance.svg"),
        )
        self.rp_content_layout.addWidget(self.rp_button_2, 0, 1, 1, 1)

        self.rp_button_3 = BlocksCustomButton(parent=self)
        self.rp_button_3.setSizePolicy(sizePolicy)
        self.rp_button_3.setMinimumSize(QtCore.QSize(250, 80))
        self.rp_button_3.setMaximumSize(QtCore.QSize(250, 80))
        self.rp_button_3.setFont(font)
        self.rp_button_3.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/extruder_related/media/btn_icons/nozzle.svg"),
        )
        self.rp_content_layout.addWidget(self.rp_button_3, 1, 0, 1, 1)

        self.rp_button_4 = BlocksCustomButton(parent=self)
        self.rp_button_4.setSizePolicy(sizePolicy)
        self.rp_button_4.setMinimumSize(QtCore.QSize(250, 80))
        self.rp_button_4.setMaximumSize(QtCore.QSize(250, 80))
        self.rp_button_4.setFont(font)
        self.rp_button_4.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(
                ":/temperature_related/media/btn_icons/temperature_plate.svg"
            ),
        )
        self.rp_content_layout.addWidget(self.rp_button_4, 1, 1, 1, 1)

        self.rp_content_layout.addWidget(self.blank, 2, 0, 1, 1)

        self.rp_content_layout.setRowMinimumHeight(0, 80)
        self.rp_content_layout.setRowMinimumHeight(1, 80)
        self.rp_content_layout.setRowMinimumHeight(2, 80)

        content_widget = QtWidgets.QWidget(parent=self)
        content_widget.setLayout(self.rp_content_layout)
        content_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.rp_content_layout.setContentsMargins(0, 0, 0, 0)
        content_widget.setFixedHeight(80 * 3 + self.rp_content_layout.spacing() * 2)

        self.verticalLayout.addWidget(content_widget)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("controlStackedWidget", "StackedWidget"))
        self.rp_header_title.setText(
            _translate("controlStackedWidget", "Routine Check")
        )

        self.rp_button_1.setText(_translate("controlStackedWidget", "Fans"))
        self.rp_button_2.setText(_translate("controlStackedWidget", "Axis"))
        self.rp_button_3.setText(_translate("controlStackedWidget", "extruder"))
        self.rp_button_4.setText(_translate("controlStackedWidget", "Bed Heater"))
