#
# Machine manager
#
import logging
import subprocess  # nosec: B404
import typing

from PyQt6 import QtCore

logger = logging.getLogger(__name__)

_HOST_MCU_UNIT = "klipper-mcu.service"
# -n: no tty to prompt on; argvs must match install-updater.sh sudoers rules verbatim.
_SYSTEMCTL = ("sudo", "-n", "systemctl", "--no-block")


class MachineControl(QtCore.QObject):
    service_restart = QtCore.pyqtSignal(str, name="service-restart")

    def __init__(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super().__init__(parent)
        self.setObjectName("MachineControl")
        self._load_states: dict[str, bool] = {}

    @QtCore.pyqtSlot(name="machine_restart")
    def machine_restart(self) -> str | None:
        """Reboot machine"""
        return self._run_command(["sudo", "-n", "systemctl", "reboot"])

    @QtCore.pyqtSlot(name="machine_shutdown")
    def machine_shutdown(self) -> str | None:
        """Shutdown machine"""
        return self._run_command(["sudo", "-n", "systemctl", "poweroff"])

    @QtCore.pyqtSlot(name="restart_klipper_service")
    def restart_klipper_service(self) -> str | None:
        """Start the host MCU, then restart Klipper; both are queued, not awaited."""
        self.restart_klipper_mcu_service()
        return self._run_command([*_SYSTEMCTL, "restart", "klipper.service"])

    @QtCore.pyqtSlot(name="restart_klipper_mcu_service")
    def restart_klipper_mcu_service(self) -> str | None:
        """Start klipper-mcu if installed; a running instance is left untouched."""
        # Before=klipper.service orders this job ahead of a queued Klipper (re)start.
        if not self._unit_loaded(_HOST_MCU_UNIT):
            return None
        return self._run_command([*_SYSTEMCTL, "start", _HOST_MCU_UNIT])

    @QtCore.pyqtSlot(name="restart_moonraker_service")
    def restart_moonraker_service(self) -> str | None:
        """Restart moonraker service"""
        return self._run_command([*_SYSTEMCTL, "restart", "moonraker.service"])

    def _unit_loaded(self, unit: str) -> bool:
        """True if systemd knows ``unit``; printers without a host MCU lack it."""
        if unit not in self._load_states:
            out = self._run_command(
                ["systemctl", "show", "--property=LoadState", "--value", unit]
            )
            words = (out or "").split()
            if not words:
                return False  # Query failed: ask again next time
            self._load_states[unit] = words[0] == "loaded"
        return self._load_states[unit]

    def check_service_state(self, service_name: str | None):
        """Check service status

        Args:
            service_name (str): service name

        Returns:
            _type_: output of the command `systemctl is-active <service name>`
        """
        if service_name is None:
            return None
        return self._run_command(["systemctl", "is-active", service_name])

    def _run_command(self, command: list[str]) -> str | None:
        """Run a shell command and return its output, or None on failure."""
        # Callers are Qt slots: an escaping exception aborts the app
        try:
            p = subprocess.run(  # nosec: B603
                command, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except subprocess.CalledProcessError as e:
            logger.error(
                "Caught exception (exit code %d) failed to run command: %s \nStderr: %s",
                e.returncode,
                command,
                e.stderr.strip(),
            )
            return None
        except (
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            logger.error("Caught exception failed to run command %s", command)
            return None
