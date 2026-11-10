"""Copies USB gcode files into local storage so prints survive drive removal."""

import functools
import hashlib
import json
import logging
import os
import pathlib
import shutil
import tempfile
import threading
import time

import helper_methods
from PyQt6 import QtCore

logger = logging.getLogger(__name__)

MB = 1024 * 1024
ALLOWED_EXT = ".gcode"  # the only extension lib.files lists and notifies
MIN_FREE_MARGIN = 64 * MB  # free space left on the SD card after the copy
SAMPLE = 64 * 1024
STATE_DIR_NAME = ".usb_import"
INDEX_NAME = "index.json"
PART_PREFIX = ".bs-usb-"  # scopes the stale-temp sweep to our own files
COPIES_DIR_NAME = "usb_copies"  # must not match helper_methods.USB_LINK_PREFIXES
MAX_COPIES = 20  # least recently used beyond this are deleted, never the current job
_INDEX_LOCK = threading.Lock()  # the index is written from pool threads
_COMMIT_LOCK = threading.Lock()  # name pick + rename, so two copies never pick one name
_SWEPT: set[pathlib.Path] = set()  # temp dirs already cleaned in this process


class UsbImportError(Exception):
    """Import failure whose message is safe to show on screen."""


def _state_dir(gcode_root: pathlib.Path) -> pathlib.Path:
    """Index and scratch dir, beside the gcodes tree so Moonraker never lists it."""
    return gcode_root.parent / STATE_DIR_NAME


def _source_key(src: pathlib.Path, st: os.stat_result) -> str:
    """Identity of a USB file from its name, size, mtime, head and tail."""
    # rsync's quick check (size + mtime) plus samples; a false miss only costs a copy.
    size = st.st_size
    h = hashlib.sha256(f"{src.name}\0{size}\0{st.st_mtime_ns}\0".encode())
    with src.open("rb") as f:
        h.update(f.read(SAMPLE))
        if size > SAMPLE:
            f.seek(max(SAMPLE, size - SAMPLE))
            h.update(f.read(SAMPLE))
    return h.hexdigest()


def _load_index(gcode_root: pathlib.Path) -> dict:
    """Source key -> {file, size, mtime_ns, used_ns} of imports; empty if unreadable."""
    try:
        data = json.loads((_state_dir(gcode_root) / INDEX_NAME).read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _indexed_copy(gcode_root: pathlib.Path, key: str) -> pathlib.Path | None:
    """The earlier local copy for *key*, if it is still there and untouched."""
    with _INDEX_LOCK:
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
    """Record *local_name* as the copy for *key* and mark it used, once processed."""
    # Moonraker and Happy Hare rewrite new gcodes, so the copy is only final now.
    root = gcode_root.resolve()
    st = (root / local_name).stat()
    with _INDEX_LOCK:
        index = {
            k: v
            for k, v in _load_index(root).items()
            if isinstance(v, dict) and (root / str(v.get("file"))).is_file()
        }
        index[key] = {
            "file": local_name,
            "size": st.st_size,
            "mtime_ns": st.st_mtime_ns,
            "used_ns": time.time_ns(),
        }
        state = _state_dir(root)
        state.mkdir(exist_ok=True)
        tmp = state / f".{INDEX_NAME}.part"
        tmp.write_text(json.dumps(index, indent=1))
        os.replace(tmp, state / INDEX_NAME)


def _remember_logged(gcode_root: pathlib.Path, key: str, local_name: str) -> None:
    """remember_import for the thread pool, where a raise would only be lost."""
    try:
        remember_import(gcode_root, key, local_name)
    except OSError as e:
        logger.warning("Could not index USB copy %s: %s", local_name, e)


def remember_import_async(gcode_root: pathlib.Path, key: str, local_name: str) -> None:
    """Run remember_import off the UI thread; the index is only a reuse cache."""
    QtCore.QThreadPool.globalInstance().start(
        functools.partial(_remember_logged, gcode_root, key, local_name)
    )


def _tmp_dir(gcode_root: pathlib.Path, dest_dir: pathlib.Path) -> pathlib.Path:
    """Scratch dir outside the gcodes tree, or *dest_dir* if on another fs."""
    # Outside Moonraker's inotify tree the final rename reads as a plain create_file.
    tmp_dir = _state_dir(gcode_root)
    try:
        tmp_dir.mkdir(exist_ok=True)
        if tmp_dir.stat().st_dev == gcode_root.stat().st_dev:
            return tmp_dir  # same fs keeps os.replace atomic
    except OSError:
        pass
    return dest_dir


def _free_name(src: pathlib.Path, dest_dir: pathlib.Path) -> pathlib.Path:
    """First unused name for *src* in *dest_dir*; never overwrites a local file."""
    # No content match: only the index knows a local copy went through Moonraker.
    n = 0
    while True:
        cand = dest_dir / (src.name if n == 0 else f"{src.stem}_{n}{src.suffix}")
        if not cand.exists() and not cand.is_symlink():
            return cand
        n += 1


def ensure_copies_dir(gcode_root: pathlib.Path) -> None:
    """Create the copies dir ahead of any import."""
    # Moonraker reports files landing in a just-created dir only via its create_dir.
    try:
        (gcode_root / COPIES_DIR_NAME).mkdir(exist_ok=True)
    except OSError as e:
        logger.warning("Could not create %s: %s", COPIES_DIR_NAME, e)


def _prune_copies(root: pathlib.Path, keep: int, job_file: str) -> None:
    """Delete the least recently used copies until at most *keep* remain."""
    # mtime is only the copy time; a reprinted copy's last use lives in the index.
    with _INDEX_LOCK:
        used = {
            v["file"]: v["used_ns"]
            for v in _load_index(root).values()
            if isinstance(v, dict)
            and isinstance(v.get("file"), str)
            and isinstance(v.get("used_ns"), int)
        }
    aged: list[tuple[int, str]] = []
    for f in (root / COPIES_DIR_NAME).glob(f"*{ALLOWED_EXT}"):
        name = f.relative_to(root).as_posix()
        try:
            if f.is_file():
                aged.append((max(f.stat().st_mtime_ns, used.get(name, 0)), name))
        except OSError:
            continue  # deleted meanwhile
    aged.sort()
    excess = len(aged) - keep
    for _, name in aged:
        if excess <= 0:
            break
        if name == job_file:
            continue  # Moonraker would drop the running job's metadata and history file
        (root / name).unlink(missing_ok=True)
        excess -= 1


def _fsync(path: pathlib.Path) -> None:
    """Flush *path* (file or directory) to disk."""
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _sweep_stale_parts(tmp_dir: pathlib.Path) -> None:
    """Delete our temp files left by a crash or power loss, once per process."""
    # Later sweeps would delete the temp file of an aborted copy still running.
    with _COMMIT_LOCK:
        if tmp_dir in _SWEPT:
            return
        _SWEPT.add(tmp_dir)
        for stale in tmp_dir.glob(f"{PART_PREFIX}*.part"):
            stale.unlink(missing_ok=True)


def _copy_atomic(
    src: pathlib.Path,
    src_st: os.stat_result,
    dest_dir: pathlib.Path,
    tmp_dir: pathlib.Path,
) -> pathlib.Path:
    """Copy *src* into *dest_dir* via a synced temp file; returns the final path."""
    _sweep_stale_parts(tmp_dir)  # tmp_dir may be the copies dir itself
    free = shutil.disk_usage(dest_dir).free
    if free < src_st.st_size + MIN_FREE_MARGIN:
        raise UsbImportError(f"Not enough free space ({free // MB} MB free)")
    fd, tmp_name = tempfile.mkstemp(suffix=".part", prefix=PART_PREFIX, dir=tmp_dir)
    os.close(fd)
    tmp = pathlib.Path(tmp_name)
    try:
        os.chmod(tmp, 0o644)  # mkstemp's 0600 would carry over to the gcode
        shutil.copyfile(src, tmp)  # kernel-side copy on Linux
        now = src.stat()
        if (now.st_size, now.st_mtime_ns) != (src_st.st_size, src_st.st_mtime_ns):
            raise UsbImportError("The file changed during the copy")
        if tmp.stat().st_size != src_st.st_size:
            raise UsbImportError("Copy incomplete")
        _fsync(tmp)
        with _COMMIT_LOCK:
            final = _free_name(src, dest_dir)
            os.replace(tmp, final)
        try:
            _fsync(dest_dir)  # persist the rename itself across power loss
        except OSError as e:
            logger.warning("Could not sync %s: %s", dest_dir, e)
    finally:
        tmp.unlink(missing_ok=True)
    return final


def import_usb_gcode(
    gcode_root: pathlib.Path, filename: str, job_file: str = ""
) -> tuple[str, bool, str]:
    """Copy USB *filename* into the copies dir; returns (gcodes-relative path, reused, key)."""
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
    if not usb_root.is_mount() or not src.is_file():
        raise UsbImportError("File not found, was the USB drive removed?")
    try:
        src_st = src.stat()
        key = _source_key(src, src_st)
        final = _indexed_copy(root, key)
        reused = final is not None
        if final is None:
            copies = root / COPIES_DIR_NAME
            try:
                copies.mkdir()
                logger.warning(
                    "Recreated %s, its new copy waits for the settle check",
                    COPIES_DIR_NAME,
                )
            except FileExistsError:
                pass
            _prune_copies(root, MAX_COPIES - 1, job_file)
            final = _copy_atomic(src, src_st, copies, _tmp_dir(root, copies))
    except OSError as e:
        raise UsbImportError(
            f"Copy failed, was the USB drive removed? ({e.strerror})"
        ) from e
    local = final.relative_to(root).as_posix()
    logger.info("USB import %s -> %s (reused=%s)", rel, local, reused)
    return local, reused, key


class UsbImportSignals(QtCore.QObject):
    """Worker result signal, owned on the UI thread by the panel that waits."""

    # (token, usb_file, local_file, key, reused, error)
    done = QtCore.pyqtSignal(int, str, str, str, bool, str)


class UsbImportTask(QtCore.QRunnable):
    """Runs import_usb_gcode off the UI thread."""

    def __init__(
        self,
        signals: UsbImportSignals,
        token: int,
        gcode_root: pathlib.Path,
        filename: str,
        job_file: str = "",
    ) -> None:
        super().__init__()
        # Pool-owned and QObject-free, so no cross-thread delete.
        self.setAutoDelete(True)
        self._signals = signals
        self._token = token
        self._gcode_root = gcode_root
        self._filename = filename
        self._job_file = job_file

    def _report(self, local: str, key: str, reused: bool, error: str) -> None:
        """Emit done; the receiver drops it if the token is stale."""
        try:
            self._signals.done.emit(
                self._token, self._filename, local, key, reused, error
            )
        except RuntimeError:  # owner deleted, i.e. the app is closing
            logger.debug("USB import of %s finished after shutdown", self._filename)

    @QtCore.pyqtSlot()
    def run(self) -> None:
        """Copy, then report the local copy or the error text."""
        try:
            local, reused, key = import_usb_gcode(
                self._gcode_root, self._filename, self._job_file
            )
        except UsbImportError as e:
            logger.warning("USB import of %s failed: %s", self._filename, e)
            self._report("", "", False, str(e))
        except Exception:  # never leave the loadscreen up on a bug
            logger.exception("USB import of %s crashed", self._filename)
            self._report("", "", False, "Unexpected error copying file")
        else:
            self._report(local, key, reused, "")
