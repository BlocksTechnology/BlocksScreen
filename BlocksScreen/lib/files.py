from __future__ import annotations

import os
import typing

import events
from events import ReceivedFileData
from lib.moonrakerComm import MoonWebSocket
from PyQt6 import QtCore, QtGui, QtWidgets


class Files(QtCore.QObject):
    request_file_list = QtCore.pyqtSignal(name="get_files_list")
    request_file_metadata = QtCore.pyqtSignal([str], name="get_file_metadata")
    request_files_thumbnails = QtCore.pyqtSignal(
        [str], name="request_files_thumbnail"
    )
    request_file_download = QtCore.pyqtSignal([str, str], name="file_download")
    on_file_list: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        list, name="on_file_list"
    )
    fileinfo: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        dict, name="fileinfo"
    )

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

    def handle_message_received(self, method: str, data, params: dict) -> None:
        if "server.files.list" in method:
            self.files.clear()
            self.files = data
            [
                self.request_file_metadata.emit(item["path"])
                for item in self.files
            ]
            self.on_file_list.emit(self.files)
        elif "server.files.metadata" in method:
            if data["filename"] in self.files_metadata.keys():
                self.files_metadata.update({data["filename"]: data})
            else:
                self.files_metadata[data["filename"]] = data

    @QtCore.pyqtSlot(str, name="on_request_fileinfo")
    def on_request_fileinfo(self, filename: str) -> None:
        if not self.files_metadata or not filename:
            return
        _data: dict = {
            "thumbnail_images": list,
            "filament_total": dict,
            "estimated_time": dict,
            "layer_count": int,
            "object_height": float,
            "size": int,
            "filament_type": str,
            "filament_weight_total": float,
            "layer_height": float,
            "first_layer_height": float,
            "first_layer_extruder_temp": float,
            "first_layer_bed_temp": float,
            "chamber_temp": float,
            "filament_name": str,
            "nozzle_diameter": float,
            "slicer": str,
        }
        _file_metadata = self.files_metadata.get(str(filename))
        if not _file_metadata:
            return
        _thumbnails = _file_metadata.get("thumbnails", {})
        _thumbnail_paths = list(
            map(
                lambda thumbnail_path: os.path.join(
                    os.path.dirname(os.path.join(self.gcode_path, filename)),
                    thumbnail_path.get("relative_path", "?"),
                ),
                _thumbnails,
            )
        )
        _thumbnail_images = list(
            map(lambda path: QtGui.QImage(path), _thumbnail_paths)
        )
        _data.update({"thumbnail_images": _thumbnail_images})

        _data.update(
            {"filament_total": _file_metadata.get("filament_total", "?")}
        )
        _data.update(
            {"estimated_time": _file_metadata.get("estimated_time", "?")}
        )
        _data.update({"layer_count": _file_metadata.get("layer_count", -1.0)})
        _data.update({"total_layer": _file_metadata.get("total_layer", -1.0)})
        _data.update(
            {"object_height": _file_metadata.get("object_height", -1.0)}
        )
        _data.update(
            {"nozzle_diameter": _file_metadata.get("nozzle_diameter", -1.0)}
        )
        _data.update(
            {"layer_height": _file_metadata.get("layer_height", -1.0)}
        )
        _data.update(
            {
                "first_layer_height": _file_metadata.get(
                    "first_layer_height", -1.0
                )
            }
        )
        _data.update(
            {
                "first_layer_extruder_temp": _file_metadata.get(
                    "first_layer_extruder_temp", -1.0
                )
            }
        )
        _data.update(
            {
                "first_layer_bed_temp": _file_metadata.get(
                    "first_layer_bed_temp", -1.0
                )
            }
        )
        _data.update(
            {"chamber_temp": _file_metadata.get("chamber_temp", -1.0)}
        )
        _data.update(
            {"filament_name": _file_metadata.get("filament_name", -1.0)}
        )
        _data.update(
            {"filament_type": _file_metadata.get("filament_type", -1.0)}
        )
        _data.update(
            {
                "filament_weight_total": _file_metadata.get(
                    "filament_weight_total", -1.0
                )
            }
        )
        _data.update({"slicer": _file_metadata.get("slicer", -1.0)})
        self.fileinfo.emit(_data)

    def eventFilter(self, a0: QtCore.QObject, a1: QtCore.QEvent) -> bool:
        if a1.type() == events.KlippyDisconnected.type():
            self.files_metadata.clear()
            self.files.clear()
            return False
        elif a1.type() == events.KlippyReady.type():
            self.request_file_list.emit()
            return False
        return super().eventFilter(a0, a1)

    def event(self, a0: QtCore.QEvent) -> bool:
        if a0.type() == ReceivedFileData.type():
            if isinstance(a0, ReceivedFileData):
                self.handle_message_received(a0.method, a0.data, a0.params)
                return True
        return super().event(a0)
