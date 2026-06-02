import typing

from devices.amu.models import GateStatus
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_linedit import BlocksCustomLinEdit
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


# ──────────────────────────────────────────────────────────────────────────────
# Spool button
# ──────────────────────────────────────────────────────────────────────────────
class Spoll_button(QtWidgets.QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QtGui.QColor(0, 0, 0)
        self.status = GateStatus.UNKNOWN
        self.slot_id = ""
        self.temp = 0
        self.material = ""
        self.weight = 0
        self.setCheckable(True)
        self.setMinimumHeight(100)
        self._icon = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/loaded_spool.svg"
        )
        self._unloaded_icon = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/half_spoll.svg"
        )

    def setColor(self, qc: QtGui.QColor):
        """sets button color

        Args:
            qc (QtGui.QColor): a Qcolor representing filament color
        """
        self.color = qc
        self.update()

    def setStatus(self, s: GateStatus):
        """sets button status

        Args:
            s (GateStatus): a GateStatus representing the gate status
        """
        self.status = s
        self.update()

    def setGateId(self, i: int):
        """sets button gate id

        Args:
            i (int): a integer representing the gate id
        """
        self.slot_id = i
        self.update()

    def setMaterial(self, mat: str):
        """sets button material

        Args:
            mat (str): a string representing the material
        """

        self.material = mat
        self.update()

    def setWeight(self, w: int):
        """sets gate weight

        Args:
            w (int): a integer representing the weight of the filament in grams
        """
        self.weight = w
        self.update()

    def setTemp(self, t: int):
        """sets gate temp

        Args:
            t (int): a integer representing the temperature of the filament
        """
        self.temp = t
        self.update()

    def update_entry(
        self,
        color: QtGui.QColor,
        slot_id: int,
        status: GateStatus,
        material: str,
        temp: int,
    ):
        """updates button and repaints it

        Args:
            color (QtGui.QColor): a Qcolor representing filament color
            slot_id (int): a integer representing the gate id
            status (GateStatus): a GateStatus representing the gate status
            material (str): a string representing the material
            temp (int): a integer representing the temperature of the filament
        """
        self.setColor(color)
        self.setGateId(slot_id)
        self.setStatus(status)
        self.setMaterial(material)
        self.setTemp(temp)
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering)

        self.style().drawPrimitive(
            QtWidgets.QStyle.PrimitiveElement.PE_Widget, opt, painter, self
        )

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


class SpoolCarousel(QtWidgets.QWidget):
    selectionChanged: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int
    )  # emits selected slot index (0-based)

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

        self.left_arrow.setFixedHeight(100)
        self.right_arrow.setFixedHeight(100)

        self.left_arrow.clicked.connect(self._scroll_left)
        self.right_arrow.clicked.connect(self._scroll_right)

        self._slot_area = QtWidgets.QWidget(self)
        self._slot_layout = QtWidgets.QHBoxLayout(self._slot_area)
        self._slot_layout.setContentsMargins(0, 0, 0, 0)

        root.addWidget(self.left_arrow)
        root.addWidget(self._slot_area)
        root.addWidget(self.right_arrow)

        self._update_arrows()

    def addSpool(
        self,
        color: QtGui.QColor,
        slot_id: int,
        material: str = "PLA",
        temp: int = 999,
        status: GateStatus = GateStatus.UNKNOWN,
    ):
        """Adds or updates a spool button in the carousel"""
        if any(btn.slot_id == slot_id for btn in self.buttons):
            self.buttons[int(slot_id)].update_entry(
                color, slot_id, status, material, temp
            )
            self.update()
            return
        btn = Spoll_button()
        btn.setColor(color)
        btn.setGateId(slot_id)
        btn.setStatus(status)
        btn.setMaterial(material)
        btn.setTemp(temp)
        btn.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        self.button_group.addButton(btn, len(self.buttons))
        btn.clicked.connect(lambda checked, b=btn: self._on_btn_clicked(b))
        self.buttons.append(btn)
        self._refresh_visible()

    def _on_btn_clicked(self, btn: Spoll_button):
        idx = self.buttons.index(btn)
        self.selectionChanged.emit(idx)

    def _refresh_visible(self):
        while self._slot_layout.count():
            item = self._slot_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        end = min(self._offset + self.VISIBLE, len(self.buttons))
        for btn in self.buttons[self._offset : end]:
            self._slot_layout.addWidget(btn)
            btn.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Preferred,
            )
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
        """returns the index of the currently selected button, or -1 if none is selected"""
        btn = self.button_group.checkedButton()
        if btn:
            return self.buttons.index(btn)
        return -1

    def selectIndex(self, idx: int):
        """seletect a button by index

        Args:
            idx (int): the indext of the button to select
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

        self._swatch = QtWidgets.QLabel()
        self._swatch.setFixedSize(52, 52)
        self._swatch.setStyleSheet("border-radius: 2px; background: #222;")
        root.addWidget(self._swatch, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)

        grid_widget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(grid_widget)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(2)

        font = QtGui.QFont()
        font.setPointSize(12)

        def make_key(text):
            """Helper to create a label for the left column of the info grid."""
            lbl = QtWidgets.QLabel(text)
            lbl.setStyleSheet("color: rgba(255,255,255,100);")
            lbl.setFont(font)
            return lbl

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
                lbl = BlocksCustomLinEdit(self)
                lbl.setText(text)
                lbl.setFont(font)
                # elif type == "qwerty":
                #     l.editingFinished.connect(lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(l.text(), self._slot_index, l, 0, 0))
            else:
                lbl = QtWidgets.QLabel(text)
                lbl.setStyleSheet("color: rgb(255,255,255);")
                lbl.setFont(font)
            return lbl

        self._lbl_status = make_val(edit=False)
        self._lbl_temp = make_val()
        self._lbl_color = make_val()
        self._lbl_mat = make_val()
        self._lbl_weight = make_val()

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

        rows = [
            ("Status", self._lbl_status, None),
            ("Temperature", self._lbl_temp, "numpad"),
            ("Color", self._lbl_color, "keypad"),
            ("Material", self._lbl_mat, "keypad"),
            ("Weight", self._lbl_weight, "numpad"),
        ]
        for i, (key, val, _) in enumerate(rows):
            grid.addWidget(make_key(key), i, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
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
        self._btn_load.setFixedSize(140, 60)
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
        self._btn_unload.setFixedSize(140, 60)
        self._btn_purge = BlocksCustomButton(self)
        self._btn_purge.setText("Eject")
        self._btn_purge.setFont(font)
        self._btn_purge.setPixmap(
            QtGui.QPixmap(":/filament_related/media/btn_icons/eject.svg")
        )
        self._btn_purge.setFixedSize(140, 60)
        self._btn_cut = BlocksCustomButton(self)
        self._btn_cut.setPixmap(
            QtGui.QPixmap(":/filament_related/media/btn_icons/check gate 1.svg")
        )
        self._btn_cut.setText("Check\nGates")
        self._btn_cut.setFont(font)
        self._btn_cut.setFixedSize(140, 60)

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
        """updates the filament status and gate index from the mmu state"""
        self.FStatus = mmu_state.filament
        self.Gate = mmu_state.gate

    def update_for_slot(self, index: int, btn: Spoll_button):
        """updates table based of the selected button

        Args:
            index (int): the index of the selected button
            btn (Spoll_button): the selected button
        """
        self._slot_index = index
        color = btn.color
        r, g, b = color.red(), color.green(), color.blue()

        self._swatch.setStyleSheet(
            f"border-radius: 12px;background: rgb({r},{g},{b});border: 2px solid white"
        )

        match btn.status:
            case GateStatus.AVAILABLE:
                text, en_load, en_unload, en_purge, en_cut = (
                    "<span style='color:#2ec4a0'>● PRE-LOADED</span>",
                    True,
                    False,
                    True,
                    True,
                )
            case GateStatus.AVAILABLE_FROM_BUFFER:
                text, en_load, en_unload, en_purge, en_cut = (
                    "<span style='color:#2ec4a0'>● PRE-LOADED</span>",
                    True,
                    False,
                    True,
                    True,
                )
            case GateStatus.EMPTY:
                text, en_load, en_unload, en_purge, en_cut = (
                    "<span style='color:#e8445a'>○ EMPTY</span>",
                    False,
                    False,
                    True,
                    True,
                )
            case _:
                text, en_load, en_unload, en_purge, en_cut = (
                    "<span style='color:#aaa'>? UNKNOWN</span>",
                    True,
                    True,
                    False,
                    True,
                )

        if self.FStatus == "Loaded" and self._slot_index == self.Gate:
            text = "<span style='color:#2ec4a0'>● LOADED</span>"
            en_load = False
            en_unload = True

        self._lbl_status.setText(text)
        self._lbl_temp.setText(f"{btn.temp}º")
        self._lbl_mat.setText(f"{btn.material}" if btn.material else "—")
        self._btn_load.setEnabled(en_load)
        self._btn_unload.setEnabled(en_unload)
        self._btn_purge.setEnabled(en_purge)
        self._btn_cut.setEnabled(en_cut)
        self._lbl_color.setText(f"#{r:02X}{g:02X}{b:02X}")
