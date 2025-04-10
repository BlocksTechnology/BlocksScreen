import json
import logging
import threading
import typing

import websocket
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication


from events import (
    WebSocketDisconnected,
    WebSocketError,
    WebSocketMessageReceived,
    WebSocketOpen,
)
from lib.moonrest import MoonRest
from utils.RepeatedTimer import RepeatedTimer

_logger = logging.getLogger(name="logs/BlocksScreen.log")


class OneShotTokenError(Exception):
    """Raised when unable to get oneshot token to connect to a websocket"""

    def __init__(self, message="Unable to get oneshot token", errors=None) -> None:
        super(OneShotTokenError).__init__(message, errors)
        self.errors = errors
        self.message = message


class MoonWebSocket(QObject, threading.Thread):
    """MoonWebSocket class object for creating a websocket connection to Moonraker.

    This class handles all there is to do with connecting to Moonraker to gather information.
    Tries the to connect the the websocket, if no connection is established the class retries three times, after which it may or may not
    successfully connect to the websocket. If not sends an event accordingly, the user may then try to connect again.


    The class also exposes an api to use with moonraker.


    Args:
        QObject (QObject): Double inheritance from QObject.
        threading.Thread (threading.Thread): Double inheritance from threading.Thread

    Raises:
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_

    """

    QUERY_KLIPPY_TIMEOUT: int = 5
    connected = False
    connecting = False
    callback_table = {}
    _reconnect_count = 0
    max_retries = 3
    timeout = 3

    # @ Signals
    connecting_signal = pyqtSignal([int], [str], name="websocket_connecting")
    connected_signal = pyqtSignal(name="websocket-connected")
    connection_lost = pyqtSignal([str], name="websocket-connection-lost")
    klippy_connected_signal = pyqtSignal(bool, name="klippy_connection_status")
    klippy_state_signal = pyqtSignal(str, name="klippy_state")
    query_server_info_signal = pyqtSignal(name="query_server_information")

    def __init__(self, parent: QObject) -> None:
        super().__init__(parent)
        self.daemon = True
        # self._main_window = parent

        # * This information should be in a  configuration file
        # self.host: str | None = None
        # self.port: int | None = None

        self.ws: websocket.WebSocketApp | None = None
        self._callback = None
        self._wst = None
        self._request_id = 0
        self.request_table = {}
        self._moonRest = MoonRest()
        self.api: MoonAPI = MoonAPI(self, self)
        self._retry_timer: RepeatedTimer

        # * Websocket options
        websocket.setdefaulttimeout(self.timeout)

        # @ Signals
        self.query_server_info_signal.connect(self.api.query_server_info)
        self.query_klippy_status_timer = RepeatedTimer(
            self.QUERY_KLIPPY_TIMEOUT, self.query_server_info_signal.emit
        )

        _logger.info("Websocket object initialized")

    @pyqtSlot(name="retry-websocket-connection")
    def retry(self):
        if self.connecting is True and self.connected is False:
            return False
        self._reconnect_count = 0
        self.try_connection()

    def try_connection(self):
        self.connecting = True
        self._retry_timer = RepeatedTimer(self.timeout, self.reconnect)
        return self.connect()

    def reconnect(self):
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
                instance = QApplication.instance()
                if instance is not None:
                    instance.sendEvent(self.parent(), unable_to_connect_event)
                else:
                    raise TypeError("QApplication.instance expected ad non-None value")
            except Exception as e:
                _logger.error(
                    f"Error sending Event {unable_to_connect_event.__class__.__name__} | Error message caught : {e}"
                )
            _logger.info(
                "Maximum number of connection retries reached, Unable to establish connection with Moonraker"
            )
            return False

        # TODO: OR in the future maybe an event or something, a callback for example
        return self.connect()

    def connect(self) -> bool:
        if self.connected:
            _logger.info("Connection is established.")
            return True
        self._reconnect_count += 1
        self.connecting_signal[int].emit(int(self._reconnect_count))
        _logger.debug(
            f"Trying to establish connection with Moonraker, try number {self._reconnect_count}"
        )

        # * Request oneshot token
        # TODO Handle if i cannot connect to moonraker, request server.info and see if i get a result
        try:
            _oneshot_token = self._moonRest.get_oneshot_token()

            if _oneshot_token is None:
                raise OneShotTokenError("Unable to get oneshot token")
        except Exception as e:
            _logger.info(f"Unexpected error when trying to acquire oneshot token: {e}")
            return False

        # TODO: Get the url from the config file, rather than being statically set

        _url = f"ws://192.168.1.100:7125/websocket?token={_oneshot_token}"

        self.ws = websocket.WebSocketApp(
            _url,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message,
        )

        _kwargs = {"reconnect": self.timeout}  # FIXME: This goes nowhere
        self._wst = threading.Thread(
            name="websocket.run_forever", target=self.ws.run_forever, daemon=True
        )
        try:
            _logger.info("Starting Websocket")
            _logger.debug(self.ws.url)
            self._wst.start()
        except (
            Exception
        ) as e:  # TEST: Send an event here when connection is unsuccessful
            _logger.info(f"Unexpected while starting websocket {self._wst.name}: {e}")
            return False
        return True

    # TODO: messages from *args, and pass it to other variables.
    def disconnect(self):
        # TODO: Handle disconnect or close state
        if self._wst is not None and self.ws is not None:
            self.ws.close()

            if self._wst.is_alive():
                self._wst.join()
            # self.join()
            # self.ws.close()

            _logger.info("Websocket closed")

    def on_error(self, *args) -> None:
        # First argument is ws second is error message
        # TODO: Handle error messages
        _error = args[1] if len(args) == 2 else args[0]
        _logger.info(f"Websocket error, disconnected: {_error}")
        self.connected = False
        self.disconnected = True

    def on_close(self, *args):
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
            instance = QApplication.instance()
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

    def on_open(self, *args):
        # TODO: Handle initial connection as per moonraker api documentation
        _ws = args[0] if len(args) == 1 else None
        self.connecting = False
        self.connected = True

        # Query server information, for klippy status
        self.query_klippy_status_timer.startTimer()
        self.query_server_info_signal.emit()

        open_event = WebSocketOpen(data="Connected")
        try:
            # QCoreApplication.instance().sendEvent(
            # TODO: the location to send the event changed from self._main_window.start_window to just self._main_window
            instance = QApplication.instance()
            if instance is not None:
                instance.postEvent(self.parent(), open_event)
            else:
                raise TypeError("QApplication.instance expected non None value")
        except Exception as e:
            _logger.info(f"Unexpected error opening websocket: {e}")

        self.connected_signal.emit()
        self._retry_timer.stopTimer()

        _logger.info(f"Connection to websocket achieved on {_ws}")

    def on_message(self, *args):
        # First argument is ws second is message
        _message = args[1] if len(args) == 2 else args[0]
        # _logger.debug(f"Message received from the websocket: {_message}")
        response: dict = json.loads(_message)
        if "id" in response and response["id"] in self.request_table:
            _entry = self.request_table.pop(response["id"])
            # * Can query and send signals about klippy connection here
            if "server.info" in _entry[0]:
                if response["result"]["klippy_state"] == "ready":
                    # * If klippy reports ready stop accessing it's state
                    self.query_klippy_status_timer.stopTimer()

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
            # This is a message received without a request,
            # but with the method in the response
            message_event = WebSocketMessageReceived(
                method=str(response["method"]),
                data=response,
                metadata=None,
            )

        try:
            instance = QApplication.instance()
            if instance is not None:
                instance.sendEvent(self.parent(), message_event)
            else:
                raise TypeError("QApplication.instance expected non None value")
        except Exception as e:
            _logger.info(
                f"Unexpected error while creating websocket message event: {e}"
            )

    def send_request(self, method: str, params: dict = {}):
        if not self.connected or self.ws is None:
            return False

        self._request_id += 1
        # * Keep track of the sent requests and their id
        # TODO: This data structure could be better, think abou other implementations
        self.request_table[self._request_id] = [method, params]

        packet = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self._request_id,
        }
        self.ws.send(json.dumps(packet))

        _logger.debug(f"Sending method:{method} , id: {self._request_id}")
        return True

    # def event(self, a0: QtCore.QEvent) -> bool:
    #     return super().event(a0)

    # def customEvent(self, a0: QtCore.QEvent | None) -> None:
    #     if a0 is not None and (a0.type() == KlippyDisconnectedEvent.type() or a0.type() == KlippyShudownEvent.type()):
    #         # * Received notify_klippy_diconnected, start querying server inforamtion again to check if klipper is available
    #         print("Klipper reported shutdown or error")
    #         self.query_klippy_status_timer.startTimer()

    #     return super().customEvent(a0)


class MoonAPI(QObject):
    # TODO: Callbacks for each method
    # TODO: Finish the pyqt slots for needed requests on the API

    def __init__(self, parent: typing.Optional["QObject"], ws: MoonWebSocket):
        super(MoonAPI, self).__init__(parent)
        self._ws: MoonWebSocket = ws

    @pyqtSlot(name="query_klippy_status")
    def query_server_info(self):
        _logger.debug("Requested server.info")
        return self._ws.send_request(method="server.info")

    def identify_connection(
        self, client_name, version, type, url, access_token, api_key
    ):
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
        return self._ws.send_request(
            method="server.temperature_store",
            params={"include_monitors": include_monitors},
        )

    @pyqtSlot(name="query_printer_info")
    def request_printer_info(self):
        return self._ws.send_request(method="printer.info")

    @pyqtSlot(name="get_available_objects")
    def get_available_objects(self):
        return self._ws.send_request(method="printer.objects.list")

    @pyqtSlot(dict, name="query_object")
    def object_query(self, objects: dict):
        return self._ws.send_request(
            method="printer.objects.query", params={"objects": objects}
        )

    @pyqtSlot(dict, name="object_subscription")
    def object_subscription(self, objects: dict):
        return self._ws.send_request(
            method="printer.objects.subscribe", params={"objects": objects}
        )

    def query_endstops(self):
        return self._ws.send_request(method="printer.query_endstops.status")

    @pyqtSlot(str, name="run_gcode")
    def run_gcode(self, gcode: str):
        if isinstance(gcode, str) is False or gcode is None:
            return False
        return self._ws.send_request(
            method="printer.gcode.script", params={"script": gcode}
        )

    def gcode_help(self):
        return self._ws.send_request(method="printer.gcode.help")

    @pyqtSlot(str, name="start_print")
    def start_print(self, filename):
        return self._ws.send_request(
            method="printer.print.start", params={"filename": filename}
        )

    @pyqtSlot(name="pause_print")
    def pause_print(self):
        return self._ws.send_request(method="printer.print.pause")

    @pyqtSlot(name="resume_print")
    def resume_print(self):
        return self._ws.send_request(method="printer.print.resume")

    @pyqtSlot(name="stop_print")
    def cancel_print(self):
        return self._ws.send_request(method="printer.print.cancel")

    def machine_system(self):
        return self._ws.send_request(method="machine.shutdown")

    def machine_reboot(self):
        return self._ws.send_request(method="machine.reboot")

    def restart_server(self):
        return self._ws.send_request(method="server.restart")

    def restart_service(self, service):
        if service is None or isinstance(service, str) is False:
            return False
        return self._ws.send_request(
            method="machine.services.restart", params={"service": service}
        )

    @pyqtSlot(name="firmware_restart")
    def firmware_restart(self):
        """firmware_restart

        HTTP_REQUEST: POST /printer/firmware_restart

        JSON_RPC_REQUEST: printer.firmware_restart
        Returns:
            _type_: _description_
        """
        # REVIEW: Whether i should send a websocket request or a post with http
        # return self._ws._moonRest.firmware_restart() # With HTTP
        return self._ws.send_request(
            method="printer.firmware_restart"
        )  # With Websocket

    def stop_service(self, service):
        if service is None or isinstance(service, str) is False:
            return False
        return self._ws.send_request(
            method="machine.services.stop", params={"service": service}
        )

    def start_service(self, service):
        if service is None or isinstance(service, str) is False:
            return False
        return self._ws.send_request(
            method="machine.services.start", params={"service": service}
        )

    def get_sudo_info(self, permission: bool = False):
        if isinstance(permission, bool) is False:
            return False
        return self._ws.send_request(
            method="machine.sudo.info", params={"check_access": permission}
        )

    def get_usb_devices(self):
        return self._ws.send_request(method="machine.peripherals.usb")

    def get_serial_devices(self):
        return self._ws.send_request(method="machine.peripherals.serial")

    def get_video_devices(self):
        return self._ws.send_request(method="machine.peripherals.video")

    def get_cabus_devices(self, interface: str = "can0"):
        return self._ws.send_request(
            method="machine.peripherals.canbus", params={"interface": interface}
        )

    @pyqtSlot(name="api_request_file_list")
    def get_file_list(self, root_folder: str | None = None):
        # If the root argument is omitted the request will default to the gcodes root.
        if root_folder is None:
            return self._ws.send_request(method="server.files.list", params={})
        return self._ws.send_request(
            method="server.files.list", params={"root": root_folder}
        )

    def list_registered_roots(self):
        return self._ws.send_request(method="server.files.roots")

    @pyqtSlot(str, name="api_request_file_list")
    def get_gcode_metadata(self, filename_dir: str):
        if isinstance(filename_dir, str) is False or filename_dir is None:
            return False
        return self._ws.send_request(
            method="server.files.metadata", params={"filename": filename_dir}
        )

    def scan_gcode_metadata(self, filename_dir: str):
        if isinstance(filename_dir, str) is False or filename_dir is None:
            return False
        return self._ws.send_request(
            method="server.files.metascan", params={"filename": filename_dir}
        )

    @pyqtSlot(name="api_get_gcode_thumbnail")
    def get_gcode_thumbnail(self, filename_dir: str):
        if isinstance(filename_dir, str) is False or filename_dir is None:
            return False
        return self._ws.send_request(
            method="server.files.thumbnails", params={"filename": filename_dir}
        )

    @pyqtSlot(str, str, name="file_download")
    def download_file(self, root: str, filename: str):
        """download_file Retrieves file *filename* at root *root*, the filename must include the relative path if
        it is not in the root folder

        Args:
            root (str): root directory where the file lies
            filename (str): file to download

        Returns:
            _type_: _description_
        """
        if not isinstance(filename, str) or not isinstance(root, str):
            return False

        return self._ws._moonRest.get_request(f"/server/files/{root}/{filename}")

    # def upload_file(self, ) # TODO: Maybe this is not necessary but either way do it

    def get_dir_information(self, directory: str):
        if isinstance(directory, str) is False or directory is None:
            return False
        return self._ws.send_request(
            method="server.files.get_directory",
            params={"path": f"gcodes/{directory}", "extended": True},
        )

    def create_directory(self, directory: str):
        if isinstance(directory, str) is False or directory is None:
            return False
        return self._ws.send_request(
            method="server.files.post_directory",
            params={
                "path": f"gcodes/{directory}",
            },
        )

    def delete_directory(self, directory: str):
        if isinstance(directory, str) is False or directory is None:
            return False
        return self._ws.send_request(
            method="server.files.delete_directory",
            params={
                "path": f"gcodes/{directory}",
            },
        )

    def move_file(self, source_dir: str, dest_dir: str):
        if (
            isinstance(source_dir, str) is False
            or isinstance(dest_dir, str) is False
            or source_dir is None
            or dest_dir is False
        ):
            return False
        return self._ws.send_request(
            method="server.files.move", params={"source": source_dir, "dest": dest_dir}
        )

    def copy_file(self, source_dir: str, dest_dir: str):
        if (
            isinstance(source_dir, str) is False
            or isinstance(dest_dir, str) is False
            or source_dir is None
            or dest_dir is False
        ):
            return False
        return self._ws.send_request(
            method="server.files.copy", params={"source": source_dir, "dest": dest_dir}
        )

    def zip_archive(self, items: list):
        raise NotImplementedError()

    # !Can implement a jog queueu

    def list_announcements(self, include_dismissed: bool = False):
        return self._ws.send_request(
            method="server.announcements.list",
            params={"include_dismissed": include_dismissed},
        )

    def update_announcements(self):
        return self._ws.send_request(method="server.announcements.update")

    def dismiss_announcements(self, entry_id: str, wake_time: int = 600):
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
        return self._ws.send_request(method="server.announcements.feeds")

    def post_announcement_feed(self, announcement_name: str):
        if isinstance(announcement_name, str) is False or announcement_name is None:
            return False
        return self._ws.send_request(
            method="server.announcements.post_feed", params={"name": announcement_name}
        )

    def delete_announcement_feed(self, announcement_name: str):
        if isinstance(announcement_name, str) is False or announcement_name is None:
            return False
        return self._ws.send_request(
            method="server.announcements.delete_feed",
            params={"name": announcement_name},
        )

    # * WEBCAM

    def list_webcams(self):
        return self._ws.send_request(method="server.webcams.list")

    def get_webcam_info(self, uid: str):
        if isinstance(uid, str) is False or uid is None:
            return False
        return self._ws.send_request(
            method="server.webcams.get_info", params={"uid": uid}
        )

    # TODO: Can create a class that irs a URL type like i've done before to validate the links
    # TODO: There are more options in this section, alot more options, later see if it's worth to implement or not
    def add_update_webcam(self, cam_name: str, snapshot_url: str, stream_url: str):
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
        if isinstance(uid, str) is False or uid is None:
            return False
        return self._ws.send_request(
            method="server.webcams.delete_item", params={"uid": uid}
        )

    def test_webcam(self, uid: str):
        if isinstance(uid, str) is False or uid is None:
            return False
        return self._ws.send_request(method="server.webcams.test", params={"uid": uid})

    def list_notifiers(self):
        return self._ws.send_request(method="server.notifiers.list")

    # UPDATES

    def update_status(self, refresh: bool = False):
        return self._ws.send_request(
            method="machine.update.status", params={"refresh": refresh}
        )

    def refresh_update_status(self, name: str):
        if isinstance(name, str) is False or name is None:
            return False
        return self._ws.send_request(
            method="machine.update.refresh", params={"name": name}
        )

    def full_update(self):
        return self._ws.send_request(method="machine.update.full")

    def update_moonraker(self):
        return self._ws.send_request(method="machine.update.moonraker")

    def update_klipper(self):
        return self._ws.send_request(method="machine.update.klipper")

    def update_client(self, client_name: str):
        if isinstance(client_name, str) is False or client_name is None:
            return False
        return self._ws.send_request(method="machine.update.client")

    def update_system(self):
        return self._ws.send_request(method="machine.update.system")

    def recover_corrupt_repo(self, name: str, hard: bool = False):
        if isinstance(name, str) is False or name is None:
            return False
        return self._ws.send_request(
            method="machine.update.recover", params={"name": name, "hard": hard}
        )

    def rollback_update(self, name: str):
        if isinstance(name, str) is False or name is None:
            return False
        return self._ws.send_request(
            method="machine,update.rollback", params={"name": name}
        )

    # If moonraker [history] is configured
    def history_list(self, limit, start, since, before, order):
        # TODO:
        raise NotImplementedError
        return self._ws.send_request(
            method="server.history.list",
            params={
                "limit": limit,
                "start": start,
                "since": since,
                "before": before,
                "order": order,
            },
        )

    def history_job_totals(self):
        raise NotImplementedError
        return self._ws.send_request(method="server.history.totals")

    def history_reset_totals(self):
        raise NotImplementedError
        return self._ws.send_request(method="server.history.reset_totals")

    def history_get_job(self, uid: str):
        raise NotImplementedError
        return self._ws.send_request(
            method="server.history.get_job", params={"uid": uid}
        )

    def history_delete_job(self, uid: str):
        raise NotImplementedError
        # It is possible to replace the uid argument with all=true to delete all jobs in the history database.
        return self._ws.send_request(
            method="server.history.delete_job", params={"uid": uid}
        )


############################################################################################################################
# TODO: WEBSOCKET NOTIFICATIONS

# TODO: Pass the logger object instanteation to another class so that the main window defines and calls it
# TODO: make host, port and websocket name not static but a argument that can be feed in the class
# TODO: Create websocket connection for each user login, which means different api keys for each user

# TEST: Try and use multiprocessing as it sidesteps the GIL
