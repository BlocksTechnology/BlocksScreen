from PyQt6.QtCore import QObject, QEvent, pyqtSignal, pyqtSlot
from enum import Enum, EnumType, IntEnum, Enum
from collections import deque
import typing




class Manager(QObject): 
    
    class KlipperState(Enum): 
        KlipperKilled = 0
        KlipperError = 1
        KlipperStandby = 2
        KlipperIdle = 3
        KlipperPrinting = 4

    def __init__(self, parent: typing.Optional[QObject], printer = None, ws = None ) -> None:
        super(Manager, self).__init__(parent)


        
        
    
    
    def add_connection(self): ...
    


    def rm_connection(self): ...

    
    def register_qtobject(self, object: QObject): ...


    

    
    



class PageViewManager(QObject):
    
    def __init__(self, parent: typing.Optional["QObject"]) -> None:
        super(PageViewManager, self).__init__(parent)

        
        self.index_stack = deque()
    
    def request_view(self, object: QObject, index: typing.Optional[int]= None) -> None: ...
    
    def clean_view(self) -> None: ...
    
    
    
    
    
    
    
    @pyqtSlot(name="request_back_button_pressed")
    def global_back_button(self) -> None:      
        if not len(self.index_stack)  : 
            _logger.debug("Index stack is empty")

        self.main_window.setCurrentIndex(self.index_stack[-1][0])
        self.set_current_panel_index(
            self.index_stack[-1][1]
        )

        self.index_stack.pop()

        self.printer_object_report_signal.connect(self.printer.report_received)
        self.printer_object_list_received_signal.connect(
            self.printer.object_list_received
        )
        
        _logger.debug("Successfully went back a page")
        
    @pyqtSlot(int, int, name="request_change_page")
    def global_change_page(self, tab_index: int, panel_index: int) -> None:
        """global_change_page Changes panels pages globally

        Args:
            tab_index (int): The tab index of the panel
            panel_index (int): The index of the panel page
        """
        if not isinstance(tab_index, int):
            _logger.debug(
                f"Tab index argument expected type int, got {type(tab_index)}"
            )
        if not isinstance(panel_index, int):
            _logger.debug(f"Panel page index expected type int, {type(panel_index)}")
        current_page = [
            self.ui.mainTabWidget.currentIndex(),
            self.current_panel_index(),
        ]
        requested_page = [tab_index, panel_index]
        # * Return if user is already on the requested page
        if requested_page == current_page:
            _logger.debug("User is already on the requested page")
            return
        # * Add to the stack of indexes the indexes of current tab and page in tab to later be able to come back to them
        self.index_stack.append(current_page)
        # * Go to the requested tab and page
        self.ui.mainTabWidget.setCurrentIndex(tab_index)
        self.set_current_panel_index(panel_index)
        _logger.debug(
            f"Requested page change -> Tab index :{requested_page[0]}, pane panel index : {requested_page[1]}"
        )

    def event(self, a0: QEvent | None) -> bool:
        return super().event(a0)

    def installEventFilter(self, a0: QObject | None) -> None:
        return super().installEventFilter(a0)

    
class SearchWindow(): ...


