from PyQt6 import QtCore, QtGui, QtWidgets
import typing

from lib.utils.icon_button import IconButton


class FilesPage(QtWidgets.QWidget):
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    file_selected: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, dict, name="file_selected"
    )
    request_file_info: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="request_file_info"
    )
    request_file_list_refresh: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="request_file_list_refresh")
    )
    _current_file_name = ""

    def __init__(self, parent, files) -> None:
        super().__init__(parent)
        self.setupUI()
        self.file_data = files
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.listWidget.itemClicked.connect(self.fileItemClicked)
        self.ReloadButton.clicked.connect(lambda: self.on_reload_list)
        self.request_file_info.connect(self.file_data.on_request_fileinfo)
        self.file_data.fileinfo.connect(self.on_fileinfo)

    @QtCore.pyqtSlot(dict, name="on_fileinfo")
    def on_fileinfo(self, filedata: dict) -> None:
        if (
            self._current_file_name
        ):  # If i don't have this, it'll break the gui
            self.file_selected.emit(str(self._current_file_name), filedata)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.add_file_entries()
        return super().showEvent(a0)

    @QtCore.pyqtSlot(name="on_reload_list")
    def on_reload_list(self) -> None:
        """Reload files list"""
        self.file_data.request_file_list.emit()
        self.add_file_entries()

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem, name="file_item_clicked")
    def fileItemClicked(self, item: QtWidgets.QListWidgetItem) -> None:
        """Slot for List Item clicked

        Args:
            item (QListWidgetItem): Clicked item
        """
        # * Get the filename from the list item pressed
        _current_item: QtWidgets.QWidget = self.listWidget.itemWidget(item)
        if _current_item is not None:
            self._current_file_name = _current_item.findChild(
                QtWidgets.QLabel
            ).text()  # type: ignore
            if self._current_file_name:
                self.request_file_info.emit(self._current_file_name)

    def add_file_entries(self) -> None:
        """Inserts the currently available gcode files on the QListWidget"""
        self.listWidget.clear()
        index = 0

        def _add_entry():
            _item = QtWidgets.QListWidgetItem()
            _item_widget = QtWidgets.QWidget()
            _item_layout = QtWidgets.QHBoxLayout()
            _item_text = QtWidgets.QLabel()
            _item_text.setText(str(item["path"]))
            _item_text.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignLeft
                & QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            _item_layout.addWidget(_item_text)
            _item_widget.setLayout(_item_layout)
            _item.setSizeHint(_item_widget.sizeHint())
            _item.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
            return _item, _item_widget

        for item in self.file_data.file_list:
            # TODO: Add a file icon before the name
            _item, _item_widget = _add_entry()
            self.listWidget.addItem(_item)
            self.listWidget.setItemWidget(_item, _item_widget)
            index += 1

    def setupUI(self):
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(720, 420))
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.setFont(font)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.setAutoFillBackground(False)
        self.setStyleSheet(
            "#file_page{\n    background-color: transparent;\n}"
        )
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
        self.fp_content_layout = QtWidgets.QVBoxLayout()
        self.fp_content_layout.setContentsMargins(5, 5, 5, 5)
        self.fp_content_layout.setObjectName("fp_content_layout")
        self.listWidget = QtWidgets.QListWidget(parent=self)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Button,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Base,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Window,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Button,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Base,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Window,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Button,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Base,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Window,
            brush,
        )
        self.listWidget.setPalette(palette)
        self.listWidget.setStyleSheet(
            "QListWidget{background-color: transparent;}\n"
            "\n"
            "QLabel{\n"
            "color: #ffffff;\n"
            "}"
        )
        self.listWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.listWidget.setProperty("showDropIndicator", False)
        self.listWidget.setDefaultDropAction(QtCore.Qt.DropAction.IgnoreAction)
        self.listWidget.setUniformItemSizes(True)
        self.listWidget.setObjectName("listWidget")
        self.fp_content_layout.addWidget(self.listWidget)
        self.verticalLayout_5.addLayout(self.fp_content_layout)
