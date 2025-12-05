from PyQt6 import QtCore, QtGui, QtWidgets


class BlocksSlider(QtWidgets.QSlider):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.highlight_color = "#2AC9F9"
        self.gradient_pos = QtCore.QPointF(0.0, 0.0)
        self.setMinimumSize(300, 100)
        self.setMaximumSize(400, 100)
        self.setMouseTracking(True)
        self.setTracking(True)
        self.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.setTickInterval(20)
        self.setMinimum(0)
        self.setMaximum(100)

    def setOrientation(self, a0: QtCore.Qt.Orientation) -> None:
        return super().setOrientation(a0)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        """Handle mouse press events"""
        if (ev.button() == QtCore.Qt.MouseButton.LeftButton) and self.hit_test(
            ev.position().toPoint().toPointF()
        ):
            self.setSliderDown(True)
            ev.accept()
        else:
            return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        """Handle mouse release events"""
        if self.isSliderDown():
            self.setSliderDown(False)
        return super().mouseReleaseEvent(ev)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent) -> None:
        """Handle mouse move events"""
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        if self.isSliderDown():
            self._set_slider_pos(ev.position().toPoint().toPointF())
            self.gradient_pos = ev.position().toPoint().toPointF()
            self.update()
            ev.accept()
        else:
            return super().mouseMoveEvent(ev)

    def hit_test(self, pos: QtCore.QPointF) -> bool:
        """Hit test to allow dragging larger handle area

        Args:
            pos (QtCore.QPointF): _description_

        Returns:
            bool: If the handle contains the specified position
        """
        _handle_path = QtGui.QPainterPath()
        _handle_path.addRoundedRect(self._handle_rect.toRectF(), 6, 6)
        return _handle_path.contains(pos)

    def _set_slider_pos(self, pos: QtCore.QPointF):
        min_val = self.minimum()
        max_val = self.maximum()
        if self.orientation() == QtCore.Qt.Orientation.Horizontal:
            slider_length = self._groove_rect.width()
            slider_start = self._groove_rect.x()
            pos_x = pos.x()
            new_val = (
                min_val + (max_val - min_val) * (pos_x - slider_start) // slider_length
            )
        else:
            slider_length = self._groove_rect.height()
            slider_start = self._groove_rect.y()
            pos_y = pos.y()
            new_val = (
                min_val + (max_val - min_val) * (pos_y - slider_start) / slider_length
            )
        self.setSliderPosition(int(round(new_val)))
        self.setValue(int(round(new_val)))
        self.update()

    def paintEvent(self, ev: QtGui.QPaintEvent) -> None:
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        _style = self.style()

        # Clip the opt rect inside, so the handle and
        # groove doesn't exceed the limits
        opt.rect = opt.rect.adjusted(12, 10, -18, 20)  # This is a bit hardcoded

        self._groove_rect = _style.subControlRect(
            QtWidgets.QStyle.ComplexControl.CC_Slider,
            opt,
            QtWidgets.QStyle.SubControl.SC_SliderGroove,
            self,
        )

        self._groove_rect.setSize(QtCore.QSize(self.width() - 25, 30))

        self._handle_rect = _style.subControlRect(
            QtWidgets.QStyle.ComplexControl.CC_Slider,
            opt,
            QtWidgets.QStyle.SubControl.SC_SliderHandle,
            self,
        )

        self._handle_rect.setSize(QtCore.QSize(20, 50))
        # self.style().subControlRect(
        #     QtWidgets.QStyle.ComplexControl.CC_Slider, opt, QtWidgets.QStyle.SubControl.SC_SliderGroove or QtWidgets.QStyle.SubControl.SC_SliderHandle
        # )

        # if opt.state & QtWidgets.QStyle.StateFlag.State_Sunken:
        #     # give the track a color
        #     ...
        # elif opt.state & QtWidgets.QStyle.StateFlag.State_MouseOver:
        #     # Give another color when the mouse is over the track
        #     ...
        # else:
        #     # give a default color for the track
        #     ...
        _groove_x = (self.width() - self._groove_rect.width()) // 2
        _groove_y = (self.height() - self._groove_rect.height()) // 2

        self._groove_rect.moveTo(QtCore.QPoint(_groove_x, _groove_y))
        _handle_y = (self.height() - self._handle_rect.height()) // 2
        self._handle_rect.moveTop(_handle_y)

        _handle_color = (
            QtGui.QColor(164, 164, 164)
            if self.isSliderDown()
            else QtGui.QColor(223, 223, 223)
        )
        _handle_path = QtGui.QPainterPath()
        _handle_path.addRoundedRect(self._handle_rect.toRectF(), 5, 5)
        _groove_path = QtGui.QPainterPath()
        _groove_path.addRoundedRect(self._groove_rect.toRectF(), 15, 15)

        if self.isSliderDown():
            _handle_x = (
                self.sliderPosition() - _handle_path.currentPosition().x()
            ) // 2
            _handle_path.moveTo(int(round(_handle_x)), _handle_y)

        gradient_path = QtGui.QPainterPath()
        gradient_path.addRoundedRect(
            self._groove_rect.toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.TextAntialiasing, True)
        _color = QtGui.QColor(164, 164, 164)
        _color.setAlphaF(0.5)
        painter.fillPath(_groove_path, _color)  # Primary groove background color

        _color = QtGui.QColor(self.highlight_color)
        _color_1 = QtGui.QColor(self.highlight_color)
        _color_2 = QtGui.QColor(self.highlight_color)
        _color.setAlpha(110)
        _color_1.setAlpha(50)
        _color_2.setAlpha(10)
        _gradient = QtGui.QRadialGradient(
            self._handle_rect.center().toPointF(),
            200.0,
            self._handle_rect.center().toPointF(),
        )
        _gradient.setColorAt(0, _color)
        _gradient.setColorAt(0.5, _color_1)
        _gradient.setColorAt(1, _color_2)

        self.text_box_rect = _style.subControlRect(
            QtWidgets.QStyle.ComplexControl.CC_Slider,
            opt,
            QtWidgets.QStyle.SubControl.SC_SliderTickmarks,
            self,
        )
        tick_interval = self.tickInterval() or self.singleStep()
        min_v, max_v = self.minimum(), self.maximum()
        painter.setPen(QtGui.QColor("#888888"))
        fm = QtGui.QFontMetrics(painter.font())
        label_offset = 4

        _style.drawComplexControl(
            QtWidgets.QStyle.ComplexControl.CC_Slider, opt, painter, self
        )
        self.setStyle(_style)

        for v in [min_v, max_v]:
            x = (
                QtWidgets.QStyle.sliderPositionFromValue(
                    min_v, max_v, v, self._groove_rect.width()
                )
                + self._groove_rect.x()
            )
            y1 = self._groove_rect.bottom()
            y2 = y1 + 15  # tick length
            label = str(v)
            text_w = fm.horizontalAdvance(label)
            text_h = fm.ascent()
            text_x = x - text_w // 2
            text_y = y2 + text_h + label_offset
            painter.setPen(QtGui.QColor(255, 255, 255))
            painter.drawLine(x, y1, x, y2)
            painter.drawText(text_x, text_y, label)

        # Paint the elements with colors
        painter.setBrush(_gradient)
        painter.fillPath(gradient_path, painter.brush())
        painter.fillPath(_handle_path, _handle_color)
        painter.end()
