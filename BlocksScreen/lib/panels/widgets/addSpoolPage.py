import typing

from lib.panels.widgets.basePopup import BasePopup
from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard
from lib.panels.widgets.loadWidget import LoadingOverlayWidget
from lib.panels.widgets.numpadPage import CustomNumpad
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_linedit import BlocksCustomLinEdit
from lib.utils.blocks_pixmap import BlocksPixmap, Icon
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets


class AddSpoolPage(QtWidgets.QWidget):
    request_filaments: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-filaments"
    )
    request_add_spool: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, dict, name="request-add-spool"
    )
    open_add_filament: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="open-add-filament"
    )
    accepted: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(name="accepted")
    cancelled: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(name="cancelled")
    request_numpad: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [str, int, "PyQt_PyObject"],
        [str, int, "PyQt_PyObject", int, int],
        name="request-numpad",
    )

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._selected_filament_id: int | None = None
        self._filament_id_map: dict[str, dict] = {}
        self._keyboard_field: QtWidgets.QLineEdit | None = None
        self._material_filter: str | None = None

        self._build_ui()

        self._keyboard = CustomQwertyKeyboard(self)
        self._keyboard.hide()
        self._keyboard.numpad_back_btn.clicked.connect(self._keyboard.hide)
        self._keyboard.value_selected.connect(self._on_keyboard_done)

        self._numpad = CustomNumpad(self)
        self._numpad.hide()

        self._numpad_popup = BasePopup(self, False, False)
        self._numpad_popup.add_widget(self._numpad)
        self._numpad.numpad_back_btn.clicked.connect(self._numpad_popup.hide)

        self.request_numpad[str, int, "PyQt_PyObject", int, int].connect(
            self.on_numpad_request
        )

    def reset(self) -> None:
        """Clear state and trigger a fresh filament fetch. Call before showing."""
        self._selected_filament_id = None
        self._submit_btn.setEnabled(False)
        self._location_field.clear()
        self._lot_field.clear()
        self._weight_field.clear()
        self._fil_list_view.hide()
        self._fil_load_widget.show()
        self._fil_model.clear()
        self._fil_delegate.clear()
        self.request_filaments.emit()

    def setFilter(self, material: str | None = None) -> None:
        """Set a material filter for the filament list. Call before reset()."""
        self.reset()
        self._material_filter = material

    @QtCore.pyqtSlot(dict, name="on-filaments-received")
    def on_filaments_received(self, result: dict) -> None:
        self._fil_load_widget.hide()
        self._fil_list_view.show()
        if result.get("error") is not None:
            return
        filaments = result.get("response")
        if not isinstance(filaments, list):
            return
        self._filament_id_map = {}
        self._fil_model.clear()
        self._fil_delegate.clear()
        self._fil_model.add_item(
            ListItem(
                text="+ Add Filament",
                left_icon=self._make_add_pixmap(),
                _lfontsize=14,
                height=60,
            )
        )

        for fil in filaments:
            fil_id = fil.get("id", "?")
            name = fil.get("name") or f"Filament #{fil_id}"
            material = fil.get("material") or ""
            if (
                self._material_filter
                and self._material_filter.lower() not in material.lower()
            ):
                continue
            self._fil_model.add_item(
                ListItem(
                    text=name,
                    right_text=material,
                    left_icon=self._make_color_pixmap(fil),
                    _lfontsize=14,
                    _rfontsize=12,
                    height=60,
                )
            )
            self._filament_id_map[name] = fil
            self.update()

    @staticmethod
    def _make_add_pixmap() -> QtGui.QPixmap:
        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        pen = QtGui.QPen(QtGui.QColor(160, 160, 160))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QtCore.QRectF(1, 1, 32 - 2, 32 - 2), 6, 6)
        mid = 32 // 2
        painter.drawLine(mid, 8, mid, 32 - 8)
        painter.drawLine(8, mid, 32 - 8, mid)
        painter.end()
        return pixmap

    @QtCore.pyqtSlot(dict, name="on-add-spool-result")
    def on_add_spool_result(self, result: dict) -> None:
        if result.get("error") is None:
            self.accepted.emit()

    @QtCore.pyqtSlot(ListItem, name="on-filament-selected")
    def _on_filament_selected(self, item: ListItem) -> None:
        if not item:
            return
        if item.text == "+ Add Filament":
            self.open_add_filament.emit()
            return
        filament = self._filament_id_map.get(item.text)
        if filament:
            self._selected_filament_id = filament.get("id")
            self._submit_btn.setEnabled(True)

    def _show_keyboard(
        self,
        field: QtWidgets.QLineEdit,
        prefix: str = "",
        suffix: str = "",
        pattern: str = "",
        max_char: int = 0,
    ) -> None:
        self._keyboard_field = field
        self._keyboard.setPrefix(prefix)
        self._keyboard.setSuffix(suffix)
        self._keyboard.setPattern(pattern)
        self._keyboard.set_value(field.text().strip("#"))
        self._keyboard.setMaxLength(max_char)
        self._keyboard.show()

    @QtCore.pyqtSlot(str, name="on-keyboard-done")
    def _on_keyboard_done(self, value: str) -> None:
        self._keyboard.hide()
        if self._keyboard_field is not None:
            self._keyboard_field.setText(value)
            self._keyboard_field = None

    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", name="on-numpad-request")
    @QtCore.pyqtSlot(str, int, "PyQt_PyObject", int, int, name="on-numpad-request")
    def on_numpad_request(
        self,
        name: str,
        current_value: int,
        callback,
        min_value: int = 0,
        max_value: int = 100,
    ) -> None:
        try:
            self._numpad.value_selected.disconnect()
        except TypeError:
            pass
        self._numpad.value_selected.connect(callback)
        self._numpad.set_name(name)
        self._numpad.set_value(current_value)
        self._numpad.set_min_value(min_value)
        self._numpad.set_max_value(max_value)
        self._numpad_popup.show()

    @QtCore.pyqtSlot(str, int, name="on-weight-change")
    def _on_weight_change(self, _name: str, value: int) -> None:
        self._numpad_popup.hide()
        self._weight_field.setText(str(value))

    def _on_submit(self) -> None:
        if self._selected_filament_id is None:
            return
        body: dict = {}
        loc = self._location_field.text().strip()
        lot = self._lot_field.text().strip()
        weight = self._weight_field.text().strip()
        if loc:
            body["location"] = loc
        if lot:
            body["lot_nr"] = lot
        if weight:
            try:
                body["initial_weight"] = float(weight)
            except ValueError:
                pass
        self.request_add_spool.emit(int(self._selected_filament_id), body)

    @staticmethod
    def _make_color_pixmap(filament: dict) -> QtGui.QPixmap:
        size = 32
        pixmap = QtGui.QPixmap(size, size)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        multi_hexes: str | None = filament.get("multi_color_hexes")
        color_hex: str | None = filament.get("color_hex")
        if multi_hexes:
            hexes = [h.strip() for h in multi_hexes.split(",") if h.strip()]
            if hexes:
                clip = QtGui.QPainterPath()
                clip.addRoundedRect(QtCore.QRectF(0, 0, size, size), 6, 6)
                painter.setClipPath(clip)
                stripe_w = size / len(hexes)
                for i, h in enumerate(hexes):
                    painter.fillRect(
                        QtCore.QRectF(i * stripe_w, 0, stripe_w, size),
                        QtGui.QColor(f"#{h}"),
                    )
        elif color_hex:
            painter.setBrush(QtGui.QColor(f"#{color_hex}"))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QtCore.QRectF(0, 0, size, size), 6, 6)
        else:
            painter.setPen(QtGui.QColor(180, 180, 180))
            painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(QtCore.QRectF(1, 1, size - 2, size - 2), 6, 6)
        painter.end()
        return pixmap

    def _build_ui(self) -> None:
        self.setMaximumHeight(470)

        def _f(pt: int) -> QtGui.QFont:
            font = QtGui.QFont()
            font.setPointSize(pt)
            return font

        def _key_lbl(text: str) -> QtWidgets.QLabel:
            lbl = QtWidgets.QLabel(text, self)
            lbl.setFont(_f(15))
            lbl.setStyleSheet("color: rgb(180,180,180); background: transparent;")
            lbl.setFixedHeight(30)
            return lbl

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)

        # Header
        hdr = QtWidgets.QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)
        hdr.setSpacing(0)
        blank = QtWidgets.QWidget(self)
        blank.setMaximumSize(60, 60)
        blank.setMinimumSize(60, 60)
        hdr.addWidget(blank)

        title_lbl = QtWidgets.QLabel("Add Spool", self)
        title_lbl.setFont(_f(22))
        title_lbl.setFixedHeight(60)
        title_lbl.setStyleSheet("color: white; background: transparent;")
        hdr.addWidget(title_lbl, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        back_btn = IconButton(self)
        back_btn.setFixedSize(QtCore.QSize(60, 60))
        back_btn.setFlat(True)
        back_btn.setPixmap(BlocksPixmap.get(Icon.BACK))
        back_btn.clicked.connect(self.cancelled)
        hdr.addWidget(back_btn)
        root.addLayout(hdr)

        # Body
        body = QtWidgets.QHBoxLayout()
        body.setSpacing(8)

        left_frame = BlocksCustomFrame(self)
        left_lay = QtWidgets.QVBoxLayout(left_frame)
        left_lay.setContentsMargins(4, 4, 4, 4)
        left_lay.setSpacing(4)

        left_lay.addWidget(_key_lbl("Select Filament:"))

        self._fil_list_view = QtWidgets.QListView(left_frame)
        self._fil_list_view.setMouseTracking(True)
        self._fil_list_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self._fil_list_view.setStyleSheet("background-color: transparent;")
        self._fil_list_view.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self._fil_list_view.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._fil_list_view.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._fil_list_view.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.NoSelection
        )
        self._fil_list_view.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        QtWidgets.QScroller.grabGesture(
            self._fil_list_view, QtWidgets.QScroller.ScrollerGestureType.TouchGesture
        )
        QtWidgets.QScroller.grabGesture(
            self._fil_list_view,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )

        self._fil_model = EntryListModel()
        self._fil_model.setParent(self._fil_list_view)
        self._fil_delegate = EntryDelegate()
        self._fil_list_view.setModel(self._fil_model)
        self._fil_list_view.setItemDelegate(self._fil_delegate)
        self._fil_delegate.item_selected.connect(self._on_filament_selected)

        self._fil_load_widget = LoadingOverlayWidget(
            left_frame, LoadingOverlayWidget.AnimationGIF.DEFAULT
        )
        left_lay.addWidget(self._fil_list_view, 1)
        left_lay.addWidget(self._fil_load_widget, 1)
        self._fil_list_view.hide()

        body.addWidget(left_frame, 1)

        # Right: optional spool fields
        right_frame = BlocksCustomFrame(self)
        right_lay = QtWidgets.QVBoxLayout(right_frame)
        right_lay.setContentsMargins(10, 8, 10, 8)
        right_lay.setSpacing(4)

        def _field(label: str) -> BlocksCustomLinEdit:
            right_lay.addWidget(_key_lbl(label))
            fld = BlocksCustomLinEdit(self)
            fld.setFont(_f(14))
            fld.setFixedHeight(52)
            right_lay.addWidget(fld)
            return fld

        self._location_field = _field("Location:")
        self._lot_field = _field("Lot Nr:")
        self._weight_field = _field("Initial Weight (g):")

        self._location_field.clicked.connect(
            lambda: self._show_keyboard(self._location_field)
        )
        self._lot_field.clicked.connect(lambda: self._show_keyboard(self._lot_field))
        self._weight_field.clicked.connect(
            lambda: self.request_numpad[str, int, "PyQt_PyObject", int, int].emit(
                "Weight",
                int(self._weight_field.text().strip() or 0),
                self._on_weight_change,
                0,
                9999,
            )
        )

        right_lay.addStretch(1)

        self._submit_btn = BlocksCustomButton(right_frame)
        self._submit_btn.setFixedHeight(60)
        self._submit_btn.setFont(_f(16))
        self._submit_btn.setText("Add Spool")
        self._submit_btn.setEnabled(False)
        self._submit_btn.clicked.connect(self._on_submit)
        self._submit_btn.setPixmap(BlocksPixmap.get(Icon.ADD_SPOOL))
        right_lay.addWidget(self._submit_btn)

        body.addWidget(right_frame, 1)
        root.addLayout(body, 1)
