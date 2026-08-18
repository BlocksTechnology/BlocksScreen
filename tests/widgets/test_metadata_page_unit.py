"""Regression tests for FileMetadataWidget sentinel hiding (metadataPage.py).

Drives the REAL pipeline FileMetadata.from_dict(raw, []).to_dict() -> on_show_widget
so dataclass asdict() sentinel defaults (-1.0 / 0 / {} / "Unknown") are exercised,
under both LeftToRight and app-global RightToLeft layout (the app runs RTL).
"""

import importlib.util
import sys
import types
from pathlib import Path

import pytest
from PyQt6 import QtCore, QtWidgets

# metadataPage imports these custom widgets; stub before it is imported.
_blocks_label = types.ModuleType("lib.utils.blocks_label")
_blocks_label.BlocksLabel = QtWidgets.QLabel
_scrollbar = types.ModuleType("lib.utils.blocks_Scrollbar")
_scrollbar.CustomScrollBar = QtWidgets.QScrollBar
sys.modules["lib.utils.blocks_label"] = _blocks_label
sys.modules["lib.utils.blocks_Scrollbar"] = _scrollbar

# Load the REAL FileMetadata by path under a private module name: sibling
# conftests stub sys.modules["lib.files"], so a plain import is unsafe.
_files_path = Path(__file__).resolve().parents[2] / "BlocksScreen" / "lib" / "files.py"
_spec = importlib.util.spec_from_file_location("_bs_real_files", _files_path)
_files = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
sys.modules["_bs_real_files"] = _files  # register so dataclass introspection resolves
_spec.loader.exec_module(_files)  # type: ignore[union-attr]
FileMetadata = _files.FileMetadata

from lib.panels.widgets.metadataPage import FileMetadataWidget  # noqa: E402

_DIRECTIONS = (
    QtCore.Qt.LayoutDirection.LeftToRight,
    QtCore.Qt.LayoutDirection.RightToLeft,
)


@pytest.fixture()
def render(qtbot, qapp):
    """Feed raw metadata through the real pipeline, return non-empty label texts."""
    original = qapp.layoutDirection()

    def _render(raw, direction):
        qapp.setLayoutDirection(direction)
        widget = FileMetadataWidget()
        qtbot.addWidget(widget)
        filedata = FileMetadata.from_dict(raw, []).to_dict()
        widget.on_show_widget("USB-Stick/part.gcode", filedata)
        return [
            label.text()
            for label in widget.findChildren(QtWidgets.QLabel)
            if label.text().strip()
        ]

    yield _render
    qapp.setLayoutDirection(original)


@pytest.mark.parametrize("direction", _DIRECTIONS)
def test_empty_metadata_shows_placeholder_no_sentinels(render, direction):
    """Empty metadata -> 'No metadata available', never a raw sentinel string."""
    texts = render({}, direction)
    joined = " ".join(texts)
    assert "No metadata available" in texts
    assert "{}" not in joined
    assert "??" not in joined
    assert "-1" not in joined


@pytest.mark.parametrize("direction", _DIRECTIONS)
def test_missing_time_and_length_hidden_not_leaked(render, direction):
    """estimated_time=0 and filament_total={} are hidden, not shown as '??'/'{}'."""
    texts = render({"slicer": "PrusaSlicer", "nozzle_diameter": 0.4}, direction)
    joined = " ".join(texts)
    assert "PrusaSlicer" in joined
    assert "Estimated Time" not in joined
    assert "Filament Length" not in joined
    assert "{}" not in joined
    assert "??" not in joined


@pytest.mark.parametrize("direction", _DIRECTIONS)
def test_real_values_render(render, direction):
    """Real metadata values render through the pipeline (no over-suppression)."""
    raw = {
        "estimated_time": 3600,
        "filament_total": 1234.5,
        "first_layer_extr_temp": 205.0,
        "filament_type": "PETG",
    }
    joined = " ".join(render(raw, direction))
    assert "1h 0m" in joined
    assert "1.23m" in joined
    assert "205" in joined
    assert "{}" not in joined
    assert "??" not in joined
