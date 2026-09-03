"""Load-once pixmap registry: 16.1 MiB at 64px against 273.0 MiB intrinsic on the RF50."""

from enum import StrEnum
from typing import ClassVar

from PyQt6 import QtCore, QtGui

# Widgets rescale anyway; 128 clears the tallest button at 64 KiB a surface.
ICON_SIZE = QtCore.QSize(128, 128)

_KEEP_ASPECT = QtCore.Qt.AspectRatioMode.KeepAspectRatio
_SMOOTH = QtCore.Qt.TransformationMode.SmoothTransformation
_SOURCE_IN = QtGui.QPainter.CompositionMode.CompositionMode_SourceIn

_SizeLike = QtCore.QSize | QtCore.QSizeF | QtCore.QRect | QtCore.QRectF

MiB = 1024 * 1024


def _as_size(size: _SizeLike) -> QtCore.QSize:
    """Round any Qt size or rect to a QSize, so a caller passes whatever it already holds."""
    if isinstance(size, (QtCore.QRect, QtCore.QRectF)):
        size = size.size()
    return size if isinstance(size, QtCore.QSize) else size.toSize()


def _cost(pixmap: QtGui.QPixmap) -> int:
    """Byte footprint of a surface: an entry count says nothing on a 2 GB board."""
    return pixmap.width() * pixmap.height() * pixmap.depth() // 8


class _PixmapCache:
    """Byte-bounded LRU, so one 400x300 thumbnail cannot evict a screenful of icons."""

    def __init__(self, budget: int) -> None:
        """Hold entries newest-last, since a dict already preserves insertion order."""
        self._entries: dict = {}
        self._budget = budget
        self._bytes = 0

    def __len__(self) -> int:
        """Report the entry count, so a caller can assert the cache emptied."""
        return len(self._entries)

    def get(self, key) -> QtGui.QPixmap | None:
        """Return the entry for *key* and move it to newest, which is the LRU touch."""
        pixmap = self._entries.pop(key, None)
        if pixmap is not None:
            self._entries[key] = pixmap
        return pixmap

    def put(self, key, pixmap: QtGui.QPixmap) -> QtGui.QPixmap:
        """Store *pixmap*, then drop least-recent entries until back inside the budget."""
        self._entries[key] = pixmap
        self._bytes += _cost(pixmap)
        # An evicted entry a widget still holds only mints a duplicate, never a fault.
        while self._bytes > self._budget and len(self._entries) > 1:
            self._bytes -= _cost(self._entries.pop(next(iter(self._entries))))
        return pixmap

    def clear(self) -> None:
        """Drop every entry and reset the running total with it."""
        self._entries.clear()
        self._bytes = 0


class Icon(StrEnum):
    """Every resource key the handwritten panels draw, one member per asset."""

    ABS_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/abs_filament_topbar.svg"
    ADD_FILAMENT = (
        ":/filament_related/media/btn_icons/filament_related/add_filament.svg"
    )
    ADD_SPOOL = ":/filament_related/media/btn_icons/filament_related/add_spool.svg"
    ARROW_DOWN = ":/arrow_icons/media/btn_icons/arrow_icons/arrow_down.svg"
    ARROW_LEFT = ":/arrow_icons/media/btn_icons/arrow_icons/arrow_left.svg"
    ARROW_RIGHT = ":/arrow_icons/media/btn_icons/arrow_icons/arrow_right.svg"
    BABYSTEP_GRAPHIC = ":/graphics/media/graphics/babystep_graphic.png"
    BABY_STEP_ICON = ":/z_levelling/media/btn_icons/z_levelling/baby_step.svg"
    BACK = ":/ui/media/btn_icons/ui/back.svg"
    BACKGROUND_1ST = ":/background/media/1st_background.png"
    BACK_FOLDER = ":/ui/media/btn_icons/ui/back_folder.svg"
    SPOOL_DATABASE_1 = (
        ":/filament_related/media/btn_icons/filament_related/spool_database_1.svg"
    )
    BLOWER = ":/fan_related/media/btn_icons/fan_related/blower.svg"
    BLTOUCH = ":/z_levelling/media/btn_icons/z_levelling/bltouch.svg"
    CHANGE_FILAMENT = (
        ":/filament_related/media/btn_icons/filament_related/change_filament.svg"
    )
    CHECK_GATE_1 = (
        ":/filament_related/media/btn_icons/filament_related/check_gate_1.svg"
    )
    EDDY_MECH = ":/z_levelling/media/btn_icons/z_levelling/eddy_mech.svg"
    EJECT = ":/filament_related/media/btn_icons/filament_related/eject.svg"
    ERROR = ":/ui/media/btn_icons/ui/error.svg"
    ETHERNET_CONNECTED = ":/network/media/btn_icons/network/ethernet_connected.svg"
    FAN = ":/fan_related/media/btn_icons/fan_related/fan.svg"
    FAN_CAGE = ":/fan_related/media/btn_icons/fan_related/fan_cage.svg"
    FILAMENT_SENSOR = (
        ":/filament_related/media/btn_icons/filament_related/filament_sensor.svg"
    )
    FILAMENT_SENSOR_OFF = (
        ":/filament_related/media/btn_icons/filament_related/filament_sensor_off.svg"
    )
    FILAMENT_SENSOR_TURN_ON = ":/filament_related/media/btn_icons/filament_related/filament_sensor_turn_on.svg"
    FILE_ICON = ":/files/media/btn_icons/files/file.svg"
    FOLDERICON = ":/ui/media/btn_icons/ui/folder.svg"
    GARBAGE_ICON = ":/ui/media/btn_icons/ui/garbage.svg"
    HALF_SPOLL = ":/filament_related/media/btn_icons/filament_related/half_spool.svg"
    HOTSPOT = ":/network/media/btn_icons/network/hotspot.svg"
    INDUCTIVE = ":/z_levelling/media/btn_icons/z_levelling/inductive.svg"
    INFO = ":/ui/media/btn_icons/ui/info.svg"
    INPUT_SHAPER_AUTO = (
        ":/input_shaper/media/btn_icons/input_shaper/input_shaper_auto.svg"
    )
    INPUT_SHAPER_MANUAL = (
        ":/input_shaper/media/btn_icons/input_shaper/input_shaper_manual.svg"
    )
    LAYERS = ":/ui/media/btn_icons/ui/layers.svg"
    LEDS = ":/ui/media/btn_icons/ui/leds.svg"
    LEFT_ARROW = ":/arrow_icons/media/btn_icons/arrow_icons/left_arrow.svg"
    LOADED_SPOOL = (
        ":/filament_related/media/btn_icons/filament_related/loaded_spool.svg"
    )
    LOAD_FILAMENT = (
        ":/filament_related/media/btn_icons/filament_related/load_filament.svg"
    )
    LOGO_BLOCKS = ":/graphics/media/logoblocks400x300.png"
    MOVE_NOZZLE_AWAY = ":/baby_step/media/btn_icons/baby_step/move_nozzle_away.svg"
    MOVE_NOZZLE_CLOSE = ":/baby_step/media/btn_icons/baby_step/move_nozzle_close.svg"
    NO = ":/dialog/media/btn_icons/dialog/no.svg"
    NOTIFICATION = ":/ui/media/btn_icons/ui/notification.svg"
    NYLON_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/nylon_filament_topbar.svg"
    PAUSE = ":/ui/media/btn_icons/ui/pause.svg"
    PC_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/pc_filament_topbar.svg"
    PETG_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/petg_filament_topbar.svg"
    PLAY = ":/ui/media/btn_icons/ui/play.svg"
    PLA_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/pla_filament_topbar.svg"
    PP_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/pp_filament_topbar.svg"
    PRINT = ":/ui/media/btn_icons/ui/print.svg"
    PRINTER_SETTINGS = ":/ui/media/btn_icons/ui/printer_settings.svg"
    REBOOT = ":/system/media/btn_icons/system/reboot.svg"
    REFRESH = ":/ui/media/btn_icons/ui/refresh.svg"
    RESTART_KLIPPER = ":/system/media/btn_icons/system/restart_klipper.svg"
    RIGHT_ARROW = ":/arrow_icons/media/btn_icons/arrow_icons/right_arrow.svg"
    SAVE = ":/ui/media/btn_icons/ui/save.svg"
    SEE = ":/ui/media/btn_icons/ui/see.svg"
    SPEED = ":/motion/media/btn_icons/motion/speed.svg"
    STATIC_IP = ":/network/media/btn_icons/network/static_ip.svg"
    STOP = ":/ui/media/btn_icons/ui/stop.svg"
    SWITCH_ZOOM = ":/extruder_related/media/btn_icons/extruder_related/switch_zoom.svg"
    TEMPERATURE = (
        ":/temperature_related/media/btn_icons/temperature_related/temperature.svg"
    )
    TEMPERATURE_PLATE = ":/temperature_related/media/btn_icons/temperature_related/temperature_plate.svg"
    TIME = ":/ui/media/btn_icons/ui/time.svg"
    TROUBLESHOOT = ":/ui/media/btn_icons/ui/troubleshoot.svg"
    TUNE = ":/ui/media/btn_icons/ui/tune.svg"
    UNLOAD_FILAMENT = (
        ":/filament_related/media/btn_icons/filament_related/unload_filament.svg"
    )
    UNSEE = ":/ui/media/btn_icons/ui/unsee.svg"
    UPDATE_SOFTWARE_ICON = ":/system/media/btn_icons/system/update_software.svg"
    USB_ICON = ":/ui/media/btn_icons/ui/usb.svg"
    WIFI_0BAR = ":/network/media/btn_icons/network/wifi_0bar.svg"
    WIFI_0BAR_PROTECTED = ":/network/media/btn_icons/network/wifi_0bar_protected.svg"
    WIFI_1BAR = ":/network/media/btn_icons/network/wifi_1bar.svg"
    WIFI_1BAR_PROTECTED = ":/network/media/btn_icons/network/wifi_1bar_protected.svg"
    WIFI_2BAR = ":/network/media/btn_icons/network/wifi_2bar.svg"
    WIFI_2BAR_PROTECTED = ":/network/media/btn_icons/network/wifi_2bar_protected.svg"
    WIFI_3BAR = ":/network/media/btn_icons/network/wifi_3bar.svg"
    WIFI_3BAR_PROTECTED = ":/network/media/btn_icons/network/wifi_3bar_protected.svg"
    WIFI_4BAR = ":/network/media/btn_icons/network/wifi_4bar.svg"
    WIFI_4BAR_PROTECTED = ":/network/media/btn_icons/network/wifi_4bar_protected.svg"
    WIFI_CONFIG = ":/network/media/btn_icons/network/wifi_config.svg"
    YES = ":/dialog/media/btn_icons/dialog/yes.svg"

    @classmethod
    def wifi(cls, bars: int, protected: bool = False) -> "Icon":
        """Return the signal-strength icon for *bars*, clamped to the 0..4 assets."""
        bars = min(max(bars, 0), 4)
        return cls[f"WIFI_{bars}BAR{'_PROTECTED' if protected else ''}"]


class BlocksPixmap:
    """Process-wide cache of QIcons and the pixmaps rendered from them."""

    # Two QIcons over one path do not share their render cache, so hold the QIcon.
    _icons: ClassVar[dict[str, QtGui.QIcon]] = {}

    # Rendered from a path: a stable set, so it never shares an eviction budget with
    # the derived caches below, which churn on every new thumbnail.
    _pixmaps: ClassVar[_PixmapCache] = _PixmapCache(12 * MiB)

    # Derived from a surface, keyed by cacheKey, so thumbnails and tints cache too.
    _scaled: ClassVar[_PixmapCache] = _PixmapCache(8 * MiB)
    _tints: ClassVar[_PixmapCache] = _PixmapCache(8 * MiB)

    @classmethod
    def icon(cls, icon: Icon | str) -> QtGui.QIcon:
        """Return the shared QIcon for *icon*, built from the path so SVGs stay scalable."""
        key = str(icon)
        cached = cls._icons.get(key)
        if cached is None:
            cached = QtGui.QIcon(key)
            cls._icons[key] = cached
        return cached

    @classmethod
    def get(
        cls,
        source: Icon | str | QtGui.QPixmap,
        size: _SizeLike = ICON_SIZE,
        aspect: QtCore.Qt.AspectRatioMode = _KEEP_ASPECT,
    ) -> QtGui.QPixmap:
        """Return *source* at *size*, cached; a path re-renders, a surface can only resample."""
        target = size if isinstance(size, QtCore.QSize) else _as_size(size)
        if isinstance(source, QtGui.QPixmap):
            return cls._resampled(source, target, aspect)
        return cls._rendered(source, target, aspect)

    @classmethod
    def _rendered(
        cls, path: Icon | str, size: QtCore.QSize, aspect: QtCore.Qt.AspectRatioMode
    ) -> QtGui.QPixmap:
        """Rasterize a resource path, which an SVG does crisply at any size."""
        # Icon is a StrEnum, so it keys identically to the bare path and needs no str().
        key = (path, size.width(), size.height(), aspect)
        cached = cls._pixmaps.get(key)
        if cached is not None:
            return cached
        pixmap = cls.icon(path).pixmap(size)
        # QIcon.pixmap always fits inside, so a distorting mode needs a second pass.
        if aspect is not _KEEP_ASPECT and pixmap.size() != size:
            pixmap = pixmap.scaled(size, aspect, _SMOOTH)
        return cls._pixmaps.put(key, pixmap)

    @classmethod
    def _resampled(
        cls,
        pixmap: QtGui.QPixmap,
        size: QtCore.QSize,
        aspect: QtCore.Qt.AspectRatioMode,
    ) -> QtGui.QPixmap:
        """Resample an existing surface, the only option when no resource path is in hand."""
        key = (pixmap.cacheKey(), size.width(), size.height(), aspect)
        cached = cls._scaled.get(key)
        if cached is not None:
            return cached
        return cls._scaled.put(key, pixmap.scaled(size, aspect, _SMOOTH))

    @classmethod
    def tinted(
        cls,
        pixmap: QtGui.QPixmap,
        color: QtGui.QColor | str,
        mode: QtGui.QPainter.CompositionMode = _SOURCE_IN,
    ) -> QtGui.QPixmap:
        """Return *pixmap* recoloured to *color* through its own alpha, cached per surface."""
        if not isinstance(color, QtGui.QColor):
            color = QtGui.QColor(color)
        key = (pixmap.cacheKey(), color.rgba(), mode)
        cached = cls._tints.get(key)
        if cached is not None:
            return cached
        result = QtGui.QPixmap(pixmap.size())
        result.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(result)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(mode)
        painter.fillRect(result.rect(), color)
        painter.end()
        return cls._tints.put(key, result)

    @classmethod
    def source(cls, icon: Icon | str) -> QtGui.QPixmap:
        """Return the intrinsic-size pixmap; only for full-bleed art, never a btn_icon."""
        return QtGui.QPixmap(str(icon))

    @classmethod
    def clear(cls) -> None:
        """Drop every cached icon and pixmap, called from on_quit while qApp is alive."""
        for cache in (cls._icons, cls._pixmaps, cls._scaled, cls._tints):
            cache.clear()
