from PyQt6 import QtCore, QtWidgets


class FansPage(QtWidgets.QWidget):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None,
        flags: QtCore.Qt.WindowType | None,
    ) -> None:
        if parent is not None and flags is not None:
            super().__init__(parent, flags)

        else:
            super().__init__()
