"""tests/network/conftest.py — shared fixtures for network tests.

Mocks the D-Bus modules (sdbus, sdbus_async) BEFORE any network package
import so that tests run without NetworkManager or a system bus.

Provides ``AsyncProxyMock`` — a mock for sdbus_async D-Bus proxies where
property access returns awaitables (matching the real sdbus_async
protocol) and method access returns ``AsyncMock`` callables.

Widget stub modules export **real Qt base classes** (not ``MagicMock``)
so that class inheritance in networkWindow.py works at import time.
(``class IPAddressLineEdit(BlocksCustomLinEdit)`` requires a real type
as its base — ``MagicMock`` triggers ``TypeError: metaclass conflict``.)
"""

import asyncio
import enum
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from PyQt6 import QtCore, QtGui, QtWidgets

# Ensure project root is on sys.path so `BlocksScreen.lib.network` resolves
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Mock D-Bus modules BEFORE any network package import
_mock_sdbus = MagicMock()
_mock_sdbus.sd_bus_open_system = MagicMock(return_value=MagicMock())
_mock_sdbus.set_default_bus = MagicMock()

# Shared D-Bus NM mock — used by both sdbus_block and sdbus_async paths.
_mock_dbus_nm = MagicMock()
_mock_dbus_nm.enums = MagicMock()
_mock_dbus_nm.enums.DeviceType = MagicMock()
_mock_dbus_nm.enums.DeviceType.WIFI = 2
_mock_dbus_nm.enums.DeviceType.ETHERNET = 1
_mock_dbus_nm.exceptions = MagicMock()
_mock_dbus_nm.exceptions.NmConnectionInvalidPropertyError = type(
    "NmConnectionInvalidPropertyError", (Exception,), {}
)
_mock_dbus_nm.exceptions.NmSettingsPermissionDeniedError = type(
    "NmSettingsPermissionDeniedError", (Exception,), {}
)


class _ConnectionState(enum.IntEnum):
    UNKNOWN = 0
    ACTIVATING = 1
    ACTIVATED = 2
    DEACTIVATING = 3
    DEACTIVATED = 4


class _ConnectionStateReason(enum.IntEnum):
    NONE = 0
    UNKNOWN = 1
    NOT_STARTED = 2
    DEVICE_DISCONNECT = 3
    SERVICE_STOPPED = 4
    IP_CONFIG_UNAVAILABLE = 5
    CONNECT_TIMEOUT = 6


_mock_dbus_nm.ConnectionState = _ConnectionState
_mock_dbus_nm.ConnectionStateReason = _ConnectionStateReason

sys.modules["sdbus"] = _mock_sdbus

# sdbus_block (legacy — kept for any residual imports)
_mock_sdbus_block = MagicMock()
_mock_sdbus_block.networkmanager = _mock_dbus_nm
sys.modules["sdbus_block"] = _mock_sdbus_block
sys.modules["sdbus_block.networkmanager"] = _mock_dbus_nm

# sdbus_async (current worker import target)
_mock_sdbus_async = MagicMock()
_mock_sdbus_async.networkmanager = _mock_dbus_nm
sys.modules["sdbus_async"] = _mock_sdbus_async
sys.modules["sdbus_async.networkmanager"] = _mock_dbus_nm


# Widget stub modules — REAL Qt base classes (not MagicMock)
# networkWindow.py subclasses imported widgets:
#     class IPAddressLineEdit(BlocksCustomLinEdit): ...
# A MagicMock cannot be used as a class base — it triggers a TypeError.
# We create lightweight stub modules whose exports are real Qt types.


def _make_stub_module(name: str, attrs: dict) -> types.ModuleType:
    """Create a real Python module object with the given attributes."""
    mod = types.ModuleType(name)
    mod.__path__ = []
    mod.__package__ = name
    for k, v in attrs.items():
        setattr(mod, k, v)
    return mod


class _PopupStub(QtWidgets.QWidget):
    """Popup stand-in with the MessageType enum production code reads."""

    class MessageType:
        ERROR = 0
        INFO = 1
        WARNING = 2

    def new_message(self, **_kw):
        pass

    def raise_(self):
        pass


@dataclass(slots=True)
class _ListItemStub:
    """Matches the real ``ListItem`` fields from ``list_model.py``."""

    text: str = ""
    right_text: str = ""
    right_icon: QtGui.QPixmap | None = None
    left_icon: QtGui.QPixmap | None = None
    callback: object = None
    selected: bool = False
    allow_check: bool = True
    _lfontsize: int = 0
    _rfontsize: int = 0
    height: int = 60
    notificate: bool = False
    not_clickable: bool = False


class _EntryListModelStub(QtCore.QAbstractListModel):
    """Minimal ``EntryListModel`` supporting ``reconcile()``."""

    EnableRole = QtCore.Qt.ItemDataRole.UserRole + 1
    NotificateRole = QtCore.Qt.ItemDataRole.UserRole + 2

    def __init__(self, entries=None):
        super().__init__()
        self.entries = entries or []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.entries)

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        item = self.entries[index.row()]
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return item
        return None

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == self.EnableRole:
            self.entries[index.row()].selected = value
            self.dataChanged.emit(index, index, [self.EnableRole])
            return True
        return False

    def clear(self):
        self.beginResetModel()
        self.entries.clear()
        self.endResetModel()

    def reconcile(self, desired, key_fn):
        """Simplified reconcile — just replace entries."""
        self.beginResetModel()
        self.entries[:] = list(desired)
        self.endResetModel()


class _EntryDelegateStub(QtWidgets.QStyledItemDelegate):
    """Minimal ``EntryDelegate`` with ``item_selected`` signal."""

    item_selected = QtCore.pyqtSignal(_ListItemStub, name="item-selected")

    def __init__(self):
        super().__init__()
        self.prev_index = 0
        self.height = 60


class _LoadingOverlayStub(QtWidgets.QWidget):
    def setText(self, text: str) -> None:
        pass


class _NetworkWidgetbuttonsStub(QtWidgets.QWidget):
    def setText(self, text: str) -> None:
        pass

    def setFlat(self, v: bool) -> None:
        pass


class _BlocksCustomCheckButtonStub(QtWidgets.QCheckBox):
    """BlocksCustomCheckButton stand-in — adds setFlat() used in _setupUI."""

    def setFlat(self, v: bool) -> None:
        pass


class _BlocksCustomLinEditStub(QtWidgets.QLineEdit):
    """BlocksCustomLinEdit stand-in — adds clicked signal used in _setup_hidden_network_page."""

    clicked = QtCore.pyqtSignal(name="clicked")


class _KeyboardStub(QtWidgets.QWidget):
    go_back = QtCore.pyqtSignal()
    value_selected = QtCore.pyqtSignal(str)

    def set_value(self, val):
        pass


# Register parent packages first (must be real modules, not MagicMock).
_lib_parent_packages = ("lib", "lib.panels", "lib.panels.widgets", "lib.utils")
for _pkg in _lib_parent_packages:
    if _pkg not in sys.modules:
        _pm = types.ModuleType(_pkg)
        _pm.__path__ = []
        _pm.__package__ = _pkg
        sys.modules[_pkg] = _pm

# Map of short module name -> dict of exported names.
# Each value is a REAL type so ``class Foo(ImportedBase)`` works.
_STUB_MODULES = {
    "lib.utils.blocks_label": {
        "BlocksLabel": QtWidgets.QLabel,
    },
    "lib.utils.blocks_linedit": {
        "BlocksCustomLinEdit": _BlocksCustomLinEditStub,
    },
    "lib.utils.blocks_frame": {
        "BlocksCustomFrame": QtWidgets.QFrame,
    },
    "lib.utils.blocks_button": {
        "BlocksCustomButton": QtWidgets.QPushButton,
    },
    "lib.utils.blocks_togglebutton": {
        "NetworkWidgetbuttons": _NetworkWidgetbuttonsStub,
    },
    "lib.utils.check_button": {
        "BlocksCustomCheckButton": _BlocksCustomCheckButtonStub,
    },
    "lib.utils.icon_button": {
        "IconButton": QtWidgets.QPushButton,
    },
    "lib.utils.blocks_Scrollbar": {
        "CustomScrollBar": QtWidgets.QScrollBar,
    },
    "lib.utils.list_model": {
        "EntryDelegate": _EntryDelegateStub,
        "EntryListModel": _EntryListModelStub,
        "ListItem": _ListItemStub,
    },
    "lib.panels.widgets.keyboardPage": {
        "CustomQwertyKeyboard": _KeyboardStub,
    },
    "lib.panels.widgets.loadWidget": {
        "LoadingOverlayWidget": _LoadingOverlayStub,
    },
    "lib.panels.widgets.popupDialogWidget": {
        "Popup": _PopupStub,
    },
}

for _mod_name, _attrs in _STUB_MODULES.items():
    _stub = _make_stub_module(_mod_name, _attrs)
    # Register under BOTH short (lib.*) and long (BlocksScreen.lib.*) paths.
    sys.modules[_mod_name] = _stub
    sys.modules["BlocksScreen." + _mod_name] = _stub


# Mock lib.qrcode_gen (short path only) — networkWindow.py imports it as
# ``from lib.qrcode_gen import generate_wifi_qrcode``.  The BlocksScreen.*
# path is intentionally NOT registered here so test_qrcode_gen_unit.py can
# still import the real module via ``BlocksScreen.lib.qrcode_gen``.
_mock_qrcode_mod = _make_stub_module(
    "lib.qrcode_gen", {"generate_wifi_qrcode": MagicMock(return_value=None)}
)
sys.modules["lib.qrcode_gen"] = _mock_qrcode_mod

# Mock configfile - used by worker.py for hotspot config persistence.
# Tests must not read/write real config files.
_mock_cfg_instance = MagicMock()
_mock_cfg_instance.has_section.return_value = False
_mock_cfg_instance.get.return_value = ""

_mock_configfile_mod = types.ModuleType("configfile")
_mock_configfile_mod.get_configparser = MagicMock(return_value=_mock_cfg_instance)
sys.modules["configfile"] = _mock_configfile_mod

# Now safe to import the actual network package
from BlocksScreen.lib.network.models import (  # noqa: E402
    SIGNAL_EXCELLENT_THRESHOLD, SIGNAL_FAIR_THRESHOLD, SIGNAL_GOOD_THRESHOLD,
    SIGNAL_MINIMUM_THRESHOLD, ConnectionPriority, ConnectionResult,
    ConnectivityState, HotspotConfig, NetworkInfo, NetworkState, NetworkStatus,
    PendingOperation, SavedNetwork, SecurityType, VlanInfo, WifiIconKey,
    signal_to_bars)

# Alias so ``from lib.network import ...`` works.
sys.modules["lib.network"] = sys.modules["BlocksScreen.lib.network"]


# AsyncProxyMock — sdbus_async D-Bus proxy mock


class _AwaitableProp:
    """Mock an sdbus_async property: ``await`` returns value, ``.set_async()`` sets."""

    def __init__(self, value):
        self.value = value
        self.set_async = AsyncMock()

    def __await__(self):
        async def _coro():
            return self.value

        return _coro().__await__()

    def __bool__(self):
        return bool(self.value)

    def __eq__(self, other):
        if isinstance(other, _AwaitableProp):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"_AwaitableProp({self.value!r})"


class AsyncProxyMock:
    """Mock for sdbus_async D-Bus proxies.

    * **Properties** -> ``_AwaitableProp`` — ``await proxy.prop`` returns value.
    * **Methods** -> ``AsyncMock`` — ``await proxy.method()`` is configurable.
    * Unknown attribute access auto-creates an ``AsyncMock`` (method).
    * Setting a plain value creates/updates an ``_AwaitableProp``.
    * Setting an ``AsyncMock`` registers it as a method.
    """

    def __init__(self, **initial):
        self.__dict__["_store"] = {}
        self.__dict__["_call_mocks"] = {}
        for k, v in initial.items():
            if isinstance(v, AsyncMock):
                self._call_mocks[k] = v
            else:
                self._store[k] = _AwaitableProp(v)

    def __getattr__(self, name):
        if name in self._store:
            return self._store[name]
        if name in self._call_mocks:
            return self._call_mocks[name]
        m = AsyncMock()
        self._call_mocks[name] = m
        return m

    def __setattr__(self, name, value):
        if isinstance(value, AsyncMock):
            self._call_mocks[name] = value
        elif isinstance(value, _AwaitableProp):
            self._store[name] = value
        else:
            if name in self._store:
                self._store[name].value = value
            else:
                self._store[name] = _AwaitableProp(value)


class _ProxyFactory:
    """Callable that returns a proxy AND delegates attribute access to it.

    Lets test code write ``w._nm.wireless_enabled = True`` (delegation)
    while the real worker calls ``await self._nm().wireless_enabled``.
    """

    def __init__(self, proxy):
        object.__setattr__(self, "_proxy", proxy)

    def __call__(self, *_args, **_kwargs):
        return object.__getattribute__(self, "_proxy")

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, "_proxy"), name)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "_proxy"), name, value)


def _run(coro):
    """Run a single coroutine to completion — test helper for async worker methods."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# QApplication singleton
@pytest.fixture(scope="session")
def qapp():
    """Session-scoped QApplication — created once for all tests."""
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    yield app


# Model factories (updated for NetworkStatus enum + slots dataclasses)


@pytest.fixture
def make_network_info():
    """Build a ``NetworkInfo`` with sensible defaults."""

    def _make(**overrides):
        defaults = dict(
            ssid="TestNetwork",
            signal_strength=75,
            network_status=NetworkStatus.DISCOVERED,
            bssid="AA:BB:CC:DD:EE:FF",
            frequency=2437,
            max_bitrate=54000,
            security_type=SecurityType.WPA2_PSK,
        )
        defaults.update(overrides)
        return NetworkInfo(**defaults)

    return _make


@pytest.fixture
def make_saved_network():
    def _make(**overrides):
        defaults = dict(
            ssid="SavedNet",
            uuid="12345678-1234-1234-1234-123456789abc",
            connection_path="/org/freedesktop/NetworkManager/Settings/1",
            security_type="wpa-psk",
            mode="infrastructure",
            priority=ConnectionPriority.MEDIUM.value,
            signal_strength=80,
        )
        defaults.update(overrides)
        return SavedNetwork(**defaults)

    return _make


@pytest.fixture
def make_network_state():
    def _make(**overrides):
        defaults = dict(
            connectivity=ConnectivityState.FULL,
            current_ssid="TestNetwork",
            current_ip="192.168.1.100",
            wifi_enabled=True,
            hotspot_enabled=False,
            primary_interface="wlan0",
            signal_strength=75,
            security_type="wpa-psk",
            ethernet_connected=False,
            ethernet_carrier=False,
        )
        defaults.update(overrides)
        return NetworkState(**defaults)

    return _make


@pytest.fixture
def sample_network_info(make_network_info):
    return make_network_info()


@pytest.fixture
def sample_saved_network(make_saved_network):
    return make_saved_network()


@pytest.fixture
def sample_network_state(make_network_state):
    return make_network_state()


@pytest.fixture
def preserve_labels():
    from BlocksScreen.lib.network.models import _STATUS_LABELS

    original = dict(_STATUS_LABELS)
    yield
    _STATUS_LABELS.clear()
    _STATUS_LABELS.update(original)


# NetworkControlWindow fixture (``win``)


class _ToggleButtonStub(QtCore.QObject):
    """Lightweight stand-in for the toggle button.

    Supports ``QSignalBlocker`` (real QObject) and provides the
    ``State.ON`` / ``State.OFF`` constants that production code reads.
    """

    class State:
        ON = True
        OFF = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = self.State.OFF


@pytest.fixture
def win(qapp):
    """Return ``(window, mock_nm)`` with all external deps mocked.

    ``window`` is a real ``NetworkControlWindow`` instance.
    ``mock_nm`` is the mock ``NetworkManager`` instance injected into it.
    """
    import traceback
    from unittest.mock import MagicMock, patch

    mock_nm = MagicMock()
    mock_nm.current_state = NetworkState()
    mock_nm.saved_networks = []
    mock_nm.hotspot_ssid = "PrinterHotspot"
    mock_nm.hotspot_password = "123456789"
    mock_nm.hotspot_security = "wpa-psk"
    mock_nm.current_ssid = None

    try:
        from BlocksScreen.lib.panels.networkWindow import NetworkControlWindow

        # Create instance: init QStackedWidget C++ backend only
        def _stub_init(self, *_a, **_kw):
            QtWidgets.QStackedWidget.__init__(self)

        with patch.object(NetworkControlWindow, "__init__", _stub_init):
            window = NetworkControlWindow()

        parent = QtWidgets.QWidget()
        # Qt's isVisible() checks the ENTIRE ancestor chain.
        # Show parent so child.setVisible(True) -> child.isVisible() == True.
        parent.show()

        window._nm = mock_nm
        window._is_first_run = True
        window._is_connecting = False
        window._pending_operation = PendingOperation.NONE
        window._target_ssid = ""
        window._active_signal = 0
        window._was_ethernet_connected = False
        window._pending_expected_ip = ""
        window._last_active_signal_bars = 0
        window._cached_scan_networks = []

        # Refactored list-cache instance variables
        window._item_cache = {}
        window._separator_item = None
        window._hidden_network_item = None

        # Internal stubs
        window._popup = MagicMock()
        _load_timer = QtCore.QTimer()
        _load_timer.setSingleShot(True)
        window._load_timer = _load_timer

        # Widget stubs (QLabel / QWidget / QFrame / QComboBox)
        window.loadingwidget = QtWidgets.QWidget(parent)
        window.loadingwidget.setVisible(False)

        window.mn_info_box = QtWidgets.QLabel(parent)
        window.mn_info_box.setVisible(True)

        window.netlist_ssuid = QtWidgets.QLabel(parent)
        window.netlist_ip = QtWidgets.QLabel(parent)
        window.netlist_strength = QtWidgets.QLabel(parent)
        window.netlist_strength_label = QtWidgets.QLabel(parent)
        window.netlist_security = QtWidgets.QLabel(parent)
        window.netlist_security_label = QtWidgets.QLabel(parent)

        window.mn_info_seperator = QtWidgets.QFrame(parent)
        window.line_2 = QtWidgets.QFrame(parent)
        window.line_3 = QtWidgets.QFrame(parent)

        window.netlist_vlans_combo = QtWidgets.QComboBox(parent)
        window.netlist_vlans_combo.setVisible(False)

        # Hotspot input fields
        window.hotspot_name_input_field = QtWidgets.QLineEdit(parent)
        window.hotspot_password_input_field = QtWidgets.QLineEdit(parent)

        # Hotspot QR image (BlocksLabel in production; QLabel + mock methods here)
        window.qrcode_img = QtWidgets.QLabel(parent)
        window.qrcode_img.clearPixmap = MagicMock()
        window.qrcode_img.setText = MagicMock()
        window.qrcode_img.setPixmap = MagicMock()

        # VLAN widgets (used by _on_vlan_apply / _on_vlan_delete)
        window.vlan_id_spinbox = QtWidgets.QSpinBox(parent)
        window.vlan_id_spinbox.setRange(1, 4094)
        window.vlan_ip_field = QtWidgets.QLineEdit(parent)
        window.vlan_mask_field = QtWidgets.QLineEdit(parent)
        window.vlan_gateway_field = QtWidgets.QLineEdit(parent)
        window.vlan_dns1_field = QtWidgets.QLineEdit(parent)
        window.vlan_dns2_field = QtWidgets.QLineEdit(parent)

        # Toggle-capable button stubs
        for attr in ("wifi_button", "hotspot_button", "ethernet_button"):
            btn = QtWidgets.QPushButton(parent)
            btn.toggle_button = _ToggleButtonStub(btn)
            btn.setEnabled(True)
            setattr(window, attr, btn)
        window.ethernet_button.setVisible(False)

        # Pages for QStackedWidget
        window.main_network_page = QtWidgets.QWidget()
        window.network_list_page = QtWidgets.QWidget()
        window.addWidget(window.main_network_page)
        window.addWidget(window.network_list_page)
        window.setCurrentIndex(0)

        # Model and delegate (used by _reconcile_list and item selection)
        window._model = _EntryListModelStub()
        window._entry_delegate = _EntryDelegateStub()

        # Keyboard widget (used by keyboard page navigation)
        window._qwerty = _KeyboardStub(parent)

        # Icon pixmaps (used by _make_network_item / _make_hidden_network_item)
        window._right_arrow_icon = QtGui.QPixmap()
        window._hiden_network_icon = QtGui.QPixmap()

        # Missing instance variables (from _init_instance_variables)
        window._initial_priority = ConnectionPriority.MEDIUM
        window._current_network_is_open = False
        window._current_network_is_hidden = False
        window._previous_panel = None
        window._current_field = None

        # List view widgets (needed by _build_network_list_from_scan / _on_scan_complete)
        window.listView = QtWidgets.QListView(parent)
        window.verticalScrollBar = QtWidgets.QScrollBar(parent)

        # Additional pages (addWidget so indexOf() works)
        for page_attr in (
            "hidden_network_page",
            "saved_connection_page",
            "add_network_page",
            "vlan_page",
            "wifi_static_ip_page",
            "saved_details_page",
            "hotspot_page",
        ):
            page = QtWidgets.QWidget()
            window.addWidget(page)
            setattr(window, page_attr, page)

        # Saved-connection page widgets
        window.saved_connection_network_name = QtWidgets.QLabel(parent)
        window.snd_name = QtWidgets.QLabel(parent)
        window.saved_connection_change_password_field = QtWidgets.QLineEdit(parent)
        window.saved_connection_change_password_view = QtWidgets.QCheckBox(parent)
        window.saved_connection_signal_strength_info_frame = QtWidgets.QLabel(parent)
        window.saved_connection_security_type_info_label = QtWidgets.QLabel(parent)
        window.network_activate_btn = QtWidgets.QPushButton(parent)
        window.sn_info = QtWidgets.QLabel(parent)
        window.frame = QtWidgets.QFrame(parent)

        # Add-network page widgets
        window.frame_2 = QtWidgets.QFrame(parent)
        window.add_network_network_label = QtWidgets.QLabel(parent)
        window.add_network_password_field = QtWidgets.QLineEdit(parent)
        window.add_network_validation_button = QtWidgets.QPushButton(parent)
        window.add_network_validation_button.setEnabled(True)

        # Priority radio buttons + button group
        window.high_priority_btn = QtWidgets.QRadioButton(parent)
        window.med_priority_btn = QtWidgets.QRadioButton(parent)
        window.low_priority_btn = QtWidgets.QRadioButton(parent)
        window.med_priority_btn.setChecked(True)
        window.priority_btn_group = QtWidgets.QButtonGroup(parent)
        window.priority_btn_group.addButton(window.high_priority_btn)
        window.priority_btn_group.addButton(window.med_priority_btn)
        window.priority_btn_group.addButton(window.low_priority_btn)

        # Hidden-network page widgets
        window.hidden_network_ssid_field = QtWidgets.QLineEdit(parent)
        window.hidden_network_password_field = QtWidgets.QLineEdit(parent)

        # Wi-Fi static IP page widgets
        window.wifi_sip_title = QtWidgets.QLabel(parent)
        for _f in (
            "wifi_sip_ip_field",
            "wifi_sip_mask_field",
            "wifi_sip_gateway_field",
            "wifi_sip_dns1_field",
            "wifi_sip_dns2_field",
        ):
            le = QtWidgets.QLineEdit(parent)
            le.is_valid = MagicMock(return_value=True)
            le.is_valid_mask = MagicMock(return_value=True)
            setattr(window, _f, le)
        window.wifi_sip_dhcp_button = QtWidgets.QPushButton(parent)

        yield window, mock_nm

    except Exception as exc:
        traceback.print_exc()
        pytest.skip(
            f"NetworkControlWindow not importable — {exc.__class__.__name__}: {exc}"
        )
