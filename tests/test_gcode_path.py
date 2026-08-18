import pytest
from pathlib import Path

from BlocksScreen.helper_methods import resolve_thumbnail_path, get_parent_dir, is_usb_mount

GCODE_ROOT = Path("/home/pi/printer_data/gcodes")


class TestThumbnailsPath:
    def test_usb_file_resolves_thumb_inside_usb_dir(self):
        result = resolve_thumbnail_path(
            GCODE_ROOT, "USB-BLOCKS/Cube.gcode", ".thumbs/Cube-300x300.png"
        )
        assert result == GCODE_ROOT / "USB-BLOCKS/.thumbs/Cube-300x300.png"

    def test_root_file_resolves_thumb_at_root(self):
        result = resolve_thumbnail_path(
            GCODE_ROOT, "Cube.gcode", ".thumbs/Cube-300x300.png"
        )
        assert result == GCODE_ROOT / ".thumbs/Cube-300x300.png"

class TestPathHelpers:
    def test_parent_of_root_file_is_empty(self):
        assert get_parent_dir("Cube.gcode") == ""

    def test_parent_of_nested_file(self):
        assert get_parent_dir("USB-BLOCKS/Cube.gcode") == "USB-BLOCKS"

    def test_usb_mount_only_at_root(self):
        assert is_usb_mount("USB-BLOCKS") is True
        assert is_usb_mount("USB-BLOCKS/sub") is False
        assert is_usb_mount("gcodes") is False

    def test_usb_mount_tolerates_leading_slash(self):
        assert is_usb_mount("/USB-BLOCKS") is True

    def test_usb_mount_accepts_unlabelled_stick_name(self):
        assert is_usb_mount("USB DRIVE") is True
        assert is_usb_mount("USB DRIVE 2") is True

    def test_usb_mount_rejects_empty(self):
        assert is_usb_mount("") is False
        assert is_usb_mount("/") is False

