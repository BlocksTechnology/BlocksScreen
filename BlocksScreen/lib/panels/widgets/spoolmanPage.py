import typing

from lib.panels.widgets.addFilamentPage import AddFilamentPage
from lib.panels.widgets.addSpoolPage import AddSpoolPage
from lib.panels.widgets.basePopup import BasePopup
from lib.panels.widgets.loadWidget import LoadingOverlayWidget
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets


class SpoolmanPage(QtWidgets.QWidget):
    request_spools: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-spools"
    )
    request_get_spool_id: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-get-spool-id"
    )
    request_set_spool_id: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, name="request-set-spool-id"
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
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-back"
    )

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._spools: list[dict] = []
        self._active_spool_id: int | None = None
        self._selected_spool: dict | None = None
        self._display_name_to_spool: dict[str, dict] = {}

        self._setupUI()

        self.model = EntryListModel()
        self.model.setParent(self.spool_list_widget)
        self.entry_delegate = EntryDelegate()
        self.spool_list_widget.setModel(self.model)
        self.spool_list_widget.setItemDelegate(self.entry_delegate)

        self.entry_delegate.item_selected.connect(self.on_item_clicked)
        self.reload_btn.clicked.connect(self._on_reload_clicked)
        self.back_btn.clicked.connect(self.request_back)
        self.set_active_btn.clicked.connect(self._on_set_active_clicked)
        self.delete_btn.clicked.connect(self._on_delete_clicked)
        self.confirm_yes_btn.clicked.connect(self._on_confirm_delete)
        self.confirm_no_btn.clicked.connect(self._on_cancel_delete)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self._setup_add_popup()
        self.show_loading(True)

    @QtCore.pyqtSlot(dict, name="on-spools-received")
    def on_spools_received(self, result: dict) -> None:
        """Handle v2 proxy response for GET /v1/spool."""
        if result.get("error") is not None:
            self.show_loading(False)
            return
        spools = result.get("response")
        if not isinstance(spools, list):
            self.show_loading(False)
            return
        self._spools = spools
        self._build_model_list()

    @QtCore.pyqtSlot(dict, name="on-active-spool-received")
    def on_active_spool_received(self, result: dict) -> None:
        """Handle response for server.spoolman.get_spool_id."""
        self._active_spool_id = (
            result.get("spool_id") if isinstance(result, dict) else None
        )
        self._build_model_list()

    @QtCore.pyqtSlot(dict, name="on-delete-spool-result")
    def on_delete_spool_result(self, result: dict) -> None:
        if result.get("error") is None:
            self._selected_spool = None
            self._on_reload_clicked()

    def _spool_display_name(self, spool: dict) -> str:
        spool_id = spool.get("id", "?")
        filament = spool.get("filament") or {}
        name = filament.get("name") or f"Spool #{spool_id}"
        if spool.get("archived", False):
            name = f"{name} [Archived]"
        return name

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
        self.show_loading(True)
        self.request_spools.emit()
        self.request_get_spool_id.emit()

    def _on_set_active_clicked(self) -> None:
        if self._selected_spool is None:
            return
        spool_id = self._selected_spool.get("id")
        if spool_id is not None:
            self.request_set_spool_id.emit(int(spool_id))

    def _on_delete_clicked(self) -> None:
        if self._selected_spool is None:
            return
        self.action_stack.setCurrentIndex(1)

    def _on_confirm_delete(self) -> None:
        self.action_stack.setCurrentIndex(0)
        if self._selected_spool is not None:
            spool_id = self._selected_spool.get("id")
            if spool_id is not None:
                self.request_delete_spool.emit(int(spool_id))

    def _on_cancel_delete(self) -> None:
        self.action_stack.setCurrentIndex(0)

    def _build_model_list(self) -> None:
        self.spool_list_widget.blockSignals(True)
        self.model.clear()
        self.entry_delegate.clear()
        self._display_name_to_spool = {}

        for spool in self._spools:
            spool_id = spool.get("id", "?")
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

            is_active = spool_id == self._active_spool_id
            item = ListItem(
                text=display_name,
                right_text=right_text,
                left_icon=self._make_color_pixmap(filament),
                selected=False,
                _lfontsize=14,
                _rfontsize=12,
                height=60,
                notificate=is_active,
            )
            self.model.add_item(item)

        self.model.add_item(
            ListItem(
                text="+ Add Spool",
                left_icon=self._make_add_pixmap(),
                _lfontsize=14,
                height=60,
            )
        )

        self.model.setData(self.model.index(0), True, EntryListModel.EnableRole)
        self.on_item_clicked(
            self.model.data(self.model.index(0), QtCore.Qt.ItemDataRole.UserRole)
        )
        self.spool_list_widget.blockSignals(False)
        self.show_loading(False)

    @QtCore.pyqtSlot(ListItem, name="on-item-clicked")
    def on_item_clicked(self, item: ListItem) -> None:
        if not item:
            return
        if item.text == "+ Add Spool":
            self._on_add_spool_clicked()
            return
        self._selected_spool = self._display_name_to_spool.get(item.text)
        self.action_stack.setCurrentIndex(0)
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

        is_active = spool.get("id") == self._active_spool_id
        self.set_active_btn.setText("Active" if is_active else "Set Active")
        self.set_active_btn.setEnabled(not is_active)

    def _update_color_swatches(self, filament: dict) -> None:
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

    def show_loading(self, loading: bool) -> None:
        self.load_widget.setVisible(loading)
        self.spool_list_widget.setVisible(not loading)

    def showEvent(self, event: QtGui.QShowEvent | None) -> None:
        self._on_reload_clicked()
        return super().showEvent(event)

    def deleteLater(self) -> None:
        self.model.clear()
        self.entry_delegate.clear()
        return super().deleteLater()

    def _setupUI(self) -> None:
        font_id = QtGui.QFontDatabase.addApplicationFont(
            ":/font/media/fonts for text/Momcake-Bold.ttf"
        )
        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

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
        title_font.setFamily(font_family)
        title_font.setPointSize(22)
        self.header_title = QtWidgets.QLabel("Spoolman", self)
        self.header_title.setFixedHeight(60)
        self.header_title.setStyleSheet("color: white; background: transparent;")
        self.header_title.setFont(title_font)
        self.header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.header_title, 1)

        self.back_btn = _icon_btn(":/ui/media/btn_icons/back.svg")
        header_layout.addWidget(self.back_btn)

        page_layout.addLayout(header_layout)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setSpacing(8)

        list_frame = BlocksCustomFrame(self)
        list_frame.setMinimumWidth(380)

        self.spool_list_widget = QtWidgets.QListView(list_frame)
        self.spool_list_widget.setMouseTracking(True)
        self.spool_list_widget.setTabletTracking(True)
        self.spool_list_widget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.spool_list_widget.setStyleSheet("background-color: transparent;")
        self.spool_list_widget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.spool_list_widget.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.spool_list_widget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.spool_list_widget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.spool_list_widget.setAutoScroll(False)
        self.spool_list_widget.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.NoSelection
        )
        self.spool_list_widget.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.spool_list_widget.setHorizontalScrollMode(
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

        self.load_widget = LoadingOverlayWidget(
            list_frame, LoadingOverlayWidget.AnimationGIF.DEFAULT
        )

        list_layout = QtWidgets.QVBoxLayout()
        list_layout.setContentsMargins(4, 4, 4, 4)
        list_layout.addWidget(self.spool_list_widget, 1)
        self.spool_list_widget.hide()
        list_layout.addWidget(self.load_widget, 1)
        list_frame.setLayout(list_layout)
        main_layout.addWidget(list_frame, 3)

        info_frame = BlocksCustomFrame()
        info_layout = QtWidgets.QVBoxLayout()
        info_layout.setContentsMargins(10, 8, 10, 6)
        info_layout.setSpacing(4)
        info_frame.setLayout(info_layout)

        key_font = QtGui.QFont()
        key_font.setFamily(font_family)
        key_font.setPointSize(12)

        val_font = QtGui.QFont()
        val_font.setFamily(font_family)
        val_font.setPointSize(14)

        white_palette = QtGui.QPalette()
        white_palette.setColor(
            white_palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF")
        )

        ROW_H = 32

        def _add_row(title_text: str) -> QtWidgets.QLabel:
            row = QtWidgets.QHBoxLayout()
            row.setSpacing(4)
            title = QtWidgets.QLabel(title_text, self)
            title.setFont(key_font)
            title.setStyleSheet("color: rgb(180,180,180); background: transparent;")
            title.setFixedHeight(ROW_H)
            title.setMinimumWidth(80)
            title.setMaximumWidth(110)
            value = QtWidgets.QLabel("—", self)
            value.setFont(val_font)
            value.setStyleSheet("color: white; background: transparent;")
            value.setFixedHeight(ROW_H)
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
        color_title.setFixedHeight(ROW_H)
        color_title.setMinimumWidth(80)
        color_title.setMaximumWidth(110)
        color_row.addWidget(color_title, 0)
        color_row.addStretch(1)
        self.color_swatch_layout = QtWidgets.QHBoxLayout()
        self.color_swatch_layout.setSpacing(4)
        color_row.addLayout(self.color_swatch_layout)
        info_layout.addLayout(color_row)

        info_layout.addStretch(1)

        # Action area: stacked (normal | delete-confirm)
        action_font = QtGui.QFont()
        action_font.setFamily(font_family)
        action_font.setPointSize(16)

        self.action_stack = QtWidgets.QStackedWidget()
        self.action_stack.setFixedHeight(60)

        # Page 0: normal actions
        normal_page = QtWidgets.QWidget()
        normal_layout = QtWidgets.QHBoxLayout(normal_page)
        normal_layout.setContentsMargins(0, 0, 0, 0)
        normal_layout.setSpacing(8)

        self.delete_btn = IconButton(self)
        self.delete_btn.setFixedSize(QtCore.QSize(60, 60))
        self.delete_btn.setFlat(True)
        self.delete_btn.setPixmap(
            QtGui.QPixmap(":/ui/media/btn_icons/garbage-icon.svg")
        )
        normal_layout.addWidget(self.delete_btn, 0)

        self.set_active_btn = BlocksCustomButton()
        self.set_active_btn.setFixedHeight(60)
        self.set_active_btn.setMinimumWidth(160)
        self.set_active_btn.setMaximumWidth(260)
        self.set_active_btn.setFont(action_font)
        self.set_active_btn.setText("Set Active")
        normal_layout.addWidget(
            self.set_active_btn, 1, QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.action_stack.addWidget(normal_page)

        # Page 1: confirm delete
        confirm_page = QtWidgets.QWidget()
        confirm_layout = QtWidgets.QHBoxLayout(confirm_page)
        confirm_layout.setContentsMargins(0, 0, 0, 0)
        confirm_layout.setSpacing(6)

        confirm_lbl = QtWidgets.QLabel("Delete spool?", self)
        confirm_lbl.setFont(val_font)
        confirm_lbl.setStyleSheet("color: white; background: transparent;")
        confirm_layout.addWidget(confirm_lbl, 1)

        self.confirm_yes_btn = BlocksCustomButton()
        self.confirm_yes_btn.setFixedSize(QtCore.QSize(90, 60))
        self.confirm_yes_btn.setFont(action_font)
        self.confirm_yes_btn.setText("Yes")
        confirm_layout.addWidget(self.confirm_yes_btn)

        self.confirm_no_btn = BlocksCustomButton()
        self.confirm_no_btn.setFixedSize(QtCore.QSize(90, 60))
        self.confirm_no_btn.setFont(action_font)
        self.confirm_no_btn.setText("No")
        confirm_layout.addWidget(self.confirm_no_btn)

        self.action_stack.addWidget(confirm_page)

        info_layout.addWidget(self.action_stack, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(info_frame, 1)
        page_layout.addLayout(main_layout, 1)
        self.setLayout(page_layout)

    def _setup_add_popup(self) -> None:
        # Add Spool popup
        self._add_spool_page = AddSpoolPage(keyboard_parent=self, parent=self)
        self._add_spool_popup = BasePopup(self, False, False)
        self._add_spool_popup.add_widget(self._add_spool_page)

        # Add Filament popup
        self._add_filament_page = AddFilamentPage(keyboard_parent=self, parent=self)
        self._add_filament_popup = BasePopup(self, False, False)
        self._add_filament_popup.add_widget(self._add_filament_page)

        # --- Add Spool signals ---
        self._add_spool_page.request_filaments.connect(self.request_filaments)
        self._add_spool_page.request_add_spool.connect(self.request_add_spool)
        self._add_spool_page.open_add_filament.connect(self._add_filament_popup.show)
        self._add_spool_page.accepted.connect(self._add_spool_popup.hide)
        self._add_spool_page.accepted.connect(self._on_reload_clicked)
        self._add_spool_page.cancelled.connect(self._add_spool_popup.hide)

        # --- Add Filament signals ---
        self._add_filament_page.request_add_filament.connect(self.request_add_filament)
        self._add_filament_page.accepted.connect(self._add_filament_popup.hide)
        self._add_filament_page.accepted.connect(self._add_spool_page.reset)
        self._add_filament_page.cancelled.connect(self._add_filament_popup.hide)

    def _on_add_spool_clicked(self) -> None:
        self._add_spool_page.reset()
        self._add_spool_popup.show()

    @QtCore.pyqtSlot(dict, name="on-filaments-received")
    def on_filaments_received(self, result: dict) -> None:
        self._add_spool_page.on_filaments_received(result)

    @QtCore.pyqtSlot(dict, name="on-add-spool-result")
    def on_add_spool_result(self, result: dict) -> None:
        self._add_spool_page.on_add_spool_result(result)

    @QtCore.pyqtSlot(dict, name="on-add-filament-result")
    def on_add_filament_result(self, result: dict) -> None:
        self._add_filament_page.on_add_filament_result(result)
