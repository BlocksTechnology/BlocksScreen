import logging
import typing

from lib.panels.widgets.addFilamentPage import AddFilamentPage
from lib.panels.widgets.addSpoolPage import AddSpoolPage
from lib.panels.widgets.basePopup import BasePopup
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets

logger: logging.Logger = logging.getLogger(__name__)


class SpoolmanPage(QtWidgets.QWidget):
    request_spools: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-spools"
    )
    request_get_spool_id: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-get-spool-id"
    )
    request_delete_spool: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, name="request-delete-spool"
    )
    request_filaments: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-filaments"
    )
    request_add_spool: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, dict, name="request-add-spool"
    )
    request_add_filament: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="request-add-filament"
    )
    request_add_manufacturer: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="request-add-manufacturer"
    )
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._spools: list[dict] = []
        self._active_spool_id: int | None = None
        self._selected_spool: dict | None = None
        self._display_name_to_spool: dict[str, dict] = {}

        self._setupUI()
        self._setup_add_popup()
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self.main_back_button.clicked.connect(self.request_back)

        self._add_spool_page.request_filaments.connect(self.request_filaments)
        self._add_spool_page.request_add_spool.connect(self.request_add_spool)
        self._add_spool_page.open_add_filament.connect(
            lambda: self._add_stack.setCurrentIndex(1)
        )
        self._add_spool_page.accepted.connect(self._add_popup.hide)
        self._add_spool_page.accepted.connect(self._on_reload_clicked)
        self._add_spool_page.cancelled.connect(self._add_popup.hide)

        self._add_filament_page.request_add_filament.connect(self.request_add_filament)
        self._add_filament_page.request_add_manufacturer.connect(
            self.request_add_manufacturer
        )
        self._add_filament_page.accepted.connect(
            lambda: self._add_stack.setCurrentIndex(0)
        )
        self._add_filament_page.accepted.connect(self._add_spool_page.reset)
        self._add_filament_page.cancelled.connect(
            lambda: self._add_stack.setCurrentIndex(0)
        )

        self.model = EntryListModel()
        self.model.setParent(self.spool_list_widget)
        self.entry_delegate = EntryDelegate()
        self.spool_list_widget.setModel(self.model)
        self.spool_list_widget.setItemDelegate(self.entry_delegate)

        self.entry_delegate.item_selected.connect(self.on_item_clicked)
        self.reload_btn.clicked.connect(self._on_reload_clicked)
        self.delete_btn.clicked.connect(self._on_delete_clicked)

        self.confirm_popup = BasePopup(self, True, True)
        self.confirm_popup.set_message("Do you want to delete this spool")
        self.confirm_popup.accepted.connect(self._on_confirm_delete)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

    @QtCore.pyqtSlot(dict, name="on-spools-received")
    def on_spools_received(self, result: dict) -> None:
        """Handle v2 proxy response for GET /v1/spool."""
        if result.get("error") is not None:
            return
        spools = result.get("response")
        if not isinstance(spools, list):
            return
        self._spools = spools
        self._build_model_list()

    @QtCore.pyqtSlot(dict, name="on-delete-spool-result")
    def on_delete_spool_result(self, result: dict) -> None:
        """Handle v2 proxy response for DELETE /v1/spool/{id}."""
        if result.get("error") is not None:
            logger.error("Delete spool failed: %s", result["error"])
            return
        self._selected_spool = None
        self._on_reload_clicked()

    def _spool_display_name(self, spool: dict) -> str:
        spool_id = spool.get("id", "?")
        filament = spool.get("filament") or {}
        name = filament.get("name") or f"Spool #{spool_id}"
        if spool.get("archived", False):
            name = f"{name} [Archived]"
        return name

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

    @staticmethod
    def _make_color_pixmap(filament: dict) -> QtGui.QPixmap:
        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        multi_hexes: str | None = filament.get("multi_color_hexes")
        color_hex: str | None = filament.get("color_hex")

        if multi_hexes:
            hexes = [h.strip() for h in multi_hexes.split(",") if h.strip()]
            if hexes:
                clip = QtGui.QPainterPath()
                clip.addRoundedRect(QtCore.QRectF(0, 0, 32, 32), 6, 6)
                painter.setClipPath(clip)
                stripe_w = 32 / len(hexes)
                for i, h in enumerate(hexes):
                    painter.fillRect(
                        QtCore.QRectF(i * stripe_w, 0, stripe_w, 32),
                        QtGui.QColor(f"#{h}"),
                    )
        elif color_hex:
            painter.setBrush(QtGui.QColor(f"#{color_hex}"))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QtCore.QRectF(0, 0, 32, 32), 6, 6)
        else:
            painter.setPen(QtGui.QColor(180, 180, 180))
            painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(QtCore.QRectF(1, 1, 32 - 2, 32 - 2), 6, 6)

        painter.end()
        return pixmap

    def _on_reload_clicked(self) -> None:
        self.request_spools.emit()
        self.request_get_spool_id.emit()

    def _on_set_active_clicked(self) -> None:
        if self._selected_spool is None:
            return
        spool_id = self._selected_spool.get("id")
        if spool_id is not None:
            self._active_spool_id = int(spool_id)
            self._refresh_info_box()

    def _on_delete_clicked(self) -> None:
        if self._selected_spool is None:
            return
        self.confirm_popup.show()

    def _on_confirm_delete(self) -> None:
        if self._selected_spool is not None:
            spool_id = self._selected_spool.get("id")
            if spool_id is not None:
                self.request_delete_spool.emit(int(spool_id))

    def _build_model_list(self) -> None:
        self.spool_list_widget.blockSignals(True)
        self.model.clear()
        self.entry_delegate.clear()
        self._display_name_to_spool = {}

        self.model.add_item(
            ListItem(
                text=" Add Spool",
                left_icon=self._make_add_pixmap(),
                _lfontsize=14,
                height=60,
            )
        )

        for spool in self._spools:
            filament = spool.get("filament") or {}
            base_name = self._spool_display_name(spool)

            display_name = base_name
            counter = 2
            while display_name in self._display_name_to_spool:
                display_name = f"{base_name} ({counter})"
                counter += 1
            self._display_name_to_spool[display_name] = spool

            material = filament.get("material") or ""
            remaining = spool.get("remaining_weight")
            if remaining is not None:
                right_text = (
                    f"{material} • {remaining:.0f}g"
                    if material
                    else f"{remaining:.0f}g"
                )
            else:
                right_text = material

            item = ListItem(
                text=display_name,
                right_text=right_text,
                left_icon=self._make_color_pixmap(filament),
                selected=False,
                _lfontsize=14,
                _rfontsize=12,
                height=60,
            )
            self.model.add_item(item)

        self.spool_list_widget.blockSignals(False)

        if self._display_name_to_spool:
            self._no_spools_label.hide()
        else:
            self._no_spools_label.show()

    @QtCore.pyqtSlot(ListItem, name="on-item-clicked")
    def on_item_clicked(self, item: ListItem) -> None:
        """Handle when a spool item is clicked in the list."""
        if not item:
            return
        if item.text == " Add Spool":
            self._on_add_spool_clicked()
            return
        self._selected_spool = self._display_name_to_spool.get(item.text)
        self._refresh_info_box()

    def _refresh_info_box(self) -> None:
        if not self._selected_spool:
            return
        spool = self._selected_spool
        filament = spool.get("filament") or {}
        vendor = filament.get("vendor") or {}

        self.filament_name_label.setText(filament.get("name") or "—")
        self.vendor_label.setText(vendor.get("name") or "—")
        self.material_label.setText(filament.get("material") or "—")

        remaining = spool.get("remaining_weight")
        initial = spool.get("initial_weight")
        if remaining is not None and initial is not None:
            self.weight_label.setText(f"{remaining:.0f} / {initial:.0f} g")
        elif remaining is not None:
            self.weight_label.setText(f"{remaining:.0f} g")
        else:
            self.weight_label.setText("—")

        extruder = filament.get("settings_extruder_temp")
        bed = filament.get("settings_bed_temp")
        extruder_str = f"{extruder}°C" if extruder is not None else "—"
        bed_str = f"{bed}°C" if bed is not None else "—"
        self.temps_label.setText(f"{extruder_str} / {bed_str}")

        self._update_color_swatches(filament)

    def _update_color_swatches(self, filament: dict) -> None:
        """ "Update the color swatches in the info box based on the filament's color information."""
        while self.color_swatch_layout.count():
            child = self.color_swatch_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        multi_color_hexes: str | None = filament.get("multi_color_hexes")
        color_hex: str | None = filament.get("color_hex")

        if multi_color_hexes:
            for hex_val in (
                h.strip() for h in multi_color_hexes.split(",") if h.strip()
            ):
                swatch = QtWidgets.QFrame(self)
                swatch.setMinimumSize(QtCore.QSize(18, 24))
                swatch.setMaximumSize(QtCore.QSize(36, 24))
                swatch.setStyleSheet(
                    f"background-color: #{hex_val}; border-radius: 4px;"
                )
                self.color_swatch_layout.addWidget(swatch)
        elif color_hex:
            swatch = QtWidgets.QFrame(self)
            swatch.setMinimumSize(QtCore.QSize(36, 24))
            swatch.setMaximumSize(QtCore.QSize(56, 24))
            swatch.setStyleSheet(f"background-color: #{color_hex}; border-radius: 5px;")
            self.color_swatch_layout.addWidget(swatch)
        else:
            swatch = QtWidgets.QFrame(self)
            swatch.setMinimumSize(QtCore.QSize(36, 24))
            swatch.setMaximumSize(QtCore.QSize(56, 24))
            swatch.setStyleSheet(
                "background-color: transparent; border: 1px solid white; border-radius: 5px;"
            )
            self.color_swatch_layout.addWidget(swatch)

    def showEvent(self, event: QtGui.QShowEvent | None) -> None:  # noqa: N802
        """reloads spool on show"""
        self._on_reload_clicked()
        return super().showEvent(event)

    def _setupUI(self) -> None:  # noqa: N802
        self.setMaximumHeight(470)

        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)
        self.setSizePolicy(size_policy)
        self.setObjectName("spoolmanPage")
        self.setStyleSheet(
            "#spoolmanPage { background-image: url(:/background/media/1st_background.png); }"
        )

        page_layout = QtWidgets.QVBoxLayout()
        page_layout.setContentsMargins(8, 8, 8, 8)
        page_layout.setSpacing(6)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setSpacing(0)
        header_layout.setContentsMargins(0, 0, 0, 0)

        def _icon_btn(icon_path: str) -> IconButton:
            btn = IconButton(self)
            btn.setFixedSize(QtCore.QSize(60, 60))
            btn.setFlat(True)
            btn.setPixmap(QtGui.QPixmap(icon_path))
            return btn

        self.reload_btn = _icon_btn(":/ui/media/btn_icons/refresh.svg")
        header_layout.addWidget(self.reload_btn)

        title_font = QtGui.QFont()
        title_font.setPointSize(22)
        self.header_title = QtWidgets.QLabel("Spoolman", self)
        self.header_title.setFixedHeight(60)
        self.header_title.setStyleSheet("color: white;")
        self.header_title.setFont(title_font)
        self.header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.header_title)

        self.main_back_button = IconButton(parent=self)
        self.main_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.main_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.main_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.main_back_button.setObjectName("main_back_button")
        header_layout.addWidget(self.main_back_button)

        page_layout.addLayout(header_layout)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setSpacing(8)

        list_frame = BlocksCustomFrame(self)
        list_frame.setMinimumWidth(380)

        self.spool_list_widget = QtWidgets.QListView(list_frame)
        self.spool_list_widget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.spool_list_widget.setStyleSheet("background-color: transparent;")
        self.spool_list_widget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.spool_list_widget.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.spool_list_widget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.spool_list_widget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.spool_list_widget.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        QtWidgets.QScroller.grabGesture(
            self.spool_list_widget,
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )
        QtWidgets.QScroller.grabGesture(
            self.spool_list_widget,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )

        self._no_spools_label = QtWidgets.QLabel("No spools found", list_frame)
        self._no_spools_label.setWordWrap(True)
        self._no_spools_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._no_spools_label.setStyleSheet("color: gray;")
        no_spools_font = QtGui.QFont()
        no_spools_font.setPointSize(13)
        self._no_spools_label.setFont(no_spools_font)
        self._no_spools_label.hide()

        list_layout = QtWidgets.QVBoxLayout()
        list_layout.setContentsMargins(4, 4, 4, 4)
        list_layout.addWidget(self.spool_list_widget, 1)
        list_layout.addWidget(self._no_spools_label)
        list_frame.setLayout(list_layout)
        main_layout.addWidget(list_frame, 3)

        info_frame = BlocksCustomFrame()
        info_layout = QtWidgets.QVBoxLayout()
        info_layout.setContentsMargins(10, 8, 10, 6)
        info_layout.setSpacing(4)
        info_frame.setLayout(info_layout)

        key_font = QtGui.QFont()
        key_font.setPointSize(12)

        val_font = QtGui.QFont()
        val_font.setPointSize(14)

        white_palette = QtGui.QPalette()
        white_palette.setColor(
            white_palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF")
        )

        spacer = QtWidgets.QSpacerItem(
            30,
            30,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        info_layout.addItem(spacer)

        def _add_row(title_text: str) -> QtWidgets.QLabel:
            row = QtWidgets.QHBoxLayout()
            row.setSpacing(4)
            title = QtWidgets.QLabel(title_text, self)
            title.setFont(key_font)
            title.setStyleSheet("color: rgb(180,180,180); background: transparent;")
            title.setFixedHeight(32)
            title.setMinimumWidth(80)
            title.setMaximumWidth(110)
            value = QtWidgets.QLabel("—", self)
            value.setFont(val_font)
            value.setStyleSheet("color: white; background: transparent;")
            value.setFixedHeight(32)
            value.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignRight
                | QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            row.addWidget(title, 0)
            row.addWidget(value, 1)
            info_layout.addLayout(row)
            return value

        self.filament_name_label = _add_row("Filament:")
        self.vendor_label = _add_row("Vendor:")
        self.material_label = _add_row("Material:")
        self.weight_label = _add_row("Remaining:")
        self.temps_label = _add_row("Ext / Bed:")

        color_row = QtWidgets.QHBoxLayout()
        color_row.setSpacing(4)
        color_title = QtWidgets.QLabel("Color:", self)
        color_title.setFont(key_font)
        color_title.setStyleSheet("color: rgb(180,180,180); background: transparent;")
        color_title.setFixedHeight(32)
        color_title.setMinimumWidth(80)
        color_title.setMaximumWidth(110)
        color_row.addWidget(color_title, 0)
        color_row.addStretch(1)
        self.color_swatch_layout = QtWidgets.QHBoxLayout()
        self.color_swatch_layout.setSpacing(4)
        color_row.addLayout(self.color_swatch_layout)
        info_layout.addLayout(color_row)

        info_layout.addStretch(1)

        button_widget = QtWidgets.QWidget()
        normal_layout = QtWidgets.QHBoxLayout(button_widget)
        normal_layout.setContentsMargins(0, 0, 0, 0)
        normal_layout.setSpacing(8)

        self.delete_btn = IconButton(self)
        self.delete_btn.setFixedSize(QtCore.QSize(60, 60))
        self.delete_btn.setFlat(True)
        self.delete_btn.setPixmap(
            QtGui.QPixmap(":/ui/media/btn_icons/garbage-icon.svg")
        )
        normal_layout.addWidget(self.delete_btn, 0)

        info_layout.addWidget(button_widget, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(info_frame, 1)
        page_layout.addLayout(main_layout, 1)
        self.setLayout(page_layout)

    def _setup_add_popup(self) -> None:
        self._add_spool_page = AddSpoolPage(parent=self)
        self._add_filament_page = AddFilamentPage(parent=self)

        self._add_stack = QtWidgets.QStackedWidget()
        self._add_stack.addWidget(self._add_spool_page)  # index 0
        self._add_stack.addWidget(self._add_filament_page)  # index 1

        self._add_popup = BasePopup(self, False, False)
        self._add_popup.add_widget(self._add_stack)

    def _on_add_spool_clicked(self) -> None:
        self._add_stack.setCurrentIndex(0)
        self._add_spool_page.reset()
        self._add_popup.show()

    @QtCore.pyqtSlot(dict, name="on-filaments-received")
    def on_filaments_received(self, result: dict) -> None:
        """Handle v2 proxy response for GET /v1/filament."""
        self._add_spool_page.on_filaments_received(result)

    @QtCore.pyqtSlot(dict, name="on-add-spool-result")
    def on_add_spool_result(self, result: dict) -> None:
        """Handle results for adding a spool."""
        self._add_spool_page.on_add_spool_result(result)

    @QtCore.pyqtSlot(dict, name="on-add-filament-result")
    def on_add_filament_result(self, result: dict) -> None:
        """Handle results for adding a filament."""
        self._add_filament_page.on_add_filament_result(result)

    @QtCore.pyqtSlot(dict, name="on-add-manufacturer-result")
    def on_add_manufacturer_result(self, result: dict) -> None:
        """Handle results for adding a manufacturer/vendor."""
        self._add_filament_page.on_add_manufacturer_result(result)
