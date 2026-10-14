"""USB symlink lifecycle in udisks2: announce and reap."""

import importlib.util
import pathlib
import sys
import types

import pytest

# Load by path: tests/panels mocks devices.storage, tests/lib shadows lib.
_SRC = pathlib.Path(__file__).resolve().parents[2] / "BlocksScreen"
_STORAGE = _SRC / "devices/storage"
_PKG = "_udisks_under_test"
if _PKG not in sys.modules:
    _pkg = types.ModuleType(_PKG)
    _pkg.__path__ = [str(_STORAGE)]
    sys.modules[_PKG] = _pkg


def _load(name: str, path: pathlib.Path) -> types.ModuleType:
    """Exec *path* as module *name*."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


helper_methods = _load(f"{_PKG}.helper_methods", _SRC / "helper_methods.py")
with pytest.MonkeyPatch.context() as _mp:
    # tests/lib mocks helper_methods; udisks2 needs the real one.
    _mp.setitem(sys.modules, "helper_methods", helper_methods)
    _udisks2 = _load(f"{_PKG}.udisks2", _STORAGE / "udisks2.py")
UDisksDBusAsync = _udisks2.UDisksDBusAsync


class _Signal:
    """Records emits; supports udisks2's sig[str] form."""

    def __init__(self):
        self.emitted = []

    def __getitem__(self, _types):
        return self

    def emit(self, *args):
        self.emitted.append(args)


class _Udisks:
    """UDisksDBusAsync symlink bits, no D-Bus session."""

    _is_symlink_live = UDisksDBusAsync._is_symlink_live
    _cleanup_broken_symlinks = UDisksDBusAsync._cleanup_broken_symlinks
    rem_symlink = UDisksDBusAsync.rem_symlink
    add_symlink = UDisksDBusAsync.add_symlink
    _announce_mount = UDisksDBusAsync._announce_mount

    def __init__(self, gcodes_path):
        self.gcodes_path = gcodes_path
        self.device_unmounted = _Signal()
        self.device_mounted = _Signal()


@pytest.fixture()
def udisks(tmp_path):
    """Stub rooted at an empty gcodes dir."""
    gcodes = tmp_path / "gcodes"
    gcodes.mkdir()
    return _Udisks(gcodes)


class TestSymlinkLiveness:
    def test_dangling_link_is_dead(self, udisks, tmp_path):
        link = udisks.gcodes_path / "USB-TESTE"
        link.symlink_to(tmp_path / "missing")
        assert udisks._is_symlink_live(link) is False

    def test_usb_link_to_plain_dir_is_dead(self, udisks, tmp_path):
        """A leftover mountpoint dir must not look like a live drive."""
        stale = tmp_path / "media" / "TESTE"
        stale.mkdir(parents=True)
        link = udisks.gcodes_path / "USB-TESTE"
        link.symlink_to(stale)
        assert udisks._is_symlink_live(link) is False

    def test_non_usb_link_to_plain_dir_is_left_alone(self, udisks, tmp_path):
        """Links we did not create are never reaped."""
        target = tmp_path / "my_prints"
        target.mkdir()
        link = udisks.gcodes_path / "my_prints"
        link.symlink_to(target)
        assert udisks._is_symlink_live(link) is True

    def test_real_mountpoint_is_live(self, udisks, monkeypatch, tmp_path):
        target = tmp_path / "media" / "TESTE"
        target.mkdir(parents=True)
        link = udisks.gcodes_path / "USB-TESTE"
        link.symlink_to(target)
        monkeypatch.setattr("os.path.ismount", lambda p: str(p) == str(target))
        assert udisks._is_symlink_live(link) is True


class TestCleanup:
    def test_dead_link_is_removed_and_announced(self, udisks, tmp_path):
        """Announce only after the unlink, or the refresh still lists it."""
        link = udisks.gcodes_path / "USB-TESTE"
        link.symlink_to(tmp_path / "missing")
        udisks._cleanup_broken_symlinks()
        assert not link.is_symlink()
        assert udisks.device_unmounted.emitted == [(link.as_posix(),)]

    def test_live_link_survives_and_is_silent(self, udisks, monkeypatch, tmp_path):
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
        assert udisks._announce_mount("/dev/sda1", "/gcodes/USB-TESTE") == (
            "/gcodes/USB-TESTE"
        )
        assert udisks.device_mounted.emitted == [("/dev/sda1", "/gcodes/USB-TESTE")]

    def test_failed_symlink_is_not_announced(self, udisks):
        """add_symlink returns '' on failure."""
        assert udisks._announce_mount("/dev/sda1", "") == ""
        assert udisks.device_mounted.emitted == []


class TestSymlinkNaming:
    """add_symlink names must pass the files UI USB check."""

    def _mount(self, tmp_path, name):
        target = tmp_path / "media" / name
        target.mkdir(parents=True)
        return target.as_posix()

    def test_labelled_drive_gets_usb_prefix(self, udisks, tmp_path):
        link = udisks.add_symlink(
            self._mount(tmp_path, "a"), udisks.gcodes_path.as_posix(), "TESTE"
        )
        assert pathlib.Path(link).name == "USB-TESTE"
        assert helper_methods.is_usb_mount(pathlib.Path(link).name)

    def test_unlabelled_drives_get_numbered_fallback(self, udisks, tmp_path):
        gcodes = udisks.gcodes_path.as_posix()
        first = udisks.add_symlink(self._mount(tmp_path, "a"), gcodes)
        second = udisks.add_symlink(self._mount(tmp_path, "b"), gcodes)
        names = [pathlib.Path(p).name for p in (first, second)]
        assert names == ["USB DRIVE", "USB DRIVE 1"]
        assert all(helper_methods.is_usb_mount(n) for n in names)
