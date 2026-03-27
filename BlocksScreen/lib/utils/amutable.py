from PyQt6 import QtCore, QtGui, QtWidgets
import enum
import typing

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from lib.utils.icon_button import IconButton


from lib.ui.resources.background_resources_rc import *
from lib.ui.resources.font_rc import *
from lib.ui.resources.graphic_resources_rc import *
from lib.ui.resources.icon_resources_rc import *
from lib.ui.resources.main_menu_resources_rc import *
from lib.ui.resources.system_resources_rc import *
from lib.ui.resources.top_bar_resources_rc import *

class FilamentStates(enum.Enum):
    LOADED = enum.auto()
    UNLOADED = enum.auto()
    UNKNOWN = -1


# ──────────────────────────────────────────────────────────────────────────────
# Spool button
# ──────────────────────────────────────────────────────────────────────────────
class Spoll_button(QtWidgets.QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color   = QtGui.QColor(0, 0, 0)
        self.status  = FilamentStates.UNKNOWN
        self.slot_id = ""
        self.setCheckable(True)
        self.setFixedSize(100, 100)
        self._icon = QtGui.QPixmap("/home/levi/Downloads/WhatSie/loadicon.svg")

    def setColor(self, c: QtGui.QColor):  self.color = c;    self.update()
    def setStatus(self, s: FilamentStates): self.status = s; self.update()
    def setSlotId(self, s: str):           self.slot_id = s; self.update()

    def paintEvent(self, e: QtGui.QPaintEvent | None) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        # # Selected: draw a colored border
        if self.isChecked():
            border_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
            border_pen.setWidth(2)
            painter.setPen(border_pen)
        else:
            painter.setPen(QtCore.Qt.PenStyle.NoPen)

        # Gradient background
        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(self.rect().bottomLeft()),
            QtCore.QPointF(self.rect().topLeft()),
        )

        white = QtGui.QColor(255,255,255)
        color1 = QtGui.QColor(white)
        color1.setAlpha(165)
        color2 = QtGui.QColor(white)
        color2.setAlpha(165)
        color3 = QtGui.QColor(white)
        color3.setAlpha(0)
        
        gradient.setColorAt(0.0, color1)
        gradient.setColorAt(0.1, color2)
        gradient.setColorAt(0.11, color3)
        painter.setBrush(gradient)
        painter.drawRect(self.rect())
        


        color1 = QtGui.QColor(self.color)
        color1.setAlpha(255)
        color2 = QtGui.QColor(self.color)
        color2.setAlpha(255)
        color3 = QtGui.QColor(self.color)
        color3.setAlpha(0)
        
        gradient.setColorAt(0.0, color1)
        gradient.setColorAt(0.1, color2)
        gradient.setColorAt(0.11, color3)
        painter.setBrush(gradient)
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))
        
        gradient2 = QtGui.QLinearGradient(
            QtCore.QPointF(self.rect().bottomLeft()),
            QtCore.QPointF(self.rect().topLeft()),
        )
        
        gradient2.setColorAt(0.0, color1)
        color2 = QtGui.QColor(QtGui.QColor(255,255,255))
        color2.setAlpha(255)
        gradient2.setColorAt(1, color2)

        # Draw icon centered
        icon_size = 80
        scaled = self.loadedspool.scaled(
            icon_size, icon_size,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2


        # Darken overlay when not selected

        
        tinted = QtGui.QPixmap(scaled.size())
        tinted.fill(QtCore.Qt.GlobalColor.transparent)
        p2 = QtGui.QPainter(tinted)
        p2.drawPixmap(0, 0, scaled)
        p2.setCompositionMode(
            QtGui.QPainter.CompositionMode.CompositionMode_SourceIn
        )
        p2.fillRect(tinted.rect(), gradient2)
        p2.end()
        painter.drawPixmap(x,y,tinted)


        tinted = QtGui.QPixmap(scaled.size())
        tinted.fill(QtCore.Qt.GlobalColor.transparent)
        
        p2 = QtGui.QPainter(tinted)
        p2.setCompositionMode(
            QtGui.QPainter.CompositionMode.CompositionMode_SourceIn
        )
        p2.fillRect(tinted.rect(), QtGui.QColor(255,255,255) if self.isChecked() else QtGui.QColor(0,0,0))
        p2.drawPixmap(x, y, scaled)

        p2.end()
        painter.end()

# ──────────────────────────────────────────────────────────────────────────────
# Frosted frame (reused as "table" panel)
# ──────────────────────────────────────────────────────────────────────────────
class BlocksCustomFrame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)

    def setRadius(self, radius: int):
        """Set widget frame radius"""
        self._radius = radius
        self.update()

    def setLeftLineWidth(self, width: int):
        """Set widget left line  width"""
        self._left_line_width = width
        self.update()

    def setCentered(self, centered: bool):
        """Set if text is centered or left-aligned"""
        self._is_centered = centered
        self.update()

    def setProperty(self, name: str | None, value: typing.Any) -> bool:
        if name == "text":
            self.text = value
            self.update()
            return True
        return super().setProperty(name, value)

    def paintEvent(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))



# ──────────────────────────────────────────────────────────────────────────────
# Arrow button
# ──────────────────────────────────────────────────────────────────────────────
class ArrowButton(QtWidgets.QAbstractButton):
    def __init__(self, direction: str, parent=None):
        super().__init__(parent)
        self.direction = direction   # "left" | "right"
        self.setFixedSize(60,60)
        self._hovered  = False
        self._pressed  = False
        self.setMouseTracking(True)

    def enterEvent(self, e): self._hovered = True;  self.update()
    def leaveEvent(self, e): self._hovered = False; self.update()
    def mousePressEvent(self, e):   self._pressed = True;  super().mousePressEvent(e)
    def mouseReleaseEvent(self, e): self._pressed = False; super().mouseReleaseEvent(e)

    def paintEvent(self, _):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        r = self.rect()


        # Arrow chevron
        arrow_alpha = 255 if self._hovered else 160
        p.setPen(QtGui.QPen(QtGui.QColor(255,255,255, arrow_alpha), 2,
                            QtCore.Qt.PenStyle.SolidLine,
                            QtCore.Qt.PenCapStyle.RoundCap,
                            QtCore.Qt.PenJoinStyle.RoundJoin))
        cx, cy = r.width()//2, r.height()//2
        arm = 8
        if self.direction == "left":
            p.drawLine(cx+arm//2, cy-arm, cx-arm//2, cy)
            p.drawLine(cx-arm//2, cy,     cx+arm//2, cy+arm)
        else:
            p.drawLine(cx-arm//2, cy-arm, cx+arm//2, cy)
            p.drawLine(cx+arm//2, cy,     cx-arm//2, cy+arm)
        p.end()


# ──────────────────────────────────────────────────────────────────────────────
# Operation button
# ──────────────────────────────────────────────────────────────────────────────
class OpButton(QtWidgets.QPushButton):
    def __init__(self, label: str, accent: QtGui.QColor, parent=None):
        super().__init__(label, parent)
        self._accent  = accent
        self._hovered = False
        self.setFixedHeight(34)
        self.setMinimumWidth(80)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setFlat(True)

    def enterEvent(self, e): self._hovered = True;  self.update()
    def leaveEvent(self, e): self._hovered = False; self.update()

    def paintEvent(self, _):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        r = self.rect()
        alpha = 200 if self._hovered else 120
        ac = QtGui.QColor(self._accent); ac.setAlpha(alpha)
        p.setPen(QtGui.QPen(ac, 1))
        fill = QtGui.QColor(self._accent); fill.setAlpha(40 if self._hovered else 20)
        p.setBrush(fill)
        p.drawRoundedRect(r.adjusted(1,1,-1,-1), 6, 6)
        p.setPen(QtGui.QColor(255, 255, 255, 220 if self._hovered else 180))
        font = p.font(); font.setPointSize(9); font.setBold(True)
        p.setFont(font)
        p.drawText(r, QtCore.Qt.AlignmentFlag.AlignCenter, self.text())
        p.end()


# ──────────────────────────────────────────────────────────────────────────────
# Carousel (scrollable spool row)
# ──────────────────────────────────────────────────────────────────────────────
class SpoolCarousel(QtWidgets.QWidget):
    selectionChanged = QtCore.pyqtSignal(int)   # emits selected slot index (0-based)

    VISIBLE = 4   # how many spools show at once

    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons: list[Spoll_button] = []
        self.button_group = QtWidgets.QButtonGroup(self)
        self.button_group.setExclusive(True)
        self._offset = 0   # first visible index

        self._anim_group: QtCore.QParallelAnimationGroup | None = None

        self._build_ui()

    def _build_ui(self):
        self.setFixedHeight(120)
        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(4)

        self.left_arrow = IconButton(self)
        self.left_arrow.setPixmap(QtGui.QPixmap(""))
        self.right_arrow = IconButton(self)
        self.right_arrow.setPixmap(QtGui.QPixmap(":/arrow_icons/media/btn_icons/arrow_right.svg"))

        self.right_arrow.setFixedWidth(60)
        self.left_arrow.setFixedWidth(60)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_arrow.setSizePolicy(sizePolicy)


        self.left_arrow.clicked.connect(self._scroll_left)
        self.right_arrow.clicked.connect(self._scroll_right)

        self._slot_area = QtWidgets.QWidget()
        self._slot_area.setFixedHeight(110)
        self._slot_layout = QtWidgets.QHBoxLayout(self._slot_area)

        root.addWidget(self.left_arrow)
        root.addWidget(self._slot_area, 1)
        root.addWidget(self.right_arrow)

        self._update_arrows()

    def addSpool(self, color: QtGui.QColor, slot_id: str,
                 status: FilamentStates = FilamentStates.UNKNOWN):
        btn = Spoll_button()
        btn.setColor(color)
        btn.setSlotId(slot_id)
        btn.setStatus(status)
        self.button_group.addButton(btn, len(self.buttons))
        btn.clicked.connect(lambda checked, b=btn: self._on_btn_clicked(b))
        self.buttons.append(btn)
        self._refresh_visible()

    def _on_btn_clicked(self, btn: Spoll_button):
        idx = self.buttons.index(btn)
        self.selectionChanged.emit(idx)

    def _refresh_visible(self):
        # Clear layout
        while self._slot_layout.count():
            item = self._slot_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        end = min(self._offset + self.VISIBLE, len(self.buttons))
        for btn in self.buttons[self._offset:end]:
            self._slot_layout.addWidget(btn)
            btn.show()

        # Fill empty slots with spacers so layout stays stable
        for _ in range(self.VISIBLE - (end - self._offset)):
            self._slot_layout.addStretch(1)

        self._update_arrows()

    def _scroll_left(self):
        if self._offset > 0:
            self._offset -= 1
            self._refresh_visible()

    def _scroll_right(self):
        if self._offset + self.VISIBLE < len(self.buttons):
            self._offset += 1
            self._refresh_visible()

    def _update_arrows(self):
        self.left_arrow.setEnabled(self._offset > 0)
        self.right_arrow.setEnabled(self._offset + self.VISIBLE < len(self.buttons))

    def selectedIndex(self) -> int:
        btn = self.button_group.checkedButton()
        if btn:
            return self.buttons.index(btn)
        return -1

    def selectIndex(self, idx: int):
        if 0 <= idx < len(self.buttons):
            self.buttons[idx].setChecked(True)
            # scroll so it's visible
            if idx < self._offset:
                self._offset = idx
                self._refresh_visible()
            elif idx >= self._offset + self.VISIBLE:
                self._offset = idx - self.VISIBLE + 1
                self._refresh_visible()


# ──────────────────────────────────────────────────────────────────────────────
# Info table panel (BlocksCustomFrame + detail grid + op buttons)
# ──────────────────────────────────────────────────────────────────────────────
class SpoolInfoPanel(BlocksCustomFrame):
    loadRequested   = QtCore.pyqtSignal(int)
    unloadRequested = QtCore.pyqtSignal(int)
    purgeRequested  = QtCore.pyqtSignal(int)
    cutRequested    = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._slot_index = -1
        self._build_ui()

    def _build_ui(self):
        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(20)

        # ── Color swatch ──
        self._swatch = QtWidgets.QLabel()
        self._swatch.setFixedSize(52, 52)
        self._swatch.setStyleSheet("border-radius: 26px; background: #222;")
        root.addWidget(self._swatch, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)

        # ── Info grid ──
        grid_widget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(grid_widget)
        grid.setContentsMargins(0,0,0,0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(4)

        def make_key(text):
            l = QtWidgets.QLabel(text)
            l.setStyleSheet("color: rgba(255,255,255,100); font-size: 10px;")
            return l

        def make_val(text="—"):
            l = QtWidgets.QLabel(text)
            l.setStyleSheet("color: rgba(255,255,255,220); font-size: 10px; font-weight: bold;")
            return l

        self._lbl_slot   = make_val()
        self._lbl_status = make_val()
        self._lbl_color  = make_val()
        self._lbl_mat    = make_val("PLA")

        rows = [
            ("Slot",    self._lbl_slot),
            ("Status",  self._lbl_status),
            ("Color",   self._lbl_color),
            ("Material",self._lbl_mat),
        ]
        for i, (key, val) in enumerate(rows):
            grid.addWidget(make_key(key), i, 0)
            grid.addWidget(val,           i, 1)

        root.addWidget(grid_widget, 1)

        # ── Divider ──
        div = QtWidgets.QFrame()
        div.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        div.setStyleSheet("color: rgba(255,255,255,30);")
        root.addWidget(div)

        # ── Operation buttons ──
        btn_col = QtWidgets.QVBoxLayout()
        btn_col.setSpacing(6)

        teal   = QtGui.QColor(46,  196, 160)
        pink   = QtGui.QColor(232, 68,  90 )
        yellow = QtGui.QColor(255, 186, 8  )
        grey   = QtGui.QColor(160, 160, 160)

        self._btn_load   = OpButton("⬇  LOAD",   teal,   self)
        self._btn_unload = OpButton("⬆  UNLOAD", pink,   self)
        self._btn_purge  = OpButton("↺  PURGE",  yellow, self)
        self._btn_cut    = OpButton("✂  CUT",    grey,   self)

        self._btn_load.clicked.connect(  lambda: self.loadRequested.emit(self._slot_index))
        self._btn_unload.clicked.connect(lambda: self.unloadRequested.emit(self._slot_index))
        self._btn_purge.clicked.connect( lambda: self.purgeRequested.emit(self._slot_index))
        self._btn_cut.clicked.connect(   lambda: self.cutRequested.emit(self._slot_index))

        top_row = QtWidgets.QHBoxLayout()
        top_row.setSpacing(6)
        top_row.addWidget(self._btn_load)
        top_row.addWidget(self._btn_unload)

        bot_row = QtWidgets.QHBoxLayout()
        bot_row.setSpacing(6)
        bot_row.addWidget(self._btn_purge)
        bot_row.addWidget(self._btn_cut)

        btn_col.addLayout(top_row)
        btn_col.addLayout(bot_row)
        root.addLayout(btn_col)

    def update_for_slot(self, index: int, btn: Spoll_button):
        self._slot_index = index
        color = btn.color
        status = btn.status

        # Swatch
        self._swatch.setStyleSheet(
            f"border-radius: 26px;"
            f"background: rgb({color.red()},{color.green()},{color.blue()});"
            f"border: 2px solid rgba(255,255,255,60);"
        )

        self._lbl_slot.setText(btn.slot_id)

        status_map = {
            FilamentStates.LOADED:   ("<span style='color:#2ec4a0'>● LOADED</span>",   True,  True,  True,  True),
            FilamentStates.UNLOADED: ("<span style='color:#e8445a'>○ UNLOADED</span>", True,  False, False, False),
            FilamentStates.UNKNOWN:  ("<span style='color:#aaa'>? UNKNOWN</span>",     True,  True,  False, False),
        }
        text, en_load, en_unload, en_purge, en_cut = status_map[status]
        self._lbl_status.setText(text)
        self._lbl_status.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self._btn_load.setEnabled(en_load)
        self._btn_unload.setEnabled(en_unload)
        self._btn_purge.setEnabled(en_purge)
        self._btn_cut.setEnabled(en_cut)

        r, g, b = color.red(), color.green(), color.blue()
        self._lbl_color.setText(f"#{r:02X}{g:02X}{b:02X}  ({r}, {g}, {b})")


# ──────────────────────────────────────────────────────────────────────────────
# AMU widget — carousel + info panel stacked
# ──────────────────────────────────────────────────────────────────────────────
class AMUWidget(QtWidgets.QWidget):
    def __init__(self, amu_id: int = 1, parent=None):
        super().__init__(parent)
        self.amu_id = amu_id
        self._build_ui()

    def _build_ui(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)


        # Carousel inside its own BlocksCustomFrame
        carousel_frame = BlocksCustomFrame(self)
        carousel_frame.setSizePolicy(sizePolicy)

        cf_layout = QtWidgets.QVBoxLayout(carousel_frame)
        cf_layout.setContentsMargins(0, 0, 0, 0)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)

        self.carousel = SpoolCarousel(carousel_frame)
        self.carousel.selectionChanged.connect(self._on_selection)
        self.carousel.setSizePolicy(sizePolicy)
        cf_layout.addWidget(self.carousel)
        root.addWidget(carousel_frame)

        # Info / operation panel
        self.info_panel = SpoolInfoPanel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.info_panel.setSizePolicy(sizePolicy)
        root.addWidget(self.info_panel)

    def addSpool(self, color: QtGui.QColor, slot_id: str,
                 status: FilamentStates = FilamentStates.UNKNOWN):
        self.carousel.addSpool(color, slot_id, status)

    def _on_selection(self, idx: int):
        btn = self.carousel.buttons[idx]
        self.info_panel.update_for_slot(idx, btn)

    def selectFirst(self):
        if self.carousel.buttons:
            self.carousel.selectIndex(0)
            self._on_selection(0)


# ──────────────────────────────────────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QWidget()
    window.setWindowTitle("AMU — Spool Carousel")
    window.setObjectName("mainWindow")
    window.setStyleSheet("""
        #mainWindow {
            background-image: url("/home/levi/BlocksScreen/BlocksScreen/lib/ui/resources/media/1st_background.png");
            background-repeat: no-repeat;
            background-position: center;
        }
    """)

    layout = QtWidgets.QVBoxLayout(window)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(16)

    spools = [
        (QtGui.QColor(10,  10,  10 ), "S01", FilamentStates.LOADED),
        (QtGui.QColor(46,  196, 160), "S02", FilamentStates.LOADED),
        (QtGui.QColor(255, 186, 8  ), "S03", FilamentStates.UNLOADED),
        (QtGui.QColor(255, 255, 255), "S04", FilamentStates.UNLOADED),
        (QtGui.QColor(232, 68,  90 ), "S05", FilamentStates.LOADED),
        (QtGui.QColor(80,  120, 220), "S06", FilamentStates.UNKNOWN),
        (QtGui.QColor(180, 80,  220), "S07", FilamentStates.UNKNOWN),
        (QtGui.QColor(220, 130, 60 ), "S08", FilamentStates.LOADED),
    ]


    amu = AMUWidget(amu_id=1, parent=window)
    for color, sid, status in spools:
        amu.addSpool(color, sid, status)
    amu.selectFirst()
    layout.addWidget(amu)

    window.setMaximumSize(710,410)
    window.setMinimumSize(710,410)
    window.show()
    sys.exit(app.exec())