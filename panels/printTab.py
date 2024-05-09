from PyQt6 import QtWidgets
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import (
    QStackedWidget,
    QWidget,
    QListView,
    QListWidget,
    QListWidgetItem,
    QStyleOption,
    QAbstractItemView,
    QHeaderView,
)
from PyQt6.QtCore import (
    pyqtSlot,
    pyqtSignal,
    pyqtBoundSignal,
    Qt,
    QAbstractListModel,
    QAbstractItemModel,
)
from PyQt6 import QtCore, QtGui
import typing
import json
from scripts.events import *
from qt_ui.printStackedWidget_ui import Ui_printStackedWidget
import re
import os
from scripts.bo_includes.bo_files import *


class PrintTab(QStackedWidget):
    request_print_file_signal = pyqtSignal(str, name="start_print")
    request_print_resume_signal = pyqtSignal(name="resume_print")
    request_print_stop_signal = pyqtSignal(name="stop_print")
    request_print_pause_signal = pyqtSignal(name="pause_print")
    request_back_button_pressed = pyqtSignal(name = "request_back_button_pressed")
    request_change_page = pyqtSignal(int, int, name = "request_change_page")

    def __init__(
        self, parent: typing.Optional["QWidget"], file_data: Files, ws: MoonWebSocket
    ) -> None:
        super(PrintTab, self).__init__(parent)
        self.main_panel = parent
        self.file_data: Files = file_data
        self.ws: MoonWebSocket = ws
        self.background: QtGui.QPixmap | None = None
        self._internal_print_status: bool = False
        #  virtual sdcard Path
        # TODO: Get this path from the configfile by asking the websocket first
        # @ GCode directory paths
        self.gcode_path = os.path.expanduser("~/printer_data/gcodes")

        self.panel = Ui_printStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.panel.listWidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        # @ Slot connections
        self.panel.main_print_btn.clicked.connect(self.showFilesPanel)
        self.panel.back_btn.clicked.connect(self.back)
        self.currentChanged.connect(self.view_changed)
        # @ Signals for QListItems
        self.panel.listWidget.itemClicked.connect(self.fileItemClicked)
        self.panel.listWidget.itemPressed.connect(self.itemPressed)
        ## Signals for confirm page
        self.panel.confirm_no_text_label.clicked.connect(self.back)
        self.panel.confirm_yes_text_label.clicked.connect(self.print_start)
        ## Signals for printing operations
        self.request_print_file_signal.connect(self.ws.api.start_print)
        self.request_print_stop_signal.connect(self.ws.api.cancel_print)
        self.request_print_resume_signal.connect(self.ws.api.resume_print)
        self.request_print_pause_signal.connect(self.ws.api.pause_print)
        self.panel.stop_printing_btn.clicked.connect(self.request_print_stop_signal.emit)
        self.panel.pause_printing_btn.clicked.connect(self.pause_resume_print)

        self.show()

    @pyqtSlot(name="pause_resume_print")
    def pause_resume_print(self):
        """pause_resume_print Handles what signal to emit to the printer when a printing job is ongoing
        
        Can either be:
        
        - A pause is supose to happen -> request a pause
        
        - A resume is suppose to happen -> request a resume
        """
        # TODO: Maybe i have to wait for the websocket to respond if it's really printing
        print(self._internal_print_status)
        if self._internal_print_status :
            # * It's printing
            self.request_print_pause_signal.emit()
            self._internal_print_status = False
        else:
            # * It's paused
            self.request_print_resume_signal.emit()
            self._internal_print_status = True

    def showFilesPanel(self) -> None:
        self.setCurrentIndex(1)

    def print_start(self) -> None:
        # * Emit the print file signal and send to the websocket the request
        self.request_print_file_signal.emit(self._current_file_name)
        self._internal_print_status = True
        # * Change the panel view
        self.setCurrentIndex(3)
        # * Display the current printing file
        self.panel.file_printing_text_label.setText(self._current_file_name)

    def back(self) -> None:
        """back Returns to the previous panel of the QStackedWidget 
        """
        _currentIndex = self.currentIndex()
        self.setCurrentIndex(_currentIndex - 1)

    def add_file_entries(self) -> None:
        """add_file_entries -> Inserts the currently available gcode files on the QListWidget 
        """
        # * Delete table contents
        self.panel.listWidget.clear()
        index = 0
        for item in self.file_data.file_list:
            # TODO: Add a file icon before the name
            # * Add a row
            _item = QtWidgets.QListWidgetItem()
            _item_widget = QWidget()
            _item_layout = QtWidgets.QHBoxLayout()
            _item_text = QtWidgets.QLabel()
            # * Add text
            _item_text.setText(str(item["path"]))
            # _file_size = "{:.2f}".format(self.convert_bytes_to_mb(item["size"]))
            # _item_size = QtWidgets.QlistWidgetItem(f" {_file_size} MB")
            # * Add items to the layout
            _item_layout.addWidget(_item_text)
            # * Set item widget layout
            _item_widget.setLayout(_item_layout)
            _item.setSizeHint(_item_widget.sizeHint())
            # * Set item Flags, make it not editable
            _item.setFlags(~Qt.ItemFlag.ItemIsEditable)
            # * Add items
            self.panel.listWidget.addItem(_item)
            self.panel.listWidget.setItemWidget(_item, _item_widget)

            index += 1

    @pyqtSlot(str)
    @pyqtSlot(name="print_state")
    def print_state(self, state:str):
        """print_state -> Slot for received signal about the current printing state of the machine
       
        States:
        - Printing
        
        - Paused
        
        - Canceled        

        Args:
            state (str): _description_
        """
        if "printing" in state:
            # * Indicate that it is printing
            self._internal_print_status = True
            self.panel.pause_printing_btn.setText("Pause")

            
        elif "paused" in state:
            self._internal_print_status = False
            self.panel.pause_printing_btn.setText("Resume")
            
        elif "canceled" in state:
            pass
    
  
    @pyqtSlot(int)
    @pyqtSlot(name="currentChanged")
    def view_changed(self, window_index: int)-> None:
        """view_changed -> Slot for the current displayed panel

        Args:
            window_index (int): Current QStackedWidget index 

        Returns:
            _type_: None
        """
        if window_index == 1:
            # * On files panel
            self.add_file_entries()
            

   
    @pyqtSlot(QListWidgetItem)
    @pyqtSlot(name="file_item_clicked")
    def fileItemClicked(self, item: QListWidgetItem) -> None:
        """fileItemClicked-> Slot for List Item clicked

        Args:
            item (QListWidgetItem): Clicked item
        """
        # * Get the filename from the list item pressed
        _current_item = self.panel.listWidget.itemWidget(item)
        self._current_file_name = _current_item.findChild(QtWidgets.QLabel).text()
        self.panel.confirm_file_name_text_label.setText(self._current_file_name)
        self.setCurrentIndex(2)

    @pyqtSlot(QListWidgetItem)
    @pyqtSlot(name="list_item_pressed")
    def itemPressed(self, item):
        pass


    def paintEvent(self, a0: QPaintEvent) -> None:
        """paintEvent-> Paints UI aspects on the current panel, such as images

        Args:
            a0 (QPaintEvent): _description_

        Returns:
            _type_: _description_
        """
        if self.background is None:
            return

        if self.panel.file_area.isVisible():
            painter = QtGui.QPainter()
            painter.begin(self)
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_SourceOver
            )
            painter.setRenderHint(painter.RenderHint.Antialiasing, True)
            painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

            list_area_rect = self.panel.file_area.geometry()

            # * Scale the pixmap to the correct Dimensions
            # TODO: Background is not really in SVG mode
            _scaled_pixmap = self.background.scaled(
                int(list_area_rect.size().width()),
                int(list_area_rect.size().height()),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            painter.drawPixmap(list_area_rect, _scaled_pixmap, self.background.rect())
            painter.end()

        if self.panel.confirm_page.isVisible():
            # * Paint the thumbnail on the image
            _item_metadata = self.file_data.files_metadata[self._current_file_name]
            _scene = QtWidgets.QGraphicsScene()
            if "thumbnails" in _item_metadata:
                _item_thumbnail = _item_metadata["thumbnails"][1]["relative_path"]
                # TODO: Better paths, need to do this in a better way
                # * Add thumbnail path to python paths
                path = os.path.join(
                    os.path.dirname(
                        os.path.join(self.gcode_path, self._current_file_name)
                    ),
                    _item_thumbnail,
                )
                # * Check if the directory is accessible
                if os.access(path, os.R_OK):
                    # * Add the thumbnail to the GraphicsView
                    _image = QtGui.QImage(path)
                    _scene.setSceneRect(_image.rect().toRectF())
                    _item = QtWidgets.QGraphicsPixmapItem(
                        QtGui.QPixmap.fromImage(_image).scaled(
                            _image.rect().width(),
                            _image.rect().height(),
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation,
                        )
                    )
                    _scene.addItem(_item)
                    self.panel.confirm_print_preview_graphics.setScene(_scene)
                    # print(self.panel.confirm_print_preview_graphics.geometry())
                    self.panel.confirm_print_preview_graphics.setFrameRect(
                        _image.rect()
                    )
            else:
                self.panel.confirm_print_preview_graphics.setScene(_scene)
        else:

            if self.panel.confirm_print_preview_graphics.isVisible():
                self.panel.confirm_print_preview_graphics.close()

        return super().paintEvent(a0)

    def convert_bytes_to_mb(self, bytes: int | float) -> float:
        """convert_bytes_to_mb-> Converts byte size to megabyte size 

        Args:
            bytes (int | float): bytes

        Returns:
            mb: float that represents the number of mb  
        """
        _relation = 2 ** (-20)
        return bytes * _relation

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


# TODO: Add folder icon to the topbar of the files list
# TODO: Add A icon such as ">" to indicate that when you press the file you get the information and go to the next page
