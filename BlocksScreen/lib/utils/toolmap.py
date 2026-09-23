from enum import IntEnum

from PyQt6 import QtCore, QtGui, QtWidgets


class FilamentPos(IntEnum):
    """State-machine position of the filament inside the MMU/extruder path."""

    UNKNOWN = -1
    UNLOADED = 0
    HOMED_GATE = 1
    START_BOWDEN = 2
    IN_BOWDEN = 3
    END_BOWDEN = 4
    HOMED_ENTRY = 5
    HOMED_EXTRUDER = 6
    EXTRUDER_ENTRY = 7
    HOMED_TS = 8
    IN_EXTRUDER = 9
    LOADED = 10


_POSITION_PERCENT: dict[FilamentPos, float] = {
    FilamentPos.UNKNOWN: 0.0,
    FilamentPos.UNLOADED: 0.0,
    FilamentPos.HOMED_GATE: 0.15,
    FilamentPos.START_BOWDEN: 0.25,
    FilamentPos.IN_BOWDEN: 0.45,
    FilamentPos.END_BOWDEN: 0.65,
    FilamentPos.HOMED_ENTRY: 0.70,
    FilamentPos.HOMED_EXTRUDER: 0.75,
    FilamentPos.EXTRUDER_ENTRY: 0.80,
    FilamentPos.HOMED_TS: 0.85,
    FilamentPos.IN_EXTRUDER: 0.92,
    FilamentPos.LOADED: 1.0,
}


class FilamentPathWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.filament_position = FilamentPos.UNLOADED
        self.gate_name = "T0"

        # Animation property for smooth transitions
        self._animation_progress = 0.0
        self._target_progress = 0.0
        self._animation = QtCore.QPropertyAnimation(self, b"animationProgress")
        self._animation.setDuration(800)  # 800ms transition
        self._animation.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)

        # Colors matching FlowGuard style
        self._fill_color = QtGui.QColor(100, 200, 255)
        self._node_color = QtGui.QColor(180, 180, 180)

        # Font
        self._label_font = QtGui.QFont("Segoe UI", 9)
        self._label_font.setBold(True)

        # Constant paint state, the widget animates so nothing here may be per frame
        self._track_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        self._node_pen = QtGui.QPen(self._node_color, 2)
        self._box_pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        self._dark_brush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
        self._fill_brush = QtGui.QBrush(self._fill_color)
        self._label_pen = QtGui.QPen(QtGui.QColor(180, 180, 180))

        # Size dependent paint state, rebuilt on resize
        self._geometry_valid = False
        self._bar_x = 0.0
        self._bar_y = 0.0
        self._bar_height = 0.0
        self._track_rect = QtCore.QRectF()
        self._box_rect = QtCore.QRectF()
        self._pregate_point = QtCore.QPointF()
        self._hub_point = QtCore.QPointF()
        self._top_rect = QtCore.QRectF()
        self._bottom_rect = QtCore.QRectF()

        self.setMinimumSize(60, 200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding
        )

    @QtCore.pyqtProperty(float)
    def animationProgress(self):
        """Property for QPropertyAnimation"""
        return self._animation_progress

    @animationProgress.setter
    def animationProgress(self, value):
        """Setter for animation progress - triggers repaint"""
        self._animation_progress = value
        self.update()

    def set_filament_position(self, position: FilamentPos) -> None:
        """Set the current filament position with smooth animation"""
        self.filament_position = position

        # Get target percentage
        target = self._get_position_percentage(position)

        # Animate from current progress to target
        self._animation.stop()
        self._animation.setStartValue(self._animation_progress)
        self._animation.setEndValue(target)
        self._animation.start()

    def set_gate_name(self, name: str) -> None:
        """Set the gate/tool name"""
        self.gate_name = name
        self.update()

    def _get_position_percentage(self, position: FilamentPos) -> float:
        """Convert FilamentPos to percentage along the path (0.0 to 1.0)"""
        return _POSITION_PERCENT.get(position, 0.0)

    def resizeEvent(self, a0: QtGui.QResizeEvent | None) -> None:
        """Re-implemented method, drop the size dependent paint state"""
        self._geometry_valid = False
        super().resizeEvent(a0)

    def _ensure_geometry(self) -> None:
        """Rebuild the bar, node and label rects after a resize"""
        if self._geometry_valid:
            return

        top_margin = 30
        bottom_margin = 30
        bar_width = 30
        self._bar_x = float(int(self.width() / 2 - bar_width / 2))
        self._bar_y = float(top_margin)
        self._bar_height = float(self.height() - top_margin - bottom_margin)

        self._track_rect = QtCore.QRectF(
            self._bar_x, self._bar_y, bar_width, self._bar_height
        )

        center_x = self._bar_x + bar_width / 2
        self._pregate_point = QtCore.QPointF(center_x, self._bar_y)
        self._hub_point = QtCore.QPointF(center_x, self._bar_y + self._bar_height)

        # Extruder box (middle ~70% down)
        box_height = 40
        box_y = self._bar_y + self._bar_height * 0.70 - box_height / 2
        self._box_rect = QtCore.QRectF(
            self._bar_x - 3, box_y, bar_width + 6, box_height
        )

        self._top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        self._bottom_rect = QtCore.QRectF(0, self.height() - 25, self.width(), 20)
        self._geometry_valid = True

    def _draw_vertical_path(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        # Draw background track
        painter.setPen(self._track_pen)
        painter.setBrush(self._dark_brush)
        painter.drawRect(self._track_rect)

        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_brush)
            painter.drawRect(
                QtCore.QRectF(
                    self._bar_x,
                    self._bar_y,
                    self._track_rect.width(),
                    self._animation_progress * self._bar_height,
                )
            )

        # Pre-Gate node (top)
        painter.setPen(self._node_pen)
        painter.setBrush(self._dark_brush)
        painter.drawEllipse(self._pregate_point, 5, 5)

        # Extruder box (middle ~70% down)
        painter.setPen(self._box_pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.drawRect(self._box_rect)

        # Hub/Gate node (bottom)
        painter.setPen(self._node_pen)
        painter.setBrush(self._dark_brush)
        painter.drawEllipse(self._hub_point, 5, 5)

    def _draw_labels(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(self._label_pen)
        painter.setFont(self._label_font)
        painter.drawText(
            self._top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name
        )
        painter.drawText(
            self._bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead"
        )

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Paint the widget"""
        self._ensure_geometry()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        self._draw_vertical_path(painter)
        self._draw_labels(painter)

        painter.end()


# Example usage
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QWidget()
    window.setWindowTitle("Filament Path Widget Test")
    window.setStyleSheet("background-color: #2a2a2a;")

    layout = QtWidgets.QHBoxLayout(window)

    # Add slider for testing
    test_widget = FilamentPathWidget()
    test_widget.set_gate_name("T0")
    test_widget.setMaximumSize(30, 200)
    layout.addWidget(test_widget)

    slider_layout = QtWidgets.QVBoxLayout()
    slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Vertical)
    slider.setMinimum(0)
    slider.setMaximum(10)
    slider.valueChanged.connect(
        lambda v: test_widget.set_filament_position(FilamentPos(v))
    )
    slider_layout.addWidget(QtWidgets.QLabel("Test"))
    slider_layout.addWidget(slider)
    layout.addLayout(slider_layout)

    window.resize(450, 350)
    window.show()

    sys.exit(app.exec())
