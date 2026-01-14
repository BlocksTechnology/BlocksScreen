import copy
import logging
import subprocess  # nosec: B404
import typing
from functools import partial

from lib.network import SdbusNetworkManagerAsync
from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard
from lib.panels.widgets.popupDialogWidget import Popup
from lib.ui.wifiConnectivityWindow_ui import Ui_wifi_stacked_page
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal

logger = logging.getLogger("logs/BlocksScreen.log")


class NetworkScanRunnable(QRunnable):
    """QRunnable task that performs network scanning using SdbusNetworkManagerAsync

    This runnable:
      - Triggers a network rescan via SdbusNetworkManagerAsync
      - collects SSIDs, signal strenght and saved status
      - emits signal with raw scan data and a processed lisgs

    Signals:
        - scan_results (dict): Emitted with raw scan results mapping SSID to properties
        - finished_network_list_build (list): Emitted with processed list of networks
        - error (str): Emitted if an error occurs during scanning

    """

    class Signals(QObject):
        scan_results = pyqtSignal(dict, name="scan-results")
        finished_network_list_build = pyqtSignal(
            list, name="finished-network-list-build"
        )
        error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.nm = SdbusNetworkManagerAsync()
        self.signals = NetworkScanRunnable.Signals()

    def run(self):
        try:
            logger.debug("NetworkScanRunnable: scanning networks")
            self.nm.rescan_networks()
            saved = self.nm.get_saved_ssid_names()
            available = (
                self.nm.get_available_networks()
                if self.nm.check_wifi_interface()
                else {}
            )

            data_dict: dict[str, dict] = {}
            for ssid, props in available.items():
                signal = int(props.get("signal_level", 0))
                data_dict[ssid] = {
                    "signal_level": signal,
                    "is_saved": ssid in saved,
                }

            self.signals.scan_results.emit(data_dict)

            items: list[typing.Union[tuple[str, int, str], str]] = []
            saved_nets = [
                (ssid, info["signal_level"])
                for ssid, info in data_dict.items()
                if info["is_saved"]
            ]
            unsaved_nets = [
                (ssid, info["signal_level"])
                for ssid, info in data_dict.items()
                if not info["is_saved"]
            ]
            saved_nets.sort(key=lambda x: -x[1])
            unsaved_nets.sort(key=lambda x: -x[1])

            for ssid, sig in saved_nets:
                status = "Active" if ssid == self.nm.get_current_ssid() else "Saved"
                items.append((ssid, sig, status))

            for ssid, sig in unsaved_nets:
                items.append((ssid, sig, "Protected"))

            self.signals.finished_network_list_build.emit(items)

        except Exception as e:
            logger.error("Error scanning networks", exc_info=True)
            self.signals.error.emit(str(e))


class BuildNetworkList(QtCore.QObject):
    """
    Controller class that schedules and manages repeted network scans

    Uses a QThreadPool to un NetworkScanRunnable tasks periodically. with a QTimer to trigger scans.
    Prevents overlapping scans by tracking whether a scan is already in progress.

    Args:
        poll_interval_ms: (int) Milliseconds between scans (default: 10000)
        _timer (QtCore.QTimer): Timer that schedules next scan
        _is_scanning (bool): Flag indicating if a scan is currently in progress

    Signals:
        scan_results (dict): Emitted with raw scan results mapping SSID to properties
        finished_network_list_build (list): Emitted with processed list of networks
        error (str): Emitted if an error occurs during scanning
    """

    scan_results = pyqtSignal(dict, name="scan-results")
    finished_network_list_build = pyqtSignal(list, name="finished-network-list-build")
    error = pyqtSignal(str)

    def __init__(self, poll_interval_ms: int = 10000):
        super().__init__()
        self.threadpool = QThreadPool.globalInstance()
        self.poll_interval_ms = poll_interval_ms
        self._is_scanning = False

        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._do_scan)

    def start_polling(self):
        """Schedule scan folowwing the `poll_interval_ms`"""
        self._schedule_next_scan()

    def stop_polling(self):
        """Start Polling for future development"""
        self._timer.stop()

    def build(self):
        """Method called by rescan button"""
        self._do_scan()

    def _schedule_next_scan(self):
        """Start next rescan timer"""
        self._timer.start(self.poll_interval_ms)

    def _on_task_finished(self, items):
        """Update data after scan finish, update saved networks list and schedule next scan"""
        self._is_scanning = False
        self.finished_network_list_build.emit(items)
        self._schedule_next_scan()

    def _on_task_scan_results(self, data_dict):
        """Emit results to main thread"""
        self.scan_results.emit(data_dict)

    def _on_task_error(self, err):
        """Emit errors to main thread"""
        self._is_scanning = False
        self.error.emit(err)
        self._schedule_next_scan()

    def _do_scan(self):
        """Start wifi scanning threadpool"""
        if self._is_scanning:
            logger.debug("Already scanning, skip scheduling.")
            self._schedule_next_scan()
            return

        self._is_scanning = True
        task = NetworkScanRunnable()
        task.signals.finished_network_list_build.connect(self._on_task_finished)
        task.signals.scan_results.connect(self._on_task_scan_results)
        task.signals.error.connect(self._on_task_error)

        self.threadpool.start(task)
        logger.debug("Submitted scan task to thread pool")


class WifiIconProvider:
    """Simple provider: loads QPixmap for WiFi bars + protection without caching."""

    def __init__(self):
        self.paths = {
            (0, False): ":/network/media/btn_icons/0bar_wifi.svg",
            (4, False): ":/network/media/btn_icons/4bar_wifi.svg",
            (3, False): ":/network/media/btn_icons/3bar_wifi.svg",
            (2, False): ":/network/media/btn_icons/2bar_wifi.svg",
            (1, False): ":/network/media/btn_icons/1bar_wifi.svg",
            (0, True): ":/network/media/btn_icons/0bar_wifi_protected.svg",
            (4, True): ":/network/media/btn_icons/4bar_wifi_protected.svg",
            (3, True): ":/network/media/btn_icons/3bar_wifi_protected.svg",
            (2, True): ":/network/media/btn_icons/2bar_wifi_protected.svg",
            (1, True): ":/network/media/btn_icons/1bar_wifi_protected.svg",
        }

    def get_pixmap(self, signal: int, state: str) -> QtGui.QPixmap:
        """Return a QPixmap for the given signal (0-100) and state ("Protected" or not)."""
        if signal < 5:
            bars = 0
        elif signal >= 75:
            bars = 4
        elif signal >= 50:
            bars = 3
        elif signal > 25:
            bars = 2
        else:
            bars = 1

        is_protected = state == "Protected"
        key = (bars, is_protected)

        path = self.paths.get(key)
        if path is None:
            logger.debug(
                f"No icon path for key {key}, falling back to no-signal unprotected"
            )
            path = self.paths[(0, False)]

        pm = QtGui.QPixmap(path)
        if pm.isNull():
            logger.debug(f"Failed to load pixmap from '{path}' for key {key}")
        return pm


class NetworkControlWindow(QtWidgets.QStackedWidget):
    """Network Control panel Widget"""

    request_network_scan = QtCore.pyqtSignal(name="scan-network")
    new_ip_signal = QtCore.pyqtSignal(str, name="ip-address-change")
    get_hotspot_ssid = QtCore.pyqtSignal(str, name="hotspot-ssid-name")
    delete_network_signal = QtCore.pyqtSignal(str, name="delete-network")

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget], /) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()

        self.panel = Ui_wifi_stacked_page()
        self.panel.setupUi(self)
        self._provider = WifiIconProvider()
        self.ongoing_update: bool = False

        self.popup = Popup(self)
        self.sdbus_network = SdbusNetworkManagerAsync()
        self.start: bool = True
        self.saved_network = {}

        self.repeated_request_status = QtCore.QTimer()
        self.repeated_request_status.setInterval(2000)

        self._load_timer = QtCore.QTimer()
        self._load_timer.setSingleShot(True)
        self._load_timer.timeout.connect(self._handle_load_timeout)

        self.model = EntryListModel()
        self.model.setParent(self.panel.listView)
        self.entry_delegate = EntryDelegate()
        self.panel.listView.setModel(self.model)
        self.panel.listView.setItemDelegate(self.entry_delegate)
        self.entry_delegate.item_selected.connect(self.ssid_item_clicked)

        self.build_network_list()
        self.network_list_worker = BuildNetworkList()
        self.network_list_worker.finished_network_list_build.connect(
            self.handle_network_list
        )
        self.network_list_worker.start_polling()
        self.panel.rescan_button.clicked.connect(self.network_list_worker.build)

        self.sdbus_network.nm_state_change.connect(self.evaluate_network_state)
        self.panel.wifi_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.panel.network_list_page))
        )
        self.panel.hotspot_button.clicked.connect(
            partial(self.setCurrentIndex, self.indexOf(self.panel.hotspot_page))
        )

        self.panel.hotspot_button.setPixmap(
            QtGui.QPixmap(":/network/media/btn_icons/hotspot.svg")
        )
        self.panel.wifi_button.setPixmap(
            QtGui.QPixmap(":/network/media/btn_icons/wifi_config.svg")
        )
        self.right_icon = QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")

        self.panel.nl_back_button.clicked.connect(
            partial(
                self.setCurrentIndex,
                self.indexOf(self.panel.main_network_page),
            )
        )

        self.panel.network_backButton.clicked.connect(self.hide)
        self.panel.rescan_button.clicked.connect(
            lambda: self.sdbus_network.rescan_networks()
        )

        self.request_network_scan.connect(self.rescan_networks)
        self.panel.add_network_validation_button.clicked.connect(self.add_network)
        self.panel.add_network_page_backButton.clicked.connect(
            partial(
                self.setCurrentIndex,
                self.indexOf(self.panel.network_list_page),
            )
        )
        self.panel.add_network_password_view.pressed.connect(
            partial(
                self.panel.add_network_password_field.setEchoMode,
                QtWidgets.QLineEdit.EchoMode.Normal,
            )
        )
        self.panel.add_network_password_view.released.connect(
            partial(
                self.panel.add_network_password_field.setEchoMode,
                QtWidgets.QLineEdit.EchoMode.Password,
            )
        )

        self.panel.saved_connection_back_button.clicked.connect(
            partial(
                self.setCurrentIndex,
                self.indexOf(self.panel.network_list_page),
            )
        )
        self.delete_network_signal.connect(self.delete_network)
        self.panel.snd_back.clicked.connect(
            lambda: self.update_network(
                ssid=self.panel.saved_connection_network_name.text(),
                password=self.panel.saved_connection_change_password_field.text(),
                new_ssid=None,
            )
        )
        self.panel.saved_connection_change_password_view.pressed.connect(
            partial(
                self.panel.saved_connection_change_password_field.setEchoMode,
                QtWidgets.QLineEdit.EchoMode.Normal,
            )
        )
        self.panel.saved_connection_change_password_view.released.connect(
            partial(
                self.panel.saved_connection_change_password_field.setEchoMode,
                QtWidgets.QLineEdit.EchoMode.Password,
            )
        )
        self.panel.hotspot_back_button.clicked.connect(
            lambda: self.setCurrentIndex(self.indexOf(self.panel.main_network_page))
        )

        self.panel.hotspot_password_input_field.setPlaceholderText(
            "Defaults to: 123456789"
        )
        self.panel.hotspot_change_confirm.clicked.connect(
            lambda: self.setCurrentIndex(self.indexOf(self.panel.main_network_page))
        )

        self.panel.hotspot_password_input_field.setHidden(True)
        self.panel.hotspot_password_view_button.pressed.connect(
            partial(self.panel.hotspot_password_input_field.setHidden, False)
        )
        self.panel.hotspot_password_view_button.released.connect(
            partial(self.panel.hotspot_password_input_field.setHidden, True)
        )
        self.panel.hotspot_name_input_field.setText(
            str(self.sdbus_network.get_hotspot_ssid())
        )
        self.panel.hotspot_password_input_field.setText(
            str(self.sdbus_network.hotspot_password)
        )
        self.panel.wifi_button.toggle_button.stateChange.connect(self.on_toggle_state)
        self.panel.hotspot_button.toggle_button.stateChange.connect(
            self.on_toggle_state
        )
        self.panel.saved_connection_change_password_view.pressed.connect(
            lambda: self.panel.saved_connection_change_password_view.setPixmap(
                QtGui.QPixmap(":/ui/media/btn_icons/see.svg")
            )
        )
        self.panel.saved_connection_change_password_view.released.connect(
            lambda: self.panel.saved_connection_change_password_view.setPixmap(
                QtGui.QPixmap(":/ui/media/btn_icons/unsee.svg")
            )
        )
        self.panel.add_network_password_view.released.connect(
            lambda: self.panel.add_network_password_view.setPixmap(
                QtGui.QPixmap(":/ui/media/btn_icons/unsee.svg")
            )
        )
        self.panel.add_network_password_view.pressed.connect(
            lambda: self.panel.add_network_password_view.setPixmap(
                QtGui.QPixmap(":/ui/media/btn_icons/see.svg")
            )
        )
        self.panel.hotspot_password_view_button.released.connect(
            lambda: self.panel.hotspot_password_view_button.setPixmap(
                QtGui.QPixmap(":/ui/media/btn_icons/unsee.svg")
            )
        )
        self.panel.hotspot_password_view_button.pressed.connect(
            lambda: self.panel.hotspot_password_view_button.setPixmap(
                QtGui.QPixmap(":/ui/media/btn_icons/see.svg")
            )
        )

        self.panel.add_network_password_field.setCursor(
            QtCore.Qt.CursorShape.BlankCursor
        )
        self.panel.hotspot_name_input_field.setCursor(QtCore.Qt.CursorShape.BlankCursor)
        self.panel.hotspot_password_input_field.setCursor(
            QtCore.Qt.CursorShape.BlankCursor
        )
        self.panel.network_delete_btn.setPixmap(
            QtGui.QPixmap(":/ui/media/btn_icons/garbage-icon.svg")
        )

        self.panel.network_activate_btn.setPixmap(
            QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )

        self.panel.network_details_btn.setPixmap(
            QtGui.QPixmap(":/ui/media/btn_icons/printer_settings.svg")
        )

        self.panel.snd_back.clicked.connect(
            lambda: self.setCurrentIndex(self.indexOf(self.panel.saved_connection_page))
        )
        self.panel.network_details_btn.clicked.connect(
            lambda: self.setCurrentIndex(self.indexOf(self.panel.saved_details_page))
        )

        self.panel.network_activate_btn.clicked.connect(
            lambda: self.saved_wifi_option_selected()
        )
        self.panel.network_delete_btn.clicked.connect(
            lambda: self.saved_wifi_option_selected()
        )

        self.network_list_worker.build()
        self.request_network_scan.emit()
        self.panel.listView.verticalScrollBar().valueChanged.connect(
            self._handle_scrollbar
        )
        self.panel.verticalScrollBar.valueChanged.connect(self._handle_scrollbar)
        self.panel.verticalScrollBar.valueChanged.connect(
            lambda value: self.panel.listView.verticalScrollBar().setValue(value)
        )
        self.panel.verticalScrollBar.show()
        self.hide()
        self.info_box_load()

        self.qwerty = CustomQwertyKeyboard(self)
        self.addWidget(self.qwerty)
        self.qwerty.value_selected.connect(self.on_qwerty_value_selected)
        self.qwerty.request_back.connect(self.on_qwerty_go_back)

        self.panel.add_network_password_field.clicked.connect(
            lambda: self.on_show_keyboard(
                self.panel.add_network_page, self.panel.add_network_password_field
            )
        )
        self.panel.hotspot_password_input_field.clicked.connect(
            lambda: self.on_show_keyboard(
                self.panel.hotspot_page, self.panel.hotspot_password_input_field
            )
        )
        self.panel.hotspot_name_input_field.clicked.connect(
            lambda: self.on_show_keyboard(
                self.panel.hotspot_page, self.panel.hotspot_name_input_field
            )
        )
        self.panel.saved_connection_change_password_field.clicked.connect(
            lambda: self.on_show_keyboard(
                self.panel.saved_connection_page,
                self.panel.saved_connection_change_password_field,
            )
        )

    def handle_update_end(self) -> None:
        """Handles update end signal
        (closes loading page, returns to normal operation)
        """
        self.repeated_request_status.stop()
        self.request_network_scan.emit()
        self.build_model_list()

    def handle_ongoing_update(self) -> None:
        """Handled ongoing update signal,
        calls loading page (blocks user interaction)
        """
        self.repeated_request_status.start(2000)

    def reset_view_model(self) -> None:
        """Clears items from ListView
        (Resets `QAbstractListModel` by clearing entries)
        """
        self.model.clear()
        self.entry_delegate.clear()

    def deleteLater(self) -> None:
        """Schedule the object for deletion, resets the list model first"""
        self.reset_view_model()
        return super().deleteLater()

    def showEvent(self, event: QtGui.QShowEvent | None) -> None:
        """Re-add clients to update list"""
        if event.type() in (
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
        ):
            return True

        self.build_model_list()
        return super().showEvent(event)

    def build_model_list(self) -> None:
        """Builds the model list (`self.model`) containing updatable clients"""
        self.panel.listView.blockSignals(True)
        self.reset_view_model()
        saved_networks: dict = copy.copy(self.saved_network)
        if saved_networks.items():
            for ssid, (signal, is_saved) in saved_networks.items():
                self.add_network_entry(ssid=ssid, signal=signal, is_saved=is_saved)
            self._setup_scrollbar()

        self.panel.listView.blockSignals(False)

    def saved_wifi_option_selected(self):
        """Handle connect/delete network button clicks"""
        _sender = self.sender()
        self.panel.wifi_button.toggle_button.state = (
            self.panel.wifi_button.toggle_button.State.ON
        )
        self.panel.hotspot_button.toggle_button.state = (
            self.panel.hotspot_button.toggle_button.State.OFF
        )

        if _sender == self.panel.network_delete_btn:
            self.sdbus_network.delete_network(
                self.panel.saved_connection_network_name.text()
            )
            self.setCurrentIndex(self.indexOf(self.panel.main_network_page))

        elif _sender == self.panel.network_activate_btn:
            self.setCurrentIndex(self.indexOf(self.panel.main_network_page))
            self.sdbus_network.connect_network(
                self.panel.saved_connection_network_name.text()
            )
            self.info_box_load(True)

    def on_show_keyboard(self, panel: QtWidgets.QWidget, field: QtWidgets.QLineEdit):
        """Handle keyboard show"""
        self.previousPanel = panel
        self.currentField = field
        self.qwerty.set_value(field.text())
        self.setCurrentIndex(self.indexOf(self.qwerty))

    def on_qwerty_go_back(self):
        """Hide keyboard"""
        self.setCurrentIndex(self.indexOf(self.previousPanel))

    def on_qwerty_value_selected(self, value: str):
        """Handle keyboard value input"""
        self.setCurrentIndex(self.indexOf(self.previousPanel))
        if hasattr(self, "currentField") and self.currentField:
            self.currentField.setText(value)

    def info_box_load(self, toggle: bool = False) -> None:
        """
        Shows or hides the loading screen.
        Sets a 30-second timeout to handle loading failures.
        """
        self._show_loadscreen(toggle)

        self.panel.wifi_button.setEnabled(not toggle)
        self.panel.hotspot_button.setEnabled(not toggle)

        if toggle:
            if self._load_timer.isActive():
                self._load_timer.stop()
            self._load_timer.start(30000)

    def _handle_load_timeout(self):
        """
        Logic to execute if the loading screen is still visible after 30 seconds.<
        """
        wifi_btn = self.panel.wifi_button
        hotspot_btn = self.panel.hotspot_button

        if self.panel.loadingwidget.isVisible():
            if wifi_btn.toggle_button.state == wifi_btn.toggle_button.State.ON:
                message = "Wi-Fi Connection Failed.\nThe connection attempt \ntimed out.\n Please check\nyour network stability \nor\n try reconnecting."

            elif hotspot_btn.toggle_button.state == hotspot_btn.toggle_button.State.ON:
                message = "Hotspot Setup Failed.\nThe local network sharing\n timed out.\n\n restart the hotspot."
            else:
                message = "Loading timed out.\n Please check your connection \n and try again."

            self.panel.mn_info_box.setText(message)
            self._show_loadscreen(False)
            self._expand_infobox(True)

        hotspot_btn.setEnabled(True)
        wifi_btn.setEnabled(True)

    def _show_loadscreen(self, toggle: bool = False):
        """Expand LOAD box on the main network panel

        Args:
            toggle (bool, optional): show or not (Defaults to False)
        """
        self.panel.netlist_ip.setVisible(not toggle)
        self.panel.netlist_ssuid.setVisible(not toggle)
        self.panel.mn_info_seperator.setVisible(not toggle)
        self.panel.line_2.setVisible(not toggle)
        self.panel.netlist_strength.setVisible(not toggle)
        self.panel.netlist_strength_label.setVisible(not toggle)

        self.panel.line_3.setVisible(not toggle)
        self.panel.netlist_security.setVisible(not toggle)
        self.panel.netlist_security_label.setVisible(not toggle)

        self.panel.mn_info_box.setVisible(not toggle)

        self.panel.loadingwidget.setVisible(toggle)

    @QtCore.pyqtSlot(object, name="stateChange")
    def on_toggle_state(self, new_state) -> None:
        """Handle toggle button changes"""
        sender_button = self.sender()
        wifi_btn = self.panel.wifi_button.toggle_button
        hotspot_btn = self.panel.hotspot_button.toggle_button
        is_sender_now_on = new_state == sender_button.State.ON
        _old_hotspot = None

        saved_network = self.sdbus_network.get_saved_networks()

        if sender_button is wifi_btn:
            if is_sender_now_on:
                hotspot_btn.state = hotspot_btn.State.OFF
                self.sdbus_network.toggle_hotspot(False)
                if saved_network:
                    try:
                        ssid = next(
                            (
                                n["ssid"]
                                for n in saved_network
                                if "ap" not in n["mode"] and n["signal"] != 0
                            ),
                            None,
                        )
                        self.sdbus_network.connect_network(str(ssid))

                    except Exception as e:
                        logger.error(f"error when turning ON wifi on_toggle_state:{e}")

        elif sender_button is hotspot_btn:
            if is_sender_now_on:
                wifi_btn.state = wifi_btn.State.OFF

                for n in saved_network:
                    if "ap" in n.get("mode", ""):
                        _old_hotspot = n
                        break

                if (
                    _old_hotspot
                    and _old_hotspot["ssid"]
                    != self.panel.hotspot_name_input_field.text()
                ):
                    self.sdbus_network.delete_network(_old_hotspot["ssid"])

                self.sdbus_network.create_hotspot(
                    self.panel.hotspot_name_input_field.text(),
                    self.panel.hotspot_password_input_field.text(),
                )
                self.sdbus_network.toggle_hotspot(True)
                self.sdbus_network.connect_network(
                    self.panel.hotspot_name_input_field.text()
                )

        self.info_box_load(False)
        if (
            hotspot_btn.state == hotspot_btn.State.OFF
            and wifi_btn.state == wifi_btn.State.OFF
        ):
            self.evaluate_network_state()
        else:
            self.info_box_load(True)

    @QtCore.pyqtSlot(str, name="nm-state-changed")
    def evaluate_network_state(self, nm_state: str = "") -> None:
        """Handles or Reloads network state

        Args:
            nm_state (str, optional): Handles Network state depending on state
        """
        # NM State Constants: UNKNOWN=0, ASLEEP=10, DISCONNECTED=20, DISCONNECTING=30,
        # CONNECTING=40, CONNECTED_LOCAL=50, CONNECTED_SITE=60, GLOBAL=70

        wifi_btn = self.panel.wifi_button.toggle_button
        hotspot_btn = self.panel.hotspot_button.toggle_button
        _nm_state = nm_state

        if not _nm_state:
            _nm_state = self.sdbus_network.check_nm_state()
            if not _nm_state:
                return

        if self.start:
            self.start = False
            saved_network = self.sdbus_network.get_saved_networks()
            for n in saved_network:
                if "ap" in n.get("mode", ""):
                    _old_hotspot = n
                    break
            if _old_hotspot:
                self.panel.hotspot_name_input_field.setText(_old_hotspot["ssid"])

            connection = self.sdbus_network.check_connectivity()
            if connection == "FULL":
                self.panel.wifi_button.toggle_button.state = (
                    self.panel.wifi_button.toggle_button.State.ON
                )
                self.panel.hotspot_button.toggle_button.state = (
                    self.panel.hotspot_button.toggle_button.State.OFF
                )
            if connection == "LIMITED":
                self.panel.wifi_button.toggle_button.state = (
                    self.panel.wifi_button.toggle_button.State.OFF
                )
                self.panel.hotspot_button.toggle_button.state = (
                    self.panel.hotspot_button.toggle_button.State.ON
                )

        if not self.sdbus_network.check_wifi_interface():
            return

        if hotspot_btn.state == hotspot_btn.State.ON:
            ipv4_addr = self.get_hotspot_ip_via_shell()

            self.panel.netlist_ssuid.setText(self.panel.hotspot_name_input_field.text())

            self.panel.netlist_ip.setText(f"IP: {ipv4_addr or 'No IP Address'}")

            self.panel.netlist_strength.setText("--")

            self.panel.netlist_security.setText("--")

            self.panel.mn_info_box.setText("Hotspot On")

        if wifi_btn.state == wifi_btn.State.ON:
            ipv4_addr = self.sdbus_network.get_current_ip_addr()
            current_ssid = self.sdbus_network.get_current_ssid()
            if current_ssid == "":
                return
            sec_type = self.sdbus_network.get_security_type_by_ssid(current_ssid)
            signal_strength = self.sdbus_network.get_connection_signal_by_ssid(
                current_ssid
            )
            self.panel.netlist_ssuid.setText(current_ssid)
            self.panel.netlist_ip.setText(f"IP: {ipv4_addr or 'No IP Address'}")
            self.panel.netlist_security.setText(str(sec_type or "--").upper())
            self.panel.netlist_strength.setText(
                str(signal_strength if signal_strength != -1 else "--")
            )
            self.panel.mn_info_box.setText("Connected")

        self._expand_infobox(False)
        self.info_box_load(False)
        self.panel.wifi_button.setEnabled(True)
        self.panel.hotspot_button.setEnabled(True)
        self.repaint()

        if (
            wifi_btn.state == wifi_btn.State.OFF
            and hotspot_btn.state == hotspot_btn.State.OFF
        ):
            self.sdbus_network.disconnect_network()
            self._expand_infobox(True)
            self.panel.mn_info_box.setText(
                "Network connection required.\n\nConnect to Wi-Fi\nor\nTurn on Hotspot"
            )

    def get_hotspot_ip_via_shell(self):
        """
        Executes a shell command to retrieve the IPv4 address for a specified interface.

        Returns:
            The IP address string (e.g., '10.42.0.1') or None if not found.
        """
        command = [
            "ip",
            "a",
            "show",
            "wlan0",
            " |",
            "grep",
            " 'inet '",
            "|",
            "awk",
            " '{{print $2}}'",
            "|",
            "cut",
            "-d/",
            "-f1",
        ]
        try:
            result = subprocess.run(  # nosec: B603
                command,
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            ip_addr = result.stdout.strip()
            if ip_addr and len(ip_addr.split(".")) == 4:
                return ip_addr
        except subprocess.CalledProcessError as e:
            logging.error(
                "Caught exception (exit code %d) failed to run command: %s \nStderr: %s",
                e.returncode,
                command,
                e.stderr.strip(),
            )
            raise
        except subprocess.TimeoutExpired as e:
            logging.error("Caught exception, failed to run command %s", e)
            raise

    def close(self) -> bool:
        """Close class, close network module"""
        self.sdbus_network.close()
        return super().close()

    def _expand_infobox(self, toggle: bool = False) -> None:
        """Expand information box on the main network panel

        Args:
            toggle (bool, optional): Expand or not (Defaults to False)
        """
        self.panel.netlist_ip.setVisible(not toggle)
        self.panel.netlist_ssuid.setVisible(not toggle)
        self.panel.mn_info_seperator.setVisible(not toggle)
        self.panel.line_2.setVisible(not toggle)
        self.panel.netlist_strength.setVisible(not toggle)
        self.panel.netlist_strength_label.setVisible(not toggle)

        self.panel.line_3.setVisible(not toggle)
        self.panel.netlist_security.setVisible(not toggle)
        self.panel.netlist_security_label.setVisible(not toggle)

        self.panel.mn_info_box.setWordWrap(True)
        self.panel.mn_info_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    @QtCore.pyqtSlot(str, name="delete-network")
    def delete_network(self, ssid: str) -> None:
        """Delete network"""
        self.sdbus_network.delete_network(ssid=ssid)

    @QtCore.pyqtSlot(name="rescan-networks")
    def rescan_networks(self) -> None:
        """Rescan for networks"""
        self.sdbus_network.rescan_networks()

    @QtCore.pyqtSlot(name="handle-hotspot-back")
    def handle_hotspot_back(self) -> None:
        """Handle go back a page from hotspot page"""
        if (
            self.panel.hotspot_password_input_field.text()
            != self.sdbus_network.hotspot_password
        ):
            self.panel.hotspot_password_input_field.setText(
                self.sdbus_network.hotspot_password
            )
        if (
            self.panel.hotspot_name_input_field.text()
            != self.sdbus_network.hotspot_ssid
        ):
            self.panel.hotspot_name_input_field.setText(self.sdbus_network.hotspot_ssid)

        self.setCurrentIndex(self.indexOf(self.panel.main_network_page))

    @QtCore.pyqtSlot(name="add_network")
    def add_network(self) -> None:
        """Slot for adding a new network

        Emitted Signals:
            - add_network_confirmation(pyqtSignal): Signal with a dict that contains the result of adding a new network to the machine.

        """

        self.panel.add_network_validation_button.setEnabled(False)
        self.panel.add_network_validation_button.repaint()

        if not self.panel.add_network_password_field.text():
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Password field cannot be empty.",
            )
            return

        _network_psk = self.panel.add_network_password_field.text()
        result = self.sdbus_network.add_wifi_network(
            ssid=self.panel.add_network_network_label.text(), psk=_network_psk
        )

        error_msg = result.get("error", "")
        self.panel.add_network_password_field.clear()
        if not error_msg:
            QtCore.QTimer().singleShot(5000, self.network_list_worker.build)
            QtCore.QTimer().singleShot(
                5000,
                lambda: self.sdbus_network.connect_network(
                    self.panel.add_network_network_label.text()
                ),
            )
            self.info_box_load(True)
            self.setCurrentIndex(self.indexOf(self.panel.main_network_page))
            self.panel.add_network_validation_button.setEnabled(True)

            self.panel.wifi_button.setEnabled(False)
            self.panel.hotspot_button.setEnabled(False)

            self.panel.add_network_validation_button.repaint()
            return

        if error_msg == "Invalid password":
            message = "Invalid password. Please try again"
        elif error_msg == "Network connection properties error":
            message = "Network connection properties error. Please try again"
        elif error_msg == "Permission Denied":
            message = "Permission Denied. Please try again"
        else:
            message = "Error while adding network. Please try again"
        self.panel.add_network_validation_button.setEnabled(True)
        self.panel.add_network_validation_button.repaint()
        self.popup.new_message(message_type=Popup.MessageType.ERROR, message=message)

    @QtCore.pyqtSlot(ListItem, name="ssid_item_clicked")
    def ssid_item_clicked(self, item: ListItem) -> None:
        """Handles when a network is clicked on the QListWidget.

        Args:
            item (QListWidgetItem): The list entry that was clicked
        """
        if not item:
            return

        _current_ssid_name = item.text
        self.selected_item = copy.copy(item)
        if _current_ssid_name in self.sdbus_network.get_saved_ssid_names():
            self.setCurrentIndex(self.indexOf(self.panel.saved_connection_page))
            self.panel.saved_connection_network_name.setText(str(_current_ssid_name))
        else:
            self.setCurrentIndex(self.indexOf(self.panel.add_network_page))
            self.panel.add_network_network_label.setText(str(_current_ssid_name))

    def update_network(
        self,
        ssid: str,
        password: typing.Union[str, None],
        new_ssid: typing.Union[str, None],
    ) -> None:
        """Update network information"""
        if not self.sdbus_network.is_known(ssid):
            return

        checked_btn = self.panel.priority_btn_group.checkedButton()
        if checked_btn == self.panel.high_priority_btn:
            priority = 90
        elif checked_btn == self.panel.low_priority_btn:
            priority = 20
        else:
            priority = 50

        self.sdbus_network.update_connection_settings(
            ssid=ssid, password=password, new_ssid=new_ssid, priority=priority
        )
        QtCore.QTimer().singleShot(10000, lambda: self.network_list_worker.build())
        self.setCurrentIndex(self.indexOf(self.panel.network_list_page))

    @QtCore.pyqtSlot(list, name="finished-network-list-build")
    def handle_network_list(self, data: typing.List[typing.Tuple]) -> None:
        """Handle available network list update"""
        for entry in data:
            if entry[0] == self.sdbus_network.hotspot_ssid:
                continue
            self.saved_network[entry[0]] = (entry[1], entry[2])
        self.build_model_list()
        self.evaluate_network_state()
        QtCore.QTimer().singleShot(10000, lambda: self.network_list_worker.build())

    def handle_button_click(self, ssid: str):
        """Handles pressing a network"""
        _saved_ssids = self.sdbus_network.get_saved_networks()
        if any(item["ssid"] == ssid for item in _saved_ssids):
            self.setCurrentIndex(self.indexOf(self.panel.saved_connection_page))
            self.panel.saved_connection_network_name.setText(str(ssid))
            self.panel.snd_name.setText(str(ssid))

            # find the entry for this SSID
            entry = next((item for item in _saved_ssids if item["ssid"] == ssid), None)

            logger.debug(_saved_ssids)

            if entry is not None:
                priority = entry.get("priority")

                if priority == 90:
                    self.panel.high_priority_btn.setChecked(True)
                elif priority == 20:
                    self.panel.low_priority_btn.setChecked(True)
                else:
                    self.panel.med_priority_btn.setChecked(True)
            _curr_ssid = self.sdbus_network.get_current_ssid()
            if _curr_ssid != str(ssid):
                self.panel.network_activate_btn.setDisabled(False)
                self.panel.sn_info.setText("Saved Network")
            else:
                self.panel.network_activate_btn.setDisabled(True)
                self.panel.sn_info.setText("Active Network")

            self.panel.frame.repaint()

        else:
            self.setCurrentIndex(self.indexOf(self.panel.add_network_page))
            self.panel.add_network_network_label.setText(str(ssid))

    def setCurrentIndex(self, index: int):
        """Re-implementation of the QStackedWidget setCurrentIndex method
            in order to clear and display text as needed for each panel on the StackedWidget
        Args:
            index (int): The index we want to change to

        """
        if not self.isVisible():
            return
        _cur = self.currentIndex()
        if index == self.indexOf(self.panel.add_network_page):
            self.panel.add_network_password_field.clear()
            self.panel.add_network_password_field.setPlaceholderText(
                "Insert password here, press enter when finished."
            )
        elif index == self.indexOf(self.panel.saved_connection_page):
            self.panel.saved_connection_change_password_field.clear()
            self.panel.saved_connection_change_password_field.setPlaceholderText(
                "Change network password"
            )
            _security_type = self.sdbus_network.get_security_type_by_ssid(
                ssid=self.panel.saved_connection_network_name.text()
            )
            if not _security_type:
                _security_type = "--"
            self.panel.saved_connection_security_type_info_label.setText(
                str(_security_type)
            )
            _signal = self.sdbus_network.get_connection_signal_by_ssid(
                self.panel.saved_connection_network_name.text()
            )
            if _signal == -1:
                _signal = "--"
            _signal_string = f"{_signal}%"
            self.panel.saved_connection_signal_strength_info_frame.setText(
                _signal_string
            )
        self.update()
        super().setCurrentIndex(index)

    def setProperty(self, name: str, value: typing.Any) -> bool:
        """setProperty-> Intercept the set property method

        Args:
            name (str): Name of the dynamic property
            value (typing.Any): Value for the dynamic property

        Returns:
            bool: Returns to the super class
        """
        if name == "backgroundPixmap":
            self.background = value
        return super().setProperty(name, value)

    @QtCore.pyqtSlot(name="call-network-panel")
    def show_network_panel(
        self,
    ) -> None:
        """Slot for displaying networkWindow Panel"""
        if not self.parent():
            return
        self.setCurrentIndex(self.indexOf(self.panel.network_list_page))
        _parent_size = self.parent().size()  # type: ignore
        self.setGeometry(0, 0, _parent_size.width(), _parent_size.height())
        self.updateGeometry()
        self.update()
        self.show()

    def add_network_entry(self, ssid: str, signal: int, is_saved: str) -> None:
        """Adds a new item to the list model"""

        wifi_pixmap = self._provider.get_pixmap(signal=signal, state=is_saved)
        ssid = ssid if ssid != "" else "UNKNOWN"
        item = ListItem(
            text=ssid,
            left_icon=wifi_pixmap,
            right_text=is_saved,
            right_icon=self.right_icon,
            selected=False,
            allow_check=False,
            _lfontsize=17,
            _rfontsize=12,
            height=80,
        )
        self.model.add_item(item)

    def _handle_scrollbar(self, value):
        self.panel.verticalScrollBar.blockSignals(True)
        self.panel.verticalScrollBar.setValue(value)
        self.panel.verticalScrollBar.blockSignals(False)

    def _setup_scrollbar(self) -> None:
        self.panel.verticalScrollBar.setMinimum(
            self.panel.listView.verticalScrollBar().minimum()
        )
        self.panel.verticalScrollBar.setMaximum(
            self.panel.listView.verticalScrollBar().maximum()
        )
        self.panel.verticalScrollBar.setPageStep(
            self.panel.listView.verticalScrollBar().pageStep()
        )

    def build_network_list(self) -> None:
        """Build available/saved network list with optimized palette setup."""

        def set_brush_for_all_groups(
            palette, role, color, style=QtCore.Qt.BrushStyle.SolidPattern
        ):
            """Helper to set a brush for Active, Inactive, and Disabled states."""
            brush = QtGui.QBrush(QtGui.QColor(*color))
            brush.setStyle(style)
            for group in [
                QtGui.QPalette.ColorGroup.Active,
                QtGui.QPalette.ColorGroup.Inactive,
                QtGui.QPalette.ColorGroup.Disabled,
            ]:
                palette.setBrush(group, role, brush)

        palette = QtGui.QPalette()

        set_brush_for_all_groups(palette, QtGui.QPalette.ColorRole.Button, (0, 0, 0, 0))
        set_brush_for_all_groups(palette, QtGui.QPalette.ColorRole.Window, (0, 0, 0, 0))

        set_brush_for_all_groups(
            palette,
            QtGui.QPalette.ColorRole.Base,
            (0, 0, 0),
            QtCore.Qt.BrushStyle.NoBrush,
        )
        set_brush_for_all_groups(
            palette, QtGui.QPalette.ColorRole.Highlight, (0, 120, 215, 0)
        )
        set_brush_for_all_groups(palette, QtGui.QPalette.ColorRole.Link, (0, 0, 255, 0))
        self.panel.listView.setPalette(palette)
