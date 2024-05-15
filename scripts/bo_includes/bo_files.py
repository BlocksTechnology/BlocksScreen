from __future__ import annotations

import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer
import typing

from scripts.events import *
from scripts.moonrakerComm import MoonWebSocket


class Files(QtCore.QObject):

    # @ Signals
    request_file_list = pyqtSignal(name="get_files_list")
    request_file_metadata = pyqtSignal([str], name="get_file_metadata")
    request_files_thumbnails = pyqtSignal([str], name="request-files-thumbnail")

    def __init__(
        self,
        parent: typing.Optional["QObject"],
        ws: MoonWebSocket,
        update_interval: int = 5000,
    ) -> None:

        super(Files, self).__init__(parent)
        self.ws = ws
        self.directories: dict = {}
        self.files: list = []
        self.thumbnails: dict = {}
        self.files_metadata: dict = {}
        # @ Connect signals
        self.request_file_list.connect(slot=self.ws.api.get_file_list)
        self.request_file_metadata.connect(slot=self.ws.api.get_gcode_metadata)
        self.request_files_thumbnails.connect(slot=self.ws.api.get_gcode_thumbnail)

    @property
    def file_list(self):
        return self.files

    @property
    def directories_list(self):
        return self.directories

    def handle_message_received(self, method, data, params):
        if "server.files.list" in method:
            self.files.clear()
            # self.update_file_list_timer.stop()
            self.files = data
            # print(self.files)
            [self.request_file_metadata.emit(item["path"]) for item in self.files]

        elif "server.files.metadata" in method:
            if data["filename"] in self.files_metadata.keys():
                self.files_metadata.update({data["filename"]: data})
            else:
                # print("Received metadata")
                self.files_metadata[data["filename"]] = data

                # print(self.files_metadata)

    def event(self, a0: QtCore.QEvent) -> bool:
        if a0.type() == ReceivedFileDataEvent.type():
            if isinstance(a0, ReceivedFileDataEvent):
                self.handle_message_received(a0.method, a0.data, a0.params)
                # * Handled
                return True
        return super().event(a0)

    