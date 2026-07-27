import typing

from devices.amu.models import FilamentPos
from PyQt6 import QtCore, QtGui, QtWidgets


class MmuToolmapWidget(QtWidgets.QWidget):
    _POS: typing.ClassVar[dict[str, int]] = {
        "BEFORE_PRE_GATE": 40,
        "AFTER_GATE": 70,
        "START_BOWDEN": 135,
        "MID_BOWDEN": 221,
        "END_BOWDEN": 290,
        "EXTRUDER": 295,
        "TOOLHEAD": 325,
        "NOZZLE_START": 371,
    }

    _H_VIEW_W = 440
    _H_VIEW_H = 130

    _TUBE_Y = 58
    _TUBE_THICKNESS = 14
    _TUBE_START_X = 25
    _TAPER_START_X = 400
    _NOZZLE_TIP_X = 408
    _NOZZLE_FILL_START_X = 380

    _GATE_ZONE = QtCore.QRectF(10, 8, 150, _H_VIEW_H - 16)
    _TOOLHEAD_ZONE = QtCore.QRectF(290, 8, 85, _H_VIEW_H - 16)

    _OUTLINE = QtGui.QColor("#ffffff")
    _ZONE_BG = QtGui.QColor("#38465B7E")
    _MUTED_TEXT = QtGui.QColor("#B4B4B4")
    _ACTIVE = QtGui.QColor("#2ec4a0")
    _HEATING = QtGui.QColor("#FF9800")

    _HEAT_ZONE = QtCore.QRectF(160, 20, 130, 30)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(680, 260)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
        )

        self._label_font = QtGui.QFont("Segoe UI", 10)
        self._zone_font = QtGui.QFont()
        self._zone_font.setBold(True)
        self._zone_font.setPointSize(9)
        self._temp_font = QtGui.QFont()
        self._temp_font.setPointSize(8)

        self._filament_pos = FilamentPos.UNLOADED
        self._bowden_progress = -1.0
        self._gate_color = QtGui.QColor("#787878")
        self._action = ""
        self._current_temp = 0.0
        self._target_temp = 0.0

        self.lefttext: str = "AMU"

        self._heat_dot_count = 0
        self._heat_dot_timer = QtCore.QTimer(self)
        self._heat_dot_timer.setInterval(1000)
        self._heat_dot_timer.timeout.connect(self._add_heat_dot)

        self._sensors = {
            "mmu_pre_gate": False,
            "mmu_gate": False,
            "toolhead": False,
        }

        self._fill_progress = 0.0
        self._fill_animation = QtCore.QPropertyAnimation(self, b"fillProgress")
        self._fill_animation.setDuration(500)
        self._fill_animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)

    @QtCore.pyqtProperty(float)
    def fillProgress(self):
        return self._fill_progress

    @fillProgress.setter
    def fillProgress(self, value):
        self._fill_progress = value
        self.update()

    def set_gate_color(self, color: QtGui.QColor) -> None:
        """Set the color of the filament fill bar, e.g. from the selected gate's spool color."""
        self._gate_color = color
        self.update()

    def set_sensor(self, name: str, active: bool) -> None:
        """Set the active state of a sensor marker ("mmu_pre_gate", "mmu_gate", "toolhead")."""
        self._sensors[name] = active
        self.update()

    def set_left_text(self, text: str) -> None:
        """sets left box title (e.g. "AMU" , "AUXILIAR EXTRUDER")"""
        self.lefttext = text
        self.update()

    def set_action(self, action: str) -> None:
        """Set the current MMU action (e.g. "Idle", "Loading", "Unloading", "Heating").

        Starts/stops the heating-dot animation timer as needed.
        """
        self._action = action
        if action == "Heating":
            if not self._heat_dot_timer.isActive():
                self._heat_dot_count = 0
                self._heat_dot_timer.start()
        else:
            self._heat_dot_timer.stop()
        self.update()

    def _add_heat_dot(self) -> None:
        self._heat_dot_count += 1
        if self._heat_dot_count > 3:
            self._heat_dot_count = 0
        self.update()

    def set_temps(self, current: float, target: float) -> None:
        """Set the extruder current/target temperatures shown under the heating message."""
        self._current_temp = current
        self._target_temp = target
        self.update()

    def set_filament_pos(self, pos: FilamentPos, bowden_progress: float = -1.0) -> None:
        """Animate the fill bar to the local-coordinate x matching the given filament position.

        Args:
            pos: Current position of the filament in the MMU/extruder path.
            bowden_progress: Percentage (0-100) through the bowden tube; only used
                when pos is START_BOWDEN/IN_BOWDEN and >= 0, otherwise the fill
                snaps to fixed checkpoints for that position.
        """
        self._filament_pos = pos
        self._bowden_progress = bowden_progress
        self._animate_fill_to(self._compute_fill_height())

    def _compute_fill_height(self) -> float:
        pos = self._filament_pos
        P = self._POS

        if pos == FilamentPos.UNLOADED:
            return P["BEFORE_PRE_GATE"]
        if pos == FilamentPos.HOMED_GATE:
            return P["AFTER_GATE"]
        if (
            pos in (FilamentPos.START_BOWDEN, FilamentPos.IN_BOWDEN)
            and self._bowden_progress >= 0
        ):
            bowden_range = P["END_BOWDEN"] - P["START_BOWDEN"]
            return P["START_BOWDEN"] + bowden_range * self._bowden_progress / 100
        if pos == FilamentPos.START_BOWDEN:
            return P["START_BOWDEN"]
        if pos == FilamentPos.IN_BOWDEN:
            return P["MID_BOWDEN"]
        if pos in (FilamentPos.END_BOWDEN, FilamentPos.HOMED_ENTRY):
            return P["EXTRUDER"]
        if pos in (FilamentPos.HOMED_EXTRUDER, FilamentPos.EXTRUDER_ENTRY):
            return P["TOOLHEAD"] - 10
        if pos == FilamentPos.HOMED_TS:
            return P["TOOLHEAD"]
        if pos == FilamentPos.IN_EXTRUDER:
            return P["TOOLHEAD"] + 13
        if pos == FilamentPos.LOADED:
            return P["NOZZLE_START"]
        return 0.0

    def _animate_fill_to(self, value: float) -> None:
        self._fill_animation.stop()
        self._fill_animation.setStartValue(self._fill_progress)
        self._fill_animation.setEndValue(value)
        self._fill_animation.start()

    def _transform(self) -> QtGui.QTransform:
        scale = min(self.width() / self._H_VIEW_W, self.height() / self._H_VIEW_H)
        offset_x = (self.width() - self._H_VIEW_W * scale) / 2
        offset_y = (self.height() - self._H_VIEW_H * scale) / 2
        t = QtGui.QTransform()
        t.translate(offset_x, offset_y)
        t.scale(scale, scale)
        return t

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setTransform(self._transform())

        self._draw_zones(painter)
        self._draw_tube(painter)
        self._draw_nozzle(painter)
        self._draw_sensors(painter)
        self._draw_heat_message(painter)

        painter.end()

    def _draw_zones(self, painter: QtGui.QPainter) -> None:
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(self._ZONE_BG)
        painter.drawRoundedRect(self._GATE_ZONE, 20, 20)
        painter.drawRoundedRect(self._TOOLHEAD_ZONE, 20, 20)

        painter.setPen(QtGui.QColor("#FFFFFF"))
        painter.setFont(self._zone_font)
        for zone, name in (
            (self._GATE_ZONE, self.lefttext),
            (self._TOOLHEAD_ZONE, "Toolhead"),
        ):
            painter.drawText(
                QtCore.QRectF(zone.left(), zone.top() + 12, zone.width(), 14),
                QtCore.Qt.AlignmentFlag.AlignHCenter,
                name,
            )

    def _draw_tube(self, painter: QtGui.QPainter) -> None:
        outline = QtGui.QPainterPath()
        outline.moveTo(self._TUBE_START_X, self._TUBE_Y)
        outline.lineTo(self._TAPER_START_X, self._TUBE_Y)
        outline.lineTo(self._NOZZLE_TIP_X, self._TUBE_Y + self._TUBE_THICKNESS / 2)
        outline.lineTo(self._TAPER_START_X, self._TUBE_Y + self._TUBE_THICKNESS)
        outline.lineTo(self._TUBE_START_X, self._TUBE_Y + self._TUBE_THICKNESS)
        painter.setPen(QtGui.QPen(self._OUTLINE, 1))
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.drawPath(outline)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(self._gate_color)
        fill_width = min(
            max(0.0, self._fill_progress), self._TAPER_START_X - self._TUBE_START_X
        )
        painter.drawRect(
            QtCore.QRectF(
                self._TUBE_START_X, self._TUBE_Y, fill_width, self._TUBE_THICKNESS
            )
        )

    def _draw_heat_message(self, painter: QtGui.QPainter) -> None:
        if self._action != "Heating":
            return
        dots = ("." * self._heat_dot_count) + (" " * (3 - self._heat_dot_count))

        top_zone = QtCore.QRectF(
            self._HEAT_ZONE.left(),
            self._HEAT_ZONE.top(),
            self._HEAT_ZONE.width(),
            self._HEAT_ZONE.height() / 2,
        )
        bottom_zone = QtCore.QRectF(
            self._HEAT_ZONE.left(),
            self._HEAT_ZONE.top() + self._HEAT_ZONE.height() / 2,
            self._HEAT_ZONE.width(),
            self._HEAT_ZONE.height() / 2,
        )

        painter.setPen(self._HEATING)
        painter.setFont(self._zone_font)
        painter.drawText(
            top_zone, QtCore.Qt.AlignmentFlag.AlignCenter, f"Heating{dots}"
        )

        painter.setPen(self._MUTED_TEXT)
        painter.setFont(self._temp_font)
        painter.drawText(
            bottom_zone,
            QtCore.Qt.AlignmentFlag.AlignCenter,
            f"{self._current_temp:.0f}°/{self._target_temp:.0f}°",
        )

    def _draw_nozzle(self, painter: QtGui.QPainter) -> None:
        if self._filament_pos != FilamentPos.LOADED:
            return
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(self._gate_color)
        painter.drawPolygon(
            QtGui.QPolygonF(
                [
                    QtCore.QPointF(self._NOZZLE_FILL_START_X, self._TUBE_Y),
                    QtCore.QPointF(self._TAPER_START_X, self._TUBE_Y),
                    QtCore.QPointF(
                        self._NOZZLE_TIP_X, self._TUBE_Y + self._TUBE_THICKNESS / 2
                    ),
                    QtCore.QPointF(
                        self._TAPER_START_X, self._TUBE_Y + self._TUBE_THICKNESS
                    ),
                    QtCore.QPointF(
                        self._NOZZLE_FILL_START_X, self._TUBE_Y + self._TUBE_THICKNESS
                    ),
                ]
            )
        )

    def _draw_sensor_marker(
        self, painter: QtGui.QPainter, x: float, label: str, active: bool
    ) -> None:
        color = self._ACTIVE if active else self._MUTED_TEXT
        line_top_y = self._TUBE_Y + self._TUBE_THICKNESS

        painter.setPen(QtGui.QPen(color, 1.5))
        painter.drawLine(QtCore.QPointF(x, line_top_y), QtCore.QPointF(x, 96))

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.drawEllipse(QtCore.QPointF(x, line_top_y), 3.5, 3.5)

        painter.setPen(color)
        painter.setFont(self._label_font)
        painter.drawText(
            QtCore.QRectF(x - 30, 98, 60, 16),
            QtCore.Qt.AlignmentFlag.AlignCenter,
            label,
        )

    def _draw_sensors(self, painter: QtGui.QPainter) -> None:
        self._draw_sensor_marker(painter, 50, "Pre-Gate", self._sensors["mmu_pre_gate"])
        self._draw_sensor_marker(painter, 110, "Gate", self._sensors["mmu_gate"])
        self._draw_sensor_marker(painter, 332, "Toolhead", self._sensors["toolhead"])
