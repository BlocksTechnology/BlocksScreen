import typing

from devices.amu.models import GateStatus, GateInfo, FilamentPos
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_linedit import BlocksCustomLinEdit
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class Spoll_button(QtWidgets.QAbstractButton):
    _ICON_SIZE = 65
    _UNCHECKED_OPACITY = 0.51  # 130/255
    _GRID_GRAY = QtGui.QColor(120, 120, 120)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QtGui.QColor(0, 0, 0)
        self.has_color = False
        self.status = GateStatus.UNKNOWN
        self.slot_id = ""
        self.gate_info: GateInfo = None
        self.filament_pos: FilamentPos = FilamentPos.UNKNOWN
        self.setCheckable(True)
        self.setMinimumHeight(80)

        self._text_rect: QtCore.QRect | None = None
        self._strip_rect: QtCore.QRect | None = None
        self._strip_path: QtGui.QPainterPath | None = None

        white = QtGui.QColor(255, 255, 255)
        self._icons = {
            "loaded": self._make_tinted_icon(
                ":/filament_related/media/btn_icons/loaded_spool.svg", white
            ),
            "unloaded": self._make_tinted_icon(
                ":/filament_related/media/btn_icons/half_spoll.svg", white
            ),
        }

        self._label_pen = QtGui.QPen(white)
        self._label_pen.setWidth(2)

        self._label_font = QtGui.QFont()
        self._label_font.setPointSize(12)
        self._label_font.setBold(True)

        self._solid_border_pen = QtGui.QPen(self._GRID_GRAY)
        self._solid_border_pen.setWidth(2)

        self._grid_border_pen = QtGui.QPen(self._GRID_GRAY)
        self._grid_border_pen.setWidth(2)

        self._grid_dark = self._GRID_GRAY.darker(150)
        self._grid_brush = QtGui.QBrush(
            self._GRID_GRAY.lighter(140), QtCore.Qt.BrushStyle.DiagCrossPattern
        )

    def _make_tinted_icon(self, resource: str, tint: QtGui.QColor) -> QtGui.QPixmap:
        scaled = QtGui.QPixmap(resource).scaled(
            self._ICON_SIZE,
            self._ICON_SIZE,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        tinted = QtGui.QPixmap(scaled.size())
        tinted.fill(QtCore.Qt.GlobalColor.transparent)
        p = QtGui.QPainter(tinted)
        p.drawPixmap(0, 0, scaled)
        p.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_SourceIn)
        p.fillRect(tinted.rect(), tint)
        p.end()
        return tinted

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        r = QtCore.QRect(self.rect())
        r.setTop(self.height() // 9)
        r.setBottom(self.height() // 4)
        self._text_rect = r

        self._strip_rect = self.rect().adjusted(1, 1, -1, -1)
        self._strip_rect.setTop(int(self._strip_rect.height() * 0.85))

        self._strip_path = QtGui.QPainterPath()
        self._strip_path.addRoundedRect(QtCore.QRectF(self._strip_rect), 5, 5)

    def update_entry(self, gate_info: GateInfo, fm: FilamentPos):
        raw = str(gate_info.color).lstrip("#")[:6] if gate_info.color else ""
        parsed = QtGui.QColor("#" + raw) if raw else QtGui.QColor()
        has_color = parsed.isValid()
        color = parsed if has_color else QtGui.QColor(0, 0, 0)

        self.filament_pos = fm
        self.gate_info = gate_info
        self.status = gate_info.status
        self.slot_id = gate_info.index
        self.has_color = has_color
        self.color = color

        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        if self._text_rect is None or self._strip_path is None:
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)

        is_loaded = self.status in (
            GateStatus.AVAILABLE,
            GateStatus.AVAILABLE_FROM_BUFFER,
        )
        is_active = self.has_color and is_loaded

        # label
        painter.setPen(self._label_pen)
        painter.setFont(self._label_font)
        painter.drawText(
            self._text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, f"Gate {self.slot_id}"
        )

        if not self.isChecked():
            painter.setOpacity(self._UNCHECKED_OPACITY)

        if is_active:
            painter.fillPath(self._strip_path, self.color)
            painter.setPen(self._solid_border_pen)
        else:
            painter.fillPath(self._strip_path, self._grid_dark)
            painter.fillPath(self._strip_path, self._grid_brush)
            painter.setPen(self._grid_border_pen)

        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.drawPath(self._strip_path)

        if is_loaded:
            icon = self._icons["loaded"]
        else:
            icon = self._icons["unloaded"]

        x = (self.width() - icon.width()) // 2
        y = int((self.height() - icon.height()) // 1.1)
        painter.drawPixmap(x, y, icon)

        painter.end()


class SpoolCarousel(QtWidgets.QWidget):
    selectionChanged: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(int)
    VISIBLE = 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons: list[Spoll_button] = []
        self._by_id: dict[typing.Any, Spoll_button] = {}
        self.button_group = QtWidgets.QButtonGroup(self)
        self.button_group.setExclusive(True)
        self._offset = 0  # first visible index

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

        self.right_arrow.setFixedSize(60, 100)
        self.left_arrow.setFixedSize(60, 100)

        self.left_arrow.clicked.connect(self._scroll_left)
        self.right_arrow.clicked.connect(self._scroll_right)

        self._slot_area = QtWidgets.QWidget(self)
        self._slot_layout = QtWidgets.QHBoxLayout(self._slot_area)
        self._slot_layout.setContentsMargins(0, 0, 0, 0)

        root.addWidget(self.left_arrow)
        root.addWidget(self._slot_area)
        root.addWidget(self.right_arrow)

        self._update_arrows()

    def addSpool(self, gate_info: GateInfo, fm: FilamentPos):
        """Adds or updates a spool button in the carousel"""
        existing = self._by_id.get(gate_info.index)
        if existing is not None:
            existing.update_entry(gate_info, fm)
            return

        btn = Spoll_button()
        btn.setMaximumHeight(80)
        btn.update_entry(gate_info, fm)
        btn.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        self.button_group.addButton(btn, len(self.buttons))
        btn.clicked.connect(lambda checked, b=btn: self._on_btn_clicked(b))
        self.buttons.append(btn)
        self._by_id[gate_info.index] = btn
        self._slot_layout.addWidget(btn)
        self._refresh_visible()

    def _on_btn_clicked(self, btn: Spoll_button):
        idx = self.buttons.index(btn)
        self.selectionChanged.emit(idx)

    def _refresh_visible(self):
        end = self._offset + self.VISIBLE
        for i, btn in enumerate(self.buttons):
            btn.setVisible(self._offset <= i < end)

        multi = len(self.buttons) > self.VISIBLE
        self.left_arrow.setVisible(multi)
        self.right_arrow.setVisible(multi)

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
        """returns the index of the currently selected button, or -1 if none is selected"""
        btn = self.button_group.checkedButton()
        if btn:
            return self.buttons.index(btn)
        return -1

    def selectIndex(self, idx: int):
        """select a button by index

        Args:
            idx (int): the index of the button to select
        """
        if 0 <= idx < len(self.buttons):
            self.buttons[idx].setChecked(True)
            if idx < self._offset:
                self._offset = idx
                self._refresh_visible()
            elif idx >= self._offset + self.VISIBLE:
                self._offset = idx - self.VISIBLE + 1
                self._refresh_visible()


class SpoolInfoPanel(QtWidgets.QWidget):
    loadRequested: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal()
    unloadRequested: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal()
    ejectRequested: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal()
    checkRequested: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal()
    request_keypad = QtCore.pyqtSignal(
        "PyQt_PyObject", str, str, str, int, name="request-keyboard"
    )  # value, slot index, caller widget
    _STATUS_TEXT: dict[GateStatus, str] = {
        GateStatus.AVAILABLE: "<span style='color:#2ec4a0'>● PRE-LOADED</span>",
        GateStatus.AVAILABLE_FROM_BUFFER: "<span style='color:#2ec4a0'>● PRE-LOADED</span>",
        GateStatus.EMPTY: "<span style='color:#e8445a'>○ EMPTY</span>",
    }
    _UNKNOWN_TEXT = "<span style='color:#aaa'>? UNKNOWN</span>"
    _LOADED_TEXT = "<span style='color:#2ec4a0'>● LOADED</span>"
    _STUCK_TEXT = "<span style='color:#f5a623'>⚠ Filament MID-PATH ⚠</span>"

    def __init__(self, amu_manager, parent=None):
        super().__init__(parent)
        self.amu_manager = amu_manager
        self._slot_index = -1
        self.Gate = -1
        self._build_ui()

    def _build_ui(self):
        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(20)

        font = QtGui.QFont()
        font.setPointSize(12)

        cap_font = QtGui.QFont()
        cap_font.setPointSize(10)

        title_font = QtGui.QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)

        info_col = QtWidgets.QVBoxLayout()
        info_col.setContentsMargins(0, 0, 0, 0)
        info_col.setSpacing(12)

        # header: swatch | gate name / status
        header = QtWidgets.QHBoxLayout()
        header.setSpacing(12)

        self._swatch = QtWidgets.QLabel()
        self._swatch.setFixedSize(52, 52)
        header.addWidget(self._swatch, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)

        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(0)

        self._lbl_gate = QtWidgets.QLabel("Gate —")
        self._lbl_gate.setFont(title_font)
        self._lbl_gate.setStyleSheet("color: rgb(255,255,255);")

        self._lbl_status = QtWidgets.QLabel()
        self._lbl_status.setFont(font)

        title_col.addWidget(self._lbl_gate)
        title_col.addWidget(self._lbl_status)
        header.addLayout(title_col, 1)

        info_col.addLayout(header)

        def _make_val(text="—"):
            lbl = BlocksCustomLinEdit(self)
            lbl.setFixedHeight(40)
            lbl.setText(text)
            lbl.setFont(font)
            return lbl

        self._lbl_temp = _make_val()
        self._lbl_color = _make_val()
        self._lbl_mat = _make_val()
        self._lbl_weight = _make_val()

        self._lbl_color.clicked.connect(
            lambda: self.request_keypad["PyQt_PyObject", str, str, str, int].emit(
                self._lbl_color, "#", "", "", 6
            )
        )
        self._lbl_mat.clicked.connect(
            lambda: self.request_keypad["PyQt_PyObject", str, str, str, int].emit(
                self._lbl_mat, "", "", "", 0
            )
        )

        def _make_field(caption: str, widget) -> QtWidgets.QVBoxLayout:
            box = QtWidgets.QVBoxLayout()
            box.setSpacing(2)
            lbl = QtWidgets.QLabel(caption)
            lbl.setFont(cap_font)
            lbl.setStyleSheet("color: rgba(255,255,255,100);")
            box.addWidget(lbl)
            box.addWidget(widget)
            return box

        fields = QtWidgets.QGridLayout()
        fields.setContentsMargins(0, 0, 0, 0)
        fields.setHorizontalSpacing(10)
        fields.setVerticalSpacing(8)
        fields.addLayout(_make_field("Temperature", self._lbl_temp), 0, 0)
        fields.addLayout(_make_field("Material", self._lbl_mat), 0, 1)
        fields.addLayout(_make_field("Color", self._lbl_color), 1, 0)
        fields.addLayout(_make_field("Weight", self._lbl_weight), 1, 1)

        info_col.addLayout(fields)
        info_col.addStretch(1)

        # fixed width so status text can never push the divider/buttons around
        info_widget = QtWidgets.QWidget()
        info_widget.setLayout(info_col)
        info_widget.setFixedWidth(300)
        root.addWidget(info_widget)
        root.addStretch(1)

        div = QtWidgets.QFrame()
        div.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        div.setStyleSheet("color: white;")
        root.addWidget(div)

        def _make_btn(text: str, icon_path: str, signal) -> BlocksCustomButton:
            btn = BlocksCustomButton(self)
            btn.setText(text)
            btn.setFont(font)
            btn.setPixmap(QtGui.QPixmap(icon_path))
            btn.setFixedSize(150, 70)
            btn.clicked.connect(signal.emit)
            return btn

        self._btn_load = _make_btn(
            "Load",
            ":/filament_related/media/btn_icons/load_filament.svg",
            self.loadRequested,
        )
        self._btn_unload = _make_btn(
            "Unload",
            ":/filament_related/media/btn_icons/unload_filament.svg",
            self.unloadRequested,
        )
        self._btn_purge = _make_btn(
            "Eject",
            ":/filament_related/media/btn_icons/eject.svg",
            self.ejectRequested,
        )
        self._btn_cut = _make_btn(
            "Check\nGate",
            ":/filament_related/media/btn_icons/check gate 1.svg",
            self.checkRequested,
        )

        btn_grid = QtWidgets.QGridLayout()
        btn_grid.setSpacing(8)
        btn_grid.addWidget(self._btn_load, 0, 0)
        btn_grid.addWidget(self._btn_unload, 0, 1)
        btn_grid.addWidget(self._btn_purge, 1, 0)
        btn_grid.addWidget(self._btn_cut, 1, 1)
        root.addLayout(btn_grid)

    def setFilamentStatus(self, mmu_state):
        """Updates the active gate index from the mmu state."""
        self.Gate = mmu_state.gate

    @staticmethod
    def _button_states_for_status(status: GateStatus):
        """Base (load, unload, purge, cut) enabled-states from gate status alone."""
        match status:
            case GateStatus.AVAILABLE | GateStatus.AVAILABLE_FROM_BUFFER:
                return True, False, True, True
            case GateStatus.EMPTY:
                return False, False, True, True
            case _:  # GateStatus.UNKNOWN
                return True, True, False, True

    def update_for_slot(self, index: int, btn: Spoll_button) -> None:
        """Update the detail panel and action buttons for the selected gate slot.

        Args:
            index: The index of the selected button/gate.
            btn: The selected button, carrying a GateInfo snapshot and
                FilamentPos for that gate.
        """
        self._slot_index = index
        color = btn.color
        r, g, b = color.red(), color.green(), color.blue()

        self._lbl_gate.setText(f"Gate {btn.slot_id}")

        if btn.has_color:
            self._swatch.setText("")
            self._swatch.setStyleSheet(
                f"border-radius: 12px;background: rgb({r},{g},{b});border: 2px solid white"
            )
        else:
            self._swatch.setText("✕")
            self._swatch.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self._swatch.setStyleSheet(
                "border-radius: 12px;"
                "background: rgb(40,40,40);"
                "border: 2px dashed rgba(255,255,255,80);"
                "color: #e8445a;"
                "font-size: 28px; font-weight: bold;"
            )

        gate_info = btn.gate_info
        status = gate_info.status if gate_info is not None else GateStatus.UNKNOWN
        en_load, en_unload, en_purge, en_cut = self._button_states_for_status(status)
        text = self._STATUS_TEXT.get(status, self._UNKNOWN_TEXT)

        is_active_gate = index == self.Gate
        filament_pos = btn.filament_pos

        if filament_pos == FilamentPos.UNLOADED:
            en_unload = False
        else:
            en_unload = True
            en_load = False

            if is_active_gate:
                en_purge = False
                if filament_pos == FilamentPos.LOADED:
                    text = self._LOADED_TEXT
                else:
                    text = self._STUCK_TEXT

        spool_id = gate_info.spool_id if gate_info is not None else -1
        if spool_id != -1:
            text += (
                "<span style='color:rgba(255,255,255,110)'>"
                f" · Spoll ID {spool_id}</span>"
            )

        # fields are read-only while the gate is bound to a spoolman spool
        editable = (
            gate_info is not None and spool_id == -1 and status != GateStatus.EMPTY
        )
        for w in (self._lbl_temp, self._lbl_color, self._lbl_mat, self._lbl_weight):
            w.setEnabled(editable)

        self._lbl_status.setText(text)
        self._lbl_temp.setText(
            f"{gate_info.temperature}º"
            if gate_info
            and gate_info.temperature is not None
            and gate_info.temperature != -1
            else "—"
        )

        self._lbl_weight.setText(
            f"{gate_info.weight_g}" if gate_info and gate_info.weight_g else "—"
        )
        self._lbl_mat.setText(
            gate_info.material if gate_info and gate_info.material else "—"
        )
        self._lbl_color.setText(
            f"#{r:02X}{g:02X}{b:02X}" if gate_info and gate_info.color else "—"
        )

        self._btn_load.setEnabled(en_load)
        self._btn_unload.setEnabled(en_unload)
        self._btn_purge.setEnabled(en_purge)
        self._btn_cut.setEnabled(en_cut)
        self.update()
