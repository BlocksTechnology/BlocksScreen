from __future__ import annotations

import os

import events
from events import ReceivedFileData
from lib.moonrakerComm import MoonWebSocket
from PyQt6 import QtCore, QtGui, QtWidgets


class Files(QtCore.QObject):
    # @ Signals
    request_file_list = QtCore.pyqtSignal(name="get_files_list")
    request_file_metadata = QtCore.pyqtSignal([str], name="get_file_metadata")
    request_files_thumbnails = QtCore.pyqtSignal(
        [str], name="request_files_thumbnail"
    )
    request_file_download = QtCore.pyqtSignal([str, str], name="file_download")

    def __init__(
        self,
        parent: QtCore.QObject,
        ws: MoonWebSocket,
        update_interval: int = 5000,
    ) -> None:
        super(Files, self).__init__(parent)
        self.ws = ws
        self.gcode_path = os.path.expanduser("~/printer_data/gcodes")
        self.files: list = []
        self.files_metadata: dict = {}
        self.request_file_list.connect(slot=self.ws.api.get_file_list)
        self.request_file_metadata.connect(slot=self.ws.api.get_gcode_metadata)
        self.request_files_thumbnails.connect(
            slot=self.ws.api.get_gcode_thumbnail
        )
        self.request_file_download.connect(slot=self.ws.api.download_file)
        QtWidgets.QApplication.instance().installEventFilter(self)

    @property
    def file_list(self):
        return self.files

    def handle_message_received(self, method, data, params):
        if "server.files.list" in method:
            self.files.clear()
            self.files = data
            [
                self.request_file_metadata.emit(item["path"])
                for item in self.files
            ]
        elif "server.files.metadata" in method:
            if data["filename"] in self.files_metadata.keys():
                self.files_metadata.update({data["filename"]: data})
            else:
                self.files_metadata[data["filename"]] = data

    def event(self, a0: QtCore.QEvent) -> bool:
        if a0.type() == ReceivedFileData.type():
            if isinstance(a0, ReceivedFileData):
                self.handle_message_received(a0.method, a0.data, a0.params)
                return True  # Event Handled
        return super().event(a0)

    @QtCore.pyqtSlot(str, name="get_file_thumbnail")
    def get_file_thumbnail(self, filename) -> QtGui.QImage | None:
        if self.files_metadata is None or filename is None:
            return None

        if filename not in self.files_metadata.keys():
            return None

        metadata = self.files_metadata[filename]
        if "thumbnails" in metadata:
            _thumbnails = metadata.get("thumbnails")
            if not _thumbnails:
                return
            if _thumbnails[2].get("relative_path"):
                _thumb_relative_path = _thumbnails[2]["relative_path"]
            else:
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

    def eventFilter(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:
        if a1.type() == events.KlippyDisconnected.type():
            self.files_metadata.clear()
            self.files.clear()
            return False
        elif a1.type() == events.KlippyReady.type():
            self.request_file_list.emit()
            return False
        return super().eventFilter(a0, a1)


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
