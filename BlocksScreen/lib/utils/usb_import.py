"""Copies USB gcode files into local storage so prints survive drive removal."""

import filecmp
import logging
import os
import pathlib
import shutil

import helper_methods
from PyQt6 import QtCore

logger = logging.getLogger(__name__)

MB = 1024 * 1024
ALLOWED_EXT = frozenset({".gcode", ".gco", ".g"})
MIN_FREE_MARGIN = 64 * MB  # free space left on the SD card after the copy
TMP_DIR_NAME = ".usb_import_tmp"


class UsbImportError(Exception):
    """Import failure whose message is safe to show on screen."""


def _tmp_dir(gcode_root: pathlib.Path) -> pathlib.Path:
    """Scratch dir outside the gcodes tree, or the gcodes root if on another fs."""
    # Outside Moonraker's inotify tree the final rename reads as a plain create_file.
    tmp_dir = gcode_root.parent / TMP_DIR_NAME
    try:
        tmp_dir.mkdir(exist_ok=True)
        if os.stat(tmp_dir).st_dev == os.stat(gcode_root).st_dev:
            return tmp_dir  # same fs keeps os.replace atomic
    except OSError:
        pass
    return gcode_root


def _is_copy_of(cand: pathlib.Path, src: pathlib.Path, src_st: os.stat_result) -> bool:
    """True if *cand* already holds the bytes of *src*."""
    try:
        st = cand.stat()
    except FileNotFoundError:
        return False
    if not cand.is_file() or st.st_size != src_st.st_size:
        return False
    if st.st_mtime_ns == src_st.st_mtime_ns:
        return True  # copies keep the drive mtime, so this skips reading both files
    return filecmp.cmp(src, cand, shallow=False)  # stops at the first differing block


def _pick_destination(
    src: pathlib.Path, src_st: os.stat_result, dest_dir: pathlib.Path
) -> tuple[pathlib.Path, bool]:
    """(path, reused): an existing copy of *src*, else the first free name."""
    n = 0
    while True:
        cand = dest_dir / (src.name if n == 0 else f"{src.stem}_{n}{src.suffix}")
        if not cand.exists() and not cand.is_symlink():
            return cand, False
        if _is_copy_of(cand, src, src_st):
            return cand, True
        n += 1  # same name, other content: never overwrite a local file


def _fsync(path: pathlib.Path) -> None:
    """Flush *path* (file or directory) to disk."""
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _copy_atomic(
    src: pathlib.Path,
    src_st: os.stat_result,
    final: pathlib.Path,
    tmp_dir: pathlib.Path,
) -> None:
    """Copy *src* to *final* via a synced temp file, so *final* is never partial."""
    for stale in tmp_dir.glob(".*.part"):  # leftovers from a crash or power loss
        stale.unlink(missing_ok=True)
    free = shutil.disk_usage(final.parent).free
    if free < src_st.st_size + MIN_FREE_MARGIN:
        raise UsbImportError(f"Not enough free space ({free // MB} MB free)")
    tmp = tmp_dir / f".{final.name}.part"
    try:
        shutil.copyfile(src, tmp)  # kernel-side copy on Linux
        now = src.stat()
        if (now.st_size, now.st_mtime_ns) != (src_st.st_size, src_st.st_mtime_ns):
            raise UsbImportError("The file changed during the copy")
        if tmp.stat().st_size != src_st.st_size:
            raise UsbImportError("Copy incomplete")
        os.utime(tmp, ns=(src_st.st_atime_ns, src_st.st_mtime_ns))
        _fsync(tmp)
        os.replace(tmp, final)
        _fsync(final.parent)  # persist the rename itself across power loss
    finally:
        tmp.unlink(missing_ok=True)


def import_usb_gcode(gcode_root: pathlib.Path, filename: str) -> tuple[str, bool]:
    """Copy USB *filename* into *gcode_root*; returns (gcodes-relative name, reused)."""
    root = gcode_root.resolve()
    rel = filename.strip("/")
    if not helper_methods.is_usb_path(rel):
        raise UsbImportError("Not a USB file")
    usb_root = (root / rel.split("/", 1)[0]).resolve()
    src = (root / rel).resolve()
    if usb_root not in src.parents:  # symlinks or ".." escaping the drive
        raise UsbImportError("Invalid file path")
    if src.suffix.lower() not in ALLOWED_EXT:
        raise UsbImportError("Unsupported file type")
    if not os.path.ismount(usb_root) or not src.is_file():
        raise UsbImportError("File not found, was the USB drive removed?")
    try:
        src_st = src.stat()
        final, reused = _pick_destination(src, src_st, root)
        if not reused:
            _copy_atomic(src, src_st, final, _tmp_dir(root))
    except OSError as e:
        raise UsbImportError(
            f"Copy failed, was the USB drive removed? ({e.strerror})"
        ) from e
    logger.info("USB import %s -> %s (reused=%s)", rel, final.name, reused)
    return final.name, reused


class _ImportSignals(QtCore.QObject):
    """Worker result signal; QRunnable can't hold signals."""

    done = QtCore.pyqtSignal(str, str, str)  # (usb_file, local_file, error)


class UsbImportTask(QtCore.QRunnable):
    """Runs import_usb_gcode off the UI thread."""

    def __init__(self, gcode_root: pathlib.Path, filename: str) -> None:
        super().__init__()
        self.setAutoDelete(False)  # the caller holds it until done fires
        self._gcode_root = gcode_root
        self._filename = filename
        self.signals = _ImportSignals()

    @QtCore.pyqtSlot()
    def run(self) -> None:
        """Copy, then report (usb_file, local_file, "") or (usb_file, "", error)."""
        try:
            local, _ = import_usb_gcode(self._gcode_root, self._filename)
            self.signals.done.emit(self._filename, local, "")
        except UsbImportError as e:
            logger.warning("USB import of %s failed: %s", self._filename, e)
            self.signals.done.emit(self._filename, "", str(e))
        except Exception:  # never leave the loadscreen up on a bug
            logger.exception("USB import of %s crashed", self._filename)
            self.signals.done.emit(self._filename, "", "Unexpected error copying file")
