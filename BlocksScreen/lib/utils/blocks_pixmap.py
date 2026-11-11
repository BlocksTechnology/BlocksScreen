"""Load-once registry of Qt resource pixmaps, rendered at draw size instead of intrinsic size."""

from enum import StrEnum

from PyQt6 import QtCore, QtGui

# Setup-time callers cannot know their paint size; 128 clears the tallest button.
_ICON_EDGE = 128

_KEEP_ASPECT = QtCore.Qt.AspectRatioMode.KeepAspectRatio
_SMOOTH = QtCore.Qt.TransformationMode.SmoothTransformation
_SOURCE_IN = QtGui.QPainter.CompositionMode.CompositionMode_SourceIn

_SizeLike = QtCore.QSize | QtCore.QSizeF | QtCore.QRect | QtCore.QRectF

_MIB = 1024 * 1024

# Largest icon surface (a 300px option card); bigger sources are thumbnails.
_ICON_SOURCE_COST = 300 * 300 * 4


def _as_size(size: _SizeLike) -> QtCore.QSize:
    """Truncate any Qt size or rect to a QSize, so an icon never outgrows its rect."""
    if isinstance(size, (QtCore.QRect, QtCore.QRectF)):
        size = size.size()
    if isinstance(size, QtCore.QSize):
        return size
    return QtCore.QSize(int(size.width()), int(size.height()))


def _cost(pixmap: QtGui.QPixmap) -> int:
    """Byte footprint of a surface: an entry count says nothing on a 2 GB board."""
    return pixmap.width() * pixmap.height() * pixmap.depth() // 8


class _PixmapCache:
    """Byte-bounded LRU, so one 400x300 thumbnail cannot evict a screenful of icons."""

    def __init__(self, budget: int) -> None:
        """Hold entries newest-last, since a dict already preserves insertion order."""
        self._entries: dict[tuple, QtGui.QPixmap] = {}
        self._budget = budget
        self._bytes = 0

    def __len__(self) -> int:
        """Report the entry count, so a caller can assert the cache emptied."""
        return len(self._entries)

    def get(self, key: tuple) -> QtGui.QPixmap | None:
        """Return the entry for *key* and move it to newest, which is the LRU touch."""
        pixmap = self._entries.pop(key, None)
        if pixmap is not None:
            self._entries[key] = pixmap
        return pixmap

    def put(self, key: tuple, pixmap: QtGui.QPixmap) -> QtGui.QPixmap:
        """Store *pixmap*, then drop least-recent entries until back inside the budget."""
        stale = self._entries.pop(key, None)
        if stale is not None:
            self._bytes -= _cost(stale)
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
    ADD_FILAMENT = ":/filament_related/media/btn_icons/add filament.svg"
    ADD_SPOOL = ":/filament_related/media/btn_icons/add spool.svg"
    ARROW_DOWN = ":/arrow_icons/media/btn_icons/arrow_down.svg"
    ARROW_LEFT = ":/arrow_icons/media/btn_icons/arrow_left.svg"
    ARROW_RIGHT = ":/arrow_icons/media/btn_icons/arrow_right.svg"
    AXIS_MAINTENANCE = ":/motion/media/btn_icons/axis_maintenance.svg"
    BABYSTEP_GRAPHIC = ":/graphics/media/graphics/babystep_graphic.png"
    BABY_STEP_ICON = ":/z_levelling/media/btn_icons/baby_step_icon.svg"
    BACK = ":/ui/media/btn_icons/back.svg"
    BACKGROUND_1ST = ":/background/media/1st_background.png"
    BACK_FOLDER = ":/ui/media/btn_icons/back_folder.svg"
    BASE_DADOS_SPOOL_1 = ":/filament_related/media/btn_icons/base dados spool 1.svg"
    BED_LEVELLING = ":/z_levelling/media/btn_icons/bed_levelling.svg"
    BLOWER = ":/fan_related/media/btn_icons/blower.svg"
    BLTOUCH = ":/z_levelling/media/btn_icons/bltouch.svg"
    CENTER_ARROWS = ":/ui/media/btn_icons/center_arrows.svg"
    CHAMBER_TEMP_TOPBAR = ":/top_bar_icons/media/topbar/chamber_temp_topbar.svg"
    CHANGE_FILAMENT = ":/filament_related/media/btn_icons/change_filament.svg"
    CHECK_GATE_1 = ":/filament_related/media/btn_icons/check gate 1.svg"
    COOLDOWN = ":/temperature_related/media/btn_icons/cooldown.svg"
    DISABLE_STEPPERS = ":/motion/media/btn_icons/disable_steppers.svg"
    DOWN_ARROW = ":/arrow_icons/media/btn_icons/down_arrow.svg"
    EDDY_MECH = ":/z_levelling/media/btn_icons/eddy_mech.svg"
    EJECT = ":/filament_related/media/btn_icons/eject.svg"
    ERROR = ":/ui/media/btn_icons/error.svg"
    ETHERNET_CONNECTED = ":/network/media/btn_icons/network/ethernet_connected.svg"
    EXTRUDE = ":/extruder_related/media/btn_icons/extrude.svg"
    FAN = ":/fan_related/media/btn_icons/fan.svg"
    FAN_CAGE = ":/fan_related/media/btn_icons/fan_cage.svg"
    FILAMENT_SENSOR = ":/filament_related/media/btn_icons/filament_sensor.svg"
    FILAMENT_SENSOR_OFF = ":/filament_related/media/btn_icons/filament_sensor_off.svg"
    FILAMENT_SENSOR_TURN_ON = (
        ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
    )
    FILE_ICON = ":/files/media/btn_icons/file_icon.svg"
    FOLDERICON = ":/ui/media/btn_icons/folderIcon.svg"
    GARBAGE_ICON = ":/ui/media/btn_icons/garbage-icon.svg"
    HALF_SPOLL = ":/filament_related/media/btn_icons/half_spoll.svg"
    HEATSOAK_ICON = ":/temperature_related/media/btn_icons/heatsoak_icon.svg"
    HOME_ALL = ":/motion/media/btn_icons/home_all.svg"
    HOME_X = ":/motion/media/btn_icons/home_x.svg"
    HOME_Y = ":/motion/media/btn_icons/home_y.svg"
    HOME_Z = ":/motion/media/btn_icons/home_z.svg"
    HOTSPOT = ":/network/media/btn_icons/hotspot.svg"
    HUMIDITY = ":/temperature_related/media/btn_icons/humidity.svg"
    INDUCTIVE = ":/z_levelling/media/btn_icons/inductive.svg"
    INFO = ":/ui/media/btn_icons/info.svg"
    INPUT_SHAPER = ":/input_shaper/media/btn_icons/input_shaper.svg"
    INPUT_SHAPER_AUTO = ":/input_shaper/media/btn_icons/input_shaper_auto.svg"
    INPUT_SHAPER_MANUAL = ":/input_shaper/media/btn_icons/input_shaper_manual.svg"
    LAYERS = ":/ui/media/btn_icons/layers.svg"
    LEDS = ":/ui/media/btn_icons/LEDs.svg"
    LEDS_OFF = ":/ui/media/btn_icons/LEDs_off.svg"
    LEFT_ARROW = ":/arrow_icons/media/btn_icons/left_arrow.svg"
    LOADED_SPOOL = ":/filament_related/media/btn_icons/loaded_spool.svg"
    LOAD_FILAMENT = ":/filament_related/media/btn_icons/load_filament.svg"
    LOGO_BLOCKS = ":/graphics/media/logoblocks400x300.png"
    MENU_CONTROL = ":/icons/media/main_menu/ICON_control.png"
    MENU_CONTROL_BLOCKED = ":/icons/media/main_menu/ICON_control_blocked.png"
    MENU_CONTROL_PRESSED = ":/icons/media/main_menu/ICON_control_pressed.png"
    MENU_FILAMENT = ":/icons/media/main_menu/ICON_filament.png"
    MENU_FILAMENT_BLOCKED = ":/icons/media/main_menu/ICON_filamente_blocked.png"
    MENU_FILAMENT_PRESSED = ":/icons/media/main_menu/ICON_filament_pressed.png"
    MENU_HOME = ":/icons/media/main_menu/ICON_home.png"
    MENU_HOME_BLOCKED = ":/icons/media/main_menu/ICON_home_blocked.png"
    MENU_HOME_PRESSED = ":/icons/media/main_menu/ICON_home_pressed.png"
    MENU_UTILITIES = ":/icons/media/main_menu/ICON_utilities.png"
    MENU_UTILITIES_BLOCKED = ":/icons/media/main_menu/ICON_utilities_blocked.png"
    MENU_UTILITIES_PRESSED = ":/icons/media/main_menu/ICON_utilities_pressed.png"
    MOVE_NOZZLE_AWAY = ":/baby_step/media/btn_icons/move_nozzle_away.svg"
    MOVE_NOZZLE_CLOSE = ":/baby_step/media/btn_icons/move_nozzle_close.svg"
    NO = ":/dialog/media/btn_icons/no.svg"
    NOTIFICATION = ":/ui/media/btn_icons/notification.svg"
    NOZZLE = ":/extruder_related/media/btn_icons/nozzle.svg"
    NOZZLE_TOPBAR = ":/extruder_related/media/btn_icons/nozzle_topbar.svg"
    NYLON_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/nylon_filament_topbar.svg"
    PAUSE = ":/ui/media/btn_icons/pause.svg"
    PC_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/pc_filament_topbar.svg"
    PETG_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/petg_filament_topbar.svg"
    PLAY = ":/ui/media/btn_icons/play.svg"
    PLA_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/pla_filament_topbar.svg"
    PP_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/pp_filament_topbar.svg"
    PRINT = ":/ui/media/btn_icons/print.svg"
    PRINTER_SETTINGS = ":/ui/media/btn_icons/printer_settings.svg"
    REBOOT = ":/system/media/btn_icons/reboot.svg"
    REFRESH = ":/ui/media/btn_icons/refresh.svg"
    RESTART_KLIPPER = ":/system/media/btn_icons/restart_klipper.svg"
    RIGHT_ARROW = ":/arrow_icons/media/btn_icons/right_arrow.svg"
    ROUTINE = ":/ui/media/btn_icons/routine.svg"
    SAVE = ":/ui/media/btn_icons/save.svg"
    SEE = ":/ui/media/btn_icons/see.svg"
    SORT_ASC = ":/arrow_icons/media/btn_icons/sort_asc.svg"
    SORT_DESC = ":/arrow_icons/media/btn_icons/sort_desc.svg"
    SPEED = ":/motion/media/btn_icons/speed.svg"
    STANDART_TEMPERATURE = (
        ":/temperature_related/media/btn_icons/standart_temperature.svg"
    )
    STATIC_IP = ":/network/media/btn_icons/network/static_ip.svg"
    STOP = ":/ui/media/btn_icons/stop.svg"
    SWITCH_ZOOM = ":/extruder_related/media/btn_icons/switch_zoom.svg"
    TEMPERATURE = ":/temperature_related/media/btn_icons/temperature.svg"
    TEMPERATURE_PLATE = ":/temperature_related/media/btn_icons/temperature_plate.svg"
    TIME = ":/ui/media/btn_icons/time.svg"
    TROUBLESHOOT = ":/ui/media/btn_icons/troubleshoot.svg"
    TUNE = ":/ui/media/btn_icons/tune.svg"
    UNLOAD_FILAMENT = ":/filament_related/media/btn_icons/unload_filament.svg"
    UNSEE = ":/ui/media/btn_icons/unsee.svg"
    UPDATE_SOFTWARE_ICON = ":/system/media/btn_icons/update-software-icon.svg"
    UP_ARROW = ":/arrow_icons/media/btn_icons/up_arrow.svg"
    USB_ICON = ":/ui/media/btn_icons/usb_icon.svg"
    WIFI_0BAR = ":/network/media/btn_icons/network/0bar_wifi.svg"
    WIFI_0BAR_PROTECTED = ":/network/media/btn_icons/network/0bar_wifi_protected.svg"
    WIFI_1BAR = ":/network/media/btn_icons/network/1bar_wifi.svg"
    WIFI_1BAR_PROTECTED = ":/network/media/btn_icons/network/1bar_wifi_protected.svg"
    WIFI_2BAR = ":/network/media/btn_icons/network/2bar_wifi.svg"
    WIFI_2BAR_PROTECTED = ":/network/media/btn_icons/network/2bar_wifi_protected.svg"
    WIFI_3BAR = ":/network/media/btn_icons/network/3bar_wifi.svg"
    WIFI_3BAR_PROTECTED = ":/network/media/btn_icons/network/3bar_wifi_protected.svg"
    WIFI_4BAR = ":/network/media/btn_icons/network/4bar_wifi.svg"
    WIFI_4BAR_PROTECTED = ":/network/media/btn_icons/network/4bar_wifi_protected.svg"
    WIFI_CONFIG = ":/network/media/btn_icons/wifi_config.svg"
    YES = ":/dialog/media/btn_icons/yes.svg"

    @classmethod
    def wifi(cls, bars: int, protected: bool = False) -> "Icon":
        """Return the signal-strength icon for *bars*, clamped to the 0..4 assets."""
        bars = min(max(bars, 0), 4)
        return cls[f"WIFI_{bars}BAR{'_PROTECTED' if protected else ''}"]


class BlocksPixmap:
    """Process-wide cache of QIcons and the pixmaps rendered from them."""

    # Two QIcons over one path do not share their render cache, so hold the QIcon.
    _icons: dict[str, QtGui.QIcon] = {}

    # Not QPixmapCache: its idle flush timer drops entries widgets still hold, so they re-render.
    _pixmaps = _PixmapCache(12 * _MIB)

    # Derived from a surface, keyed by cacheKey; separate so thumbnail churn spares the icons.
    _scaled = _PixmapCache(8 * _MIB)
    _tints = _PixmapCache(8 * _MIB)
    # Thumbnails are big and shown once per file, so browsing must not evict icons.
    _thumbnails = _PixmapCache(4 * _MIB)

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
        size: _SizeLike | None = None,
        aspect: QtCore.Qt.AspectRatioMode = _KEEP_ASPECT,
    ) -> QtGui.QPixmap:
        """Return *source* at *size*, cached; an Icon defaults to 128x128, a surface to itself."""
        if isinstance(source, QtGui.QPixmap):
            if size is None:
                return source
            return cls._resampled(source, _as_size(size), aspect)
        target = (
            QtCore.QSize(_ICON_EDGE, _ICON_EDGE) if size is None else _as_size(size)
        )
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
        dpr = pixmap.devicePixelRatio()
        if aspect != _KEEP_ASPECT and pixmap.deviceIndependentSize().toSize() != size:
            pixmap = pixmap.scaled(size * dpr, aspect, _SMOOTH)
            pixmap.setDevicePixelRatio(dpr)
        return cls._pixmaps.put(key, pixmap)

    @classmethod
    def _resampled(
        cls,
        pixmap: QtGui.QPixmap,
        size: QtCore.QSize,
        aspect: QtCore.Qt.AspectRatioMode,
    ) -> QtGui.QPixmap:
        """Resample an existing surface, the only option when no resource path is in hand."""
        if pixmap.isNull():
            return pixmap
        cache = cls._scaled if _cost(pixmap) <= _ICON_SOURCE_COST else cls._thumbnails
        key = (pixmap.cacheKey(), size.width(), size.height(), aspect)
        cached = cache.get(key)
        if cached is not None:
            return cached
        dpr = pixmap.devicePixelRatio()
        scaled = pixmap.scaled(size * dpr, aspect, _SMOOTH)
        scaled.setDevicePixelRatio(dpr)
        return cache.put(key, scaled)

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
        # Same device pixels and ratio, or a HiDPI icon draws at half size.
        result.setDevicePixelRatio(pixmap.devicePixelRatio())
        result.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(result)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(mode)
        painter.fillRect(result.rect(), color)
        painter.end()
        return cls._tints.put(key, result)

    @classmethod
    def source(cls, icon: Icon | str) -> QtGui.QPixmap:
        """Return the intrinsic-size pixmap; only for full-bleed or raster art, never an SVG icon."""
        return QtGui.QPixmap(str(icon))

    @classmethod
    def clear(cls) -> None:
        """Drop every cached icon and pixmap, called from on_quit while qApp is alive."""
        for cache in (
            cls._icons,
            cls._pixmaps,
            cls._scaled,
            cls._tints,
            cls._thumbnails,
        ):
            cache.clear()
