"""Files data layer: listings, metadata, history, USB events."""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Some conftests stub helper_methods; Files needs the real one.
_hm_path = Path(__file__).resolve().parents[2] / "BlocksScreen/helper_methods.py"
_spec = importlib.util.spec_from_file_location("helper_methods", _hm_path)
_hm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hm)
sys.modules["helper_methods"] = _hm

# Drop a conftest MagicMock so the real Files loads.
sys.modules.pop("lib.files", None)

from lib.files import Files  # noqa: E402


@pytest.fixture()
def files(qtbot):
    """Files with a mocked websocket."""
    return Files(None, MagicMock())


def _dir_response(files_list, dirs):
    """A server.files.get_directory response envelope."""
    return {"files": files_list, "dirs": dirs, "disk_usage": {}, "root_info": {}}


class TestProcessDirectoryInfo:
    def test_emits_file_list_and_dirs(self, files, qtbot):
        resp = _dir_response(
            [{"filename": "a.gcode", "modified": 2}], [{"dirname": "sub"}]
        )
        with qtbot.waitSignal(files.on_dirs, timeout=500):
            files._process_directory_info(resp)
        assert any(d.get("dirname") == "sub" for d in files.directories)

    def test_inline_metadata_emits_fileinfo_without_request(self, files, qtbot):
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
        resp = _dir_response([{"filename": "b.gcode", "modified": 2}], [])
        with qtbot.waitSignal(files.request_file_metadata, timeout=500):
            files._process_directory_info(resp)

    def test_inline_metadata_keyed_by_path(self, files, qtbot):
        """Entries keyed by 'path' keep their USB prefix."""
        resp = _dir_response(
            [{"path": "USB-BLOCKS/c.gcode", "modified": 2, "estimated_time": 60}], []
        )
        with qtbot.assertNotEmitted(files.request_file_metadata):
            with qtbot.waitSignal(files.fileinfo, timeout=500):
                files._process_directory_info(resp)

    def test_subdir_inline_emits_full_path(self, files, qtbot):
        """Bare subdir names emit as full paths, so thumbnails resolve."""
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
        files._process_directory_info(resp, "USB-BLOCKS")
        assert seen.get("filename") == "USB-BLOCKS/cube.gcode"

    def test_missing_metadata_requests_full_path(self, files, qtbot):
        resp = _dir_response([{"filename": "x.gcode", "modified": 1}], [])
        seen = []
        files.request_file_metadata.connect(seen.append)
        files._process_directory_info(resp, "sub")
        assert seen == ["sub/x.gcode"]

    def test_interleaved_dir_responses_use_their_own_dir(self, files):
        """A late response resolves against its own dir, not the newest."""
        seen = []
        files.request_file_metadata.connect(seen.append)
        files._process_directory_info(
            _dir_response([{"filename": "a.gcode", "modified": 1}], []), "dirA"
        )
        files._process_directory_info(
            _dir_response([{"filename": "b.gcode", "modified": 1}], []), "dirB"
        )
        assert seen == ["dirA/a.gcode", "dirB/b.gcode"]

    def test_relisting_skips_cached_file(self, files, qtbot):
        """Metadata is processed once per file, not on every listing."""
        entry = {"filename": "a.gcode", "size": 10, "modified": 2.0}
        files._process_metadata(entry | {"estimated_time": 60})
        with qtbot.assertNotEmitted(files.fileinfo):
            with qtbot.assertNotEmitted(files.request_file_metadata):
                files._process_directory_info(_dir_response([entry], []))

    @pytest.mark.parametrize("change", [{"size": 11}, {"modified": 3.0}])
    def test_changed_file_is_reprocessed(self, files, qtbot, change):
        """A new size or mtime invalidates, as in Moonraker's _has_valid_data."""
        entry = {"filename": "a.gcode", "size": 10, "modified": 2.0}
        files._process_metadata(entry | {"estimated_time": 60})
        with qtbot.waitSignal(files.request_file_metadata, timeout=500):
            files._process_directory_info(_dir_response([entry | change], []))


def _job(status: str, duration: float = 61.2) -> dict:
    """A server.history.get_job reply."""
    return {"job": {"print_duration": duration, "status": status}}


class TestHistoryPrintDuration:
    @pytest.fixture(autouse=True)
    def _listed(self, files):
        files._process_metadata(
            {"filename": "a.gcode", "modified": 2, "job_id": "000023"}
        )

    def test_listing_sends_no_history_rpc(self, files):
        """Durations are fetched on demand, not per listed file."""
        files.ws.api.history_get_job.assert_not_called()

    def test_asks_once_per_job(self, files):
        files.request_print_duration("a.gcode")
        files.request_print_duration("/a.gcode")
        files.ws.api.history_get_job.assert_called_once()
        assert files.ws.api.history_get_job.call_args.args[0] == "000023"

    def test_history_reply_updates_frozen_metadata(self, files, qtbot):
        """Frozen metadata is replaced, not mutated."""
        files.request_print_duration("a.gcode")
        callback = files.ws.api.history_get_job.call_args.args[1]
        with qtbot.waitSignal(files.fileinfo, timeout=500) as blocker:
            callback(_job("completed"))
        assert blocker.args[0]["print_duration"] == pytest.approx(61.2)
        assert files._files_metadata["a.gcode"].print_duration == pytest.approx(61.2)

    def test_cached_duration_applies_on_relisting(self, files):
        files._on_history_job("a.gcode", "000023", _job("completed"))
        files._files_metadata.clear()
        files._process_metadata(
            {"filename": "a.gcode", "modified": 2, "job_id": "000023"}
        )
        assert files._files_metadata["a.gcode"].print_duration == pytest.approx(61.2)

    def test_history_reply_ignored_when_absent(self, files, qtbot):
        """No usable duration leaves the metadata untouched."""
        with qtbot.assertNotEmitted(files.fileinfo):
            files._on_history_job("a.gcode", "000023", _job("completed", 0))
        assert files._files_metadata["a.gcode"].print_duration is None

    def test_cancelled_job_duration_is_ignored(self, files, qtbot):
        """A cancelled run stopped early, so its time misleads."""
        files.request_print_duration("a.gcode")
        with qtbot.assertNotEmitted(files.fileinfo):
            files._on_history_job("a.gcode", "000023", _job("cancelled"))
        assert files._files_metadata["a.gcode"].print_duration is None
        files.request_print_duration("a.gcode")
        files.ws.api.history_get_job.assert_called_once()

    def test_in_progress_job_is_asked_again(self, files):
        """A running job has no final duration yet."""
        files.request_print_duration("a.gcode")
        files._on_history_job("a.gcode", "000023", _job("in_progress"))
        files.request_print_duration("a.gcode")
        assert files.ws.api.history_get_job.call_count == 2


class TestFilelistNotifications:
    def test_every_batched_entry_is_applied(self, files):
        """Moonraker batches params; every entry must be handled."""
        files.handle_filelist_changed(
            {
                "params": [
                    {"action": "create_file", "item": {"path": "a.gcode"}},
                    {"action": "create_file", "item": {"path": "b.gcode"}},
                ]
            }
        )
        assert {"a.gcode", "b.gcode"} <= set(files._files)

    def test_other_roots_are_ignored(self, files):
        """A config dir must not appear in or remove from the gcodes list."""
        files._directories["backup"] = {"dirname": "backup"}
        for action in ("create_dir", "delete_dir"):
            item = {"root": "config", "path": "backup"}
            files.handle_filelist_changed({"action": action, "item": item})
        assert "backup" in files._directories
        files.handle_filelist_changed(
            {"action": "create_dir", "item": {"root": "config", "path": "extra"}}
        )
        assert "extra" not in files._directories

    def test_move_out_of_gcodes_removes_the_dir(self, files):
        """A cross-root move only deletes on our side."""
        files._directories["old"] = {"dirname": "old"}
        files.handle_filelist_changed(
            {
                "action": "move_dir",
                "item": {"root": "config", "path": "old"},
                "source_item": {"root": "gcodes", "path": "old"},
            }
        )
        assert "old" not in files._directories

    def test_bare_dict_notification_still_works(self, files):
        files.handle_filelist_changed(
            {"action": "create_file", "item": {"path": "a.gcode"}}
        )
        assert "a.gcode" in files._files


class TestUsbMountNotifications:
    """Root USB symlinks arrive as file events."""

    @pytest.mark.parametrize("action", ["create_file", "modify_file"])
    def test_symlink_event_becomes_a_directory(self, files, qtbot, action):
        """Any file action on a mount surfaces as a directory."""
        with qtbot.waitSignal(files.dir_added, timeout=500) as sig:
            files.handle_filelist_changed(
                {"action": action, "item": {"path": "USB-TESTE"}}
            )
        assert sig.args[0]["dirname"] == "USB-TESTE"
        assert "USB-TESTE" in files._directories

    def test_fallback_symlink_name_is_recognised(self, files, qtbot):
        """Unlabelled sticks link as 'USB DRIVE'."""
        with qtbot.waitSignal(files.dir_added, timeout=500):
            files.handle_filelist_changed(
                {"action": "modify_file", "item": {"path": "USB DRIVE 1"}}
            )
        assert "USB DRIVE 1" in files._directories

    def test_leading_slash_is_tolerated(self, files, qtbot):
        """Keys and the preload stay slash-free so its reply matches."""
        with qtbot.waitSignal(files.dir_added, timeout=500):
            files.handle_filelist_changed(
                {"action": "modify_file", "item": {"path": "/USB-TESTE"}}
            )
        assert "USB-TESTE" in files._directories
        assert files._pending_usb_preloads == {"USB-TESTE"}
        files.handle_filelist_changed(
            {"action": "delete_file", "item": {"path": "/USB-TESTE"}}
        )
        assert "USB-TESTE" not in files._directories
        assert not files._pending_usb_preloads

    def test_duplicate_mount_event_preloads_once(self, files):
        """A second reply would replace the shown listing."""
        for action in ("create_file", "modify_file"):
            files.handle_filelist_changed({"action": action, "item": {"path": "USB-X"}})
        files.ws.api.get_dir_information.assert_called_once_with("USB-X", True)

    def test_plain_file_modification_is_untouched(self, files, qtbot):
        """The USB re-route must not swallow normal modifications."""
        with qtbot.waitSignal(files.file_modified, timeout=500):
            files.handle_filelist_changed(
                {"action": "modify_file", "item": {"path": "a.gcode"}}
            )
        assert "a.gcode" in files._files


class TestThumbnails:
    def test_sorted_small_to_large_beside_the_gcode(self, files, qtbot):
        """Consumers take [-1] as largest; .thumbs sits beside the gcode."""
        with qtbot.waitSignal(files.fileinfo, timeout=500) as blocker:
            files._process_metadata(
                {
                    "filename": "sub/a.gcode",
                    "modified": 2,
                    "thumbnails": [
                        {"relative_path": ".thumbs/a-300x300.png", "size": 9000},
                        {"relative_path": ".thumbs/a-32x32.png", "size": 500},
                        {"relative_path": ""},
                        "junk",
                    ],
                }
            )
        assert blocker.args[0]["thumbnail_paths"] == [
            str(files.gcode_path / "sub/.thumbs/a-32x32.png"),
            str(files.gcode_path / "sub/.thumbs/a-300x300.png"),
        ]

    def test_no_thumbnail_rpc_when_metadata_has_none(self, files):
        """server.files.thumbnails reads the same metadata."""
        files._process_metadata({"filename": "a.gcode", "modified": 2})
        files.ws.api.get_gcode_thumbnail.assert_not_called()


class TestDirectoryNotifications:
    def test_nested_delete_emits_full_path(self, files, qtbot):
        """sub/x, not x, so a same-named root folder survives."""
        with qtbot.waitSignal(files.dir_removed, timeout=500) as sig:
            files.handle_filelist_changed(
                {"action": "delete_dir", "item": {"root": "gcodes", "path": "sub/x"}}
            )
        assert sig.args[0] == "sub/x"

    def test_usb_named_user_folder_is_not_preloaded(self, files):
        """A subdir named USB-* is a folder, not a mount."""
        files._preload_usb_contents = MagicMock()
        files.handle_filelist_changed(
            {"action": "create_dir", "item": {"root": "gcodes", "path": "sub/USB-x"}}
        )
        files._preload_usb_contents.assert_not_called()
        files.handle_filelist_changed(
            {"action": "create_dir", "item": {"root": "gcodes", "path": "USB-x"}}
        )
        files._preload_usb_contents.assert_called_once_with("USB-x")


@pytest.fixture()
def loader(monkeypatch):
    """Stand-in for the shared thumbnail loader."""
    fake = MagicMock()
    monkeypatch.setattr("lib.files.gcode_loader.get_loader", lambda: fake)
    monkeypatch.setattr("lib.files.gcode_loader.get_metadata_loader", lambda: None)
    return fake


class TestCacheInvalidation:
    def test_drive_removal_forgets_only_that_drive(self, files, loader):
        for name in ("USB-X/a.gcode", "USB-XY/b.gcode"):
            files._process_metadata({"filename": name, "modified": 1})
        files.handle_filelist_changed(
            {"action": "delete_file", "item": {"path": "USB-X"}}
        )
        assert set(files._files_metadata) == {"USB-XY/b.gcode"}
        loader.forget.assert_called_once_with("USB-X")

    def test_reupload_forgets_old_parse(self, files, loader):
        """A same-name upload arrives as modify_file."""
        files._process_metadata({"filename": "a.gcode", "modified": 1})
        files.handle_filelist_changed(
            {"action": "modify_file", "item": {"path": "a.gcode"}}
        )
        assert "a.gcode" not in files._files_metadata
        loader.forget.assert_called_once_with("a.gcode")


class TestUsbMetadataRouting:
    """Moonraker cannot scan read-only USB gcodes; they parse locally."""

    @pytest.fixture()
    def meta_loader(self, files, monkeypatch):
        fake = MagicMock()
        monkeypatch.setattr(files, "_usb_metadata_loader", lambda: fake)
        return fake

    def test_fileinfo_miss_parses_locally(self, files, qtbot, meta_loader):
        with qtbot.assertNotEmitted(files.request_file_metadata):
            files.on_request_fileinfo("/USB-X/a.gcode")
        meta_loader.request.assert_called_once_with("USB-X/a.gcode")

    def test_file_event_parses_locally(self, files, qtbot, meta_loader):
        item = {"path": "USB-X/a.gcode", "size": 5}
        with qtbot.assertNotEmitted(files.request_file_metadata):
            files.handle_filelist_changed({"action": "create_file", "item": item})
        meta_loader.request.assert_called_once_with("USB-X/a.gcode")
        assert files._usb_meta_base["USB-X/a.gcode"]["size"] == 5
