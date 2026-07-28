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


class TestHistoryPrintDuration:
    def test_history_reply_updates_frozen_metadata(self, files, qtbot):
        """A history reply re-emits fileinfo with print_duration (FileMetadata is frozen)."""
        files._process_metadata(
            {"filename": "a.gcode", "modified": 2, "job_id": "000023"}
        )
        with qtbot.waitSignal(files.fileinfo, timeout=500) as blocker:
            files._on_history_job(
                "a.gcode", {"job": {"print_duration": 61.2, "status": "completed"}}
            )
        assert blocker.args[0]["print_duration"] == pytest.approx(61.2)
        assert files._files_metadata["a.gcode"].print_duration == pytest.approx(61.2)

    def test_history_reply_ignored_when_absent(self, files, qtbot):
        """A job with no usable duration leaves the cache untouched."""
        files._process_metadata({"filename": "a.gcode", "modified": 2})
        with qtbot.assertNotEmitted(files.fileinfo):
            files._on_history_job(
                "a.gcode", {"job": {"print_duration": 0, "status": "completed"}}
            )
        assert files._files_metadata["a.gcode"].print_duration is None

    def test_cancelled_job_duration_is_ignored(self, files, qtbot):
        """A cancelled run stopped early, so its elapsed time does not describe the file."""
        files._process_metadata({"filename": "a.gcode", "modified": 2})
        with qtbot.assertNotEmitted(files.fileinfo):
            files._on_history_job(
                "a.gcode", {"job": {"print_duration": 61.2, "status": "cancelled"}}
            )
        assert files._files_metadata["a.gcode"].print_duration is None


class TestFilelistNotifications:
    def test_every_batched_entry_is_applied(self, files):
        """Moonraker batches params, so all entries must reach a handler, not just the first."""
        files.handle_filelist_changed(
            {
                "params": [
                    {"action": "create_file", "item": {"path": "a.gcode"}},
                    {"action": "create_file", "item": {"path": "b.gcode"}},
                ]
            }
        )
        assert {"a.gcode", "b.gcode"} <= set(files._files)

    def test_bare_dict_notification_still_works(self, files):
        """A non-batched notification stays supported."""
        files.handle_filelist_changed(
            {"action": "create_file", "item": {"path": "a.gcode"}}
        )
        assert "a.gcode" in files._files


class TestThumbnailProbe:
    def test_probes_moonraker_when_metadata_has_no_thumbnails(self, files, qtbot):
        """A scanned gcode without thumbnails is probed once and re-emitted with paths."""
        files._process_metadata({"filename": "a.gcode", "modified": 2})
        assert files.ws.api.get_gcode_thumbnail.call_count == 1
        with qtbot.waitSignal(files.fileinfo, timeout=500) as blocker:
            files._on_thumbnails("a.gcode", [{"thumbnail_path": "sub/.thumbs/a.png"}])
        assert blocker.args[0]["thumbnail_paths"] == [
            str(files.gcode_path / "sub/.thumbs/a.png")
        ]
        files._process_metadata({"filename": "a.gcode", "modified": 3})
        assert files.ws.api.get_gcode_thumbnail.call_count == 1

    def test_no_probe_when_thumbnails_already_known(self, files):
        """Inline thumbnails make the extra round trip pointless."""
        files._process_metadata(
            {
                "filename": "a.gcode",
                "modified": 2,
                "thumbnails": [{"relative_path": ".thumbs/a.png"}],
            }
        )
        files.ws.api.get_gcode_thumbnail.assert_not_called()
