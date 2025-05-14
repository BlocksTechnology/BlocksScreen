import typing

from functools import partial
from lib.ui.customNumpad_ui import Ui_customNumpad
from PyQt6 import QtCore, QtGui, QtWidgets


class CustomNumpad(QtWidgets.QWidget):
    """CustomNumpad
        A custom numpad for inserting integer values.

    Args:
        QFrame (_type_): _description_
    """

    inserted_new_value = QtCore.pyqtSignal(
        [str, int], [str, float], name="numpad_new_value"
    )
    request_change_page = QtCore.pyqtSignal(
        int, int, name="request_change_page"
    )
    request_back_button_pressed = QtCore.pyqtSignal(
        name="request_back_button_pressed"
    )

    def __init__(
        self,
        widget_ui,
    ) -> None:
        super(CustomNumpad, self).__init__()

        self.panel = Ui_customNumpad()
        self.panel.setupUi(self)
        self.hide()
        # TODO: Add the current temperature to display the user the current temperature of the extruder for example or just leave it as nothing in the beginning
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        self.global_panel_index: int = -1
        self.current_number: str = ""
        self.current_object: str | None = None
        self.slot_method = None
        self.numpad_window_index: int = -1
        self.previous_window_index: int = -1
        self.caller_panel: QtWidgets.QStackedWidget | None = None
        self.panel.numpad_0.clicked.connect(partial(self.insert_number, 0))
        self.panel.numpad_1.clicked.connect(partial(self.insert_number, 1))
        self.panel.numpad_2.clicked.connect(partial(self.insert_number, 2))
        self.panel.numpad_3.clicked.connect(partial(self.insert_number, 3))
        self.panel.numpad_4.clicked.connect(partial(self.insert_number, 4))
        self.panel.numpad_5.clicked.connect(partial(self.insert_number, 5))
        self.panel.numpad_6.clicked.connect(partial(self.insert_number, 6))
        self.panel.numpad_7.clicked.connect(partial(self.insert_number, 7))
        self.panel.numpad_8.clicked.connect(partial(self.insert_number, 8))
        self.panel.numpad_9.clicked.connect(partial(self.insert_number, 9))
        self.panel.numpad_enter.clicked.connect(
            partial(self.insert_number, "enter")
        )
        self.panel.numpad_clear.clicked.connect(
            partial(self.insert_number, "clear")
        )

        self.panel.numpad_back_btn.clicked.connect(self.back_button)

    def insert_number(self, value: int | str) -> None:
        if isinstance(value, int):
            #
            self.current_number = self.current_number + str(value)
            self.panel.inserted_value.setText(self.current_number)
        elif isinstance(value, str):
            if (
                "enter" in value
                and self.current_number.isnumeric()
                and self.current_object is not None
            ):
                if self.current_object.startswith("fan"):
                    if 0 <= int(self.current_number) <= 100:
                        # * For the fan i'll the user will only be able to insert a value between 0 and 100
                        ("Sending the new value for the fan")
                        self.inserted_new_value[str, float].emit(
                            self.current_object, float(self.current_number)
                        )
                else:
                    self.inserted_new_value[str, int].emit(
                        self.current_object, int(self.current_number)
                    )
                self.reset_numpad()
                self.hide()
            elif "clear" in value:
                self.current_number = self.current_number[
                    : len(self.current_number) - 1
                ]
                self.panel.inserted_value.setText(self.current_number)

    def back_button(self):
        """back_button
        Controls what the numpad page does when the back button is pressed.
        """
        self.reset_numpad()
        self.request_back_button_pressed.emit()

    @QtCore.pyqtSlot(
        int,
        str,
        str,
        "PyQt_PyObject",
        QtWidgets.QStackedWidget,
        name="call_numpad",
    )
    def call_numpad(
        self,
        global_panel_index: int,
        printer_object: str,
        current_temperature: str,
        callback_slot,
        caller: QtWidgets.QStackedWidget,
    ) -> None:
        self.caller_panel = caller

        if callable(callback_slot):
            self.slot_method = callback_slot
            if "fan" in printer_object:
                self.inserted_new_value[str, float].connect(callback_slot)  # type: ignore
            else:
                self.inserted_new_value[str, int].connect(callback_slot)  # type: ignore

        self.global_panel_index = global_panel_index
        self.previous_window_index = self.caller_panel.currentIndex()
        self.numpad_window_index = self.caller_panel.addWidget(self)

        self.request_change_page.emit(
            global_panel_index, self.numpad_window_index
        )

        # * Reset the displayed temperature
        self.panel.inserted_value.setText(current_temperature)
        self.current_object = printer_object

    def reset_numpad(self) -> bool:
        try:
            self.current_number = ""
            if self.slot_method is not None and callable(self.slot_method):
                if (
                    self.current_object is not None
                    and "fan" in self.current_object
                ):
                    self.inserted_new_value[str, float].disconnect(
                        self.slot_method  # type: ignore
                    )
                else:
                    self.inserted_new_value[str, int].disconnect(
                        self.slot_method  # type:ignore
                    )
                self.slot_method = None
                if self.caller_panel is not None:
                    self.caller_panel.setCurrentIndex(
                        self.previous_window_index
                    )
                    self.caller_panel.removeWidget(self)
                    self.window_index = -1
                    self.caller_panel = None
            self.global_panel_index = -1
            self.numpad_window_index = -1
            self.previous_window_index = -1
            self.panel.inserted_value.setText(self.current_number)
            return True
        except Exception as e:
            raise Exception(
                f"Could not reset numpad, error message caught : {e}"
            )

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        """paintEvent
            Repaints the widget with custom controls

        Args:
            a0 (QtGui.QPaintEvent | None): The event for repainting

        """
        if self.current_object is not None:
            self.panel.value_name.setText(self.current_object)
            self.panel.numpad_title.setText(self.current_object)

        if self.isVisible():
            if (
                self.current_object is not None
                and "fan" in self.current_object
            ):
                pass
