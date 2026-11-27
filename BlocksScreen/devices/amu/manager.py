"""Qt-side facade for the AMU: owns MMU state and issues Happy-Hare gcode."""

from __future__ import annotations

import json
import logging
import math
import shlex
import typing
from pathlib import Path

from PyQt6 import QtCore

from .config_toggler import ConfigToggler, ToggleResult
from .models import (
    FilamentPos,
    GateInfo,
    GateStatus,
    MMUState,
    SpoolmanSupport,
)

if typing.TYPE_CHECKING:
    from BlocksScreen.lib.moonrakerComm import MoonWebSocket


logger: logging.Logger = logging.getLogger(__name__)

CONFIG_PATH: Path = Path("~/printer_data/config/printer.cfg").expanduser()

# HH job detection never ends these (only complete/error); MMU_PRINT_END parks only on complete.
_STALE_JOB_STATES: tuple[str, ...] = ("cancelled", "standby")
_STALE_JOB_GRACE_MS: int = 5000
# Outlasts the gap between Klipper's restart and the updater linking mmu_server.
_MMU_SERVER_GRACE_MS: int = 300_000
_HH_COMPONENT: str = "Happy-Hare"
_MMU_SERVER_MISSING_MSG: str = (
    "Spool tracking is unavailable: Moonraker could not load the Happy Hare module.\n"
    "Filament usage is not being recorded.\n"
    "Contact Support: support@blockstec.com"
)
_WARNING_PRIORITY: int = 2


def _gcode_value(value: object) -> str:
    """Quote a value for Klipper's shlex-based extended gcode parser."""
    if isinstance(value, float):
        value = round(value)
    # A raw newline ends the gcode line; '%' crashes save_variables' configparser.
    text = " ".join(str(value).replace("%", "").split())
    return shlex.quote(text)


class AMUManager(QtCore.QObject):
    """Owns the MMU state and turns UI intents into guarded Happy-Hare gcode."""

    run_gcode_signal: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="run-gcode"
    )

    mmu_state_changed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        object, name="mmu-state-changed"
    )

    amu_toggled: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        bool, name="amu-toggled"
    )

    pre_gate_changed: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        int, bool, name="pre-gate-changed"
    )

    show_notification: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, str, int, bool, name="show-notification"
    )

    retract_notification: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="retract-notification"
    )

    def __init__(self, ws: MoonWebSocket, parent: QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._config_toggler = ConfigToggler(CONFIG_PATH)
        self._ws = ws
        self._mmu_state: MMUState | None = None
        self._pre_gate_sensors: dict[int, bool] = {}
        self._print_state = ""
        self._stale_job_timer = QtCore.QTimer(self)
        self._stale_job_timer.setSingleShot(True)
        self._stale_job_timer.setInterval(_STALE_JOB_GRACE_MS)
        self._stale_job_timer.timeout.connect(self._end_stale_mmu_job)
        self._moonraker_components: frozenset[str] | None = None
        self._mmu_server_warned = False
        self._updater_busy = False
        self._updater_provisioning = False
        self._hh_install_pending = False
        self._mmu_server_timer = QtCore.QTimer(self)
        self._mmu_server_timer.setSingleShot(True)
        self._mmu_server_timer.setInterval(_MMU_SERVER_GRACE_MS)
        self._mmu_server_timer.timeout.connect(self._warn_mmu_server_missing)

    def _gate_map(self, gate: int, **params: object) -> bool:
        """Emit MMU_GATE_MAP for one gate; False when no gate is selected yet."""
        if gate < 0:
            logger.warning("Ignoring gate command for unselected gate %d", gate)
            return False
        # TEMP=0 keeps the current temp; TEMP=None omits it, resetting to the default.
        params.setdefault("TEMP", 0)
        args = "".join(
            f" {key}={_gcode_value(value)}"
            for key, value in params.items()
            if value is not None
        )
        self.run_gcode_signal.emit(f"MMU_GATE_MAP GATE={gate}{args} QUIET=1")
        return True

    def toggle_amu_system(self, activate: bool) -> None:
        """Swap the printer.cfg variant, restarting on change; emits amu_toggled."""
        if self._print_state in ("printing", "paused"):
            logger.warning(
                "Ignoring AMU toggle while the print is %s", self._print_state
            )
            self.amu_toggled.emit(False)
            return
        result = self._config_toggler.toggle(activate)
        self.amu_toggled.emit(result is not ToggleResult.FAILED)
        if result is ToggleResult.CHANGED:
            # FIRMWARE_RESTART as gcode drops the socket and replies a false 503.
            self._ws.api.firmware_restart()

    def get_state(self) -> MMUState | None:
        """Return the latest MMU state, or None before the first status arrives."""
        return self._mmu_state

    def get_pre_gate_sensors(self) -> dict[int, bool]:
        """Return a copy of the per-gate pre-gate switch states, keyed by gate index."""
        return dict(self._pre_gate_sensors)

    def is_amu_configured(self) -> bool:
        """Return True if AMU includes are uncommented in printer.cfg."""
        return self._config_toggler.is_configured()

    def is_amu_active(self) -> bool:
        """Return True if the AMU is configured, reporting, and not MMU-disabled."""
        state = self._mmu_state
        return self.is_amu_configured() and state is not None and state.enabled

    def set_gate_info(
        self,
        gate: int,
        material: str,
        color: str,
        spool_id: int,
        filament_name: str = "",
        temperature: int | None = None,
    ) -> bool:
        """Overwrite all gate fields; '' clears one, None temp resets to HH default."""
        return self._gate_map(
            gate,
            NAME=filament_name,
            MATERIAL=material,
            COLOR=color.lstrip("#"),
            SPOOLID=spool_id,
            TEMP=temperature,
        )

    def clear_gate(self, gate: int) -> None:
        """Blank a gate's map entry the way Happy-Hare resets one."""
        self._gate_map(gate, NAME="", MATERIAL="", COLOR="", SPOOLID=-1, TEMP=None)

    def set_gate_material(self, gate: int, material: str) -> None:
        """Set the material of *gate*, keeping its temperature."""
        self._gate_map(gate, MATERIAL=material)

    def set_gate_temp(self, gate: int, temp: int) -> None:
        """Set *gate*'s temp; skips TEMP<=0 since Happy-Hare reads 0 as "keep"."""
        state = self._mmu_state
        if state is not None and state.spoolman_support is SpoolmanSupport.PULL:
            logger.warning("Ignoring gate %d temperature: Spoolman pull owns it", gate)
            return
        if not math.isfinite(temp) or round(temp) <= 0:
            logger.warning("Ignoring gate %d temperature %s: not positive", gate, temp)
            return
        self._gate_map(gate, TEMP=temp)

    def set_gate_color(self, gate: int, color: str) -> None:
        """Set the hex colour of *gate*, with or without a leading #."""
        self._gate_map(gate, COLOR=color.lstrip("#"))

    def set_gate_spool(self, gate: int, spool_id: int) -> None:
        """Bind *gate* to a Spoolman spool; -1 unbinds."""
        self._gate_map(gate, SPOOLID=spool_id)

    def assign_spool(self, gate: int, spool: dict) -> None:
        """Map *gate* from a Spoolman spool payload."""
        filament = spool.get("filament") or {}
        self.set_gate_info(
            gate,
            filament.get("material") or "",
            filament.get("color_hex") or "",
            spool.get("id", -1),
            filament_name=filament.get("name") or "",
            temperature=filament.get("settings_extruder_temp"),
        )

    def home_mmu(self) -> None:
        """Re-select the current tool via MMU_HOME; refused while filament is loaded."""
        state = self._mmu_state
        if state is None:
            logger.warning("Ignoring MMU_HOME: no MMU state yet")
            return
        # Bare MMU_HOME defaults to TOOL=0 with no loaded guard.
        if state.filament_pos not in (FilamentPos.UNLOADED, FilamentPos.UNKNOWN):
            logger.warning(
                "Ignoring MMU_HOME while filament is %s", state.filament_pos.name
            )
            return
        tool = state.tool
        self.run_gcode_signal.emit(f"MMU_HOME TOOL={tool}" if tool >= 0 else "MMU_HOME")

    def reset_mmu(self) -> None:
        """Erase all persisted MMU state (gate map, TTG map, statistics) and re-init."""
        self.run_gcode_signal.emit("MMU_RESET CONFIRM=1")

    @staticmethod
    def _busy_refusal(state: MMUState) -> str:
        """Return why the MMU cannot take a command now, or "" when it is idle."""
        # No print guard: HH v3 parks and restores the toolhead around these mid-print.
        if not state.enabled:
            return "MMU is disabled."
        if state.is_busy:
            return f"MMU is busy ({state.action})."
        return ""

    def check_refusal(self) -> str:
        """Return why the selected gate cannot be checked, or "" when it can."""
        state = self._mmu_state
        if state is None:
            return "MMU status not received yet."
        if reason := self._busy_refusal(state):
            return reason
        if not state.is_homed:
            return "MMU is not homed."
        if state.current_gate_info is None:
            return "No gate is selected."
        return ""

    def load_refusal(self) -> str:
        """Return why the selected gate cannot load, or "" when it is idle-ready."""
        reason = self.check_refusal()
        state = self._mmu_state
        if reason or state is None:
            return reason
        if state.filament_pos != FilamentPos.UNLOADED:
            return "Filament is not fully unloaded."
        return ""

    def unload_refusal(self) -> str:
        """Return why the filament cannot be unloaded, or "" when it can."""
        state = self._mmu_state
        if state is None:
            return "MMU status not received yet."
        if reason := self._busy_refusal(state):
            return reason
        if state.filament_pos == FilamentPos.UNLOADED:
            return "Filament is already unloaded."
        return ""

    def print_start_refusal(self) -> str:
        """Return why RF50-Klipper SDCARD_PRINT_FILE would refuse to start, or ""."""
        sensors = self._mmu_state.sensors if self._mmu_state is not None else {}
        # The macro tests `== False`: a missing or disabled (None) sensor passes.
        if sensors.get("mmu_pre_gate") is False:
            return "No filament in the selected gate. Load filament before printing."
        if sensors.get("mmu_gate") is False:
            return (
                "Filament is not loaded past the gate. Load filament before printing."
            )
        if sensors.get("toolhead") is False:
            return "No filament at the toolhead. Load filament before printing."
        return ""

    def _selected_gate_unloaded(self) -> GateInfo | None:
        """Return the selected gate when the MMU is idle-ready: enabled, homed, unloaded."""
        if self._mmu_state is None or self.load_refusal():
            return None
        return self._mmu_state.current_gate_info

    def load_gate(self) -> bool:
        """Load filament from the selected gate by sending MMU_LOAD; True if sent."""
        if reason := self.load_refusal():
            logger.warning("Ignoring MMU_LOAD: %s", reason)
            return False
        self.run_gcode_signal.emit("MMU_LOAD")
        return True

    def unload(self, eject: bool = False) -> bool:
        """Unload via MMU_UNLOAD, or MMU_EJECT when *eject*; True if sent."""
        if reason := self.unload_refusal():
            logger.warning("Ignoring unload: %s", reason)
            return False
        self.run_gcode_signal.emit("MMU_EJECT" if eject else "MMU_UNLOAD")
        return True

    def select_gate(self, gate: int) -> None:
        """Send MMU_SELECT unless invalid, already selected, or filament is loaded."""
        state = self._mmu_state
        if (
            state is None
            or not (state.enabled and state.is_homed)
            or state.is_busy
            or not 0 <= gate < state.num_gates
            or gate == state.gate
        ):
            return
        if state.filament_pos != FilamentPos.UNLOADED:
            logger.warning(
                "Ignoring MMU_SELECT while filament is %s", state.filament_pos.name
            )
            return
        self.run_gcode_signal.emit(f"MMU_SELECT GATE={gate}")

    def eject_gate(self) -> None:
        """Fully eject filament from the selected gate, the only gate that can eject."""
        if self._mmu_state is not None and self._mmu_state.is_printing:
            logger.warning("Ignoring MMU_EJECT: not available while printing")
            return
        gate = self._selected_gate_unloaded()
        if gate is None or gate.status == GateStatus.EMPTY:
            logger.warning("Ignoring MMU_EJECT: no unloaded, non-empty gate selected")
            return
        self.run_gcode_signal.emit("MMU_EJECT")

    def check_gate(self) -> None:
        """Check the selected gate for filament by sending MMU_CHECK_GATE."""
        # Happy-Hare v3 unloads first when not UNLOADED and reloads a LOADED tool after.
        if reason := self.check_refusal():
            logger.warning("Ignoring MMU_CHECK_GATE: %s", reason)
            return
        self.run_gcode_signal.emit("MMU_CHECK_GATE")

    def recover_single_gate(self, loaded: bool) -> None:
        """Tell Happy-Hare whether the single-gate filament path is loaded."""
        self.run_gcode_signal.emit(f"MMU_RECOVER GATE=0 LOADED={int(loaded)}")

    def change_tool(self, tool: int) -> None:
        """Select *tool* with MMU_CHANGE_TOOL, swapping filament if needed."""
        self.run_gcode_signal.emit(f"MMU_CHANGE_TOOL TOOL={tool}")

    def update_mmu_state(self, data: dict) -> None:
        """Build state from a full status or apply a diff; emit mmu_state_changed."""
        if self._mmu_state is None:
            if "num_gates" not in data:
                return
            self._mmu_state = MMUState.from_status(data)
        else:
            state = self._mmu_state.apply_diff(data)
            if state == self._mmu_state:
                return
            self._mmu_state = state
        self.mmu_state_changed.emit(self._mmu_state)
        self._check_stale_mmu_job()
        self._check_mmu_server()

    def on_object_updated(
        self, object_type: str, object_name: str, values: dict
    ) -> None:
        """Route object_updated signal from Printer to the appropriate handler."""
        if object_type == "mmu":
            self.update_mmu_state(values)
        elif object_type == "filament_switch_sensor":
            self.on_pre_gate_update(values, object_name)
        elif object_type == "print_stats" and "state" in values:
            self._print_state = values["state"]
            self._check_stale_mmu_job()

    def _is_stale_mmu_job(self) -> bool:
        """Return True while Happy-Hare runs a job print_stats has already left."""
        state = self._mmu_state
        return (
            state is not None
            and state.is_printing
            and self._print_state in _STALE_JOB_STATES
        )

    def _check_stale_mmu_job(self) -> None:
        """Arm the grace timer on a job desync, disarm it once the states agree."""
        if not self._is_stale_mmu_job():
            self._stale_job_timer.stop()
        elif not self._stale_job_timer.isActive():
            self._stale_job_timer.start()

    def _end_stale_mmu_job(self) -> None:
        """End the job HH's deferred MMU_PRINT_START re-opens after a fast cancel."""
        if self._is_stale_mmu_job():
            logger.warning(
                "Ending HH job left open by print_stats %s", self._print_state
            )
            self.run_gcode_signal.emit(f"MMU_PRINT_END STATE={self._print_state}")

    @QtCore.pyqtSlot(list, name="on-server-components")
    def on_server_components(self, components: list) -> None:
        """Track Moonraker's loaded components for the mmu_server check."""
        self._moonraker_components = frozenset(components)
        self._check_mmu_server()

    def _is_mmu_server_missing(self) -> bool:
        """Return True when Happy Hare uses Spoolman but Moonraker lacks mmu_server."""
        state = self._mmu_state
        return (
            state is not None
            and state.spoolman_support is not SpoolmanSupport.OFF
            and self._moonraker_components is not None
            and "mmu_server" not in self._moonraker_components
        )

    @QtCore.pyqtSlot(bool, name="on-updater-busy")
    def on_updater_busy(self, busy: bool) -> None:
        """Hold the mmu_server warning while the updater runs a batch."""
        self._updater_busy = busy
        self._check_mmu_server()

    @QtCore.pyqtSlot(bool, name="on-updater-provisioning")
    def on_updater_provisioning(self, provisioning: bool) -> None:
        """Hold the mmu_server warning while the updater installs missing components."""
        self._updater_provisioning = provisioning
        self._check_mmu_server()

    @QtCore.pyqtSlot(name="on-updater-unavailable")
    def on_updater_unavailable(self) -> None:
        """Drop every updater hold when the daemon is gone; reconnect re-sends its state."""
        self._updater_busy = False
        self._updater_provisioning = False
        self._hh_install_pending = False
        self._check_mmu_server()

    @QtCore.pyqtSlot(str, name="on-updater-status")
    def on_updater_status(self, json_str: str) -> None:
        """Hold the mmu_server warning while the updater still has Happy Hare to install."""
        try:
            hh = json.loads(json_str).get(_HH_COMPONENT) or {}
            self._hh_install_pending = bool(hh.get("needs_install"))
        except (json.JSONDecodeError, TypeError, AttributeError):
            logger.debug("Ignoring malformed updater status for the mmu_server check")
            return
        self._check_mmu_server()

    def _updater_owns_hh(self) -> bool:
        """Return True while the updater may still be linking mmu_server."""
        return (
            self._updater_busy or self._updater_provisioning or self._hh_install_pending
        )

    def _check_mmu_server(self) -> None:
        """Arm the mmu_server warning, holding it during updates; retract it on load."""
        if self._is_mmu_server_missing():
            if self._updater_owns_hh():
                # Re-armed with a full grace once the updater is done.
                self._mmu_server_timer.stop()
            elif not (self._mmu_server_warned or self._mmu_server_timer.isActive()):
                self._mmu_server_timer.start()
            return
        self._mmu_server_timer.stop()
        if self._moonraker_components and "mmu_server" in self._moonraker_components:
            if self._mmu_server_warned:
                self.retract_notification.emit(_MMU_SERVER_MISSING_MSG)
            self._mmu_server_warned = False

    def _warn_mmu_server_missing(self) -> None:
        """Warn once that Happy Hare's Spoolman calls fail without mmu_server."""
        if not self._is_mmu_server_missing() or self._updater_owns_hh():
            return
        self._mmu_server_warned = True
        logger.warning(
            "Moonraker has no mmu_server component; Happy Hare Spoolman calls fail"
        )
        self.show_notification.emit(
            "amu", _MMU_SERVER_MISSING_MSG, _WARNING_PRIORITY, True
        )

    def on_pre_gate_update(self, values: dict, name: str) -> None:
        """Track one pre-gate switch; the mmu aggregate hides unselected gates."""
        if not name.startswith("mmu_pre_gate_"):
            return
        try:
            gate = int(name.removeprefix("mmu_pre_gate_"))
        except ValueError:
            logger.error("Failed to parse Pre-Gate: %s", name)
            return
        # Enabled-only diffs omit it; reading False would invent empty gates.
        if "filament_detected" not in values:
            return
        detected = bool(values["filament_detected"])
        self._pre_gate_sensors[gate] = detected
        self.pre_gate_changed.emit(gate, detected)

    @QtCore.pyqtSlot(str)
    def on_klippy_state(self, state: str) -> None:
        """Drop cached MMU state when klippy leaves ready and tell the UI it is gone."""
        if state.lower() == "ready":
            return
        self._pre_gate_sensors = {}
        if self._mmu_state is None:
            return
        self._mmu_state = None
        self.mmu_state_changed.emit(None)
        self._mmu_server_timer.stop()
