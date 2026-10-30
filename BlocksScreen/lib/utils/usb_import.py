"""Copies USB gcode files into local storage so prints survive drive removal."""

import filecmp
import hashlib
import json
import logging
import os
import pathlib
import shutil

import helper_methods
from PyQt6 import QtCore

logger = logging.getLogger(__name__)

MB = 1024 * 1024
ALLOWED_EXT = ".gcode"  # the only extension lib.files lists and notifies
MIN_FREE_MARGIN = 64 * MB  # free space left on the SD card after the copy
SAMPLE = 64 * 1024
STATE_DIR_NAME = ".usb_import"
INDEX_NAME = "index.json"


class UsbImportError(Exception):
    """Import failure whose message is safe to show on screen."""


def _state_dir(gcode_root: pathlib.Path) -> pathlib.Path:
    """Index and scratch dir, beside the gcodes tree so Moonraker never lists it."""
    return gcode_root.parent / STATE_DIR_NAME


def _source_key(src: pathlib.Path, size: int) -> str:
    """Identity of a USB file from its name, size, head and tail."""
    # Slicers stamp the header and append their config, so ends differ per slice.
    h = hashlib.sha256(f"{src.name}\0{size}\0".encode())
    with src.open("rb") as f:
        h.update(f.read(SAMPLE))
        if size > SAMPLE:
            f.seek(max(SAMPLE, size - SAMPLE))
            h.update(f.read(SAMPLE))
    return h.hexdigest()


def _load_index(gcode_root: pathlib.Path) -> dict:
    """Source key -> {file, size, mtime_ns} of earlier imports; empty if unreadable."""
    try:
        data = json.loads((_state_dir(gcode_root) / INDEX_NAME).read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _indexed_copy(gcode_root: pathlib.Path, key: str) -> pathlib.Path | None:
    """The earlier local copy for *key*, if it is still there and untouched."""
    entry = _load_index(gcode_root).get(key)
    if not isinstance(entry, dict) or not isinstance(entry.get("file"), str):
        return None
    local = gcode_root / entry["file"]
    try:
        st = local.stat()
    except OSError:
        return None
    if (st.st_size, st.st_mtime_ns) != (entry.get("size"), entry.get("mtime_ns")):
        return None  # replaced or edited since, so it may no longer be this file
    return local


def remember_import(gcode_root: pathlib.Path, key: str, local_name: str) -> None:
    """Record *local_name* as the copy for *key*, once Moonraker has processed it."""
    # Moonraker and Happy Hare rewrite new gcodes, so the copy is only final now.
    root = gcode_root.resolve()
    st = (root / local_name).stat()
    index = {
        k: v
        for k, v in _load_index(root).items()
        if isinstance(v, dict) and (root / str(v.get("file"))).is_file()
    }
    index[key] = {"file": local_name, "size": st.st_size, "mtime_ns": st.st_mtime_ns}
    state = _state_dir(root)
    state.mkdir(exist_ok=True)
    tmp = state / f".{INDEX_NAME}.part"
    tmp.write_text(json.dumps(index, indent=1))
    os.replace(tmp, state / INDEX_NAME)


def _tmp_dir(gcode_root: pathlib.Path) -> pathlib.Path:
    """Scratch dir outside the gcodes tree, or the gcodes root if on another fs."""
    # Outside Moonraker's inotify tree the final rename reads as a plain create_file.
    tmp_dir = _state_dir(gcode_root)
    try:
        tmp_dir.mkdir(exist_ok=True)
        if os.stat(tmp_dir).st_dev == os.stat(gcode_root).st_dev:
            return tmp_dir  # same fs keeps os.replace atomic
    except OSError:
        pass
    return gcode_root


def _pick_destination(
    src: pathlib.Path, size: int, dest_dir: pathlib.Path
) -> tuple[pathlib.Path, bool]:
    """(path, reused): a byte-identical existing file, else the first free name."""
    n = 0
    while True:
        cand = dest_dir / (src.name if n == 0 else f"{src.stem}_{n}{src.suffix}")
        if not cand.exists() and not cand.is_symlink():
            return cand, False
        if (
            cand.is_file()
            and cand.stat().st_size == size
            and filecmp.cmp(src, cand, shallow=False)
        ):
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
        _fsync(tmp)
        os.replace(tmp, final)
        _fsync(final.parent)  # persist the rename itself across power loss
    finally:
        tmp.unlink(missing_ok=True)


def import_usb_gcode(gcode_root: pathlib.Path, filename: str) -> tuple[str, bool, str]:
    """Copy USB *filename* into *gcode_root*; returns (local name, reused, key)."""
    root = gcode_root.resolve()
    rel = filename.strip("/")
    if not helper_methods.is_usb_path(rel):
        raise UsbImportError("Not a USB file")
    usb_root = (root / rel.split("/", 1)[0]).resolve()
    src = (root / rel).resolve()
    if usb_root not in src.parents:  # symlinks or ".." escaping the drive
        raise UsbImportError("Invalid file path")
    if src.suffix.lower() != ALLOWED_EXT:
        raise UsbImportError("Unsupported file type")
    if not os.path.ismount(usb_root) or not src.is_file():
        raise UsbImportError("File not found, was the USB drive removed?")
    try:
        src_st = src.stat()
        key = _source_key(src, src_st.st_size)
        final, reused = _indexed_copy(root, key), True
        if final is None:
            final, reused = _pick_destination(src, src_st.st_size, root)
        if not reused:
            _copy_atomic(src, src_st, final, _tmp_dir(root))
    except OSError as e:
        raise UsbImportError(
            f"Copy failed, was the USB drive removed? ({e.strerror})"
        ) from e
    logger.info("USB import %s -> %s (reused=%s)", rel, final.name, reused)
    return final.name, reused, key


class _ImportSignals(QtCore.QObject):
    """Worker result signal; QRunnable can't hold signals."""

    # (usb_file, local_file, key, reused, error)
    done = QtCore.pyqtSignal(str, str, str, bool, str)


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
        """Copy, then report the local copy or the error text."""
        try:
            local, reused, key = import_usb_gcode(self._gcode_root, self._filename)
            self.signals.done.emit(self._filename, local, key, reused, "")
        except UsbImportError as e:
            logger.warning("USB import of %s failed: %s", self._filename, e)
            self.signals.done.emit(self._filename, "", "", False, str(e))
        except Exception:  # never leave the loadscreen up on a bug
            logger.exception("USB import of %s crashed", self._filename)
            self.signals.done.emit(
                self._filename, "", "", False, "Unexpected error copying file"
            )
