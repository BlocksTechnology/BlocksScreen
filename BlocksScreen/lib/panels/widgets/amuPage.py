from PyQt6 import QtCore, QtGui, QtWidgets
import typing
from lib.utils.icon_button import IconButton
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_linedit import BlocksCustomLinEdit

from devices.amu.models import GateInfo, GateStatus


from lib.panels.widgets.basePopup import BasePopup


# ──────────────────────────────────────────────────────────────────────────────
# Spool button
# ──────────────────────────────────────────────────────────────────────────────
class Spoll_button(QtWidgets.QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QtGui.QColor(0, 0, 0)
        self.status = GateStatus.UNKNOWN
        self.slot_id = ""
        self.setCheckable(True)
        self.setMinimumSize(100, 100)
        self._icon = QtGui.QPixmap("/home/levi/Downloads/loaded_spool.svg")
        self._unloaded_icon = QtGui.QPixmap("/home/levi/Downloads/spool.svg")

    def setColor(self, qc: QtGui.QColor):
        self.color = qc
        self.update()

    def setStatus(self, s: GateStatus):
        self.status = s
        self.repaint()

    def setGateId(self, i: int):
        self.slot_id = i
        self.update()

    def setMaterial(self, mat: str):
        self.material = mat
        self.update()

    def setWeight(self, w: int):
        self.weight = w
        self.update()

    def update_entry(
        self, color: QtGui.QColor, slot_id: int, status: GateStatus, material: str
    ):
        self.setColor(color)
        self.setGateId(slot_id)
        self.setStatus(status)
        self.setMaterial(material)
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
            "Gate " + str(self.slot_id),
        )
        if not self.isChecked():
            white.setAlpha(130)
            color.setAlpha(130)

        rect = self.rect().adjusted(1, 1, -1, -1)
        rect.setY(int(rect.height() - rect.height() * 0.15))
        painter.fillRect(rect, color)

        pen = QtGui.QPen(white)
        pen.setWidth(2)
        painter.setPen(pen)
        rect = self.rect().adjusted(1, 1, -1, -1)
        rect.setY(int(rect.height() - rect.height() * 0.15))
        painter.drawRect(rect)

        # Draw icon centered
        icon_size = 65
        icon = (
            self._icon
            if self.status in [GateStatus.AVAILABLE, GateStatus.AVAILABLE_FROM_BUFFER]
            else self._unloaded_icon
        )
        scaled = icon.scaled(
            icon_size,
            icon_size,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        x = (self.width() - scaled.width()) // 2
        y = int((self.height() - scaled.height()) // 1.1)

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
        slot_id: int,
        material: str = "PLA",
        status: GateStatus = GateStatus.UNKNOWN,
    ):
        if any(btn.slot_id == slot_id for btn in self.buttons):
            self.buttons[int(slot_id)].update_entry(color, slot_id, status, material)
            self.update()
            return
        btn = Spoll_button()
        btn.setColor(color)
        btn.setGateId(slot_id)
        btn.setStatus(status)
        btn.setMaterial(material)
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

        if len(self.button_group.buttons()) <= 4:
            self.left_arrow.hide()
            self.right_arrow.hide()
        else:
            self.left_arrow.show()
            self.right_arrow.show()

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
    loadRequested = QtCore.pyqtSignal()
    unloadRequested = QtCore.pyqtSignal()
    ejectRequested = QtCore.pyqtSignal()
    checkRequested = QtCore.pyqtSignal()

    request_keypad = QtCore.pyqtSignal(
        "PyQt_PyObject", name="request-keyboard"
    )  # value, slot index, caller widget

    def __init__(self, amu_manager, parent=None):
        super().__init__(parent)
        self.amu_manager = amu_manager
        self._slot_index = -1
        self.FStatus = "Unknown"
        self._build_ui()

    def _build_ui(self):
        root = QtWidgets.QHBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(20)

        # ── Color swatch ──
        self._swatch = QtWidgets.QLabel()
        self._swatch.setFixedSize(52, 52)
        self._swatch.setStyleSheet("border-radius: 2px; background: #222;")
        root.addWidget(self._swatch, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)

        # ── Info grid ──
        grid_widget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(grid_widget)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(2)

        font = QtGui.QFont()
        font.setPointSize(12)

        def make_key(text):
            l = QtWidgets.QLabel(text)
            l.setStyleSheet("color: rgba(255,255,255,100);")
            l.setFont(font)
            return l

        def make_val(text="—", edit: bool = True, type: str = "keypad"):
            """Make either an editable line edit or a static label, depending on the *edit* flag. The *type* arg determines the signal emitted on edit (numpad vs qwerty).

            Args:
                text (str, optional): _description_. Defaults to "—".
                edit (bool, optional): _description_. Defaults to True.
                type (str, optional): type of the input field gets ignored if edit is False. Defaults to "keypad".

            Returns:
                _type_: retuns label or line edit widget depending on the edit flag.
            """

            if edit:
                l = BlocksCustomLinEdit(self)
                l.setText(text)
                l.setFont(font)
                if type == "keypad":
                    l.clicked.connect(lambda: self.request_keypad.emit(l))
                # elif type == "qwerty":
                #     l.editingFinished.connect(lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(l.text(), self._slot_index, l, 0, 0))
            else:
                l = QtWidgets.QLabel(text)
                l.setStyleSheet("color: rgb(255,255,255);")
                l.setFont(font)
            return l

        self._lbl_slot = make_val(edit=False)
        self._lbl_status = make_val(edit=False)
        self._lbl_color = make_val()
        self._lbl_mat = make_val()
        self._lbl_weight = make_val()

        rows = [
            ("Slot", self._lbl_slot, None),
            ("Status", self._lbl_status, None),
            ("Color", self._lbl_color, "keypad"),
            ("Material", self._lbl_mat, "keypad"),
            ("Weight", self._lbl_weight, "numpad"),
        ]
        for i, (key, val, _) in enumerate(rows):
            grid.addWidget(make_key(key), i, 0)
            grid.addWidget(val, i, 1)

        root.addWidget(grid_widget, 1)

        # ── Divider ──
        div = QtWidgets.QFrame()
        div.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        div.setStyleSheet("color: white;")
        root.addWidget(div)

        # ── Operation buttons ──
        btn_col = QtWidgets.QVBoxLayout()
        btn_col.setSpacing(6)

        font = QtGui.QFont()
        font.setPointSize(12)

        self._btn_load = BlocksCustomButton(self)
        self._btn_load.setText("Load")
        self._btn_load.setFixedSize(160, 60)
        self._btn_load.setFont(font)
        self._btn_load.setPixmap(
            QtGui.QPixmap(":/filament_related/media/btn_icons/load_filament.svg")
        )
        self._btn_unload = BlocksCustomButton(self)
        self._btn_unload.setText("Unload")
        self._btn_unload.setFont(font)
        self._btn_unload.setPixmap(
            QtGui.QPixmap(":/filament_related/media/btn_icons/unload_filament.svg")
        )
        self._btn_unload.setFixedSize(160, 60)
        self._btn_purge = BlocksCustomButton(self)
        self._btn_purge.setText("Eject")
        self._btn_purge.setFont(font)
        self._btn_purge.setPixmap(
            QtGui.QPixmap(":/filament_related/media/btn_icons/eject.svg")
        )
        self._btn_purge.setFixedSize(160, 60)
        self._btn_cut = BlocksCustomButton(self)
        self._btn_cut.setPixmap(QtGui.QPixmap(":/load_icons/media/btn_icons/cut.svg"))
        self._btn_cut.setText("Check\nGates")
        self._btn_cut.setFont(font)
        self._btn_cut.setFixedSize(160, 60)

        self._btn_load.clicked.connect(lambda: self.loadRequested.emit())
        self._btn_unload.clicked.connect(lambda: self.unloadRequested.emit())
        self._btn_purge.clicked.connect(lambda: self.ejectRequested.emit())
        self._btn_cut.clicked.connect(lambda: self.checkRequested.emit())

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

    def setFilamentStatus(self, mmu_state):
        self.FStatus = mmu_state.filament
        self.Gate = mmu_state.gate

    def update_for_slot(self, index: int, btn: Spoll_button):
        self._slot_index = index
        color = btn.color
        status = btn.status
        material = btn.material

        # Swatch
        self._swatch.setStyleSheet(
            f"border-radius: 12px;"
            f"background: rgb({color.red()},{color.green()},{color.blue()});"
            f"border: 2px solid white;"
        )

        self._lbl_slot.setText(str(btn.slot_id))

        status_map = {
            GateStatus.AVAILABLE.value: (
                "<span style='color:#2ec4a0'>● LOADED</span>",
                False,
                True,
                True,
                True,
            ),
            GateStatus.AVAILABLE_FROM_BUFFER.value: (  # Add this
                "<span style='color:#2ec4a0'>● LOADED (BUFFER)</span>",  # Or whatever text you want
                False,
                True,
                True,
                True,
            ),
            GateStatus.EMPTY.value: (
                "<span style='color:#e8445a'>○ EMPTY</span>",
                True,
                True,
                True,
                True,
            ),
            GateStatus.UNKNOWN.value: (
                "<span style='color:#aaa'>? UNKNOWN</span>",
                True,
                True,
                False,
                True,
            ),
        }
        text, en_load, en_unload, en_purge, en_cut = status_map[status.value]

        if self.FStatus == "Unloaded" and self._slot_index == self.Gate:
            text = "<span style='color:#e8445a'>○ UNLOADED</span>"
            en_load = True
            en_unload = False
        elif self.FStatus == "Loaded" and self._slot_index == self.Gate:
            text = "<span style='color:#2ec4a0'>● LOADED</span>"
            en_load = False
            en_unload = True

        self._lbl_status.setText(text)
        self._lbl_mat.setText(material if material else "—")
        self._btn_load.setEnabled(en_load)
        self._btn_unload.setEnabled(en_unload)
        self._btn_purge.setEnabled(en_purge)
        self._btn_cut.setEnabled(en_cut)

        r, g, b = color.red(), color.green(), color.blue()
        self._lbl_color.setText(f"#{r:02X}{g:02X}{b:02X}")


from devices.amu import AMUManager
from devices.amu.models import (
    GateStatus,
)
from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard


# ──────────────────────────────────────────────────────────────────────────────
# AMU widget — carousel + info panel stacked
# ──────────────────────────────────────────────────────────────────────────────
class AMUpage(QtWidgets.QStackedWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )

    def __init__(self, amu_manager, parent=None):
        super().__init__(parent)
        self.amu_manager: AMUManager = amu_manager
        self.amu_manager.mmu_state_changed.connect(self.on_mmu_state_changed)
        self._build_ui()
        self.current_index = -1
        self.info_panel._lbl_color.editingFinished.connect(
            lambda: self.amu_manager.set_gate_color(
                self.current_index,
                self.info_panel._lbl_color.text().removeprefix("#") + "FF",
            )
        )
        self.info_panel._lbl_mat.editingFinished.connect(
            lambda: self.amu_manager.set_gate_material(
                self.current_index, self.info_panel._lbl_mat.text()
            )
        )
        # self.info_panel._lbl_weight.editingFinished.connect(lambda:self.amu_manager.set_gate_weight(self.current_index, int(self.info_panel._lbl_weight.text())))

        self._qwerty = CustomQwertyKeyboard(self)
        self._qwerty.hide()

        self._qwerty.numpad_back_btn.clicked.connect(self._on_qwerty_go_back)
        self._qwerty.value_selected.connect(self._on_qwerty_value_selected)

        self.info_panel.request_keypad.connect(self._on_show_keyboard)
        self._previous_gate_states: dict[int, bool] = {}

        self.info_panel.loadRequested.connect(self.amu_manager.load_gate)
        self.info_panel.unloadRequested.connect(self.amu_manager.unload)
        self.info_panel.ejectRequested.connect(self.amu_manager.eject_gate)
        self.info_panel.checkRequested.connect(self.amu_manager.check_gate)

        self.amu_manager.pre_gate_changed.connect(self.on_pre_gate)
        self.carousel.selectionChanged.connect(self._select_gate)


        self._setup_popup()

    def _setup_popup(self):
        self.popup = BasePopup(self, False, False)
        self.popup_wiget = self._popup_widget_ui()
        self.popup.add_widget(self.popup_wiget)

    def on_mmu_state_changed(self, mmu_state):
        self.status = mmu_state
        if not self._previous_gate_states:
            for gate_info in mmu_state.gates:
                self._previous_gate_states[gate_info.index] = gate_info.status in [
                    GateStatus.AVAILABLE,
                    GateStatus.AVAILABLE_FROM_BUFFER,
                ]

        for i in range(len(mmu_state.gates)):
            gate_info = mmu_state.gates[i]
            self.addSpool(gate_info)
            self.update()
        self._on_selection(mmu_state.gate)
        self.info_panel.setFilamentStatus(mmu_state)

    def on_pre_gate(self, gate_index: int, detected: bool):
        """Only show popup when gate transitions from False to True."""
        previous_state = self._previous_gate_states.get(gate_index)
        self._previous_gate_states[gate_index] = detected
        if previous_state is False and detected is True:
            self.popup.show()

    def addSpool(
        self,
        gate_info: GateInfo,
    ):
        self.carousel.addSpool(
            QtGui.QColor("#" + str(gate_info.color)[:-2]),
            gate_info.index,
            gate_info.material,
            gate_info.status,
        )

    def _select_gate(self, idx: int):
        self.carousel.selectIndex(self.current_index)
        self.amu_manager.select_tool(idx)


    def _on_selection(self, idx: int):
        # self.amu_manager.sele
        btn = self.carousel.buttons[idx]
        self.current_index = idx
        self.info_panel.update_for_slot(idx, btn)
        self.carousel.selectIndex(idx)

    @QtCore.pyqtSlot("PyQt_PyObject", name="request-keyboard")
    def _on_show_keyboard(self, field: QtWidgets.QLineEdit) -> None:
        """Show the QWERTY keyboard panel, saving the originating panel and input field."""
        self._current_field = field
        self._qwerty.set_value(field.text())
        field.clearFocus()  # ← Add this
        self._qwerty.show()

    def _on_qwerty_go_back(self) -> None:
        """Hide the keyboard and return to the previously active panel."""
        self._qwerty.hide()

    def _on_qwerty_value_selected(self, value: str) -> None:
        """Apply the keyboard-selected *value* to the previously focused input field."""
        self._qwerty.hide()
        if self._current_field:
            self._current_field.setText(value)
            self._current_field.editingFinished.emit()

    def _popup_widget_ui(self):
        widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(widget)

        font = QtGui.QFont()
        font.setPointSize(20)

        label = QtWidgets.QLabel("Filament Detected")
        label.setFont(font)
        label.setStyleSheet("color:white")
        label.setMinimumSize(0, 60)
        layout.addWidget(label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        grid_widget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(grid_widget)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(2)

        font = QtGui.QFont()
        font.setPointSize(14)

        def make_key(text):
            l = QtWidgets.QLabel(text)
            l.setStyleSheet("color: rgb(255,255,255);")
            l.setFont(font)
            return l

        def make_val(edit: bool = True, type: str = "keypad"):
            """Make either an editable line edit or a static label, depending on the *edit* flag. The *type* arg determines the signal emitted on edit (numpad vs qwerty).

            Args:
                text (str, optional): _description_. Defaults to "—".
                edit (bool, optional): _description_. Defaults to True.
                type (str, optional): type of the input field gets ignored if edit is False. Defaults to "keypad".

            Returns:
                _type_: retuns label or line edit widget depending on the edit flag.
            """

            if edit:
                l = BlocksCustomLinEdit(self)
                l.setFont(font)
                l.setMinimumSize(0, 60)
            else:
                l = QtWidgets.QLabel()
                l.setStyleSheet("color: rgb(255,255,255);")
                l.setFont(font)
            return l

        self._lbl_color = make_val()
        self._lbl_mat = make_val()
        self._lbl_weight = make_val()

        rows = [
            ("Color", self._lbl_color, "keypad"),
            ("Material", self._lbl_mat, "keypad"),
            ("Weight", self._lbl_weight, "numpad"),
        ]
        for i, (key, val, _) in enumerate(rows):
            grid.addWidget(make_key(key), i, 0)
            grid.addWidget(val, i, 1)

        layout.addWidget(grid_widget, 1)

        self._lbl_color.clicked.connect(lambda: self._on_show_keyboard(self._lbl_color))
        self._lbl_mat.clicked.connect(lambda: self._on_show_keyboard(self._lbl_mat))
        self._lbl_weight.clicked.connect(
            lambda: self._on_show_keyboard(self._lbl_weight)
        )

        widget.setLayout(layout)
        return widget

    def _build_ui(self):
        self.setMinimumSize(720, 420)
        self.setObjectName("fans_page")
        widget = QtWidgets.QWidget(parent=self)
        widget.setMinimumSize(720, 420)
        self.setObjectName("temperature_page")
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        widget.setObjectName("filament_control_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.filament_page_header_layout = QtWidgets.QHBoxLayout()
        self.filament_page_header_layout.setObjectName("filament_page_header_layout")

        self.spacerItem1 = QtWidgets.QSpacerItem(
            60,
            0,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.filament_page_header_layout.addItem(self.spacerItem1)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)

        self.filament_page_header_title = QtWidgets.QLabel(parent=self)
        self.filament_page_header_title.setSizePolicy(sizePolicy)
        self.filament_page_header_title.setMinimumSize(QtCore.QSize(0, 60))
        self.filament_page_header_title.setMaximumSize(QtCore.QSize(16777215, 60))
        self.filament_page_header_title.setFont(font)
        self.filament_page_header_title.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.filament_page_header_title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.filament_page_header_title.setObjectName("filament_page_header_title")
        self.filament_page_header_layout.addWidget(
            self.filament_page_header_title,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.main_back_button = IconButton(parent=self)
        self.main_back_button.setSizePolicy(sizePolicy)
        self.main_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.main_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.main_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.main_back_button.setObjectName("main_back_button")
        self.filament_page_header_layout.addWidget(self.main_back_button)

        self.verticalLayout.addLayout(self.filament_page_header_layout)

        amu_widget = QtWidgets.QWidget(parent=self)
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

        self.carousel = SpoolCarousel(carousel_frame)
        self.carousel.setSizePolicy(sizePolicy)
        cf_layout.addWidget(self.carousel)
        root.addWidget(carousel_frame)

        # Info / operation panel
        self.info_panel = SpoolInfoPanel(parent=self, amu_manager=self.amu_manager)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.info_panel.setSizePolicy(sizePolicy)

        # self.info_panel.request_numpad[str, int, "PyQt_PyObject", int, int].connect(
        #     self.on_numpad_request
        # )
        root.addWidget(self.info_panel)
        amu_widget.setLayout(root)

        self.verticalLayout.addWidget(amu_widget)
        widget.setLayout(self.verticalLayout)
        self.addWidget(widget)

        _translate = QtCore.QCoreApplication.translate

        self.filament_page_header_title.setText(
            _translate("widget", "Filament Control")
        )
