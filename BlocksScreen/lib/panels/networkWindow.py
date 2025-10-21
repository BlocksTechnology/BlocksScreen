import enum
import logging
import typing
from functools import partial

from lib.network import SdbusNetworkManagerAsync
from lib.panels.widgets.popupDialogWidget import Popup
from lib.ui.wifiConnectivityWindow_ui import Ui_wifi_stacked_page
from lib.utils.list_button import ListCustomButton
from lib.panels.widgets.keyboardPage import CustomQwertyKeyboard
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger("logs/BlocksScreen.log")


class BuildNetworkList(QtCore.QThread):
    """Retrieves information from sdbus interface about scanned networks"""

    scan_result: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="scan-results"
    )
    finished_network_list_build: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        list, name="finished-network-list-build"
    )

    def __init__(self) -> None:
        super().__init__()
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.restart = False
        self.mutex.unlock()
        self.network_items_list = []
        self.nm = SdbusNetworkManagerAsync()
        if not self.nm:
            logger.error(
                "Cannot scan for networks, parent does not have \
                sdbus_network ('SdbusNetworkManagerAsync' instance class)"
            )
            return
        logger.info("Network Scanner Thread Initiated")

    def build(self) -> None:
        """Starts QThread"""
        with QtCore.QMutexLocker(self.mutex):
            if not self.isRunning():
                self.start(QtCore.QThread.Priority.LowPriority)
            else:
                self.restart = True
                self.condition.wakeOne()

    def stop(self):
        """Stops QThread execution"""
        self.mutex.lock()
        self.condition.wakeOne()
        self.mutex.unlock()
        self.deleteLater()

    def run(self) -> None:
        """BuildNetworkList main thread logic"""
        logger.debug("Scanning and building network list")
        while True:
            self.mutex.lock()
            self.network_items_list.clear()
            self.nm.rescan_networks()
            saved_ssids = self.nm.get_saved_ssid_names()
            saved_networks = self.nm.get_saved_networks()
            unsaved_networks = []
            networks = []
            if self.nm.check_wifi_interface():
                available_networks = self.nm.get_available_networks()
                if not available_networks:  # Skip everything if no networks exist
                    logger.debug("No available networks after scan")
                    self.finished_network_list_build.emit(self.network_items_list)
                    return
                for ssid_key in available_networks:
                    properties = available_networks.get(ssid_key, {})
                    signal = int(properties.get("signal_level", 0))
                    networks.append(
                        {
                            "ssid": ssid_key if ssid_key else "UNKNOWN",
                            "signal": signal,
                            "is_saved": bool(ssid_key in saved_ssids),
                        }
                    )
            if networks:
                saved_networks = sorted(
                    [n for n in networks if n["is_saved"]],
                    key=lambda x: -x["signal"],
                )
                unsaved_networks = sorted(
                    [n for n in networks if not n["is_saved"]],
                    key=lambda x: -x["signal"],
                )
            elif saved_networks:
                saved_networks = sorted([n for n in saved_networks], key=lambda x: -1)
            if saved_networks:
                for net in saved_networks:
                    ssid = net.get("ssid", "UNKNOWN")
                    signal = (
                        self.nm.get_connection_signal_by_ssid(ssid)
                        if ssid != "UNKNOWN"
                        else 0
                    )
                    if ssid == self.nm.get_current_ssid():
                        self.network_items_list.append((ssid, signal, "Active"))
                    else:
                        self.network_items_list.append((ssid, signal, "Saved"))
            if saved_networks and unsaved_networks:  # Separator
                self.network_items_list.append("separator")
            if unsaved_networks:
                for net in unsaved_networks:
                    ssid = net.get("ssid", "UNKNOWN")
                    signal = (
                        self.nm.get_connection_signal_by_ssid(ssid)
                        if ssid != "UNKNOWN"
                        else 0
                    )
                    self.network_items_list.append((ssid, signal, "Protected"))
            # Add a dummy blank space at the end if there are any unsaved networks
            if unsaved_networks:
                self.network_items_list.append("blank")

            self.finished_network_list_build.emit(self.network_items_list)
            if not self.restart:
                self.condition.wait(self.mutex)
            self.restart = False
            self.mutex.unlock()


class NetworkControlWindow(QtWidgets.QStackedWidget):
    """Network Control panel Widget"""
    request_network_scan = QtCore.pyqtSignal(name="scan-network")
    new_ip_signal = QtCore.pyqtSignal(str, name="ip-address-change")
    get_hotspot_ssid = QtCore.pyqtSignal(str, name="hotspot-ssid-name")
    delete_network_signal = QtCore.pyqtSignal(str, name="delete-network")

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget], /) -> None:
        super(NetworkControlWindow, self).__init__(parent)
        self.background: typing.Optional[QtGui.QPixmap] = None
        self.panel = Ui_wifi_stacked_page()
        self.panel.setupUi(self)
        self.popup = Popup(self)
        self.sdbus_network = SdbusNetworkManagerAsync()
        self.network_dead: bool = not self.sdbus_network.check_wifi_interface()

        # Network Scan
        self.network_list_widget = QtWidgets.QListWidget(
            parent=self.panel.network_list_page
        )
        self.build_network_list()

        self.network_list_worker = BuildNetworkList()
        self.network_list_worker.finished_network_list_build.connect(
            self.handle_network_list
        )
        self.panel.rescan_button.clicked.connect(
            lambda: QtCore.QTimer.singleShot(
                100, self.network_list_worker.build
            )
        )

        self.sdbus_network.nm_state_change.connect(self.evaluate_network_state)
        self.panel.wifi_button.clicked.connect(
            partial(
                self.setCurrentIndex,
                self.indexOf(self.panel.network_list_page),
            )
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

        self.panel.hotspot_password_input_field.installEventFilter(self)

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
        self.panel.saved_connection_change_password_field.returnPressed.connect(
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
        self.panel.hotspot_back_button.clicked.connect(self.handle_hotspot_back)

        self.panel.hotspot_password_input_field.setPlaceholderText(
            "Defaults to: 123456789"
        )
        self.panel.hotspot_change_confirm.clicked.connect(
            lambda: self.update_network(
                ssid=self.sdbus_network.get_hotspot_ssid(),
                password=self.panel.hotspot_password_input_field.text(),
                new_ssid=self.panel.hotspot_name_input_field.text(),
            )
        )

        self.panel.hotspot_change_confirm.clicked.connect(  
            lambda: self.setCurrentIndex(
                self.indexOf(self.panel.main_network_page)
            )
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
            QtGui.QPixmap(":/ui/dialog/btn_icons/on.svg")
        )

        self.panel.network_activate_btn.clicked.connect(
            lambda: self.sdbus_network.connect_network(
                self.panel.saved_connection_network_name.text()
            )
        )
        self.panel.network_delete_btn.clicked.connect(
            lambda: self.sdbus_network.delete_network(
                self.panel.saved_connection_network_name.text()
            )
        )

        self.network_list_worker.build()
        self.request_network_scan.emit()
        self.evaluate_network_state()
        self.hide()
        self.info_box_load()

        self.qwerty = CustomQwertyKeyboard(self)
        self.addWidget(self.qwerty)
        self.qwerty.value_selected.connect(self.on_qwerty_value_selected)
        self.qwerty.request_back.connect(self.on_qwerty_go_back)

        self.panel.add_network_password_field.clicked.connect(lambda: self.on_show_keyboard(self.panel.add_network_page, self.panel.add_network_password_field))
        self.panel.hotspot_password_input_field.clicked.connect(lambda: self.on_show_keyboard(self.panel.hotspot_page, self.panel.hotspot_password_input_field))
        self.panel.hotspot_name_input_field.clicked.connect(lambda: self.on_show_keyboard(self.panel.hotspot_page, self.panel.hotspot_name_input_field))
        self.panel.saved_connection_change_password_field.clicked.connect(lambda: self.on_show_keyboard(self.panel.saved_connection_page, self.panel.saved_connection_change_password_field))


    def on_show_keyboard(self, panel: QtWidgets.QWidget, field: QtWidgets.QLineEdit):
        self.previousPanel = panel
        print(self.previousPanel.objectName())
        self.currentField = field
        self.qwerty.set_value(field.text())
        self.setCurrentIndex(self.indexOf(self.qwerty))
            
    def on_qwerty_go_back(self):
        self.setCurrentIndex(self.indexOf(self.previousPanel))

    def on_qwerty_value_selected(self, value: str):
        QtWidgets.QApplication.instance().focusWidget().clearFocus()
        self.setCurrentIndex(self.indexOf(self.previousPanel))
        if hasattr(self, "currentField") and self.currentField:
            self.currentField.setText(value)

    def info_box_load(self, toggle: bool = False) -> None:
        if toggle:
            self.panel.netlist_ssuid.hide()
            self.panel.mn_info_seperator.hide()
            self.panel.netlist_ip.hide()

            self.panel.netlist_strength_label.hide()
            self.panel.line_2.hide()
            self.panel.netlist_strength.hide()

            self.panel.netlist_security_label.hide()
            self.panel.line_3.hide()
            self.panel.netlist_security.hide()

            self.panel.mn_info_box.hide()

            self.panel.loadingwidget.show()
        else:
            self.panel.netlist_ssuid.show()
            self.panel.mn_info_seperator.show()
            self.panel.netlist_ip.show()

            self.panel.netlist_strength_label.show()
            self.panel.line_2.show()
            self.panel.netlist_strength.show()

            self.panel.netlist_security_label.show()
            self.panel.line_3.show()
            self.panel.netlist_security.show()
        
            self.panel.mn_info_box.show()

            self.panel.loadingwidget.hide()

    @QtCore.pyqtSlot(enum.Enum, name="stateChange")
    def on_toggle_state(self, state) -> None:
        if (
            self.panel.wifi_button.toggle_button.state
            == self.panel.wifi_button.toggle_button.State.OFF
        ):
            self.panel.wifi_button.toggle_button.setDisabled(False)
            self.panel.hotspot_button.toggle_button.state = (
                self.panel.hotspot_button.toggle_button.State.OFF
            )
            self.panel.hotspot_button.toggle_button.setDisabled(True)
            self.sdbus_network.toggle_wifi(False)
            self.sdbus_network.toggle_hotspot(False)
        elif (
            self.panel.wifi_button.toggle_button.state
            == self.panel.wifi_button.toggle_button.State.ON
            and self.panel.hotspot_button.toggle_button.state
            == self.panel.hotspot_button.toggle_button.State.OFF
        ):
            self.panel.hotspot_button.toggle_button.state = (
                self.panel.hotspot_button.toggle_button.State.OFF
            )
            self.panel.wifi_button.toggle_button.setDisabled(False)
            self.panel.hotspot_button.toggle_button.setDisabled(False)
            self.sdbus_network.toggle_wifi(True)
            self.sdbus_network.toggle_hotspot(False)
        elif (
            self.panel.wifi_button.toggle_button.state
            == self.panel.wifi_button.toggle_button.State.ON
            and self.panel.hotspot_button.toggle_button.state
            == self.panel.hotspot_button.toggle_button.State.ON
        ):
            self.panel.wifi_button.toggle_button.setDisabled(True)
            self.panel.hotspot_button.toggle_button.setDisabled(False)
            self.sdbus_network.toggle_hotspot(True)
        elif (
            self.panel.hotspot_button.toggle_button.state
            == self.panel.hotspot_button.toggle_button.State.OFF
        ):
            self.panel.wifi_button.toggle_button.setDisabled(False)
            self.sdbus_network.toggle_hotspot(False)

    @QtCore.pyqtSlot(str, name="nm-state-changed")
    def evaluate_network_state(self, nm_state: str = "") -> None:
        # UNKNOWN = 0           # Networking state is unknown daemon error, assume connectivity might be present, may hide network accessibility
        # ASLEEP = 10           # networking is not enabled system is being suspended or resumed from suspend
        # DISCONNECTED = 20     # there is no active network connection
        # DISCONNECTING = 30    # network connections are being cleaned up
        # CONNECTING = 40       # network connection is being started
        # CONNECTED_LOCAL=50    # only local ipv4/ipv6 connectivity, no route to access internet
        # CONNECTED_SITE = 60   # site-wide ipv4/ipv4 connectivity
        # GLOBAL = 70           # Global ipv4/ipv6 internet connectivity, internet check succeeded, should display full connectivity
        _nm_state = nm_state
        if not _nm_state:
            _nm_state = self.sdbus_network.check_nm_state()
            if not _nm_state:
                return
        self.info_box_load(True)
        if _nm_state in ("CONNECTED_LOCAL", "CONNECTED_SITE", "GLOBAL"):
            if not self.sdbus_network.check_wifi_interface():
                self._expand_infobox(True)
                self.panel.mn_info_box.setText(
                    "No wifi interface detected.\nWifi and Hotspot unavailable\nResort to Ethernet connection."
                )
                self.panel.mn_info_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.panel.hotspot_button.setDisabled(True)
                self.panel.wifi_button.setDisabled(True)
                self.panel.wifi_button.toggle_button.state = (
                    self.panel.wifi_button.toggle_button.State.OFF
                )
                self.panel.wifi_button.toggle_button.state = (
                    self.panel.wifi_button.toggle_button.State.OFF
                )
                self.info_box_load(False)
                return

            logger.debug("Network Interface recognized, Connection available")
            self._expand_infobox(False)
            self.panel.hotspot_button.setDisabled(False)
            self.panel.wifi_button.setDisabled(False)
            if self.sdbus_network.wifi_enabled():
                self.panel.wifi_button.toggle_button.state = (
                    self.panel.wifi_button.toggle_button.State.ON
                )
            else:
                self.panel.wifi_button.toggle_button.state = (
                    self.panel.wifi_button.toggle_button.State.OFF
                )
                self.panel.hotspot_button.toggle_button.state = (
                    self.panel.hotspot_button.toggle_button.State.OFF
                )
            if self.sdbus_network.hotspot_enabled():
                self.panel.wifi_button.toggle_button.state = (
                    self.panel.wifi_button.toggle_button.State.ON
                )
                self.panel.hotspot_button.toggle_button.state = (
                    self.panel.hotspot_button.toggle_button.State.ON
                )
            ipv4_addr = self.sdbus_network.get_current_ip_addr()
            if not ipv4_addr:
                ipv4_addr = "No IP Address"
            self.panel.netlist_ip.setProperty("text_color", "white")
            self.panel.netlist_ip.setText(
                f"IP: {ipv4_addr}"
            )  # Set the current ip address on the network list page
            self.panel.mn_info_box.setText("Connected")
            current_ssid = self.sdbus_network.get_current_ssid()
            self.panel.netlist_ssuid.setText(current_ssid)
            sec_type = self.sdbus_network.get_security_type_by_ssid(current_ssid)
            if not sec_type:
                sec_type = "--"
            self.panel.netlist_security.setText(str(sec_type).upper())
            signal_strength = self.sdbus_network.get_connection_signal_by_ssid(
                current_ssid
            )
            if signal_strength == -1:
                signal_strength = "--"
            self.panel.netlist_strength.setText(str(signal_strength))
            self.info_box_load(False)
        else:
            self.info_box_load(False)
            self._expand_infobox(True)
            self.panel.mn_info_box.setText(
                "No Network connection\n Hotspot not enabled\nConnect to a network."
            )
            self.panel.mn_info_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            return

    def close(self) -> bool:
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
        # Align text
        self.panel.mn_info_box.setWordWrap(True)
        self.panel.mn_info_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    @QtCore.pyqtSlot(str, name="delete-network")
    def delete_network(self, ssid: str) -> None:
        self.sdbus_network.delete_network(ssid=ssid)

    @QtCore.pyqtSlot(name="rescan-networks")
    def rescan_networks(self) -> None:
        self.sdbus_network.rescan_networks()

    @QtCore.pyqtSlot(name="handle-hotspot-back")
    def handle_hotspot_back(self) -> None:
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
        # Check if a password was inserted

        if not self.panel.add_network_password_field.text():
            return
        _network_psk = self.panel.add_network_password_field.text()
        self.sdbus_network.add_wifi_network(
            ssid=self.panel.add_network_network_label.text(), psk=_network_psk
        )
        QtCore.QTimer().singleShot(10000, lambda: self.network_list_worker.build())
        self.setCurrentIndex(self.indexOf(self.panel.network_list_page))

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem, name="ssid_item_clicked")
    def ssid_item_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        """Handles when a network is clicked on the QListWidget.

        Args:
            item (QListWidgetItem): The list entry that was clicked
        """
        _current_item: QtWidgets.QWidget = (
            self.panel.network_list_widget.itemWidget(item)  # type: ignore
        )
        if _current_item:
            _current_ssid_name = _current_item.findChild(QtWidgets.QLabel).text()

            if (
                _current_ssid_name in self.sdbus_network.get_saved_ssid_names()
            ):  # Network already saved go to the information page
                self.setCurrentIndex(self.indexOf(self.panel.saved_connection_page))
                self.panel.saved_connection_network_name.setText(
                    str(_current_ssid_name)
                )
            else:  # Network not saved go to the add network page
                self.setCurrentIndex(self.indexOf(self.panel.add_network_page))
                self.panel.add_network_network_label.setText(
                    str(_current_ssid_name)
                )  # Add the network name to the title

    def update_network(
        self,
        ssid: str,
        password: typing.Union[str, None],
        new_ssid: typing.Union[str, None],
    ) -> None:
        if not self.sdbus_network.is_known(ssid):
            return

        self.sdbus_network.update_connection_settings(
            ssid=ssid,
            password=password,
            new_ssid=new_ssid,
        )
        QtCore.QTimer().singleShot(10000, lambda: self.network_list_worker.build())
        self.setCurrentIndex(self.indexOf(self.panel.network_list_page))

    def eventFilter(self, obj, event):
        if (
            obj == self.panel.hotspot_password_input_field
            or obj == self.panel.add_network_password_field
        ) and event.type() == QtCore.QEvent.Type.MouseButtonPress:
            self.panel.hotspot_password_input_field.setFocus()
            return True  # event handled
            # TODO: Open virtual keyboard here
            # subprocess.Popen(["onboard"])  # Open the virtual keyboard
        return super().eventFilter(obj, event)

    @QtCore.pyqtSlot(list, name="finished-network-list-build")
    def handle_network_list(self, data: typing.List[typing.Tuple]) -> None:
        scroll_bar_position = self.network_list_widget.verticalScrollBar().value()
        self.network_list_widget.blockSignals(True)
        self.network_list_widget.clear()
        self.network_list_widget.setSpacing(35)
        for entry in data:
            if entry == "separator":
                self.separator_item()
                continue
            elif entry == "blank":
                self.blank_space_item()
                continue
            if entry[0] == self.sdbus_network.hotspot_ssid:
                continue
            self.network_button_item(*entry)

        max_v = self.network_list_widget.verticalScrollBar().maximum()
        if scroll_bar_position > max_v:
            self.network_list_widget.verticalScrollBar().setValue(max_v)
        else:
            self.network_list_widget.verticalScrollBar().setValue(scroll_bar_position)
        self.network_list_widget.verticalScrollBar().update()
        self.network_list_widget.update()
        self.network_list_widget.blockSignals(False)
        QtCore.QTimer().singleShot(10000, lambda: self.network_list_worker.build())

    def handle_button_click(self, ssid: str):
        """Handles pressing a network"""
        if ssid in self.sdbus_network.get_saved_ssid_names():
            self.setCurrentIndex(self.indexOf(self.panel.saved_connection_page))
            self.panel.saved_connection_network_name.setText(str(ssid))
            _curr_ssid = self.sdbus_network.get_current_ssid()
            if _curr_ssid != str(ssid):
                self.panel.network_activate_btn.show()
            else:
                self.panel.network_activate_btn.hide()
            self.panel.frame.repaint()

        else:
            self.setCurrentIndex(self.indexOf(self.panel.add_network_page))
            self.panel.add_network_network_label.setText(str(ssid))

    def event(self, event: QtCore.QEvent) -> bool:
        """Receives PyQt eEvents, this method is reimplemented from the QEvent class

        Args:
            event (QtCore.QEvent)

        Returns:
            bool: Event has been handled or not 1
        """
        if event.type() == QtCore.QEvent.Type.ApplicationActivated:
            # Request a networks scan right at the start of the application
            self.request_network_scan.emit()
            return False
        return super().event(event)

    def setCurrentIndex(self, index: int):
        """Re-implementation of the QStackedWidget setCurrentIndex method
            in order to clear and display text as needed for each panel on the StackedWidget
        Args:
            index (int): The index we want to change to

        """
        if not self.isVisible():
            return
        _cur = self.currentIndex()
        if index == self.indexOf(self.panel.add_network_page):  # Add network page 2
            self.panel.add_network_password_field.clear()
            self.panel.add_network_password_field.setPlaceholderText(
                "Insert password here, press enter when finished."
            )
        elif index == self.indexOf(
            self.panel.saved_connection_page
        ):  # Network information page 3
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

    def build_network_list(self) -> None:
        """Build available/saved network list"""
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Button,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Base,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Window,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Highlight,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Link,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Button,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Base,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Window,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Highlight,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Link,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Button,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Base,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Window,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Highlight,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Link,
            brush,
        )
        self.network_list_widget.setPalette(palette)
        self.network_list_widget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.network_list_widget.setStyleSheet("background-color:transparent")
        self.network_list_widget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.network_list_widget.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.network_list_widget.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.network_list_widget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.network_list_widget.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.network_list_widget.setAutoScroll(False)
        self.network_list_widget.setProperty("showDropIndicator", False)
        self.network_list_widget.setDefaultDropAction(QtCore.Qt.DropAction.IgnoreAction)
        self.network_list_widget.setAlternatingRowColors(False)
        self.network_list_widget.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.NoSelection
        )
        self.network_list_widget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.network_list_widget.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.network_list_widget.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        QtWidgets.QScroller.grabGesture(
            self.network_list_widget,
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )
        QtWidgets.QScroller.grabGesture(
            self.network_list_widget,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )

        self.network_list_widget.setObjectName("network_list_widget")
        self.panel.nl_content_layout.addWidget(self.network_list_widget)

    def separator_item(self) -> None:
        """Add separator item to network list"""
        separator_item = QtWidgets.QListWidgetItem()
        separator_widget = QtWidgets.QLabel()
        separator_widget.setStyleSheet(
            "background-color: gray; margin: 1px 1px; min-height: 1px; max-height: 1px;"
        )
        separator_item.setSizeHint(QtCore.QSize(0, 2))  # Total vertical space: 2px
        self.network_list_widget.addItem(separator_item)
        self.network_list_widget.setItemWidget(separator_item, separator_widget)

    def blank_space_item(self) -> None:
        """Add blank space item to network list"""
        spacer_item = QtWidgets.QListWidgetItem()
        spacer_widget = QtWidgets.QWidget()
        spacer_widget.setFixedHeight(10)  # Adjust height as needed
        spacer_item.setSizeHint(spacer_widget.sizeHint())
        self.network_list_widget.addItem(spacer_item)
        self.network_list_widget.setItemWidget(spacer_item, spacer_widget)

    def network_button_item(self, ssid, signal, right_text, /) -> None:
        """Add a network entry to network list"""
        wifi_pixmap = QtGui.QPixmap(":/network/media/btn_icons/no_wifi.svg")
        if 70 <= signal <= 100:
            wifi_pixmap = QtGui.QPixmap(":/network/media/btn_icons/3bar_wifi.svg")
        elif signal >= 40:
            wifi_pixmap = QtGui.QPixmap(":/network/media/btn_icons/2bar_wifi.svg")
        elif 1 < signal < 40:
            wifi_pixmap = QtGui.QPixmap(":/network/media/btn_icons/1bar_wifi.svg")

        button = ListCustomButton(parent=self.network_list_widget)
        button.setText(ssid)
        button.setRightText(right_text)
        button.setPixmap(QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg"))
        button.setSecondPixmap(wifi_pixmap)
        button.setFixedHeight(80)
        button.setLeftFontSize(17)
        button.setRightFontSize(12)

        button.clicked.connect(lambda checked, s=ssid: self.handle_button_click(s))
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(button.sizeHint())
        self.network_list_widget.addItem(item)
        self.network_list_widget.setItemWidget(item, button)
