from __future__ import annotations
import os

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import typing

from events import ReceivedFileData
from lib.moonrakerComm import MoonWebSocket


class Files(QtCore.QObject):
    # @ Signals
    request_file_list = pyqtSignal(name="get_files_list")
    request_file_metadata = pyqtSignal([str], name="get_file_metadata")
    request_files_thumbnails = pyqtSignal([str], name="request_files_thumbnail")
    request_file_download = pyqtSignal([str, str], name="file_download")

    def __init__(
        self,
        parent: typing.Optional["QObject"],
        ws: MoonWebSocket,
        update_interval: int = 5000,
    ) -> None:
        super(Files, self).__init__(parent)
        self.ws = ws

        self.gcode_path = os.path.expanduser("~/printer_data/gcodes")

        self.files: list = []
        self.files_metadata: dict = {}
        # @ Connect signals
        self.request_file_list.connect(slot=self.ws.api.get_file_list)
        self.request_file_metadata.connect(slot=self.ws.api.get_gcode_metadata)
        self.request_files_thumbnails.connect(slot=self.ws.api.get_gcode_thumbnail)
        self.request_file_download.connect(slot=self.ws.api.download_file)

    @property
    def file_list(self):
        return self.files

    def handle_message_received(self, method, data, params):
        if "server.files.list" in method:
            self.files.clear()
            self.files = data
            [self.request_file_metadata.emit(item["path"]) for item in self.files]

        elif "server.files.metadata" in method:
            if data["filename"] in self.files_metadata.keys():
                self.files_metadata.update({data["filename"]: data})
            else:
                self.files_metadata[data["filename"]] = data

    def event(self, a0: QtCore.QEvent) -> bool:
        if a0.type() == ReceivedFileData.type():
            if isinstance(a0, ReceivedFileData):
                self.handle_message_received(a0.method, a0.data, a0.params)
                # Handled
                return True
        return super().event(a0)

    @pyqtSlot(str, name="get_file_thumbnail")
    def get_file_thumbnail(self, filename) -> QtGui.QImage | None:
        if self.files_metadata is None or filename is None:
            return None

        if filename not in self.files_metadata.keys():
            return None

        metadata = self.files_metadata[filename]

        if "thumbnails" in metadata:
            _thumbnails = metadata["thumbnails"]
            _thumb_relative_path = _thumbnails[1]["relative_path"]
            path = os.path.join(
                os.path.dirname(os.path.join(self.gcode_path, filename)),
                _thumb_relative_path,
            )
            if os.access(path, os.R_OK):  # Has access to the thumbnail
                return QtGui.QImage(path)
            else:  # Does not have access to the thumbnail, check if i can download the file from moonraker
                return self.request_file_download[str, str].emit(
                    "~/printer_data/gcodes/.thumbs", filename
                )

        return None


# _image = None
#                 _item_thumbnail = _item_metadata["thumbnails"][1]["relative_path"]
#                 # TODO: Better paths, need to do this in a better way
#                 path = os.path.join(
#                     os.path.dirname(
#                         os.path.join(self.gcode_path, self._current_file_name)
#                     ),
#                     _item_thumbnail,
#                 )
#                 if os.access(path, os.R_OK): # Can access the image and the directory it resides
#                     _image = QtGui.QImage(path)
