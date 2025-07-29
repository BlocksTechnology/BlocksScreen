from PyQt6 import QtCore, QtWidgets, QtGui


class LoadingPage(QtWidgets.QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

    def setupUI(self) -> None:
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
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)

        
        # centered_x = (self.width() - myloadingicon.width()) // 2
        # centered_y = (self.height() - myloadingicon.height()) // 2
        # myloadingicon.moveTo(QtCore.QPoint(centered_x, centered_y))
