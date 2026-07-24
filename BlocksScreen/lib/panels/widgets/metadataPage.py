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
        """Populate the page with all metadata fields for the given file."""
        self.title_label.setText(os.path.basename(text))
        self._clear_rows()
        pairs: list[tuple[str, str]] = []
        for key, value in (filedata or {}).items():
            if key in _HIDDEN_FIELDS:
                continue
            formatted = self._format_value(key, value)
            if formatted is None:
                continue
            pairs.append((self._humanize(key), formatted))
        if not pairs:
            pairs.append(("No metadata available", ""))
        for index, (label, value) in enumerate(pairs):
            self._add_row(label, value, index // 2, index % 2)
        self._rows_layout.setRowStretch(self._rows_layout.rowCount(), 1)

    def _humanize(self, key: str) -> str:
        """Map a metadata key to its display label."""
        return _FIELD_LABELS.get(key, key.replace("_", " ").title())

    def _format_value(self, key: str, value: object) -> str | None:
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

    def _add_row(self, label: str, value: str, row: int, col: int) -> None:
        """Place a single key/value cell into the two-column grid."""
        cell = QtWidgets.QHBoxLayout()
        cell.setContentsMargins(0, 0, 0, 0)
        key_label = QtWidgets.QLabel(label, parent=self._rows_container)
        key_label.setStyleSheet(
            "background: transparent; color: white; font-size: 18px;"
        )
        key_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        value_label = QtWidgets.QLabel(value, parent=self._rows_container)
        value_label.setStyleSheet(
            "background: transparent; color: white; font-size: 18px;"
        )
        value_label.setWordWrap(True)
        value_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        cell.addWidget(value_label, 1)
        cell.addWidget(key_label, 1)
        self._rows_layout.addLayout(cell, row, col)

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
        self.title_label.setMinimumSize(QtCore.QSize(0, 60))
        self.title_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
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
        outer.addSpacing(20)

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
        self._rows_layout.setContentsMargins(20, 0, 20, 0)
        self._rows_layout.setHorizontalSpacing(40)
        self._rows_layout.setVerticalSpacing(10)
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
