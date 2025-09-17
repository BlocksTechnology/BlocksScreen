import enum

from lib.utils.blocks_label import BlocksLabel
from lib.utils.toggleAnimatedButton import ToggleAnimatedButton
from PyQt6 import QtCore, QtGui, QtWidgets


class NetworkWidgetbuttons(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = ("la test")
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )
        
        self.setupUI()
        self.tb = self.toggle_button

    def text(self) -> str:
        return self._text

    def setText(self, new_text) -> None:
        if self._text_label is not None:
            self._text_label.setText(f"{new_text}")
            self._text = new_text


    def setPixmap(self,pixmap: QtGui.QPixmap):
        self.icon_pixmap_fp = pixmap

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if self.toggle_button.geometry().contains(event.pos()):
            event.ignore()
            return
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
        event.accept() 

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(
            style_painter.RenderHint.Antialiasing, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        
        _color = QtGui.QColor(13, 99, 128, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()



    def setupUI(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(
            self._icon_label.sizePolicy().hasHeightForWidth()
        )
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(
            self.icon_pixmap_fp
        )
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(
            self._text_label.sizePolicy().hasHeightForWidth()
        )
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.White
        )
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)
