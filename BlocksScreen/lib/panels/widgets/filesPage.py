import logging
import typing

import helper_methods
from lib.utils.blocks_Scrollbar import CustomScrollBar
from lib.utils.icon_button import IconButton
from lib.utils.list_button import ListCustomButton
from PyQt6 import QtCore, QtGui, QtWidgets

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
    request_file_list_refresh: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(name="request-file-list-refresh")
    )
    _current_file_name: str = ""
    file_list: list = []

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUI()
        self.setMouseTracking(True)
        self.buttons: bool = False
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.ReloadButton.clicked.connect(
            lambda: self.request_file_list_refresh.emit()
        )
        self.listWidget.verticalScrollBar().valueChanged.connect(
            self.handle_scrollbar
        )
        self.scrollbar.valueChanged.connect(self.handle_scrollbar)
        self.scrollbar.valueChanged.connect(
            lambda value: self.listWidget.verticalScrollBar().setValue(value)
        )
        self.listWidget.itemClicked.connect(self.fileItemClicked)
        self.show()

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.add_file_entries()
        return super().showEvent(a0)

    @QtCore.pyqtSlot(dict, name="on-fileinfo")
    def on_fileinfo(self, filedata: dict) -> None:
        if self.buttons:
            estimated_time = filedata.get("estimated_time", 0)
            seconds = (
                int(estimated_time)
                if isinstance(estimated_time, (int, float))
                else 0
            )

            filament_type = (
                filedata.get("filament_type", "Unknown filament")
                if filedata.get("filament_type", "Unknown filament") != -1.0
                else "Unknown filament"
            )
            time_str = ""
            days, hours, minutes, _ = helper_methods.estimate_print_time(
                seconds
            )
            if seconds <= 0:
                time_str = "No time estimated"
            elif seconds < 60:
                time_str = "less than 1 minute"
            else:
                if days > 0:
                    time_str = f"{days}d {hours}h {minutes}m"
                elif hours > 0:
                    time_str = f"{hours}h {minutes}m"
                else:
                    time_str = f"{minutes}m"

            self.button.setRightText(f"{filament_type} - {time_str}")
            return
        if self.isVisible():
            self.file_selected.emit(str(self._current_file_name), filedata)

    @QtCore.pyqtSlot(list, name="on-file-list")
    def on_file_list(self, file_list: list) -> None:
        self.file_list.clear()
        self.file_list = file_list
        if self.isVisible(): 
            self.add_file_entries()

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem, name="file-item-clicked")
    def fileItemClicked(self, item: str) -> None:
        """Slot for List Item clicked

        Args:
            item (QListWidgetItem): Clicked item
        """
        if item:
            self._current_file_name = item
            if self._current_file_name:
                self.request_file_info.emit(self._current_file_name)

    def add_file_entries(self) -> None:
        """Inserts the currently available gcode files on the QListWidget"""
        self.listWidget.blockSignals(True)
        self.listWidget.clear()
        index = 0
        self.buttons = True
        if not self.file_list:
            self.listWidget.setSpacing(-1)
            self.scrollbar.hide()
            placeholder_item = QtWidgets.QListWidgetItem()
            placeholder_item.setSizeHint(
                QtCore.QSize(self.listWidget.width(), self.listWidget.height())
            )
            self.listWidget.addItem(placeholder_item)
            self.listWidget.setItemWidget(
                placeholder_item, self.placeholder_label
            )
            self.listWidget.blockSignals(False)
            return

        self.listWidget.setSpacing(35)
        sorted_list = sorted(
            self.file_list, key=lambda x: x["modified"], reverse=True
        )
        for item in sorted_list:
            self.button = ListCustomButton(self)
            self.button.setText(str(item["path"][:-6]))
            self.request_file_info.emit(item["path"])
            self.button.setPixmap(
                QtGui.QPixmap(":/arrow_icons/media/btn_icons/right_arrow.svg")
            )
            self.button.setFixedSize(600, 80)
            self.button.setLeftFontSize(17)
            self.button.setRightFontSize(12)
            list_item = QtWidgets.QListWidgetItem()
            list_item.setSizeHint(self.button.sizeHint())
            self.listWidget.addItem(list_item)
            self.listWidget.setItemWidget(list_item, self.button)
            filename = str(item["path"])
            self.button.clicked.connect(lambda: self.fileItemClicked(filename))
            index += 1
        self.buttons = False
        spacer_item = QtWidgets.QListWidgetItem()
        spacer_widget = QtWidgets.QWidget()
        spacer_widget.setFixedHeight(10)
        spacer_item.setSizeHint(spacer_widget.sizeHint())
        self.listWidget.addItem(spacer_item)
        self.scrollbar.setMinimum(
            self.listWidget.verticalScrollBar().minimum()
        )
        self.scrollbar.setMaximum(
            self.listWidget.verticalScrollBar().maximum()
        )
        self.scrollbar.setPageStep(
            self.listWidget.verticalScrollBar().pageStep()
        )
        self.scrollbar.show()
        self.listWidget.blockSignals(False)

    def handle_scrollbar(self, value):
        # Block signals to avoid recursion
        self.scrollbar.blockSignals(True)
        self.scrollbar.setValue(value)
        self.scrollbar.blockSignals(False)

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
        self.fp_content_layout = QtWidgets.QHBoxLayout()
        self.fp_content_layout.setContentsMargins(0, 0, 0, 0)
        self.fp_content_layout.setObjectName("fp_content_layout")
        self.listWidget = QtWidgets.QListWidget(parent=self)
        self.listWidget.setProperty("showDropIndicator", False)
        self.listWidget.setProperty("selectionMode", "NoSelection")
        self.listWidget.setStyleSheet("background: transparent;")
        self.listWidget.setDefaultDropAction(QtCore.Qt.DropAction.IgnoreAction)
        self.listWidget.setUniformItemSizes(True)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.listWidget.setDefaultDropAction(QtCore.Qt.DropAction.IgnoreAction)
        self.listWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.listWidget.setHorizontalScrollBarPolicy(  # No horizontal scroll
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
            0.05,  # Lower = more responsive
        )
        scroller_props.setScrollMetric(
            QtWidgets.QScrollerProperties.ScrollMetric.DecelerationFactor,
            0.4,  # higher = less inertia
        )
        QtWidgets.QScroller.scroller(self.listWidget).setScrollerProperties(
            scroller_props
        )
        font = QtGui.QFont()
        font.setPointSize(25)
        placeholder_item = QtWidgets.QListWidgetItem()
        placeholder_item.setSizeHint(
            QtCore.QSize(self.listWidget.width(), self.listWidget.height())
        )
        self.placeholder_label = QtWidgets.QLabel("No Files found")
        self.placeholder_label.setFont(font)
        self.placeholder_label.setStyleSheet("color: gray;")
        self.placeholder_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.placeholder_label.setMinimumSize(
            QtCore.QSize(self.listWidget.width(), self.listWidget.height())
        )
        self.fp_content_layout.addWidget(self.listWidget)
        self.scrollbar = CustomScrollBar()
        self.fp_content_layout.addWidget(self.scrollbar)
        self.verticalLayout_5.addLayout(self.fp_content_layout)
        self.scrollbar.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
        )
        self.scroller = QtWidgets.QScroller.scroller(self.listWidget)
