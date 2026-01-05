# Moonraker api
import json
import logging
import threading

import websocket
from events import (
    WebSocketDisconnected,
    WebSocketError,
    WebSocketMessageReceived,
    WebSocketOpen,
)
from lib.moonrest import MoonRest
from lib.utils.RepeatedTimer import RepeatedTimer
from PyQt6 import QtCore, QtWidgets

_logger = logging.getLogger(name="logs/BlocksScreen.log")


class OneShotTokenError(Exception):
    """Raised when unable to get oneshot token to connect to a websocket"""

    def __init__(self, message="Unable to get oneshot token", errors=None) -> None:
        super(OneShotTokenError).__init__(message, errors)
        self.errors = errors
        self.message = message


class MoonWebSocket(QtCore.QObject, threading.Thread):
    """MoonWebSocket class object for creating a websocket connection to Moonraker."""

    QUERY_KLIPPY_TIMEOUT: int = 2
    connected = False
    connecting = False
    callback_table = {}
    _reconnect_count = 0
    max_retries = 3
    timeout = 3

    connecting_signal = QtCore.pyqtSignal([int], [str], name="websocket_connecting")
    connected_signal = QtCore.pyqtSignal(name="websocket-connected")
    connection_lost = QtCore.pyqtSignal([str], name="websocket-connection-lost")
    klippy_connected_signal = QtCore.pyqtSignal(bool, name="klippy_connection_status")
    klippy_state_signal = QtCore.pyqtSignal(str, name="klippy_state")
    query_server_info_signal = QtCore.pyqtSignal(name="query_server_information")

    def __init__(self, parent: QtCore.QObject) -> None:
        super().__init__(parent)
        self.daemon = True

        self._host = parent.config.get("host", parser=str, default="localhost")
        self._port = parent.config.get("port", parser=int, default=7125)

        self.ws: websocket.WebSocketApp | None = None
        self._callback = None
        self._wst = None
        self._request_id = 0
        self.request_table = {}
        self._moonRest = MoonRest(host=self._host, port=self._port)
        self.api: MoonAPI = MoonAPI(self)
        self._retry_timer: RepeatedTimer
        websocket.setdefaulttimeout(self.timeout)

        self.query_server_info_signal.connect(self.api.api_query_server_info)
        self.query_klippy_status_timer = RepeatedTimer(
            self.QUERY_KLIPPY_TIMEOUT, self.query_server_info_signal.emit
        )

        self.klippy_state_signal.connect(self.api.request_printer_info)
        _logger.info("Websocket object initialized")

    @property
    def moonRest(self) -> MoonRest:
        """Returns the current moonrestAPI object"""
        return self._moonRest

    @QtCore.pyqtSlot(name="retry_wb_conn")
    def retry_wb_conn(self):
        """Retry websocket connection"""
        if self.connecting is True and self.connected is False:
            return False
        self._reconnect_count = 0
        self.try_connection()

    def try_connection(self):
        """Try connecting to websocket"""
        self.connecting = True
        self._retry_timer = RepeatedTimer(self.timeout, self.reconnect)
        return self.connect()

    def reconnect(self):
        """Reconnect to websocket"""
        if self.connected:
            return True

        if self._reconnect_count >= self.max_retries:
            self._retry_timer.stopTimer()
            unable_to_connect_event = WebSocketError(
                data="Unable to establish connection to Websocket"
            )
            self.connecting_signal[int].emit(0)
            self.connecting = False
            try:
                instance = QtWidgets.QApplication.instance()
                if instance is not None:
                    instance.sendEvent(self.parent(), unable_to_connect_event)
                else:
                    raise TypeError("QApplication.instance expected ad non-None value")
            except Exception as e:
                _logger.error(
                    f"Error on sending Event {unable_to_connect_event.__class__.__name__} | Error message: {e}"
                )
            _logger.info(
                "Maximum number of connection retries reached, Unable to establish connection with Moonraker"
            )
            return False
        return self.connect()

    def connect(self) -> bool:
        """Connect to websocket"""
        if self.connected:
            _logger.info("Connection established")
            return True
        self._reconnect_count += 1
        self.connecting_signal[int].emit(int(self._reconnect_count))
        _logger.debug(
            f"Establishing connection to Moonraker...\n Try number {self._reconnect_count}"
        )
        # TODO Handle if i cannot connect to moonraker, request server.info and see if i get a result
        try:
            _oneshot_token = self.moonRest.get_oneshot_token()
            if _oneshot_token is None:
                raise OneShotTokenError("Unable to retrieve oneshot token")
        except Exception as e:
            _logger.info(
                f"Unexpected error occurred when trying to acquire oneshot token: {e}"
            )
            return False

        _url = f"ws://{self._host}:{self._port}/websocket?token={_oneshot_token}"
        self.ws = websocket.WebSocketApp(
            _url,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message,
        )
        _kwargs = {"reconnect": self.timeout}  # FIXME: This goes nowhere

        self._wst = threading.Thread(
            name="websocket.run_forever",
            target=self.ws.run_forever,
            daemon=True,
        )
        try:
            _logger.info("Websocket Start...")
            _logger.debug(self.ws.url)
            self._wst.start()
        except Exception as e:
            _logger.info(f"Unexpected while starting websocket {self._wst.name}: {e}")
            return False
        return True

    def wb_disconnect(self) -> None:
        """Websocket disconnect"""
        if self._wst is not None and self.ws is not None:
            self.ws.close()
            if self._wst.is_alive():
                self._wst.join()
            _logger.info("Websocket closed")

    def on_error(self, *args) -> None:
        """Websocket error callback"""
        # First argument is ws second is error message
        # TODO: Handle error messages
        _error = args[1] if len(args) == 2 else args[0]
        _logger.info(f"Websocket error, disconnected: {_error}")
        self.connected = False
        self.disconnected = True

    def on_close(self, *args) -> None:
        """Websocket on close callback

        Raises:
            TypeError: When websocket Events cannot be sent because QApplication.instance `is` None
        """
        # First argument is ws, second is close status code, third is close message
        if self.ws is None:
            return
        _close_status_code = args[1] if len(args) == 3 else None
        _close_message = args[2] if len(args) == 3 else None
        self.connected = False
        self.ws.keep_running = False
        self.connection_lost[str].emit(
            f"code: {_close_status_code} | message {_close_message}"
        )
        close_event = WebSocketDisconnected(
            data="Disconnected", args=[_close_status_code, _close_message]
        )
        try:
            instance = QtWidgets.QApplication.instance()
            if instance is not None:
                instance.postEvent(self.parent(), close_event)
            else:
                raise TypeError("QApplication.instance expected non None value")
        except Exception as e:
            _logger.info(
                f"Unexpected error when sending websocket close_event on disconnection: {e}"
            )

        _logger.info(
            f"Websocket closed, code: {_close_status_code}, message: {_close_message}"
        )

    @QtCore.pyqtSlot(name="evaluate_klippy_status")
    def evaluate_klippy_status(self) -> None:
        """Query server information for klippy status"""
        self.query_klippy_status_timer.startTimer()
        self.query_server_info_signal.emit()

    def on_open(self, *args) -> None:
        """Websocket on open callback

        Raises:
            TypeError: When QApplication.instance `is` None
        """
        _ws = args[0] if len(args) == 1 else None
        self.connecting = False
        self.connected = True
        self.evaluate_klippy_status()
        open_event = WebSocketOpen(data="Connected")
        try:
            instance = QtWidgets.QApplication.instance()
            if instance is not None:
                instance.postEvent(self.parent(), open_event)
            else:
                raise TypeError("QApplication.instance expected non None value")
        except Exception as e:
            _logger.info(f"Unexpected error opening websocket: {e}")

        self.connected_signal.emit()
        self._retry_timer.stopTimer()
        _logger.info(f"Connection to websocket achieved on {_ws}")

    def on_message(self, *args) -> None:
        """Websocket on message callback

        Raises:
            TypeError: Raised when events cannot be sent because QApplication.instance is None
        """
        _message = (
            args[1] if len(args) == 2 else args[0]
        )  # First argument is ws second is message

        response: dict = json.loads(_message)
        if "id" in response and response["id"] in self.request_table:
            _entry = self.request_table.pop(response["id"])
            if "server.info" in _entry[0]:
                if response["result"]["klippy_state"] == "ready":
                    self.query_klippy_status_timer.stopTimer()
                    self.api.update_status()  # Request update status immediately after klippy ready DEVDEBT
                elif response["result"]["klippy_state"] == "startup":
                    # request server.info in 2 seconds
                    if not self.query_klippy_status_timer.running:
                        self.query_klippy_status_timer.startTimer()
                elif response["result"]["klippy_state"] == "disconnected":
                    if not self.query_klippy_status_timer.running:
                        self.query_klippy_status_timer.startTimer()
                self.klippy_connected_signal.emit(
                    response["result"]["klippy_connected"]
                )
                self.klippy_state_signal.emit(response["result"]["klippy_state"])
                return
            else:
                if "error" in response:
                    message_event = WebSocketMessageReceived(
                        method="error",
                        data=response["error"],
                        metadata=_entry,
                    )
                else:
                    message_event = WebSocketMessageReceived(
                        method=str(_entry[0]),
                        data=response["result"],
                        metadata=_entry,
                    )
        elif "method" in response:
            if (
                str(response["method"]).lower() == "notify_klippy_disconnected"
            ):  # Checkout for notify_klippy_disconnect
                self.evaluate_klippy_status()

            message_event = (
                WebSocketMessageReceived(  # mainly used to pass websocket notifications
                    method=str(response["method"]),
                    data=response,
                    metadata=None,
                )
            )

        try:
            instance = QtWidgets.QApplication.instance()
            if instance:
                instance.postEvent(self.parent(), message_event)
            else:
                raise TypeError("QApplication.instance expected non None value")
        except Exception as e:
            _logger.info(
                f"Unexpected error while creating websocket message event: {e}"
            )

    def send_request(self, method: str, params: dict = {}) -> bool:
        """Send a request over the websocket

        Args:
            method (str): Websocket method name
            params (dict, optional): parameters for the websocket method. Defaults to {}.

        Returns:
            bool: Whether the method finished and a request was sent
        """
        if not self.connected or self.ws is None:
            return False

        self._request_id += 1
        self.request_table[self._request_id] = [method, params]
        packet = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self._request_id,
        }
        self.ws.send(json.dumps(packet))
        return True


class MoonAPI(QtCore.QObject):
    def __init__(self, ws: MoonWebSocket):
        super(MoonAPI, self).__init__(ws)
        self._ws: MoonWebSocket = ws

    @QtCore.pyqtSlot(name="api_query_server_info")
    def api_query_server_info(self):
        """Query server information"""
        return self._ws.send_request(method="server.info")

    def identify_connection(
        self, client_name, version, type, url, access_token, api_key
    ):
        """Request moonraker to identify connection"""
        return self._ws.send_request(
            method="server.connection.identify",
            params={
                "client_name": client_name,
                "version": version,
                "type": type,
                "url": url,
                "access_token": access_token,
                "api_key": api_key,
            },
        )

    def request_temperature_cached_data(self, include_monitors: bool = False):
        """Request stored temperature monitors"""
        return self._ws.send_request(
            method="server.temperature_store",
            params={"include_monitors": include_monitors},
        )

    def request_server_info(self):
        """Requested printer information"""
        return self._ws.send_request(method="server.config")

    @QtCore.pyqtSlot(name="query_printer_info")
    def request_printer_info(self):
        """Requested printer information"""
        return self._ws.send_request(method="printer.info")

    @QtCore.pyqtSlot(name="get_available_objects")
    def get_available_objects(self):
        """Request available printer objects"""
        return self._ws.send_request(method="printer.objects.list")

    @QtCore.pyqtSlot(dict, name="query_object")
    def object_query(self, objects: dict):
        """Query printer object"""
        return self._ws.send_request(
            method="printer.objects.query", params={"objects": objects}
        )

    @QtCore.pyqtSlot(dict, name="object_subscription")
    def object_subscription(self, objects: dict):
        """Subscribe to printer object"""
        return self._ws.send_request(
            method="printer.objects.subscribe", params={"objects": objects}
        )

    @QtCore.pyqtSlot(name="ws_query_endstops")
    def query_endstops(self):
        """Query printer endstops"""
        return self._ws.send_request(method="printer.query_endstops.status")

    @QtCore.pyqtSlot(str, name="run_gcode")
    def run_gcode(self, gcode: str):
        """Run Gcode"""
        if isinstance(gcode, str) is False or gcode is None:
            return False
        return self._ws.send_request(
            method="printer.gcode.script", params={"script": gcode}
        )

    def gcode_help(self):
        """Request Gcode information"""
        return self._ws.send_request(method="printer.gcode.help")

    @QtCore.pyqtSlot(str, name="start_print")
    def start_print(self, filename):
        """Start print job"""
        return self._ws.send_request(
            method="printer.print.start", params={"filename": filename}
        )

    @QtCore.pyqtSlot(name="pause_print")
    def pause_print(self):
        """Pause print job"""
        return self._ws.send_request(method="printer.print.pause")

    @QtCore.pyqtSlot(name="resume_print")
    def resume_print(self):
        """Resume print job"""
        return self._ws.send_request(method="printer.print.resume")

    @QtCore.pyqtSlot(name="stop_print")
    def cancel_print(self):
        """Cancel print job"""
        return self._ws.send_request(method="printer.print.cancel")

    def machine_shutdown(self):
        """Request machine shutdown"""
        return self._ws.send_request(method="machine.shutdown")

    def machine_reboot(self):
        """Request machine reboot"""
        return self._ws.send_request(method="machine.reboot")

    def restart_server(self):
        """Request server restart"""
        return self._ws.send_request(method="server.restart")

    def restart_service(self, service):
        """Request service restart"""
        if service is None or isinstance(service, str) is False:
            return False
        return self._ws.send_request(
            method="machine.services.restart", params={"service": service}
        )

    def system_info(self):
        """Returns a top level System Info object containing various attributes that report info"""
        return self._ws.send_request(method="machine.system_info")

    @QtCore.pyqtSlot(name="firmware_restart")
    def firmware_restart(self):
        """Request Klipper firmware restart

        HTTP_REQUEST: POST /printer/firmware_restart

        JSON_RPC_REQUEST: printer.firmware_restart
        """
        return self._ws.send_request(method="printer.firmware_restart")

    def stop_service(self, service):
        """Request service stop"""
        if service is None or isinstance(service, str) is False:
            return False
        return self._ws.send_request(
            method="machine.services.stop", params={"service": service}
        )

    def start_service(self, service):
        """Request service start"""
        if service is None or isinstance(service, str) is False:
            return False
        return self._ws.send_request(
            method="machine.services.start", params={"service": service}
        )

    def get_sudo_info(self, permission: bool = False):
        """Request sudo privileges information"""
        if isinstance(permission, bool) is False:
            return False
        return self._ws.send_request(
            method="machine.sudo.info", params={"check_access": permission}
        )

    def get_usb_devices(self):
        """Request available usb devices"""
        return self._ws.send_request(method="machine.peripherals.usb")

    def get_serial_devices(self):
        """Request available serial devices"""
        return self._ws.send_request(method="machine.peripherals.serial")

    def get_video_devices(self):
        """Request available video devices"""
        return self._ws.send_request(method="machine.peripherals.video")

    def get_cabus_devices(self, interface: str = "can0"):
        """Request available CAN devices"""
        return self._ws.send_request(
            method="machine.peripherals.canbus",
            params={"interface": interface},
        )

    @QtCore.pyqtSlot(name="api-request-file-list")
    @QtCore.pyqtSlot(str, name="api-request-file-list")
    def get_file_list(self, root_folder: str = "gcodes"):
        """Get available files"""
        return self._ws.send_request(
            method="server.files.list", params={"root": root_folder}
        )

    @QtCore.pyqtSlot(name="api-list-roots")
    def list_registered_roots(self):
        """Get available root directories"""
        return self._ws.send_request(method="server.files.roots")

    @QtCore.pyqtSlot(str, name="api_request_file_list")
    def get_gcode_metadata(self, filename_dir: str):
        """Request gcode metadata"""
        if not isinstance(filename_dir, str) or not filename_dir:
            return False
        return self._ws.send_request(
            method="server.files.metadata", params={"filename": filename_dir}
        )

    @QtCore.pyqtSlot(str, name="api-scan-gcode-metadata")
    def scan_gcode_metadata(self, filename_dir: str):
        """Scan gcode metadata"""
        if isinstance(filename_dir, str) is False or filename_dir is None:
            return False
        return self._ws.send_request(
            method="server.files.metascan", params={"filename": filename_dir}
        )

    @QtCore.pyqtSlot(name="api_get_gcode_thumbnail")
    def get_gcode_thumbnail(self, filename_dir: str):
        """Request gcode thumbnail"""
        if isinstance(filename_dir, str) is False or filename_dir is None:
            return False
        return self._ws.send_request(
            method="server.files.thumbnails", params={"filename": filename_dir}
        )

    @QtCore.pyqtSlot(str, str, name="api-delete-file")
    @QtCore.pyqtSlot(str, name="api-delete-file")
    def delete_file(self, filename: str, root_dir: str = "gcodes"):
        """Request file deletion"""
        filepath = f"{root_dir}/{filename}"
        filepath = f"gcodes/{root_dir}/{filename}" if root_dir != "gcodes" else filepath
        return self._ws.send_request(
            method="server.files.delete_file",
            params={"path": filepath},
        )

    @QtCore.pyqtSlot(str, str, name="api-file_download")
    def download_file(self, root: str, filename: str):
        """Retrieves file *filename* at root *root*, the filename must include the relative path if
        it is not in the root folder

        Args:
            root (str): root directory where the file lies
            filename (str): file to download

        Returns:
            dict: The body of the response contains the contents of the requested file.
        """
        if not isinstance(filename, str) or not isinstance(root, str):
            return False

        return self._ws.moonRest.get_request(f"/server/files/{root}/{filename}")

    @QtCore.pyqtSlot(name="api-get-dir-info")
    @QtCore.pyqtSlot(str, name="api-get-dir-info")
    @QtCore.pyqtSlot(str, bool, name="api-get-dir-info")
    def get_dir_information(self, directory: str = "", extended: bool = True):
        """Request directory information"""
        if not isinstance(directory, str):
            return False
        return self._ws.send_request(
            method="server.files.get_directory",
            params={"path": f"gcodes/{directory}", "extended": extended},
        )

    def create_directory(self, directory: str):
        """Create directory"""
        if isinstance(directory, str) is False or directory is None:
            return False
        return self._ws.send_request(
            method="server.files.post_directory",
            params={
                "path": f"gcodes/{directory}",
            },
        )

    def delete_directory(self, directory: str):
        """Delete directory"""
        if isinstance(directory, str) is False or directory is None:
            return False
        return self._ws.send_request(
            method="server.files.delete_directory",
            params={
                "path": f"gcodes/{directory}",
            },
        )

    def move_file(self, source_dir: str, dest_dir: str):
        """Move file"""
        if (
            isinstance(source_dir, str) is False
            or isinstance(dest_dir, str) is False
            or source_dir is None
            or dest_dir is False
        ):
            return False
        return self._ws.send_request(
            method="server.files.move",
            params={"source": source_dir, "dest": dest_dir},
        )

    def copy_file(self, source_dir: str, dest_dir: str):
        """Copy file"""
        if (
            isinstance(source_dir, str) is False
            or isinstance(dest_dir, str) is False
            or source_dir is None
            or dest_dir is False
        ):
            return False
        return self._ws.send_request(
            method="server.files.copy",
            params={"source": source_dir, "dest": dest_dir},
        )

    def list_announcements(self, include_dismissed: bool = False):
        """Request available announcements"""
        return self._ws.send_request(
            method="server.announcements.list",
            params={"include_dismissed": include_dismissed},
        )

    def update_announcements(self):
        """Request announcements update to moonraker"""
        return self._ws.send_request(method="server.announcements.update")

    def dismiss_announcements(self, entry_id: str, wake_time: int = 600):
        """Dismiss announcements"""
        if (
            isinstance(entry_id, str) is False
            or entry_id is None
            or isinstance(wake_time, int) is False
        ):
            return False
        return self._ws.send_request(
            method="server.announcements.dismiss",
            params={"entry_id": entry_id, "wake_time": wake_time},
        )

    def list_announcements_feeds(self):
        """List announcement feeds"""
        return self._ws.send_request(method="server.announcements.feeds")

    def post_announcement_feed(self, announcement_name: str):
        """Post annoucement feeds"""
        if isinstance(announcement_name, str) is False or announcement_name is None:
            return False
        return self._ws.send_request(
            method="server.announcements.post_feed",
            params={"name": announcement_name},
        )

    def delete_announcement_feed(self, announcement_name: str):
        """Delete announcement feeds"""
        if isinstance(announcement_name, str) is False or announcement_name is None:
            return False
        return self._ws.send_request(
            method="server.announcements.delete_feed",
            params={"name": announcement_name},
        )

    def list_webcams(self):
        """List available webcams"""
        return self._ws.send_request(method="server.webcams.list")

    def get_webcam_info(self, uid: str):
        """Get webcamera information"""
        if isinstance(uid, str) is False or uid is None:
            return False
        return self._ws.send_request(
            method="server.webcams.get_info", params={"uid": uid}
        )

    def add_update_webcam(self, cam_name: str, snapshot_url: str, stream_url: str):
        """Add or update webcamera"""
        if (
            isinstance(cam_name, str) is False
            or isinstance(snapshot_url, str) is False
            or isinstance(stream_url, str) is False
            or cam_name is None
            or snapshot_url is None
            or stream_url is None
        ):
            return False
        return self._ws.send_request(
            method="server.webcams.post_item",
            params={
                "name": cam_name,
                "snapshot_url": snapshot_url,
                "stream_url": stream_url,
            },
        )

    def delete_webcam(self, uid: str):
        """Delete webcamera"""
        if isinstance(uid, str) is False or uid is None:
            return False
        return self._ws.send_request(
            method="server.webcams.delete_item", params={"uid": uid}
        )

    def test_webcam(self, uid: str):
        """Test webcamera connection"""
        if isinstance(uid, str) is False or uid is None:
            return False
        return self._ws.send_request(method="server.webcams.test", params={"uid": uid})

    def list_notifiers(self):
        """List configured notifiers"""
        return self._ws.send_request(method="server.notifiers.list")

    @QtCore.pyqtSlot(bool, name="update-status")
    def update_status(self, refresh: bool = False) -> bool:
        """Get packages state"""
        return self._ws.send_request(
            method="machine.update.status", params={"refresh": refresh}
        )

    @QtCore.pyqtSlot(name="update-refresh")
    @QtCore.pyqtSlot(str, name="update-refresh")
    def refresh_update_status(self, name: str = "") -> bool:
        """Refresh packages state"""
        if not isinstance(name, str) or not name:
            return False
        return self._ws.send_request(
            method="machine.update.refresh", params={"name": name}
        )

    @QtCore.pyqtSlot(name="update-full")
    def full_update(self) -> bool:
        """Issue full upgrade to all packages"""
        return self._ws.send_request(method="machine.update.full")

    @QtCore.pyqtSlot(name="update-moonraker")
    def update_moonraker(self) -> bool:
        """Issue moonraker update"""
        return self._ws.send_request(method="machine.update.moonraker")

    @QtCore.pyqtSlot(name="update-klipper")
    def update_klipper(self) -> bool:
        """Issue klipper update"""
        return self._ws.send_request(method="machine.update.klipper")

    @QtCore.pyqtSlot(str, name="update-client")
    def update_client(self, client_name: str = "") -> bool:
        """Issue client update"""
        if not isinstance(client_name, str) or not client_name:
            return False
        return self._ws.send_request(method="machine.update.client")

    @QtCore.pyqtSlot(name="update-system")
    def update_system(self):
        """Issue system update"""
        return self._ws.send_request(method="machine.update.system")

    @QtCore.pyqtSlot(str, name="recover-repo")
    @QtCore.pyqtSlot(str, bool, name="recover-repo")
    def recover_corrupt_repo(self, name: str, hard: bool = False):
        """Issue package recovery"""
        if isinstance(name, str) is False or name is None:
            return False
        return self._ws.send_request(
            method="machine.update.recover",
            params={"name": name, "hard": hard},
        )

    @QtCore.pyqtSlot(str, name="rollback-update")
    def rollback_update(self, name: str):
        """Issue rollback update"""
        if not isinstance(name, str) or not name:
            return False
        return self._ws.send_request(
            method="machine,update.rollback", params={"name": name}
        )

    def get_user(self):
        """Request current username"""
        return self._ws.send_request(method="access.get_user")

    def get_user_list(self):
        """Request users list"""
        return self._ws.send_request(method="access.users.list")

    def history_list(self, limit, start, since, before, order):
        """Request Job history list"""
        raise NotImplementedError

    def history_job_totals(self):
        """Request total job history"""
        raise NotImplementedError

    def history_reset_totals(self):
        """Request history reset"""
        raise NotImplementedError

    def history_get_job(self, uid: str):
        """Request job history"""
        raise NotImplementedError

    def history_delete_job(self, uid: str):
        """Request delete job history"""
        raise NotImplementedError
