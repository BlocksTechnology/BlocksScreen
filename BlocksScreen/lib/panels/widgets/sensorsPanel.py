import typing

from lib.utils.blocks_frame import BlocksCustomFrame
from lib.utils.icon_button import IconButton
from lib.panels.widgets.sensorWidget import SensorWidget
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets


class SensorsWindow(QtWidgets.QWidget):
    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run_gcode"
    )
    change_fil_sensor_state: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        SensorWidget.FilamentState, name="change_fil_sensor_state"
    )
    request_back: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="request_back"
    )
    def __init__(self, parent):
        super(SensorsWindow, self).__init__(parent)
        self.model = EntryListModel()
        self.entry_delegate = EntryDelegate()
        self.sensor_tracking_widget = {}
        self.current_widget = None
        self.sensor_list: list[SensorWidget] = []
        self.setupUi()
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setTabletTracking(True)
        self.fs_back_button.clicked.connect(self.request_back)

    def reset_view_model(self) -> None:
        """Clears items from ListView
        (Resets `QAbstractListModel` by clearing entries)
        """
        self.model.clear()
        self.entry_delegate.clear()
        
    @QtCore.pyqtSlot(dict, name="handle_available_fil_sensors")
    def handle_available_fil_sensors(self, sensors: dict) -> None:
        """Handle available filament sensors, create `SensorWidget` for each detected
        sensor
        """
        if not isinstance(sensors, dict):
            return
        self.reset_view_model()
        filtered_sensors = list(
        filter(
            lambda printer_obj: str(printer_obj).startswith("filament_switch_sensor")
            or str(printer_obj).startswith("filament_motion_sensor") or str(printer_obj).startswith("cutter_sensor"),
            sensors.keys(),
            )
        )
        if filtered_sensors:
            self.sensor_list = [
                self.create_sensor_widget(name=sensor) for sensor in filtered_sensors
            ]
        else:
            self.no_update_placeholder.show()



    @QtCore.pyqtSlot(str, str, bool, name="handle_fil_state_change")
    def handle_fil_state_change(
        self, sensor_name: str, parameter: str, value: bool
    ) -> None:
        _item = self.sensor_tracking_widget.get(sensor_name)
        if _item:
            if parameter == "filament_detected":
                state = SensorWidget.FilamentState(not value) 
                _item.change_fil_sensor_state(
                        state
                )
            elif parameter == "enabled":
                _item.toggle_button_state(SensorWidget.SensorState(value))
                    
    def showEvent(self, event: QtGui.QShowEvent | None) -> None:
        """Re-add clients to update list"""
        return super().showEvent(event)
    

    @QtCore.pyqtSlot(ListItem, name="on-item-clicked")
    def on_item_clicked(self, item: ListItem) -> None:
        """Setup information for the currently clicked list item on the info box.
        Keeps track of the list item
        """
        if not item:
            return
        
        if self.current_widget:
            self.current_widget.hide()
        
        name_id = item.text
        current_widget = self.sensor_tracking_widget.get(name_id)
        if current_widget is None:
            return
        self.current_widget = current_widget
        self.current_widget.show()


    def create_sensor_widget(self, name: str) -> SensorWidget:
        """Creates a sensor row to be added to the QListWidget

        Args:
            name (str): The name of the filament sensor object
        """
        _item_widget = SensorWidget(self.infobox_frame, name)
        self.info_box_layout.addWidget(_item_widget)


        if self.current_widget:
            _item_widget.hide()
        else:
            _item_widget.show()
            self.current_widget = _item_widget
        name_id = str(name).split(" ")[1]
        item = ListItem(
            text=name_id,
            right_text="",
            right_icon=self.pixmap,
            left_icon=None,
            callback= None,
            selected=False,
            allow_check=False,
            _lfontsize=17,
            _rfontsize=12,
            height=80,
            notificate=False
        )
        _item_widget.run_gcode_signal.connect(self.run_gcode_signal)
        self.sensor_tracking_widget[name_id] = _item_widget
        self.model.add_item(item)
        
        return _item_widget

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None: ...
    
    def setupUi(self) -> None:
        """Setup UI for updatePage"""
        font_id = QtGui.QFontDatabase.addApplicationFont(
            ":/font/media/fonts for text/Momcake-Bold.ttf"
        )
        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(710, 400))
        self.setMaximumSize(QtCore.QSize(720, 420))
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.update_page_content_layout = QtWidgets.QVBoxLayout()
        self.update_page_content_layout.setContentsMargins(15, 15, 2, 2)

        self.header_content_layout = QtWidgets.QHBoxLayout()
        self.header_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.fs_page_title = QtWidgets.QLabel(self)
        self.fs_page_title.setMinimumSize(QtCore.QSize(100, 60))
        self.fs_page_title.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily(font_family)
        font.setPointSize(24)
        palette = self.fs_page_title.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColor("#FFFFFF"))
        self.fs_page_title.setFont(font)
        self.fs_page_title.setPalette(palette)
        self.fs_page_title.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.fs_page_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.fs_page_title.setObjectName("fs_page_title")
        self.fs_page_title.setText("Filament Sensors")
        self.header_content_layout.addWidget(self.fs_page_title, 0)
        self.fs_back_button = IconButton(self)
        self.fs_back_button.setMinimumSize(QtCore.QSize(60, 60))
        self.fs_back_button.setMaximumSize(QtCore.QSize(60, 60))
        self.fs_back_button.setFlat(True)
        self.fs_back_button.setPixmap(QtGui.QPixmap(":/ui/media/btn_icons/back.svg"))
        self.header_content_layout.addWidget(self.fs_back_button, 0)
        self.update_page_content_layout.addLayout(self.header_content_layout, 0)

        self.main_content_layout = QtWidgets.QHBoxLayout()
        self.main_content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.sensor_buttons_frame = BlocksCustomFrame(self)

        self.sensor_buttons_frame.setMinimumSize(QtCore.QSize(320, 300))
        self.sensor_buttons_frame.setMaximumSize(QtCore.QSize(450, 500))

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
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Highlight,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Active,
            QtGui.QPalette.ColorRole.Link,
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
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Highlight,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Inactive,
            QtGui.QPalette.ColorRole.Link,
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
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Highlight,
            brush,
        )
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.ColorGroup.Disabled,
            QtGui.QPalette.ColorRole.Link,
            brush,
        )
        self.fs_sensors_list = QtWidgets.QListView(self.sensor_buttons_frame)
        self.fs_sensors_list.setModel(self.model)
        self.fs_sensors_list.setItemDelegate(self.entry_delegate)
        self.entry_delegate.item_selected.connect(self.on_item_clicked)
        self.fs_sensors_list.setMouseTracking(True)
        self.fs_sensors_list.setTabletTracking(True)
        self.fs_sensors_list.setSpacing(7)
        self.fs_sensors_list.setPalette(palette)
        self.fs_sensors_list.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.fs_sensors_list.setStyleSheet("background-color:transparent")
        self.fs_sensors_list.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.fs_sensors_list.setMinimumSize(self.sensor_buttons_frame.size())
        self.fs_sensors_list.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.fs_sensors_list.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.fs_sensors_list.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.fs_sensors_list.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.fs_sensors_list.setAutoScroll(False)
        self.fs_sensors_list.setProperty("showDropIndicator", False)
        self.fs_sensors_list.setDefaultDropAction(
            QtCore.Qt.DropAction.IgnoreAction
        )
        self.fs_sensors_list.setAlternatingRowColors(False)
        self.fs_sensors_list.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.NoSelection
        )
        self.fs_sensors_list.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.fs_sensors_list.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        self.fs_sensors_list.setHorizontalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        QtWidgets.QScroller.grabGesture(
            self.fs_sensors_list,
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )
        QtWidgets.QScroller.grabGesture(
            self.fs_sensors_list,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )
        self.sensor_buttons_layout = QtWidgets.QVBoxLayout()
        self.sensor_buttons_layout.setContentsMargins(15, 20, 20, 5)
        self.sensor_buttons_layout.addWidget(self.fs_sensors_list, 0)
        self.sensor_buttons_frame.setLayout(self.sensor_buttons_layout)

        self.main_content_layout.addWidget(self.sensor_buttons_frame, 0)
        
        self.infobox_frame = BlocksCustomFrame()
        self.infobox_frame.setMinimumSize(QtCore.QSize(250, 300))
        self.infobox_frame.setMaximumSize(QtCore.QSize(450, 500))

        self.info_box_layout = QtWidgets.QVBoxLayout()
        self.info_box_layout.setContentsMargins(0, 0, 0, 0)

        font = QtGui.QFont()
        font.setFamily(font_family)
        font.setPointSize(20)
        self.version_box = QtWidgets.QHBoxLayout()
        self.no_update_placeholder = QtWidgets.QLabel(self)
        self.no_update_placeholder.setMinimumSize(QtCore.QSize(200, 60))
        self.no_update_placeholder.setMaximumSize(QtCore.QSize(300, 60))
        self.no_update_placeholder.setFont(font)
        self.no_update_placeholder.setPalette(palette)
        self.no_update_placeholder.setSizePolicy(sizePolicy)
        self.no_update_placeholder.setText("No Sensors Available")
        self.no_update_placeholder.setWordWrap(True)
        self.no_update_placeholder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_box_layout.addWidget(
            self.no_update_placeholder, 0, QtCore.Qt.AlignmentFlag.AlignBottom
        )
        self.pixmap = QtGui.QPixmap(":/ui/media/btn_icons/info.svg")
        self.no_update_placeholder.hide()
        self.infobox_frame.setLayout(self.info_box_layout)
        self.main_content_layout.addWidget(self.infobox_frame, 1)
        self.update_page_content_layout.addLayout(self.main_content_layout, 1)
        self.setLayout(self.update_page_content_layout) 