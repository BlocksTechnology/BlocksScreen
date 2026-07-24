"""File metadata detail page: lists every available gcode metadata field."""

import os
import typing

from lib.utils.blocks_label import BlocksLabel
from lib.utils.blocks_Scrollbar import CustomScrollBar
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets

# Human-readable labels for known Moonraker gcode-metadata keys.
_FIELD_LABELS: dict[str, str] = {
    "size": "File Size",
    "modified": "Modified",
    "print_start_time": "Last Print",
    "job_id": "Job ID",
    "slicer": "Slicer",
    "slicer_version": "Slicer Version",
    "gcode_start_byte": "G-code Start Byte",
    "gcode_end_byte": "G-code End Byte",
    "layer_count": "Layer Count",
    "object_height": "Object Height",
    "estimated_time": "Estimated Time",
    "nozzle_diameter": "Nozzle Size",
    "layer_height": "Layer Height",
    "first_layer_height": "First Layer Height",
    "first_layer_extr_temp": "First Layer Nozzle Temp",
    "first_layer_bed_temp": "First Layer Bed Temp",
    "chamber_temp": "Chamber Temp",
    "filament_name": "Filament Name",
    "filament_type": "Filament Type",
    "filament_total": "Filament Length",
    "filament_weight_total": "Filament Weight",
    "filament_change_count": "Filament Changes",
    "mmu_print": "MMU Print",
}
# First-layer temps re-labeled to plain extruder/bed names.
_FIELD_LABELS["first_layer_extr_temp"] = "Extruder Temp"
_FIELD_LABELS["first_layer_bed_temp"] = "Bed Temp"
# Titled sections and the ordered keys shown under each.
_CATEGORIES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("General", ("slicer", "slicer_version", "print_start_time", "estimated_time", "mmu_print")),
    ("Geometry", ("object_height", "layer_height", "nozzle_diameter")),
    ("Temperatures", ("first_layer_extr_temp", "first_layer_bed_temp", "chamber_temp")),
    (
        "Filament",
        ("filament_type", "filament_total", "filament_weight_total", "filament_change_count"),
    ),
)
# Units appended to numeric values.
_UNITS: dict[str, str] = {
    "object_height": " mm",
    "layer_height": " mm",
    "nozzle_diameter": " mm",
    "first_layer_extr_temp": " °C",
    "first_layer_bed_temp": " °C",
    "chamber_temp": " °C",
}
# Internal fields not meaningful to the user.
_HIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "thumbnails",
        "thumbnail_paths",
        "uuid",
        "size",
        "gcode_start_byte",
        "gcode_end_byte",
        "filament_name",
        "filename",
        "path",
        "layer_count",
        "modified",
        "first_layer_height",
        "job_id",
    }
)


class FileMetadataWidget(QtWidgets.QWidget):
    """Scrollable list of every available metadata field for a gcode file."""

    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setupUI()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.back_btn.clicked.connect(self.request_back.emit)

    @QtCore.pyqtSlot(str, dict, name="on_show_widget")
    def on_show_widget(self, text: str, filedata: dict | None = None) -> None:
        """Populate the page with metadata grouped into titled category cards."""
        self.title_label.setText(os.path.basename(text))
        self._clear_rows()
        data = filedata or {}
        shown = False
        for title, keys in _CATEGORIES:
            pairs: list[tuple[str, str]] = []
            for key in keys:
                if key in _HIDDEN_FIELDS:
                    continue
                formatted = self._format_value(key, data.get(key))
                if formatted is None:
                    continue
                pairs.append((self._humanize(key), formatted))
            if pairs:
                self._add_category_card(title, pairs)
                shown = True
        if not shown:
            self._add_category_card("Info", [("No metadata available", "")])
        self._rows_layout.addStretch(1)

    def _humanize(self, key: str) -> str:
        """Map a metadata key to its display label."""
        return _FIELD_LABELS.get(key, key.replace("_", " ").title())

    def _format_value(self, key: str, value: object) -> str | None:
        """Render a metadata value as text with its unit, or None to skip it."""
        base = self._raw_value(key, value)
        if base is None:
            return None
        return f"{base}{_UNITS.get(key, '')}"

    def _raw_value(self, key: str, value: object) -> str | None:
        """Render a metadata value as text, or None to skip it."""
        if value is None or value == "" or value == []:
            return None
        if isinstance(value, bool):
            return "Yes" if value else "No"
        if key == "filament_weight_total" and isinstance(value, (int, float)):
            return f"{value / 1000:.2f}kg" if value > 499 else f"{value:.2f}g"
        if key == "filament_total" and isinstance(value, (int, float)):
            return f"{value / 1000:.2f}m"
        if key in ("size", "gcode_start_byte", "gcode_end_byte") and isinstance(
            value, (int, float)
        ):
            return self._format_bytes(int(value))
        if key in ("modified", "print_start_time") and isinstance(value, (int, float)):
            return QtCore.QDateTime.fromSecsSinceEpoch(int(value)).toString(
                "yyyy-MM-dd hh:mm"
            )
        if key == "estimated_time" and isinstance(value, (int, float)):
            return self._format_duration(int(value))
        if isinstance(value, float):
            return f"{value:g}"
        if isinstance(value, (list, tuple)):
            return ", ".join(str(v) for v in value)
        return str(value)

    def _format_bytes(self, num: int) -> str:
        """Human-readable byte size."""
        size = float(num)
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024 or unit == "GB":
                return f"{size:.0f}{unit}" if unit == "B" else f"{size:.2f}{unit}"
            size /= 1024
        return f"{num}B"

    def _format_duration(self, seconds: int) -> str:
        """Human-readable duration from seconds."""
        if seconds <= 0:
            return "??"
        days, rem = divmod(seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, _ = divmod(rem, 60)
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    def _add_category_card(self, title: str, pairs: list[tuple[str, str]]) -> None:
        """Add a titled card holding a two-column grid of key/value rows."""
        card = QtWidgets.QFrame(parent=self._rows_container)
        card.setObjectName("md_card")
        card.setStyleSheet(
            "#md_card { background: rgba(26, 143, 191, 0.12); border-radius: 12px; }"
        )
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(12, 6, 12, 6)
        card_layout.setSpacing(2)
        header = QtWidgets.QLabel(title, parent=card)
        header_font = QtGui.QFont()
        header_font.setFamily("Momcake")
        header_font.setPointSize(13)
        header.setFont(header_font)
        header.setStyleSheet("background: transparent; color: #1A8FBF;")
        card_layout.addWidget(header)
        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(2)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        for index, (label, value) in enumerate(pairs):
            self._add_row(grid, label, value, index // 2, index % 2)
        card_layout.addLayout(grid)
        self._rows_layout.addWidget(card)

    def _add_row(
        self, grid: QtWidgets.QGridLayout, label: str, value: str, row: int, col: int
    ) -> None:
        """Place a single key/value cell into a card's two-column grid."""
        value_style = "background: transparent; color: white; font-size: 12px;"
        title_style = (
            "background: transparent; color: white; "
            "font-size: 13px; font-weight: bold;"
        )
        cell = QtWidgets.QHBoxLayout()
        cell.setContentsMargins(0, 0, 0, 0)
        cell.setSpacing(0)
        key_label = QtWidgets.QLabel(label, parent=self._rows_container)
        key_label.setStyleSheet(title_style)
        key_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        sep_label = QtWidgets.QLabel(": ", parent=self._rows_container)
        sep_label.setStyleSheet(title_style)
        sep_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        value_label = QtWidgets.QLabel(value, parent=self._rows_container)
        value_label.setStyleSheet(value_style)
        value_label.setWordWrap(True)
        value_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        cell.addStretch(1)
        cell.addWidget(value_label, 0)
        cell.addWidget(sep_label, 0)
        cell.addWidget(key_label, 0)
        cell.addStretch(1)
        grid.addLayout(cell, row, col)

    def _clear_rows(self) -> None:
        """Remove every row currently in the list."""
        while self._rows_layout.count():
            item = self._rows_layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                continue
            child = item.layout()
            if child is not None:
                self._clear_layout(child)

    def _clear_layout(self, layout: QtWidgets.QLayout) -> None:
        """Delete all widgets in a nested layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        layout.deleteLater()

    def _setupUI(self) -> None:
        """Build the header and scrollable metadata list."""
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(720, 420))
        outer = QtWidgets.QVBoxLayout(self)
        outer.setObjectName("md_outer_layout")

        header = QtWidgets.QHBoxLayout()
        header.setObjectName("md_header")

        self.title_label = BlocksLabel(parent=self)
        self.title_label.setMinimumSize(QtCore.QSize(0, 44))
        self.title_label.setMaximumSize(QtCore.QSize(16777215, 44))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(20)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("background: transparent; color: white;")
        self.title_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.title_label.setObjectName("md_title_label")
        header.addWidget(self.title_label, 1)

        self.back_btn = IconButton(self)
        self.back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.back_btn.setFlat(True)
        self.back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.back_btn.setObjectName("md_back_btn")
        header.addWidget(self.back_btn, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        outer.addLayout(header)
        outer.addSpacing(6)

        self._scroll_area = QtWidgets.QScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self._scroll_area.setStyleSheet("background: transparent;")
        self._scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll_area.setVerticalScrollBar(CustomScrollBar())

        self._rows_container = QtWidgets.QWidget()
        self._rows_container.setStyleSheet("background: transparent;")
        self._rows_layout = QtWidgets.QVBoxLayout(self._rows_container)
        self._rows_layout.setContentsMargins(12, 0, 12, 0)
        self._rows_layout.setSpacing(8)
        self._scroll_area.setWidget(self._rows_container)
        viewport = self._scroll_area.viewport()
        QtWidgets.QScroller.grabGesture(
            viewport, QtWidgets.QScroller.ScrollerGestureType.TouchGesture
        )
        QtWidgets.QScroller.grabGesture(
            viewport, QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture
        )
        outer.addWidget(self._scroll_area)
