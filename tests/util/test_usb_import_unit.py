"""import_usb_gcode copies USB gcodes into the gcodes root safely."""

import importlib.util
import os
import pathlib
import sys
import threading
from collections import namedtuple

import pytest

# tests/lib, a regular package, shadows the namespace package BlocksScreen/lib here.
_BLOCKSSCREEN = pathlib.Path(__file__).parents[2] / "BlocksScreen"
if str(_BLOCKSSCREEN) not in sys.path:
    sys.path.append(str(_BLOCKSSCREEN))  # usb_import's bare helper_methods import
_spec = importlib.util.spec_from_file_location(
    "_usb_import_under_test", _BLOCKSSCREEN / "lib" / "utils" / "usb_import.py"
)
usb_import = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(usb_import)
UsbImportError = usb_import.UsbImportError
import_usb_gcode = usb_import.import_usb_gcode
remember_import = usb_import.remember_import
COPIES = usb_import.COPIES_DIR_NAME

_Usage = namedtuple("_Usage", "total used free")


@pytest.fixture
def layout(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
    """printer_data/gcodes with a USB-STICK symlink to a fake mounted drive."""
    gcodes = tmp_path / "printer_data" / "gcodes"
    gcodes.mkdir(parents=True)
    drive = tmp_path / "media" / "stick"
    drive.mkdir(parents=True)
    (gcodes / "USB-STICK").symlink_to(drive)
    mounts = {drive.resolve()}
    monkeypatch.setattr(
        pathlib.Path, "is_mount", lambda p: pathlib.Path(p).resolve() in mounts
    )
    return gcodes, drive, mounts


def _state(gcodes: pathlib.Path) -> pathlib.Path:
    return gcodes.parent / usb_import.STATE_DIR_NAME


def test_copies_into_copies_dir(layout) -> None:
    gcodes, drive, _ = layout
    (drive / "sub").mkdir()
    (drive / "sub" / "cube.gcode").write_bytes(b"G28\n" * 1000)
    name, reused, key = import_usb_gcode(gcodes, "USB-STICK/sub/cube.gcode")
    assert (name, reused) == (f"{COPIES}/cube.gcode", False)
    assert len(key) == 64
    assert (gcodes / name).read_bytes() == b"G28\n" * 1000
    assert not list(_state(gcodes).glob("*.part"))


@pytest.mark.parametrize("local", [b"G28\n", b"G1\n", b"G29\n"])
def test_unindexed_same_name_file_gets_suffix(layout, local: bytes) -> None:
    # Even an equal file: it may never have gone through Moonraker's processing.
    gcodes, drive, _ = layout
    copies = gcodes / COPIES
    copies.mkdir()
    (drive / "cube.gcode").write_bytes(b"G28\n")
    (copies / "cube.gcode").write_bytes(local)
    assert import_usb_gcode(gcodes, "/USB-STICK/cube.gcode")[:2] == (
        f"{COPIES}/cube_1.gcode",
        False,
    )
    assert (copies / "cube.gcode").read_bytes() == local
    assert (copies / "cube_1.gcode").read_bytes() == b"G28\n"


def test_processed_copy_is_reused_through_index(layout) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"T0\n" * 50_000)
    name, _, key = import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    # Happy Hare's preprocessor rewrites the copy before it settles.
    (gcodes / name).write_bytes(b"; processed by HappyHare\nMMU_CHANGE_TOOL TOOL=0\n")
    remember_import(gcodes, key, name)
    assert import_usb_gcode(gcodes, "USB-STICK/cube.gcode") == (name, True, key)
    assert sorted(p.name for p in (gcodes / COPIES).iterdir()) == ["cube.gcode"]


def test_edited_indexed_copy_is_not_reused(layout) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    name, _, key = import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    remember_import(gcodes, key, name)
    (gcodes / name).write_bytes(b"G1 X10\n")  # replaced after indexing
    assert import_usb_gcode(gcodes, "USB-STICK/cube.gcode")[:2] == (
        f"{COPIES}/cube_1.gcode",
        False,
    )


def test_same_size_usb_edit_is_not_reused(layout) -> None:
    gcodes, drive, _ = layout
    src = drive / "cube.gcode"
    body = bytearray(b"G28\n" * 100_000)
    src.write_bytes(body)
    name, _, key = import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    remember_import(gcodes, key, name)
    body[200_000:200_003] = b"G29"  # mid-file, outside both samples, same size
    src.write_bytes(body)
    st = src.stat()
    os.utime(src, ns=(st.st_atime_ns, st.st_mtime_ns + 2_000_000_000))
    assert import_usb_gcode(gcodes, "USB-STICK/cube.gcode")[:2] == (
        f"{COPIES}/cube_1.gcode",
        False,
    )


def test_index_drops_deleted_copies(layout) -> None:
    gcodes, drive, _ = layout
    for n in ("a", "b"):
        (drive / f"{n}.gcode").write_bytes(n.encode())
        name, _, key = import_usb_gcode(gcodes, f"USB-STICK/{n}.gcode")
        remember_import(gcodes, key, name)
    (gcodes / COPIES / "a.gcode").unlink()
    (drive / "c.gcode").write_bytes(b"c")
    name, _, key = import_usb_gcode(gcodes, "USB-STICK/c.gcode")
    remember_import(gcodes, key, name)
    files = {v["file"] for v in usb_import._load_index(gcodes).values()}
    assert files == {f"{COPIES}/b.gcode", f"{COPIES}/c.gcode"}


def test_corrupt_index_falls_back_to_copy(layout) -> None:
    gcodes, drive, _ = layout
    _state(gcodes).mkdir()
    (_state(gcodes) / usb_import.INDEX_NAME).write_text("{not json")
    (drive / "cube.gcode").write_bytes(b"G28\n")
    assert import_usb_gcode(gcodes, "USB-STICK/cube.gcode")[:2] == (
        f"{COPIES}/cube.gcode",
        False,
    )


def test_key_differs_by_tail(layout) -> None:
    _, drive, _ = layout
    head = b"G28\n" * 40_000
    (drive / "a").mkdir()
    (drive / "b").mkdir()
    a, b = drive / "a" / "cube.gcode", drive / "b" / "cube.gcode"
    a.write_bytes(head + b"; layer_height = 0.2\n")
    b.write_bytes(head + b"; layer_height = 0.3\n")
    os.utime(b, ns=(a.stat().st_atime_ns, a.stat().st_mtime_ns))
    assert usb_import._source_key(a, a.stat()) != usb_import._source_key(b, b.stat())


def test_only_own_stale_part_files_are_cleaned(layout, monkeypatch) -> None:
    gcodes, drive, _ = layout
    # State dir on another fs: the temp file lands in the copies dir.
    monkeypatch.setattr(usb_import, "_tmp_dir", lambda _root, dest: dest)
    copies = gcodes / COPIES
    copies.mkdir()
    (copies / ".bs-usb-old.gcode.part").write_bytes(b"x")
    (copies / ".other-tool.gcode.part").write_bytes(b"x")
    (drive / "cube.gcode").write_bytes(b"G28\n")
    import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert not (copies / ".bs-usb-old.gcode.part").exists()
    assert (copies / ".other-tool.gcode.part").exists()


def test_later_imports_keep_running_copies_temp(layout) -> None:
    # An aborted copy still runs in the pool; a new import must not delete its temp.
    gcodes, drive, _ = layout
    (drive / "a.gcode").write_bytes(b"G28\n")
    (drive / "b.gcode").write_bytes(b"G1\n")
    import_usb_gcode(gcodes, "USB-STICK/a.gcode")
    running = _state(gcodes) / ".bs-usb-inflight.part"
    running.write_bytes(b"x")
    import_usb_gcode(gcodes, "USB-STICK/b.gcode")
    assert running.exists()


def test_name_taken_during_copy_gets_suffix(layout, monkeypatch) -> None:
    # A concurrent import committing the same name first must not be overwritten.
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    real_copy = usb_import._copy_file

    def copy_then_race(src, dst, cancelled):
        real_copy(src, dst, cancelled)
        (gcodes / COPIES / "cube.gcode").write_bytes(b"other")

    monkeypatch.setattr(usb_import, "_copy_file", copy_then_race)
    name, _, _ = import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert name == f"{COPIES}/cube_1.gcode"
    assert (gcodes / COPIES / "cube.gcode").read_bytes() == b"other"
    assert (gcodes / name).read_bytes() == b"G28\n"
    assert oct((gcodes / name).stat().st_mode & 0o777) == "0o644"


def test_name_taken_between_check_and_rename_gets_suffix(layout, monkeypatch) -> None:
    # Another process (scp, Moonraker upload) may create the name after the check.
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    real_free = usb_import._free_name

    def free_then_race(src, dest_dir):
        cand = real_free(src, dest_dir)
        if cand.name == "cube.gcode":
            cand.write_bytes(b"other")
        return cand

    monkeypatch.setattr(usb_import, "_free_name", free_then_race)
    name, _, _ = import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert name == f"{COPIES}/cube_1.gcode"
    assert (gcodes / COPIES / "cube.gcode").read_bytes() == b"other"


def test_rename_noreplace_keeps_existing_file(tmp_path) -> None:
    src, dst = tmp_path / "a", tmp_path / "b"
    src.write_text("new")
    dst.write_text("old")
    with pytest.raises(FileExistsError):
        usb_import._rename_noreplace(src, dst)
    assert (src.read_text(), dst.read_text()) == ("new", "old")


def test_cancelled_import_commits_nothing(layout) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    cancelled = threading.Event()
    cancelled.set()
    with pytest.raises(UsbImportError, match="Cancelled"):
        import_usb_gcode(gcodes, "USB-STICK/cube.gcode", cancelled=cancelled)
    assert not list((gcodes / COPIES).glob("*.gcode"))
    assert not list(_state(gcodes).glob("*.part"))


@pytest.mark.parametrize(
    ("filename", "message"),
    [
        ("cube.gcode", "Not a USB file"),
        ("USB-STICK/../../etc.gcode", "Invalid file path"),
        ("USB-STICK/escape.gcode", "Invalid file path"),
        ("USB-STICK/notes.txt", "Unsupported file type"),
        ("USB-STICK/part.gco", "Unsupported file type"),
        ("USB-STICK/missing.gcode", "File not found"),
    ],
)
def test_rejects_bad_requests(layout, filename: str, message: str) -> None:
    gcodes, drive, _ = layout
    (drive / "notes.txt").write_text("hi")
    (drive / "part.gco").write_text("G28")
    outside = gcodes.parent / "secret.gcode"
    outside.write_text("G28")
    (drive / "escape.gcode").symlink_to(outside)
    with pytest.raises(UsbImportError, match=message):
        import_usb_gcode(gcodes, filename)
    assert sorted(p.name for p in gcodes.iterdir()) == ["USB-STICK"]


def test_unmounted_drive_is_rejected(layout) -> None:
    gcodes, drive, mounts = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    mounts.clear()
    with pytest.raises(UsbImportError, match="was the USB drive removed"):
        import_usb_gcode(gcodes, "USB-STICK/cube.gcode")


def test_low_disk_space_is_rejected(layout, monkeypatch) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    monkeypatch.setattr(usb_import.shutil, "disk_usage", lambda _p: _Usage(0, 0, 10))
    with pytest.raises(UsbImportError, match="Not enough free space"):
        import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert not (gcodes / COPIES / "cube.gcode").exists()


def test_fsync_error_leaves_no_partial_file(layout, monkeypatch) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")

    def _fail(_fd: int) -> None:
        raise OSError(5, os.strerror(5))

    monkeypatch.setattr(usb_import.os, "fsync", _fail)
    with pytest.raises(UsbImportError, match="Copy failed"):
        import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert not list((gcodes / COPIES).iterdir())
    assert not list(_state(gcodes).glob("*.part"))


def test_dir_sync_error_keeps_committed_copy(layout, monkeypatch, caplog) -> None:
    # The file itself is synced; only the rename may be lost on power loss.
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    real_fsync = usb_import._fsync

    def _fail_dirs(path: pathlib.Path) -> None:
        if path.is_dir():
            raise OSError(22, os.strerror(22))
        real_fsync(path)

    monkeypatch.setattr(usb_import, "_fsync", _fail_dirs)
    name, _, _ = import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert (gcodes / name).read_bytes() == b"G28\n"
    assert "Could not sync" in caplog.text


def _aged_copies(gcodes: pathlib.Path, names: tuple[str, ...]) -> pathlib.Path:
    """Copies dir holding *names*, oldest mtime first."""
    copies = gcodes / COPIES
    copies.mkdir()
    for age, n in enumerate(names):
        f = copies / f"{n}.gcode"
        f.write_bytes(b"x")
        os.utime(f, ns=(age * 10**9, age * 10**9))
    (copies / "notes.txt").write_bytes(b"x")  # never ours to delete
    return copies


@pytest.mark.parametrize(
    ("job_file", "survivors"),
    [("", ["mid", "new"]), (f"{COPIES}/old.gcode", ["new", "old"])],
)
def test_oldest_copies_are_pruned(layout, monkeypatch, job_file, survivors) -> None:
    gcodes, drive, _ = layout
    monkeypatch.setattr(usb_import, "MAX_COPIES", 3)
    copies = _aged_copies(gcodes, ("old", "mid", "new"))
    (drive / "cube.gcode").write_bytes(b"G28\n")
    import_usb_gcode(gcodes, "USB-STICK/cube.gcode", job_file)
    left = sorted(p.stem for p in copies.glob("*.gcode"))
    assert left == sorted(["cube", *survivors])
    assert (copies / "notes.txt").exists()


def test_reprinted_copy_outlives_newer_copies(layout, monkeypatch) -> None:
    gcodes, drive, _ = layout
    monkeypatch.setattr(usb_import, "MAX_COPIES", 3)
    copies = _aged_copies(gcodes, ("old", "mid", "new"))
    remember_import(gcodes, "k", f"{COPIES}/old.gcode")  # printed again just now
    (drive / "cube.gcode").write_bytes(b"G28\n")
    import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert sorted(p.stem for p in copies.glob("*.gcode")) == ["cube", "new", "old"]


def test_deleted_copies_dir_is_recreated(layout, caplog) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    name, _, _ = import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert name == f"{COPIES}/cube.gcode"
    assert f"Recreated {COPIES}" in caplog.text


def test_ensure_copies_dir(tmp_path, caplog) -> None:
    usb_import.ensure_copies_dir(tmp_path)
    assert (tmp_path / COPIES).is_dir()
    usb_import.ensure_copies_dir(tmp_path / "missing")
    assert f"Could not create {COPIES}" in caplog.text


def test_task_reports_copy(layout, qtbot) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    signals = usb_import.UsbImportSignals()
    task = usb_import.UsbImportTask(signals, 7, gcodes, "USB-STICK/cube.gcode")
    assert task.autoDelete()
    with qtbot.waitSignal(signals.done) as blocker:
        task.run()
    token, usb_file, local, key, reused, error = blocker.args
    assert (token, usb_file, local, reused, error) == (
        7,
        "USB-STICK/cube.gcode",
        f"{COPIES}/cube.gcode",
        False,
        "",
    )
    assert key


def test_task_reports_error(layout, qtbot) -> None:
    gcodes, _, _ = layout
    signals = usb_import.UsbImportSignals()
    task = usb_import.UsbImportTask(signals, 1, gcodes, "USB-STICK/missing.gcode")
    with qtbot.waitSignal(signals.done) as blocker:
        task.run()
    assert blocker.args[:5] == [1, "USB-STICK/missing.gcode", "", "", False]
    assert "File not found" in blocker.args[5]


def test_background_remember_logs_index_errors(tmp_path, caplog) -> None:
    usb_import._remember_logged(tmp_path, "k", "missing.gcode")
    assert "Could not index USB copy missing.gcode" in caplog.text


def test_upper_case_copies_are_pruned(layout, monkeypatch) -> None:
    gcodes, drive, _ = layout
    monkeypatch.setattr(usb_import, "MAX_COPIES", 2)
    copies = _aged_copies(gcodes, ())
    for age, n in enumerate(("OLD.GCODE", "Mid.Gcode")):
        (copies / n).write_bytes(b"x")
        os.utime(copies / n, ns=(age * 10**9, age * 10**9))
    (drive / "cube.gcode").write_bytes(b"G28\n")
    import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert sorted(p.name for p in copies.iterdir()) == [
        "Mid.Gcode",
        "cube.gcode",
        "notes.txt",
    ]


def test_failed_import_prunes_nothing(layout, monkeypatch) -> None:
    gcodes, drive, _ = layout
    monkeypatch.setattr(usb_import, "MAX_COPIES", 1)
    copies = _aged_copies(gcodes, ("old",))
    (drive / "cube.gcode").write_bytes(b"G28\n")
    monkeypatch.setattr(usb_import.shutil, "disk_usage", lambda _p: _Usage(0, 0, 10))
    with pytest.raises(UsbImportError, match="Not enough free space"):
        import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert (copies / "old.gcode").exists()


def test_cancel_stops_a_running_copy(tmp_path, monkeypatch) -> None:
    # Klipper shut down mid-copy: the copy stops within one chunk, not at the end
    monkeypatch.setattr(usb_import, "CHUNK", 4)
    src, dst = tmp_path / "big.gcode", tmp_path / "big.part"
    src.write_bytes(b"G1 X1\n" * 64)
    usb_import._copy_file(src, dst, None)
    assert dst.read_bytes() == src.read_bytes()
    cancelled = threading.Event()
    cancelled.set()
    with pytest.raises(UsbImportError, match="Cancelled"):
        usb_import._copy_file(src, dst, cancelled)
    assert dst.stat().st_size == 0


def test_running_copies_reserve_their_space(tmp_path, monkeypatch) -> None:
    # Two imports both passed the free-space check before either temp file grew
    monkeypatch.setattr(usb_import, "MIN_FREE_MARGIN", 0)
    monkeypatch.setattr(usb_import.shutil, "disk_usage", lambda _p: _Usage(0, 0, 100))
    with usb_import._reserve_space(tmp_path, 60):
        with pytest.raises(UsbImportError, match="40 MB|0 MB"):
            with usb_import._reserve_space(tmp_path, 60):
                pass
    with usb_import._reserve_space(tmp_path, 60):
        assert usb_import._reserved
    assert not usb_import._reserved
