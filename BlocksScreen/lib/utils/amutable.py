from PyQt6 import QtCore, QtGui, QtWidgets
import enum

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from lib.utils.icon_button import IconButton
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame


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
        self.color = QtGui.QColor(0, 0, 0)
        self.status = FilamentStates.UNKNOWN
        self.slot_id = ""
        self.setCheckable(True)
        self.setMinimumSize(100, 100)
        self._icon = QtGui.QPixmap("/home/levi/Downloads/WhatSie/loadicon.svg")

    def setColor(self, c: QtGui.QColor):
        self.color = c
        self.update()

    def setStatus(self, s: FilamentStates):
        self.status = s
        self.update()

    def setGateId(self, s: str):
        self.slot_id = s
        self.update()

    def paintEvent(self, e: QtGui.QPaintEvent | None) -> None:
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)


        color = QtGui.QColor(self.color)
        white = QtGui.QColor(255, 255, 255)


        pen = QtGui.QPen(white)
        pen.setWidth(2)
        painter.setPen(pen)

        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)

        _text_rect = self.rect()
        _text_rect.setTop(int(self.rect().height() / 9))

        _text_rect.setBottom(int(self.rect().height() / 4))

        _text_rect.setLeft(int(self.rect().width() - self.rect().width() * 1.6))
        _text_rect.setRight(int(self.rect().width()))

        painter.drawText(
            _text_rect,
            QtCore.Qt.TextFlag.TextShowMnemonic | QtCore.Qt.AlignmentFlag.AlignCenter,
            str(self.slot_id),
        )


        if not self.isChecked():
            white.setAlpha(130)
            color.setAlpha(130)
        

        rect = self.rect().adjusted(1, 1, -1, -1)
        rect.setY(int(rect.height()- rect.height() * 0.15))
        painter.fillRect(rect, color)


        pen = QtGui.QPen(white)
        pen.setWidth(2)
        painter.setPen(pen)
        rect = self.rect().adjusted(1, 1, -1, -1)
        rect.setY(int(rect.height()- rect.height() * 0.15))
        painter.drawRect(rect)

        # Draw icon centered
        icon_size = 80
        scaled = self._icon.scaled(
            icon_size,
            icon_size,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2

        tinted = QtGui.QPixmap(scaled.size())
        tinted.fill(QtCore.Qt.GlobalColor.transparent)
        p2 = QtGui.QPainter(tinted)
        p2.drawPixmap(0, 0, scaled)
        p2.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_SourceIn)
        p2.fillRect(tinted.rect(), white)
        p2.end()
        painter.drawPixmap(x, y, tinted)

        tinted = QtGui.QPixmap(scaled.size())
        tinted.fill(QtCore.Qt.GlobalColor.transparent)

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.end()


# ──────────────────────────────────────────────────────────────────────────────
# Operation button
# ──────────────────────────────────────────────────────────────────────────────
class OpButton(QtWidgets.QPushButton):
    def __init__(self, label: str, accent: QtGui.QColor, parent=None):
        super().__init__(label, parent)
        self._accent = accent
        self._hovered = False
        self.setFixedHeight(34)
        self.setMinimumWidth(80)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setFlat(True)

    def enterEvent(self, e):
        self._hovered = True
        self.update()

    def leaveEvent(self, e):
        self._hovered = False
        self.update()

    def paintEvent(self, _):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        r = self.rect()
        alpha = 200 if self._hovered else 120
        ac = QtGui.QColor(self._accent)
        ac.setAlpha(alpha)
        p.setPen(QtGui.QPen(ac, 1))
        fill = QtGui.QColor(self._accent)
        fill.setAlpha(40 if self._hovered else 20)
        p.setBrush(fill)
        p.drawRoundedRect(r.adjusted(1, 1, -1, -1), 6, 6)
        p.setPen(QtGui.QColor(255, 255, 255, 220 if self._hovered else 180))
        font = p.font()
        font.setPointSize(9)
        font.setBold(True)
        p.setFont(font)
        p.drawText(r, QtCore.Qt.AlignmentFlag.AlignCenter, self.text())
        p.end()


# ──────────────────────────────────────────────────────────────────────────────
# Carousel (scrollable spool row)
# ──────────────────────────────────────────────────────────────────────────────
class SpoolCarousel(QtWidgets.QWidget):
    selectionChanged = QtCore.pyqtSignal(int)  # emits selected slot index (0-based)

    VISIBLE = 4  # how many spools show at once

    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons: list[Spoll_button] = []
        self.button_group = QtWidgets.QButtonGroup(self)
        self.button_group.setExclusive(True)
        self._offset = 0  # first visible index

        self._anim_group: QtCore.QParallelAnimationGroup | None = None

        self._build_ui()

    def _build_ui(self):
        root = QtWidgets.QHBoxLayout(self)

        self.left_arrow = IconButton(self)
        self.left_arrow.setPixmap(
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/arrow_left.svg")
        )
        self.right_arrow = IconButton(self)
        self.right_arrow.setPixmap(
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/arrow_right.svg")
        )

        self.right_arrow.setFixedWidth(60)
        self.left_arrow.setFixedWidth(60)

        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        # self.right_arrow.setSizePolicy(sizePolicy)
        # self.left_arrow.setSizePolicy(sizePolicy)

        self.left_arrow.clicked.connect(self._scroll_left)
        self.right_arrow.clicked.connect(self._scroll_right)

        self._slot_area = QtWidgets.QWidget()
        self._slot_layout = QtWidgets.QHBoxLayout(self._slot_area)

        self.left_arrow.setFixedHeight(100)
        self.right_arrow.setFixedHeight(100)

        root.addWidget(self.left_arrow)
        root.addWidget(self._slot_area)
        root.addWidget(self.right_arrow)

        self._update_arrows()

    def addSpool(
        self,
        color: QtGui.QColor,
        slot_id: str,
        status: FilamentStates = FilamentStates.UNKNOWN,
    ):
        btn = Spoll_button()
        btn.setColor(color)
        btn.setGateId(slot_id)
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
        for btn in self.buttons[self._offset : end]:
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
    loadRequested = QtCore.pyqtSignal(int)
    unloadRequested = QtCore.pyqtSignal(int)
    purgeRequested = QtCore.pyqtSignal(int)
    cutRequested = QtCore.pyqtSignal(int)

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
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(4)

        def make_key(text):
            l = QtWidgets.QLabel(text)
            l.setStyleSheet("color: rgba(255,255,255,100); font-size: 10px;")
            return l

        def make_val(text="—"):
            l = QtWidgets.QLabel(text)
            l.setStyleSheet(
                "color: rgba(255,255,255,220); font-size: 10px; font-weight: bold;"
            )
            return l

        self._lbl_slot = make_val()
        self._lbl_status = make_val()
        self._lbl_color = make_val()
        self._lbl_mat = make_val("PLA")

        rows = [
            ("Slot", self._lbl_slot),
            ("Status", self._lbl_status),
            ("Color", self._lbl_color),
            ("Material", self._lbl_mat),
        ]
        for i, (key, val) in enumerate(rows):
            grid.addWidget(make_key(key), i, 0)
            grid.addWidget(val, i, 1)

        root.addWidget(grid_widget, 1)

        # ── Divider ──
        div = QtWidgets.QFrame()
        div.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        div.setStyleSheet("color: rgba(255,255,255,30);")
        root.addWidget(div)

        # ── Operation buttons ──
        btn_col = QtWidgets.QVBoxLayout()
        btn_col.setSpacing(6)

        self._btn_load = BlocksCustomButton(self)
        self._btn_load.setText("Load")
        self._btn_load.setFixedSize(160, 60)
        self._btn_load.setPixmap(
            QtGui.QPixmap(":/filament_related/media/btn_icons/load_filament.svg")
        )
        self._btn_unload = BlocksCustomButton(self)
        self._btn_unload.setText("Unload")
        self._btn_unload.setPixmap(
            QtGui.QPixmap(":/filament_related/media/btn_icons/unload_filament.svg")
        )
        self._btn_unload.setFixedSize(160, 60)
        self._btn_purge = BlocksCustomButton(self)
        self._btn_purge.setText("Eject")
        self._btn_purge.setPixmap(
            QtGui.QPixmap(":/filament_related/media/btn_icons/eject.svg")
        )
        self._btn_purge.setFixedSize(160, 60)
        self._btn_cut = BlocksCustomButton(self)
        self._btn_cut.setPixmap(QtGui.QPixmap(":/load_icons/media/btn_icons/cut.svg"))
        self._btn_cut.setText("Check Gates")
        self._btn_cut.setFixedSize(160, 60)

        self._btn_load.clicked.connect(
            lambda: self.loadRequested.emit(self._slot_index)
        )
        self._btn_unload.clicked.connect(
            lambda: self.unloadRequested.emit(self._slot_index)
        )
        self._btn_purge.clicked.connect(
            lambda: self.purgeRequested.emit(self._slot_index)
        )
        self._btn_cut.clicked.connect(lambda: self.cutRequested.emit(self._slot_index))

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
            FilamentStates.LOADED: (
                "<span style='color:#2ec4a0'>● LOADED</span>",
                True,
                True,
                True,
                True,
            ),
            FilamentStates.UNLOADED: (
                "<span style='color:#e8445a'>○ UNLOADED</span>",
                True,
                False,
                False,
                False,
            ),
            FilamentStates.UNKNOWN: (
                "<span style='color:#aaa'>? UNKNOWN</span>",
                True,
                True,
                False,
                False,
            ),
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
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )

        # Carousel inside its own BlocksCustomFrame
        carousel_frame = BlocksCustomFrame(self)
        carousel_frame.setSizePolicy(sizePolicy)

        cf_layout = QtWidgets.QVBoxLayout(carousel_frame)
        cf_layout.setContentsMargins(0, 0, 0, 0)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )

        self.carousel = SpoolCarousel(carousel_frame)
        self.carousel.selectionChanged.connect(self._on_selection)
        self.carousel.setSizePolicy(sizePolicy)
        cf_layout.addWidget(self.carousel)
        root.addWidget(carousel_frame)

        # Info / operation panel
        self.info_panel = SpoolInfoPanel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.info_panel.setSizePolicy(sizePolicy)
        root.addWidget(self.info_panel)

    def addSpool(
        self,
        color: QtGui.QColor,
        slot_id: str,
        status: FilamentStates = FilamentStates.UNKNOWN,
    ):
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
        (QtGui.QColor(10, 10, 10), "Gate 1", FilamentStates.LOADED),
        (QtGui.QColor(46, 196, 160), "Gate 2", FilamentStates.LOADED),
        (QtGui.QColor(255, 186, 8), "Gate 3", FilamentStates.UNLOADED),
        (QtGui.QColor(255, 255, 255), "Gate 4", FilamentStates.UNLOADED),
        (QtGui.QColor(232, 68, 90), "Gate 5", FilamentStates.LOADED),
        (QtGui.QColor(80, 120, 220), "Gate 6", FilamentStates.UNKNOWN),
        (QtGui.QColor(180, 80, 220), "Gate 7", FilamentStates.UNKNOWN),
        (QtGui.QColor(220, 130, 60), "Gate 8", FilamentStates.LOADED),
    ]

    amu = AMUWidget(amu_id=1, parent=window)
    for color, sid, status in spools:
        amu.addSpool(color, sid, status)
    amu.selectFirst()
    layout.addWidget(amu)

    window.setMaximumSize(710, 410)
    window.setMinimumSize(710, 410)
    window.show()
    sys.exit(app.exec())
