import logging
import os
import typing

import helper_methods
from lib.utils.blocks_Scrollbar import CustomScrollBar
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets

from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem

logger = logging.getLogger("logs/BlocksScreen.log")


class FilesPage(QtWidgets.QWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request-back"
    )
    file_selected: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, dict, name="file-selected"
    )
    request_file_info: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="request-file-info"
    )
    request_dir_info: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [], [str], [str, bool], name="api-get-dir-info"
    )
    request_file_list: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        [], [str], name="api-get-files-list"
    )
    request_file_metadata: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="api-get-gcode-metadata"
    )
    file_list: list = []
    files_data: dict = {}
    directories: list = []

    def __init__(self, parent) -> None:
        super().__init__()
        self.model = EntryListModel()
        self.entry_delegate = EntryDelegate()
        self._setupUI()
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.curr_dir: str = ""
        self.ReloadButton.clicked.connect(
            lambda: self.request_dir_info[str].emit(self.curr_dir)
        )
        self.listWidget.verticalScrollBar().valueChanged.connect(self._handle_scrollbar)
        self.scrollbar.valueChanged.connect(self._handle_scrollbar)
        self.scrollbar.valueChanged.connect(
            lambda value: self.listWidget.verticalScrollBar().setValue(value)
        )
        self.back_btn.clicked.connect(self.reset_dir)

        self.entry_delegate.item_selected.connect(self._on_item_selected)
        self._refresh_one_and_half_sec_timer = QtCore.QTimer()
        self._refresh_one_and_half_sec_timer.timeout.connect(
            lambda: self.request_dir_info[str].emit(self.curr_dir)
        )
        self._refresh_one_and_half_sec_timer.start(1500)

    @QtCore.pyqtSlot(ListItem, name="on-item-selected")
    def _on_item_selected(self, item: ListItem) -> None:
        """Slot called when a list item is selected in the UI.
        This method is connected to the `item_selected` signal of the entry delegate.
        It handles the selection of a `ListItem` and process it accoding it with its type
        Args:
            item : ListItem The item that was selected by the user.
        """
        if not item.left_icon:
            filename = self.curr_dir + "/" + item.text + ".gcode"
            self._fileItemClicked(filename)
        else:
            if item.text == "Go Back":
                go_back_path = os.path.dirname(self.curr_dir)
                if go_back_path == "/":
                    go_back_path = ""
                self._on_goback_dir(go_back_path)
            else:
                self._dirItemClicked("/" + item.text)

    @QtCore.pyqtSlot(name="reset-dir")
    def reset_dir(self) -> None:
        """Reset current directory"""
        self.curr_dir = ""
        self.request_dir_info[str].emit(self.curr_dir)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        """Re-implemented method, handle widget show event"""
        self._build_file_list()
        return super().showEvent(a0)

    @QtCore.pyqtSlot(list, name="on-file-list")
    def on_file_list(self, file_list: list) -> None:
        """Handle receiving files list from websocket"""
        self.files_data.clear()
        self.file_list = file_list

    @QtCore.pyqtSlot(list, name="on-dirs")
    def on_directories(self, directories_data: list) -> None:
        """Handle receiving available directories from websocket"""
        self.directories = directories_data
        if self.isVisible():
            self._build_file_list()

    @QtCore.pyqtSlot(dict, name="on-fileinfo")
    def on_fileinfo(self, filedata: dict) -> None:
        """Method called per file to contruct file entry to the list"""
        if not filedata or not self.isVisible():
            return
        filename = filedata.get("filename", "")
        if not filename:
            return
        self.files_data.update({f"{filename}": filedata})
        estimated_time = filedata.get("estimated_time", 0)
        seconds = int(estimated_time) if isinstance(estimated_time, (int, float)) else 0
        filament_type = (
            filedata.get("filament_type", "Unknown filament")
            if filedata.get("filament_type", "Unknown filament") != -1.0
            else "Unknown filament"
        )
        time_str = ""
        days, hours, minutes, _ = helper_methods.estimate_print_time(seconds)
        if seconds <= 0:
            time_str = "??"
        elif seconds < 60:
            time_str = "less than 1 minute"
        else:
            if days > 0:
                time_str = f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                time_str = f"{hours}h {minutes}m"
            else:
                time_str = f"{minutes}m"

        name = helper_methods.get_file_name(filename)
        item = ListItem(
            text=name[:-6],
            right_text=f"{filament_type} - {time_str}",
            right_icon=self.path.get("right_arrow"),
            left_icon=None,
            callback=None,
            selected=False,
            allow_check=False,
            _lfontsize=17,
            _rfontsize=12,
            height=80,
            notificate=False,
        )

        self.model.add_item(item)

    @QtCore.pyqtSlot(str, name="file-item-clicked")
    def _fileItemClicked(self, filename: str) -> None:
        """Slot for List Item clicked

        Args:
            filename (str): Clicked item path
        """
        self.file_selected.emit(
            str(filename.removeprefix("/")),
            self.files_data.get(filename.removeprefix("/")),
        )

    def _dirItemClicked(self, directory: str) -> None:
        """Method that changes the current view in the list"""
        self.curr_dir = self.curr_dir + directory
        self.request_dir_info[str].emit(self.curr_dir)

    def _build_file_list(self) -> None:
        """Inserts the currently available gcode files on the QListWidget"""
        self.listWidget.blockSignals(True)
        self.model.clear()
        self.entry_delegate.clear()
        if (
            not self.file_list
            and not self.directories
            and os.path.islink(self.curr_dir)
        ):
            self._add_placeholder()
            return

        if self.directories or self.curr_dir != "":
            if self.curr_dir != "" and self.curr_dir != "/":
                self._add_back_folder_entry()
            for dir_data in self.directories:
                if dir_data.get("dirname").startswith("."):
                    continue
                self._add_directory_list_item(dir_data)
        sorted_list = sorted(self.file_list, key=lambda x: x["modified"], reverse=True)
        for item in sorted_list:
            self._add_file_list_item(item)

        self._setup_scrollbar()
        self.listWidget.blockSignals(False)
        self.listWidget.update()

    def _add_directory_list_item(self, dir_data: dict) -> None:
        """Method that adds directories to the list"""
        dir_name = dir_data.get("dirname", "")
        if not dir_name:
            return
        item = ListItem(
            text=str(dir_name),
            left_icon=self.path.get("folderIcon"),
            right_text="",
            selected=False,
            callback=None,
            allow_check=False,
            _lfontsize=17,
            _rfontsize=12,
            height=80,
        )
        self.model.add_item(item)

    def _add_back_folder_entry(self) -> None:
        """Method to insert in the list the "Go back" item"""
        go_back_path = os.path.dirname(self.curr_dir)
        if go_back_path == "/":
            go_back_path = ""

        item = ListItem(
            text="Go Back",
            right_text="",
            right_icon=None,
            left_icon=self.path.get("back_folder"),
            callback=None,
            selected=False,
            allow_check=False,
            _lfontsize=17,
            _rfontsize=12,
            height=80,
            notificate=False,
        )
        self.model.add_item(item)

    @QtCore.pyqtSlot(str, str, name="on-goback-dir")
    def _on_goback_dir(self, directory) -> None:
        """Go back behaviour"""
        self.request_dir_info[str].emit(directory)
        self.curr_dir = directory

    def _add_file_list_item(self, file_data_item) -> None:
        """Request file information and metadata to create filelist"""
        if not file_data_item:
            return

        name = (
            file_data_item["path"]
            if "path" in file_data_item.keys()
            else file_data_item["filename"]
        )
        if not name.endswith(".gcode"):
            return
        file_path = (
            name if not self.curr_dir else str(self.curr_dir + "/" + name)
        ).removeprefix("/")

        self.request_file_metadata.emit(file_path.removeprefix("/"))
        self.request_file_info.emit(file_path.removeprefix("/"))

    def _add_placeholder(self) -> None:
        """Shows placeholder when no items exist"""
        self.scrollbar.hide()
        self.listWidget.hide()
        self.label.show()

    def _handle_scrollbar(self, value):
        """Updates scrollbar value"""
        self.scrollbar.blockSignals(True)
        self.scrollbar.setValue(value)
        self.scrollbar.blockSignals(False)

    def _setup_scrollbar(self) -> None:
        """Syncs the scrollbar with the list size"""
        self.scrollbar.setMinimum(self.listWidget.verticalScrollBar().minimum())
        self.scrollbar.setMaximum(self.listWidget.verticalScrollBar().maximum())
        self.scrollbar.setPageStep(self.listWidget.verticalScrollBar().pageStep())
        self.scrollbar.show()

    def _setupUI(self):
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 400))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.setFont(font)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.setAutoFillBackground(False)
        self.setStyleSheet("#file_page{\n    background-color: transparent;\n}")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.fp_header_layout = QtWidgets.QHBoxLayout()
        self.fp_header_layout.setObjectName("fp_header_layout")
        self.back_btn = IconButton(parent=self)
        self.back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.back_btn.setFlat(True)
        self.back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.back_btn.setObjectName("back_btn")
        self.fp_header_layout.addWidget(
            self.back_btn, 0, QtCore.Qt.AlignmentFlag.AlignLeft
        )
        self.ReloadButton = IconButton(parent=self)
        self.ReloadButton.setMinimumSize(QtCore.QSize(60, 60))
        self.ReloadButton.setMaximumSize(QtCore.QSize(60, 60))
        self.ReloadButton.setFlat(True)
        self.ReloadButton.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/refresh.svg")
        )
        self.ReloadButton.setObjectName("ReloadButton")
        self.fp_header_layout.addWidget(
            self.ReloadButton, 0, QtCore.Qt.AlignmentFlag.AlignRight
        )
        self.verticalLayout_5.addLayout(self.fp_header_layout)
        self.line = QtWidgets.QFrame(parent=self)
        self.line.setMinimumSize(QtCore.QSize(0, 0))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_5.addWidget(self.line)
        self.fp_content_layout = QtWidgets.QHBoxLayout()
        self.fp_content_layout.setContentsMargins(0, 0, 0, 0)
        self.fp_content_layout.setObjectName("fp_content_layout")
        self.listWidget = QtWidgets.QListView(parent=self)
        self.listWidget.setModel(self.model)
        self.listWidget.setItemDelegate(self.entry_delegate)
        self.listWidget.setSpacing(5)
        self.listWidget.setProperty("showDropIndicator", False)
        self.listWidget.setProperty("selectionMode", "NoSelection")
        self.listWidget.setStyleSheet("background: transparent;")
        self.listWidget.setDefaultDropAction(QtCore.Qt.DropAction.IgnoreAction)
        self.listWidget.setUniformItemSizes(True)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.listWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.listWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.listWidget.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.listWidget.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        QtWidgets.QScroller.grabGesture(
            self.listWidget,
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )
        QtWidgets.QScroller.grabGesture(
            self.listWidget,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )
        self.listWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )

        scroller_instance = QtWidgets.QScroller.scroller(self.listWidget)
        scroller_props = scroller_instance.scrollerProperties()
        scroller_props.setScrollMetric(
            QtWidgets.QScrollerProperties.ScrollMetric.DragVelocitySmoothingFactor,
            0.05,
        )
        scroller_props.setScrollMetric(
            QtWidgets.QScrollerProperties.ScrollMetric.DecelerationFactor,
            0.4,
        )
        QtWidgets.QScroller.scroller(self.listWidget).setScrollerProperties(
            scroller_props
        )

        font = QtGui.QFont()
        font.setPointSize(25)
        self.label = QtWidgets.QLabel("No Files found")
        self.label.setFont(font)
        self.label.setStyleSheet("color: gray;")
        self.label.setMinimumSize(
            QtCore.QSize(self.listWidget.width(), self.listWidget.height())
        )

        self.scrollbar = CustomScrollBar()

        self.fp_content_layout.addWidget(
            self.label,
            alignment=QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )
        self.fp_content_layout.addWidget(self.listWidget)
        self.fp_content_layout.addWidget(self.scrollbar)
        self.verticalLayout_5.addLayout(self.fp_content_layout)
        self.scrollbar.show()
        self.label.hide()

        self.path = {
            "back_folder": QtGui.QPixmap(":/ui/media/btn_icons/back_folder.svg"),
            "folderIcon": QtGui.QPixmap(":/ui/media/btn_icons/folderIcon.svg"),
            "right_arrow": QtGui.QPixmap(
                ":/arrow_icons/media/btn_icons/right_arrow.svg"
            ),
        }
