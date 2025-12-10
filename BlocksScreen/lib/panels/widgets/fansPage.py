from PyQt6 import QtCore, QtWidgets
import typing


class FansPage(QtWidgets.QWidget):
    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, self).__init__(parent, flags)

        else:
            super(FansPage, self).__init__()
