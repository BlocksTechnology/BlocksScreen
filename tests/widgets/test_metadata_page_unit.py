"""FileMetadataWidget sentinel hiding via the real from_dict pipeline, LTR and RTL."""

import importlib.util
import sys
import types
from pathlib import Path

import pytest
from PyQt6 import QtCore, QtWidgets

# Stub metadataPage's custom widgets before importing it.
_blocks_label = types.ModuleType("lib.utils.blocks_label")
_blocks_label.BlocksLabel = QtWidgets.QLabel
_scrollbar = types.ModuleType("lib.utils.blocks_Scrollbar")
_scrollbar.CustomScrollBar = QtWidgets.QScrollBar
sys.modules["lib.utils.blocks_label"] = _blocks_label
sys.modules["lib.utils.blocks_Scrollbar"] = _scrollbar

# Real FileMetadata by path: sibling conftests stub lib.files.
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
    """Render raw metadata; return the non-empty label texts."""
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
    """Guards against over-suppression."""
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


@pytest.mark.parametrize("direction", _DIRECTIONS)
def test_nozzle_temp_falls_back_to_filament_type(render, direction):
    joined = " ".join(render({"filament_type": "PLA+"}, direction))
    assert "Nozzle Temperature" in joined
    assert "210 °C" in joined


@pytest.mark.parametrize("direction", _DIRECTIONS)
def test_slicer_nozzle_temp_beats_fallback(render, direction):
    raw = {"filament_type": "PETG", "first_layer_extr_temp": 245.0}
    joined = " ".join(render(raw, direction))
    assert "245 °C" in joined
    assert "235 °C" not in joined


@pytest.mark.parametrize("direction", _DIRECTIONS)
def test_unknown_material_has_no_nozzle_fallback(render, direction):
    joined = " ".join(render({"filament_type": "Unobtainium"}, direction))
    assert "Nozzle Temperature" not in joined
