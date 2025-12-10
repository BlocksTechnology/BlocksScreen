from PyQt6 import QtCore, QtGui, QtWidgets

from lib.utils.icon_button import IconButton


class TroubleshootPage(QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
            #troubleshoot_page { 
                background-image: url(:/background/media/1st_background.png); 
                border: none;
            }
            """
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.label_4.setText(
            "For more information check our website \n www.blockstec.com \n or \nsupport@blockstec.com"
        )
        self.repaint()

    def _geometry_calc(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, width, height)

    def show(self) -> None:
        """Re-implemented method, widget show"""
        self._geometry_calc()
        self.repaint()
        return super().show()

    def _setupUI(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)
