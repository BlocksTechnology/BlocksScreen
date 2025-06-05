import typing

from PyQt6 import QtCore, QtGui, QtWidgets
from lib.utils.blocks_label import BlocksLabel
from lib.utils.icon_button import IconButton


class OptionCard(QtWidgets.QFrame):
    continue_clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        "PyQt_PyObject", name="continue_clicked"
    )

    def __init__(
        self,
        parent: QtWidgets.QFrame,
        text: str,
        name: str,
        icon: QtGui.QPixmap,
        /,
    ) -> None:
        super().__init__(parent)
        self.color = QtGui.QColor(100, 130, 180, 80)
        self.highlight_color = "#2AC9F9"
        self.text_color = QtGui.QColor(255, 255, 255, 255)
        self.icon_background_color = QtGui.QColor(150, 150, 130, 80)
        self.name = name
        self.card_text = text
        self.setupUi(self)
        self.continue_button.clicked.connect(
            lambda: self.continue_clicked.emit(self)
        )
        self.set_card_icon(icon)
        self.set_card_text(text)

    def disable_button(self) -> None:
        self.continue_button.setDisabled(True)
        self.repaint()

    def enable_button(self) -> None:
        self.continue_button.setEnabled(True)
        self.repaint()

    def set_card_icon(self, pixmap: QtGui.QPixmap) -> None:
        self.option_icon.setPixmap(pixmap)
        self.repaint()

    def set_card_text(self, text: str) -> None:
        self.option_text.setText(text)
        self.repaint()

    def set_card_text_color(self, color: QtGui.QColor) -> None:
        self.text_color = color
        _palette = self.option_text.palette()
        _palette.setColor(QtGui.QPalette.ColorRole.WindowText, color)
        self.option_text.setPalette(_palette)
        self.repaint()

    def set_background_color(self, color: QtGui.QColor) -> None:
        self.color = color
        self.repaint()

    def sizeHint(self) -> QtCore.QSize:
        return super().sizeHint()

    def underMouse(self) -> bool:
        return super().underMouse()

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        # Illuminate the edges to a lighter blue
        # To achieve this just Force update the widget
        self.update()
        return super().enterEvent(event)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        # Reset the color
        # Just as before force update the widget
        self.update()
        return super().leaveEvent(a0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.update()
        return super().mousePressEvent(a0)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # Rounded background edges
        self.background_path = QtGui.QPainterPath()
        self.background_path.addRoundedRect(
            self.rect().toRectF(), 20.0, 20.0, QtCore.Qt.SizeMode.AbsoluteSize
        )

        bg_color = (
            QtGui.QColor(self.color)
            if self.underMouse()
            else QtGui.QColor(
                *(
                    map(
                        lambda component: int(component * 0.70),
                        self.color.getRgb(),
                    )
                )
            )
        )

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)
        painter.fillPath(self.background_path, bg_color)
        if self.underMouse():
            _pen = QtGui.QPen()
            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            _pen.setJoinStyle(QtCore.Qt.PenJoinStyle.RoundJoin)
            _pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            _color = QtGui.QColor(self.highlight_color)
            _color2 = QtGui.QColor(self.highlight_color)
            _color3 = QtGui.QColor(self.highlight_color)
            _color.setAlpha(30)
            _color2.setAlpha(30)
            _color3.setAlpha(2)
            _pen.setColor(_color)
            _gradient = QtGui.QRadialGradient(
                QtCore.QPointF(
                    self.rect().toRectF().left() + 10,
                    self.rect().toRectF().top(),
                ),
                330.0,
                self.rect().toRectF().center(),
            )
            _gradient.setColorAt(0, _color)
            _gradient.setColorAt(0.5, _color2)
            _gradient.setColorAt(1, _color3)
            painter.setBrush(_gradient)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.fillPath(self.background_path, painter.brush())

        painter.end()

    def setupUi(self, option_card):
        option_card.setObjectName("option_card")
        option_card.resize(200, 300)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Ignored,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            option_card.sizePolicy().hasHeightForWidth()
        )
        option_card.setSizePolicy(sizePolicy)
        option_card.setMinimumSize(QtCore.QSize(200, 300))
        option_card.setMaximumSize(QtCore.QSize(200, 300))
        self.verticalLayout = QtWidgets.QVBoxLayout(option_card)
        self.verticalLayout.setContentsMargins(0, 0, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.option_icon = BlocksLabel(parent=option_card)
        self.option_icon.setMinimumSize(QtCore.QSize(200, 150))
        self.option_icon.setObjectName("option_icon")
        self.verticalLayout.addWidget(
            self.option_icon, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )
        self.line_separator = QtWidgets.QFrame(parent=option_card)
        self.line_separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_separator.setMinimumSize(150, 2)
        self.line_separator.setMaximumSize(200, 5)
        self.line_separator.setObjectName("line_separator")
        self.verticalLayout.addWidget(
            self.line_separator,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.option_text = QtWidgets.QLabel(parent=option_card)
        self.option_text.setMinimumSize(QtCore.QSize(200, 50))
        self.option_text.setObjectName("option_text")
        self.verticalLayout.addWidget(
            self.option_text,
        )
        self.continue_button = IconButton(parent=option_card)
        self.option_text.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.option_text.setWordWrap(True)
        _button_font = QtGui.QFont()
        _button_font.setBold(True)
        _palette = self.option_text.palette()
        _palette.setColor(QtGui.QPalette.ColorRole.WindowText, self.text_color)
        self.option_text.setPalette(_palette)
        _button_font.setPointSize(15)
        self.option_text.setFont(_button_font)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.continue_button.sizePolicy().hasHeightForWidth()
        )
        self.continue_button.setSizePolicy(sizePolicy)
        self.continue_button.setMinimumSize(QtCore.QSize(200, 80))
        self.continue_button.setText("")
        self.continue_button.setFlat(True)
        self.continue_button.setProperty(
            "icon_pixmap",
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg"),
        )
        self.continue_button.setObjectName("continue_button")
        self.verticalLayout.addWidget(self.continue_button)

        self.retranslateUi(option_card)
        QtCore.QMetaObject.connectSlotsByName(option_card)

    def retranslateUi(self, option_card):
        _translate = QtCore.QCoreApplication.translate
        option_card.setWindowTitle(_translate("option_card", "Frame"))
        self.option_text.setText(_translate("option_card", "TextLabel"))
        self.continue_button.setProperty(
            "button_type", _translate("option_card", "icon")
        )
