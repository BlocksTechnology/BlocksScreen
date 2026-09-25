"""Configuration manager package contains tools that automatically configure a Blocks machine."""

from .configurator import ConfigManager
from .device_configurator import DeviceConfigManager
from .device_watcher import DeviceConfigWatcher

__version__ = "0.0.1"
__all__ = ["ConfigManager", "DeviceConfigManager", "DeviceConfigWatcher"]
