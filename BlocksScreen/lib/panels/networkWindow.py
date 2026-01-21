import logging
import socket
import threading
from functools import partial
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
)

import psutil
from lib.network import SdbusNetworkManagerAsync
from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard
from lib.panels.widgets.popupDialogWidget import Popup
from lib.ui.wifiConnectivityWindow_ui import Ui_wifi_stacked_page
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal

logger = logging.getLogger("logs/BlocksScreen.log")


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


class NetworkInfo(NamedTuple):
    signal: int
    status: str
    is_open: bool = False
    is_saved: bool = False


class NetworkScanResult(NamedTuple):
    ssid: str
    signal: int
    status: str
    is_open: bool = False


class NetworkScanRunnable(QRunnable):

    class Signals(QObject):
        scan_results = pyqtSignal(dict, name="scan-results")
        finished_network_list_build = pyqtSignal(list, name="finished-network-list-build")
        error = pyqtSignal(str)

    def __init__(self, nm: SdbusNetworkManagerAsync) -> None:
        super().__init__()
        self._nm = nm
        self.signals = NetworkScanRunnable.Signals()

    def run(self) -> None:
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
        if self._nm.check_wifi_interface():
            return self._nm.get_available_networks() or {}
        return {}

    def _build_data_dict(
        self,
        available: Dict[str, Dict],
        saved_ssids: List[str]
    ) -> Dict[str, Dict]:
        data_dict: Dict[str, Dict] = {}
        for ssid, props in available.items():
            signal = int(props.get("signal_level", 0))
            sec_tuple = props.get("security", (0, 0, 0))
            caps_value = sec_tuple[2] if len(sec_tuple) > 2 else 0
            is_open = (caps_value & PRIVACY_BIT) == 0
            data_dict[ssid] = {
                "signal_level": signal,
                "is_saved": ssid in saved_ssids,
                "is_open": is_open,
            }
        return data_dict

    def _build_network_list(self, data_dict: Dict[str, Dict]) -> List[tuple]:
        current_ssid = self._nm.get_current_ssid()

        saved_nets = [
            (ssid, info["signal_level"], info["is_open"])
            for ssid, info in data_dict.items()
            if info["is_saved"]
        ]
        unsaved_nets = [
            (ssid, info["signal_level"], info["is_open"])
            for ssid, info in data_dict.items()
            if not info["is_saved"]
        ]

        saved_nets.sort(key=lambda x: -x[1])
        unsaved_nets.sort(key=lambda x: -x[1])

        items: List[tuple] = []

        for ssid, signal, is_open in saved_nets:
            status = "Active" if ssid == current_ssid else "Saved"
            items.append((ssid, signal, status, is_open, True))

        for ssid, signal, is_open in unsaved_nets:
            status = "Open" if is_open else "Protected"
            items.append((ssid, signal, status, is_open, False))

        return items


class BuildNetworkList(QtCore.QObject):

    scan_results = pyqtSignal(dict, name="scan-results")
    finished_network_list_build = pyqtSignal(list, name="finished-network-list-build")
    error = pyqtSignal(str)

    def __init__(
        self,
        nm: SdbusNetworkManagerAsync,
        poll_interval_ms: int = DEFAULT_POLL_INTERVAL_MS,
    ) -> None:
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
        self._schedule_next_scan()

    def stop_polling(self) -> None:
        self._timer.stop()

    def build(self) -> None:
        self._do_scan()

    def _schedule_next_scan(self) -> None:
        self._timer.start(self._poll_interval_ms)

    def _on_task_finished(self, items: List) -> None:
        with self._scan_lock:
            self._is_scanning = False
        self.finished_network_list_build.emit(items)
        self._schedule_next_scan()

    def _on_task_scan_results(self, data_dict: Dict) -> None:
        self.scan_results.emit(data_dict)

    def _on_task_error(self, err: str) -> None:
        with self._scan_lock:
            self._is_scanning = False
        self.error.emit(err)
        self._schedule_next_scan()

    def _do_scan(self) -> None:
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

    def __init__(self) -> None:
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
        bars = self._signal_to_bars(signal)
        is_protected = status == "Protected"
        key = (bars, is_protected)
        path = self._paths.get(key, self._paths[(0, False)])
        return QtGui.QPixmap(path)

    @staticmethod
    def _signal_to_bars(signal: int) -> int:
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

    request_network_scan = pyqtSignal(name="scan-network")
    new_ip_signal = pyqtSignal(str, name="ip-address-change")
    get_hotspot_ssid = pyqtSignal(str, name="hotspot-ssid-name")
    delete_network_signal = pyqtSignal(str, name="delete-network")

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None, /) -> None:
        super().__init__(parent) if parent else super().__init__()

        self._init_instance_variables()
        self._init_ui()
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
        self._set_loading_state(False)

    def _init_instance_variables(self) -> None:
        self._icon_provider = WifiIconProvider()
        self._ongoing_update = False
        self._is_first_run = True
        self._networks: Dict[str, NetworkInfo] = {}
        self._previous_panel: Optional[QtWidgets.QWidget] = None
        self._current_field: Optional[QtWidgets.QLineEdit] = None
        self._cached_hotspot_ip = ""
        self._current_network_is_open = False

    def _init_ui(self) -> None:
        self._panel = Ui_wifi_stacked_page()
        self._panel.setupUi(self)
        self._popup = Popup(self)
        self._sdbus_network = SdbusNetworkManagerAsync()
        self._right_arrow_icon = QtGui.QPixmap(
            ":/arrow_icons/media/btn_icons/right_arrow.svg"
        )

    def _init_timers(self) -> None:
        self._status_check_timer = QtCore.QTimer(self)
        self._status_check_timer.setInterval(STATUS_CHECK_INTERVAL_MS)

        self._delayed_action_timer = QtCore.QTimer(self)
        self._delayed_action_timer.setSingleShot(True)

        self._load_timer = QtCore.QTimer(self)
        self._load_timer.setSingleShot(True)
        self._load_timer.timeout.connect(self._handle_load_timeout)

    def _init_model_view(self) -> None:
        self._model = EntryListModel()
        self._model.setParent(self._panel.listView)
        self._entry_delegate = EntryDelegate()
        self._panel.listView.setModel(self._model)
        self._panel.listView.setItemDelegate(self._entry_delegate)
        self._entry_delegate.item_selected.connect(self._on_ssid_item_clicked)
        self._configure_list_view_palette()

    def _init_network_worker(self) -> None:
        self._network_list_worker = BuildNetworkList(
            nm=self._sdbus_network,
            poll_interval_ms=DEFAULT_POLL_INTERVAL_MS
        )
        self._network_list_worker.finished_network_list_build.connect(
            self._handle_network_list
        )
        self._network_list_worker.start_polling()
        self._panel.rescan_button.clicked.connect(self._network_list_worker.build)

    def _setup_navigation_signals(self) -> None:
        self._panel.wifi_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self._panel.network_list_page))
        )
        self._panel.hotspot_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self._panel.hotspot_page))
        )
        self._panel.nl_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self._panel.main_network_page))
        )
        self._panel.network_backButton.clicked.connect(self.hide)

        self._panel.add_network_page_backButton.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self._panel.network_list_page))
        )

        self._panel.saved_connection_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self._panel.network_list_page))
        )
        self._panel.snd_back.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self._panel.saved_connection_page))
        )
        self._panel.network_details_btn.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self._panel.saved_details_page))
        )

        self._panel.hotspot_back_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self._panel.main_network_page))
        )
        self._panel.hotspot_change_confirm.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self._panel.main_network_page))
        )

    def _setup_action_signals(self) -> None:
        self._sdbus_network.nm_state_change.connect(self._evaluate_network_state)
        self.request_network_scan.connect(self._rescan_networks)
        self.delete_network_signal.connect(self._delete_network)

        self._panel.add_network_validation_button.clicked.connect(self._add_network)

        self._panel.snd_back.clicked.connect(self._on_save_network_settings)
        self._panel.network_activate_btn.clicked.connect(self._on_saved_wifi_option_selected)
        self._panel.network_delete_btn.clicked.connect(self._on_saved_wifi_option_selected)

    def _setup_toggle_signals(self) -> None:
        self._panel.wifi_button.toggle_button.stateChange.connect(self._on_toggle_state)
        self._panel.hotspot_button.toggle_button.stateChange.connect(self._on_toggle_state)

    def _setup_password_visibility_signals(self) -> None:
        self._setup_password_visibility_toggle(
            self._panel.add_network_password_view,
            self._panel.add_network_password_field,
        )
        self._setup_password_visibility_toggle(
            self._panel.saved_connection_change_password_view,
            self._panel.saved_connection_change_password_field,
        )

        self._panel.hotspot_password_input_field.setHidden(True)
        self._panel.hotspot_password_view_button.pressed.connect(
            partial(self._panel.hotspot_password_input_field.setHidden, False)
        )
        self._panel.hotspot_password_view_button.released.connect(
            partial(self._panel.hotspot_password_input_field.setHidden, True)
        )

        see_icon = QtGui.QPixmap(":/ui/media/btn_icons/see.svg")
        unsee_icon = QtGui.QPixmap(":/ui/media/btn_icons/unsee.svg")
        self._panel.hotspot_password_view_button.pressed.connect(
            lambda: self._panel.hotspot_password_view_button.setPixmap(see_icon)
        )
        self._panel.hotspot_password_view_button.released.connect(
            lambda: self._panel.hotspot_password_view_button.setPixmap(unsee_icon)
        )

    def _setup_password_visibility_toggle(
        self,
        view_button: QtWidgets.QWidget,
        password_field: QtWidgets.QLineEdit
    ) -> None:
        see_icon = QtGui.QPixmap(":/ui/media/btn_icons/see.svg")
        unsee_icon = QtGui.QPixmap(":/ui/media/btn_icons/unsee.svg")

        view_button.pressed.connect(
            lambda: password_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        )
        view_button.released.connect(
            lambda: password_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        )
        view_button.pressed.connect(lambda: view_button.setPixmap(see_icon))
        view_button.released.connect(lambda: view_button.setPixmap(unsee_icon))

    def _setup_icons(self) -> None:
        self._panel.hotspot_button.setPixmap(
            QtGui.QPixmap(":/network/media/btn_icons/hotspot.svg")
        )
        self._panel.wifi_button.setPixmap(
            QtGui.QPixmap(":/network/media/btn_icons/wifi_config.svg")
        )
        self._panel.network_delete_btn.setPixmap(
            QtGui.QPixmap(":/ui/media/btn_icons/garbage-icon.svg")
        )
        self._panel.network_activate_btn.setPixmap(
            QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self._panel.network_details_btn.setPixmap(
            QtGui.QPixmap(":/ui/media/btn_icons/printer_settings.svg")
        )

    def _setup_input_fields(self) -> None:
        self._panel.add_network_password_field.setCursor(QtCore.Qt.CursorShape.BlankCursor)
        self._panel.hotspot_name_input_field.setCursor(QtCore.Qt.CursorShape.BlankCursor)
        self._panel.hotspot_password_input_field.setCursor(QtCore.Qt.CursorShape.BlankCursor)

        self._panel.hotspot_password_input_field.setPlaceholderText("Defaults to: 123456789")
        self._panel.hotspot_name_input_field.setText(
            str(self._sdbus_network.get_hotspot_ssid())
        )
        self._panel.hotspot_password_input_field.setText(
            str(self._sdbus_network.hotspot_password)
        )

    def _setup_keyboard(self) -> None:
        self._qwerty = CustomQwertyKeyboard(self)
        self.addWidget(self._qwerty)
        self._qwerty.value_selected.connect(self._on_qwerty_value_selected)
        self._qwerty.request_back.connect(self._on_qwerty_go_back)

        self._panel.add_network_password_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self._panel.add_network_page,
                self._panel.add_network_password_field
            )
        )
        self._panel.hotspot_password_input_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self._panel.hotspot_page,
                self._panel.hotspot_password_input_field
            )
        )
        self._panel.hotspot_name_input_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self._panel.hotspot_page,
                self._panel.hotspot_name_input_field
            )
        )
        self._panel.saved_connection_change_password_field.clicked.connect(
            lambda: self._on_show_keyboard(
                self._panel.saved_connection_page,
                self._panel.saved_connection_change_password_field,
            )
        )

    def _setup_scrollbar_signals(self) -> None:
        self._panel.listView.verticalScrollBar().valueChanged.connect(
            self._handle_scrollbar_change
        )
        self._panel.verticalScrollBar.valueChanged.connect(self._handle_scrollbar_change)
        self._panel.verticalScrollBar.valueChanged.connect(
            lambda value: self._panel.listView.verticalScrollBar().setValue(value)
        )
        self._panel.verticalScrollBar.show()

    def _configure_list_view_palette(self) -> None:
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

        self._panel.listView.setPalette(palette)

    def _show_error_popup(self, message: str, timeout: int = 6000) -> None:
        self._popup.new_message(
            message_type=Popup.MessageType.ERROR,
            message=message,
            timeout=timeout,
            userInput=False,
        )

    def _show_info_popup(self, message: str, timeout: int = 4000) -> None:
        self._popup.new_message(
            message_type=Popup.MessageType.INFO,
            message=message,
            timeout=timeout,
            userInput=False,
        )

    def _show_warning_popup(self, message: str, timeout: int = 5000) -> None:
        self._popup.new_message(
            message_type=Popup.MessageType.WARNING,
            message=message,
            timeout=timeout,
            userInput=False,
        )

    def closeEvent(self, event: Optional[QtGui.QCloseEvent]) -> None:
        self._stop_all_timers()
        self._network_list_worker.stop_polling()
        super().closeEvent(event)

    def showEvent(self, event: Optional[QtGui.QShowEvent]) -> None:
        if self._networks:
            self._build_model_list()
        self._evaluate_network_state()
        super().showEvent(event)

    def _stop_all_timers(self) -> None:
        timers = [
            self._load_timer,
            self._status_check_timer,
            self._delayed_action_timer,
        ]
        for timer in timers:
            if timer.isActive():
                timer.stop()

    def _on_show_keyboard(
        self,
        panel: QtWidgets.QWidget,
        field: QtWidgets.QLineEdit
    ) -> None:
        self._previous_panel = panel
        self._current_field = field
        self._qwerty.set_value(field.text())
        self.setCurrentIndex(self.indexOf(self._qwerty))

    def _on_qwerty_go_back(self) -> None:
        if self._previous_panel:
            self.setCurrentIndex(self.indexOf(self._previous_panel))

    def _on_qwerty_value_selected(self, value: str) -> None:
        if self._previous_panel:
            self.setCurrentIndex(self.indexOf(self._previous_panel))
        if self._current_field:
            self._current_field.setText(value)

    def _set_loading_state(self, loading: bool) -> None:
        self._set_info_panel_visibility(show_details=not loading, show_loading=loading)
        self._panel.wifi_button.setEnabled(not loading)
        self._panel.hotspot_button.setEnabled(not loading)

        if loading:
            if self._load_timer.isActive():
                self._load_timer.stop()
            self._load_timer.start(LOAD_TIMEOUT_MS)
        else:
            if self._load_timer.isActive():
                self._load_timer.stop()

    def _handle_load_timeout(self) -> None:
        if not self._panel.loadingwidget.isVisible():
            return

        wifi_btn = self._panel.wifi_button
        hotspot_btn = self._panel.hotspot_button

        message = self._get_timeout_message(wifi_btn, hotspot_btn)

        self._panel.mn_info_box.setText(message)
        self._set_info_panel_visibility(show_details=False, show_loading=False)
        self._configure_info_box_centered()

        hotspot_btn.setEnabled(True)
        wifi_btn.setEnabled(True)

    def _get_timeout_message(self, wifi_btn, hotspot_btn) -> str:
        if wifi_btn.toggle_button.state == wifi_btn.toggle_button.State.ON:
            return (
                    "Wi-Fi Connection Failed.\nThe connection attempt timed out."
            )
        elif hotspot_btn.toggle_button.state == hotspot_btn.toggle_button.State.ON:
            return (
                "Hotspot Setup Failed.\n"
                "The local network sharing timed out.\n"
                "Please restart the hotspot."
            )
        else:
            return "Loading timed out.\nPlease check your connection and try again."

    def _set_info_panel_visibility(
        self,
        show_details: bool,
        show_loading: bool = False
    ) -> None:
        self._panel.netlist_ip.setVisible(show_details)
        self._panel.netlist_ssuid.setVisible(show_details)
        self._panel.mn_info_seperator.setVisible(show_details)
        self._panel.line_2.setVisible(show_details)
        self._panel.netlist_strength.setVisible(show_details)
        self._panel.netlist_strength_label.setVisible(show_details)
        self._panel.line_3.setVisible(show_details)
        self._panel.netlist_security.setVisible(show_details)
        self._panel.netlist_security_label.setVisible(show_details)
        self._panel.mn_info_box.setVisible(not show_loading)
        self._panel.loadingwidget.setVisible(show_loading)

    def _configure_info_box_centered(self) -> None:
        self._panel.mn_info_box.setWordWrap(True)
        self._panel.mn_info_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    @QtCore.pyqtSlot(object, name="stateChange")
    def _on_toggle_state(self, new_state) -> None:
        sender_button = self.sender()
        wifi_btn = self._panel.wifi_button.toggle_button
        hotspot_btn = self._panel.hotspot_button.toggle_button
        is_sender_now_on = new_state == sender_button.State.ON

        saved_networks = self._sdbus_network.get_saved_networks_with_for()

        if sender_button is wifi_btn:
            self._handle_wifi_toggle(is_sender_now_on, hotspot_btn, saved_networks)
        elif sender_button is hotspot_btn:
            self._handle_hotspot_toggle(is_sender_now_on, wifi_btn, saved_networks)

        self._set_loading_state(False)

        if (
            hotspot_btn.state == hotspot_btn.State.OFF
            and wifi_btn.state == wifi_btn.State.OFF
        ):
            self._evaluate_network_state()
        else:
            self._set_loading_state(True)

    def _handle_wifi_toggle(
        self,
        is_on: bool,
        hotspot_btn,
        saved_networks: List[Dict]
    ) -> None:
        if not is_on:
            return

        hotspot_btn.state = hotspot_btn.State.OFF
        self._sdbus_network.toggle_hotspot(False)
        self._clear_hotspot_ip_cache()

        if not saved_networks:
            return

        try:
            ssid = next(
                (
                    n["ssid"]
                    for n in saved_networks
                    if "ap" not in n.get("mode", "") and n.get("signal", 0) != 0
                ),
                None,
            )
            if ssid:
                self._sdbus_network.connect_network(str(ssid))
        except Exception as e:
            logger.error("Error when turning ON wifi: %s",e)

    def _handle_hotspot_toggle(
        self,
        is_on: bool,
        wifi_btn,
        saved_networks: List[Dict]
    ) -> None:
        if not is_on:
            self._clear_hotspot_ip_cache()
            return

        wifi_btn.state = wifi_btn.State.OFF

        old_hotspot = self._find_hotspot_in_saved(saved_networks)

        new_hotspot_name = self._panel.hotspot_name_input_field.text()
        if old_hotspot and old_hotspot["ssid"] != new_hotspot_name:
            self._sdbus_network.delete_network(old_hotspot["ssid"])

        self._sdbus_network.create_hotspot(
            new_hotspot_name,
            self._panel.hotspot_password_input_field.text(),
        )
        self._sdbus_network.toggle_hotspot(True)
        try: 
            self._sdbus_network.connect_network(new_hotspot_name)
        except Exception as e:
            logger.error(e)

    def _find_hotspot_in_saved(self, saved_networks: List[Dict]) -> Optional[Dict]:
        return next(
            (n for n in saved_networks if "ap" in n.get("mode", "")),
            None
        )

    def _find_wifi_networks_in_saved(self, saved_networks: List[Dict]) -> List[Dict]:
        return [
            n for n in saved_networks
            if "ap" not in n.get("mode", "") and n.get("signal", 0) != 0
        ]

    @QtCore.pyqtSlot(str, name="nm-state-changed")
    def _evaluate_network_state(self, nm_state: str = "") -> None:
        wifi_btn = self._panel.wifi_button.toggle_button
        hotspot_btn = self._panel.hotspot_button.toggle_button

        state = nm_state or self._sdbus_network.check_nm_state()
        if not state:
            return

        if self._is_first_run:
            self._handle_first_run_state()
            self._is_first_run = False

        if not self._sdbus_network.check_wifi_interface():
            return

        if hotspot_btn.state == hotspot_btn.State.ON:
            self._update_hotspot_display()
        elif wifi_btn.state == wifi_btn.State.ON:
            self._update_wifi_display()

        self._set_info_panel_visibility(show_details=True)
        self._set_loading_state(False)
        self._panel.wifi_button.setEnabled(True)
        self._panel.hotspot_button.setEnabled(True)

        if (
            wifi_btn.state == wifi_btn.State.OFF
            and hotspot_btn.state == hotspot_btn.State.OFF
        ):
            self._sdbus_network.disconnect_network()
            self._set_info_panel_visibility(show_details=False)
            self._configure_info_box_centered()
            self._panel.mn_info_box.setText(
                "Network connection required.\n\nConnect to Wi-Fi\nor\nTurn on Hotspot"
            )
        self.repaint()

    def _handle_first_run_state(self) -> None:
        saved_networks = self._sdbus_network.get_saved_networks_with_for()

        old_hotspot = self._find_hotspot_in_saved(saved_networks)
        if old_hotspot:
            self._panel.hotspot_name_input_field.setText(old_hotspot["ssid"])

        connection = self._sdbus_network.check_connectivity()
        wifi_btn = self._panel.wifi_button.toggle_button
        hotspot_btn = self._panel.hotspot_button.toggle_button

        if connection == "FULL":
            wifi_btn.state = wifi_btn.State.ON
            hotspot_btn.state = hotspot_btn.State.OFF
        elif connection == "LIMITED":
            wifi_btn.state = wifi_btn.State.OFF
            hotspot_btn.state = hotspot_btn.State.ON

    def _update_hotspot_display(self) -> None:
        ipv4_addr = self._get_hotspot_ip_via_psutil()

        self._panel.netlist_ssuid.setText(self._panel.hotspot_name_input_field.text())
        self._panel.netlist_ip.setText(f"IP: {ipv4_addr or 'No IP Address'}")
        self._panel.netlist_strength.setText("--")
        self._panel.netlist_security.setText("--")
        self._panel.mn_info_box.setText("Hotspot On")

    def _update_wifi_display(self) -> None:
        current_ssid = self._sdbus_network.get_current_ssid()

        if current_ssid:
            ipv4_addr = self._sdbus_network.get_current_ip_addr()
            sec_type = self._sdbus_network.get_security_type_by_ssid(current_ssid)
            signal_strength = self._sdbus_network.get_connection_signal_by_ssid(current_ssid)

            self._panel.netlist_ssuid.setText(current_ssid)
            self._panel.netlist_ip.setText(f"IP: {ipv4_addr}")
            self._panel.netlist_security.setText(str(sec_type or "--").upper())
            self._panel.netlist_strength.setText(
                str(signal_strength) if signal_strength != -1 else "--"
            )
            self._panel.mn_info_box.setText("Connected")
        else:
            self._panel.netlist_ssuid.setText("")
            self._panel.netlist_ip.setText("No IP Address")
            self._panel.netlist_security.setText("--")
            self._panel.netlist_strength.setText("--")
            self._panel.mn_info_box.setText("Disconnected")

    def _get_hotspot_ip_via_psutil(self, iface: str = "wlan0") -> str:
        """
        Get the IPv4 address for the given interface using psutil.
        Returns an empty string if no address is found.
        """
        if self._cached_hotspot_ip:
            return self._cached_hotspot_ip

        try:
            addrs = psutil.net_if_addrs().get(iface, [])
            for addr in addrs:
                # Only look at IPv4 addresses
                if addr.family == socket.AF_INET:
                    ip = addr.address
                    self._cached_hotspot_ip = ip
                    return ip
        except Exception:
            # If psutil isn't installed or something goes wrong, ignore
            pass

        return ""

    def _clear_hotspot_ip_cache(self) -> None:
        self._cached_hotspot_ip = ""

    @QtCore.pyqtSlot(str, name="delete-network")
    def _delete_network(self, ssid: str) -> None:
        try:
            self._sdbus_network.delete_network(ssid=ssid)
        except Exception as e:
            logger.error("Failed to delete network %s: %s",ssid,e)
            self._show_error_popup("Failed to delete network")

    @QtCore.pyqtSlot(name="rescan-networks")
    def _rescan_networks(self) -> None:
        self._sdbus_network.rescan_networks()

    @QtCore.pyqtSlot(name="add-network")
    def _add_network(self) -> None:
        self._panel.add_network_validation_button.setEnabled(False)
        self._panel.add_network_validation_button.update()

        password = self._panel.add_network_password_field.text()
        ssid = self._panel.add_network_network_label.text()

        if not password and not self._current_network_is_open:
            self._show_error_popup("Password field cannot be empty.")
            self._panel.add_network_validation_button.setEnabled(True)
            return

        result = self._sdbus_network.add_wifi_network(ssid=ssid, psk=password)
        self._panel.add_network_password_field.clear()

        error_msg = result.get("error", "") if result else ""

        if not error_msg:
            self._handle_successful_network_add(ssid)
        else:
            self._handle_failed_network_add(error_msg)

    def _handle_successful_network_add(self, ssid: str) -> None:
        self._schedule_delayed_action(
            self._network_list_worker.build,
            NETWORK_CONNECT_DELAY_MS
        )
        QtCore.QTimer.singleShot(
            NETWORK_CONNECT_DELAY_MS,
            lambda: self._sdbus_network.connect_network(ssid)
        )

        self._set_loading_state(True)
        self.setCurrentIndex(self.indexOf(self._panel.main_network_page))
        self._panel.add_network_validation_button.setEnabled(True)
        self._panel.wifi_button.setEnabled(False)
        self._panel.hotspot_button.setEnabled(False)
        self._panel.add_network_validation_button.update()

    def _handle_failed_network_add(self, error_msg: str) -> None:
        error_messages = {
            "Invalid password": "Invalid password. Please try again",
            "Network connection properties error": (
                "Network connection properties error. Please try again"
            ),
            "Permission Denied": "Permission Denied. Please try again",
        }

        message = error_messages.get(
            error_msg,
            "Error while adding network. Please try again"
        )

        self._panel.add_network_validation_button.setEnabled(True)
        self._panel.add_network_validation_button.update()
        self._show_error_popup(message)

    def _on_save_network_settings(self) -> None:
        self._update_network(
            ssid=self._panel.saved_connection_network_name.text(),
            password=self._panel.saved_connection_change_password_field.text(),
            new_ssid=None,
        )

    def _update_network(
        self,
        ssid: str,
        password: Optional[str],
        new_ssid: Optional[str],
    ) -> None:
        if not self._sdbus_network.is_known(ssid):
            return

        priority = self._get_selected_priority()

        try:
            self._sdbus_network.update_connection_settings(
                ssid=ssid,
                password=password,
                new_ssid=new_ssid,
                priority=priority
            )
        except Exception as e:
            logger.error("Failed to update network settings: %s",e)
            self._show_error_popup("Failed to update network settings")

        self.setCurrentIndex(self.indexOf(self._panel.network_list_page))

    def _get_selected_priority(self) -> int:
        checked_btn = self._panel.priority_btn_group.checkedButton()

        if checked_btn == self._panel.high_priority_btn:
            return PRIORITY_HIGH
        elif checked_btn == self._panel.low_priority_btn:
            return PRIORITY_LOW
        else:
            return PRIORITY_MEDIUM

    def _on_saved_wifi_option_selected(self) -> None:
        sender = self.sender()

        wifi_toggle = self._panel.wifi_button.toggle_button
        hotspot_toggle = self._panel.hotspot_button.toggle_button

        with QtCore.QSignalBlocker(wifi_toggle), QtCore.QSignalBlocker(hotspot_toggle):
            wifi_toggle.state = wifi_toggle.State.ON
            hotspot_toggle.state = hotspot_toggle.State.OFF

        ssid = self._panel.saved_connection_network_name.text()

        if sender == self._panel.network_delete_btn:
            self._handle_network_delete(ssid)
        elif sender == self._panel.network_activate_btn:
            self._handle_network_activate(ssid)

    def _handle_network_delete(self, ssid: str) -> None:
        try:
            self._sdbus_network.delete_network(ssid)
            if ssid in self._networks:
                network_was_saved = self._networks[ssid].is_saved
                del self._networks[ssid]
                if network_was_saved:
                    self._network_list_worker.build()
            self.setCurrentIndex(self.indexOf(self._panel.network_list_page))
            self._build_model_list()
            self._show_info_popup(f"Network '{ssid}' deleted")
        except Exception as e:
            logger.error("Failed to delete network %s: %s",ssid,e)
            self._show_error_popup("Failed to delete network")

    def _handle_network_activate(self, ssid: str) -> None:
        self.setCurrentIndex(self.indexOf(self._panel.main_network_page))
        try:
            self._sdbus_network.connect_network(ssid)
            self._set_loading_state(True)
        except Exception as e:
            logger.error("Failed to connect to %s: %s",ssid,e)
            self._set_loading_state(False)
            self._show_error_popup("Failed to connect to network")

    @QtCore.pyqtSlot(name="handle-hotspot-back")
    def _handle_hotspot_back(self) -> None:
        if (
            self._panel.hotspot_password_input_field.text()
            != self._sdbus_network.hotspot_password
        ):
            self._panel.hotspot_password_input_field.setText(
                self._sdbus_network.hotspot_password
            )
        if (
            self._panel.hotspot_name_input_field.text()
            != self._sdbus_network.hotspot_ssid
        ):
            self._panel.hotspot_name_input_field.setText(
                self._sdbus_network.hotspot_ssid
            )

        self.setCurrentIndex(self.indexOf(self._panel.main_network_page))

    @QtCore.pyqtSlot(list, name="finished-network-list-build")
    def _handle_network_list(self, data: List[tuple]) -> None:
        self._networks.clear()
        hotspot_ssid = self._sdbus_network.hotspot_ssid

        for entry in data:
            if len(entry) >= 5:
                ssid, signal, status, is_open, is_saved = entry
            elif len(entry) >= 4:
                ssid, signal, status, is_open = entry
                is_saved = status in ("Active", "Saved")
            else:
                ssid, signal, status = entry[0], entry[1], entry[2]
                is_open = status == "Open"
                is_saved = status in ("Active", "Saved")

            if ssid == hotspot_ssid:
                continue

            self._networks[ssid] = NetworkInfo(
                signal=signal,
                status=status,
                is_open=is_open,
                is_saved=is_saved
            )

        self._build_model_list()

    def _build_model_list(self) -> None:
        self._panel.listView.blockSignals(True)
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
                is_open=info.is_open
            )

        if saved_networks and unsaved_networks:
            self._add_separator_entry()

        for ssid, info in unsaved_networks:
            self._add_network_entry(
                ssid=ssid,
                signal=info.signal,
                status=info.status,
                is_open=info.is_open
            )

        self._sync_scrollbar()
        self._panel.listView.blockSignals(False)
        self._panel.listView.update()

    def _reset_view_model(self) -> None:
        self._model.clear()
        self._entry_delegate.clear()

    def _add_separator_entry(self) -> None:
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

    def _add_network_entry(
        self,
        ssid: str,
        signal: int,
        status: str,
        is_open: bool = False
    ) -> None:
        wifi_pixmap = self._icon_provider.get_pixmap(signal=signal, status=status)
        display_ssid = ssid if ssid else "UNKNOWN"
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
            not_clickable=False,
        )
        self._model.add_item(item)

    @QtCore.pyqtSlot(ListItem, name="ssid-item-clicked")
    def _on_ssid_item_clicked(self, item: ListItem) -> None:
        ssid = item.text
        if not ssid:
            return

        network_info = self._networks.get(ssid)
        if network_info is None:
            return

        if network_info.is_saved:
            saved_networks = self._sdbus_network.get_saved_networks_with_for()
            self._show_saved_network_page(ssid, saved_networks)
        else:
            self._show_add_network_page(ssid, is_open=network_info.is_open)

    def _show_saved_network_page(self, ssid: str, saved_networks: List[Dict]) -> None:
        self._panel.saved_connection_network_name.setText(str(ssid))
        self._panel.snd_name.setText(str(ssid))

        entry = next((net for net in saved_networks if net["ssid"] == ssid), None)

        if entry is not None:
            self._set_priority_button(entry.get("priority"))

        network_info = self._networks.get(ssid)
        if network_info:
            signal_text = f"{network_info.signal}%" if network_info.signal >= 0 else "--%"
            self._panel.saved_connection_signal_strength_info_frame.setText(signal_text)

            if network_info.is_open:
                self._panel.saved_connection_security_type_info_label.setText("OPEN")
            else:
                sec_type = self._sdbus_network.get_security_type_by_ssid(ssid)
                self._panel.saved_connection_security_type_info_label.setText(
                    str(sec_type or "WPA").upper()
                )
        else:
            self._panel.saved_connection_signal_strength_info_frame.setText("--%")
            self._panel.saved_connection_security_type_info_label.setText("--")

        current_ssid = self._sdbus_network.get_current_ssid()
        if current_ssid != ssid:
            self._panel.network_activate_btn.setDisabled(False)
            self._panel.sn_info.setText("Saved Network")
        else:
            self._panel.network_activate_btn.setDisabled(True)
            self._panel.sn_info.setText("Active Network")

        self.setCurrentIndex(self.indexOf(self._panel.saved_connection_page))
        self._panel.frame.repaint()

    def _set_priority_button(self, priority: Optional[int]) -> None:
        if priority == PRIORITY_HIGH:
            self._panel.high_priority_btn.setChecked(True)
        elif priority == PRIORITY_LOW:
            self._panel.low_priority_btn.setChecked(True)
        else:
            self._panel.med_priority_btn.setChecked(True)

    def _show_add_network_page(self, ssid: str, is_open: bool = False) -> None:
        self._current_network_is_open = is_open
        self._panel.add_network_network_label.setText(str(ssid))
        self.setCurrentIndex(self.indexOf(self._panel.add_network_page))

    def _set_add_network_page_password_visibility(self, show_password: bool) -> None:
        self._panel.frame_2.setVisible(show_password)

    def _handle_scrollbar_change(self, value: int) -> None:
        self._panel.verticalScrollBar.blockSignals(True)
        self._panel.verticalScrollBar.setValue(value)
        self._panel.verticalScrollBar.blockSignals(False)

    def _sync_scrollbar(self) -> None:
        list_scrollbar = self._panel.listView.verticalScrollBar()
        self._panel.verticalScrollBar.setMinimum(list_scrollbar.minimum())
        self._panel.verticalScrollBar.setMaximum(list_scrollbar.maximum())
        self._panel.verticalScrollBar.setPageStep(list_scrollbar.pageStep())

    def _schedule_delayed_action(self, callback: Callable, delay_ms: int) -> None:
        try:
            self._delayed_action_timer.timeout.disconnect()
        except TypeError:
            pass

        self._delayed_action_timer.timeout.connect(callback)
        self._delayed_action_timer.start(delay_ms)

    def close(self) -> bool:
        self._network_list_worker.stop_polling()
        self._sdbus_network.close()
        return super().close()

    def setCurrentIndex(self, index: int) -> None:
        if not self.isVisible():
            return

        if index == self.indexOf(self._panel.add_network_page):
            self._setup_add_network_page()
        elif index == self.indexOf(self._panel.saved_connection_page):
            self._setup_saved_connection_page()

        self.repaint()
        super().setCurrentIndex(index)

    def _setup_add_network_page(self) -> None:
        self._panel.add_network_password_field.clear()

        if self._current_network_is_open:
            self._panel.frame_2.setVisible(False)
            self._panel.add_network_validation_button.setText("Connect")
        else:
            self._panel.frame_2.setVisible(True)
            self._panel.add_network_password_field.setPlaceholderText(
                "Insert password here, press enter when finished."
            )
            self._panel.add_network_validation_button.setText("Activate")

    def _setup_saved_connection_page(self) -> None:
        self._panel.saved_connection_change_password_field.clear()
        self._panel.saved_connection_change_password_field.setPlaceholderText(
            "Change network password"
        )

    def setProperty(self, name: str, value: Any) -> bool:
        if name == "backgroundPixmap":
            self._background = value
        return super().setProperty(name, value)

    @QtCore.pyqtSlot(name="call-network-panel")
    def show_network_panel(self) -> None:
        if not self.parent():
            return

        self.setCurrentIndex(self.indexOf(self._panel.network_list_page))
        parent_size = self.parent().size()
        self.setGeometry(0, 0, parent_size.width(), parent_size.height())
        self.updateGeometry()
        self.repaint()
        self.show()