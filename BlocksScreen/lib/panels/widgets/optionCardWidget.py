import typing

from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


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
        # Paint caches, geometry ones invalidated on resize
        self._background: QtGui.QPainterPath | None = None
        self._gradient: QtGui.QRadialGradient | None = None
        self._idle_color = self._dim(self.color)
        self._setupUi(self)
        self.option_icon.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.option_text.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.secondtext.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.line_separator.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.continue_button.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        self.setMode(False)
        self.set_card_icon(icon)
        self.set_card_text(text)

    @staticmethod
    def _dim(color: QtGui.QColor) -> QtGui.QColor:
        """Idle shade of the card, every channel at 70%"""
        return QtGui.QColor(*(int(component * 0.70) for component in color.getRgb()))

    def disable_button(self) -> None:
        """Disable widget button"""
        self.continue_button.setDisabled(True)
        self.update()

    def enable_button(self) -> None:
        """Enable widget button"""
        self.continue_button.setEnabled(True)
        self.update()

    def set_card_icon(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget icon"""
        scaled = pixmap.scaled(
            300,
            300,
            QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        self.option_icon.setPixmap(scaled)
        self.update()

    def set_card_text(self, text: str) -> None:
        """Set widget text"""
        self.option_text.setText(text)
        self.update()

    def set_card_text_color(self, color: QtGui.QColor) -> None:
        """Set widget text color"""
        self.text_color = color
        _palette = self.option_text.palette()
        _palette.setColor(QtGui.QPalette.ColorRole.WindowText, color)
        self.option_text.setPalette(_palette)
        self.update()

    def set_background_color(self, color: QtGui.QColor) -> None:
        """Set widget background color"""
        self.color = color
        self._idle_color = self._dim(color)
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """Re-implemented method, drop the size dependent paint caches"""
        self._background = None
        self._gradient = None
        return super().resizeEvent(a0)

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
        rect_f = self.rect().toRectF()
        hovered = self.underMouse()

        if self._background is None:
            # Rounded background edges
            background_path = QtGui.QPainterPath()
            background_path.addRoundedRect(
                rect_f, 20.0, 20.0, QtCore.Qt.SizeMode.AbsoluteSize
            )
            self._background = background_path

        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.fillPath(self._background, self.color if hovered else self._idle_color)
        if hovered:
            if self._gradient is None:
                _color = QtGui.QColor(self.highlight_color)
                _color.setAlpha(30)
                _edge = QtGui.QColor(self.highlight_color)
                _edge.setAlpha(2)
                _gradient = QtGui.QRadialGradient(
                    QtCore.QPointF(rect_f.left() + 10, rect_f.top()),
                    330.0,
                    rect_f.center(),
                )
                _gradient.setColorAt(0, _color)
                _gradient.setColorAt(0.5, _color)
                _gradient.setColorAt(1, _edge)
                self._gradient = _gradient
            painter.fillPath(self._background, self._gradient)

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
        self.option_icon = IconButton(parent=option_card)
        self.option_icon.setMinimumSize(QtCore.QSize(200, 150))
        self.option_icon.setObjectName("option_icon")
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
