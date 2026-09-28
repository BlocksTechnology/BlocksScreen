"""Gcode metadata detail page."""

import typing
from pathlib import Path

import helper_methods

from lib.utils.blocks_label import BlocksLabel
from lib.utils.blocks_Scrollbar import CustomScrollBar
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets

_FIELD_LABELS: dict[str, str] = {
    "print_start_time": "Last Print",
    "print_duration": "Last Print Duration",
    "slicer": "Slicer",
    "slicer_version": "Slicer Version",
    "layer_count": "Layer Count",
    "object_height": "Object Height",
    "estimated_time": "Estimated Time",
    "nozzle_diameter": "Nozzle Size",
    "layer_height": "Layer Height",
    "first_layer_extr_temp": "Nozzle Temperature",
    "first_layer_bed_temp": "Bed Temperature",
    "filament_type": "Filament Type",
    "filament_total": "Filament Length",
    "filament_weight_total": "Filament Weight",
    "filament_change_count": "Filament Changes",
    "mmu_print": "MMU Print",
}
_CATEGORIES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "General",
        (
            "estimated_time",
            "print_duration",
            "slicer",
            "slicer_version",
            "print_start_time",
            "mmu_print",
        ),
    ),
    ("Geometry", ("nozzle_diameter", "layer_height", "object_height", "layer_count")),
    ("Temperature", ("first_layer_extr_temp", "first_layer_bed_temp")),
    (
        "Filament",
        (
            "filament_type",
            "filament_total",
            "filament_weight_total",
            "filament_change_count",
        ),
    ),
)
_UNITS: dict[str, str] = {
    "object_height": " mm",
    "layer_height": " mm",
    "nozzle_diameter": " mm",
    "first_layer_extr_temp": " °C",
    "first_layer_bed_temp": " °C",
}
# Nozzle temp (°C) fallback when the slicer omits it.
_FILAMENT_NOZZLE_TEMP: dict[str, int] = {
    "PLA": 210,
    "PETG": 235,
    "ABS": 240,
    "ASA": 240,
    "TPU": 220,
    "PC": 260,
    "NYLON": 250,
    "PVA": 200,
    "HIPS": 240,
    "PP": 230,
}
# One sheet per card; per-label sheets re-polish on every show.
_CARD_STYLE = (
    "#md_card { background: rgba(26, 143, 191, 0.12); border-radius: 12px; }"
    " QLabel { background: transparent; color: white; }"
    " QLabel#md_key { font-size: 17px; font-weight: bold; }"
    " QLabel#md_value { font-size: 16px; }"
)


def _format_timestamp(value: float) -> str:
    """Epoch seconds as a local wall-clock stamp."""
    return QtCore.QDateTime.fromSecsSinceEpoch(int(value)).toString("yyyy-MM-dd hh:mm")


def _format_seconds(value: float) -> str | None:
    """A duration, or None when the slicer left it unset."""
    return helper_methods.format_duration(int(value)) if value > 0 else None


# Unlisted keys render as plain text.
_NUMERIC_RENDERERS: dict[str, typing.Callable[[float], str | None]] = {
    "filament_weight_total": helper_methods.format_weight,
    "filament_total": lambda value: f"{value / 1000:.2f}m",
    "print_start_time": _format_timestamp,
    "estimated_time": _format_seconds,
    "print_duration": _format_seconds,
}


def _numeric_value(key: str, value: float) -> str | None:
    """Render a number, hiding the slicers' -1 "unknown" sentinel."""
    if value == -1:
        return None
    render = _NUMERIC_RENDERERS.get(key)
    if render is not None:
        return render(value)
    return f"{value:g}" if isinstance(value, float) else str(value)


class FileMetadataWidget(QtWidgets.QWidget):
    """Scrollable metadata cards for one gcode file."""

    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._shown_path: str = ""
        self._setupUI()
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.back_btn.clicked.connect(self.request_back.emit)

    @QtCore.pyqtSlot(dict, name="on_fileinfo")
    def on_fileinfo(self, filedata: dict) -> None:
        """Re-render on fresh metadata for the shown file."""
        path = filedata.get("filename", "").removeprefix("/")
        if self.isVisible() and path and path == self._shown_path:
            self.on_show_widget(path, filedata)

    @QtCore.pyqtSlot(str, dict, name="on_show_widget")
    def on_show_widget(self, text: str, filedata: dict | None = None) -> None:
        """Render *filedata* as titled category cards."""
        self._shown_path = text.removeprefix("/")
        self.title_label.setText(Path(text).name)
        data = dict(filedata or {})
        cur = data.get("first_layer_extr_temp")
        if not isinstance(cur, (int, float)) or cur <= 0:
            temp = self._filament_nozzle_temp(data.get("filament_type"))
            if temp is not None:
                data["first_layer_extr_temp"] = temp
        self._clear_rows()
        placed = 0
        for title, keys in _CATEGORIES:
            pairs: list[tuple[str, str]] = []
            for key in keys:
                formatted = self._format_value(key, data.get(key))
                if formatted is None:
                    continue
                pairs.append((self._humanize(key), formatted))
            if pairs:
                self._add_category_card(title, pairs, placed)
                placed += 1
        if placed == 0:
            self._add_category_card("Info", [("No metadata available", "")], 0)
            placed = 1
        used = (placed + 1) // 2
        # rowCount never shrinks; a stale stretch on an empty row halves the cards.
        for row in range(self._rows_layout.rowCount()):
            self._rows_layout.setRowStretch(row, 1 if row < used else 0)

    def _filament_nozzle_temp(self, filament_type: object) -> int | None:
        """Typical nozzle temp for the material, or None."""
        if not isinstance(filament_type, str):
            return None
        name = filament_type.upper()
        for material, temp in _FILAMENT_NOZZLE_TEMP.items():
            if material in name:
                return temp
        return None

    def _humanize(self, key: str) -> str:
        """Map a metadata key to its display label."""
        return _FIELD_LABELS.get(key, key.replace("_", " ").title())

    def _format_value(self, key: str, value: object) -> str | None:
        """Value text with its unit, None to skip."""
        base = self._raw_value(key, value)
        if base is None:
            return None
        return f"{base}{_UNITS.get(key, '')}"

    def _raw_value(self, key: str, value: object) -> str | None:
        """Value text, None to skip."""
        if value is None or value in ("", [], {}, "Unknown"):
            return None
        if isinstance(value, bool):
            return "Yes" if value else "No"
        if isinstance(value, (int, float)):
            return _numeric_value(key, value)
        if isinstance(value, (list, tuple)):
            return ", ".join(str(v) for v in value)
        return str(value)

    def _add_category_card(
        self, title: str, pairs: list[tuple[str, str]], position: int
    ) -> None:
        """Add a titled card (2 per row) listing its key/value rows."""
        card = QtWidgets.QFrame(parent=self._rows_container)
        card.setObjectName("md_card")
        card.setStyleSheet(_CARD_STYLE)
        card.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(12, 6, 12, 6)
        card_layout.setSpacing(2)
        header = QtWidgets.QLabel(title, parent=card)
        header_font = QtGui.QFont()
        header_font.setFamily("Momcake")
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(header)
        grid = QtWidgets.QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(2)
        grid.setColumnStretch(0, 1)
        for row, (label, value) in enumerate(pairs):
            grid.addLayout(self._make_row(card, label, value), row, 0)
        card_layout.addLayout(grid)
        self._rows_layout.addWidget(card, position // 2, position % 2)

    def _make_row(
        self, card: QtWidgets.QFrame, label: str, value: str
    ) -> QtWidgets.QHBoxLayout:
        """Build one key/value cell whose labels belong to *card*."""
        cell = QtWidgets.QHBoxLayout()
        cell.setContentsMargins(0, 0, 0, 0)
        cell.setSpacing(0)
        key_label = QtWidgets.QLabel(label, parent=card)
        key_label.setObjectName("md_key")
        key_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        sep_label = QtWidgets.QLabel(": ", parent=card)
        sep_label.setObjectName("md_key")
        sep_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        value_label = QtWidgets.QLabel(value, parent=card)
        value_label.setObjectName("md_value")
        value_label.setWordWrap(True)
        value_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        cell.addWidget(key_label, 0)
        cell.addWidget(sep_label, 0)
        cell.addStretch(1)
        cell.addWidget(value_label, 0)
        return cell

    def _clear_rows(self) -> None:
        """Delete all cards with their labels and layouts."""
        while (item := self._rows_layout.takeAt(0)) is not None:
            if (card := item.widget()) is not None:
                card.deleteLater()

    def _setupUI(self) -> None:
        """Build the header and scrollable metadata list."""
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
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
        self._rows_layout = QtWidgets.QGridLayout(self._rows_container)
        self._rows_layout.setContentsMargins(12, 0, 12, 0)
        self._rows_layout.setHorizontalSpacing(8)
        self._rows_layout.setVerticalSpacing(8)
        self._rows_layout.setColumnStretch(0, 1)
        self._rows_layout.setColumnStretch(1, 1)
        self._scroll_area.setWidget(self._rows_container)
        viewport = self._scroll_area.viewport()
        QtWidgets.QScroller.grabGesture(
            viewport, QtWidgets.QScroller.ScrollerGestureType.TouchGesture
        )
        QtWidgets.QScroller.grabGesture(
            viewport, QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture
        )
        outer.addWidget(self._scroll_area)
