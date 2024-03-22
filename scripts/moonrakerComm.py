#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals, annotations
import threading
import json
import logging
import sys
import websocket
import json
from time import monotonic as monotonic_time
from threading import Timer
import json
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QEvent, QEventLoop, QCoreApplication

from scripts.util import RepeatedTimer
from scripts.moonrest import MoonRest


# My Logger object
logging.basicConfig(format="'%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s",
                    filename=r"E:\gitHub\Blocks_Screen\logFile.log", encoding="utf-8", level=logging.DEBUG)
_logger = logging.getLogger(__name__)

# TODO: make host, port and websocket name not static but a argument that can be feed in the class


class MoonWebSocket(QObject, threading.Thread):

    connected = False
    connecting = False
    callback_table = {}
    _reconnect_count = 0
    max_retries = 3
    timeout = 3

    message_signal = pyqtSignal()

    def __init__(self, mainWindow):
        # * Both lines bellow are the same shit i guess
        super(MoonWebSocket, self).__init__()
        self.daemon = True
        self._main_window = mainWindow
        # self.host: str=None
        # self.port: int = None
        # self.ws: websocket.WebSocketApp = None
        self._callback = None
        self._wst = None
        self._request_id = 0

        self._moonRest = MoonRest()
        self.api = MoonAPI(self)

        self._retry_timer: RepeatedTimer = None
        # ! Websocket options
        # websocket.enableTrace(True)
        websocket.setdefaulttimeout(self.timeout)

        # Events
        # ! Probably not needed, and may be deleted in the future 
        self.connectEvent = threading.Event()
        self.connectingEvent = threading.Event()
        self.disconnectEvent = threading.Event()

    def retry(self):
        _logger.info("Retrying connection.")

        self._reconnect_count = 0
        self.try_connection()

    # TODO: isinstance for each type
    def try_connection(self):
        self.connecting = True
        self.connectEvent.set()
        self._retry_timer = RepeatedTimer(self.timeout, self.reconnect)
        return self.connect()

    def reconnect(self):
        if self.connected:
            return True

        if self._reconnect_count >= self.max_retries:
            self._retry_timer.stopTimer()
            unable_to_connect_event = WebSocketErrorEvent(data="Unable to Connect to Websocket")
            try:
                QCoreApplication.sendEvent(self._main_window, unable_to_connect_event)
            except Exception as e:
                _logger.error(f"Error sending Event {unable_to_connect_event.__class__.__name__}")
            _logger.debug("Max number of connection retries reached.")
            _logger.info("Could not connect to moonraker.")
            return False
        _logger.info("Retrying connection to moonraker websocket.")

        # OR in the future maybe an event or something, a callback for example
        return self.connect()

    def connect(self):
        if self.connected:
            _logger.debug("Connection already established.")
            return True
        self._reconnect_count += 1
        _logger.debug(f"Connect try number:{self._reconnect_count}")

        # Request oneshot token
        # TODO Handle if i cannot connect to moonraker, request server.info and see if i get a result
        try:
            _oneshot_token = self._moonRest.get_oneshot_token()

        except Exception as e:
            _logger.debug("Unable to get oneshot token")
            return False
        self.ws = websocket.WebSocketApp(
            f"ws://localhost:7125/websocket?token={_oneshot_token}",
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message
        )

        _kwargs = {'reconnect': self.timeout}
        self._wst = threading.Thread(name="websocket.run_forever",
                                     target=self.ws.run_forever,
                                     daemon=True)  # , kwargs=_kwargs)
        try:
            _logger.info("Starting websocket.")
            _logger.debug(self.ws.url)
            self._wst.start()
        except Exception as e:
            _logger.info(e, exc_info=True)
            _logger.debug(f"Error starting websocket: {e}")
            return False
        return True

    # TODO: messages from *args, and pass it to other variables.
    def disconnect(self):
        # TODO: Handle disconnect or close state
        self.ws.close()
        # _logger.info("Socket disconnected:")

    def on_error(self, *args):  # ws, error):
        # First argument is ws second is error message
        _error = args[1] if len(args) == 2 else args[0]
        # TODO: Handle error messages
        _logger.info(f"Websocket error:{_error}")
        self.connected = False
        self.disconnected = True

    def on_close(self, *args):
        # First argument is ws, second is close status code, third is close message
        _close_status_code = args[1] if len(args) == 3 else None
        _close_message = args[2] if len(args) == 3 else None
        # _close_status_code, _close_message = args[1],args[2] if len(args) == 3 else None, None
        self.connected = False
        self.ws.keep_running = False
        # self.reconnect()

        _logger.info(
            f"Websocket closed, code: {_close_status_code}, message: {_close_message}")

    def on_open(self, *args):
        # TODO: Handle initial connection as per moonraker api documentation
        _ws = args[0] if len(args) == 1 else None
        self.connecting = False
        self.connected = True
        
        connecting_event = WebSocketConnectEvent(
            data="Connected")
        try:
            QCoreApplication.postEvent(self._main_window.start_window, connecting_event, 10000)
        except Exception as e:
            _logger.error(f"Error posting event: {e}")
            
        _logger.info(f"Connection to websocket made on {_ws}")
        # * Verify the connection is made
        self.api.query_server_info()

    def on_message(self, *args):  # ws, message):
        # TODO: Handle receiving message from websocket
        # First argument is ws second is message
        _message = args[1] if len(args) == 2 else args[0]
        _logger.debug(f"Message received from websocket: {_message}")
        response = json.loads(_message)

        # !         EXPERIMENTS WITH SIGNALS SLOTS AND EVENTS, ALL WORKING I GUESS
        # ? Signals and Slots or do i create an Event?
        # self.message_signal.emit()
        # _logger.info(json.loads(response))
        # ! An error on th websocket daemon appears when i call this message.
        message_event = WebSocketMessageReceivedEvent(
            data="websocket message", kwargs=response)
        try:
            QCoreApplication.postEvent(self._main_window, message_event, 10000)         # Queue, pop, push, definir prioridade do evento  
            QCoreApplication.sendEvent(self._main_window, message_event)                # Mais rapido e não ha queue
        except Exception as e:
            _logger.error(f"Error posting event: {e}")





    def send_request(self, method: str, params: dict = {}):
        # TODO: Missing callbacks in here
        if not self.connected:
            return False
        self._request_id += 1

        packet = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self._request_id
        }
        self.ws.send(json.dumps(packet))
        _logger.debug(f"Sending method:{method} , id: {self._request_id}")
        return True


class WebSocketMessageReceivedEvent(QEvent):
    message_event_type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, **kwargs):
        super(WebSocketMessageReceivedEvent, self).__init__(
            WebSocketMessageReceivedEvent.message_event_type)
        self.data = data
        self.kwargs = kwargs


class WebSocketDisconnectEvent(QEvent):
    """WebSocketDisconnectEvent Event for websocket diconnection to Moonraker

    Args:
        QEvent (__type__): QEvent type argument
    """
    wb_disconnect_event_type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        super(WebSocketDisconnectEvent, self).__init__(
            WebSocketDisconnectEvent.wb_disconnect_event_type)
        self.data = data
        self.args = args
        self.kwargs = kwargs


class KlipperConnectEvent(QEvent):
    """KlipperConnectEvent Event to klipper connection

    Args:
        QEvent (_type_): QEvent type argument
    """
    kp_connected_event_type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        super(KlipperConnectEvent, self).__init__(
            KlipperConnectEvent.kp_connected_event_type
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs


class WebSocketConnectEvent(QEvent):
    """WebSocketConnectEvent Event for websocket connection to Moonraker

    Args:
        QEvent (_type_): QEvent type argument
    """
    wb_connect_event_type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        super(WebSocketConnectEvent, self).__init__(
            WebSocketConnectEvent.wb_connect_event_type)
        self.data = data
        self.args = args
        self.kwargs = kwargs


class WebSocketErrorEvent(QEvent):
    """WebSocketErrorEvent Event for websocket error

    Args:
        QEvent (_type_): QEvent type argument
    """
    wb_error_event_type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        super(WebSocketErrorEvent, self).__init__(
            WebSocketErrorEvent.wb_error_event_type)
        self.data = data
        self.args = args
        self.kwargs = kwargs


class MoonAPI:
    # TODO: Callbacks for each method
    def __init__(self, ws):
        self._ws = ws

    def query_server_info(self):
        _logger.debug("Requested server.info")
        return self._ws.send_request(
            method="server.info"
        )

    def identify_connection(self, client_name, version, type, url, access_token, api_key):
        return self._ws.send_request(
            method="server.connection.identify",
            params={
                "client_name": client_name,
                "version": version,
                "type": type,
                "url": url,
                "access_token": access_token,
                "api_key": api_key
            }
        )

    def request_temperature_cached_data(self, include_monitors: bool = False):
        return self._ws.send_request(
            method="server.temperature_store",
            params={
                "include_monitors": include_monitors
            }
        )

    def get_available_objects(self):
        return self._ws.send_request(
            method="printer.objects.list"
        )

    def object_query(self, objects: dict, attributes: list[str]):
        # TODO: Finish
        # Check if the types are correct
        return self._ws.send_request(
            method="printer.objects.query",
            params={
                "objects": objects
            }
        )

    def object_subscription(self, objects: dict, attributes: list[str]):
        # TODO: finishi this
        return self._ws.send_request(
            method="printer.objects.subscribe",
            params={
                "objects": objects
            }
        )

    def query_endstops(self):
        return self._ws.send_request(
            method="printer.query_endstops.status"
        )

    def run_gcode(self, gcode: str):
        if isinstance(gcode, str) is False or gcode is None:
            return False
        return self._ws.send_request(
            method="printer.gcode.script",
            params={
                "script": gcode
            }
        )

    def gcode_help(self):
        return self._ws.send_request(
            method="printer.gcode.help"
        )

    def start_print(self, filename):
        return self._ws.send_request(
            method="printer.print.start",
            params={
                "filename": filename
            }
        )

    def pause_print(self):
        return self._ws.send_request(
            method="printer.print.pause"
        )

    def resume_print(self):
        return self._ws.send_request(
            method="printer.print.resume"
        )

    def cancel_print(self):
        return self._ws.send_request(
            method="printer.print.cancel"
        )

    def machine_system(self):
        return self._ws.send_request(
            method="machine.shutdown"
        )

    def machine_reboot(self):
        return self._ws.send_request(
            method="machine.reboot"
        )

    def restart_server(self):
        return self._ws.send_request(
            method="server.restart"
        )

    def restart_service(self, service):
        if service is None or isinstance(service, str) is False:
            return False
        return self._ws.send_request(
            method="machine.services.restart",
            params={
                "service": service
            }
        )

    def stop_service(self, service):
        if service is None or isinstance(service, str) is False:
            return False
        return self._ws.send_request(
            method="machine.services.stop",
            params={
                "service": service
            }
        )

    def start_service(self, service):
        if service is None or isinstance(service, str) is False:
            return False
        return self._ws.send_request(
            method="machine.services.start",
            params={
                "service": service
            }
        )

    def get_sudo_info(self, permission: bool = False):
        if isinstance(permission, bool) is False:
            return False
        return self._ws.send_request(
            method="machine.sudo.info",
            params={
                "check_access": permission
            }
        )

    def get_usb_devices(self):
        return self._ws.send_request(
            method="machine.peripherals.usb"
        )

    def get_serial_devices(self):
        return self._ws.send_request(
            method="machine.peripherals.serial"
        )

    def get_video_devices(self):
        return self._ws.send_request(
            method="machine.peripherals.video"
        )

    def get_cabus_devices(self, interface: str = "can0"):
        return self._ws.send_request(
            method="machine.peripherals.canbus",
            params={
                "interface": interface
            }
        )

    def get_file_list(self, root_folder: str):
        # If the root argument is omitted the request will default to the gcodes root.
        return self._ws.send_request(
            method="server.files.list",
            params={
                "root": root_folder
            }
        )

    def list_registered_roots(self):
        return self._ws.send_request(
            method="server.files.roots"
        )

    def get_gcode_metadata(self, filename_dir: str):
        if isinstance(filename_dir, str) is False or filename_dir is None:
            return False
        return self._ws.send_request(
            method="server.files.metadata",
            params={
                "filename": filename_dir
            }
        )

    def scan_gcode_metadata(self, filename_dir: str):
        if isinstance(filename_dir, str) is False or filename_dir is None:
            return False
        return self._ws.send_request(
            method="server.files.metascan",
            params={
                "filename": filename_dir
            }
        )

    def get_gcode_thumbnail(self, filename_dir: str):
        if isinstance(filename_dir, str) is False or filename_dir is None:
            return False
        return self._ws.send_request(
            method="server.files.thumbnails",
            params={
                "filename": filename_dir
            }
        )

    def get_dir_information(self, directory: str):
        if isinstance(directory, str) is False or directory is None:
            return False
        return self._ws.send_request(
            method="server.files.get_directory",
            params={
                "path": f"gcodes/{directory}",
                "extended": True
            }
        )

    def create_directory(self, directory: str):
        if isinstance(directory, str) is False or directory is None:
            return False
        return self._ws.send_request(
            method="server.files.post_directory",
            params={
                "path": f"gcodes/{directory}",
            }
        )

    def delete_directory(self, directory: str):
        if isinstance(directory, str) is False or directory is None:
            return False
        return self._ws.send_request(
            method="server.files.delete_directory",
            params={
                "path": f"gcodes/{directory}",
            }
        )

    def move_file(self, source_dir: str, dest_dir: str):
        if isinstance(source_dir, str) is False or isinstance(dest_dir, str) is False or \
                source_dir is None or dest_dir is False:
            return False
        return self._ws.send_request(
            method="server.files.move",
            params={
                "source": source_dir,
                "dest": dest_dir
            }
        )

    def copy_file(self, source_dir: str, dest_dir: str):
        if isinstance(source_dir, str) is False or isinstance(dest_dir, str) is False or \
                source_dir is None or dest_dir is False:
            return False
        return self._ws.send_request(
            method="server.files.copy",
            params={
                "source": source_dir,
                "dest": dest_dir
            }
        )

    def zip_archive(self, items: list):
        raise NotImplementedError()

    # !Can implement a jog queueu

    def list_announcements(self, include_dismissed: bool = False):
        return self._ws.send_request(
            method="server.announcements.list",
            params={
                "include_dismissed": include_dismissed
            }
        )

    def update_announcements(self):
        return self._ws.send_request(
            method="server.announcements.update"
        )

    def dismiss_announcements(self, entry_id: str, wake_time: int = 600):
        if isinstance(entry_id, str) is False or entry_id is None or isinstance(wake_time, int) is False:
            return False
        return self._ws.send_request(
            method="server.announcements.dismiss",
            params={
                "entry_id": entry_id,
                "wake_time": wake_time
            }
        )

    def list_announcements_feeds(self):
        return self._ws.send_request(
            method="server.announcements.feeds"
        )

    def post_announcement_feed(self, announcement_name: str):
        if isinstance(announcement_name, str) is False or announcement_name is None:
            return False
        return self._ws.send_request(
            method="server.announcements.post_feed",
            params={
                "name": announcement_name
            }
        )

    def delete_announcement_feed(self, announcement_name: str):
        if isinstance(announcement_name, str) is False or announcement_name is None:
            return False
        return self._ws.send_request(
            method="server.announcements.delete_feed",
            params={
                "name": announcement_name
            }
        )

    # * WEBCAM

    def list_webcams(self):
        return self._ws.send_request(
            method="server.webcams.list"
        )

    def get_webcam_info(self, uid: str):
        if isinstance(uid, str) is False or uid is None:
            return False
        return self._ws.send_request(
            method="server.webcams.get_info",
            params={
                "uid": uid
            }
        )

    # TODO: Can create a class that irs a URL type like i've done before to validate the links
    # TODO: There are more options in this section, alot more options, later see if it's worth to implement or not
    def add_update_webcam(self, cam_name: str, snapshot_url: str, stream_url: str):
        if isinstance(cam_name, str) is False or isinstance(snapshot_url, str) is False or \
                isinstance(stream_url, str) is False or cam_name is None or snapshot_url is None or \
                stream_url is None:
            return False
        return self._ws.send_request(
            method="server.webcams.post_item",
            params={
                "name": cam_name,
                "snapshot_url": snapshot_url,
                "stream_url": stream_url
            }
        )

    def delete_webcam(self, uid: str):
        if isinstance(uid, str) is False or uid is None:
            return False
        return self._ws.send_request(
            method="server.webcams.delete_item",
            params={
                "uid": uid
            }
        )

    def test_webcam(self, uid: str):
        if isinstance(uid, str) is False or uid is None:
            return False
        return self._ws.send_request(
            method="server.webcams.test",
            params={
                "uid": uid
            }
        )

    def list_notifiers(self):
        return self._ws.send_request(
            method="server.notifiers.list"
        )

    # UPDATES

    def update_status(self, refresh: bool = False):
        return self._ws.send_request(
            method="machine.update.status",
            params={
                "refresh": refresh
            }
        )

    def refresh_update_status(self, name: str):
        if isinstance(name, str) is False or name is None:
            return False
        return self._ws.send_request(
            method="machine.update.refresh",
            params={
                "name": name
            }
        )

    def full_update(self):
        return self._ws.send_request(
            method="machine.update.full"
        )

    def update_moonraker(self):
        return self._ws.send_request(
            method="machine.update.moonraker"
        )

    def update_klipper(self):
        return self._ws.send_request(
            method="machine.update.klipper"
        )

    def update_client(self, client_name: str):
        if isinstance(client_name, str) is False or client_name is None:
            return False
        return self._ws.send_request(
            method="machine.update.client"
        )

    def update_system(self):
        return self._ws.send_request(
            method="machine.update.system"
        )

    def recover_corrupt_repo(self, name: str, hard: bool = False):
        if isinstance(name, str) is False or name is None:
            return False
        return self._ws.send_request(
            method="machine.update.recover",
            params={
                "name": name,
                "hard": hard
            }
        )

    def rollback_update(self, name: str):
        if isinstance(name, str) is False or name is None:
            return False
        return self._ws.send_request(
            method="machine,update.rollback",
            params={
                "name": name
            }
        )

    # If moonrakers [history] is configured
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
                "order": order
            }
        )

    def history_job_totals(self):
        raise NotImplementedError
        return self._ws.send_request(
            method="server.history.totals"
        )

    def history_reset_totals(self):
        raise NotImplementedError
        return self._ws.send_request(
            method="server.history.reset_totals"
        )

    def history_get_job(self, uid: str):
        raise NotImplementedError
        return self._ws.send_request(
            method="server.history.get_job",
            params={
                "uid": uid
            }
        )

    def history_delete_job(self, uid: str):
        raise NotImplementedError
        # It is possible to replace the uid argument with all=true to delete all jobs in the history database.
        return self._ws.send_request(
            method="server.history.delete_job",
            params={
                "uid": uid
            }
        )

    # TODO: WEBSOCKET NOTIFICATIONS


##############################################################################
# if __name__ == "__main__":
#     try:
#         _api = MoonRest()
#         wb = MoonWebSocket()
#         wb.start()
#         wb.try_connection()

#         while wb.is_alive:
#             if wb._request_id == 0:
#                 # wb.send_request("access.oneshot_token")
#                 wb.send_request("access.get_api_key")
#             if wb._request_id == 1:
#                 wb.send_request(method="server.info")

#             if wb._request_id == 2:
#                 wb.send_request(method="access.info")

#             if wb._request_id == 3:
#                 wb.send_request(method="access.users.list")
#             # _this_time = time.monotonic()
#             # _current = _this_time - _inital_time
#             # if _current > 2:
#             #     wb.disconnect()
#             # for thread in threading.enumerate():
#             #     print(thread.name)
#             wb.join(0.5)
#     except KeyboardInterrupt:
#         sys.exit(1)


# ! Can also connect to the moonraker using Unix Socket connection instead of websocket.
