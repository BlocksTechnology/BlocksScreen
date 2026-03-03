import logging
import threading
from functools import partial
from typing import Any, Callable, Dict, List, NamedTuple, Optional

from lib.network import SdbusNetworkManagerAsync
from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard
from lib.panels.widgets.loadWidget import LoadingOverlayWidget
from lib.panels.widgets.popupDialogWidget import Popup
from lib.utils.blocks_button import BlocksCustomButton
from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.blocks_linedit import BlocksCustomLinEdit
from lib.utils.blocks_Scrollbar import CustomScrollBar
from lib.utils.blocks_togglebutton import NetworkWidgetbuttons
from lib.utils.check_button import BlocksCustomCheckButton
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal

logger = logging.getLogger(__name__)


LOAD_TIMEOUT_MS = 30_000
NETWORK_CONNECT_DELAY_MS = 5_000
NETWORK_LIST_REFRESH_MS = 10_000
STATUS_CHECK_INTERVAL_MS = 2_000
DEFAULT_POLL_INTERVAL_MS = 10_000

SIGNAL_EXCELLENT_THRESHOLD = 75
SIGNAL_GOOD_THRESHOLD = 50
SIGNAL_FAIR_THRESHOLD = 25
SIGNAL_MINIMUM_THRESHOLD = 5

PRIORITY_HIGH = 90
PRIORITY_MEDIUM = 50
PRIORITY_LOW = 20

SEPARATOR_SIGNAL_VALUE = -10
PRIVACY_BIT = 1

# SSIDs that indicate hidden networks
HIDDEN_NETWORK_INDICATORS = ("", "UNKNOWN", "<hidden>", None)


class NetworkInfo(NamedTuple):
    """Information about a network."""

    signal: int
    status: str
    is_open: bool = False
    is_saved: bool = False
    is_hidden: bool = False  # Added flag for hidden networks


class NetworkScanResult(NamedTuple):
    """Result of a network scan."""

    ssid: str
    signal: int
    status: str
    is_open: bool = False


class NetworkScanRunnable(QRunnable):
    """Runnable for scanning networks in background thread."""

    class Signals(QObject):
        """Signals for network scan results."""

        scan_results = pyqtSignal(dict, name="scan-results")
        finished_network_list_build = pyqtSignal(
            list, name="finished-network-list-build"
        )
        error = pyqtSignal(str)

    def __init__(self, nm: SdbusNetworkManagerAsync) -> None:
        """Initialize the network scan runnable."""
        super().__init__()
        self._nm = nm
        self.signals = NetworkScanRunnable.Signals()

    def run(self) -> None:
        """Execute the network scan."""
        try:
            self._nm.rescan_networks()
            saved_ssids = self._nm.get_saved_ssid_names()
            available = self._get_available_networks()
            data_dict = self._build_data_dict(available, saved_ssids)
            self.signals.scan_results.emit(data_dict)
            items = self._build_network_list(data_dict)
            self.signals.finished_network_list_build.emit(items)
        except Exception as e:
            logger.error("Error scanning networks", exc_info=True)
            self.signals.error.emit(str(e))

    def _get_available_networks(self) -> Dict[str, Dict]:
        """Get available networks from NetworkManager."""
        if self._nm.check_wifi_interface():
            return self._nm.get_available_networks() or {}
        return {}

    def _build_data_dict(
        self, available: Dict[str, Dict], saved_ssids: List[str]
    ) -> Dict[str, Dict]:
        """Build data dictionary from available networks."""
        data_dict: Dict[str, Dict] = {}
        for ssid, props in available.items():
            signal = int(props.get("signal_level", 0))
            sec_tuple = props.get("security", (0, 0, 0))
            caps_value = sec_tuple[2] if len(sec_tuple) > 2 else 0
            is_open = (caps_value & PRIVACY_BIT) == 0
            # Check if this is a hidden network
            is_hidden = ssid in HIDDEN_NETWORK_INDICATORS or not ssid.strip()
            data_dict[ssid] = {
                "signal_level": signal,
                "is_saved": ssid in saved_ssids,
                "is_open": is_open,
                "is_hidden": is_hidden,
            }
        return data_dict

    def _build_network_list(self, data_dict: Dict[str, Dict]) -> List[tuple]:
        """Build sorted network list for display."""
        current_ssid = self._nm.get_current_ssid()

        saved_nets = [
            (ssid, info["signal_level"], info["is_open"], info.get("is_hidden", False))
            for ssid, info in data_dict.items()
            if info["is_saved"]
        ]
        unsaved_nets = [
            (ssid, info["signal_level"], info["is_open"], info.get("is_hidden", False))
            for ssid, info in data_dict.items()
            if not info["is_saved"]
        ]

        saved_nets.sort(key=lambda x: -x[1])
        unsaved_nets.sort(key=lambda x: -x[1])

        items: List[tuple] = []

        for ssid, signal, is_open, is_hidden in saved_nets:
            status = "Active" if ssid == current_ssid else "Saved"
            items.append((ssid, signal, status, is_open, True, is_hidden))

        for ssid, signal, is_open, is_hidden in unsaved_nets:
            status = "Open" if is_open else "Protected"
            items.append((ssid, signal, status, is_open, False, is_hidden))

        return items


class BuildNetworkList(QtCore.QObject):
    """Worker class for building network lists with polling support."""

    scan_results = pyqtSignal(dict, name="scan-results")
    finished_network_list_build = pyqtSignal(list, name="finished-network-list-build")
    error = pyqtSignal(str)

    def __init__(
        self,
        nm: SdbusNetworkManagerAsync,
        poll_interval_ms: int = DEFAULT_POLL_INTERVAL_MS,
    ) -> None:
        """Initialize the network list builder."""
        super().__init__()
        self._nm = nm
        self._threadpool = QThreadPool.globalInstance()
        self._poll_interval_ms = poll_interval_ms
        self._is_scanning = False
        self._scan_lock = threading.Lock()
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._do_scan)

    def start_polling(self) -> None:
        """Start periodic network scanning."""
        self._schedule_next_scan()

    def stop_polling(self) -> None:
        """Stop periodic network scanning."""
        self._timer.stop()

    def build(self) -> None:
        """Trigger immediate network scan."""
        self._do_scan()

    def _schedule_next_scan(self) -> None:
        """Schedule the next network scan."""
        self._timer.start(self._poll_interval_ms)

    def _on_task_finished(self, items: List) -> None:
        """Handle scan completion."""
        with self._scan_lock:
            self._is_scanning = False
        self.finished_network_list_build.emit(items)
        self._schedule_next_scan()

    def _on_task_scan_results(self, data_dict: Dict) -> None:
        """Handle scan results."""
        self.scan_results.emit(data_dict)

    def _on_task_error(self, err: str) -> None:
        """Handle scan error."""
        with self._scan_lock:
            self._is_scanning = False
        self.error.emit(err)
        self._schedule_next_scan()

    def _do_scan(self) -> None:
        """Execute network scan in background thread."""
        with self._scan_lock:
            if self._is_scanning:
                return
            self._is_scanning = True

        task = NetworkScanRunnable(self._nm)
        task.signals.finished_network_list_build.connect(self._on_task_finished)
        task.signals.scan_results.connect(self._on_task_scan_results)
        task.signals.error.connect(self._on_task_error)
        self._threadpool.start(task)


class WifiIconProvider:
    """Provider for Wi-Fi signal strength icons."""

    def __init__(self) -> None:
        """Initialize icon paths."""
        self._paths = {
            (0, False): ":/network/media/btn_icons/0bar_wifi.svg",
            (1, False): ":/network/media/btn_icons/1bar_wifi.svg",
            (2, False): ":/network/media/btn_icons/2bar_wifi.svg",
            (3, False): ":/network/media/btn_icons/3bar_wifi.svg",
            (4, False): ":/network/media/btn_icons/4bar_wifi.svg",
            (0, True): ":/network/media/btn_icons/0bar_wifi_protected.svg",
            (1, True): ":/network/media/btn_icons/1bar_wifi_protected.svg",
            (2, True): ":/network/media/btn_icons/2bar_wifi_protected.svg",
            (3, True): ":/network/media/btn_icons/3bar_wifi_protected.svg",
            (4, True): ":/network/media/btn_icons/4bar_wifi_protected.svg",
        }

    def get_pixmap(self, signal: int, status: str) -> QtGui.QPixmap:
        """Get pixmap for given signal strength and status."""
        bars = self._signal_to_bars(signal)
        is_protected = status == "Protected"
        key = (bars, is_protected)
        path = self._paths.get(key, self._paths[(0, False)])
        return QtGui.QPixmap(path)

    @staticmethod
    def _signal_to_bars(signal: int) -> int:
        """Convert signal strength to bar count."""
        if signal < SIGNAL_MINIMUM_THRESHOLD:
            return 0
        elif signal >= SIGNAL_EXCELLENT_THRESHOLD:
            return 4
        elif signal >= SIGNAL_GOOD_THRESHOLD:
            return 3
        elif signal > SIGNAL_FAIR_THRESHOLD:
            return 2
        else:
            return 1


class NetworkControlWindow(QtWidgets.QStackedWidget):
    """Main network control window widget."""

    request_network_scan = pyqtSignal(name="scan-network")
    new_ip_signal = pyqtSignal(str, name="ip-address-change")
    get_hotspot_ssid = pyqtSignal(str, name="hotspot-ssid-name")
    delete_network_signal = pyqtSignal(str, name="delete-network")

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None, /) -> None:
        """Initialize the network control window."""
        super().__init__(parent) if parent else super().__init__()

        self._init_instance_variables()
        self._setupUI()
        self._init_timers()
        self._init_model_view()
        self._init_network_worker()
        self._setup_navigation_signals()
        self._setup_action_signals()
        self._setup_toggle_signals()
        self._setup_password_visibility_signals()
        self._setup_icons()
        self._setup_input_fields()
        self._setup_keyboard()
        self._setup_scrollbar_signals()

        self._network_list_worker.build()
        self.request_network_scan.emit()
        self.hide()

        # Initialize UI state
        self._init_ui_state()

    def _init_ui_state(self) -> None:
        """Initialize UI to a clean disconnected state."""
        self.loadingwidget.setVisible(False)
        self._hide_all_info_elements()
        self._configure_info_box_centered()
        self.mn_info_box.setVisible(True)
        self.mn_info_box.setText(
            "Network connection required.\n\nConnect to Wi-Fi\nor\nTurn on Hotspot"
        )

    def _hide_all_info_elements(self) -> None:
        """Hide ALL elements in the info panel (details, loading, info box)."""
        # Hide network details
        self.netlist_ip.setVisible(False)
        self.netlist_ssuid.setVisible(False)
        self.mn_info_seperator.setVisible(False)
        self.line_2.setVisible(False)
        self.netlist_strength.setVisible(False)
        self.netlist_strength_label.setVisible(False)
        self.line_3.setVisible(False)
        self.netlist_security.setVisible(False)
        self.netlist_security_label.setVisible(False)
        # Hide loading
        self.loadingwidget.setVisible(False)
        # Hide info box
        self.mn_info_box.setVisible(False)

    def _init_instance_variables(self) -> None:
        """Initialize all instance variables."""
        self._icon_provider = WifiIconProvider()
        self._ongoing_update = False
        self._is_first_run = True
        self._networks: Dict[str, NetworkInfo] = {}
        self._previous_panel: Optional[QtWidgets.QWidget] = None
        self._current_field: Optional[QtWidgets.QLineEdit] = None
        self._current_network_is_open = False
        self._current_network_is_hidden = False
        self._is_connecting = False
        self._target_ssid: Optional[str] = None
        self._last_displayed_ssid: Optional[str] = None
        self._current_network_ssid: Optional[str] = (
            None  # Track current network for priority
        )

    def _setupUI(self) -> None:
        """Setup all UI elements programmatically."""
        self.setObjectName("wifi_stacked_page")
        self.resize(800, 480)

        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(0, 400))
        self.setMaximumSize(QtCore.QSize(16777215, 575))
        self.setStyleSheet(
            "#wifi_stacked_page{\n"
            "    background-image: url(:/background/media/1st_background.png);\n"
            "}\n"
        )

        self._sdbus_network = SdbusNetworkManagerAsync()
        self._popup = Popup(self)
        self._right_arrow_icon = QtGui.QPixmap(
            ":/arrow_icons/media/btn_icons/right_arrow.svg"
        )

        # Create all pages
        self._setup_main_network_page()
        self._setup_network_list_page()
        self._setup_add_network_page()
        self._setup_saved_connection_page()
        self._setup_saved_details_page()
        self._setup_hotspot_page()
        self._setup_hidden_network_page()

        self.setCurrentIndex(0)

    def _create_white_palette(self) -> QtGui.QPalette:
        """Create a palette with white text."""
        palette = QtGui.QPalette()
        white_brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        white_brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        grey_brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        grey_brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)

        for group in [
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorGroup.Inactive,
        ]:
            palette.setBrush(group, QtGui.QPalette.ColorRole.WindowText, white_brush)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Text, white_brush)

        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.WindowText,
            grey_brush,
        )
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Text,
            grey_brush,
        )

        return palette

    def _setup_main_network_page(self) -> None:
        """Setup the main network page."""
        self.main_network_page = QtWidgets.QWidget()
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.main_network_page.setSizePolicy(size_policy)
        self.main_network_page.setObjectName("main_network_page")

        main_layout = QtWidgets.QVBoxLayout(self.main_network_page)
        main_layout.setObjectName("verticalLayout_14")

        # Header layout
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setObjectName("main_network_header_layout")

        header_layout.addItem(
            QtWidgets.QSpacerItem(
                60,
                60,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.network_main_title = QtWidgets.QLabel(parent=self.main_network_page)
        title_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.network_main_title.setSizePolicy(title_policy)
        self.network_main_title.setMinimumSize(QtCore.QSize(300, 0))
        self.network_main_title.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.network_main_title.setFont(font)
        self.network_main_title.setStyleSheet("color:white")
        self.network_main_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.network_main_title.setText("Networks")
        self.network_main_title.setObjectName("network_main_title")
        header_layout.addWidget(self.network_main_title)

        self.network_backButton = IconButton(parent=self.main_network_page)
        self.network_backButton.setMinimumSize(QtCore.QSize(60, 60))
        self.network_backButton.setMaximumSize(QtCore.QSize(60, 60))
        self.network_backButton.setText("")
        self.network_backButton.setFlat(True)
        self.network_backButton.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.network_backButton.setObjectName("network_backButton")
        header_layout.addWidget(self.network_backButton)

        main_layout.addLayout(header_layout)

        # Content layout
        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setObjectName("main_network_content_layout")

        # Information frame
        self.mn_information_layout = BlocksCustomFrame(parent=self.main_network_page)
        info_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.mn_information_layout.setSizePolicy(info_policy)
        self.mn_information_layout.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.mn_information_layout.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.mn_information_layout.setObjectName("mn_information_layout")

        info_layout = QtWidgets.QVBoxLayout(self.mn_information_layout)
        info_layout.setObjectName("verticalLayout_3")

        # SSID label
        self.netlist_ssuid = QtWidgets.QLabel(parent=self.mn_information_layout)
        ssid_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.netlist_ssuid.setSizePolicy(ssid_policy)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.netlist_ssuid.setFont(font)
        self.netlist_ssuid.setStyleSheet("color: rgb(255, 255, 255);")
        self.netlist_ssuid.setText("")
        self.netlist_ssuid.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_ssuid.setObjectName("netlist_ssuid")
        info_layout.addWidget(self.netlist_ssuid)

        # Separator
        self.mn_info_seperator = QtWidgets.QFrame(parent=self.mn_information_layout)
        self.mn_info_seperator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.mn_info_seperator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.mn_info_seperator.setObjectName("mn_info_seperator")
        info_layout.addWidget(self.mn_info_seperator)

        # IP label
        self.netlist_ip = QtWidgets.QLabel(parent=self.mn_information_layout)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_ip.setFont(font)
        self.netlist_ip.setStyleSheet("color: rgb(255, 255, 255);")
        self.netlist_ip.setText("")
        self.netlist_ip.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_ip.setObjectName("netlist_ip")
        info_layout.addWidget(self.netlist_ip)

        # Connection info layout
        conn_info_layout = QtWidgets.QHBoxLayout()
        conn_info_layout.setObjectName("mn_conn_info")

        # Signal strength section
        sg_info_layout = QtWidgets.QVBoxLayout()
        sg_info_layout.setObjectName("mn_sg_info_layout")

        self.netlist_strength_label = QtWidgets.QLabel(
            parent=self.mn_information_layout
        )
        self.netlist_strength_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_strength_label.setFont(font)
        self.netlist_strength_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_strength_label.setText("Signal\nStrength")
        self.netlist_strength_label.setObjectName("netlist_strength_label")
        sg_info_layout.addWidget(self.netlist_strength_label)

        self.line_2 = QtWidgets.QFrame(parent=self.mn_information_layout)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        sg_info_layout.addWidget(self.line_2)

        self.netlist_strength = QtWidgets.QLabel(parent=self.mn_information_layout)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.netlist_strength.setFont(font)
        self.netlist_strength.setStyleSheet("color: rgb(255, 255, 255);")
        self.netlist_strength.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_strength.setText("")
        self.netlist_strength.setObjectName("netlist_strength")
        sg_info_layout.addWidget(self.netlist_strength)

        conn_info_layout.addLayout(sg_info_layout)

        # Security section
        sec_info_layout = QtWidgets.QVBoxLayout()
        sec_info_layout.setObjectName("mn_sec_info_layout")

        self.netlist_security_label = QtWidgets.QLabel(
            parent=self.mn_information_layout
        )
        self.netlist_security_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_security_label.setFont(font)
        self.netlist_security_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_security_label.setText("Security\nType")
        self.netlist_security_label.setObjectName("netlist_security_label")
        sec_info_layout.addWidget(self.netlist_security_label)

        self.line_3 = QtWidgets.QFrame(parent=self.mn_information_layout)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        sec_info_layout.addWidget(self.line_3)

        self.netlist_security = QtWidgets.QLabel(parent=self.mn_information_layout)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.netlist_security.setFont(font)
        self.netlist_security.setStyleSheet("color: rgb(255, 255, 255);")
        self.netlist_security.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_security.setText("")
        self.netlist_security.setObjectName("netlist_security")
        sec_info_layout.addWidget(self.netlist_security)

        conn_info_layout.addLayout(sec_info_layout)
        info_layout.addLayout(conn_info_layout)

        # Info box
        self.mn_info_box = QtWidgets.QLabel(parent=self.mn_information_layout)
        self.mn_info_box.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.mn_info_box.setFont(font)
        self.mn_info_box.setStyleSheet("color: white")
        self.mn_info_box.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.mn_info_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mn_info_box.setText(
            "No network connection.\n\n"
            "Try connecting to Wi-Fi \n"
            "or turn on the hotspot\n"
            "using the buttons on the side."
        )
        self.mn_info_box.setObjectName("mn_info_box")
        info_layout.addWidget(self.mn_info_box)

        # Loading widget
        self.loadingwidget = LoadingOverlayWidget(parent=self.mn_information_layout)
        self.loadingwidget.setEnabled(True)
        loading_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.loadingwidget.setSizePolicy(loading_policy)
        self.loadingwidget.setText("")
        self.loadingwidget.setObjectName("loadingwidget")
        info_layout.addWidget(self.loadingwidget)

        content_layout.addWidget(self.mn_information_layout)

        # Option buttons layout
        option_layout = QtWidgets.QVBoxLayout()
        option_layout.setObjectName("mn_option_button_layout")

        self.wifi_button = NetworkWidgetbuttons(parent=self.main_network_page)
        wifi_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.wifi_button.setSizePolicy(wifi_policy)
        self.wifi_button.setMaximumSize(QtCore.QSize(400, 9999))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.wifi_button.setFont(font)
        self.wifi_button.setText("Wi-Fi")
        self.wifi_button.setObjectName("wifi_button")
        option_layout.addWidget(self.wifi_button)

        self.hotspot_button = NetworkWidgetbuttons(parent=self.main_network_page)
        self.hotspot_button.setSizePolicy(wifi_policy)
        self.hotspot_button.setMaximumSize(QtCore.QSize(400, 9999))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.hotspot_button.setFont(font)
        self.hotspot_button.setText("Hotspot")
        self.hotspot_button.setObjectName("hotspot_button")
        option_layout.addWidget(self.hotspot_button)

        content_layout.addLayout(option_layout)
        main_layout.addLayout(content_layout)

        self.addWidget(self.main_network_page)

    def _setup_network_list_page(self) -> None:
        """Setup the network list page."""
        self.network_list_page = QtWidgets.QWidget()
        self.network_list_page.setObjectName("network_list_page")

        main_layout = QtWidgets.QVBoxLayout(self.network_list_page)
        main_layout.setObjectName("verticalLayout_9")

        # Header layout
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setObjectName("nl_header_layout")

        self.rescan_button = IconButton(parent=self.network_list_page)
        self.rescan_button.setMinimumSize(QtCore.QSize(60, 60))
        self.rescan_button.setMaximumSize(QtCore.QSize(60, 60))
        self.rescan_button.setText("Reload")
        self.rescan_button.setFlat(True)
        self.rescan_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/refresh.svg")
        )
        self.rescan_button.setProperty("button_type", "icon")
        self.rescan_button.setObjectName("rescan_button")
        header_layout.addWidget(self.rescan_button)

        self.network_list_title = QtWidgets.QLabel(parent=self.network_list_page)
        self.network_list_title.setMaximumSize(QtCore.QSize(16777215, 60))
        self.network_list_title.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(20)
        self.network_list_title.setFont(font)
        self.network_list_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.network_list_title.setText("Wi-Fi List")
        self.network_list_title.setObjectName("network_list_title")
        header_layout.addWidget(self.network_list_title)

        self.nl_back_button = IconButton(parent=self.network_list_page)
        self.nl_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.nl_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.nl_back_button.setText("Back")
        self.nl_back_button.setFlat(True)
        self.nl_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.nl_back_button.setProperty("class", "back_btn")
        self.nl_back_button.setProperty("button_type", "icon")
        self.nl_back_button.setObjectName("nl_back_button")
        header_layout.addWidget(self.nl_back_button)

        main_layout.addLayout(header_layout)

        # List view layout
        list_layout = QtWidgets.QHBoxLayout()
        list_layout.setObjectName("horizontalLayout_2")

        self.listView = QtWidgets.QListView(self.network_list_page)
        list_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        list_policy.setHorizontalStretch(1)
        list_policy.setVerticalStretch(1)
        self.listView.setSizePolicy(list_policy)
        self.listView.setMinimumSize(QtCore.QSize(0, 0))
        self.listView.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.listView.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.listView.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.listView.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.listView.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.listView.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.listView.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.listView.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.listView.setUniformItemSizes(True)
        self.listView.setSpacing(5)

        # Setup touch scrolling
        QtWidgets.QScroller.grabGesture(
            self.listView,
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )
        QtWidgets.QScroller.grabGesture(
            self.listView,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )

        scroller_instance = QtWidgets.QScroller.scroller(self.listView)
        scroller_props = scroller_instance.scrollerProperties()
        scroller_props.setScrollMetric(
            QtWidgets.QScrollerProperties.ScrollMetric.DragVelocitySmoothingFactor,
            0.05,
        )
        scroller_props.setScrollMetric(
            QtWidgets.QScrollerProperties.ScrollMetric.DecelerationFactor,
            0.4,
        )
        QtWidgets.QScroller.scroller(self.listView).setScrollerProperties(
            scroller_props
        )

        self.verticalScrollBar = CustomScrollBar(parent=self.network_list_page)
        scrollbar_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.verticalScrollBar.setSizePolicy(scrollbar_policy)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.verticalScrollBar.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )

        self.listView.setVerticalScrollBar(self.verticalScrollBar)
        self.listView.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        list_layout.addWidget(self.listView)
        list_layout.addWidget(self.verticalScrollBar)

        main_layout.addLayout(list_layout)

        self.scroller = QtWidgets.QScroller.scroller(self.listView)

        self.addWidget(self.network_list_page)

    def _setup_add_network_page(self) -> None:
        """Setup the add network page."""
        self.add_network_page = QtWidgets.QWidget()
        self.add_network_page.setObjectName("add_network_page")

        main_layout = QtWidgets.QVBoxLayout(self.add_network_page)
        main_layout.setObjectName("verticalLayout_10")

        # Header layout
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setObjectName("add_np_header_layout")

        header_layout.addItem(
            QtWidgets.QSpacerItem(
                40,
                60,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.add_network_network_label = QtWidgets.QLabel(parent=self.add_network_page)
        label_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        self.add_network_network_label.setSizePolicy(label_policy)
        self.add_network_network_label.setMinimumSize(QtCore.QSize(0, 60))
        self.add_network_network_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.add_network_network_label.setFont(font)
        self.add_network_network_label.setStyleSheet("color:white")
        self.add_network_network_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.add_network_network_label.setText("TextLabel")
        self.add_network_network_label.setObjectName("add_network_network_label")
        header_layout.addWidget(self.add_network_network_label)

        self.add_network_page_backButton = IconButton(parent=self.add_network_page)
        self.add_network_page_backButton.setMinimumSize(QtCore.QSize(60, 60))
        self.add_network_page_backButton.setMaximumSize(QtCore.QSize(60, 60))
        self.add_network_page_backButton.setText("Back")
        self.add_network_page_backButton.setFlat(True)
        self.add_network_page_backButton.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.add_network_page_backButton.setProperty("class", "back_btn")
        self.add_network_page_backButton.setProperty("button_type", "icon")
        self.add_network_page_backButton.setObjectName("add_network_page_backButton")
        header_layout.addWidget(self.add_network_page_backButton)

        main_layout.addLayout(header_layout)

        # Content layout
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMinimumSize
        )
        content_layout.setObjectName("add_np_content_layout")

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                50,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        # Password frame
        self.frame_2 = BlocksCustomFrame(parent=self.add_network_page)
        frame_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        frame_policy.setVerticalStretch(2)
        self.frame_2.setSizePolicy(frame_policy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 90))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")

        frame_layout_widget = QtWidgets.QWidget(parent=self.frame_2)
        frame_layout_widget.setGeometry(QtCore.QRect(10, 10, 761, 82))
        frame_layout_widget.setObjectName("layoutWidget_2")

        password_layout = QtWidgets.QHBoxLayout(frame_layout_widget)
        password_layout.setSizeConstraint(
            QtWidgets.QLayout.SizeConstraint.SetMaximumSize
        )
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setObjectName("horizontalLayout_5")

        self.add_network_password_label = QtWidgets.QLabel(parent=frame_layout_widget)
        self.add_network_password_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.add_network_password_label.setFont(font)
        self.add_network_password_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.add_network_password_label.setText("Password")
        self.add_network_password_label.setObjectName("add_network_password_label")
        password_layout.addWidget(self.add_network_password_label)

        self.add_network_password_field = BlocksCustomLinEdit(
            parent=frame_layout_widget
        )
        self.add_network_password_field.setHidden(True)
        self.add_network_password_field.setMinimumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_network_password_field.setFont(font)
        self.add_network_password_field.setObjectName("add_network_password_field")
        password_layout.addWidget(self.add_network_password_field)

        self.add_network_password_view = IconButton(parent=frame_layout_widget)
        self.add_network_password_view.setMinimumSize(QtCore.QSize(60, 60))
        self.add_network_password_view.setMaximumSize(QtCore.QSize(60, 60))
        self.add_network_password_view.setText("View")
        self.add_network_password_view.setFlat(True)
        self.add_network_password_view.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/unsee.svg")
        )
        self.add_network_password_view.setProperty("class", "back_btn")
        self.add_network_password_view.setProperty("button_type", "icon")
        self.add_network_password_view.setObjectName("add_network_password_view")
        password_layout.addWidget(self.add_network_password_view)

        content_layout.addWidget(self.frame_2)

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                150,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        # Validation button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        button_layout.setObjectName("horizontalLayout_6")

        self.add_network_validation_button = BlocksCustomButton(
            parent=self.add_network_page
        )
        self.add_network_validation_button.setEnabled(True)
        btn_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        btn_policy.setHorizontalStretch(1)
        btn_policy.setVerticalStretch(1)
        self.add_network_validation_button.setSizePolicy(btn_policy)
        self.add_network_validation_button.setMinimumSize(QtCore.QSize(250, 80))
        self.add_network_validation_button.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(15)
        self.add_network_validation_button.setFont(font)
        self.add_network_validation_button.setIconSize(QtCore.QSize(16, 16))
        self.add_network_validation_button.setCheckable(False)
        self.add_network_validation_button.setChecked(False)
        self.add_network_validation_button.setFlat(True)
        self.add_network_validation_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.add_network_validation_button.setText("Activate")
        self.add_network_validation_button.setObjectName(
            "add_network_validation_button"
        )
        button_layout.addWidget(
            self.add_network_validation_button,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop,
        )

        content_layout.addLayout(button_layout)
        main_layout.addLayout(content_layout)

        self.addWidget(self.add_network_page)

    def _setup_hidden_network_page(self) -> None:
        """Setup the hidden network page for connecting to networks with hidden SSID."""
        self.hidden_network_page = QtWidgets.QWidget()
        self.hidden_network_page.setObjectName("hidden_network_page")

        main_layout = QtWidgets.QVBoxLayout(self.hidden_network_page)
        main_layout.setObjectName("hidden_network_layout")

        # Header layout
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addItem(
            QtWidgets.QSpacerItem(
                40,
                60,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.hidden_network_title = QtWidgets.QLabel(parent=self.hidden_network_page)
        self.hidden_network_title.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(20)
        self.hidden_network_title.setFont(font)
        self.hidden_network_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hidden_network_title.setText("Hidden Network")
        header_layout.addWidget(self.hidden_network_title)

        self.hidden_network_back_button = IconButton(parent=self.hidden_network_page)
        self.hidden_network_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.hidden_network_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.hidden_network_back_button.setFlat(True)
        self.hidden_network_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.hidden_network_back_button.setProperty("button_type", "icon")
        header_layout.addWidget(self.hidden_network_back_button)

        main_layout.addLayout(header_layout)

        # Content
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                30,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        # SSID Frame
        ssid_frame = BlocksCustomFrame(parent=self.hidden_network_page)
        ssid_frame.setMinimumSize(QtCore.QSize(0, 80))
        ssid_frame.setMaximumSize(QtCore.QSize(16777215, 90))
        ssid_frame_layout = QtWidgets.QHBoxLayout(ssid_frame)

        ssid_label = QtWidgets.QLabel("Network\nName", parent=ssid_frame)
        ssid_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        ssid_label.setFont(font)
        ssid_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        ssid_frame_layout.addWidget(ssid_label)

        self.hidden_network_ssid_field = BlocksCustomLinEdit(parent=ssid_frame)
        self.hidden_network_ssid_field.setMinimumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.hidden_network_ssid_field.setFont(font)
        self.hidden_network_ssid_field.setPlaceholderText("Enter network name")
        ssid_frame_layout.addWidget(self.hidden_network_ssid_field)

        content_layout.addWidget(ssid_frame)

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        # Password Frame
        password_frame = BlocksCustomFrame(parent=self.hidden_network_page)
        password_frame.setMinimumSize(QtCore.QSize(0, 80))
        password_frame.setMaximumSize(QtCore.QSize(16777215, 90))
        password_frame_layout = QtWidgets.QHBoxLayout(password_frame)

        password_label = QtWidgets.QLabel("Password", parent=password_frame)
        password_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        password_label.setFont(font)
        password_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        password_frame_layout.addWidget(password_label)

        self.hidden_network_password_field = BlocksCustomLinEdit(parent=password_frame)
        self.hidden_network_password_field.setHidden(True)
        self.hidden_network_password_field.setMinimumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.hidden_network_password_field.setFont(font)
        self.hidden_network_password_field.setPlaceholderText(
            "Enter password (leave empty for open networks)"
        )
        self.hidden_network_password_field.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Password
        )
        password_frame_layout.addWidget(self.hidden_network_password_field)

        self.hidden_network_password_view = IconButton(parent=password_frame)
        self.hidden_network_password_view.setMinimumSize(QtCore.QSize(60, 60))
        self.hidden_network_password_view.setMaximumSize(QtCore.QSize(60, 60))
        self.hidden_network_password_view.setFlat(True)
        self.hidden_network_password_view.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/unsee.svg")
        )
        self.hidden_network_password_view.setProperty("button_type", "icon")
        password_frame_layout.addWidget(self.hidden_network_password_view)

        content_layout.addWidget(password_frame)

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                50,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        # Connect button
        self.hidden_network_connect_button = BlocksCustomButton(
            parent=self.hidden_network_page
        )
        self.hidden_network_connect_button.setMinimumSize(QtCore.QSize(250, 80))
        self.hidden_network_connect_button.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.hidden_network_connect_button.setFont(font)
        self.hidden_network_connect_button.setFlat(True)
        self.hidden_network_connect_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.hidden_network_connect_button.setText("Connect")
        content_layout.addWidget(
            self.hidden_network_connect_button, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        main_layout.addLayout(content_layout)
        self.addWidget(self.hidden_network_page)

        # Connect signals
        self.hidden_network_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.network_list_page))
        )
        self.hidden_network_connect_button.clicked.connect(
            self._on_hidden_network_connect
        )
        self.hidden_network_ssid_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.hidden_network_page, self.hidden_network_ssid_field
            )
        )
        self.hidden_network_password_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.hidden_network_page, self.hidden_network_password_field
            )
        )
        self._setup_password_visibility_toggle(
            self.hidden_network_password_view, self.hidden_network_password_field
        )

    def _on_hidden_network_connect(self) -> None:
        """Handle connection to hidden network."""
        ssid = self.hidden_network_ssid_field.text().strip()
        password = self.hidden_network_password_field.text()

        if not ssid:
            self._show_error_popup("Please enter a network name.")
            return

        self._current_network_is_hidden = True
        self._current_network_is_open = not password

        result = self._sdbus_network.add_wifi_network(ssid=ssid, psk=password)

        if result is None:
            self._handle_failed_network_add("Failed to add network")
            return

        error_msg = result.get("error", "") if isinstance(result, dict) else ""

        if not error_msg:
            self.hidden_network_ssid_field.clear()
            self.hidden_network_password_field.clear()
            self._handle_successful_network_add(ssid)
        else:
            self._handle_failed_network_add(error_msg)

    def _setup_saved_connection_page(self) -> None:
        """Setup the saved connection page."""
        self.saved_connection_page = QtWidgets.QWidget()
        self.saved_connection_page.setObjectName("saved_connection_page")

        main_layout = QtWidgets.QVBoxLayout(self.saved_connection_page)
        main_layout.setObjectName("verticalLayout_11")

        # Header layout
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setObjectName("horizontalLayout_7")

        header_layout.addItem(
            QtWidgets.QSpacerItem(
                60,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.saved_connection_network_name = QtWidgets.QLabel(
            parent=self.saved_connection_page
        )
        name_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.saved_connection_network_name.setSizePolicy(name_policy)
        self.saved_connection_network_name.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.saved_connection_network_name.setFont(font)
        self.saved_connection_network_name.setStyleSheet("color: rgb(255, 255, 255);")
        self.saved_connection_network_name.setText("")
        self.saved_connection_network_name.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.saved_connection_network_name.setObjectName(
            "saved_connection_network_name"
        )
        header_layout.addWidget(self.saved_connection_network_name)

        self.saved_connection_back_button = IconButton(
            parent=self.saved_connection_page
        )
        self.saved_connection_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.saved_connection_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.saved_connection_back_button.setText("Back")
        self.saved_connection_back_button.setFlat(True)
        self.saved_connection_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.saved_connection_back_button.setProperty("class", "back_btn")
        self.saved_connection_back_button.setProperty("button_type", "icon")
        self.saved_connection_back_button.setObjectName("saved_connection_back_button")
        header_layout.addWidget(
            self.saved_connection_back_button, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )

        main_layout.addLayout(header_layout)

        # Content layout
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setObjectName("verticalLayout_5")

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        # Main content horizontal layout
        main_content_layout = QtWidgets.QHBoxLayout()
        main_content_layout.setObjectName("horizontalLayout_9")

        # Info frame layout
        info_layout = QtWidgets.QVBoxLayout()
        info_layout.setObjectName("verticalLayout_2")

        self.frame = BlocksCustomFrame(parent=self.saved_connection_page)
        frame_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.frame.setSizePolicy(frame_policy)
        self.frame.setMaximumSize(QtCore.QSize(400, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        frame_inner_layout = QtWidgets.QVBoxLayout(self.frame)
        frame_inner_layout.setObjectName("verticalLayout_6")

        # Signal strength row
        signal_layout = QtWidgets.QHBoxLayout()
        signal_layout.setObjectName("horizontalLayout")

        self.netlist_strength_label_2 = QtWidgets.QLabel(parent=self.frame)
        self.netlist_strength_label_2.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_strength_label_2.setFont(font)
        self.netlist_strength_label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_strength_label_2.setText("Signal\nStrength")
        self.netlist_strength_label_2.setObjectName("netlist_strength_label_2")
        signal_layout.addWidget(self.netlist_strength_label_2)

        self.saved_connection_signal_strength_info_frame = QtWidgets.QLabel(
            parent=self.frame
        )
        self.saved_connection_signal_strength_info_frame.setMinimumSize(
            QtCore.QSize(250, 0)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.saved_connection_signal_strength_info_frame.setFont(font)
        self.saved_connection_signal_strength_info_frame.setStyleSheet(
            "color: rgb(255, 255, 255);"
        )
        self.saved_connection_signal_strength_info_frame.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.saved_connection_signal_strength_info_frame.setText("TextLabel")
        self.saved_connection_signal_strength_info_frame.setObjectName(
            "saved_connection_signal_strength_info_frame"
        )
        signal_layout.addWidget(self.saved_connection_signal_strength_info_frame)

        frame_inner_layout.addLayout(signal_layout)

        self.line_4 = QtWidgets.QFrame(parent=self.frame)
        self.line_4.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_4.setObjectName("line_4")
        frame_inner_layout.addWidget(self.line_4)

        # Security type row
        security_layout = QtWidgets.QHBoxLayout()
        security_layout.setObjectName("horizontalLayout_2")

        self.netlist_security_label_2 = QtWidgets.QLabel(parent=self.frame)
        self.netlist_security_label_2.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_security_label_2.setFont(font)
        self.netlist_security_label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_security_label_2.setText("Security\nType")
        self.netlist_security_label_2.setObjectName("netlist_security_label_2")
        security_layout.addWidget(self.netlist_security_label_2)

        self.saved_connection_security_type_info_label = QtWidgets.QLabel(
            parent=self.frame
        )
        self.saved_connection_security_type_info_label.setMinimumSize(
            QtCore.QSize(250, 0)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.saved_connection_security_type_info_label.setFont(font)
        self.saved_connection_security_type_info_label.setStyleSheet(
            "color: rgb(255, 255, 255);"
        )
        self.saved_connection_security_type_info_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.saved_connection_security_type_info_label.setText("TextLabel")
        self.saved_connection_security_type_info_label.setObjectName(
            "saved_connection_security_type_info_label"
        )
        security_layout.addWidget(self.saved_connection_security_type_info_label)

        frame_inner_layout.addLayout(security_layout)

        self.line_5 = QtWidgets.QFrame(parent=self.frame)
        self.line_5.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_5.setObjectName("line_5")
        frame_inner_layout.addWidget(self.line_5)

        # Status row
        status_layout = QtWidgets.QHBoxLayout()
        status_layout.setObjectName("horizontalLayout_8")

        self.netlist_security_label_4 = QtWidgets.QLabel(parent=self.frame)
        self.netlist_security_label_4.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(15)
        self.netlist_security_label_4.setFont(font)
        self.netlist_security_label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.netlist_security_label_4.setText("Status")
        self.netlist_security_label_4.setObjectName("netlist_security_label_4")
        status_layout.addWidget(self.netlist_security_label_4)

        self.sn_info = QtWidgets.QLabel(parent=self.frame)
        self.sn_info.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sn_info.setFont(font)
        self.sn_info.setStyleSheet("color: rgb(255, 255, 255);")
        self.sn_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sn_info.setText("TextLabel")
        self.sn_info.setObjectName("sn_info")
        status_layout.addWidget(self.sn_info)

        frame_inner_layout.addLayout(status_layout)
        info_layout.addWidget(self.frame)
        main_content_layout.addLayout(info_layout)

        # Action buttons frame
        self.frame_8 = BlocksCustomFrame(parent=self.saved_connection_page)
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName("frame_8")

        buttons_layout = QtWidgets.QVBoxLayout(self.frame_8)
        buttons_layout.setObjectName("verticalLayout_4")

        self.network_activate_btn = BlocksCustomButton(parent=self.frame_8)
        self.network_activate_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.network_activate_btn.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.network_activate_btn.setFont(font)
        self.network_activate_btn.setFlat(True)
        self.network_activate_btn.setText("Connect")
        self.network_activate_btn.setObjectName("network_activate_btn")
        buttons_layout.addWidget(
            self.network_activate_btn,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.network_details_btn = BlocksCustomButton(parent=self.frame_8)
        self.network_details_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.network_details_btn.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.network_details_btn.setFont(font)
        self.network_details_btn.setFlat(True)
        self.network_details_btn.setText("Details")
        self.network_details_btn.setObjectName("network_details_btn")
        buttons_layout.addWidget(
            self.network_details_btn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.network_delete_btn = BlocksCustomButton(parent=self.frame_8)
        self.network_delete_btn.setMinimumSize(QtCore.QSize(250, 80))
        self.network_delete_btn.setMaximumSize(QtCore.QSize(250, 80))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.network_delete_btn.setFont(font)
        self.network_delete_btn.setFlat(True)
        self.network_delete_btn.setText("Forget")
        self.network_delete_btn.setObjectName("network_delete_btn")
        buttons_layout.addWidget(
            self.network_delete_btn,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        main_content_layout.addWidget(self.frame_8)
        content_layout.addLayout(main_content_layout)
        main_layout.addLayout(content_layout)

        self.addWidget(self.saved_connection_page)

    def _setup_saved_details_page(self) -> None:
        """Setup the saved network details page."""
        self.saved_details_page = QtWidgets.QWidget()
        self.saved_details_page.setObjectName("saved_details_page")

        main_layout = QtWidgets.QVBoxLayout(self.saved_details_page)
        main_layout.setObjectName("verticalLayout_19")

        # Header layout
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setObjectName("horizontalLayout_14")

        header_layout.addItem(
            QtWidgets.QSpacerItem(
                60,
                60,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.snd_name = QtWidgets.QLabel(parent=self.saved_details_page)
        name_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.snd_name.setSizePolicy(name_policy)
        self.snd_name.setMaximumSize(QtCore.QSize(16777215, 60))
        self.snd_name.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(20)
        self.snd_name.setFont(font)
        self.snd_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.snd_name.setText("SSID")
        self.snd_name.setObjectName("snd_name")
        header_layout.addWidget(self.snd_name)

        self.snd_back = IconButton(parent=self.saved_details_page)
        self.snd_back.setMinimumSize(QtCore.QSize(60, 60))
        self.snd_back.setMaximumSize(QtCore.QSize(60, 60))
        self.snd_back.setText("Back")
        self.snd_back.setFlat(True)
        self.snd_back.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.snd_back.setProperty("class", "back_btn")
        self.snd_back.setProperty("button_type", "icon")
        self.snd_back.setObjectName("snd_back")
        header_layout.addWidget(self.snd_back)

        main_layout.addLayout(header_layout)

        # Content layout
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setObjectName("verticalLayout_8")

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        # Password change frame
        self.frame_9 = BlocksCustomFrame(parent=self.saved_details_page)
        frame_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.frame_9.setSizePolicy(frame_policy)
        self.frame_9.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_9.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName("frame_9")

        frame_layout_widget = QtWidgets.QWidget(parent=self.frame_9)
        frame_layout_widget.setGeometry(QtCore.QRect(0, 0, 776, 62))
        frame_layout_widget.setObjectName("layoutWidget_8")

        password_layout = QtWidgets.QHBoxLayout(frame_layout_widget)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setObjectName("horizontalLayout_10")

        self.saved_connection_change_password_label_3 = QtWidgets.QLabel(
            parent=frame_layout_widget
        )
        self.saved_connection_change_password_label_3.setPalette(
            self._create_white_palette()
        )
        font = QtGui.QFont()
        font.setPointSize(15)
        self.saved_connection_change_password_label_3.setFont(font)
        self.saved_connection_change_password_label_3.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.saved_connection_change_password_label_3.setText("Change\nPassword")
        self.saved_connection_change_password_label_3.setObjectName(
            "saved_connection_change_password_label_3"
        )
        password_layout.addWidget(
            self.saved_connection_change_password_label_3,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        self.saved_connection_change_password_field = BlocksCustomLinEdit(
            parent=frame_layout_widget
        )
        self.saved_connection_change_password_field.setHidden(True)
        self.saved_connection_change_password_field.setMinimumSize(
            QtCore.QSize(500, 60)
        )
        self.saved_connection_change_password_field.setMaximumSize(
            QtCore.QSize(500, 16777215)
        )
        font = QtGui.QFont()
        font.setPointSize(12)
        self.saved_connection_change_password_field.setFont(font)
        self.saved_connection_change_password_field.setObjectName(
            "saved_connection_change_password_field"
        )
        password_layout.addWidget(
            self.saved_connection_change_password_field,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter,
        )

        self.saved_connection_change_password_view = IconButton(
            parent=frame_layout_widget
        )
        self.saved_connection_change_password_view.setMinimumSize(QtCore.QSize(60, 60))
        self.saved_connection_change_password_view.setMaximumSize(QtCore.QSize(60, 60))
        self.saved_connection_change_password_view.setText("View")
        self.saved_connection_change_password_view.setFlat(True)
        self.saved_connection_change_password_view.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/unsee.svg")
        )
        self.saved_connection_change_password_view.setProperty("class", "back_btn")
        self.saved_connection_change_password_view.setProperty("button_type", "icon")
        self.saved_connection_change_password_view.setObjectName(
            "saved_connection_change_password_view"
        )
        password_layout.addWidget(
            self.saved_connection_change_password_view,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        content_layout.addWidget(self.frame_9)

        # Priority buttons layout
        priority_outer_layout = QtWidgets.QHBoxLayout()
        priority_outer_layout.setObjectName("horizontalLayout_13")

        priority_inner_layout = QtWidgets.QVBoxLayout()
        priority_inner_layout.setObjectName("verticalLayout_13")

        self.frame_12 = BlocksCustomFrame(parent=self.saved_details_page)
        frame_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.frame_12.setSizePolicy(frame_policy)
        self.frame_12.setMinimumSize(QtCore.QSize(400, 160))
        self.frame_12.setMaximumSize(QtCore.QSize(400, 99999))
        self.frame_12.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_12.setProperty("text", "Network priority")
        self.frame_12.setObjectName("frame_12")

        frame_inner_layout = QtWidgets.QVBoxLayout(self.frame_12)
        frame_inner_layout.setObjectName("verticalLayout_17")

        frame_inner_layout.addItem(
            QtWidgets.QSpacerItem(
                10,
                10,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        # Priority buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setObjectName("horizontalLayout_4")

        self.priority_btn_group = QtWidgets.QButtonGroup(self)
        self.priority_btn_group.setObjectName("priority_btn_group")

        self.low_priority_btn = BlocksCustomCheckButton(parent=self.frame_12)
        self.low_priority_btn.setMinimumSize(QtCore.QSize(100, 100))
        self.low_priority_btn.setMaximumSize(QtCore.QSize(100, 100))
        self.low_priority_btn.setCheckable(True)
        self.low_priority_btn.setAutoExclusive(True)
        self.low_priority_btn.setFlat(True)
        self.low_priority_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/indf_svg.svg")
        )
        self.low_priority_btn.setText("Low")
        self.low_priority_btn.setProperty("class", "back_btn")
        self.low_priority_btn.setProperty("button_type", "icon")
        self.low_priority_btn.setObjectName("low_priority_btn")
        self.priority_btn_group.addButton(self.low_priority_btn)
        buttons_layout.addWidget(self.low_priority_btn)

        self.med_priority_btn = BlocksCustomCheckButton(parent=self.frame_12)
        self.med_priority_btn.setMinimumSize(QtCore.QSize(100, 100))
        self.med_priority_btn.setMaximumSize(QtCore.QSize(100, 100))
        self.med_priority_btn.setCheckable(True)
        self.med_priority_btn.setChecked(False)  # Don't set default checked
        self.med_priority_btn.setAutoExclusive(True)
        self.med_priority_btn.setFlat(True)
        self.med_priority_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/indf_svg.svg")
        )
        self.med_priority_btn.setText("Medium")
        self.med_priority_btn.setProperty("class", "back_btn")
        self.med_priority_btn.setProperty("button_type", "icon")
        self.med_priority_btn.setObjectName("med_priority_btn")
        self.priority_btn_group.addButton(self.med_priority_btn)
        buttons_layout.addWidget(self.med_priority_btn)

        self.high_priority_btn = BlocksCustomCheckButton(parent=self.frame_12)
        self.high_priority_btn.setMinimumSize(QtCore.QSize(100, 100))
        self.high_priority_btn.setMaximumSize(QtCore.QSize(100, 100))
        self.high_priority_btn.setCheckable(True)
        self.high_priority_btn.setChecked(False)
        self.high_priority_btn.setAutoExclusive(True)
        self.high_priority_btn.setFlat(True)
        self.high_priority_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/indf_svg.svg")
        )
        self.high_priority_btn.setText("High")
        self.high_priority_btn.setProperty("class", "back_btn")
        self.high_priority_btn.setProperty("button_type", "icon")
        self.high_priority_btn.setObjectName("high_priority_btn")
        self.priority_btn_group.addButton(self.high_priority_btn)
        buttons_layout.addWidget(self.high_priority_btn)

        frame_inner_layout.addLayout(buttons_layout)

        priority_inner_layout.addWidget(
            self.frame_12,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        priority_outer_layout.addLayout(priority_inner_layout)
        content_layout.addLayout(priority_outer_layout)
        main_layout.addLayout(content_layout)

        self.addWidget(self.saved_details_page)

    def _setup_hotspot_page(self) -> None:
        """Setup the hotspot configuration page."""
        self.hotspot_page = QtWidgets.QWidget()
        self.hotspot_page.setObjectName("hotspot_page")

        main_layout = QtWidgets.QVBoxLayout(self.hotspot_page)
        main_layout.setObjectName("verticalLayout_12")

        # Header layout
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setObjectName("hospot_page_header_layout")

        header_layout.addItem(
            QtWidgets.QSpacerItem(
                40,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        self.hotspot_header_title = QtWidgets.QLabel(parent=self.hotspot_page)
        self.hotspot_header_title.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setPointSize(20)
        self.hotspot_header_title.setFont(font)
        self.hotspot_header_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hotspot_header_title.setText("Hotspot")
        self.hotspot_header_title.setObjectName("hotspot_header_title")
        header_layout.addWidget(self.hotspot_header_title)

        self.hotspot_back_button = IconButton(parent=self.hotspot_page)
        self.hotspot_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.hotspot_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.hotspot_back_button.setText("Back")
        self.hotspot_back_button.setFlat(True)
        self.hotspot_back_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.hotspot_back_button.setProperty("class", "back_btn")
        self.hotspot_back_button.setProperty("button_type", "icon")
        self.hotspot_back_button.setObjectName("hotspot_back_button")
        header_layout.addWidget(self.hotspot_back_button)

        main_layout.addLayout(header_layout)

        # Content layout
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setContentsMargins(-1, 5, -1, 5)
        content_layout.setObjectName("hotspot_page_content_layout")

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                50,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        # Hotspot name frame
        self.frame_6 = BlocksCustomFrame(parent=self.hotspot_page)
        frame_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.frame_6.setSizePolicy(frame_policy)
        self.frame_6.setMinimumSize(QtCore.QSize(70, 80))
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")

        frame_layout_widget = QtWidgets.QWidget(parent=self.frame_6)
        frame_layout_widget.setGeometry(QtCore.QRect(0, 10, 776, 61))
        frame_layout_widget.setObjectName("layoutWidget_6")

        name_layout = QtWidgets.QHBoxLayout(frame_layout_widget)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setObjectName("horizontalLayout_11")

        self.hotspot_info_name_label = QtWidgets.QLabel(parent=frame_layout_widget)
        label_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum
        )
        self.hotspot_info_name_label.setSizePolicy(label_policy)
        self.hotspot_info_name_label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.hotspot_info_name_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(10)
        self.hotspot_info_name_label.setFont(font)
        self.hotspot_info_name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hotspot_info_name_label.setText("Hotspot Name: ")
        self.hotspot_info_name_label.setObjectName("hotspot_info_name_label")
        name_layout.addWidget(self.hotspot_info_name_label)

        self.hotspot_name_input_field = BlocksCustomLinEdit(parent=frame_layout_widget)
        field_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self.hotspot_name_input_field.setSizePolicy(field_policy)
        self.hotspot_name_input_field.setMinimumSize(QtCore.QSize(500, 40))
        self.hotspot_name_input_field.setMaximumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.hotspot_name_input_field.setFont(font)
        # Name should be visible, not masked
        self.hotspot_name_input_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.hotspot_name_input_field.setObjectName("hotspot_name_input_field")
        name_layout.addWidget(
            self.hotspot_name_input_field, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        name_layout.addItem(
            QtWidgets.QSpacerItem(
                60,
                20,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        content_layout.addWidget(self.frame_6)

        content_layout.addItem(
            QtWidgets.QSpacerItem(
                773,
                128,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Minimum,
            )
        )

        # Hotspot password frame
        self.frame_7 = BlocksCustomFrame(parent=self.hotspot_page)
        frame_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.frame_7.setSizePolicy(frame_policy)
        self.frame_7.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")

        password_layout_widget = QtWidgets.QWidget(parent=self.frame_7)
        password_layout_widget.setGeometry(QtCore.QRect(0, 10, 776, 62))
        password_layout_widget.setObjectName("layoutWidget_7")

        password_layout = QtWidgets.QHBoxLayout(password_layout_widget)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setObjectName("horizontalLayout_12")

        self.hotspot_info_password_label = QtWidgets.QLabel(
            parent=password_layout_widget
        )
        self.hotspot_info_password_label.setSizePolicy(label_policy)
        self.hotspot_info_password_label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.hotspot_info_password_label.setPalette(self._create_white_palette())
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(10)
        self.hotspot_info_password_label.setFont(font)
        self.hotspot_info_password_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.hotspot_info_password_label.setText("Hotspot Password:")
        self.hotspot_info_password_label.setObjectName("hotspot_info_password_label")
        password_layout.addWidget(self.hotspot_info_password_label)

        self.hotspot_password_input_field = BlocksCustomLinEdit(
            parent=password_layout_widget
        )
        self.hotspot_password_input_field.setHidden(True)
        self.hotspot_password_input_field.setSizePolicy(field_policy)
        self.hotspot_password_input_field.setMinimumSize(QtCore.QSize(500, 40))
        self.hotspot_password_input_field.setMaximumSize(QtCore.QSize(500, 60))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.hotspot_password_input_field.setFont(font)
        self.hotspot_password_input_field.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Password
        )
        self.hotspot_password_input_field.setObjectName("hotspot_password_input_field")
        password_layout.addWidget(
            self.hotspot_password_input_field, 0, QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        self.hotspot_password_view_button = IconButton(parent=password_layout_widget)
        self.hotspot_password_view_button.setMinimumSize(QtCore.QSize(60, 60))
        self.hotspot_password_view_button.setMaximumSize(QtCore.QSize(60, 60))
        self.hotspot_password_view_button.setText("View")
        self.hotspot_password_view_button.setFlat(True)
        self.hotspot_password_view_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/unsee.svg")
        )
        self.hotspot_password_view_button.setProperty("class", "back_btn")
        self.hotspot_password_view_button.setProperty("button_type", "icon")
        self.hotspot_password_view_button.setObjectName("hotspot_password_view_button")
        password_layout.addWidget(self.hotspot_password_view_button)

        content_layout.addWidget(self.frame_7)

        # Save button
        self.hotspot_change_confirm = BlocksCustomButton(parent=self.hotspot_page)
        self.hotspot_change_confirm.setMinimumSize(QtCore.QSize(200, 80))
        self.hotspot_change_confirm.setMaximumSize(QtCore.QSize(250, 100))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.hotspot_change_confirm.setFont(font)
        self.hotspot_change_confirm.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/save.svg")
        )
        self.hotspot_change_confirm.setText("Save")
        self.hotspot_change_confirm.setObjectName("hotspot_change_confirm")
        content_layout.addWidget(
            self.hotspot_change_confirm,
            0,
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        main_layout.addLayout(content_layout)

        self.addWidget(self.hotspot_page)

    def _init_timers(self) -> None:
        """Initialize all timers."""
        self._status_check_timer = QtCore.QTimer(self)
        self._status_check_timer.setInterval(STATUS_CHECK_INTERVAL_MS)

        self._delayed_action_timer = QtCore.QTimer(self)
        self._delayed_action_timer.setSingleShot(True)

        self._load_timer = QtCore.QTimer(self)
        self._load_timer.setSingleShot(True)
        self._load_timer.timeout.connect(self._handle_load_timeout)

    def _init_model_view(self) -> None:
        """Initialize the model and view for network list."""
        self._model = EntryListModel()
        self._model.setParent(self.listView)
        self._entry_delegate = EntryDelegate()
        self.listView.setModel(self._model)
        self.listView.setItemDelegate(self._entry_delegate)
        self._entry_delegate.item_selected.connect(self._on_ssid_item_clicked)
        self._configure_list_view_palette()

    def _init_network_worker(self) -> None:
        """Initialize the network list worker."""
        self._network_list_worker = BuildNetworkList(
            nm=self._sdbus_network, poll_interval_ms=DEFAULT_POLL_INTERVAL_MS
        )
        self._network_list_worker.finished_network_list_build.connect(
            self._handle_network_list
        )
        self._network_list_worker.start_polling()
        self.rescan_button.clicked.connect(self._network_list_worker.build)

    def _setup_navigation_signals(self) -> None:
        """Setup navigation button signals."""
        self.wifi_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.network_list_page))
        )
        self.hotspot_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.hotspot_page))
        )
        self.nl_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.main_network_page))
        )
        self.network_backButton.clicked.connect(self.hide)

        self.add_network_page_backButton.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.network_list_page))
        )

        self.saved_connection_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.network_list_page))
        )
        self.snd_back.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.saved_connection_page))
        )
        self.network_details_btn.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.saved_details_page))
        )

        self.hotspot_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.main_network_page))
        )
        self.hotspot_change_confirm.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.main_network_page))
        )

    def _setup_action_signals(self) -> None:
        """Setup action button signals."""
        self._sdbus_network.nm_state_change.connect(self._evaluate_network_state)
        self.request_network_scan.connect(self._rescan_networks)
        self.delete_network_signal.connect(self._delete_network)

        self.add_network_validation_button.clicked.connect(self._add_network)

        self.snd_back.clicked.connect(self._on_save_network_settings)
        self.network_activate_btn.clicked.connect(self._on_saved_wifi_option_selected)
        self.network_delete_btn.clicked.connect(self._on_saved_wifi_option_selected)

        self._status_check_timer.timeout.connect(self._check_connection_status)

    def _setup_toggle_signals(self) -> None:
        """Setup toggle button signals."""
        self.wifi_button.toggle_button.stateChange.connect(self._on_toggle_state)
        self.hotspot_button.toggle_button.stateChange.connect(self._on_toggle_state)

    def _setup_password_visibility_signals(self) -> None:
        """Setup password visibility toggle signals."""
        self._setup_password_visibility_toggle(
            self.add_network_password_view,
            self.add_network_password_field,
        )
        self._setup_password_visibility_toggle(
            self.saved_connection_change_password_view,
            self.saved_connection_change_password_field,
        )
        self._setup_password_visibility_toggle(
            self.hotspot_password_view_button,
            self.hotspot_password_input_field,
        )

    def _setup_password_visibility_toggle(
        self, view_button: QtWidgets.QWidget, password_field: QtWidgets.QLineEdit
    ) -> None:
        """Setup password visibility toggle for a button/field pair."""
        view_button.setCheckable(True)

        see_icon = QtGui.QPixmap(":/ui/media/btn_icons/see.svg")
        unsee_icon = QtGui.QPixmap(":/ui/media/btn_icons/unsee.svg")

        # Connect toggle signal
        view_button.toggled.connect(
            lambda checked: password_field.setHidden(not checked)
        )

        # Update icon based on toggle state
        view_button.toggled.connect(
            lambda checked: view_button.setPixmap(
                unsee_icon if not checked else see_icon
            )
        )

    def _setup_icons(self) -> None:
        """Setup button icons."""
        self.hotspot_button.setPixmap(
            QtGui.QPixmap(":/network/media/btn_icons/hotspot.svg")
        )
        self.wifi_button.setPixmap(
            QtGui.QPixmap(":/network/media/btn_icons/wifi_config.svg")
        )
        self.network_delete_btn.setPixmap(
            QtGui.QPixmap(":/ui/media/btn_icons/garbage-icon.svg")
        )
        self.network_activate_btn.setPixmap(
            QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.network_details_btn.setPixmap(
            QtGui.QPixmap(":/ui/media/btn_icons/printer_settings.svg")
        )

    def _setup_input_fields(self) -> None:
        """Setup input field properties."""
        self.add_network_password_field.setCursor(QtCore.Qt.CursorShape.BlankCursor)
        self.hotspot_name_input_field.setCursor(QtCore.Qt.CursorShape.BlankCursor)
        self.hotspot_password_input_field.setCursor(QtCore.Qt.CursorShape.BlankCursor)

        self.hotspot_password_input_field.setPlaceholderText("Defaults to: 123456789")
        self.hotspot_name_input_field.setText(
            str(self._sdbus_network.get_hotspot_ssid() or "PrinterHotspot")
        )
        self.hotspot_password_input_field.setText(
            str(self._sdbus_network.hotspot_password or "123456789")
        )

    def _setup_keyboard(self) -> None:
        """Setup the on-screen keyboard."""
        self._qwerty = CustomQwertyKeyboard(self)
        self.addWidget(self._qwerty)
        self._qwerty.value_selected.connect(self._on_qwerty_value_selected)
        self._qwerty.request_back.connect(self._on_qwerty_go_back)

        self.add_network_password_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.add_network_page, self.add_network_password_field
            )
        )
        self.hotspot_password_input_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.hotspot_page, self.hotspot_password_input_field
            )
        )
        self.hotspot_name_input_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.hotspot_page, self.hotspot_name_input_field
            )
        )
        self.saved_connection_change_password_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self.saved_connection_page,
                self.saved_connection_change_password_field,
            )
        )

    def _setup_scrollbar_signals(self) -> None:
        """Setup scrollbar synchronization signals."""
        self.listView.verticalScrollBar().valueChanged.connect(
            self._handle_scrollbar_change
        )
        self.verticalScrollBar.valueChanged.connect(self._handle_scrollbar_change)
        self.verticalScrollBar.valueChanged.connect(
            lambda value: self.listView.verticalScrollBar().setValue(value)
        )
        self.verticalScrollBar.show()

    def _configure_list_view_palette(self) -> None:
        """Configure the list view palette for transparency."""
        palette = QtGui.QPalette()

        for group in [
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorGroup.Disabled,
        ]:
            transparent = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
            transparent.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Button, transparent)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Window, transparent)

            no_brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            no_brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Base, no_brush)

            highlight = QtGui.QBrush(QtGui.QColor(0, 120, 215, 0))
            highlight.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Highlight, highlight)

            link = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
            link.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
            palette.setBrush(group, QtGui.QPalette.ColorRole.Link, link)

        self.listView.setPalette(palette)

    def _show_error_popup(self, message: str, timeout: int = 6000) -> None:
        """Show an error popup message."""
        self._popup.raise_()
        self._popup.new_message(
            message_type=Popup.MessageType.ERROR,
            message=message,
            timeout=timeout,
            userInput=False,
        )

    def _show_info_popup(self, message: str, timeout: int = 4000) -> None:
        """Show an info popup message."""
        self._popup.raise_()
        self._popup.new_message(
            message_type=Popup.MessageType.INFO,
            message=message,
            timeout=timeout,
            userInput=False,
        )

    def _show_warning_popup(self, message: str, timeout: int = 5000) -> None:
        """Show a warning popup message."""
        self._popup.raise_()
        self._popup.new_message(
            message_type=Popup.MessageType.WARNING,
            message=message,
            timeout=timeout,
            userInput=False,
        )

    def closeEvent(self, event: Optional[QtGui.QCloseEvent]) -> None:
        """Handle close event."""
        self._stop_all_timers()
        self._network_list_worker.stop_polling()
        super().closeEvent(event)

    def showEvent(self, event: Optional[QtGui.QShowEvent]) -> None:
        """Handle show event."""
        if self._networks:
            self._build_model_list()
        self._evaluate_network_state()
        super().showEvent(event)

    def _stop_all_timers(self) -> None:
        """Stop all active timers."""
        timers = [
            self._load_timer,
            self._status_check_timer,
            self._delayed_action_timer,
        ]
        for timer in timers:
            if timer.isActive():
                timer.stop()

    def _on_show_keyboard(
        self, panel: QtWidgets.QWidget, field: QtWidgets.QLineEdit
    ) -> None:
        """Show the on-screen keyboard for a field."""
        self._previous_panel = panel
        self._current_field = field
        self._qwerty.set_value(field.text())
        self.setCurrentIndex(self.indexOf(self._qwerty))

    def _on_qwerty_go_back(self) -> None:
        """Handle keyboard back button."""
        if self._previous_panel:
            self.setCurrentIndex(self.indexOf(self._previous_panel))

    def _on_qwerty_value_selected(self, value: str) -> None:
        """Handle keyboard value selection."""
        if self._previous_panel:
            self.setCurrentIndex(self.indexOf(self._previous_panel))
        if self._current_field:
            self._current_field.setText(value)

    def _set_loading_state(self, loading: bool) -> None:
        """Set loading state - controls loading widget visibility.

        This method ensures mutual exclusivity between
        loading widget, network details, and info box.
        """
        self.wifi_button.setEnabled(not loading)
        self.hotspot_button.setEnabled(not loading)

        if loading:
            self._is_connecting = True
            #
            # Hide ALL other elements first before showing loading
            # This prevents the dual panel visibility bug
            self._hide_all_info_elements()
            # Force UI update to ensure elements are hidden
            self.repaint()
            # Now show loading
            self.loadingwidget.setVisible(True)

            if self._load_timer.isActive():
                self._load_timer.stop()
            self._load_timer.start(LOAD_TIMEOUT_MS)
            if not self._status_check_timer.isActive():
                self._status_check_timer.start()
        else:
            self._is_connecting = False
            self._target_ssid = None
            # Just hide loading - caller decides what to show next
            self.loadingwidget.setVisible(False)

            if self._load_timer.isActive():
                self._load_timer.stop()
            if self._status_check_timer.isActive():
                self._status_check_timer.stop()

    def _show_network_details(self) -> None:
        """Show network details panel - HIDES everything else first."""
        # Hide everything else first to prevent dual panel
        self.loadingwidget.setVisible(False)
        self.mn_info_box.setVisible(False)
        # Force UI update
        self.repaint()

        # Then show only the details
        self.netlist_ip.setVisible(True)
        self.netlist_ssuid.setVisible(True)
        self.mn_info_seperator.setVisible(True)
        self.line_2.setVisible(True)
        self.netlist_strength.setVisible(True)
        self.netlist_strength_label.setVisible(True)
        self.line_3.setVisible(True)
        self.netlist_security.setVisible(True)
        self.netlist_security_label.setVisible(True)

    def _show_disconnected_message(self) -> None:
        """Show the disconnected state message - HIDES everything else first."""
        # Hide everything else first to prevent dual panel
        self.loadingwidget.setVisible(False)
        self._hide_network_detail_labels()
        # Force UI update
        self.repaint()

        # Then show info box
        self._configure_info_box_centered()
        self.mn_info_box.setVisible(True)
        self.mn_info_box.setText(
            "Network connection required.\n\nConnect to Wi-Fi\nor\nTurn on Hotspot"
        )

    def _hide_network_detail_labels(self) -> None:
        """Hide only the network detail labels (not loading or info box)."""
        self.netlist_ip.setVisible(False)
        self.netlist_ssuid.setVisible(False)
        self.mn_info_seperator.setVisible(False)
        self.line_2.setVisible(False)
        self.netlist_strength.setVisible(False)
        self.netlist_strength_label.setVisible(False)
        self.line_3.setVisible(False)
        self.netlist_security.setVisible(False)
        self.netlist_security_label.setVisible(False)

    def _check_connection_status(self) -> None:
        """Backup periodic check to detect successful connections."""
        if not self.loadingwidget.isVisible():
            if self._status_check_timer.isActive():
                self._status_check_timer.stop()
            return

        connectivity = self._sdbus_network.check_connectivity()
        is_connected = connectivity in ("FULL", "LIMITED")

        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button

        if hotspot_btn.state == hotspot_btn.State.ON:
            hotspot_ip = self._sdbus_network.get_device_ip_by_interface("wlan0")
            if hotspot_ip:
                logger.debug("Hotspot connection detected via status check")
                # Stop loading first, then show details
                self._set_loading_state(False)
                self._update_hotspot_display()
                self._show_network_details()
                return

        if wifi_btn.state == wifi_btn.State.ON:
            current_ssid = self._sdbus_network.get_current_ssid()

            if self._target_ssid:
                if current_ssid == self._target_ssid and is_connected:
                    logger.debug("Target Wi-Fi connection detected: %s", current_ssid)
                    # Stop loading first, then show details
                    self._set_loading_state(False)
                    self._update_wifi_display()
                    self._show_network_details()
                    return
            else:
                if current_ssid and is_connected:
                    logger.debug("Wi-Fi connection detected: %s", current_ssid)
                    # Stop loading first, then show details
                    self._set_loading_state(False)
                    self._update_wifi_display()
                    self._show_network_details()
                    return

    def _handle_load_timeout(self) -> None:
        """Handle connection timeout."""
        if not self.loadingwidget.isVisible():
            return

        connectivity = self._sdbus_network.check_connectivity()
        is_connected = connectivity in ("FULL", "LIMITED")

        wifi_btn = self.wifi_button
        hotspot_btn = self.hotspot_button

        # Final check if connection succeeded
        if wifi_btn.toggle_button.state == wifi_btn.toggle_button.State.ON:
            current_ssid = self._sdbus_network.get_current_ssid()

            if self._target_ssid:
                if current_ssid == self._target_ssid and is_connected:
                    logger.debug("Target connection succeeded on timeout check")
                    self._set_loading_state(False)
                    self._update_wifi_display()
                    self._show_network_details()
                    return
            else:
                if current_ssid and is_connected:
                    logger.debug("Connection succeeded on timeout check")
                    self._set_loading_state(False)
                    self._update_wifi_display()
                    self._show_network_details()
                    return

        elif hotspot_btn.toggle_button.state == hotspot_btn.toggle_button.State.ON:
            hotspot_ip = self._sdbus_network.get_device_ip_by_interface("wlan0")
            if hotspot_ip:
                logger.debug("Hotspot succeeded on timeout check")
                self._set_loading_state(False)
                self._update_hotspot_display()
                self._show_network_details()
                return

        # Connection actually failed
        self._is_connecting = False
        self._target_ssid = None
        self._set_loading_state(False)

        # Show error message
        self._hide_all_info_elements()
        self._configure_info_box_centered()
        self.mn_info_box.setVisible(True)
        self.mn_info_box.setText(self._get_timeout_message(wifi_btn, hotspot_btn))

        hotspot_btn.setEnabled(True)
        wifi_btn.setEnabled(True)

        self._show_error_popup("Connection timed out. Please try again.")

    def _get_timeout_message(self, wifi_btn, hotspot_btn) -> str:
        """Get appropriate timeout message based on state."""
        if wifi_btn.toggle_button.state == wifi_btn.toggle_button.State.ON:
            return "Wi-Fi Connection Failed.\nThe connection attempt\n timed out."
        elif hotspot_btn.toggle_button.state == hotspot_btn.toggle_button.State.ON:
            return "Hotspot Setup Failed.\nPlease restart the hotspot."
        else:
            return "Loading timed out.\nPlease check your connection\n and try again."

    def _configure_info_box_centered(self) -> None:
        """Configure info box for centered text."""
        self.mn_info_box.setWordWrap(True)
        self.mn_info_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def _clear_network_display(self) -> None:
        """Clear all network display labels."""
        self.netlist_ssuid.setText("")
        self.netlist_ip.setText("")
        self.netlist_strength.setText("")
        self.netlist_security.setText("")
        self._last_displayed_ssid = None

    @QtCore.pyqtSlot(object, name="stateChange")
    def _on_toggle_state(self, new_state) -> None:
        """Handle toggle button state change."""
        sender_button = self.sender()
        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button
        is_sender_now_on = new_state == sender_button.State.ON

        # Show loading IMMEDIATELY when turning something on
        if is_sender_now_on:
            self._set_loading_state(True)
            self.repaint()

        saved_networks = self._sdbus_network.get_saved_networks_with_for()

        if sender_button is wifi_btn:
            self._handle_wifi_toggle(is_sender_now_on, hotspot_btn, saved_networks)
        elif sender_button is hotspot_btn:
            self._handle_hotspot_toggle(is_sender_now_on, wifi_btn, saved_networks)

        # Handle both OFF
        if (
            hotspot_btn.state == hotspot_btn.State.OFF
            and wifi_btn.state == wifi_btn.State.OFF
        ):
            self._set_loading_state(False)
            self._show_disconnected_message()

    def _handle_wifi_toggle(
        self, is_on: bool, hotspot_btn, saved_networks: List[Dict]
    ) -> None:
        """Handle Wi-Fi toggle state change."""
        if not is_on:
            self._target_ssid = None
            return

        hotspot_btn.state = hotspot_btn.State.OFF
        self._sdbus_network.toggle_hotspot(False)

        # Check if already connected
        current_ssid = self._sdbus_network.get_current_ssid()
        connectivity = self._sdbus_network.check_connectivity()

        if current_ssid and connectivity == "FULL":
            # Already connected - show immediately
            self._target_ssid = current_ssid
            self._set_loading_state(False)
            self._update_wifi_display()
            self._show_network_details()
            return

        # Filter wifi networks (not hotspots)
        wifi_networks = [
            n for n in saved_networks if "ap" not in str(n.get("mode", ""))
        ]

        if not wifi_networks:
            self._set_loading_state(False)
            self._show_warning_popup(
                "No saved Wi-Fi networks. Please add a network first."
            )
            self._show_disconnected_message()
            return

        try:
            ssid = wifi_networks[0]["ssid"]
            self._target_ssid = ssid
            self._sdbus_network.connect_network(str(ssid))
        except Exception as e:
            logger.error("Error when turning ON wifi: %s", e)
            self._set_loading_state(False)
            self._show_error_popup("Failed to connect to Wi-Fi")

    def _handle_hotspot_toggle(
        self, is_on: bool, wifi_btn, saved_networks: List[Dict]
    ) -> None:
        """Handle hotspot toggle state change."""
        if not is_on:
            self._target_ssid = None
            return

        wifi_btn.state = wifi_btn.State.OFF
        self._target_ssid = None

        new_hotspot_name = self.hotspot_name_input_field.text() or "PrinterHotspot"
        new_hotspot_password = self.hotspot_password_input_field.text() or "123456789"

        # Use QTimer to defer async operations
        def setup_hotspot():
            try:
                self._sdbus_network.create_hotspot(
                    new_hotspot_name, new_hotspot_password
                )
                self._sdbus_network.toggle_hotspot(True)
            except Exception as e:
                logger.error("Error creating/activating hotspot: %s", e)
                self._show_error_popup("Failed to start hotspot")
                self._set_loading_state(False)

        QtCore.QTimer.singleShot(100, setup_hotspot)

    @QtCore.pyqtSlot(str, name="nm-state-changed")
    def _evaluate_network_state(self, nm_state: str = "") -> None:
        """Evaluate and update network state."""
        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button

        state = nm_state or self._sdbus_network.check_nm_state()
        if not state:
            return

        if self._is_first_run:
            self._handle_first_run_state()
            self._is_first_run = False
            return

        if not self._sdbus_network.check_wifi_interface():
            return

        # Handle both OFF first
        if (
            wifi_btn.state == wifi_btn.State.OFF
            and hotspot_btn.state == hotspot_btn.State.OFF
        ):
            self._sdbus_network.disconnect_network()
            self._clear_network_display()
            self._set_loading_state(False)
            self._show_disconnected_message()
            return

        connectivity = self._sdbus_network.check_connectivity()
        is_connected = connectivity in ("FULL", "LIMITED")

        # Handle hotspot
        if hotspot_btn.state == hotspot_btn.State.ON:
            hotspot_ip = self._sdbus_network.get_device_ip_by_interface("wlan0")
            if hotspot_ip or is_connected:
                # Stop loading first, then update display, then show details
                self._set_loading_state(False)
                self._update_hotspot_display()
                self._show_network_details()
                self.wifi_button.setEnabled(True)
                self.hotspot_button.setEnabled(True)
            return

        # Handle wifi
        if wifi_btn.state == wifi_btn.State.ON:
            current_ssid = self._sdbus_network.get_current_ssid()

            if self._target_ssid:
                if current_ssid == self._target_ssid and is_connected:
                    logger.debug("Connected to target: %s", current_ssid)
                    # Stop loading first, then update display, then show details
                    self._set_loading_state(False)
                    self._update_wifi_display()
                    self._show_network_details()
                    self.wifi_button.setEnabled(True)
                    self.hotspot_button.setEnabled(True)
            else:
                if current_ssid and is_connected:
                    # Stop loading first, then update display, then show details
                    self._set_loading_state(False)
                    self._update_wifi_display()
                    self._show_network_details()
                    self.wifi_button.setEnabled(True)
                    self.hotspot_button.setEnabled(True)
        self.update()

    def _handle_first_run_state(self) -> None:
        """Handle initial state on first run."""
        saved_networks = self._sdbus_network.get_saved_networks_with_for()

        old_hotspot = next(
            (n for n in saved_networks if "ap" in str(n.get("mode", ""))), None
        )
        if old_hotspot:
            self.hotspot_name_input_field.setText(old_hotspot["ssid"])

        connectivity = self._sdbus_network.check_connectivity()
        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button
        current_ssid = self._sdbus_network.get_current_ssid()

        self._is_connecting = False
        self.loadingwidget.setVisible(False)

        with QtCore.QSignalBlocker(wifi_btn), QtCore.QSignalBlocker(hotspot_btn):
            if connectivity == "FULL" and current_ssid:
                wifi_btn.state = wifi_btn.State.ON
                hotspot_btn.state = hotspot_btn.State.OFF
                self._update_wifi_display()
                self._show_network_details()
                self.wifi_button.setEnabled(True)
                self.hotspot_button.setEnabled(True)
            elif connectivity == "LIMITED":
                wifi_btn.state = wifi_btn.State.OFF
                hotspot_btn.state = hotspot_btn.State.ON
                self._update_hotspot_display()
                self._show_network_details()
                self.wifi_button.setEnabled(True)
                self.hotspot_button.setEnabled(True)
            else:
                wifi_btn.state = wifi_btn.State.OFF
                hotspot_btn.state = hotspot_btn.State.OFF
                self._clear_network_display()
                self._show_disconnected_message()
                self.wifi_button.setEnabled(True)
                self.hotspot_button.setEnabled(True)

    def _update_hotspot_display(self) -> None:
        """Update display for hotspot mode."""
        ipv4_addr = self._sdbus_network.get_device_ip_by_interface("wlan0")
        if not ipv4_addr:
            ipv4_addr = self._sdbus_network.get_current_ip_addr()

        hotspot_name = self.hotspot_name_input_field.text()
        if not hotspot_name:
            hotspot_name = self._sdbus_network.hotspot_ssid or "Hotspot"
            self.hotspot_name_input_field.setText(hotspot_name)

        self.netlist_ssuid.setText(hotspot_name)
        # Handle empty IP properly
        if ipv4_addr and ipv4_addr.strip():
            self.netlist_ip.setText(f"IP: {ipv4_addr}")
        else:
            self.netlist_ip.setText("IP: Obtaining...")
        self.netlist_strength.setText("--")
        self.netlist_security.setText("WPA2")
        self._last_displayed_ssid = hotspot_name

    def _update_wifi_display(self) -> None:
        """Update display for wifi connection."""
        current_ssid = self._sdbus_network.get_current_ssid()

        if current_ssid:
            ipv4_addr = self._sdbus_network.get_current_ip_addr()
            sec_type = self._sdbus_network.get_security_type_by_ssid(current_ssid)
            signal_strength = self._sdbus_network.get_connection_signal_by_ssid(
                current_ssid
            )

            self.netlist_ssuid.setText(current_ssid)
            # Handle empty IP properly
            if ipv4_addr and ipv4_addr.strip():
                self.netlist_ip.setText(f"IP: {ipv4_addr}")
            else:
                self.netlist_ip.setText("IP: Obtaining...")
            self.netlist_security.setText(str(sec_type or "OPEN").upper())
            self.netlist_strength.setText(
                f"{signal_strength}%"
                if signal_strength and signal_strength != -1
                else "--"
            )
            self._last_displayed_ssid = current_ssid
        else:
            self._clear_network_display()

    @QtCore.pyqtSlot(str, name="delete-network")
    def _delete_network(self, ssid: str) -> None:
        """Delete a network."""
        try:
            self._sdbus_network.delete_network(ssid=ssid)
        except Exception as e:
            logger.error("Failed to delete network %s: %s", ssid, e)
            self._show_error_popup("Failed to delete network")

    @QtCore.pyqtSlot(name="rescan-networks")
    def _rescan_networks(self) -> None:
        """Trigger network rescan."""
        self._sdbus_network.rescan_networks()

    @QtCore.pyqtSlot(name="add-network")
    def _add_network(self) -> None:
        """Add a new network."""
        self.add_network_validation_button.setEnabled(False)
        self.add_network_validation_button.update()

        password = self.add_network_password_field.text()
        ssid = self.add_network_network_label.text()

        if not password and not self._current_network_is_open:
            self._show_error_popup("Password field cannot be empty.")
            self.add_network_validation_button.setEnabled(True)
            return

        result = self._sdbus_network.add_wifi_network(ssid=ssid, psk=password)
        self.add_network_password_field.clear()

        if result is None:
            self._handle_failed_network_add("Failed to add network")
            return

        error_msg = result.get("error", "") if isinstance(result, dict) else ""

        if not error_msg:
            self._handle_successful_network_add(ssid)
        else:
            self._handle_failed_network_add(error_msg)

    def _handle_successful_network_add(self, ssid: str) -> None:
        """Handle successful network addition."""
        self._target_ssid = ssid
        self._set_loading_state(True)
        self.setCurrentIndex(self.indexOf(self.main_network_page))

        wifi_btn = self.wifi_button.toggle_button
        hotspot_btn = self.hotspot_button.toggle_button
        with QtCore.QSignalBlocker(wifi_btn), QtCore.QSignalBlocker(hotspot_btn):
            wifi_btn.state = wifi_btn.State.ON
            hotspot_btn.state = hotspot_btn.State.OFF

        self._schedule_delayed_action(
            self._network_list_worker.build, NETWORK_CONNECT_DELAY_MS
        )

        def connect_and_refresh():
            try:
                self._sdbus_network.connect_network(ssid)
            except Exception as e:
                logger.error("Failed to connect to %s: %s", ssid, e)
                self._show_error_popup(f"Failed to connect to {ssid}")
                self._set_loading_state(False)

        QtCore.QTimer.singleShot(NETWORK_CONNECT_DELAY_MS, connect_and_refresh)

        self.add_network_validation_button.setEnabled(True)
        self.wifi_button.setEnabled(False)
        self.hotspot_button.setEnabled(False)
        self.add_network_validation_button.update()

    def _handle_failed_network_add(self, error_msg: str) -> None:
        """Handle failed network addition."""
        logger.error(error_msg)
        error_messages = {
            "Invalid password": "Invalid password. Please try again",
            "Network connection properties error": (
                "Network connection properties error. Please try again"
            ),
            "Permission Denied": "Permission Denied. Please try again",
        }

        message = error_messages.get(
            error_msg, "Error while adding network. Please try again"
        )

        self.add_network_validation_button.setEnabled(True)
        self.add_network_validation_button.update()
        self._show_error_popup(message)

    def _on_save_network_settings(self) -> None:
        """Save network settings."""
        self._update_network(
            ssid=self.saved_connection_network_name.text(),
            password=self.saved_connection_change_password_field.text(),
            new_ssid=None,
        )

    def _update_network(
        self,
        ssid: str,
        password: Optional[str],
        new_ssid: Optional[str],
    ) -> None:
        """Update network settings."""
        if not self._sdbus_network.is_known(ssid):
            return

        priority = self._get_selected_priority()

        try:
            self._sdbus_network.update_connection_settings(
                ssid=ssid, password=password, new_ssid=new_ssid, priority=priority
            )
        except Exception as e:
            logger.error("Failed to update network settings: %s", e)
            self._show_error_popup("Failed to update network settings")

        self.setCurrentIndex(self.indexOf(self.network_list_page))

    def _get_selected_priority(self) -> int:
        """Get selected priority from radio buttons."""
        checked_btn = self.priority_btn_group.checkedButton()

        if checked_btn == self.high_priority_btn:
            return PRIORITY_HIGH
        elif checked_btn == self.low_priority_btn:
            return PRIORITY_LOW
        else:
            return PRIORITY_MEDIUM

    def _on_saved_wifi_option_selected(self) -> None:
        """Handle saved wifi option selection."""
        sender = self.sender()

        wifi_toggle = self.wifi_button.toggle_button
        hotspot_toggle = self.hotspot_button.toggle_button

        with QtCore.QSignalBlocker(wifi_toggle), QtCore.QSignalBlocker(hotspot_toggle):
            wifi_toggle.state = wifi_toggle.State.ON
            hotspot_toggle.state = hotspot_toggle.State.OFF

        ssid = self.saved_connection_network_name.text()

        if sender == self.network_delete_btn:
            self._handle_network_delete(ssid)
        elif sender == self.network_activate_btn:
            self._handle_network_activate(ssid)

    def _handle_network_delete(self, ssid: str) -> None:
        """Handle network deletion."""
        try:
            self._sdbus_network.delete_network(ssid)
            if ssid in self._networks:
                del self._networks[ssid]
            self.setCurrentIndex(self.indexOf(self.network_list_page))
            self._build_model_list()
            self._network_list_worker.build()
            self._show_info_popup(f"Network '{ssid}' deleted")
        except Exception as e:
            logger.error("Failed to delete network %s: %s", ssid, e)
            self._show_error_popup("Failed to delete network")

    def _handle_network_activate(self, ssid: str) -> None:
        """Handle network activation."""
        self._target_ssid = ssid
        # Show loading IMMEDIATELY
        self._set_loading_state(True)
        self.repaint()

        self.setCurrentIndex(self.indexOf(self.main_network_page))

        try:
            self._sdbus_network.connect_network(ssid)
        except Exception as e:
            logger.error("Failed to connect to %s: %s", ssid, e)
            self._set_loading_state(False)
            self._show_disconnected_message()
            self._show_error_popup("Failed to connect to network")

    @QtCore.pyqtSlot(list, name="finished-network-list-build")
    def _handle_network_list(self, data: List[tuple]) -> None:
        """Handle network list build completion."""
        self._networks.clear()
        hotspot_ssid = self._sdbus_network.hotspot_ssid

        for entry in data:
            # Handle different tuple lengths
            if len(entry) >= 6:
                ssid, signal, status, is_open, is_saved, is_hidden = entry
            elif len(entry) >= 5:
                ssid, signal, status, is_open, is_saved = entry
                is_hidden = self._is_hidden_ssid(ssid)
            elif len(entry) >= 4:
                ssid, signal, status, is_open = entry
                is_saved = status in ("Active", "Saved")
                is_hidden = self._is_hidden_ssid(ssid)
            else:
                ssid, signal, status = entry[0], entry[1], entry[2]
                is_open = status == "Open"
                is_saved = status in ("Active", "Saved")
                is_hidden = self._is_hidden_ssid(ssid)

            if ssid == hotspot_ssid:
                continue

            self._networks[ssid] = NetworkInfo(
                signal=signal,
                status=status,
                is_open=is_open,
                is_saved=is_saved,
                is_hidden=is_hidden,
            )

        self._build_model_list()

        # Update main panel if connected
        if self._last_displayed_ssid and self._last_displayed_ssid in self._networks:
            network_info = self._networks[self._last_displayed_ssid]
            self.netlist_strength.setText(
                f"{network_info.signal}%" if network_info.signal != -1 else "--"
            )

    def _is_hidden_ssid(self, ssid: str) -> bool:
        """Check if an SSID indicates a hidden network."""
        if ssid is None:
            return True
        ssid_stripped = ssid.strip()
        ssid_lower = ssid_stripped.lower()
        # Check for empty, unknown, or hidden indicators
        return (
            ssid_stripped == ""
            or ssid_lower == "unknown"
            or ssid_lower == "<hidden>"
            or ssid_lower == "hidden"
            or not ssid_stripped
        )

    def _build_model_list(self) -> None:
        """Build the network list model."""
        self.listView.blockSignals(True)
        self._reset_view_model()

        saved_networks = []
        unsaved_networks = []

        for ssid, info in self._networks.items():
            if info.is_saved:
                saved_networks.append((ssid, info))
            else:
                unsaved_networks.append((ssid, info))

        saved_networks.sort(key=lambda x: -x[1].signal)
        unsaved_networks.sort(key=lambda x: -x[1].signal)

        for ssid, info in saved_networks:
            self._add_network_entry(
                ssid=ssid,
                signal=info.signal,
                status=info.status,
                is_open=info.is_open,
                is_hidden=info.is_hidden,
            )

        if saved_networks and unsaved_networks:
            self._add_separator_entry()

        for ssid, info in unsaved_networks:
            self._add_network_entry(
                ssid=ssid,
                signal=info.signal,
                status=info.status,
                is_open=info.is_open,
                is_hidden=info.is_hidden,
            )

        # Add "Connect to Hidden Network" entry at the end
        self._add_hidden_network_entry()

        self._sync_scrollbar()
        self.listView.blockSignals(False)
        self.listView.update()

    def _reset_view_model(self) -> None:
        """Reset the view model."""
        self._model.clear()
        self._entry_delegate.clear()

    def _add_separator_entry(self) -> None:
        """Add a separator entry to the list."""
        item = ListItem(
            text="",
            left_icon=None,
            right_text="",
            right_icon=None,
            selected=False,
            allow_check=False,
            _lfontsize=17,
            _rfontsize=12,
            height=20,
            not_clickable=True,
        )
        self._model.add_item(item)

    def _add_hidden_network_entry(self) -> None:
        """Add a 'Connect to Hidden Network' entry at the end of the list."""
        wifi_pixmap = QtGui.QPixmap(":/network/media/btn_icons/0bar_wifi_protected.svg")
        item = ListItem(
            text="Connect to Hidden Network...",
            left_icon=wifi_pixmap,
            right_text="",
            right_icon=self._right_arrow_icon,
            selected=False,
            allow_check=False,
            _lfontsize=17,
            _rfontsize=12,
            height=80,
            not_clickable=False,
        )
        self._model.add_item(item)

    def _add_network_entry(
        self,
        ssid: str,
        signal: int,
        status: str,
        is_open: bool = False,
        is_hidden: bool = False,
    ) -> None:
        """Add a network entry to the list."""
        wifi_pixmap = self._icon_provider.get_pixmap(signal=signal, status=status)

        # Skipping hidden networks
        # Check both the is_hidden flag AND the ssid content
        if is_hidden or self._is_hidden_ssid(ssid):
            return
        display_ssid = ssid

        item = ListItem(
            text=display_ssid,
            left_icon=wifi_pixmap,
            right_text=status,
            right_icon=self._right_arrow_icon,
            selected=False,
            allow_check=False,
            _lfontsize=17,
            _rfontsize=12,
            height=80,
            not_clickable=False,  # All entries are clickable
        )
        self._model.add_item(item)

    @QtCore.pyqtSlot(ListItem, name="ssid-item-clicked")
    def _on_ssid_item_clicked(self, item: ListItem) -> None:
        """Handle network item click."""
        ssid = item.text

        # Handle hidden network entries - check for various hidden indicators
        if (
            self._is_hidden_ssid(ssid)
            or ssid == "Hidden Network"
            or ssid == "Connect to Hidden Network..."
        ):
            self.setCurrentIndex(self.indexOf(self.hidden_network_page))
            return

        network_info = self._networks.get(ssid)
        if network_info is None:
            # Also check if it might be a hidden network in the _networks dict
            # Hidden networks might have empty or UNKNOWN as key
            for key, info in self._networks.items():
                if info.is_hidden:
                    self.setCurrentIndex(self.indexOf(self.hidden_network_page))
                    return
            return

        if network_info.is_saved:
            saved_networks = self._sdbus_network.get_saved_networks_with_for()
            self._show_saved_network_page(ssid, saved_networks)
        else:
            self._show_add_network_page(ssid, is_open=network_info.is_open)

    def _show_saved_network_page(self, ssid: str, saved_networks: List[Dict]) -> None:
        """Show the saved network page."""
        self.saved_connection_network_name.setText(str(ssid))
        self.snd_name.setText(str(ssid))
        self._current_network_ssid = ssid  # Track for priority lookup

        # Fetch priority from get_saved_networks() which includes priority
        # get_saved_networks_with_for() does NOT include priority field
        priority = None
        try:
            full_saved_networks = self._sdbus_network.get_saved_networks()
            if full_saved_networks:
                for net in full_saved_networks:
                    if net.get("ssid") == ssid:
                        priority = net.get("priority")
                        logger.debug("Found priority %s for network %s", priority, ssid)
                        break
        except Exception as e:
            logger.error("Failed to get priority for %s: %s", ssid, e)

        self._set_priority_button(priority)

        network_info = self._networks.get(ssid)
        if network_info:
            signal_text = (
                f"{network_info.signal}%" if network_info.signal >= 0 else "--%"
            )
            self.saved_connection_signal_strength_info_frame.setText(signal_text)

            if network_info.is_open:
                self.saved_connection_security_type_info_label.setText("OPEN")
            else:
                sec_type = self._sdbus_network.get_security_type_by_ssid(ssid)
                self.saved_connection_security_type_info_label.setText(
                    str(sec_type or "WPA").upper()
                )
        else:
            self.saved_connection_signal_strength_info_frame.setText("--%")
            self.saved_connection_security_type_info_label.setText("--")

        current_ssid = self._sdbus_network.get_current_ssid()
        if current_ssid != ssid:
            self.network_activate_btn.setDisabled(False)
            self.sn_info.setText("Saved Network")
        else:
            self.network_activate_btn.setDisabled(True)
            self.sn_info.setText("Active Network")

        self.setCurrentIndex(self.indexOf(self.saved_connection_page))
        self.frame.repaint()

    def _set_priority_button(self, priority: Optional[int]) -> None:
        """Set the priority button based on value.

        Block signals while setting to prevent unwanted triggers.
        """
        # Block signals to prevent any side effects
        with (
            QtCore.QSignalBlocker(self.high_priority_btn),
            QtCore.QSignalBlocker(self.med_priority_btn),
            QtCore.QSignalBlocker(self.low_priority_btn),
        ):
            # Uncheck all first
            self.high_priority_btn.setChecked(False)
            self.med_priority_btn.setChecked(False)
            self.low_priority_btn.setChecked(False)

            # Then check the correct one
            if priority is not None:
                if priority >= PRIORITY_HIGH:
                    self.high_priority_btn.setChecked(True)
                elif priority <= PRIORITY_LOW:
                    self.low_priority_btn.setChecked(True)
                else:
                    self.med_priority_btn.setChecked(True)
            else:
                # Default to medium if no priority set
                self.med_priority_btn.setChecked(True)

    def _show_add_network_page(self, ssid: str, is_open: bool = False) -> None:
        """Show the add network page."""
        self._current_network_is_open = is_open
        self._current_network_is_hidden = False
        self.add_network_network_label.setText(str(ssid))
        self.setCurrentIndex(self.indexOf(self.add_network_page))

    def _handle_scrollbar_change(self, value: int) -> None:
        """Handle scrollbar value change."""
        self.verticalScrollBar.blockSignals(True)
        self.verticalScrollBar.setValue(value)
        self.verticalScrollBar.blockSignals(False)

    def _sync_scrollbar(self) -> None:
        """Synchronize scrollbar with list view."""
        list_scrollbar = self.listView.verticalScrollBar()
        self.verticalScrollBar.setMinimum(list_scrollbar.minimum())
        self.verticalScrollBar.setMaximum(list_scrollbar.maximum())
        self.verticalScrollBar.setPageStep(list_scrollbar.pageStep())

    def _schedule_delayed_action(self, callback: Callable, delay_ms: int) -> None:
        """Schedule a delayed action."""
        try:
            self._delayed_action_timer.timeout.disconnect()
        except TypeError:
            pass

        self._delayed_action_timer.timeout.connect(callback)
        self._delayed_action_timer.start(delay_ms)

    def close(self) -> bool:
        """Close the window."""
        self._network_list_worker.stop_polling()
        self._sdbus_network.close()
        return super().close()

    def setCurrentIndex(self, index: int) -> None:
        """Set the current page index."""
        if not self.isVisible():
            return

        if index == self.indexOf(self.add_network_page):
            self._setup_add_network_page_state()
        elif index == self.indexOf(self.saved_connection_page):
            self._setup_saved_connection_page_state()

        self.repaint()
        super().setCurrentIndex(index)

    def _setup_add_network_page_state(self) -> None:
        """Setup add network page state."""
        self.add_network_password_field.clear()

        if self._current_network_is_open:
            self.frame_2.setVisible(False)
            self.add_network_validation_button.setText("Connect")
        else:
            self.frame_2.setVisible(True)
            self.add_network_password_field.setPlaceholderText(
                "Insert password here, press enter when finished."
            )
            self.add_network_validation_button.setText("Activate")

    def _setup_saved_connection_page_state(self) -> None:
        """Setup saved connection page state."""
        self.saved_connection_change_password_field.clear()
        self.saved_connection_change_password_field.setPlaceholderText(
            "Change network password"
        )

    def setProperty(self, name: str, value: Any) -> bool:
        """Set a property value."""
        if name == "backgroundPixmap":
            self._background = value
        return super().setProperty(name, value)

    @QtCore.pyqtSlot(name="call-network-panel")
    def show_network_panel(self) -> None:
        """Show the network panel."""
        if not self.parent():
            return

        self.setCurrentIndex(self.indexOf(self.network_list_page))
        parent_size = self.parent().size()
        self.setGeometry(0, 0, parent_size.width(), parent_size.height())
        self.updateGeometry()
        self.repaint()
        self.show()
