# pylint: disable=protected-access

import asyncio
import logging

from PyQt6.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot

from .models import (
    ConnectionPriority,
    ConnectionResult,
    ConnectivityState,
    NetworkInfo,
    NetworkState,
    SavedNetwork,
)
from .worker import NetworkManagerWorker

logger = logging.getLogger(__name__)

_KEEPALIVE_POLL_MS: int = 300_000  # 5 minutes — safety net for missed signals
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


class NetworkManager(QObject):
    """Main-thread manager/interface to the NetworkManager D-Bus worker.

    The UI layer should only interact with this class.  Internally it owns
    a ``NetworkManagerWorker`` that runs all D-Bus coroutines on its
    dedicated asyncio thread.

    Coroutines are submitted to ``worker._asyncio_loop`` — the same loop
    on which the D-Bus file-descriptor was registered — so signal delivery
    and async I/O always occur on the correct selector.

    """

    state_changed = pyqtSignal(NetworkState)
    networks_scanned = pyqtSignal(list)
    saved_networks_loaded = pyqtSignal(list)
    connection_result = pyqtSignal(ConnectionResult)
    connectivity_changed = pyqtSignal(ConnectivityState)
    error_occurred = pyqtSignal(str, str)
    reconnect_complete = pyqtSignal()
    hotspot_config_updated = pyqtSignal(str, str, str)

    def __init__(self, parent: QObject | None = None) -> None:
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁ__init____mutmut_orig(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_1(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(None)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_2(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = None
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_3(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = None
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_4(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = None
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_5(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = None
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_6(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = None

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_7(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = None
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_8(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = True
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_9(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = None

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_10(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = True

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_11(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = None

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_12(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = None

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_13(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = None
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_14(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = None
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_15(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = None
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_16(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(None)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_17(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(None)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_18(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(None)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_19(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(None)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_20(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(None)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_21(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(None)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_22(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(None)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_23(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(None)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_24(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(None)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_25(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = None
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_26(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(None)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_27(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(None)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_28(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(None)

        logger.info("NetworkManager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_29(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info(None)

    def xǁNetworkManagerǁ__init____mutmut_30(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("XXNetworkManager manager created (waiting for worker init)XX")

    def xǁNetworkManagerǁ__init____mutmut_31(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("networkmanager manager created (waiting for worker init)")

    def xǁNetworkManagerǁ__init____mutmut_32(self, parent: QObject | None = None) -> None:
        """Create the worker, wire all signals"""
        super().__init__(parent)

        self._cached_state: NetworkState = NetworkState()
        self._cached_networks: list[NetworkInfo] = []
        self._cached_saved: list[SavedNetwork] = []
        self._network_info_map: dict[str, NetworkInfo] = {}
        self._saved_network_map: dict[str, SavedNetwork] = {}

        self._shutting_down: bool = False
        self._worker_ready: bool = False

        self._pending_futures: set["asyncio.Future"] = set()

        self._worker = NetworkManagerWorker()

        self._cached_hotspot_ssid: str = self._worker._hotspot_config.ssid
        self._cached_hotspot_password: str = self._worker._hotspot_config.password
        self._cached_hotspot_security: str = self._worker._hotspot_config.security
        self._worker.state_changed.connect(self._on_state_changed)
        self._worker.networks_scanned.connect(self._on_networks_scanned)
        self._worker.saved_networks_loaded.connect(self._on_saved_networks_loaded)
        self._worker.connection_result.connect(self.connection_result)
        self._worker.connectivity_changed.connect(self.connectivity_changed)
        self._worker.error_occurred.connect(self.error_occurred)
        self._worker.hotspot_info_ready.connect(self._on_hotspot_info_ready)
        self._worker.reconnect_complete.connect(self.reconnect_complete)
        self._worker.initialized.connect(self._on_worker_initialized)

        # Keepalive timer — safety net for any missed D-Bus signals.
        self._keepalive_timer = QTimer(self)
        self._keepalive_timer.setInterval(_KEEPALIVE_POLL_MS)
        self._keepalive_timer.timeout.connect(self._on_keepalive_tick)

        logger.info("NETWORKMANAGER MANAGER CREATED (WAITING FOR WORKER INIT)")
    
    xǁNetworkManagerǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁ__init____mutmut_1': xǁNetworkManagerǁ__init____mutmut_1, 
        'xǁNetworkManagerǁ__init____mutmut_2': xǁNetworkManagerǁ__init____mutmut_2, 
        'xǁNetworkManagerǁ__init____mutmut_3': xǁNetworkManagerǁ__init____mutmut_3, 
        'xǁNetworkManagerǁ__init____mutmut_4': xǁNetworkManagerǁ__init____mutmut_4, 
        'xǁNetworkManagerǁ__init____mutmut_5': xǁNetworkManagerǁ__init____mutmut_5, 
        'xǁNetworkManagerǁ__init____mutmut_6': xǁNetworkManagerǁ__init____mutmut_6, 
        'xǁNetworkManagerǁ__init____mutmut_7': xǁNetworkManagerǁ__init____mutmut_7, 
        'xǁNetworkManagerǁ__init____mutmut_8': xǁNetworkManagerǁ__init____mutmut_8, 
        'xǁNetworkManagerǁ__init____mutmut_9': xǁNetworkManagerǁ__init____mutmut_9, 
        'xǁNetworkManagerǁ__init____mutmut_10': xǁNetworkManagerǁ__init____mutmut_10, 
        'xǁNetworkManagerǁ__init____mutmut_11': xǁNetworkManagerǁ__init____mutmut_11, 
        'xǁNetworkManagerǁ__init____mutmut_12': xǁNetworkManagerǁ__init____mutmut_12, 
        'xǁNetworkManagerǁ__init____mutmut_13': xǁNetworkManagerǁ__init____mutmut_13, 
        'xǁNetworkManagerǁ__init____mutmut_14': xǁNetworkManagerǁ__init____mutmut_14, 
        'xǁNetworkManagerǁ__init____mutmut_15': xǁNetworkManagerǁ__init____mutmut_15, 
        'xǁNetworkManagerǁ__init____mutmut_16': xǁNetworkManagerǁ__init____mutmut_16, 
        'xǁNetworkManagerǁ__init____mutmut_17': xǁNetworkManagerǁ__init____mutmut_17, 
        'xǁNetworkManagerǁ__init____mutmut_18': xǁNetworkManagerǁ__init____mutmut_18, 
        'xǁNetworkManagerǁ__init____mutmut_19': xǁNetworkManagerǁ__init____mutmut_19, 
        'xǁNetworkManagerǁ__init____mutmut_20': xǁNetworkManagerǁ__init____mutmut_20, 
        'xǁNetworkManagerǁ__init____mutmut_21': xǁNetworkManagerǁ__init____mutmut_21, 
        'xǁNetworkManagerǁ__init____mutmut_22': xǁNetworkManagerǁ__init____mutmut_22, 
        'xǁNetworkManagerǁ__init____mutmut_23': xǁNetworkManagerǁ__init____mutmut_23, 
        'xǁNetworkManagerǁ__init____mutmut_24': xǁNetworkManagerǁ__init____mutmut_24, 
        'xǁNetworkManagerǁ__init____mutmut_25': xǁNetworkManagerǁ__init____mutmut_25, 
        'xǁNetworkManagerǁ__init____mutmut_26': xǁNetworkManagerǁ__init____mutmut_26, 
        'xǁNetworkManagerǁ__init____mutmut_27': xǁNetworkManagerǁ__init____mutmut_27, 
        'xǁNetworkManagerǁ__init____mutmut_28': xǁNetworkManagerǁ__init____mutmut_28, 
        'xǁNetworkManagerǁ__init____mutmut_29': xǁNetworkManagerǁ__init____mutmut_29, 
        'xǁNetworkManagerǁ__init____mutmut_30': xǁNetworkManagerǁ__init____mutmut_30, 
        'xǁNetworkManagerǁ__init____mutmut_31': xǁNetworkManagerǁ__init____mutmut_31, 
        'xǁNetworkManagerǁ__init____mutmut_32': xǁNetworkManagerǁ__init____mutmut_32
    }
    xǁNetworkManagerǁ__init____mutmut_orig.__name__ = 'xǁNetworkManagerǁ__init__'

    def _schedule(self, coro: "asyncio.Coroutine") -> None:
        args = [coro]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁ_schedule__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁ_schedule__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁ_schedule__mutmut_orig(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_1(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = None
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_2(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = None
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_3(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(None, loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_4(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, None)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_5(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_6(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, )
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_7(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(None)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_8(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(future)
            future.add_done_callback(None)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_9(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                None,
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_10(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                None,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_11(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_12(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "Dropping early coroutine — loop not yet running: %s",
                )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_13(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "XXDropping early coroutine — loop not yet running: %sXX",
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_14(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "dropping early coroutine — loop not yet running: %s",
                coro.__qualname__,
            )
            coro.close()

    def xǁNetworkManagerǁ_schedule__mutmut_15(self, coro: "asyncio.Coroutine") -> None:
        """Submit *coro* to the worker's asyncio loop from the main thread.

         Stores a strong reference to the returned
        Future to prevent Python's GC from destroying the underlying
        asyncio.Task while it is still running.
        """
        if self._shutting_down:
            coro.close()
            return
        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(coro, loop)
            self._pending_futures.add(future)
            future.add_done_callback(self._pending_futures.discard)
        else:
            logger.debug(
                "DROPPING EARLY COROUTINE — LOOP NOT YET RUNNING: %S",
                coro.__qualname__,
            )
            coro.close()
    
    xǁNetworkManagerǁ_schedule__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁ_schedule__mutmut_1': xǁNetworkManagerǁ_schedule__mutmut_1, 
        'xǁNetworkManagerǁ_schedule__mutmut_2': xǁNetworkManagerǁ_schedule__mutmut_2, 
        'xǁNetworkManagerǁ_schedule__mutmut_3': xǁNetworkManagerǁ_schedule__mutmut_3, 
        'xǁNetworkManagerǁ_schedule__mutmut_4': xǁNetworkManagerǁ_schedule__mutmut_4, 
        'xǁNetworkManagerǁ_schedule__mutmut_5': xǁNetworkManagerǁ_schedule__mutmut_5, 
        'xǁNetworkManagerǁ_schedule__mutmut_6': xǁNetworkManagerǁ_schedule__mutmut_6, 
        'xǁNetworkManagerǁ_schedule__mutmut_7': xǁNetworkManagerǁ_schedule__mutmut_7, 
        'xǁNetworkManagerǁ_schedule__mutmut_8': xǁNetworkManagerǁ_schedule__mutmut_8, 
        'xǁNetworkManagerǁ_schedule__mutmut_9': xǁNetworkManagerǁ_schedule__mutmut_9, 
        'xǁNetworkManagerǁ_schedule__mutmut_10': xǁNetworkManagerǁ_schedule__mutmut_10, 
        'xǁNetworkManagerǁ_schedule__mutmut_11': xǁNetworkManagerǁ_schedule__mutmut_11, 
        'xǁNetworkManagerǁ_schedule__mutmut_12': xǁNetworkManagerǁ_schedule__mutmut_12, 
        'xǁNetworkManagerǁ_schedule__mutmut_13': xǁNetworkManagerǁ_schedule__mutmut_13, 
        'xǁNetworkManagerǁ_schedule__mutmut_14': xǁNetworkManagerǁ_schedule__mutmut_14, 
        'xǁNetworkManagerǁ_schedule__mutmut_15': xǁNetworkManagerǁ_schedule__mutmut_15
    }
    xǁNetworkManagerǁ_schedule__mutmut_orig.__name__ = 'xǁNetworkManagerǁ_schedule'

    @pyqtSlot()
    def _on_worker_initialized(self) -> None:
        """Called once when the worker finishes
            D-Bus init and interface detection.

        Starts the keepalive timer *after* _primary_wifi_path and
        _primary_wired_path are populated, eliminating the old 2-second
        guess-timer that raced with init on slow boots.
        """
        if self._shutting_down:
            return
        self._worker_ready = True
        logger.info(
            "Worker initialised — starting keepalive (every %d ms)",
            _KEEPALIVE_POLL_MS,
        )
        self._keepalive_timer.start()
        self._schedule(self._worker._async_get_current_state())
        self._schedule(self._worker._async_scan_networks())
        self._schedule(self._worker._async_load_saved_networks())

    def shutdown(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁshutdown__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁshutdown__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁshutdown__mutmut_orig(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_1(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = None
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_2(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = False
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_3(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = None
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_4(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = None
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_5(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                None, loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_6(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), None
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_7(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_8(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_9(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=None)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_10(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=6.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_11(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning(None, exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_12(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", None)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_13(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning(exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_14(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", )

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_15(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("XXWorker shutdown coroutine raised: %sXX", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_16(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_17(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("WORKER SHUTDOWN COROUTINE RAISED: %S", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_18(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=None)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_19(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=4.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_20(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning(None)

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_21(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("XXAsyncio thread did not exit within 3 sXX")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_22(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_23(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("ASYNCIO THREAD DID NOT EXIT WITHIN 3 S")

        self._pending_futures.clear()

        logger.info("NetworkManager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_24(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info(None)

    def xǁNetworkManagerǁshutdown__mutmut_25(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("XXNetworkManager manager shutdown completeXX")

    def xǁNetworkManagerǁshutdown__mutmut_26(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("networkmanager manager shutdown complete")

    def xǁNetworkManagerǁshutdown__mutmut_27(self) -> None:
        """Gracefully stop the worker, asyncio loop, and background thread."""
        self._shutting_down = True
        self._keepalive_timer.stop()

        loop = self._worker._asyncio_loop
        if loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._worker._async_shutdown(), loop
            )
            try:
                future.result(timeout=5.0)
            except Exception as exc:
                logger.warning("Worker shutdown coroutine raised: %s", exc)

        self._worker._asyncio_thread.join(timeout=3.0)
        if self._worker._asyncio_thread.is_alive():
            logger.warning("Asyncio thread did not exit within 3 s")

        self._pending_futures.clear()

        logger.info("NETWORKMANAGER MANAGER SHUTDOWN COMPLETE")
    
    xǁNetworkManagerǁshutdown__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁshutdown__mutmut_1': xǁNetworkManagerǁshutdown__mutmut_1, 
        'xǁNetworkManagerǁshutdown__mutmut_2': xǁNetworkManagerǁshutdown__mutmut_2, 
        'xǁNetworkManagerǁshutdown__mutmut_3': xǁNetworkManagerǁshutdown__mutmut_3, 
        'xǁNetworkManagerǁshutdown__mutmut_4': xǁNetworkManagerǁshutdown__mutmut_4, 
        'xǁNetworkManagerǁshutdown__mutmut_5': xǁNetworkManagerǁshutdown__mutmut_5, 
        'xǁNetworkManagerǁshutdown__mutmut_6': xǁNetworkManagerǁshutdown__mutmut_6, 
        'xǁNetworkManagerǁshutdown__mutmut_7': xǁNetworkManagerǁshutdown__mutmut_7, 
        'xǁNetworkManagerǁshutdown__mutmut_8': xǁNetworkManagerǁshutdown__mutmut_8, 
        'xǁNetworkManagerǁshutdown__mutmut_9': xǁNetworkManagerǁshutdown__mutmut_9, 
        'xǁNetworkManagerǁshutdown__mutmut_10': xǁNetworkManagerǁshutdown__mutmut_10, 
        'xǁNetworkManagerǁshutdown__mutmut_11': xǁNetworkManagerǁshutdown__mutmut_11, 
        'xǁNetworkManagerǁshutdown__mutmut_12': xǁNetworkManagerǁshutdown__mutmut_12, 
        'xǁNetworkManagerǁshutdown__mutmut_13': xǁNetworkManagerǁshutdown__mutmut_13, 
        'xǁNetworkManagerǁshutdown__mutmut_14': xǁNetworkManagerǁshutdown__mutmut_14, 
        'xǁNetworkManagerǁshutdown__mutmut_15': xǁNetworkManagerǁshutdown__mutmut_15, 
        'xǁNetworkManagerǁshutdown__mutmut_16': xǁNetworkManagerǁshutdown__mutmut_16, 
        'xǁNetworkManagerǁshutdown__mutmut_17': xǁNetworkManagerǁshutdown__mutmut_17, 
        'xǁNetworkManagerǁshutdown__mutmut_18': xǁNetworkManagerǁshutdown__mutmut_18, 
        'xǁNetworkManagerǁshutdown__mutmut_19': xǁNetworkManagerǁshutdown__mutmut_19, 
        'xǁNetworkManagerǁshutdown__mutmut_20': xǁNetworkManagerǁshutdown__mutmut_20, 
        'xǁNetworkManagerǁshutdown__mutmut_21': xǁNetworkManagerǁshutdown__mutmut_21, 
        'xǁNetworkManagerǁshutdown__mutmut_22': xǁNetworkManagerǁshutdown__mutmut_22, 
        'xǁNetworkManagerǁshutdown__mutmut_23': xǁNetworkManagerǁshutdown__mutmut_23, 
        'xǁNetworkManagerǁshutdown__mutmut_24': xǁNetworkManagerǁshutdown__mutmut_24, 
        'xǁNetworkManagerǁshutdown__mutmut_25': xǁNetworkManagerǁshutdown__mutmut_25, 
        'xǁNetworkManagerǁshutdown__mutmut_26': xǁNetworkManagerǁshutdown__mutmut_26, 
        'xǁNetworkManagerǁshutdown__mutmut_27': xǁNetworkManagerǁshutdown__mutmut_27
    }
    xǁNetworkManagerǁshutdown__mutmut_orig.__name__ = 'xǁNetworkManagerǁshutdown'

    def close(self) -> None:
        """Alias for ``shutdown``"""
        self.shutdown()

    @pyqtSlot(NetworkState)
    def _on_state_changed(self, state: NetworkState) -> None:
        """Cache the new state and re-emit to UI consumers."""
        if self._shutting_down:
            return
        self._cached_state = state
        self.state_changed.emit(state)

    @pyqtSlot(list)
    def _on_networks_scanned(self, networks: list) -> None:
        """Cache scan results, rebuild SSID lookup map, and re-emit."""
        if self._shutting_down:
            return
        self._cached_networks = networks
        self._network_info_map = {n.ssid: n for n in networks}
        self.networks_scanned.emit(networks)

    @pyqtSlot(list)
    def _on_saved_networks_loaded(self, networks: list) -> None:
        """Cache saved profiles, rebuild lowercase lookup map, and re-emit."""
        if self._shutting_down:
            return
        self._cached_saved = networks
        self._saved_network_map = {n.ssid.lower(): n for n in networks}
        self.saved_networks_loaded.emit(networks)

    @pyqtSlot(str, str, str)
    def _on_hotspot_info_ready(self, ssid: str, password: str, security: str) -> None:
        """Update the main-thread hotspot cache and notify UI via ``hotspot_config_updated``."""
        self._cached_hotspot_ssid = ssid
        self._cached_hotspot_password = password
        self._cached_hotspot_security = security
        self.hotspot_config_updated.emit(ssid, password, security)

    @pyqtSlot()
    def _on_keepalive_tick(self) -> None:
        """Safety-net refresh — runs every 5 min to catch any missed signals."""
        if self._shutting_down:
            return
        self._schedule(self._worker._async_get_current_state())
        self._schedule(self._worker._async_check_connectivity())
        self._schedule(self._worker._async_load_saved_networks())

    def request_state_soon(self, delay_ms: int = 500) -> None:
        args = [delay_ms]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁrequest_state_soon__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁrequest_state_soon__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁrequest_state_soon__mutmut_orig(self, delay_ms: int = 500) -> None:
        """Request a state refresh after a short delay."""
        QTimer.singleShot(
            delay_ms,
            lambda: self._schedule(self._worker._async_get_current_state()),
        )

    def xǁNetworkManagerǁrequest_state_soon__mutmut_1(self, delay_ms: int = 501) -> None:
        """Request a state refresh after a short delay."""
        QTimer.singleShot(
            delay_ms,
            lambda: self._schedule(self._worker._async_get_current_state()),
        )

    def xǁNetworkManagerǁrequest_state_soon__mutmut_2(self, delay_ms: int = 500) -> None:
        """Request a state refresh after a short delay."""
        QTimer.singleShot(
            None,
            lambda: self._schedule(self._worker._async_get_current_state()),
        )

    def xǁNetworkManagerǁrequest_state_soon__mutmut_3(self, delay_ms: int = 500) -> None:
        """Request a state refresh after a short delay."""
        QTimer.singleShot(
            delay_ms,
            None,
        )

    def xǁNetworkManagerǁrequest_state_soon__mutmut_4(self, delay_ms: int = 500) -> None:
        """Request a state refresh after a short delay."""
        QTimer.singleShot(
            lambda: self._schedule(self._worker._async_get_current_state()),
        )

    def xǁNetworkManagerǁrequest_state_soon__mutmut_5(self, delay_ms: int = 500) -> None:
        """Request a state refresh after a short delay."""
        QTimer.singleShot(
            delay_ms,
            )

    def xǁNetworkManagerǁrequest_state_soon__mutmut_6(self, delay_ms: int = 500) -> None:
        """Request a state refresh after a short delay."""
        QTimer.singleShot(
            delay_ms,
            lambda: None,
        )

    def xǁNetworkManagerǁrequest_state_soon__mutmut_7(self, delay_ms: int = 500) -> None:
        """Request a state refresh after a short delay."""
        QTimer.singleShot(
            delay_ms,
            lambda: self._schedule(None),
        )
    
    xǁNetworkManagerǁrequest_state_soon__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁrequest_state_soon__mutmut_1': xǁNetworkManagerǁrequest_state_soon__mutmut_1, 
        'xǁNetworkManagerǁrequest_state_soon__mutmut_2': xǁNetworkManagerǁrequest_state_soon__mutmut_2, 
        'xǁNetworkManagerǁrequest_state_soon__mutmut_3': xǁNetworkManagerǁrequest_state_soon__mutmut_3, 
        'xǁNetworkManagerǁrequest_state_soon__mutmut_4': xǁNetworkManagerǁrequest_state_soon__mutmut_4, 
        'xǁNetworkManagerǁrequest_state_soon__mutmut_5': xǁNetworkManagerǁrequest_state_soon__mutmut_5, 
        'xǁNetworkManagerǁrequest_state_soon__mutmut_6': xǁNetworkManagerǁrequest_state_soon__mutmut_6, 
        'xǁNetworkManagerǁrequest_state_soon__mutmut_7': xǁNetworkManagerǁrequest_state_soon__mutmut_7
    }
    xǁNetworkManagerǁrequest_state_soon__mutmut_orig.__name__ = 'xǁNetworkManagerǁrequest_state_soon'

    def get_current_state(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁget_current_state__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁget_current_state__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁget_current_state__mutmut_orig(self) -> None:
        """Request an immediate state refresh from the worker."""
        self._schedule(self._worker._async_get_current_state())

    def xǁNetworkManagerǁget_current_state__mutmut_1(self) -> None:
        """Request an immediate state refresh from the worker."""
        self._schedule(None)
    
    xǁNetworkManagerǁget_current_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁget_current_state__mutmut_1': xǁNetworkManagerǁget_current_state__mutmut_1
    }
    xǁNetworkManagerǁget_current_state__mutmut_orig.__name__ = 'xǁNetworkManagerǁget_current_state'

    def refresh_state(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁrefresh_state__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁrefresh_state__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁrefresh_state__mutmut_orig(self) -> None:
        """Request a state refresh and a saved-network reload from the worker."""
        self._schedule(self._worker._async_get_current_state())
        self._schedule(self._worker._async_load_saved_networks())

    def xǁNetworkManagerǁrefresh_state__mutmut_1(self) -> None:
        """Request a state refresh and a saved-network reload from the worker."""
        self._schedule(None)
        self._schedule(self._worker._async_load_saved_networks())

    def xǁNetworkManagerǁrefresh_state__mutmut_2(self) -> None:
        """Request a state refresh and a saved-network reload from the worker."""
        self._schedule(self._worker._async_get_current_state())
        self._schedule(None)
    
    xǁNetworkManagerǁrefresh_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁrefresh_state__mutmut_1': xǁNetworkManagerǁrefresh_state__mutmut_1, 
        'xǁNetworkManagerǁrefresh_state__mutmut_2': xǁNetworkManagerǁrefresh_state__mutmut_2
    }
    xǁNetworkManagerǁrefresh_state__mutmut_orig.__name__ = 'xǁNetworkManagerǁrefresh_state'

    def scan_networks(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁscan_networks__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁscan_networks__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁscan_networks__mutmut_orig(self) -> None:
        """Request an immediate Wi-Fi scan from the worker."""
        self._schedule(self._worker._async_scan_networks())

    def xǁNetworkManagerǁscan_networks__mutmut_1(self) -> None:
        """Request an immediate Wi-Fi scan from the worker."""
        self._schedule(None)
    
    xǁNetworkManagerǁscan_networks__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁscan_networks__mutmut_1': xǁNetworkManagerǁscan_networks__mutmut_1
    }
    xǁNetworkManagerǁscan_networks__mutmut_orig.__name__ = 'xǁNetworkManagerǁscan_networks'

    def load_saved_networks(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁload_saved_networks__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁload_saved_networks__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁload_saved_networks__mutmut_orig(self) -> None:
        """Request a reload of saved connection profiles from the worker."""
        self._schedule(self._worker._async_load_saved_networks())

    def xǁNetworkManagerǁload_saved_networks__mutmut_1(self) -> None:
        """Request a reload of saved connection profiles from the worker."""
        self._schedule(None)
    
    xǁNetworkManagerǁload_saved_networks__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁload_saved_networks__mutmut_1': xǁNetworkManagerǁload_saved_networks__mutmut_1
    }
    xǁNetworkManagerǁload_saved_networks__mutmut_orig.__name__ = 'xǁNetworkManagerǁload_saved_networks'

    def check_connectivity(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁcheck_connectivity__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁcheck_connectivity__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁcheck_connectivity__mutmut_orig(self) -> None:
        """Request an NM connectivity check from the worker."""
        self._schedule(self._worker._async_check_connectivity())

    def xǁNetworkManagerǁcheck_connectivity__mutmut_1(self) -> None:
        """Request an NM connectivity check from the worker."""
        self._schedule(None)
    
    xǁNetworkManagerǁcheck_connectivity__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁcheck_connectivity__mutmut_1': xǁNetworkManagerǁcheck_connectivity__mutmut_1
    }
    xǁNetworkManagerǁcheck_connectivity__mutmut_orig.__name__ = 'xǁNetworkManagerǁcheck_connectivity'

    def add_network(
        self,
        ssid: str,
        password: str = "",  # nosec B107
        priority: int = ConnectionPriority.MEDIUM.value,
    ) -> None:
        args = [ssid, password, priority]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁadd_network__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁadd_network__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁadd_network__mutmut_orig(
        self,
        ssid: str,
        password: str = "",  # nosec B107
        priority: int = ConnectionPriority.MEDIUM.value,
    ) -> None:
        """Add a new Wi-Fi profile (and connect immediately) with optional priority."""
        self._schedule(self._worker._async_add_network(ssid, password, priority))

    def xǁNetworkManagerǁadd_network__mutmut_1(
        self,
        ssid: str,
        password: str = "XXXX",  # nosec B107
        priority: int = ConnectionPriority.MEDIUM.value,
    ) -> None:
        """Add a new Wi-Fi profile (and connect immediately) with optional priority."""
        self._schedule(self._worker._async_add_network(ssid, password, priority))

    def xǁNetworkManagerǁadd_network__mutmut_2(
        self,
        ssid: str,
        password: str = "",  # nosec B107
        priority: int = ConnectionPriority.MEDIUM.value,
    ) -> None:
        """Add a new Wi-Fi profile (and connect immediately) with optional priority."""
        self._schedule(None)

    def xǁNetworkManagerǁadd_network__mutmut_3(
        self,
        ssid: str,
        password: str = "",  # nosec B107
        priority: int = ConnectionPriority.MEDIUM.value,
    ) -> None:
        """Add a new Wi-Fi profile (and connect immediately) with optional priority."""
        self._schedule(self._worker._async_add_network(None, password, priority))

    def xǁNetworkManagerǁadd_network__mutmut_4(
        self,
        ssid: str,
        password: str = "",  # nosec B107
        priority: int = ConnectionPriority.MEDIUM.value,
    ) -> None:
        """Add a new Wi-Fi profile (and connect immediately) with optional priority."""
        self._schedule(self._worker._async_add_network(ssid, None, priority))

    def xǁNetworkManagerǁadd_network__mutmut_5(
        self,
        ssid: str,
        password: str = "",  # nosec B107
        priority: int = ConnectionPriority.MEDIUM.value,
    ) -> None:
        """Add a new Wi-Fi profile (and connect immediately) with optional priority."""
        self._schedule(self._worker._async_add_network(ssid, password, None))

    def xǁNetworkManagerǁadd_network__mutmut_6(
        self,
        ssid: str,
        password: str = "",  # nosec B107
        priority: int = ConnectionPriority.MEDIUM.value,
    ) -> None:
        """Add a new Wi-Fi profile (and connect immediately) with optional priority."""
        self._schedule(self._worker._async_add_network(password, priority))

    def xǁNetworkManagerǁadd_network__mutmut_7(
        self,
        ssid: str,
        password: str = "",  # nosec B107
        priority: int = ConnectionPriority.MEDIUM.value,
    ) -> None:
        """Add a new Wi-Fi profile (and connect immediately) with optional priority."""
        self._schedule(self._worker._async_add_network(ssid, priority))

    def xǁNetworkManagerǁadd_network__mutmut_8(
        self,
        ssid: str,
        password: str = "",  # nosec B107
        priority: int = ConnectionPriority.MEDIUM.value,
    ) -> None:
        """Add a new Wi-Fi profile (and connect immediately) with optional priority."""
        self._schedule(self._worker._async_add_network(ssid, password, ))
    
    xǁNetworkManagerǁadd_network__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁadd_network__mutmut_1': xǁNetworkManagerǁadd_network__mutmut_1, 
        'xǁNetworkManagerǁadd_network__mutmut_2': xǁNetworkManagerǁadd_network__mutmut_2, 
        'xǁNetworkManagerǁadd_network__mutmut_3': xǁNetworkManagerǁadd_network__mutmut_3, 
        'xǁNetworkManagerǁadd_network__mutmut_4': xǁNetworkManagerǁadd_network__mutmut_4, 
        'xǁNetworkManagerǁadd_network__mutmut_5': xǁNetworkManagerǁadd_network__mutmut_5, 
        'xǁNetworkManagerǁadd_network__mutmut_6': xǁNetworkManagerǁadd_network__mutmut_6, 
        'xǁNetworkManagerǁadd_network__mutmut_7': xǁNetworkManagerǁadd_network__mutmut_7, 
        'xǁNetworkManagerǁadd_network__mutmut_8': xǁNetworkManagerǁadd_network__mutmut_8
    }
    xǁNetworkManagerǁadd_network__mutmut_orig.__name__ = 'xǁNetworkManagerǁadd_network'

    def connect_network(self, ssid: str) -> None:
        args = [ssid]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁconnect_network__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁconnect_network__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁconnect_network__mutmut_orig(self, ssid: str) -> None:
        """Connect to an already-saved network by *ssid*."""
        self._schedule(self._worker._async_connect_network(ssid))

    def xǁNetworkManagerǁconnect_network__mutmut_1(self, ssid: str) -> None:
        """Connect to an already-saved network by *ssid*."""
        self._schedule(None)

    def xǁNetworkManagerǁconnect_network__mutmut_2(self, ssid: str) -> None:
        """Connect to an already-saved network by *ssid*."""
        self._schedule(self._worker._async_connect_network(None))
    
    xǁNetworkManagerǁconnect_network__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁconnect_network__mutmut_1': xǁNetworkManagerǁconnect_network__mutmut_1, 
        'xǁNetworkManagerǁconnect_network__mutmut_2': xǁNetworkManagerǁconnect_network__mutmut_2
    }
    xǁNetworkManagerǁconnect_network__mutmut_orig.__name__ = 'xǁNetworkManagerǁconnect_network'

    def disconnect(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁdisconnect__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁdisconnect__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁdisconnect__mutmut_orig(self) -> None:
        """Disconnect the currently active Wi-Fi connection."""
        self._schedule(self._worker._async_disconnect())

    def xǁNetworkManagerǁdisconnect__mutmut_1(self) -> None:
        """Disconnect the currently active Wi-Fi connection."""
        self._schedule(None)
    
    xǁNetworkManagerǁdisconnect__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁdisconnect__mutmut_1': xǁNetworkManagerǁdisconnect__mutmut_1
    }
    xǁNetworkManagerǁdisconnect__mutmut_orig.__name__ = 'xǁNetworkManagerǁdisconnect'

    def delete_network(self, ssid: str) -> None:
        args = [ssid]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁdelete_network__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁdelete_network__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁdelete_network__mutmut_orig(self, ssid: str) -> None:
        """Delete the saved profile for *ssid*."""
        self._schedule(self._worker._async_delete_network(ssid))

    def xǁNetworkManagerǁdelete_network__mutmut_1(self, ssid: str) -> None:
        """Delete the saved profile for *ssid*."""
        self._schedule(None)

    def xǁNetworkManagerǁdelete_network__mutmut_2(self, ssid: str) -> None:
        """Delete the saved profile for *ssid*."""
        self._schedule(self._worker._async_delete_network(None))
    
    xǁNetworkManagerǁdelete_network__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁdelete_network__mutmut_1': xǁNetworkManagerǁdelete_network__mutmut_1, 
        'xǁNetworkManagerǁdelete_network__mutmut_2': xǁNetworkManagerǁdelete_network__mutmut_2
    }
    xǁNetworkManagerǁdelete_network__mutmut_orig.__name__ = 'xǁNetworkManagerǁdelete_network'

    def update_network(  # nosec B107
        self, ssid: str, password: str = "", priority: int = 0
    ) -> None:
        args = [ssid, password, priority]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁupdate_network__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁupdate_network__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁupdate_network__mutmut_orig(  # nosec B107
        self, ssid: str, password: str = "", priority: int = 0
    ) -> None:
        """Update the password and/or autoconnect priority for a saved profile."""
        self._schedule(self._worker._async_update_network(ssid, password, priority))

    def xǁNetworkManagerǁupdate_network__mutmut_1(  # nosec B107
        self, ssid: str, password: str = "XXXX", priority: int = 0
    ) -> None:
        """Update the password and/or autoconnect priority for a saved profile."""
        self._schedule(self._worker._async_update_network(ssid, password, priority))

    def xǁNetworkManagerǁupdate_network__mutmut_2(  # nosec B107
        self, ssid: str, password: str = "", priority: int = 1
    ) -> None:
        """Update the password and/or autoconnect priority for a saved profile."""
        self._schedule(self._worker._async_update_network(ssid, password, priority))

    def xǁNetworkManagerǁupdate_network__mutmut_3(  # nosec B107
        self, ssid: str, password: str = "", priority: int = 0
    ) -> None:
        """Update the password and/or autoconnect priority for a saved profile."""
        self._schedule(None)

    def xǁNetworkManagerǁupdate_network__mutmut_4(  # nosec B107
        self, ssid: str, password: str = "", priority: int = 0
    ) -> None:
        """Update the password and/or autoconnect priority for a saved profile."""
        self._schedule(self._worker._async_update_network(None, password, priority))

    def xǁNetworkManagerǁupdate_network__mutmut_5(  # nosec B107
        self, ssid: str, password: str = "", priority: int = 0
    ) -> None:
        """Update the password and/or autoconnect priority for a saved profile."""
        self._schedule(self._worker._async_update_network(ssid, None, priority))

    def xǁNetworkManagerǁupdate_network__mutmut_6(  # nosec B107
        self, ssid: str, password: str = "", priority: int = 0
    ) -> None:
        """Update the password and/or autoconnect priority for a saved profile."""
        self._schedule(self._worker._async_update_network(ssid, password, None))

    def xǁNetworkManagerǁupdate_network__mutmut_7(  # nosec B107
        self, ssid: str, password: str = "", priority: int = 0
    ) -> None:
        """Update the password and/or autoconnect priority for a saved profile."""
        self._schedule(self._worker._async_update_network(password, priority))

    def xǁNetworkManagerǁupdate_network__mutmut_8(  # nosec B107
        self, ssid: str, password: str = "", priority: int = 0
    ) -> None:
        """Update the password and/or autoconnect priority for a saved profile."""
        self._schedule(self._worker._async_update_network(ssid, priority))

    def xǁNetworkManagerǁupdate_network__mutmut_9(  # nosec B107
        self, ssid: str, password: str = "", priority: int = 0
    ) -> None:
        """Update the password and/or autoconnect priority for a saved profile."""
        self._schedule(self._worker._async_update_network(ssid, password, ))
    
    xǁNetworkManagerǁupdate_network__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁupdate_network__mutmut_1': xǁNetworkManagerǁupdate_network__mutmut_1, 
        'xǁNetworkManagerǁupdate_network__mutmut_2': xǁNetworkManagerǁupdate_network__mutmut_2, 
        'xǁNetworkManagerǁupdate_network__mutmut_3': xǁNetworkManagerǁupdate_network__mutmut_3, 
        'xǁNetworkManagerǁupdate_network__mutmut_4': xǁNetworkManagerǁupdate_network__mutmut_4, 
        'xǁNetworkManagerǁupdate_network__mutmut_5': xǁNetworkManagerǁupdate_network__mutmut_5, 
        'xǁNetworkManagerǁupdate_network__mutmut_6': xǁNetworkManagerǁupdate_network__mutmut_6, 
        'xǁNetworkManagerǁupdate_network__mutmut_7': xǁNetworkManagerǁupdate_network__mutmut_7, 
        'xǁNetworkManagerǁupdate_network__mutmut_8': xǁNetworkManagerǁupdate_network__mutmut_8, 
        'xǁNetworkManagerǁupdate_network__mutmut_9': xǁNetworkManagerǁupdate_network__mutmut_9
    }
    xǁNetworkManagerǁupdate_network__mutmut_orig.__name__ = 'xǁNetworkManagerǁupdate_network'

    def set_wifi_enabled(self, enabled: bool) -> None:
        args = [enabled]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁset_wifi_enabled__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁset_wifi_enabled__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁset_wifi_enabled__mutmut_orig(self, enabled: bool) -> None:
        """Enable or disable the Wi-Fi radio."""
        self._schedule(self._worker._async_set_wifi_enabled(enabled))

    def xǁNetworkManagerǁset_wifi_enabled__mutmut_1(self, enabled: bool) -> None:
        """Enable or disable the Wi-Fi radio."""
        self._schedule(None)

    def xǁNetworkManagerǁset_wifi_enabled__mutmut_2(self, enabled: bool) -> None:
        """Enable or disable the Wi-Fi radio."""
        self._schedule(self._worker._async_set_wifi_enabled(None))
    
    xǁNetworkManagerǁset_wifi_enabled__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁset_wifi_enabled__mutmut_1': xǁNetworkManagerǁset_wifi_enabled__mutmut_1, 
        'xǁNetworkManagerǁset_wifi_enabled__mutmut_2': xǁNetworkManagerǁset_wifi_enabled__mutmut_2
    }
    xǁNetworkManagerǁset_wifi_enabled__mutmut_orig.__name__ = 'xǁNetworkManagerǁset_wifi_enabled'

    def create_hotspot(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        args = [ssid, password, security]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁcreate_hotspot__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁcreate_hotspot__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁcreate_hotspot__mutmut_orig(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(ssid, password, security)
        )

    def xǁNetworkManagerǁcreate_hotspot__mutmut_1(
        self,
        ssid: str = "XXXX",
        password: str = "",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(ssid, password, security)
        )

    def xǁNetworkManagerǁcreate_hotspot__mutmut_2(
        self,
        ssid: str = "",
        password: str = "XXXX",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(ssid, password, security)
        )

    def xǁNetworkManagerǁcreate_hotspot__mutmut_3(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "XXwpa-pskXX",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(ssid, password, security)
        )

    def xǁNetworkManagerǁcreate_hotspot__mutmut_4(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "WPA-PSK",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(ssid, password, security)
        )

    def xǁNetworkManagerǁcreate_hotspot__mutmut_5(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            None
        )

    def xǁNetworkManagerǁcreate_hotspot__mutmut_6(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(None, password, security)
        )

    def xǁNetworkManagerǁcreate_hotspot__mutmut_7(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(ssid, None, security)
        )

    def xǁNetworkManagerǁcreate_hotspot__mutmut_8(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(ssid, password, None)
        )

    def xǁNetworkManagerǁcreate_hotspot__mutmut_9(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(password, security)
        )

    def xǁNetworkManagerǁcreate_hotspot__mutmut_10(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(ssid, security)
        )

    def xǁNetworkManagerǁcreate_hotspot__mutmut_11(
        self,
        ssid: str = "",
        password: str = "",
        security: str = "wpa-psk",  # nosec B107
    ) -> None:
        """Create and immediately activate a hotspot with the given credentials."""
        self._schedule(
            self._worker._async_create_and_activate_hotspot(ssid, password, )
        )
    
    xǁNetworkManagerǁcreate_hotspot__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁcreate_hotspot__mutmut_1': xǁNetworkManagerǁcreate_hotspot__mutmut_1, 
        'xǁNetworkManagerǁcreate_hotspot__mutmut_2': xǁNetworkManagerǁcreate_hotspot__mutmut_2, 
        'xǁNetworkManagerǁcreate_hotspot__mutmut_3': xǁNetworkManagerǁcreate_hotspot__mutmut_3, 
        'xǁNetworkManagerǁcreate_hotspot__mutmut_4': xǁNetworkManagerǁcreate_hotspot__mutmut_4, 
        'xǁNetworkManagerǁcreate_hotspot__mutmut_5': xǁNetworkManagerǁcreate_hotspot__mutmut_5, 
        'xǁNetworkManagerǁcreate_hotspot__mutmut_6': xǁNetworkManagerǁcreate_hotspot__mutmut_6, 
        'xǁNetworkManagerǁcreate_hotspot__mutmut_7': xǁNetworkManagerǁcreate_hotspot__mutmut_7, 
        'xǁNetworkManagerǁcreate_hotspot__mutmut_8': xǁNetworkManagerǁcreate_hotspot__mutmut_8, 
        'xǁNetworkManagerǁcreate_hotspot__mutmut_9': xǁNetworkManagerǁcreate_hotspot__mutmut_9, 
        'xǁNetworkManagerǁcreate_hotspot__mutmut_10': xǁNetworkManagerǁcreate_hotspot__mutmut_10, 
        'xǁNetworkManagerǁcreate_hotspot__mutmut_11': xǁNetworkManagerǁcreate_hotspot__mutmut_11
    }
    xǁNetworkManagerǁcreate_hotspot__mutmut_orig.__name__ = 'xǁNetworkManagerǁcreate_hotspot'

    def toggle_hotspot(self, enable: bool) -> None:
        args = [enable]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁtoggle_hotspot__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁtoggle_hotspot__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁtoggle_hotspot__mutmut_orig(self, enable: bool) -> None:
        """Deactivate the hotspot (enable=False) or create+activate (enable=True)."""
        self._schedule(self._worker._async_toggle_hotspot(enable))

    def xǁNetworkManagerǁtoggle_hotspot__mutmut_1(self, enable: bool) -> None:
        """Deactivate the hotspot (enable=False) or create+activate (enable=True)."""
        self._schedule(None)

    def xǁNetworkManagerǁtoggle_hotspot__mutmut_2(self, enable: bool) -> None:
        """Deactivate the hotspot (enable=False) or create+activate (enable=True)."""
        self._schedule(self._worker._async_toggle_hotspot(None))
    
    xǁNetworkManagerǁtoggle_hotspot__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁtoggle_hotspot__mutmut_1': xǁNetworkManagerǁtoggle_hotspot__mutmut_1, 
        'xǁNetworkManagerǁtoggle_hotspot__mutmut_2': xǁNetworkManagerǁtoggle_hotspot__mutmut_2
    }
    xǁNetworkManagerǁtoggle_hotspot__mutmut_orig.__name__ = 'xǁNetworkManagerǁtoggle_hotspot'

    def update_hotspot_config(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        args = [old_ssid, new_ssid, new_password, security]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁupdate_hotspot_config__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁupdate_hotspot_config__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_orig(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                old_ssid, new_ssid, new_password, security
            )
        )

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_1(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "XXwpa-pskXX",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                old_ssid, new_ssid, new_password, security
            )
        )

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_2(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "WPA-PSK",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                old_ssid, new_ssid, new_password, security
            )
        )

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_3(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            None
        )

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_4(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                None, new_ssid, new_password, security
            )
        )

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_5(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                old_ssid, None, new_password, security
            )
        )

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_6(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                old_ssid, new_ssid, None, security
            )
        )

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_7(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                old_ssid, new_ssid, new_password, None
            )
        )

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_8(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                new_ssid, new_password, security
            )
        )

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_9(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                old_ssid, new_password, security
            )
        )

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_10(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                old_ssid, new_ssid, security
            )
        )

    def xǁNetworkManagerǁupdate_hotspot_config__mutmut_11(
        self,
        old_ssid: str,
        new_ssid: str,
        new_password: str,
        security: str = "wpa-psk",
    ) -> None:
        """Change hotspot name/password/security — cleans up old profiles."""
        self._schedule(
            self._worker._async_update_hotspot_config(
                old_ssid, new_ssid, new_password, )
        )
    
    xǁNetworkManagerǁupdate_hotspot_config__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁupdate_hotspot_config__mutmut_1': xǁNetworkManagerǁupdate_hotspot_config__mutmut_1, 
        'xǁNetworkManagerǁupdate_hotspot_config__mutmut_2': xǁNetworkManagerǁupdate_hotspot_config__mutmut_2, 
        'xǁNetworkManagerǁupdate_hotspot_config__mutmut_3': xǁNetworkManagerǁupdate_hotspot_config__mutmut_3, 
        'xǁNetworkManagerǁupdate_hotspot_config__mutmut_4': xǁNetworkManagerǁupdate_hotspot_config__mutmut_4, 
        'xǁNetworkManagerǁupdate_hotspot_config__mutmut_5': xǁNetworkManagerǁupdate_hotspot_config__mutmut_5, 
        'xǁNetworkManagerǁupdate_hotspot_config__mutmut_6': xǁNetworkManagerǁupdate_hotspot_config__mutmut_6, 
        'xǁNetworkManagerǁupdate_hotspot_config__mutmut_7': xǁNetworkManagerǁupdate_hotspot_config__mutmut_7, 
        'xǁNetworkManagerǁupdate_hotspot_config__mutmut_8': xǁNetworkManagerǁupdate_hotspot_config__mutmut_8, 
        'xǁNetworkManagerǁupdate_hotspot_config__mutmut_9': xǁNetworkManagerǁupdate_hotspot_config__mutmut_9, 
        'xǁNetworkManagerǁupdate_hotspot_config__mutmut_10': xǁNetworkManagerǁupdate_hotspot_config__mutmut_10, 
        'xǁNetworkManagerǁupdate_hotspot_config__mutmut_11': xǁNetworkManagerǁupdate_hotspot_config__mutmut_11
    }
    xǁNetworkManagerǁupdate_hotspot_config__mutmut_orig.__name__ = 'xǁNetworkManagerǁupdate_hotspot_config'

    def disconnect_ethernet(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁdisconnect_ethernet__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁdisconnect_ethernet__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁdisconnect_ethernet__mutmut_orig(self) -> None:
        """Deactivate the primary wired interface."""
        self._schedule(self._worker._async_disconnect_ethernet())

    def xǁNetworkManagerǁdisconnect_ethernet__mutmut_1(self) -> None:
        """Deactivate the primary wired interface."""
        self._schedule(None)
    
    xǁNetworkManagerǁdisconnect_ethernet__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁdisconnect_ethernet__mutmut_1': xǁNetworkManagerǁdisconnect_ethernet__mutmut_1
    }
    xǁNetworkManagerǁdisconnect_ethernet__mutmut_orig.__name__ = 'xǁNetworkManagerǁdisconnect_ethernet'

    def connect_ethernet(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁconnect_ethernet__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁconnect_ethernet__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁconnect_ethernet__mutmut_orig(self) -> None:
        """Activate the primary wired interface."""
        self._schedule(self._worker._async_connect_ethernet())

    def xǁNetworkManagerǁconnect_ethernet__mutmut_1(self) -> None:
        """Activate the primary wired interface."""
        self._schedule(None)
    
    xǁNetworkManagerǁconnect_ethernet__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁconnect_ethernet__mutmut_1': xǁNetworkManagerǁconnect_ethernet__mutmut_1
    }
    xǁNetworkManagerǁconnect_ethernet__mutmut_orig.__name__ = 'xǁNetworkManagerǁconnect_ethernet'

    def create_vlan_connection(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        args = [vlan_id, ip_address, subnet_mask, gateway, dns1, dns2]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁcreate_vlan_connection__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁcreate_vlan_connection__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_orig(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_1(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "XXXX",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_2(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "XXXX",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_3(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            None
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_4(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                None, ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_5(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, None, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_6(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, None, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_7(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, subnet_mask, None, dns1, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_8(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, subnet_mask, gateway, None, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_9(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, subnet_mask, gateway, dns1, None
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_10(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_11(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_12(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_13(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, subnet_mask, dns1, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_14(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, subnet_mask, gateway, dns2
            )
        )

    def xǁNetworkManagerǁcreate_vlan_connection__mutmut_15(
        self,
        vlan_id: int,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Create and activate a VLAN connection with
        given static IP settings"""
        self._schedule(
            self._worker._async_create_vlan(
                vlan_id, ip_address, subnet_mask, gateway, dns1, )
        )
    
    xǁNetworkManagerǁcreate_vlan_connection__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁcreate_vlan_connection__mutmut_1': xǁNetworkManagerǁcreate_vlan_connection__mutmut_1, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_2': xǁNetworkManagerǁcreate_vlan_connection__mutmut_2, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_3': xǁNetworkManagerǁcreate_vlan_connection__mutmut_3, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_4': xǁNetworkManagerǁcreate_vlan_connection__mutmut_4, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_5': xǁNetworkManagerǁcreate_vlan_connection__mutmut_5, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_6': xǁNetworkManagerǁcreate_vlan_connection__mutmut_6, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_7': xǁNetworkManagerǁcreate_vlan_connection__mutmut_7, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_8': xǁNetworkManagerǁcreate_vlan_connection__mutmut_8, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_9': xǁNetworkManagerǁcreate_vlan_connection__mutmut_9, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_10': xǁNetworkManagerǁcreate_vlan_connection__mutmut_10, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_11': xǁNetworkManagerǁcreate_vlan_connection__mutmut_11, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_12': xǁNetworkManagerǁcreate_vlan_connection__mutmut_12, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_13': xǁNetworkManagerǁcreate_vlan_connection__mutmut_13, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_14': xǁNetworkManagerǁcreate_vlan_connection__mutmut_14, 
        'xǁNetworkManagerǁcreate_vlan_connection__mutmut_15': xǁNetworkManagerǁcreate_vlan_connection__mutmut_15
    }
    xǁNetworkManagerǁcreate_vlan_connection__mutmut_orig.__name__ = 'xǁNetworkManagerǁcreate_vlan_connection'

    def delete_vlan_connection(self, vlan_id: int) -> None:
        args = [vlan_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁdelete_vlan_connection__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁdelete_vlan_connection__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁdelete_vlan_connection__mutmut_orig(self, vlan_id: int) -> None:
        """Delete all NM profiles for *vlan_id*."""
        self._schedule(self._worker._async_delete_vlan(vlan_id))

    def xǁNetworkManagerǁdelete_vlan_connection__mutmut_1(self, vlan_id: int) -> None:
        """Delete all NM profiles for *vlan_id*."""
        self._schedule(None)

    def xǁNetworkManagerǁdelete_vlan_connection__mutmut_2(self, vlan_id: int) -> None:
        """Delete all NM profiles for *vlan_id*."""
        self._schedule(self._worker._async_delete_vlan(None))
    
    xǁNetworkManagerǁdelete_vlan_connection__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁdelete_vlan_connection__mutmut_1': xǁNetworkManagerǁdelete_vlan_connection__mutmut_1, 
        'xǁNetworkManagerǁdelete_vlan_connection__mutmut_2': xǁNetworkManagerǁdelete_vlan_connection__mutmut_2
    }
    xǁNetworkManagerǁdelete_vlan_connection__mutmut_orig.__name__ = 'xǁNetworkManagerǁdelete_vlan_connection'

    def update_wifi_static_ip(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        args = [ssid, ip_address, subnet_mask, gateway, dns1, dns2]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_orig(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_1(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "XXXX",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_2(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "XXXX",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_3(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            None
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_4(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                None, ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_5(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, None, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_6(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, None, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_7(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, subnet_mask, None, dns1, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_8(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, subnet_mask, gateway, None, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_9(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, subnet_mask, gateway, dns1, None
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_10(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ip_address, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_11(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, subnet_mask, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_12(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, gateway, dns1, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_13(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, subnet_mask, dns1, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_14(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, subnet_mask, gateway, dns2
            )
        )

    def xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_15(
        self,
        ssid: str,
        ip_address: str,
        subnet_mask: str,
        gateway: str,
        dns1: str = "",
        dns2: str = "",
    ) -> None:
        """Apply a static IP configuration to a saved Wi-Fi profile."""
        self._schedule(
            self._worker._async_update_wifi_static_ip(
                ssid, ip_address, subnet_mask, gateway, dns1, )
        )
    
    xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_1': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_1, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_2': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_2, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_3': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_3, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_4': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_4, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_5': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_5, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_6': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_6, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_7': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_7, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_8': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_8, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_9': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_9, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_10': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_10, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_11': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_11, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_12': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_12, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_13': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_13, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_14': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_14, 
        'xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_15': xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_15
    }
    xǁNetworkManagerǁupdate_wifi_static_ip__mutmut_orig.__name__ = 'xǁNetworkManagerǁupdate_wifi_static_ip'

    def reset_wifi_to_dhcp(self, ssid: str) -> None:
        args = [ssid]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁreset_wifi_to_dhcp__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁreset_wifi_to_dhcp__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁreset_wifi_to_dhcp__mutmut_orig(self, ssid: str) -> None:
        """Reset a saved Wi-Fi profile back to DHCP."""
        self._schedule(self._worker._async_reset_wifi_to_dhcp(ssid))

    def xǁNetworkManagerǁreset_wifi_to_dhcp__mutmut_1(self, ssid: str) -> None:
        """Reset a saved Wi-Fi profile back to DHCP."""
        self._schedule(None)

    def xǁNetworkManagerǁreset_wifi_to_dhcp__mutmut_2(self, ssid: str) -> None:
        """Reset a saved Wi-Fi profile back to DHCP."""
        self._schedule(self._worker._async_reset_wifi_to_dhcp(None))
    
    xǁNetworkManagerǁreset_wifi_to_dhcp__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁreset_wifi_to_dhcp__mutmut_1': xǁNetworkManagerǁreset_wifi_to_dhcp__mutmut_1, 
        'xǁNetworkManagerǁreset_wifi_to_dhcp__mutmut_2': xǁNetworkManagerǁreset_wifi_to_dhcp__mutmut_2
    }
    xǁNetworkManagerǁreset_wifi_to_dhcp__mutmut_orig.__name__ = 'xǁNetworkManagerǁreset_wifi_to_dhcp'

    @property
    def current_state(self) -> NetworkState:
        """Most recently cached ``NetworkState`` snapshot."""
        return self._cached_state

    @property
    def current_ssid(self) -> str | None:
        """SSID of the currently active Wi-Fi connection, or ``None``."""
        return self._cached_state.current_ssid

    @property
    def saved_networks(self) -> list[SavedNetwork]:
        """Most recently cached list of saved ``SavedNetwork`` profiles."""
        return self._cached_saved

    @property
    def hotspot_ssid(self) -> str:
        """Hotspot SSID — read from main-thread cache (thread-safe)."""
        return self._cached_hotspot_ssid

    @property
    def hotspot_password(self) -> str:
        """Hotspot password — read from main-thread cache (thread-safe)."""
        return self._cached_hotspot_password

    @property
    def hotspot_security(self) -> str:
        """Hotspot security type — always 'wpa-psk' (WPA2-PSK, thread-safe)."""
        return self._cached_hotspot_security

    def get_network_info(self, ssid: str) -> NetworkInfo | None:
        args = [ssid]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁget_network_info__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁget_network_info__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁget_network_info__mutmut_orig(self, ssid: str) -> NetworkInfo | None:
        """Return the scanned ``NetworkInfo`` for *ssid*, or ``None``."""
        return self._network_info_map.get(ssid)

    def xǁNetworkManagerǁget_network_info__mutmut_1(self, ssid: str) -> NetworkInfo | None:
        """Return the scanned ``NetworkInfo`` for *ssid*, or ``None``."""
        return self._network_info_map.get(None)
    
    xǁNetworkManagerǁget_network_info__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁget_network_info__mutmut_1': xǁNetworkManagerǁget_network_info__mutmut_1
    }
    xǁNetworkManagerǁget_network_info__mutmut_orig.__name__ = 'xǁNetworkManagerǁget_network_info'

    def get_saved_network(self, ssid: str) -> SavedNetwork | None:
        args = [ssid]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkManagerǁget_saved_network__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkManagerǁget_saved_network__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkManagerǁget_saved_network__mutmut_orig(self, ssid: str) -> SavedNetwork | None:
        """Return the saved ``SavedNetwork`` for *ssid* (case-insensitive)."""
        return self._saved_network_map.get(ssid.lower())

    def xǁNetworkManagerǁget_saved_network__mutmut_1(self, ssid: str) -> SavedNetwork | None:
        """Return the saved ``SavedNetwork`` for *ssid* (case-insensitive)."""
        return self._saved_network_map.get(None)

    def xǁNetworkManagerǁget_saved_network__mutmut_2(self, ssid: str) -> SavedNetwork | None:
        """Return the saved ``SavedNetwork`` for *ssid* (case-insensitive)."""
        return self._saved_network_map.get(ssid.upper())
    
    xǁNetworkManagerǁget_saved_network__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkManagerǁget_saved_network__mutmut_1': xǁNetworkManagerǁget_saved_network__mutmut_1, 
        'xǁNetworkManagerǁget_saved_network__mutmut_2': xǁNetworkManagerǁget_saved_network__mutmut_2
    }
    xǁNetworkManagerǁget_saved_network__mutmut_orig.__name__ = 'xǁNetworkManagerǁget_saved_network'
