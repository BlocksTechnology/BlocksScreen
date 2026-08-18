"""Contract tests for the USB symlink lifecycle in udisks2 (mount announce + reap)."""

import importlib.util
import pathlib
import sys
import types

import pytest

# Load udisks2 by path under a private package: tests/panels stubs devices.storage
# with a MagicMock, and tests/lib shadows the real lib package on sys.path.
_STORAGE = pathlib.Path(__file__).resolve().parents[2] / "BlocksScreen/devices/storage"
_PKG = "_udisks_under_test"
if _PKG not in sys.modules:
    _pkg = types.ModuleType(_PKG)
    _pkg.__path__ = [str(_STORAGE)]
    sys.modules[_PKG] = _pkg
_spec = importlib.util.spec_from_file_location(
    f"{_PKG}.udisks2", _STORAGE / "udisks2.py"
)
_udisks2 = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _udisks2
_spec.loader.exec_module(_udisks2)
UDisksDBusAsync = _udisks2.UDisksDBusAsync


class _Signal:
    """Records emissions and accepts the sig[str] subscript form used in udisks2."""

    def __init__(self):
        self.emitted = []

    def __getitem__(self, _types):
        return self

    def emit(self, *args):
        self.emitted.append(args)


class _Udisks:
    """The bits of UDisksDBusAsync the symlink helpers touch, without a D-Bus session."""

    _is_symlink_live = UDisksDBusAsync._is_symlink_live
    _cleanup_broken_symlinks = UDisksDBusAsync._cleanup_broken_symlinks
    rem_symlink = UDisksDBusAsync.rem_symlink
    _announce_mount = UDisksDBusAsync._announce_mount

    def __init__(self, gcodes_path):
        self.gcodes_path = gcodes_path
        self.device_unmounted = _Signal()
        self.device_mounted = _Signal()


@pytest.fixture()
def udisks(tmp_path):
    """A stub instance rooted at an empty fake gcodes directory."""
    gcodes = tmp_path / "gcodes"
    gcodes.mkdir()
    return _Udisks(gcodes)


class TestSymlinkLiveness:
    def test_dangling_link_is_dead(self, udisks, tmp_path):
        """The classic case: the target directory is gone."""
        link = udisks.gcodes_path / "USB-TESTE"
        link.symlink_to(tmp_path / "missing")
        assert udisks._is_symlink_live(link) is False

    def test_usb_link_to_plain_dir_is_dead(self, udisks, tmp_path):
        """A leftover mountpoint dir must not keep a yanked drive looking healthy."""
        stale = tmp_path / "media" / "TESTE"
        stale.mkdir(parents=True)
        link = udisks.gcodes_path / "USB-TESTE"
        link.symlink_to(stale)
        assert udisks._is_symlink_live(link) is False

    def test_non_usb_link_to_plain_dir_is_left_alone(self, udisks, tmp_path):
        """Links this module did not create are never reaped, mountpoint or not."""
        target = tmp_path / "my_prints"
        target.mkdir()
        link = udisks.gcodes_path / "my_prints"
        link.symlink_to(target)
        assert udisks._is_symlink_live(link) is True

    def test_real_mountpoint_is_live(self, udisks, monkeypatch, tmp_path):
        """A mounted drive stays listed."""
        target = tmp_path / "media" / "TESTE"
        target.mkdir(parents=True)
        link = udisks.gcodes_path / "USB-TESTE"
        link.symlink_to(target)
        monkeypatch.setattr("os.path.ismount", lambda p: str(p) == str(target))
        assert udisks._is_symlink_live(link) is True


class TestCleanup:
    def test_dead_link_is_removed_and_announced(self, udisks, tmp_path):
        """The UI only refreshes if the reap is announced, and only after the unlink."""
        link = udisks.gcodes_path / "USB-TESTE"
        link.symlink_to(tmp_path / "missing")
        udisks._cleanup_broken_symlinks()
        assert not link.is_symlink()
        assert udisks.device_unmounted.emitted == [(link.as_posix(),)]

    def test_live_link_survives_and_is_silent(self, udisks, monkeypatch, tmp_path):
        """A still-mounted drive is not reaped and raises no removal signal."""
        target = tmp_path / "media" / "TESTE"
        target.mkdir(parents=True)
        link = udisks.gcodes_path / "USB-TESTE"
        link.symlink_to(target)
        monkeypatch.setattr("os.path.ismount", lambda p: str(p) == str(target))
        udisks._cleanup_broken_symlinks()
        assert link.is_symlink()
        assert udisks.device_unmounted.emitted == []


class TestAnnounceMount:
    def test_successful_symlink_is_announced(self, udisks):
        """Without this signal the file view never learns the USB folder appeared."""
        assert udisks._announce_mount("/dev/sda1", "/gcodes/USB-TESTE") == (
            "/gcodes/USB-TESTE"
        )
        assert udisks.device_mounted.emitted == [("/dev/sda1", "/gcodes/USB-TESTE")]

    def test_failed_symlink_is_not_announced(self, udisks):
        """add_symlink returns '' on failure, refreshing then would show nothing."""
        assert udisks._announce_mount("/dev/sda1", "") == ""
        assert udisks.device_mounted.emitted == []
