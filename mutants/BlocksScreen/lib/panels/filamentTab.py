import enum
from functools import partial

import logging
from lib.printer import Printer
from lib.filament import Filament
from lib.panels.widgets.popupDialogWidget import Popup
from PyQt6 import QtCore, QtWidgets

from devices.amu import AMUManager

from lib.panels.widgets.amuPage import AMUpage
from lib.panels.widgets.spoolmanPage import SpoolmanPage
from lib.panels.widgets.basePopup import BasePopup

from lib.ui.filamentStackedWidget_ui import Ui_filamentStackedWidget


logger = logging.getLogger(__name__)
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


class FilamentTypes(enum.Enum):
    PLA = Filament(name="PLA", temperature=220)
    PETG = Filament(name="PETG", temperature=240)
    ABS = Filament(name="ABS", temperature=250)
    HIPS = Filament(name="HIPS", temperature=250)
    NYLON = Filament(name="NYLON", temperature=270)
    TPU = Filament(name="TPU", temperature=230)
    UNKNOWN = Filament(name="UNKNOWN", temperature=250)


class FilamentTab(QtWidgets.QStackedWidget):
    request_filament_change_page = QtCore.pyqtSignal(name="filament_change_page")
    request_filament_load = QtCore.pyqtSignal(name="filament_load_t1")
    request_back = QtCore.pyqtSignal(name="request_back")
    request_change_page = QtCore.pyqtSignal(int, int, name="request_change_page")
    request_change_tab = QtCore.pyqtSignal(int, name="request_change_tab")
    request_toolhead_count = QtCore.pyqtSignal(int, name="toolhead_number_received")
    run_gcode = QtCore.pyqtSignal(str, name="run_gcode")
    call_load_panel = QtCore.pyqtSignal(bool, str, name="call-load-panel")

    class FilamentStates(enum.Enum):
        UNKNOWN = -1
        LOADED = enum.auto()
        UNLOADED = enum.auto()

        def __repr__(self) -> str:
            return "<%s.%s>" % (self.__class__.__name__, self._name_)

    def __init__(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        args = [parent, printer, ws, config, amu_manager]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentTabǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁFilamentTabǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁFilamentTabǁ__init____mutmut_orig(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.state = "standby"
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_1(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(None)

        self.ws = ws
        self.printer = printer
        self.state = "standby"
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_2(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = None
        self.printer = printer
        self.state = "standby"
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_3(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = None
        self.state = "standby"
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_4(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.state = None
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_5(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.state = "XXstandbyXX"
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_6(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.state = "STANDBY"
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_7(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.state = "standby"
        self.load_state = None
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_8(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.state = "standby"
        self.load_state = True
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_9(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.state = "standby"
        self.load_state = False
        self.cfg = None
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_10(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.state = "standby"
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = None
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_11(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.state = "standby"
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = None

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_12(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.state = "standby"
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = True

        self.setup_ui()
        self.run_gcode.connect(self.ws.api.run_gcode)

    def xǁFilamentTabǁ__init____mutmut_13(
        self, parent, printer: Printer, ws, config, amu_manager: AMUManager
    ) -> None:
        super().__init__(parent)

        self.ws = ws
        self.printer = printer
        self.state = "standby"
        self.load_state = False
        self.cfg = config
        self.amu_manager: AMUManager = amu_manager
        self.amu_configured = False

        self.setup_ui()
        self.run_gcode.connect(None)
    
    xǁFilamentTabǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentTabǁ__init____mutmut_1': xǁFilamentTabǁ__init____mutmut_1, 
        'xǁFilamentTabǁ__init____mutmut_2': xǁFilamentTabǁ__init____mutmut_2, 
        'xǁFilamentTabǁ__init____mutmut_3': xǁFilamentTabǁ__init____mutmut_3, 
        'xǁFilamentTabǁ__init____mutmut_4': xǁFilamentTabǁ__init____mutmut_4, 
        'xǁFilamentTabǁ__init____mutmut_5': xǁFilamentTabǁ__init____mutmut_5, 
        'xǁFilamentTabǁ__init____mutmut_6': xǁFilamentTabǁ__init____mutmut_6, 
        'xǁFilamentTabǁ__init____mutmut_7': xǁFilamentTabǁ__init____mutmut_7, 
        'xǁFilamentTabǁ__init____mutmut_8': xǁFilamentTabǁ__init____mutmut_8, 
        'xǁFilamentTabǁ__init____mutmut_9': xǁFilamentTabǁ__init____mutmut_9, 
        'xǁFilamentTabǁ__init____mutmut_10': xǁFilamentTabǁ__init____mutmut_10, 
        'xǁFilamentTabǁ__init____mutmut_11': xǁFilamentTabǁ__init____mutmut_11, 
        'xǁFilamentTabǁ__init____mutmut_12': xǁFilamentTabǁ__init____mutmut_12, 
        'xǁFilamentTabǁ__init____mutmut_13': xǁFilamentTabǁ__init____mutmut_13
    }
    xǁFilamentTabǁ__init____mutmut_orig.__name__ = 'xǁFilamentTabǁ__init__'

    def setup_ui(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentTabǁsetup_ui__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentTabǁsetup_ui__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentTabǁsetup_ui__mutmut_orig(self):

        #        if self.amu_manager.is_amu_configured():
        self.amu_manager.mmu_state_changed.connect(self.on_mmu_state_changed)

    def xǁFilamentTabǁsetup_ui__mutmut_1(self):

        #        if self.amu_manager.is_amu_configured():
        self.amu_manager.mmu_state_changed.connect(None)
    
    xǁFilamentTabǁsetup_ui__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentTabǁsetup_ui__mutmut_1': xǁFilamentTabǁsetup_ui__mutmut_1
    }
    xǁFilamentTabǁsetup_ui__mutmut_orig.__name__ = 'xǁFilamentTabǁsetup_ui'

    #        else:
    #            self.without_amu()

    def on_mmu_state_changed(self, mmu_state):
        args = [mmu_state]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentTabǁon_mmu_state_changed__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentTabǁon_mmu_state_changed__mutmut_mutants'), args, kwargs, self)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_orig(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_1(self, mmu_state):
        if self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_2(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) >= 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_3(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 1:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_4(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(None, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_5(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, None)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_6(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_7(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, )
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_8(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(721, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_9(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 421)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_10(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = None
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_11(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(None, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_12(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=None)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_13(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_14(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, )
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_15(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(None)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_16(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(None)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_17(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(None)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_18(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    None
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_19(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: None
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_20(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        None, "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_21(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", None, callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_22(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=None
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_23(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_24(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_25(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_26(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "XXGETXX", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_27(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "get", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_28(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "XX/v1/spoolXX", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_29(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/V1/SPOOL", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_30(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = None
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_31(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(None)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_32(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = None
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_33(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(None, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_34(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, None, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_35(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, None)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_36(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_37(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_38(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, )
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_39(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, True, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_40(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, True)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_41(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(None)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_42(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    None
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_43(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: None
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_44(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        None,
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_45(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        None,
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_46(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=None,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_47(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_48(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_49(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_50(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "XXGETXX",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_51(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "get",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_52(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "XX/v1/spoolXX",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_53(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/V1/SPOOL",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_54(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    None
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_55(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: None
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_56(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=None
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_57(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    None
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_58(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: None
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_59(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(None)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_60(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    None
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_61(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: None
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_62(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        None,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_63(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=None,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_64(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_65(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_66(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    None
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_67(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: None
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_68(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=None
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_69(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    None
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_70(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: None
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_71(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        None,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_72(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        None,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_73(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=None,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_74(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_75(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_76(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_77(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    None
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_78(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: None
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_79(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        None,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_80(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=None,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_81(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_82(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_83(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(None)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_84(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(None)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_85(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = None

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_86(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = False

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_87(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action != "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_88(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "XXIdleXX":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_89(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_90(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "IDLE":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_91(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = None
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_92(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = True
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_93(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(None, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_94(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, None)
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_95(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit("")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_96(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, )
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_97(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(True, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_98(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "XXXX")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_99(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(None, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_100(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, None)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_101(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_102(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, )

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_103(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(False, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_104(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" and mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_105(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action != "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_106(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "XXLoadingXX" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_107(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_108(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "LOADING" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_109(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action != "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_110(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "XXUnloadingXX":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_111(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "unloading":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_112(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "UNLOADING":
            self.load_state = True
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_113(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = None
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_114(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = False
            self.call_load_panel.emit(True, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_115(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(None, mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_116(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, None)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_117(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(mmu_state.action)

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_118(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(True, )

    #        else:
    #            self.without_amu()

    def xǁFilamentTabǁon_mmu_state_changed__mutmut_119(self, mmu_state):
        if not self.amu_configured:
            if len(mmu_state.gates) > 0:
                self.setMinimumSize(720, 420)
                self.amupage = AMUpage(self.amu_manager, parent=self)
                self.addWidget(self.amupage)
                self.amupage.request_back.connect(self.request_back)
                self.amupage.request_gate_map.connect(self.run_gcode)
                self.amupage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET", "/v1/spool", callback=self.amupage.on_spools_received
                    )
                )

                self.spoolmanPage = SpoolmanPage(self)
                self._spoolman_popup = BasePopup(self, False, False)
                self._spoolman_popup.add_widget(self.spoolmanPage)
                self.spoolmanPage.request_spools.connect(
                    lambda: self.ws.api.spoolman_proxy(
                        "GET",
                        "/v1/spool",
                        callback=self.spoolmanPage.on_spools_received,
                    )
                )
                self.spoolmanPage.request_get_spool_id.connect(
                    lambda: self.ws.api.get_spool_id(
                        callback=self.spoolmanPage.on_active_spool_received
                    )
                )
                self.spoolmanPage.request_set_spool_id.connect(
                    lambda spool_id: self.ws.api.set_spool_id(spool_id)
                )
                self.spoolmanPage.request_delete_spool.connect(
                    lambda spool_id: self.ws.api.delete_spool(
                        spool_id,
                        callback=self.spoolmanPage.on_delete_spool_result,
                    )
                )
                self.spoolmanPage.request_filaments.connect(
                    lambda: self.ws.api.get_filaments(
                        callback=self.spoolmanPage.on_filaments_received
                    )
                )
                self.spoolmanPage.request_add_spool.connect(
                    lambda filament_id, body: self.ws.api.add_spool(
                        filament_id,
                        body,
                        callback=self.spoolmanPage.on_add_spool_result,
                    )
                )
                self.spoolmanPage.request_add_filament.connect(
                    lambda body: self.ws.api.add_filament(
                        body,
                        callback=self.spoolmanPage.on_add_filament_result,
                    )
                )
                self.spoolmanPage.request_back.connect(self._spoolman_popup.hide)
                self.amupage.request_open_spoolman.connect(self._spoolman_popup.show)

            else:
                self.without_amu()

            self.amu_configured = True

        if self.load_state:
            if mmu_state.action == "Idle":
                self.load_state = False
                self.call_load_panel.emit(False, "")
                return
            self.call_load_panel.emit(True, mmu_state.action)

        if mmu_state.action == "Loading" or mmu_state.action == "Unloading":
            self.load_state = True
            self.call_load_panel.emit(False, mmu_state.action)
    
    xǁFilamentTabǁon_mmu_state_changed__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentTabǁon_mmu_state_changed__mutmut_1': xǁFilamentTabǁon_mmu_state_changed__mutmut_1, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_2': xǁFilamentTabǁon_mmu_state_changed__mutmut_2, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_3': xǁFilamentTabǁon_mmu_state_changed__mutmut_3, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_4': xǁFilamentTabǁon_mmu_state_changed__mutmut_4, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_5': xǁFilamentTabǁon_mmu_state_changed__mutmut_5, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_6': xǁFilamentTabǁon_mmu_state_changed__mutmut_6, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_7': xǁFilamentTabǁon_mmu_state_changed__mutmut_7, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_8': xǁFilamentTabǁon_mmu_state_changed__mutmut_8, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_9': xǁFilamentTabǁon_mmu_state_changed__mutmut_9, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_10': xǁFilamentTabǁon_mmu_state_changed__mutmut_10, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_11': xǁFilamentTabǁon_mmu_state_changed__mutmut_11, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_12': xǁFilamentTabǁon_mmu_state_changed__mutmut_12, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_13': xǁFilamentTabǁon_mmu_state_changed__mutmut_13, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_14': xǁFilamentTabǁon_mmu_state_changed__mutmut_14, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_15': xǁFilamentTabǁon_mmu_state_changed__mutmut_15, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_16': xǁFilamentTabǁon_mmu_state_changed__mutmut_16, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_17': xǁFilamentTabǁon_mmu_state_changed__mutmut_17, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_18': xǁFilamentTabǁon_mmu_state_changed__mutmut_18, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_19': xǁFilamentTabǁon_mmu_state_changed__mutmut_19, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_20': xǁFilamentTabǁon_mmu_state_changed__mutmut_20, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_21': xǁFilamentTabǁon_mmu_state_changed__mutmut_21, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_22': xǁFilamentTabǁon_mmu_state_changed__mutmut_22, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_23': xǁFilamentTabǁon_mmu_state_changed__mutmut_23, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_24': xǁFilamentTabǁon_mmu_state_changed__mutmut_24, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_25': xǁFilamentTabǁon_mmu_state_changed__mutmut_25, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_26': xǁFilamentTabǁon_mmu_state_changed__mutmut_26, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_27': xǁFilamentTabǁon_mmu_state_changed__mutmut_27, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_28': xǁFilamentTabǁon_mmu_state_changed__mutmut_28, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_29': xǁFilamentTabǁon_mmu_state_changed__mutmut_29, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_30': xǁFilamentTabǁon_mmu_state_changed__mutmut_30, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_31': xǁFilamentTabǁon_mmu_state_changed__mutmut_31, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_32': xǁFilamentTabǁon_mmu_state_changed__mutmut_32, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_33': xǁFilamentTabǁon_mmu_state_changed__mutmut_33, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_34': xǁFilamentTabǁon_mmu_state_changed__mutmut_34, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_35': xǁFilamentTabǁon_mmu_state_changed__mutmut_35, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_36': xǁFilamentTabǁon_mmu_state_changed__mutmut_36, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_37': xǁFilamentTabǁon_mmu_state_changed__mutmut_37, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_38': xǁFilamentTabǁon_mmu_state_changed__mutmut_38, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_39': xǁFilamentTabǁon_mmu_state_changed__mutmut_39, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_40': xǁFilamentTabǁon_mmu_state_changed__mutmut_40, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_41': xǁFilamentTabǁon_mmu_state_changed__mutmut_41, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_42': xǁFilamentTabǁon_mmu_state_changed__mutmut_42, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_43': xǁFilamentTabǁon_mmu_state_changed__mutmut_43, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_44': xǁFilamentTabǁon_mmu_state_changed__mutmut_44, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_45': xǁFilamentTabǁon_mmu_state_changed__mutmut_45, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_46': xǁFilamentTabǁon_mmu_state_changed__mutmut_46, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_47': xǁFilamentTabǁon_mmu_state_changed__mutmut_47, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_48': xǁFilamentTabǁon_mmu_state_changed__mutmut_48, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_49': xǁFilamentTabǁon_mmu_state_changed__mutmut_49, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_50': xǁFilamentTabǁon_mmu_state_changed__mutmut_50, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_51': xǁFilamentTabǁon_mmu_state_changed__mutmut_51, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_52': xǁFilamentTabǁon_mmu_state_changed__mutmut_52, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_53': xǁFilamentTabǁon_mmu_state_changed__mutmut_53, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_54': xǁFilamentTabǁon_mmu_state_changed__mutmut_54, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_55': xǁFilamentTabǁon_mmu_state_changed__mutmut_55, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_56': xǁFilamentTabǁon_mmu_state_changed__mutmut_56, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_57': xǁFilamentTabǁon_mmu_state_changed__mutmut_57, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_58': xǁFilamentTabǁon_mmu_state_changed__mutmut_58, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_59': xǁFilamentTabǁon_mmu_state_changed__mutmut_59, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_60': xǁFilamentTabǁon_mmu_state_changed__mutmut_60, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_61': xǁFilamentTabǁon_mmu_state_changed__mutmut_61, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_62': xǁFilamentTabǁon_mmu_state_changed__mutmut_62, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_63': xǁFilamentTabǁon_mmu_state_changed__mutmut_63, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_64': xǁFilamentTabǁon_mmu_state_changed__mutmut_64, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_65': xǁFilamentTabǁon_mmu_state_changed__mutmut_65, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_66': xǁFilamentTabǁon_mmu_state_changed__mutmut_66, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_67': xǁFilamentTabǁon_mmu_state_changed__mutmut_67, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_68': xǁFilamentTabǁon_mmu_state_changed__mutmut_68, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_69': xǁFilamentTabǁon_mmu_state_changed__mutmut_69, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_70': xǁFilamentTabǁon_mmu_state_changed__mutmut_70, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_71': xǁFilamentTabǁon_mmu_state_changed__mutmut_71, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_72': xǁFilamentTabǁon_mmu_state_changed__mutmut_72, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_73': xǁFilamentTabǁon_mmu_state_changed__mutmut_73, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_74': xǁFilamentTabǁon_mmu_state_changed__mutmut_74, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_75': xǁFilamentTabǁon_mmu_state_changed__mutmut_75, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_76': xǁFilamentTabǁon_mmu_state_changed__mutmut_76, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_77': xǁFilamentTabǁon_mmu_state_changed__mutmut_77, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_78': xǁFilamentTabǁon_mmu_state_changed__mutmut_78, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_79': xǁFilamentTabǁon_mmu_state_changed__mutmut_79, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_80': xǁFilamentTabǁon_mmu_state_changed__mutmut_80, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_81': xǁFilamentTabǁon_mmu_state_changed__mutmut_81, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_82': xǁFilamentTabǁon_mmu_state_changed__mutmut_82, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_83': xǁFilamentTabǁon_mmu_state_changed__mutmut_83, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_84': xǁFilamentTabǁon_mmu_state_changed__mutmut_84, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_85': xǁFilamentTabǁon_mmu_state_changed__mutmut_85, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_86': xǁFilamentTabǁon_mmu_state_changed__mutmut_86, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_87': xǁFilamentTabǁon_mmu_state_changed__mutmut_87, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_88': xǁFilamentTabǁon_mmu_state_changed__mutmut_88, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_89': xǁFilamentTabǁon_mmu_state_changed__mutmut_89, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_90': xǁFilamentTabǁon_mmu_state_changed__mutmut_90, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_91': xǁFilamentTabǁon_mmu_state_changed__mutmut_91, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_92': xǁFilamentTabǁon_mmu_state_changed__mutmut_92, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_93': xǁFilamentTabǁon_mmu_state_changed__mutmut_93, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_94': xǁFilamentTabǁon_mmu_state_changed__mutmut_94, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_95': xǁFilamentTabǁon_mmu_state_changed__mutmut_95, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_96': xǁFilamentTabǁon_mmu_state_changed__mutmut_96, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_97': xǁFilamentTabǁon_mmu_state_changed__mutmut_97, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_98': xǁFilamentTabǁon_mmu_state_changed__mutmut_98, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_99': xǁFilamentTabǁon_mmu_state_changed__mutmut_99, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_100': xǁFilamentTabǁon_mmu_state_changed__mutmut_100, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_101': xǁFilamentTabǁon_mmu_state_changed__mutmut_101, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_102': xǁFilamentTabǁon_mmu_state_changed__mutmut_102, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_103': xǁFilamentTabǁon_mmu_state_changed__mutmut_103, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_104': xǁFilamentTabǁon_mmu_state_changed__mutmut_104, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_105': xǁFilamentTabǁon_mmu_state_changed__mutmut_105, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_106': xǁFilamentTabǁon_mmu_state_changed__mutmut_106, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_107': xǁFilamentTabǁon_mmu_state_changed__mutmut_107, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_108': xǁFilamentTabǁon_mmu_state_changed__mutmut_108, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_109': xǁFilamentTabǁon_mmu_state_changed__mutmut_109, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_110': xǁFilamentTabǁon_mmu_state_changed__mutmut_110, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_111': xǁFilamentTabǁon_mmu_state_changed__mutmut_111, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_112': xǁFilamentTabǁon_mmu_state_changed__mutmut_112, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_113': xǁFilamentTabǁon_mmu_state_changed__mutmut_113, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_114': xǁFilamentTabǁon_mmu_state_changed__mutmut_114, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_115': xǁFilamentTabǁon_mmu_state_changed__mutmut_115, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_116': xǁFilamentTabǁon_mmu_state_changed__mutmut_116, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_117': xǁFilamentTabǁon_mmu_state_changed__mutmut_117, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_118': xǁFilamentTabǁon_mmu_state_changed__mutmut_118, 
        'xǁFilamentTabǁon_mmu_state_changed__mutmut_119': xǁFilamentTabǁon_mmu_state_changed__mutmut_119
    }
    xǁFilamentTabǁon_mmu_state_changed__mutmut_orig.__name__ = 'xǁFilamentTabǁon_mmu_state_changed'

    def without_amu(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentTabǁwithout_amu__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentTabǁwithout_amu__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentTabǁwithout_amu__mutmut_orig(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_1(self):
        self.panel = None
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_2(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(None)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_3(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(None)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_4(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(1)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_5(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = None
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_6(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 1
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_7(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = None
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_8(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 1
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_9(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = None
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_10(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 1
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_11(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = None
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_12(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(None)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_13(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = ""
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_14(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = None
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_15(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = None

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_16(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section(None):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_17(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("XXfilament_presenceXX"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_18(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("FILAMENT_PRESENCE"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_19(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = None
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_20(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section(None, None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_21(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section(None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_22(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", )
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_23(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("XXfilament_presenceXX", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_24(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("FILAMENT_PRESENCE", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_25(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = None
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_26(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get(None, str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_27(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", None, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_28(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get(str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_29(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_30(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, )
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_31(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("XXnameXX", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_32(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("NAME", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_33(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = ""
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_34(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            None
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_35(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(None, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_36(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, None)
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_37(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_38(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, )
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_39(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(None))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_40(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(None)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_41(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(None)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_42(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            None
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_43(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(None, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_44(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=None, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_45(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=None)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_46(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_47(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_48(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, )
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_49(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=1, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_50(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            None
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_51(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(None, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_52(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=None, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_53(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=None)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_54(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_55(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_56(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, )
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_57(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=1, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_58(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            None
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_59(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(None, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_60(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=None, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_61(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=None)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_62(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_63(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_64(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, )
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_65(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=1, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_66(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            None
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_67(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(None, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_68(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=None, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_69(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=None)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_70(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_71(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_72(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, )
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_73(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=1, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_74(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            None
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_75(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(None, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_76(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=None, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_77(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=None)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_78(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_79(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_80(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, )
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_81(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=1, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_82(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            None
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_83(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(None, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_84(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=None, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_85(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=None)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_86(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_87(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_88(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, )
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_89(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=1, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_90(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            None
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_91(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: None
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_92(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=None, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_93(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=None)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_94(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_95(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, )
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_96(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=1, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_97(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=251)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_98(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            None
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_99(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: None
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_100(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(None)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_101(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(1)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_102(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(None)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_103(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(None)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_104(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            None
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_105(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(None)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_106(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(None)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_107(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(None)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_108(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(None)
        self.state = "standby"

    def xǁFilamentTabǁwithout_amu__mutmut_109(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = None

    def xǁFilamentTabǁwithout_amu__mutmut_110(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "XXstandbyXX"

    def xǁFilamentTabǁwithout_amu__mutmut_111(self):
        self.panel = Ui_filamentStackedWidget()
        self.panel.setupUi(self)
        self.setCurrentIndex(0)
        self.toolhead_count: int = 0
        self.target_temp: int = 0
        self.current_temp: int = 0
        self.popup = Popup(self)
        self.has_load_unload_objects = None
        self._filament_state = self.FilamentStates.UNKNOWN
        self.filament_type = FilamentTypes.UNKNOWN

        if self.cfg.has_section("filament_presence"):
            i = self.cfg.get_section("filament_presence", None)
            self.filament_sensor = i.get("name", str, None)
        else:
            self.filament_sensor = None
        self.panel.filament_page_load_btn.clicked.connect(
            partial(self.change_page, self.indexOf(self.panel.load_page))
        )
        self.panel.custom_filament_header_back_btn.clicked.connect(self.back_button)
        self.panel.load_custom_btn.hide()
        self.panel.load_header_back_button.clicked.connect(self.back_button)
        self.panel.load_pla_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PLA)
        )
        self.panel.load_petg_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.PETG)
        )
        self.panel.load_abs_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.ABS)
        )
        self.panel.load_hips_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.HIPS)
        )
        self.panel.load_nylon_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.NYLON)
        )
        self.panel.load_tpu_btn.clicked.connect(
            partial(self.load_filament, toolhead=0, filament=FilamentTypes.TPU)
        )
        self.panel.filament_page_unload_btn.clicked.connect(
            lambda: self.unload_filament(toolhead=0, temp=250)
        )
        self.panel.main_back_button.clicked.connect(
            lambda: self.request_change_tab.emit(0)
        )
        self.printer.unload_filament_update.connect(self.on_unload_filament)
        self.printer.load_filament_update.connect(self.on_load_filament)
        self.printer.filament_switch_sensor_update.connect(
            self.on_filament_sensor_update
        )

        self.printer.print_stats_update[str, str].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, dict].connect(self.on_print_stats_update)
        self.printer.print_stats_update[str, float].connect(self.on_print_stats_update)

        self.printer.save_variables_update.connect(self.on_save_variables_update)
        self.state = "STANDBY"
    
    xǁFilamentTabǁwithout_amu__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentTabǁwithout_amu__mutmut_1': xǁFilamentTabǁwithout_amu__mutmut_1, 
        'xǁFilamentTabǁwithout_amu__mutmut_2': xǁFilamentTabǁwithout_amu__mutmut_2, 
        'xǁFilamentTabǁwithout_amu__mutmut_3': xǁFilamentTabǁwithout_amu__mutmut_3, 
        'xǁFilamentTabǁwithout_amu__mutmut_4': xǁFilamentTabǁwithout_amu__mutmut_4, 
        'xǁFilamentTabǁwithout_amu__mutmut_5': xǁFilamentTabǁwithout_amu__mutmut_5, 
        'xǁFilamentTabǁwithout_amu__mutmut_6': xǁFilamentTabǁwithout_amu__mutmut_6, 
        'xǁFilamentTabǁwithout_amu__mutmut_7': xǁFilamentTabǁwithout_amu__mutmut_7, 
        'xǁFilamentTabǁwithout_amu__mutmut_8': xǁFilamentTabǁwithout_amu__mutmut_8, 
        'xǁFilamentTabǁwithout_amu__mutmut_9': xǁFilamentTabǁwithout_amu__mutmut_9, 
        'xǁFilamentTabǁwithout_amu__mutmut_10': xǁFilamentTabǁwithout_amu__mutmut_10, 
        'xǁFilamentTabǁwithout_amu__mutmut_11': xǁFilamentTabǁwithout_amu__mutmut_11, 
        'xǁFilamentTabǁwithout_amu__mutmut_12': xǁFilamentTabǁwithout_amu__mutmut_12, 
        'xǁFilamentTabǁwithout_amu__mutmut_13': xǁFilamentTabǁwithout_amu__mutmut_13, 
        'xǁFilamentTabǁwithout_amu__mutmut_14': xǁFilamentTabǁwithout_amu__mutmut_14, 
        'xǁFilamentTabǁwithout_amu__mutmut_15': xǁFilamentTabǁwithout_amu__mutmut_15, 
        'xǁFilamentTabǁwithout_amu__mutmut_16': xǁFilamentTabǁwithout_amu__mutmut_16, 
        'xǁFilamentTabǁwithout_amu__mutmut_17': xǁFilamentTabǁwithout_amu__mutmut_17, 
        'xǁFilamentTabǁwithout_amu__mutmut_18': xǁFilamentTabǁwithout_amu__mutmut_18, 
        'xǁFilamentTabǁwithout_amu__mutmut_19': xǁFilamentTabǁwithout_amu__mutmut_19, 
        'xǁFilamentTabǁwithout_amu__mutmut_20': xǁFilamentTabǁwithout_amu__mutmut_20, 
        'xǁFilamentTabǁwithout_amu__mutmut_21': xǁFilamentTabǁwithout_amu__mutmut_21, 
        'xǁFilamentTabǁwithout_amu__mutmut_22': xǁFilamentTabǁwithout_amu__mutmut_22, 
        'xǁFilamentTabǁwithout_amu__mutmut_23': xǁFilamentTabǁwithout_amu__mutmut_23, 
        'xǁFilamentTabǁwithout_amu__mutmut_24': xǁFilamentTabǁwithout_amu__mutmut_24, 
        'xǁFilamentTabǁwithout_amu__mutmut_25': xǁFilamentTabǁwithout_amu__mutmut_25, 
        'xǁFilamentTabǁwithout_amu__mutmut_26': xǁFilamentTabǁwithout_amu__mutmut_26, 
        'xǁFilamentTabǁwithout_amu__mutmut_27': xǁFilamentTabǁwithout_amu__mutmut_27, 
        'xǁFilamentTabǁwithout_amu__mutmut_28': xǁFilamentTabǁwithout_amu__mutmut_28, 
        'xǁFilamentTabǁwithout_amu__mutmut_29': xǁFilamentTabǁwithout_amu__mutmut_29, 
        'xǁFilamentTabǁwithout_amu__mutmut_30': xǁFilamentTabǁwithout_amu__mutmut_30, 
        'xǁFilamentTabǁwithout_amu__mutmut_31': xǁFilamentTabǁwithout_amu__mutmut_31, 
        'xǁFilamentTabǁwithout_amu__mutmut_32': xǁFilamentTabǁwithout_amu__mutmut_32, 
        'xǁFilamentTabǁwithout_amu__mutmut_33': xǁFilamentTabǁwithout_amu__mutmut_33, 
        'xǁFilamentTabǁwithout_amu__mutmut_34': xǁFilamentTabǁwithout_amu__mutmut_34, 
        'xǁFilamentTabǁwithout_amu__mutmut_35': xǁFilamentTabǁwithout_amu__mutmut_35, 
        'xǁFilamentTabǁwithout_amu__mutmut_36': xǁFilamentTabǁwithout_amu__mutmut_36, 
        'xǁFilamentTabǁwithout_amu__mutmut_37': xǁFilamentTabǁwithout_amu__mutmut_37, 
        'xǁFilamentTabǁwithout_amu__mutmut_38': xǁFilamentTabǁwithout_amu__mutmut_38, 
        'xǁFilamentTabǁwithout_amu__mutmut_39': xǁFilamentTabǁwithout_amu__mutmut_39, 
        'xǁFilamentTabǁwithout_amu__mutmut_40': xǁFilamentTabǁwithout_amu__mutmut_40, 
        'xǁFilamentTabǁwithout_amu__mutmut_41': xǁFilamentTabǁwithout_amu__mutmut_41, 
        'xǁFilamentTabǁwithout_amu__mutmut_42': xǁFilamentTabǁwithout_amu__mutmut_42, 
        'xǁFilamentTabǁwithout_amu__mutmut_43': xǁFilamentTabǁwithout_amu__mutmut_43, 
        'xǁFilamentTabǁwithout_amu__mutmut_44': xǁFilamentTabǁwithout_amu__mutmut_44, 
        'xǁFilamentTabǁwithout_amu__mutmut_45': xǁFilamentTabǁwithout_amu__mutmut_45, 
        'xǁFilamentTabǁwithout_amu__mutmut_46': xǁFilamentTabǁwithout_amu__mutmut_46, 
        'xǁFilamentTabǁwithout_amu__mutmut_47': xǁFilamentTabǁwithout_amu__mutmut_47, 
        'xǁFilamentTabǁwithout_amu__mutmut_48': xǁFilamentTabǁwithout_amu__mutmut_48, 
        'xǁFilamentTabǁwithout_amu__mutmut_49': xǁFilamentTabǁwithout_amu__mutmut_49, 
        'xǁFilamentTabǁwithout_amu__mutmut_50': xǁFilamentTabǁwithout_amu__mutmut_50, 
        'xǁFilamentTabǁwithout_amu__mutmut_51': xǁFilamentTabǁwithout_amu__mutmut_51, 
        'xǁFilamentTabǁwithout_amu__mutmut_52': xǁFilamentTabǁwithout_amu__mutmut_52, 
        'xǁFilamentTabǁwithout_amu__mutmut_53': xǁFilamentTabǁwithout_amu__mutmut_53, 
        'xǁFilamentTabǁwithout_amu__mutmut_54': xǁFilamentTabǁwithout_amu__mutmut_54, 
        'xǁFilamentTabǁwithout_amu__mutmut_55': xǁFilamentTabǁwithout_amu__mutmut_55, 
        'xǁFilamentTabǁwithout_amu__mutmut_56': xǁFilamentTabǁwithout_amu__mutmut_56, 
        'xǁFilamentTabǁwithout_amu__mutmut_57': xǁFilamentTabǁwithout_amu__mutmut_57, 
        'xǁFilamentTabǁwithout_amu__mutmut_58': xǁFilamentTabǁwithout_amu__mutmut_58, 
        'xǁFilamentTabǁwithout_amu__mutmut_59': xǁFilamentTabǁwithout_amu__mutmut_59, 
        'xǁFilamentTabǁwithout_amu__mutmut_60': xǁFilamentTabǁwithout_amu__mutmut_60, 
        'xǁFilamentTabǁwithout_amu__mutmut_61': xǁFilamentTabǁwithout_amu__mutmut_61, 
        'xǁFilamentTabǁwithout_amu__mutmut_62': xǁFilamentTabǁwithout_amu__mutmut_62, 
        'xǁFilamentTabǁwithout_amu__mutmut_63': xǁFilamentTabǁwithout_amu__mutmut_63, 
        'xǁFilamentTabǁwithout_amu__mutmut_64': xǁFilamentTabǁwithout_amu__mutmut_64, 
        'xǁFilamentTabǁwithout_amu__mutmut_65': xǁFilamentTabǁwithout_amu__mutmut_65, 
        'xǁFilamentTabǁwithout_amu__mutmut_66': xǁFilamentTabǁwithout_amu__mutmut_66, 
        'xǁFilamentTabǁwithout_amu__mutmut_67': xǁFilamentTabǁwithout_amu__mutmut_67, 
        'xǁFilamentTabǁwithout_amu__mutmut_68': xǁFilamentTabǁwithout_amu__mutmut_68, 
        'xǁFilamentTabǁwithout_amu__mutmut_69': xǁFilamentTabǁwithout_amu__mutmut_69, 
        'xǁFilamentTabǁwithout_amu__mutmut_70': xǁFilamentTabǁwithout_amu__mutmut_70, 
        'xǁFilamentTabǁwithout_amu__mutmut_71': xǁFilamentTabǁwithout_amu__mutmut_71, 
        'xǁFilamentTabǁwithout_amu__mutmut_72': xǁFilamentTabǁwithout_amu__mutmut_72, 
        'xǁFilamentTabǁwithout_amu__mutmut_73': xǁFilamentTabǁwithout_amu__mutmut_73, 
        'xǁFilamentTabǁwithout_amu__mutmut_74': xǁFilamentTabǁwithout_amu__mutmut_74, 
        'xǁFilamentTabǁwithout_amu__mutmut_75': xǁFilamentTabǁwithout_amu__mutmut_75, 
        'xǁFilamentTabǁwithout_amu__mutmut_76': xǁFilamentTabǁwithout_amu__mutmut_76, 
        'xǁFilamentTabǁwithout_amu__mutmut_77': xǁFilamentTabǁwithout_amu__mutmut_77, 
        'xǁFilamentTabǁwithout_amu__mutmut_78': xǁFilamentTabǁwithout_amu__mutmut_78, 
        'xǁFilamentTabǁwithout_amu__mutmut_79': xǁFilamentTabǁwithout_amu__mutmut_79, 
        'xǁFilamentTabǁwithout_amu__mutmut_80': xǁFilamentTabǁwithout_amu__mutmut_80, 
        'xǁFilamentTabǁwithout_amu__mutmut_81': xǁFilamentTabǁwithout_amu__mutmut_81, 
        'xǁFilamentTabǁwithout_amu__mutmut_82': xǁFilamentTabǁwithout_amu__mutmut_82, 
        'xǁFilamentTabǁwithout_amu__mutmut_83': xǁFilamentTabǁwithout_amu__mutmut_83, 
        'xǁFilamentTabǁwithout_amu__mutmut_84': xǁFilamentTabǁwithout_amu__mutmut_84, 
        'xǁFilamentTabǁwithout_amu__mutmut_85': xǁFilamentTabǁwithout_amu__mutmut_85, 
        'xǁFilamentTabǁwithout_amu__mutmut_86': xǁFilamentTabǁwithout_amu__mutmut_86, 
        'xǁFilamentTabǁwithout_amu__mutmut_87': xǁFilamentTabǁwithout_amu__mutmut_87, 
        'xǁFilamentTabǁwithout_amu__mutmut_88': xǁFilamentTabǁwithout_amu__mutmut_88, 
        'xǁFilamentTabǁwithout_amu__mutmut_89': xǁFilamentTabǁwithout_amu__mutmut_89, 
        'xǁFilamentTabǁwithout_amu__mutmut_90': xǁFilamentTabǁwithout_amu__mutmut_90, 
        'xǁFilamentTabǁwithout_amu__mutmut_91': xǁFilamentTabǁwithout_amu__mutmut_91, 
        'xǁFilamentTabǁwithout_amu__mutmut_92': xǁFilamentTabǁwithout_amu__mutmut_92, 
        'xǁFilamentTabǁwithout_amu__mutmut_93': xǁFilamentTabǁwithout_amu__mutmut_93, 
        'xǁFilamentTabǁwithout_amu__mutmut_94': xǁFilamentTabǁwithout_amu__mutmut_94, 
        'xǁFilamentTabǁwithout_amu__mutmut_95': xǁFilamentTabǁwithout_amu__mutmut_95, 
        'xǁFilamentTabǁwithout_amu__mutmut_96': xǁFilamentTabǁwithout_amu__mutmut_96, 
        'xǁFilamentTabǁwithout_amu__mutmut_97': xǁFilamentTabǁwithout_amu__mutmut_97, 
        'xǁFilamentTabǁwithout_amu__mutmut_98': xǁFilamentTabǁwithout_amu__mutmut_98, 
        'xǁFilamentTabǁwithout_amu__mutmut_99': xǁFilamentTabǁwithout_amu__mutmut_99, 
        'xǁFilamentTabǁwithout_amu__mutmut_100': xǁFilamentTabǁwithout_amu__mutmut_100, 
        'xǁFilamentTabǁwithout_amu__mutmut_101': xǁFilamentTabǁwithout_amu__mutmut_101, 
        'xǁFilamentTabǁwithout_amu__mutmut_102': xǁFilamentTabǁwithout_amu__mutmut_102, 
        'xǁFilamentTabǁwithout_amu__mutmut_103': xǁFilamentTabǁwithout_amu__mutmut_103, 
        'xǁFilamentTabǁwithout_amu__mutmut_104': xǁFilamentTabǁwithout_amu__mutmut_104, 
        'xǁFilamentTabǁwithout_amu__mutmut_105': xǁFilamentTabǁwithout_amu__mutmut_105, 
        'xǁFilamentTabǁwithout_amu__mutmut_106': xǁFilamentTabǁwithout_amu__mutmut_106, 
        'xǁFilamentTabǁwithout_amu__mutmut_107': xǁFilamentTabǁwithout_amu__mutmut_107, 
        'xǁFilamentTabǁwithout_amu__mutmut_108': xǁFilamentTabǁwithout_amu__mutmut_108, 
        'xǁFilamentTabǁwithout_amu__mutmut_109': xǁFilamentTabǁwithout_amu__mutmut_109, 
        'xǁFilamentTabǁwithout_amu__mutmut_110': xǁFilamentTabǁwithout_amu__mutmut_110, 
        'xǁFilamentTabǁwithout_amu__mutmut_111': xǁFilamentTabǁwithout_amu__mutmut_111
    }
    xǁFilamentTabǁwithout_amu__mutmut_orig.__name__ = 'xǁFilamentTabǁwithout_amu'

    def on_save_variables_update(self, save_variables: dict):
        args = [save_variables]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentTabǁon_save_variables_update__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentTabǁon_save_variables_update__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentTabǁon_save_variables_update__mutmut_orig(self, save_variables: dict):
        """Handle query response"""
        for i in FilamentTypes:
            if i.value.name in save_variables["variables"]["filament_type"]:
                self.filament_type = i
                break
            else:
                self.filament_type = FilamentTypes.UNKNOWN
        self.panel.label_2.setText(self.filament_type.value.name)

    def xǁFilamentTabǁon_save_variables_update__mutmut_1(self, save_variables: dict):
        """Handle query response"""
        for i in FilamentTypes:
            if i.value.name not in save_variables["variables"]["filament_type"]:
                self.filament_type = i
                break
            else:
                self.filament_type = FilamentTypes.UNKNOWN
        self.panel.label_2.setText(self.filament_type.value.name)

    def xǁFilamentTabǁon_save_variables_update__mutmut_2(self, save_variables: dict):
        """Handle query response"""
        for i in FilamentTypes:
            if i.value.name in save_variables["XXvariablesXX"]["filament_type"]:
                self.filament_type = i
                break
            else:
                self.filament_type = FilamentTypes.UNKNOWN
        self.panel.label_2.setText(self.filament_type.value.name)

    def xǁFilamentTabǁon_save_variables_update__mutmut_3(self, save_variables: dict):
        """Handle query response"""
        for i in FilamentTypes:
            if i.value.name in save_variables["VARIABLES"]["filament_type"]:
                self.filament_type = i
                break
            else:
                self.filament_type = FilamentTypes.UNKNOWN
        self.panel.label_2.setText(self.filament_type.value.name)

    def xǁFilamentTabǁon_save_variables_update__mutmut_4(self, save_variables: dict):
        """Handle query response"""
        for i in FilamentTypes:
            if i.value.name in save_variables["variables"]["XXfilament_typeXX"]:
                self.filament_type = i
                break
            else:
                self.filament_type = FilamentTypes.UNKNOWN
        self.panel.label_2.setText(self.filament_type.value.name)

    def xǁFilamentTabǁon_save_variables_update__mutmut_5(self, save_variables: dict):
        """Handle query response"""
        for i in FilamentTypes:
            if i.value.name in save_variables["variables"]["FILAMENT_TYPE"]:
                self.filament_type = i
                break
            else:
                self.filament_type = FilamentTypes.UNKNOWN
        self.panel.label_2.setText(self.filament_type.value.name)

    def xǁFilamentTabǁon_save_variables_update__mutmut_6(self, save_variables: dict):
        """Handle query response"""
        for i in FilamentTypes:
            if i.value.name in save_variables["variables"]["filament_type"]:
                self.filament_type = None
                break
            else:
                self.filament_type = FilamentTypes.UNKNOWN
        self.panel.label_2.setText(self.filament_type.value.name)

    def xǁFilamentTabǁon_save_variables_update__mutmut_7(self, save_variables: dict):
        """Handle query response"""
        for i in FilamentTypes:
            if i.value.name in save_variables["variables"]["filament_type"]:
                self.filament_type = i
                return
            else:
                self.filament_type = FilamentTypes.UNKNOWN
        self.panel.label_2.setText(self.filament_type.value.name)

    def xǁFilamentTabǁon_save_variables_update__mutmut_8(self, save_variables: dict):
        """Handle query response"""
        for i in FilamentTypes:
            if i.value.name in save_variables["variables"]["filament_type"]:
                self.filament_type = i
                break
            else:
                self.filament_type = None
        self.panel.label_2.setText(self.filament_type.value.name)

    def xǁFilamentTabǁon_save_variables_update__mutmut_9(self, save_variables: dict):
        """Handle query response"""
        for i in FilamentTypes:
            if i.value.name in save_variables["variables"]["filament_type"]:
                self.filament_type = i
                break
            else:
                self.filament_type = FilamentTypes.UNKNOWN
        self.panel.label_2.setText(None)
    
    xǁFilamentTabǁon_save_variables_update__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentTabǁon_save_variables_update__mutmut_1': xǁFilamentTabǁon_save_variables_update__mutmut_1, 
        'xǁFilamentTabǁon_save_variables_update__mutmut_2': xǁFilamentTabǁon_save_variables_update__mutmut_2, 
        'xǁFilamentTabǁon_save_variables_update__mutmut_3': xǁFilamentTabǁon_save_variables_update__mutmut_3, 
        'xǁFilamentTabǁon_save_variables_update__mutmut_4': xǁFilamentTabǁon_save_variables_update__mutmut_4, 
        'xǁFilamentTabǁon_save_variables_update__mutmut_5': xǁFilamentTabǁon_save_variables_update__mutmut_5, 
        'xǁFilamentTabǁon_save_variables_update__mutmut_6': xǁFilamentTabǁon_save_variables_update__mutmut_6, 
        'xǁFilamentTabǁon_save_variables_update__mutmut_7': xǁFilamentTabǁon_save_variables_update__mutmut_7, 
        'xǁFilamentTabǁon_save_variables_update__mutmut_8': xǁFilamentTabǁon_save_variables_update__mutmut_8, 
        'xǁFilamentTabǁon_save_variables_update__mutmut_9': xǁFilamentTabǁon_save_variables_update__mutmut_9
    }
    xǁFilamentTabǁon_save_variables_update__mutmut_orig.__name__ = 'xǁFilamentTabǁon_save_variables_update'

    @QtCore.pyqtSlot(str, dict, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, float, name="on_print_stats_update")
    @QtCore.pyqtSlot(str, str, name="on_print_stats_update")
    def on_print_stats_update(self, field: str, value: dict | float | str) -> None:
        """Handle print stats object update"""
        if isinstance(value, str):
            if "state" in field:
                self.state = value
                if value in ("printing", "pausing", "paused", "resuming"):
                    self.panel.main_back_button.show()
                    self.panel.spacerItem1.changeSize(
                        60,
                        0,
                        QtWidgets.QSizePolicy.Policy.Minimum,
                        QtWidgets.QSizePolicy.Policy.Minimum,
                    )
                if value in ("standby"):
                    self.panel.main_back_button.hide()
                    self.panel.spacerItem1.changeSize(
                        0,
                        0,
                        QtWidgets.QSizePolicy.Policy.Minimum,
                        QtWidgets.QSizePolicy.Policy.Minimum,
                    )

    @QtCore.pyqtSlot(str, str, bool, name="on_filament_sensor_update")
    def on_filament_sensor_update(self, sensor_name: str, parameter: str, value: bool):
        """Handle filament sensor object update"""
        if parameter == "filament_detected":
            if not isinstance(value, bool):
                self._filament_state = self.FilamentStates.UNKNOWN
                self.handle_filament_state()
                return
            if sensor_name == self.filament_sensor:
                if value:
                    self._filament_state = self.FilamentStates.LOADED
                else:
                    self._filament_state = self.FilamentStates.UNLOADED
                return
        self.handle_filament_state()

    @QtCore.pyqtSlot(dict, name="on_load_filament")
    def on_load_filament(self, status: dict):
        """Handle load filament object updated"""
        if "state" in status.keys():
            if not status["state"]:
                self.target_temp = 0
                self.call_load_panel.emit(False, "")
                if self.state == "paused":
                    self.request_change_tab.emit(0)
                return
        self.call_load_panel.emit(
            True, f"Loading Filament\n{status['step'].capitalize()}"
        )
        self.handle_filament_state()

    @QtCore.pyqtSlot(dict, name="on_unload_filament")
    def on_unload_filament(self, status: dict):
        """Handle unload filament object updated"""
        if "state" in status.keys():
            if not status["state"]:
                self.target_temp = 0
                self.call_load_panel.emit(False, "")
                return
        self.call_load_panel.emit(
            True, f"Unloading Filament\n{status['step'].capitalize()}"
        )
        self.handle_filament_state()

    @QtCore.pyqtSlot(int, int, name="load_filament")
    def load_filament(
        self, toolhead: int = 0, filament: FilamentTypes = FilamentTypes.UNKNOWN
    ) -> None:
        """Handle load filament buttons clicked"""
        if not self.isVisible:
            return

        if self._filament_state == self.FilamentStates.UNKNOWN:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Unable to detect whether the filament is loaded or unloaded.",
            )

        if self._filament_state == self.FilamentStates.LOADED:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Filament is already loaded.",
            )
            return
        self.call_load_panel.emit(True, "Loading Filament")
        self.run_gcode.emit(
            f"""SAVE_VARIABLE VARIABLE=filament_type VALUE='"{filament.value.name}"'"""
        )
        self.run_gcode.emit("MMU_LOAD")

    @QtCore.pyqtSlot(str, int, name="unload_filament")
    def unload_filament(self, toolhead: int = 0, temp: int = 220) -> None:
        """Handle unload filament button clicked"""
        if not self.isVisible:
            return

        if self._filament_state == self.FilamentStates.UNKNOWN:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Unable to detect whether the filament is loaded or unloaded.",
            )

        if self._filament_state == self.FilamentStates.UNLOADED:
            self.popup.new_message(
                message_type=Popup.MessageType.ERROR,
                message="Filament is already unloaded.",
            )
            return

        self.find_routine_objects()
        self.call_load_panel.emit(True, "Unloading Filament")
        self.run_gcode.emit(
            f"""SAVE_VARIABLE VARIABLE=filament_type VALUE='"{FilamentTypes.UNKNOWN.value.name}"'"""
        )
        self.run_gcode.emit("MMU_UNLOAD")

    def handle_filament_state(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentTabǁhandle_filament_state__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentTabǁhandle_filament_state__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentTabǁhandle_filament_state__mutmut_orig(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_1(self):
        """Handle ui changes on filament states"""
        if self._filament_state != self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_2(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(None)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_3(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_4(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(None)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_5(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(True)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_6(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state != self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_7(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(None)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_8(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_9(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(None)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_10(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(False)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_11(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(None)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_12(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(False)
            self.panel.filament_page_unload_btn.setEnabled(True)

    def xǁFilamentTabǁhandle_filament_state__mutmut_13(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(None)

    def xǁFilamentTabǁhandle_filament_state__mutmut_14(self):
        """Handle ui changes on filament states"""
        if self._filament_state == self.FilamentStates.LOADED:
            self.panel.filament_page_unload_btn.setEnabled(True)
            self.panel.filament_page_load_btn.setEnabled(False)
        elif self._filament_state == self.FilamentStates.UNLOADED:
            self.panel.filament_page_unload_btn.setEnabled(False)
            self.panel.filament_page_load_btn.setEnabled(True)
        else:
            self.panel.filament_page_load_btn.setEnabled(True)
            self.panel.filament_page_unload_btn.setEnabled(False)
    
    xǁFilamentTabǁhandle_filament_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentTabǁhandle_filament_state__mutmut_1': xǁFilamentTabǁhandle_filament_state__mutmut_1, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_2': xǁFilamentTabǁhandle_filament_state__mutmut_2, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_3': xǁFilamentTabǁhandle_filament_state__mutmut_3, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_4': xǁFilamentTabǁhandle_filament_state__mutmut_4, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_5': xǁFilamentTabǁhandle_filament_state__mutmut_5, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_6': xǁFilamentTabǁhandle_filament_state__mutmut_6, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_7': xǁFilamentTabǁhandle_filament_state__mutmut_7, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_8': xǁFilamentTabǁhandle_filament_state__mutmut_8, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_9': xǁFilamentTabǁhandle_filament_state__mutmut_9, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_10': xǁFilamentTabǁhandle_filament_state__mutmut_10, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_11': xǁFilamentTabǁhandle_filament_state__mutmut_11, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_12': xǁFilamentTabǁhandle_filament_state__mutmut_12, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_13': xǁFilamentTabǁhandle_filament_state__mutmut_13, 
        'xǁFilamentTabǁhandle_filament_state__mutmut_14': xǁFilamentTabǁhandle_filament_state__mutmut_14
    }
    xǁFilamentTabǁhandle_filament_state__mutmut_orig.__name__ = 'xǁFilamentTabǁhandle_filament_state'

    @property
    def filament_state(self):
        return self._filament_state

    def change_page(self, index):
        args = [index]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentTabǁchange_page__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentTabǁchange_page__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentTabǁchange_page__mutmut_orig(self, index):
        """Issue a page change"""
        self.request_change_page.emit(1, index)

    def xǁFilamentTabǁchange_page__mutmut_1(self, index):
        """Issue a page change"""
        self.request_change_page.emit(None, index)

    def xǁFilamentTabǁchange_page__mutmut_2(self, index):
        """Issue a page change"""
        self.request_change_page.emit(1, None)

    def xǁFilamentTabǁchange_page__mutmut_3(self, index):
        """Issue a page change"""
        self.request_change_page.emit(index)

    def xǁFilamentTabǁchange_page__mutmut_4(self, index):
        """Issue a page change"""
        self.request_change_page.emit(1, )

    def xǁFilamentTabǁchange_page__mutmut_5(self, index):
        """Issue a page change"""
        self.request_change_page.emit(2, index)
    
    xǁFilamentTabǁchange_page__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentTabǁchange_page__mutmut_1': xǁFilamentTabǁchange_page__mutmut_1, 
        'xǁFilamentTabǁchange_page__mutmut_2': xǁFilamentTabǁchange_page__mutmut_2, 
        'xǁFilamentTabǁchange_page__mutmut_3': xǁFilamentTabǁchange_page__mutmut_3, 
        'xǁFilamentTabǁchange_page__mutmut_4': xǁFilamentTabǁchange_page__mutmut_4, 
        'xǁFilamentTabǁchange_page__mutmut_5': xǁFilamentTabǁchange_page__mutmut_5
    }
    xǁFilamentTabǁchange_page__mutmut_orig.__name__ = 'xǁFilamentTabǁchange_page'

    def back_button(self):
        """Go back a page"""
        self.request_back.emit()

    def find_routine_objects(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentTabǁfind_routine_objects__mutmut_orig'), object.__getattribute__(self, 'xǁFilamentTabǁfind_routine_objects__mutmut_mutants'), args, kwargs, self)

    def xǁFilamentTabǁfind_routine_objects__mutmut_orig(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_1(self):
        """Check if printer has load/unload printer objects"""
        if self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_2(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = None

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_3(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "XXload_filamentXX" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_4(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "LOAD_FILAMENT" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_5(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" not in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_6(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = None
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_7(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = False
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_8(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return False
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_9(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "XXunload_filamentXX" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_10(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "UNLOAD_FILAMENT" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_11(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" not in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_12(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = None
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_13(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = False
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_14(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return False
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_15(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "XXgcode_macro LOAD_FILAMENTXX" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_16(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro load_filament" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_17(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "GCODE_MACRO LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_18(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" not in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_19(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return False
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_20(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "XXgcode_macro UNLOAD_FILAMENTXX" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_21(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro unload_filament" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_22(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "GCODE_MACRO UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_23(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" not in _available_objects.keys():
            return True

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_24(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return False

        return False

    def xǁFilamentTabǁfind_routine_objects__mutmut_25(self):
        """Check if printer has load/unload printer objects"""
        if not self.printer:
            return

        _available_objects = self.printer.available_objects.copy()

        if "load_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "unload_filament" in _available_objects.keys():
            self.has_load_unload_objects = True
            return True
        if "gcode_macro LOAD_FILAMENT" in _available_objects.keys():
            return True
        if "gcode_macro UNLOAD_FILAMENT" in _available_objects.keys():
            return True

        return True
    
    xǁFilamentTabǁfind_routine_objects__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentTabǁfind_routine_objects__mutmut_1': xǁFilamentTabǁfind_routine_objects__mutmut_1, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_2': xǁFilamentTabǁfind_routine_objects__mutmut_2, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_3': xǁFilamentTabǁfind_routine_objects__mutmut_3, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_4': xǁFilamentTabǁfind_routine_objects__mutmut_4, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_5': xǁFilamentTabǁfind_routine_objects__mutmut_5, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_6': xǁFilamentTabǁfind_routine_objects__mutmut_6, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_7': xǁFilamentTabǁfind_routine_objects__mutmut_7, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_8': xǁFilamentTabǁfind_routine_objects__mutmut_8, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_9': xǁFilamentTabǁfind_routine_objects__mutmut_9, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_10': xǁFilamentTabǁfind_routine_objects__mutmut_10, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_11': xǁFilamentTabǁfind_routine_objects__mutmut_11, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_12': xǁFilamentTabǁfind_routine_objects__mutmut_12, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_13': xǁFilamentTabǁfind_routine_objects__mutmut_13, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_14': xǁFilamentTabǁfind_routine_objects__mutmut_14, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_15': xǁFilamentTabǁfind_routine_objects__mutmut_15, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_16': xǁFilamentTabǁfind_routine_objects__mutmut_16, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_17': xǁFilamentTabǁfind_routine_objects__mutmut_17, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_18': xǁFilamentTabǁfind_routine_objects__mutmut_18, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_19': xǁFilamentTabǁfind_routine_objects__mutmut_19, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_20': xǁFilamentTabǁfind_routine_objects__mutmut_20, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_21': xǁFilamentTabǁfind_routine_objects__mutmut_21, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_22': xǁFilamentTabǁfind_routine_objects__mutmut_22, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_23': xǁFilamentTabǁfind_routine_objects__mutmut_23, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_24': xǁFilamentTabǁfind_routine_objects__mutmut_24, 
        'xǁFilamentTabǁfind_routine_objects__mutmut_25': xǁFilamentTabǁfind_routine_objects__mutmut_25
    }
    xǁFilamentTabǁfind_routine_objects__mutmut_orig.__name__ = 'xǁFilamentTabǁfind_routine_objects'
