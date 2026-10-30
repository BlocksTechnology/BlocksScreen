"""import_usb_gcode copies USB gcodes into the gcodes root safely."""

import filecmp
import os
import pathlib
from collections import namedtuple

import pytest
from lib.utils import usb_import
from lib.utils.usb_import import UsbImportError, import_usb_gcode

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
        usb_import.os.path, "ismount", lambda p: pathlib.Path(p).resolve() in mounts
    )
    return gcodes, drive, mounts


def test_copies_into_gcodes_root(layout) -> None:
    gcodes, drive, _ = layout
    (drive / "sub").mkdir()
    (drive / "sub" / "cube.gcode").write_bytes(b"G28\n" * 1000)
    name, reused = import_usb_gcode(gcodes, "USB-STICK/sub/cube.gcode")
    assert (name, reused) == ("cube.gcode", False)
    assert (gcodes / "cube.gcode").read_bytes() == b"G28\n" * 1000
    assert not list((gcodes.parent / usb_import.TMP_DIR_NAME).iterdir())


def test_identical_copy_is_reused(layout) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    (gcodes / "cube.gcode").write_bytes(b"G28\n")
    assert import_usb_gcode(gcodes, "USB-STICK/cube.gcode") == ("cube.gcode", True)
    assert sorted(p.name for p in gcodes.iterdir()) == ["USB-STICK", "cube.gcode"]


def test_same_name_different_content_gets_suffix(layout) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    (gcodes / "cube.gcode").write_bytes(b"G1\n")
    assert import_usb_gcode(gcodes, "/USB-STICK/cube.gcode") == ("cube_1.gcode", False)
    assert (gcodes / "cube.gcode").read_bytes() == b"G1\n"
    assert (gcodes / "cube_1.gcode").read_bytes() == b"G28\n"


def test_second_import_reuses_without_reading(layout, monkeypatch) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n" * 10)
    assert import_usb_gcode(gcodes, "USB-STICK/cube.gcode") == ("cube.gcode", False)

    def _no_read(*_args) -> bool:
        raise AssertionError("matching mtime must skip the byte compare")

    monkeypatch.setattr(filecmp, "cmp", _no_read)
    assert import_usb_gcode(gcodes, "USB-STICK/cube.gcode") == ("cube.gcode", True)


def test_same_size_different_content_gets_suffix(layout) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    (gcodes / "cube.gcode").write_bytes(b"G29\n")
    assert import_usb_gcode(gcodes, "USB-STICK/cube.gcode") == ("cube_1.gcode", False)
    assert (gcodes / "cube.gcode").read_bytes() == b"G29\n"


def test_reuses_matching_suffixed_copy(layout) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")
    (gcodes / "cube.gcode").write_bytes(b"G1\n")
    (gcodes / "cube_1.gcode").write_bytes(b"G28\n")
    assert import_usb_gcode(gcodes, "USB-STICK/cube.gcode") == ("cube_1.gcode", True)


def test_stale_part_files_are_cleaned(layout) -> None:
    gcodes, drive, _ = layout
    tmp = gcodes.parent / usb_import.TMP_DIR_NAME
    tmp.mkdir()
    (tmp / ".old.gcode.part").write_bytes(b"x")
    (drive / "cube.gcode").write_bytes(b"G28\n")
    import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert not (tmp / ".old.gcode.part").exists()


@pytest.mark.parametrize(
    ("filename", "message"),
    [
        ("cube.gcode", "Not a USB file"),
        ("USB-STICK/../../etc.gcode", "Invalid file path"),
        ("USB-STICK/escape.gcode", "Invalid file path"),
        ("USB-STICK/notes.txt", "Unsupported file type"),
        ("USB-STICK/missing.gcode", "File not found"),
    ],
)
def test_rejects_bad_requests(layout, filename: str, message: str) -> None:
    gcodes, drive, _ = layout
    (drive / "notes.txt").write_text("hi")
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
    assert not (gcodes / "cube.gcode").exists()


def test_read_error_leaves_no_partial_file(layout, monkeypatch) -> None:
    gcodes, drive, _ = layout
    (drive / "cube.gcode").write_bytes(b"G28\n")

    def _fail(_fd: int) -> None:
        raise OSError(5, os.strerror(5))

    monkeypatch.setattr(usb_import.os, "fsync", _fail)
    with pytest.raises(UsbImportError, match="Copy failed"):
        import_usb_gcode(gcodes, "USB-STICK/cube.gcode")
    assert sorted(p.name for p in gcodes.iterdir()) == ["USB-STICK"]
    assert not list((gcodes.parent / usb_import.TMP_DIR_NAME).iterdir())


def test_task_reports_error(layout, qtbot) -> None:
    gcodes, _, _ = layout
    task = usb_import.UsbImportTask(gcodes, "USB-STICK/missing.gcode")
    with qtbot.waitSignal(task.signals.done) as blocker:
        task.run()
    assert blocker.args[0] == "USB-STICK/missing.gcode"
    assert blocker.args[1] == ""
    assert "File not found" in blocker.args[2]
