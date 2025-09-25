import typing

from lib.panels.widgets.sensorWidget import SensorWidget
from lib.utils.icon_button import IconButton
from PyQt6 import QtCore, QtGui, QtWidgets


class SensorsWindow(QtWidgets.QWidget):
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )
    change_fil_sensor_state: typing.ClassVar[QtCore.pyqtSignal] = (
        QtCore.pyqtSignal(
            SensorWidget.FilamentState, name="change_fil_sensor_state"
        )
    )
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    sensor_list: list[SensorWidget] = []

    def __init__(self, parent):
        super(SensorsWindow, self).__init__(parent)
        self.setupUi()
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setTabletTracking(True)
        self.fs_sensors_list.itemClicked.connect(self.handle_sensor_clicked)
        self.fs_sensors_list.itemClicked
        self.fs_back_button.clicked.connect(self.request_back)

    @QtCore.pyqtSlot(dict, name="handle_available_fil_sensors")
    def handle_available_fil_sensors(self, sensors: dict) -> None:
        if not isinstance(sensors, dict):
            return

        filtered_sensors = list(
        filter(
            lambda printer_obj: str(printer_obj).startswith("filament_switch_sensor")
            or str(printer_obj).startswith("filament_motion_sensor"),
            sensors.keys(),
            )
        )

        if filtered_sensors:
            self.fs_sensors_list.setRowHidden(self.fs_sensors_list.row(self.item), True)
            self.sensor_list = [
                self.create_sensor_widget(name=sensor) for sensor in filtered_sensors
            ]
        else:
            self.fs_sensors_list.setRowHidden(self.fs_sensors_list.row(self.item), False)



    @QtCore.pyqtSlot(str, str, bool, name="handle_fil_state_change")
    def handle_fil_state_change(
        self, sensor_name: str, parameter: str, value: bool
    ) -> None:
        if sensor_name in self.sensor_list:
            state = SensorWidget.FilamentState(value)
            _split = sensor_name.split(" ")
            _item = self.fs_sensors_list.findChild(
                SensorWidget,
                name=_split[1],
                options=QtCore.Qt.FindChildOption.FindChildrenRecursively,
            )
            if parameter == "filament_detected":
                if isinstance(_item, SensorWidget) and hasattr(
                    _item, "change_fil_sensor_state"
                ):
                    _item.change_fil_sensor_state(
                        SensorWidget.FilamentState.PRESENT
                    )
                    _item.repaint()
            elif parameter == "filament_missing":
                if isinstance(_item, SensorWidget) and hasattr(
                    _item, "change_fil_sensor_state"
                ):
                    _item.change_fil_sensor_state(
                        SensorWidget.FilamentState.MISSING
                    )
                    _item.repaint()
            elif parameter == "enabled":
                if _item and isinstance(_item, SensorWidget):
                    self.run_gcode_signal.emit(
                        _item.toggle_sensor_gcode_command
                    )

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem, name="handle_sensor_clicked")
    def handle_sensor_clicked(self, sensor: QtWidgets.QListWidgetItem) -> None:
        _item = self.fs_sensors_list.itemWidget(sensor)
        # FIXME: This is just not working
        _item.toggle_button.state = ~_item.toggle_button.state
        if _item and isinstance(_item, SensorWidget):
            self.run_gcode_signal.emit(_item.toggle_sensor_gcode_command)

    def create_sensor_widget(self, name: str) -> SensorWidget:
        """Creates a sensor row to be added to the QListWidget

        Args:
            name (str): The name of the filament sensor object
        """
        _item_widget = SensorWidget(self.fs_sensors_list, name)
        _list_item = QtWidgets.QListWidgetItem()
        _list_item.setFlags(~QtCore.Qt.ItemFlag.ItemIsEditable)
        _list_item.setSizeHint(
            QtCore.QSize(self.fs_sensors_list.contentsRect().width(), 80)
        )
        _item_widget.toggle_button.stateChange.connect(
            lambda: self.fs_sensors_list.itemClicked.emit(_item_widget)
        )

        self.fs_sensors_list.setItemWidget(_list_item, _item_widget)

        return _item_widget

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None: ...

    def setupUi(self):
        self.setObjectName("filament_sensors_page")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 410))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.content_vertical_layout = QtWidgets.QVBoxLayout()
        self.content_vertical_layout.setObjectName("contentVerticalLayout")
        self.fs_header_layout = QtWidgets.QHBoxLayout()
        self.fs_header_layout.setContentsMargins(0, 0, 0, 0)
        self.fs_header_layout.setObjectName("fs_header_layout")
        self.fs_header_layout.setGeometry(QtCore.QRect(10, 10, 691, 71))
        self.fs_page_title = QtWidgets.QLabel(parent=self)
        sizePolicy.setHeightForWidth(
            self.fs_page_title.sizePolicy().hasHeightForWidth()
        )
        self.fs_page_title.setSizePolicy(sizePolicy)
        self.fs_page_title.setMinimumSize(QtCore.QSize(300, 71))
        self.fs_page_title.setMaximumSize(QtCore.QSize(16777215, 71))
        font = QtGui.QFont()
        font.setPointSize(22)
        palette = QtGui.QPalette()
        palette.setColor(
            palette.ColorRole.WindowText, QtGui.QColorConstants.White
        )
        self.fs_page_title.setPalette(palette)
        self.fs_page_title.setFont(font)
        self.fs_page_title.setObjectName("fs_page_title")
        self.fs_header_layout.addWidget(self.fs_page_title, 0)
        self.fs_back_button = IconButton(self)
        sizePolicy.setHeightForWidth(
            self.fs_back_button.sizePolicy().hasHeightForWidth()
        )
        self.fs_back_button.setSizePolicy(sizePolicy)
        self.fs_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.fs_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.fs_back_button.setFlat(True)
        self.fs_back_button.setPixmap(
            QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.fs_back_button.setObjectName("fs_back_button")
        self.fs_header_layout.addWidget(
            self.fs_back_button,
            0,
        )
        self.content_vertical_layout.addLayout(self.fs_header_layout)
        self.fs_sensors_list = QtWidgets.QListWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.fs_sensors_list.sizePolicy().hasHeightForWidth()
        )
        self.fs_sensors_list.setSizePolicy(sizePolicy)
        self.fs_sensors_list.setMinimumSize(QtCore.QSize(650, 300))
        self.fs_sensors_list.setMaximumSize(QtCore.QSize(700, 300))
        self.fs_sensors_list.setLayoutDirection(
            QtCore.Qt.LayoutDirection.LeftToRight
        )
        self.fs_sensors_list.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.fs_sensors_list.setObjectName("fs_sensors_list")
        self.fs_sensors_list.setViewMode(
            self.fs_sensors_list.ViewMode.ListMode
        )
        self.fs_sensors_list.setItemAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self.fs_sensors_list.setFlow(self.fs_sensors_list.Flow.TopToBottom)
        self.fs_sensors_list.setFrameStyle(0)
        palette = self.fs_sensors_list.palette()
        palette.setColor(
            palette.ColorRole.Base, QtGui.QColorConstants.Transparent
        )
        self.fs_sensors_list.setPalette(palette)
        self.fs_sensors_list.setDropIndicatorShown(False)
        self.fs_sensors_list.setAcceptDrops(False)
        self.fs_sensors_list.setProperty("showDropIndicator", False)
        self.content_vertical_layout.setStretch(0, 0)
        self.content_vertical_layout.setStretch(1, 1)
        self.content_vertical_layout.addWidget(
            self.fs_sensors_list,
            1,
            QtCore.Qt.AlignmentFlag.AlignHCenter
            | QtCore.Qt.AlignmentFlag.AlignVCenter,
        )

        font = QtGui.QFont()
        font.setPointSize(25)


        self.item = QtWidgets.QListWidgetItem()
        self.item.setSizeHint(QtCore.QSize(self.fs_sensors_list.width(),self.fs_sensors_list.height())) 


        self.label = QtWidgets.QLabel("No sensors found")
        self.label.setFont(font)
        self.label.setStyleSheet("color: gray;")  
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.hide()

        self.fs_sensors_list.addItem(self.item)
        self.fs_sensors_list.setItemWidget(self.item,self.label)



        self.content_vertical_layout.addSpacing(5)
        self.setLayout(self.content_vertical_layout)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("filament_sensors_page", "Form"))
        self.fs_page_title.setText(
            _translate("filament_sensors_page", "Filament Sensors")
        )
        self.fs_back_button.setProperty(
            "button_type", _translate("filament_sensors_page", "icon")
        )
