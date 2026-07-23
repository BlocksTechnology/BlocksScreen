"""Contract tests for Files (files.py) directory-load + metadata flow."""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Force real helper_methods (some conftests stub it); Files needs real path logic.
_hm_path = Path(__file__).resolve().parents[2] / "BlocksScreen/helper_methods.py"
_spec = importlib.util.spec_from_file_location("helper_methods", _hm_path)
_hm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hm)
sys.modules["helper_methods"] = _hm

# Drop any stale MagicMock left by other conftests so the real Files loads.
sys.modules.pop("lib.files", None)

from lib.files import Files  # noqa: E402


@pytest.fixture()
def files(qtbot):
    """A Files data layer with a mocked websocket backend."""
    return Files(None, MagicMock())


def _dir_response(files_list, dirs):
    """A server.files.get_directory response envelope."""
    return {"files": files_list, "dirs": dirs, "disk_usage": {}, "root_info": {}}


class TestProcessDirectoryInfo:
    def test_emits_file_list_and_dirs(self, files, qtbot):
        """A directory load publishes the file list and directory list."""
        resp = _dir_response(
            [{"filename": "a.gcode", "modified": 2}], [{"dirname": "sub"}]
        )
        with qtbot.waitSignal(files.on_dirs, timeout=500):
            files._process_directory_info(resp)
        assert any(d.get("dirname") == "sub" for d in files.directories)

    def test_inline_metadata_emits_fileinfo_without_request(self, files, qtbot):
        """Extended metadata is used inline: emit fileinfo, no redundant request."""
        resp = _dir_response(
            [
                {
                    "filename": "a.gcode",
                    "modified": 2,
                    "estimated_time": 3600,
                    "filament_total": 5.0,
                    "thumbnails": [],
                }
            ],
            [],
        )
        with qtbot.assertNotEmitted(files.request_file_metadata):
            with qtbot.waitSignal(files.fileinfo, timeout=500):
                files._process_directory_info(resp)

    def test_missing_metadata_requests_it(self, files, qtbot):
        """A gcode file with no inline metadata triggers a metadata request."""
        resp = _dir_response([{"filename": "b.gcode", "modified": 2}], [])
        with qtbot.waitSignal(files.request_file_metadata, timeout=500):
            files._process_directory_info(resp)

    def test_inline_metadata_keyed_by_path(self, files, qtbot):
        """Inline entries keyed by 'path' (USB prefix kept) still emit fileinfo."""
        resp = _dir_response(
            [{"path": "USB-BLOCKS/c.gcode", "modified": 2, "estimated_time": 60}], []
        )
        with qtbot.assertNotEmitted(files.request_file_metadata):
            with qtbot.waitSignal(files.fileinfo, timeout=500):
                files._process_directory_info(resp)

    def test_subdir_inline_emits_full_path(self, files, qtbot):
        """Bare subdir filenames are emitted as full USB/subdir paths (BUG-2 + thumbs)."""
        files._requested_dir = "USB-BLOCKS"
        resp = _dir_response(
            [
                {
                    "filename": "cube.gcode",
                    "modified": 1,
                    "estimated_time": 60,
                    "thumbnails": [{"relative_path": ".thumbs/cube.png"}],
                }
            ],
            [],
        )
        seen = {}
        files.fileinfo.connect(lambda d: seen.update(d))
        files._process_directory_info(resp)
        assert seen.get("filename") == "USB-BLOCKS/cube.gcode"

    def test_missing_metadata_requests_full_path(self, files, qtbot):
        """Fallback metadata request uses the full subdir path, not the bare name."""
        files._requested_dir = "sub"
        resp = _dir_response([{"filename": "x.gcode", "modified": 1}], [])
        seen = []
        files.request_file_metadata.connect(seen.append)
        files._process_directory_info(resp)
        assert seen == ["sub/x.gcode"]
