from PyQt6 import QtWidgets, QtGui, QtCore
from enum import IntEnum


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
        position_map = {
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
        return position_map.get(position, 0.0)

    def _draw_vertical_path(self, painter: QtGui.QPainter) -> None:
        """Draw the vertical path bar"""
        rect = self.rect()

        top_margin = 30
        bottom_margin = 30

        bar_width = 30
        bar_x = int(rect.width() / 2 - bar_width / 2)
        bar_y = top_margin
        bar_height = rect.height() - top_margin - bottom_margin

        # Draw background track
        bg_pen = QtGui.QPen(QtGui.QColor(40, 40, 40), 2)
        painter.setPen(bg_pen)
        painter.setBrush(QtGui.QColor(25, 25, 25))

        track_rect = QtCore.QRectF(bar_x, bar_y, bar_width, bar_height)
        painter.drawRect(track_rect)

        # Draw filament fill (from bottom up) using animated progress
        if self._animation_progress > 0.0:
            fill_height = self._animation_progress * bar_height

            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.setBrush(self._fill_color)

            fill_rect = QtCore.QRectF(bar_x, bar_y, bar_width, fill_height)
            painter.drawRect(fill_rect)

        # Draw position nodes
        center_x = bar_x + bar_width / 2

        # Pre-Gate node (top)
        pregate_y = bar_y
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, pregate_y), 5, 5)

        # Extruder box (middle ~75% down)
        extruder_y = bar_y + bar_height * 0.70
        box_height = 40
        box_y = extruder_y - box_height / 2

        pen = QtGui.QPen(QtGui.QColor(0, 150, 150), 2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)

        box_rect = QtCore.QRectF(bar_x - 3, box_y, bar_width + 6, box_height)
        painter.drawRect(box_rect)

        # Hub/Gate node (bottom)
        hub_y = bar_y + bar_height
        painter.setPen(QtGui.QPen(self._node_color, 2))
        painter.setBrush(QtGui.QColor(25, 25, 25))
        painter.drawEllipse(QtCore.QPointF(center_x, hub_y), 5, 5)

    def _draw_labels(self, painter: QtGui.QPainter) -> None:
        """Draw labels"""
        painter.setPen(QtGui.QColor(180, 180, 180))
        painter.setFont(self._label_font)

        # Top label
        top_rect = QtCore.QRectF(0, 5, self.width(), 20)
        painter.drawText(top_rect, QtCore.Qt.AlignmentFlag.AlignCenter, self.gate_name)

        # Bottom label
        bottom_y = self.height() - 25
        bottom_rect = QtCore.QRectF(0, bottom_y, self.width(), 20)
        painter.drawText(bottom_rect, QtCore.Qt.AlignmentFlag.AlignCenter, "Toolhead")

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Paint the widget"""
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
