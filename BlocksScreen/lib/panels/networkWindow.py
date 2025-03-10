import typing
from functools import partial

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QListWidgetItem, QStackedWidget, QWidget

from lib.ui.wifiConnectivityWindow_ui import Ui_wifi_stacked_page
from lib.bo.network import SdbusNetworkManager , SdbusNetworkManagerDummy

# TEST: Network saving, Adding new Network connections, Toggle on and off hotspot, etc....
# TODO: Complete this panel
# TODO: Add a Virtual Keyboard

class NetworkControlWindow(QStackedWidget):
    request_change_page = pyqtSignal(int, int, name="request_change_page")
    request_back_button_pressed = pyqtSignal(name="request_back_button_pressed")
    request_network_scan = pyqtSignal(name="scan_network")

    new_ip_signal = pyqtSignal(str, name="ip_address_change")
    get_hotspot_ssid = pyqtSignal(str, name="hotspot_ssid_name")
    delete_network_signal = pyqtSignal(str, name="delete_network")
    new_connection_result = pyqtSignal(
        [],
        [
            str,
        ],
        name="new_connection_result",
    )

    request_signal_strength = pyqtSignal(str, name="network_signal_strength")

    def __init__(self, parent: typing.Optional["QWidget"]) -> None:
        super(NetworkControlWindow, self).__init__(parent)

        self.main_panel = parent
        self.background: QtGui.QPixmap | None = None
        self.panel = Ui_wifi_stacked_page()
        self.panel.setupUi(self)
        self.panel.network_list_widget.setLayoutDirection(
            Qt.LayoutDirection.LeftToRight
        )
        # * Instantiate the network control class sdbus
        self.sdbus_network = SdbusNetworkManagerDummy()
        self.current_ip_address: typing.List | None = []
        # * Network List
        self.panel.network_list_widget.itemClicked.connect(self.ssid_item_clicked)
        self.panel.wifi_backButton.clicked.connect(self.hide)
        self.panel.rescan_button.clicked.connect(self.sdbus_network.rescan_networks)
        self.panel.rescan_button.clicked.connect(
            self.add_ssid_network_entry
        )  # To Update the network list
        self.panel.wifi_toggle_button.clicked.connect(
            partial(
                self.sdbus_network.toggle_wifi,
                toggle=not self.sdbus_network.wifi_enabled(),
            )
        )  # Turn off if enabled/Turn on if disabled
        self.request_network_scan.connect(self.rescan_networks)
        self.panel.call_hotspot_button.clicked.connect(
            partial(self.setCurrentIndex, 3)
        )  # Go to hotspot settings page
        # * Add Network page widget
        self.panel.add_network_validation_button.clicked.connect(self.add_network)
        self.panel.add_network_page_backButton.clicked.connect(
            partial(self.setCurrentIndex, 0)
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

        # * Saved Connection page widget
        self.panel.saved_connection_back_button.clicked.connect(
            partial(self.setCurrentIndex, 0)
        )  # Back button on this page always leads to the network list page
        self.delete_network_signal.connect(self.delete_network)
        self.panel.saved_connection_change_password_field.returnPressed.connect(
            partial(
                self.sdbus_network.update_connection_settings,
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
        self.panel.saved_connection_change_password_view.pressed.connect(
            partial(
                self.panel.saved_connection_change_password_field.setEchoMode,
                QtWidgets.QLineEdit.EchoMode.Password,
            )
        )

        # * Hotspot page
        self.panel.hotspot_toggle.clicked.connect(self.sdbus_network.toggle_hotspot)
        self.panel.hotspot_back_button.clicked.connect(partial(self.setCurrentIndex, 0))

        self.panel.hotspot_name_input_field.returnPressed.connect(
            partial(
                self.sdbus_network.update_connection_settings,
                ssid=self.sdbus_network.hotspot_ssid,
                password=None,
                new_ssid=self.panel.hotspot_name_input_field.text(),
            )
        )  # Automatically create a new hotspot connection when a new hotspot name is inserted and enter is pressed
        self.panel.hotspot_password_input_field.returnPressed.connect(
            partial(
                self.sdbus_network.update_connection_settings,
                ssid=self.sdbus_network.hotspot_ssid,
                password=self.panel.hotspot_password_input_field.text(),
                new_ssid=None,
            )
        )
        self.panel.hotspot_password_view_button.pressed.connect(
            partial(
                self.panel.hotspot_password_input_field.setEchoMode,
                QtWidgets.QLineEdit.EchoMode.Normal,
            )
        )
        self.panel.hotspot_password_view_button.released.connect(
            partial(
                self.panel.hotspot_password_input_field.setEchoMode,
                QtWidgets.QLineEdit.EchoMode.Password,
            )
        )
        self.new_connection_result.connect(self.process_new_connection_result)

        # * Set ip address boxes with the corresponding ip
        self.new_ip_signal.connect(partial(self.panel.hotspot_info_ip_field.setText))
        # * request a initial network scan
        self.request_network_scan.emit()
        self.hide()

    @pyqtSlot(str, name="delete_network")
    def delete_network(self, ssid: str) -> None:
        self.sdbus_network.delete_network(ssid=ssid)

    @pyqtSlot(name="rescan_networks")
    def rescan_networks(self) -> None:
        self.sdbus_network.rescan_networks()

    request_signal_strength = pyqtSignal(str, name="network_signal_strength")

    @pyqtSlot(str, name="network_signal_strength")
    def network_signal_strength(self, ssid: str):
        _strength = self.sdbus_network.get_connection_signal_by_ssid(ssid)

    @pyqtSlot(name="new_connection_result")
    @pyqtSlot(str, name="new_connection_result")
    def process_new_connection_result(self, msg: str | None):
        print("In the processingnn")
        if msg is not None:
            self.panel.add_network_password_field.setStyleSheet(
                "border: 2px solid red;"
            )
            self.panel.add_network_message_label.setText(msg)
            self.update()

        else:
            print("Connection was added, with no return message")

    @pyqtSlot(name="add_network")
    def add_network(self) -> None:
        """Slot for adding a new network

        Emitted Signals:
            - add_network_confirmation(pyqtSignal): Signal with a dict that contains the result of adding a new network to the machine.

        """
        # Check if a password was inserted

        if self.panel.add_network_password_field.text() is None:
            return
        _network_psk = self.panel.add_network_password_field.text()

        _add_network_result: typing.Dict = self.sdbus_network.add_wifi_network(
            ssid=self.panel.add_network_network_label.text(), psk=_network_psk
        )  # Add the network connection
        # Send a signal with the result of adding a new network
        if ("error" or "exception" or "failure") in _add_network_result["status"]:
            self.new_connection_result[str].emit(str(_add_network_result["msg"]))
        else:
            self.new_connection_result.emit()

    @pyqtSlot(QListWidgetItem, name="ssid_item_clicked")
    def ssid_item_clicked(self, item: QListWidgetItem) -> None:
        """Handles when a network is clicked on the QListWidget.

        Args:
            item (QListWidgetItem): The list entry that was clicked
        """
        _current_item: QWidget | None = self.panel.network_list_widget.itemWidget(item)

        if _current_item is not None:
            _current_ssid_name = _current_item.findChild(QtWidgets.QLabel).text()
            if (
                _current_ssid_name in self.sdbus_network.get_saved_ssid_names()
            ):  # Network already saved go to the information page
                self.setCurrentIndex(2)
                self.panel.saved_connection_network_name.setText(
                    str(_current_ssid_name)
                )
            else:  # Network not saved go to the add network page
                self.setCurrentIndex(1)
                self.panel.add_network_network_label.setText(
                    str(_current_ssid_name)
                )  # Add the network name to the title

    def add_ssid_network_entry(self) -> None:
        """Add scanned networks entries to listWidget"""
        index = 0
        self.panel.network_list_widget.clear()
        for item in self.sdbus_network.get_available_networks():
            if not isinstance(item, dict):
                continue
            if "ssid" in item.keys() and item is not None:
                results = self.configure_network_entry(str(item["ssid"]))
                # _item, _item_widget = self.configure_network_entry(str(item["ssid"]))
                if results is not None and isinstance(results, tuple):
                    _item, _item_widget = results
                    if (_item and _item_widget) is not None:
                        self.panel.network_list_widget.addItem(_item)
                        self.panel.network_list_widget.setItemWidget(
                            _item, _item_widget
                        )
                        index += 1

    @staticmethod
    def configure_network_entry(
        ssid: str,
    ) -> typing.Tuple[QtWidgets.QListWidgetItem, QWidget] | None:
        """Creates a QListWidgetItem to be inserted on the QListWidget with a network information.

        Args:
            ssid (str): String with the ssid of the network

        Returns:
            typing.Tuple[QtWidgets.QListWidgetItem, QWidget] | None: None if the argument is invalid, not a string
        """
        if not isinstance(ssid, str):
            return None

        _list_item = QtWidgets.QListWidgetItem()
        _list_item_widget = QWidget()
        _item_layout = QtWidgets.QHBoxLayout()
        _item_text = QtWidgets.QLabel()
        _item_button = QtWidgets.QPushButton()

        _item_button.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        _item_button.setStyleSheet("QPushButton{background:Transparent;}")

        _item_text.setText(str(ssid))
        _item_layout.addWidget(_item_text)
        _item_layout.addWidget(_item_button)
        _list_item_widget.setLayout(_item_layout)
        _list_item.setSizeHint(_list_item_widget.sizeHint())
        _item_button.setText(">")
        _size = _list_item_widget.geometry()
        _button_size = QtCore.QSize(50, 30)
        _item_button.setFixedSize(_button_size)
        _item_button.setBackgroundRole(QtGui.QPalette.ColorRole.Highlight)

        _list_item.setFlags(
            ~Qt.ItemFlag.ItemIsEditable
        )  # ~ is for making the item not editable

        return _list_item, _list_item_widget

    ####################################################################################
    # *     Reimplemented methods from parent class | Page index control methods     * #
    ####################################################################################

    def paintEvent(self, a0: QPaintEvent) -> None:
        """Controls UI aspects of the current panel, such as images

        Args:
            a0 (QPaintEvent)
        """
        if not self.isVisible():
            return super().paintEvent(a0)

        self.updateGeometry()

        return super().paintEvent(a0)

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
        if index == 0:  # Main page
            self.panel.network_list_widget.clear()
            self.add_ssid_network_entry()  # Add network entries to the list
        elif index == 1:  # Add network page
            self.panel.add_network_password_field.clear()
            self.panel.add_network_password_field.setPlaceholderText(
                "Insert password here, press enter when finished."
            )
        elif index == 2:  # Network information page
            self.panel.saved_connection_change_password_field.clear()
            self.panel.saved_connection_change_password_field.setPlaceholderText(
                "Change network password"
            )
            _security_type = self.sdbus_network.get_security_type_by_ssid(
                ssid=self.panel.saved_connection_network_name.text()
            )

            self.panel.saved_connection_security_type_info_label.setText(
                str(_security_type)
            )
            self.panel.saved_connection_signal_strength_info_frame.setText(
                f"{self.sdbus_network.get_connection_signal_by_ssid(self.panel.saved_connection_network_name.text())}%"
            )

        elif index == 3:  # Hotspot settings page
            self.panel.hotspot_info_ip_field.clear()
            self.panel.hotspot_name_input_field.clear()

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

    # @pyqtSlot(QtCore.QRect, "PyQt_PyObject", name="call_network_page")
    # @pyqtSlot(QtCore.QRect, name="call_network_page")
    @pyqtSlot(name="call_network_page")
    def call_network_panel(
        self,
    ) -> None:
        if self.main_panel is None:
            return

        self.panel.network_list_widget.clear()

        _main_size = self.main_panel.size()
        self.setGeometry(0, 0, _main_size.width(), _main_size.height())

        self.updateGeometry()
        self.add_ssid_network_entry()
        self.setCurrentIndex(0)
        self.show()


# TODO: Capture events to know when we have no network, in order to automatically enable the hotspot
# TODO: Add Icons to buttons and others to the panel
# TODO: Add a our custom q push buttons to make it pretty
# TODO: When adding a new connection, if the password is wrong, make the screen red or the input text box shake to indicate that it didn't work
# TODO: Add a button inside the item that permits the user to delete the network if it's saved or not
# TODO: On each entry on the networks list, make it so, there is an icon that also displays the signal strength, the wifi icon we have on the project
