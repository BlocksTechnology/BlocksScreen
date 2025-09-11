import logging
import typing
from functools import partial

from lib.network import SdbusNetworkManagerAsync
from lib.panels.widgets.popupDialogWidget import Popup
from lib.ui.wifiConnectivityWindow_ui import Ui_wifi_stacked_page
from lib.utils.list_button import ListCustomButton
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger("logs/BlocksScreen.log")


class NetworkControlWindow(QtWidgets.QStackedWidget):
    request_network_scan = QtCore.pyqtSignal(name="scan-network")
    new_ip_signal = QtCore.pyqtSignal(str, name="ip-address-change")
    get_hotspot_ssid = QtCore.pyqtSignal(str, name="hotspot-ssid-name")
    delete_network_signal = QtCore.pyqtSignal(str, name="delete-network")
    new_connection_result = QtCore.pyqtSignal(
        [],
        [
            str,
        ],
        name="new-connection-result",
    )

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget], /) -> None:
        super(NetworkControlWindow, self).__init__(parent)
        self.background: typing.Optional[QtGui.QPixmap] = None
        self.panel = Ui_wifi_stacked_page()
        self.panel.setupUi(self)
        self.popup = Popup(self)
        self.panel.network_list_widget.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.sdbus_network = SdbusNetworkManagerAsync()
        self.network_dead: bool = not self.sdbus_network.check_wifi_interface()

        self.sdbus_network.nm_state_change.connect(self.evaluate_network_state)

        self.panel.wifi_button.clicked.connect(
            partial(
                self.setCurrentIndex,
                self.indexOf(self.panel.wifi_page),
            )
        )
        self.panel.hotspot_button.clicked.connect(
            partial(
                self.setCurrentIndex, self.indexOf(self.panel.hotspot_page)
            )
        )

        self.panel.hotspot_button.setPixmap(
            QtGui.QPixmap(":/network/media/btn_icons/hotspot.svg")
        )
        self.panel.wifi_button.setPixmap(
            QtGui.QPixmap(":/network/media/btn_icons/wifi_config.svg")
        )

        self.panel.hotspot_password_input_field.installEventFilter(self)
        QtWidgets.QScroller.grabGesture(
            self.panel.network_list_widget,
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )
        QtWidgets.QScroller.grabGesture(
            self.panel.network_list_widget,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )

        self.panel.wifi_backButton.clicked.connect(
            partial(
                self.setCurrentIndex,
                self.indexOf(self.panel.network_list_page),
            )
        )
        self.panel.network_list_widget.itemClicked.connect(
            self.ssid_item_clicked
        )
        self.panel.network_backButton.clicked.connect(self.hide)
        self.panel.rescan_button.clicked.connect(
            lambda: self.sdbus_network.rescan_networks()
        )
        self.panel.rescan_button.clicked.connect(
            self.add_ssid_network_entry
        )  # To Update the network list
        self.request_network_scan.connect(self.rescan_networks)
        self.panel.add_network_validation_button.clicked.connect(
            self.add_network
        )
        self.panel.add_network_page_backButton.clicked.connect(
            partial(
                self.setCurrentIndex,
                self.indexOf(self.panel.wifi_page),
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
                self.indexOf(self.panel.wifi_page),
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
        self.panel.hotspot_back_button.clicked.connect(
            partial(
                self.setCurrentIndex,
                self.indexOf(self.panel.network_list_page),
            )
        )

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
        self.panel.hotspot_change_confirm.clicked.connect(  # Also goes back to the main page
            lambda: self.setCurrentIndex(
                self.indexOf(self.panel.network_list_page)
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
        self.new_connection_result.connect(self.process_new_connection_result)
        self.request_network_scan.emit()
        self.evaluate_network_state()
        self.hide()

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
        # logger.info(self.sdbus_network.primary_wifi_interface)

        if not _nm_state:
            _nm_state = self.sdbus_network.check_nm_state()
            if not _nm_state:
                return

        if _nm_state in ("CONNECTED_LOCAL", "CONNECTED_SITE", "GLOBAL"):
            if not self.sdbus_network.check_wifi_interface():
                self._expand_infobox(True)
                self.panel.mn_info_box.setText(
                    "No wifi interface detected.\nWifi and Hotspot unavailable\nResort to Ethernet connection."
                )
                self.panel.mn_info_box.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                )
                self.panel.hotspot_button.setDisabled(True)
                self.panel.wifi_button.setDisabled(True)
                self.panel.wifi_button.toggle_button.state = (
                    self.panel.wifi_button.toggle_button.State.OFF
                )
                self.panel.wifi_button.toggle_button.state = (
                    self.panel.wifi_button.toggle_button.State.OFF
                )
                return

            logger.debug("Network Interface recognized, Connection available")
            self._expand_infobox(False)
            self.panel.hotspot_button.setDisabled(False)
            self.panel.wifi_button.setDisabled(False)
            if self.sdbus_network.wifi_enabled():
                self.panel.wifi_button.toggle_button.state = (
                    self.panel.wifi_button.toggle_button.State.ON
                )
            if self.sdbus_network.hotspot_enabled():
                self.panel.wifi_button.toggle_button.state = (
                    self.panel.wifi_button.toggle_button.State.ON
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
            sec_type = self.sdbus_network.get_security_type_by_ssid(
                current_ssid
            )
            if not sec_type:
                sec_type = "--"
            self.panel.netlist_security.setText(str(sec_type).upper())
            signal_strength = self.sdbus_network.get_connection_signal_by_ssid(
                current_ssid
            )
            if signal_strength == -1:
                signal_strength = "--"
            self.panel.netlist_strength.setText(str(signal_strength))
            try:
                self.add_ssid_network_entry()
            except Exception as e:
                logger.error(
                    f"Exception caught while adding scanned networks{e}"
                )
        else:
            self._expand_infobox(True)
            self.panel.mn_info_box.setText(
                "No Network connection\n Hotspot not enabled\nConnect to a network."
            )
            self.panel.mn_info_box.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignCenter
            )
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
        self.panel.mn_info_box.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter
        )

    @QtCore.pyqtSlot(str, name="delete-network")
    def delete_network(self, ssid: str) -> None:
        self.sdbus_network.delete_network(ssid=ssid)

    @QtCore.pyqtSlot(name="rescan-networks")
    def rescan_networks(self) -> None:
        self.sdbus_network.rescan_networks()

    @QtCore.pyqtSlot(name="new-connection-result")
    @QtCore.pyqtSlot(str, name="new-connection-result")
    def process_new_connection_result(
        self, msg: typing.Optional[str] = None
    ) -> None:
        if msg:
            self.panel.add_network_password_field.setStyleSheet(
                "border: 2px solid red;"
            )
            self.panel.add_network_network_label.setText(msg)
            self.update()

        else:
            self.popup.new_message(
                self.popup.MessageType.INFO,
                message="Connection was added, no result message",
                persistent=False,
                timeout=200,
            )

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
        _add_network_result: typing.Dict = self.sdbus_network.add_wifi_network(
            ssid=self.panel.add_network_network_label.text(), psk=_network_psk
        )

        if any(
            word in _add_network_result.get("status", "")
            for word in ("error", "exception", "failure")
        ):
            self.new_connection_result[str].emit(
                str(_add_network_result.get("msg", ""))
            )
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message=f"Could not connect to '{self.panel.add_network_network_label.text()}'\n \
                    Please check your password or try again later.",
            )
        else:
            self.new_connection_result[str].emit(
                str(_add_network_result.get("msg", ""))
            )
            self.popup.new_message(
                message_type=Popup.MessageType.INFO,
                message=f"Connected to '{self.panel.add_network_network_label.text()}' successfully",
            )
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
            _current_ssid_name = _current_item.findChild(
                QtWidgets.QLabel
            ).text()

            if (
                _current_ssid_name in self.sdbus_network.get_saved_ssid_names()
            ):  # Network already saved go to the information page
                self.setCurrentIndex(
                    self.indexOf(self.panel.saved_connection_page)
                )
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

        _update_network_result: typing.Dict = (
            self.sdbus_network.update_connection_settings(
                ssid=ssid,
                password=password,
                new_ssid=new_ssid,
            )
        )

        if any(
            word in _update_network_result.get("status", "")
            for word in ("error", "exception", "failure")
        ):
            self.new_connection_result[str].emit(
                str(_update_network_result.get("msg", ""))
            )
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message=f"Could not update the settings for '{ssid}'",
            )

        else:
            self.new_connection_result[str].emit(
                str(_update_network_result.get("msg", ""))
            )
            self.popup.new_message(
                message_type=Popup.MessageType.INFO,
                message=f"Network settings for '{ssid}' updated successfully",
            )

    def eventFilter(self, obj, event):
        if (
            obj == self.panel.hotspot_password_input_field
            and event.type() == QtCore.QEvent.Type.MouseButtonPress
        ):
            self.panel.hotspot_password_input_field.setFocus()
            return True  # event handled
            # TODO: Open virtual keyboard here
            # subprocess.Popen(["onboard"])  # Open the virtual keyboard
        return super().eventFilter(obj, event)

    def add_ssid_network_entry(self) -> None:
        """Add scanned networks: saved go to network_list_widget, unsaved to network_list_widget_."""
        self.panel.network_list_widget.clear()
        self.panel.network_list_widget.setSpacing(35)

        saved_ssids = set(self.sdbus_network.get_saved_ssid_names())
        unsaved_networks = []
        saved_networks = self.sdbus_network.get_saved_networks()
        spacer_item = None
        spacer_widget = None
        networks = []
        if self.sdbus_network.check_wifi_interface():
            # available_networks = self.sdbus_network.get_available_networks()[
            #     0
            # ]  # unpack tuple
            available_networks: dict = (
                self.sdbus_network.get_available_networks()
            )
            # logger.info(available_networks)
            for item in available_networks:
                # logger.info(item)
                # if not isinstance(item, dict) or "ssid" not in item:
                #     continue
                # ssid = str(item["ssid"])

                # signal = self.sdbus_network.get_connection_signal_by_ssid(item)
                #
                signal = available_networks.get("signal_level", "0")
                try:
                    signal_value = int(signal)
                except (ValueError, TypeError):
                    signal_value = 0
                networks.append(
                    {
                        "ssid": item,
                        "signal": signal_value,
                        "is_saved": bool(item in saved_ssids),
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
        else:
            saved_networks = sorted(
                [n for n in saved_networks], key=lambda x: -1
            )

        for net in saved_networks:
            self._add_network_button(
                ssid=net.get("ssid", "UNKNOWN"),
                signal=net.get("signal", -1),
                right_text="Saved",
                target_widget=self.panel.network_list_widget,
            )

        if saved_networks and unsaved_networks:
            separator_item = QtWidgets.QListWidgetItem()
            separator_widget = QtWidgets.QLabel()
            separator_widget.setStyleSheet(
                "background-color: gray; margin: 1px 1px; min-height: 1px; max-height: 1px;"
            )
            separator_item.setSizeHint(
                QtCore.QSize(0, 2)
            )  # Total vertical space: 2px
            self.panel.network_list_widget.addItem(separator_item)
            self.panel.network_list_widget.setItemWidget(
                separator_item, separator_widget
            )

        for net in unsaved_networks:
            self._add_network_button(
                ssid=net.get("ssid", "UNKNOWN"),
                signal=net.get("signal", "0"),
                right_text="Protected",
                target_widget=self.panel.network_list_widget,
            )
        # Add a dummy blank space at the end if there are any unsaved networks
        if unsaved_networks:
            spacer_item = QtWidgets.QListWidgetItem()
            spacer_widget = QtWidgets.QWidget()
            spacer_widget.setFixedHeight(10)  # Adjust height as needed
            spacer_item.setSizeHint(spacer_widget.sizeHint())
            self.panel.network_list_widget.addItem(spacer_item)

        if spacer_item and spacer_widget:
            self.panel.network_list_widget.setItemWidget(
                spacer_item, spacer_widget
            )

    def _add_network_button(
        self,
        ssid: str,
        signal: int,
        right_text: str,
        target_widget: QtWidgets.QListWidget,
    ):
        """Helper to create and insert a network button into the given list widget."""
        if signal >= 70:
            wifi_pixmap = QtGui.QPixmap(
                ":/network/media/btn_icons/4bar_wifi.svg"
            )
        elif signal >= 40:
            wifi_pixmap = QtGui.QPixmap(
                ":/network/media/btn_icons/3bar_wifi.svg"
            )
        elif signal >= 20:
            wifi_pixmap = QtGui.QPixmap(
                ":/network/media/btn_icons/2bar_wifi.svg"
            )
        elif signal < 20:
            wifi_pixmap = QtGui.QPixmap(
                ":/network/media/btn_icons/1bar_wifi.svg"
            )
        else:
            wifi_pixmap = QtGui.QPixmap(
                ":/network/media/btn_icons/no_wifi.svg"
            )
        button = ListCustomButton(parent=target_widget)
        button.setText(ssid)
        button.setRightText(right_text)
        button.setPixmap(
            QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
        )
        button.setSecondPixmap(wifi_pixmap)
        button.setFixedHeight(80)
        button.setLeftFontSize(17)
        button.setRightFontSize(12)

        button.clicked.connect(
            lambda checked, s=ssid: self.handle_button_click(s)
        )

        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(button.sizeHint())
        target_widget.addItem(item)
        target_widget.setItemWidget(item, button)

    def handle_button_click(self, ssid: str):
        if ssid in self.sdbus_network.get_saved_ssid_names():
            self.setCurrentIndex(
                self.indexOf(self.panel.saved_connection_page)
            )
            self.panel.saved_connection_network_name.setText(str(ssid))

        else:
            self.setCurrentIndex(self.indexOf(self.panel.add_network_page))
            self.panel.add_network_network_label.setText(str(ssid))

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        """Controls UI aspects of the current panel, such as images

        Args:
            a0 (QPaintEvent)
        """
        if not self.isVisible():
            return super().paintEvent(a0)

        self.updateGeometry()

        # return super().paintEvent(a0)

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
        """Reimplementation of the QStackedWidget setCurrentIndex method
            in order to clear and display text as needed for each panel on the StackedWidget
        Args:
            index (int): The index we want to change to

        """
        if not self.isVisible():
            return

        _cur = self.currentIndex()
        if index == self.indexOf(self.panel.network_list_page):  # Main page 1
            self.panel.network_list_widget.clear()
            self.add_ssid_network_entry()  # Add network entries to the list
        elif index == self.indexOf(
            self.panel.add_network_page
        ):  # Add network page 2
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
        return super().setCurrentIndex(index)

    def sizeHint(self) -> QtCore.QSize:
        """
        When implementing a new widget, it is almost always useful to reimplement sizeHint() to provide a reasonable default size for the widget and to set the correct size policy with setSizePolicy().

        By default, composite widgets that do not provide a size hint will be sized according to the space requirements of their child widgets.

        The size policy lets you supply good default behavior for the layout management system, so that other widgets can contain and manage yours easily. The default size policy indicates that the size hint represents the preferred size of the widget, and this is often good enough for many widgets.

        Note: The size of top-level widgets are constrained to 2/3 of the desktop’s height and width. You can resize() the widget manually if these bounds are inadequate
        """
        return super().sizeHint()

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

    @QtCore.pyqtSlot(name="call_network_page")
    def call_network_panel(
        self,
    ) -> None:
        if not self.parent():
            return

        self.panel.network_list_widget.clear()
        self.setCurrentIndex(self.indexOf(self.panel.network_list_page))
        _parent_size = self.parent().size()
        self.setGeometry(0, 0, _parent_size.width(), _parent_size.height())
        self.updateGeometry()
        self.update()
        self.add_ssid_network_entry()
        self.show()
