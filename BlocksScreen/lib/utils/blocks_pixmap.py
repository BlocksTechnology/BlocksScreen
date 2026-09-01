"""One load-once registry for every Qt resource pixmap the panel draws.

Loading an icon by path yields its intrinsic buffer, which for most of the
btn_icons is a 600x600 RGBA surface costing 1.37 MiB even when it is painted at
32px. Going through QIcon instead makes QSvgIconEngine rasterize at the
requested size: measured on the RF50, the whole set costs 16.1 MiB at 64px
against 273.0 MiB intrinsic, and loads in 278 ms against 848 ms.

Every path lives in the Icon enum so a typo is a NameError rather than Qt's
silent null pixmap, and tests/util/test_blocks_pixmap_unit.py proves each member
still resolves.
"""

from enum import StrEnum
from typing import ClassVar

from PyQt6 import QtCore, QtGui

# Setup-time callers cannot know their paint size, and the widgets rescale anyway;
# 128 clears the tallest button (90px hole, 0.8 fill) at 64 KiB a surface.
ICON_SIZE = QtCore.QSize(128, 128)


class Icon(StrEnum):
    """Every resource key the handwritten panels draw, one member per asset."""

    ABS_FILAMENT_TOPBAR = ":/top_bar_icons/media/topbar/abs_filament_topbar.svg"
    ADD_FILAMENT = ":/filament_related/media/btn_icons/add filament.svg"
    ADD_SPOOL = ":/filament_related/media/btn_icons/add spool.svg"
    ARROW_DOWN = ":/arrow_icons/media/btn_icons/arrow_down.svg"
    ARROW_LEFT = ":/arrow_icons/media/btn_icons/arrow_left.svg"
    ARROW_RIGHT = ":/arrow_icons/media/btn_icons/arrow_right.svg"
    BABYSTEP_GRAPHIC = ":/graphics/media/graphics/babystep_graphic.png"
    BABY_STEP_ICON = ":/z_levelling/media/btn_icons/baby_step_icon.svg"
    BACK = ":/ui/media/btn_icons/back.svg"
    BACKGROUND_1ST = ":/background/media/1st_background.png"
    BACK_FOLDER = ":/ui/media/btn_icons/back_folder.svg"
    BASE_DADOS_SPOOL_1 = ":/filament_related/media/btn_icons/base dados spool 1.svg"
    BLOWER = ":/fan_related/media/btn_icons/blower.svg"
    BLTOUCH = ":/z_levelling/media/btn_icons/bltouch.svg"
    CHANGE_FILAMENT = ":/filament_related/media/btn_icons/change_filament.svg"
    CHECK_GATE_1 = ":/filament_related/media/btn_icons/check gate 1.svg"
    EDDY_MECH = ":/z_levelling/media/btn_icons/eddy_mech.svg"
    EJECT = ":/filament_related/media/btn_icons/eject.svg"
    ERROR = ":/ui/media/btn_icons/error.svg"
    ETHERNET_CONNECTED = ":/network/media/btn_icons/network/ethernet_connected.svg"
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
    HOTSPOT = ":/network/media/btn_icons/hotspot.svg"
    INDUCTIVE = ":/z_levelling/media/btn_icons/inductive.svg"
    INFO = ":/ui/media/btn_icons/info.svg"
    INPUT_SHAPER_AUTO = ":/input_shaper/media/btn_icons/input_shaper_auto.svg"
    INPUT_SHAPER_MANUAL = ":/input_shaper/media/btn_icons/input_shaper_manual.svg"
    LAYERS = ":/ui/media/btn_icons/layers.svg"
    LEDS = ":/ui/media/btn_icons/LEDs.svg"
    LEFT_ARROW = ":/arrow_icons/media/btn_icons/left_arrow.svg"
    LOADED_SPOOL = ":/filament_related/media/btn_icons/loaded_spool.svg"
    LOAD_FILAMENT = ":/filament_related/media/btn_icons/load_filament.svg"
    MOVE_NOZZLE_AWAY = ":/baby_step/media/btn_icons/move_nozzle_away.svg"
    MOVE_NOZZLE_CLOSE = ":/baby_step/media/btn_icons/move_nozzle_close.svg"
    NO = ":/dialog/media/btn_icons/no.svg"
    NOTIFICATION = ":/ui/media/btn_icons/notification.svg"
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
    SAVE = ":/ui/media/btn_icons/save.svg"
    SEE = ":/ui/media/btn_icons/see.svg"
    SPEED = ":/motion/media/btn_icons/speed.svg"
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
    _icons: ClassVar[dict[str, QtGui.QIcon]] = {}
    _pixmaps: ClassVar[dict[tuple[str, int, int], QtGui.QPixmap]] = {}

    _MAX_PIXMAPS = 64

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
    def get(cls, icon: Icon | str, size: QtCore.QSize = ICON_SIZE) -> QtGui.QPixmap:
        """Return *icon* rasterized at *size*, cached across calls."""
        key = (str(icon), size.width(), size.height())
        cached = cls._pixmaps.get(key)
        if cached is not None:
            return cached
        pixmap = cls.icon(icon).pixmap(size)
        cls._pixmaps[key] = pixmap
        # A widget resizing mid-drag mints one entry per pixel width; drop the oldest half.
        if len(cls._pixmaps) > cls._MAX_PIXMAPS:
            for stale in list(cls._pixmaps)[: cls._MAX_PIXMAPS // 2]:
                del cls._pixmaps[stale]
        return pixmap

    @classmethod
    def source(cls, icon: Icon | str) -> QtGui.QPixmap:
        """Return the intrinsic-size pixmap; only for full-bleed art, never a btn_icon."""
        return QtGui.QPixmap(str(icon))

    @classmethod
    def clear(cls) -> None:
        """Drop every cached icon and pixmap, called from on_quit while qApp is alive."""
        cls._icons.clear()
        cls._pixmaps.clear()
