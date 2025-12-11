import typing

from PyQt6 import QtCore, QtGui, QtWidgets
from lib.utils.blocks_label import BlocksLabel
from lib.utils.icon_button import IconButton


class OptionCard(QtWidgets.QAbstractButton):
    clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
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
        self.doubleT: bool = False
        self._setupUi(self)
        self.option_icon.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.option_text.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.secondtext.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.line_separator.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)


        self.setMode(False)
        self.set_card_icon(icon)
        self.set_card_text(text)

    def disable_button(self) -> None:
        """Disable widget button"""
        self.continue_button.setDisabled(True)
        self.repaint()

    def enable_button(self) -> None:
        """Enable widget button"""
        self.continue_button.setEnabled(True)
        self.repaint()

    def set_card_icon(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget icon"""
        scaled = pixmap.scaled(
            300,
            300,
            QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self.option_icon.setPixmap(scaled)
        self.repaint()

    def set_card_text(self, text: str) -> None:
        """Set widget text"""
        self.option_text.setText(text)
        self.repaint()

    def set_card_text_color(self, color: QtGui.QColor) -> None:
        """Set widget text color"""
        self.text_color = color
        _palette = self.option_text.palette()
        _palette.setColor(QtGui.QPalette.ColorRole.WindowText, color)
        self.option_text.setPalette(_palette)
        self.repaint()

    def set_background_color(self, color: QtGui.QColor) -> None:
        """Set widget background color"""
        self.color = color
        self.repaint()

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:
        """Re-implemented method, highlight widget edges"""
        # Illuminate the edges to a lighter blue
        # To achieve this just Force update the widget
        self.update()
        return super().enterEvent(event)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        """Re-implemented method, disable widget edges highlight"""
        # Reset the color
        # Just as before force update the widget
        self.update()
        return super().leaveEvent(a0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        """Re-implemented method, handle mouse press event"""
        self.clicked.emit(self)
        self.update()
        return super().mousePressEvent(a0)

    def setMode(self, double_mode: bool = False):
        """Set the mode of the layout: single or double text."""
        self.doubleT = double_mode

        # Clear existing widgets from layout before adding new ones
        while self.verticalLayout.count():
            item = self.verticalLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        if self.doubleT:
            self.verticalLayout.addWidget(
                self.option_icon,
                0,
                QtCore.Qt.AlignmentFlag.AlignHCenter
                | QtCore.Qt.AlignmentFlag.AlignBottom,
            )
            self.verticalLayout.addWidget(
                self.secondtext, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
            )
            self.verticalLayout.addWidget(
                self.line_separator, 0, QtCore.Qt.AlignmentFlag.AlignCenter
            )
            self.verticalLayout.addWidget(self.option_text)
            self.verticalLayout.addItem(self.spacer)
            self.secondtext.show()
        else:
            self.verticalLayout.addWidget(
                self.option_icon, 0, QtCore.Qt.AlignmentFlag.AlignCenter
            )
            self.verticalLayout.addWidget(
                self.line_separator, 0, QtCore.Qt.AlignmentFlag.AlignCenter
            )
            self.verticalLayout.addWidget(self.option_text)
            self.verticalLayout.addWidget(self.continue_button)

        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
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

    def _setupUi(self, option_card):
        option_card.setObjectName("option_card")
        option_card.resize(200, 300)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.Ignored,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(option_card.sizePolicy().hasHeightForWidth())
        option_card.setSizePolicy(sizePolicy)
        option_card.setMinimumSize(QtCore.QSize(200, 300))
        option_card.setMaximumSize(QtCore.QSize(200, 300))
        self.verticalLayout = QtWidgets.QVBoxLayout(option_card)
        self.verticalLayout.setContentsMargins(0, 0, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.option_icon = BlocksLabel(parent=option_card)
        self.option_icon.setMinimumSize(QtCore.QSize(200, 150))
        self.option_icon.setObjectName("option_icon")
        self.option_icon.setScaledContents(True)
        _button_font = QtGui.QFont()
        _button_font.setBold(True)
        _button_font.setPointSize(20)
        self.secondtext = QtWidgets.QLabel(parent=option_card)
        self.secondtext.setText("%")
        self.secondtext.setStyleSheet("color:white")
        self.secondtext.setFont(_button_font)
        self.secondtext.setObjectName("option_text")
        self.secondtext.setWordWrap(True)
        self.secondtext.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.secondtext.hide()
        self.line_separator = QtWidgets.QFrame(parent=option_card)
        self.line_separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_separator.setMinimumSize(150, 2)
        self.line_separator.setMaximumSize(200, 5)
        self.line_separator.setObjectName("line_separator")
        self.verticalLayout.addWidget(
            self.line_separator,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.option_text = QtWidgets.QLabel(parent=option_card)
        self.option_text.setMinimumSize(QtCore.QSize(200, 50))
        self.option_text.setObjectName("option_text")
        self.option_text.setWordWrap(True)
        self.option_text.setStyleSheet("color:white")
        self.option_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        _palette = self.option_text.palette()
        _palette.setColor(QtGui.QPalette.ColorRole.WindowText, self.text_color)
        self.option_text.setPalette(_palette)

        self.option_text.setFont(_button_font)
        self.continue_button = IconButton(parent=option_card)
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

        self.spacer = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self._retranslateUi(option_card)
        QtCore.QMetaObject.connectSlotsByName(option_card)

    def _retranslateUi(self, option_card):
        _translate = QtCore.QCoreApplication.translate
        option_card.setWindowTitle(_translate("option_card", "Frame"))
        self.option_text.setText(_translate("option_card", "TextLabel"))
        self.continue_button.setProperty(
            "button_type", _translate("option_card", "icon")
        )
