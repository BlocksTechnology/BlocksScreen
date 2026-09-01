import logging
import os
import shutil
import signal
import socket
import subprocess  # nosec B404
import sys
import typing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from configfile import get_configparser
from lib.panels.mainWindow import MainWindow
from lib.utils.blocks_pixmap import BlocksPixmap
from logger import CrashHandler, LogManager, install_crash_handler, setup_logging
from PyQt6 import QtCore, QtGui, QtWidgets
from tools.configuration_manager import ConfigManager

install_crash_handler()

_SPLASH_CACHE = Path("/home/blocks/.cache/blockscreen/splash.raw")
_SPLASH_PNG = Path("/home/blocks/.cache/blockscreen/splash.png")
_FB0 = Path("/dev/fb0")
_BOOT_CACHE = _SPLASH_CACHE.parent
_BS_REPO = Path(__file__).resolve().parent.parent

_LOGO: Path | None = next(
    (
        p
        for p in [
            Path(__file__).parent / "lib/ui/resources/media/logoblocks400x300.png",
            Path(__file__).parent / "lib/ui/resources/media/logoblocks.png",
            Path(__file__).parent / "lib/ui/resources/media/graphics/logo_blocks.png",
        ]
        if p.exists()
    ),
    None,
)


class BlocksScreenApp(QtWidgets.QApplication):
    """QApplication subclass that routes unhandled slot exceptions to CrashHandler."""

    def notify(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:  # type: ignore[override]
        try:
            return super().notify(a0, a1)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            handler = CrashHandler._instance
            if handler is not None and exc_type is not None and exc_value is not None:
                handler._exception_hook(exc_type, exc_value, exc_tb)
            return False


QtGui.QGuiApplication.setAttribute(
    QtCore.Qt.ApplicationAttribute.AA_SynthesizeMouseForUnhandledTouchEvents,
    True,
)
QtGui.QGuiApplication.setAttribute(
    QtCore.Qt.ApplicationAttribute.AA_SynthesizeTouchForUnhandledMouseEvents,
    True,
)

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def _write_splash_to_fb0() -> None:
    """Write precomputed splash to fb0 while KD_GRAPHICS is still active.

    Called from SIGTERM handler so fb0 already shows the splash before X exits,
    eliminating the brief black frame between X shutdown and ExecStopPost.
    """
    try:
        if _SPLASH_CACHE.exists():
            _FB0.write_bytes(_SPLASH_CACHE.read_bytes())
    except OSError as exc:
        logging.getLogger(__name__).warning("splash write to fb0 failed: %s", exc)


def show_splash() -> QtWidgets.QSplashScreen:
    """Show a fullscreen splash immediately after QApplication is created.

    Centres the logo on a dark background matching the current screen geometry,
    with a 'Starting ...' message below the logo.
    Returns the QSplashScreen so the caller can call splash.finish(main_window).
    """
    screen = QtWidgets.QApplication.primaryScreen()
    geom = screen.geometry() if screen is not None else None

    if _SPLASH_PNG.exists() and geom is not None:
        # Re-use the PIL-rendered PNG so both splashes are pixel-identical.
        bg = QtGui.QPixmap(str(_SPLASH_PNG)).scaled(
            geom.size(),
            QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        splash = QtWidgets.QSplashScreen(bg, QtCore.Qt.WindowType.WindowStaysOnTopHint)
        splash.setGeometry(geom)
    else:
        # Fallback: render in Qt when no cached PNG exists yet.
        logo = QtGui.QPixmap(str(_LOGO)) if _LOGO is not None else QtGui.QPixmap()
        if geom is not None:
            if not logo.isNull():
                max_w = min(geom.width() // 2, 600)
                max_h = min(geom.height() // 2, 400)
                lw, lh = logo.width(), logo.height()
                if lw > 0 and lh > 0:
                    scale = min(max_w / lw, max_h / lh, 1.0)
                    if scale < 1.0:
                        logo = logo.scaled(
                            int(lw * scale),
                            int(lh * scale),
                            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                            QtCore.Qt.TransformationMode.SmoothTransformation,
                        )
            bg = QtGui.QPixmap(geom.size())
            bg.fill(QtGui.QColor(20, 20, 20))
            painter = QtGui.QPainter(bg)
            lx = (bg.width() - logo.width()) // 2
            ly = (bg.height() - logo.height()) // 2
            if not logo.isNull():
                painter.drawPixmap(lx, ly, logo)
            painter.setFont(QtGui.QFont("DejaVu Sans", 14))
            painter.setPen(QtGui.QColor(180, 180, 180))
            painter.drawText(
                0,
                ly + logo.height() + 24,
                bg.width(),
                32,
                QtCore.Qt.AlignmentFlag.AlignHCenter,
                "Starting ...",
            )
            painter.end()
            splash = QtWidgets.QSplashScreen(
                bg, QtCore.Qt.WindowType.WindowStaysOnTopHint
            )
            splash.setGeometry(geom)
        else:
            splash = QtWidgets.QSplashScreen(
                logo, QtCore.Qt.WindowType.WindowStaysOnTopHint
            )
    splash.show()
    QtWidgets.QApplication.processEvents()
    return splash


def _setup_sigterm(app: BlocksScreenApp) -> None:
    def _do_shutdown() -> None:
        logging.getLogger(__name__).info("SIGTERM: showing restart splash before exit")
        # Cover the live UI before the multi-second teardown freezes its last frame.
        try:
            show_splash()
        except Exception as exc:  # noqa: BLE001
            logging.getLogger(__name__).warning("restart splash failed: %s", exc)
        _write_splash_to_fb0()
        app.quit()

    def _handler(__signum: int, __frame: typing.Any) -> None:
        # Defer off the signal trampoline: inline paint reenters Qt mid-paint and SEGVs.
        QtCore.QTimer.singleShot(0, _do_shutdown)

    signal.signal(signal.SIGTERM, _handler)


def on_quit() -> None:
    logging.info("Final exit cleanup")
    # aboutToQuit still has a live qApp, which QPixmap destruction requires.
    BlocksPixmap.clear()
    LogManager.shutdown()


def initialize_conf_manager() -> None:
    global conf_man
    try:
        conf_man = ConfigManager(get_configparser())
    except Exception as e:
        _logger.error(
            "Caught Exception on configuration_manager tool: %s" % e, exc_info=True
        )


def _sd_notify(msg: str) -> None:
    sock_path = os.environ.get("NOTIFY_SOCKET", "")
    if not sock_path:
        return
    if sock_path.startswith("@"):
        sock_path = "\0" + sock_path[1:]
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as s:
            s.sendto(msg.encode(), sock_path)
    except OSError as exc:
        logging.getLogger(__name__).warning("sd_notify(%s) failed: %s", msg, exc)


def _setup_watchdog() -> None:
    """Ping the systemd watchdog from the Qt event loop.

    Driving the ping from the event loop (not a background thread) means a
    frozen UI stops the pings, so systemd's WatchdogSec restarts us. A
    thread-based ping would keep a hung GUI alive and defeat the watchdog.
    The interval is derived from WATCHDOG_USEC (half the deadline), falling
    back to 15s when systemd did not set it.
    """
    usec = os.environ.get("WATCHDOG_USEC", "")
    try:
        interval_ms = int(usec) // 2000 if usec else 15000
    except ValueError:
        interval_ms = 15000
    interval_ms = max(1000, interval_ms)
    _sd_notify("WATCHDOG=1")
    timer = QtCore.QTimer(QtWidgets.QApplication.instance())
    timer.timeout.connect(lambda: _sd_notify("WATCHDOG=1"))
    timer.start(interval_ms)


def _record_boot_success() -> None:
    """Mark the current commit as last-well-known-good and clear the boot-attempt counter.

    BlocksScreen-start.sh reads theses to auto-roll-back a crash-looping update.
    """
    log = logging.getLogger(__name__)
    try:
        _git = shutil.which("git") or "/usr/bin/git"
        head = subprocess.run(  # nosec B603
            [_git, "-C", str(_BS_REPO), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        ).stdout.strip()
    except (subprocess.SubprocessError, OSError) as exc:
        log.warning("record_boot_success: git rev-parse failed: %s", exc)
        return
    if not head:
        return
    try:
        _BOOT_CACHE.mkdir(parents=True, exist_ok=True)
        marker = _BOOT_CACHE / "last_good_commit"
        try:
            already = marker.read_text().strip()
        except OSError:
            already = ""
        # Always clear the boot counter; rewrite the commit marker only when it
        # actually changed (avoids a redundant SD write on every healthy boot).
        writes = [("boot_attempts", "0\n")]
        if already != head:
            writes.append(("last_good_commit", head + "\n"))
        for name, text in writes:
            tmp = _BOOT_CACHE / f".{name}.tmp"
            tmp.write_text(text)
            os.replace(tmp, _BOOT_CACHE / name)
    except OSError as exc:
        log.warning("record_boot_success: write failed %s", exc)


def _force_screen_refresh() -> None:
    """Repaint the screen so a restarted GUI is presented over the splash.

    X.Org persists across Qt restarts, so the newly mapped MainWindow never gets
    an Expose and its first frame is not flushed to the KMS scanout, leaving the
    feh restart splash frozen on the panel. xrefresh forces the repaint; a no-op
    on a cold boot.
    """
    if not os.environ.get("DISPLAY"):
        return
    xrefresh = shutil.which("xrefresh")
    if not xrefresh:
        return
    try:
        subprocess.run([xrefresh], timeout=5, check=False)  # nosec B603
    except (subprocess.SubprocessError, OSError) as exc:
        logging.getLogger(__name__).warning("xrefresh failed: %s", exc)


class _FirstPaintRefresh(QtCore.QObject):
    """Trigger :func:`_force_screen_refresh` on the window's first paint.

    Event-driven companion to the fixed 300/1500 ms nudges: it fires the repaint
    the instant the restarted GUI first paints (often well before 300 ms),
    removing the dependency on a magic delay, then detaches itself. The xrefresh
    call is deferred via ``singleShot(0)`` so it never blocks inside the paint
    handler. The fixed nudges remain as a slow-paint safety net.
    """

    def __init__(self, target: QtCore.QObject) -> None:
        super().__init__(target)
        target.installEventFilter(self)

    def eventFilter(self, a0: QtCore.QObject | None, a1: QtCore.QEvent | None) -> bool:
        if a1 is not None and a1.type() == QtCore.QEvent.Type.Paint:
            if a0 is not None:
                a0.removeEventFilter(self)
            QtCore.QTimer.singleShot(0, _force_screen_refresh)
        return False


if __name__ == "__main__":
    setup_logging(
        filename="logs/BlocksScreen.log",
        level=logging.DEBUG,
        console_output=True,
        console_level=logging.DEBUG,
        capture_stderr=True,
        capture_stdout=False,
    )
    _logger = logging.getLogger(__name__)
    _logger.info("============ BlocksScreen Initializing ============")
    initialize_conf_manager()
    BlocksScreen = BlocksScreenApp([])
    BlocksScreen.setApplicationName("BlocksScreen")
    BlocksScreen.setApplicationDisplayName("BlocksScreen")
    BlocksScreen.setDesktopFileName("BlocksScreen")
    _splash = show_splash()
    main_window = MainWindow()
    BlocksScreen.processEvents()
    BlocksScreen.aboutToQuit.connect(on_quit)
    _setup_sigterm(BlocksScreen)
    # Event-driven repaint: fire the moment the window first paints (parented to
    # main_window so it lives as long as the window).
    _FirstPaintRefresh(main_window)
    main_window.show()
    _splash.finish(main_window)
    _sd_notify("READY=1")
    _setup_watchdog()
    # Belt-and-suspenders: fixed nudges still cover a pathologically slow paint.
    QtCore.QTimer.singleShot(300, _force_screen_refresh)
    QtCore.QTimer.singleShot(1500, _force_screen_refresh)
    QtCore.QTimer.singleShot(5000, _record_boot_success)
    sys.exit(BlocksScreen.exec())
