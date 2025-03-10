import typing
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot, pyqtsignal


class MoonAPI(QtCore.QObject):
    """MoonAPI
         Moonraker API implementation


    Args:
         QObject (_type_): _description_

     Raises:
         NotImplementedError: _description_
         NotImplementedError: _description_
         NotImplementedError: _description_
         NotImplementedError: _description_
         NotImplementedError: _description_
         NotImplementedError: _description_

     Returns:
         _type_: _description_
    """

    # TODO: Callbacks for each method
    # TODO: Finish the pyqt slots for needed requests on the API

    def __init__(self, parent: typing.Optional["QObject"], ws: typing.MoonWebSocket):
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
        # TODO: Finish
        # Check if the types are correct
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
