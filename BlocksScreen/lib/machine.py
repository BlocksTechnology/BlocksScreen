#
# Machine manager
#
import logging
import shlex
import subprocess
import typing

from PyQt6 import QtCore


class MachineControl(QtCore.QObject):
    service_restart = QtCore.pyqtSignal(str, name="service-restart")

    def __init__(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super(MachineControl, self).__init__(parent)
        self.setObjectName("MachineControl")

    @QtCore.pyqtSlot(name="machine_restart")
    def machine_restart(self):
        """Reboot machine"""
        return self._run_command("sudo reboot now")

    @QtCore.pyqtSlot(name="machine_shutdown")
    def machine_shutdown(self):
        """Shutdown machine"""
        return self._run_command("sudo shutdown now")

    @QtCore.pyqtSlot(name="restart_klipper_service")
    def restart_klipper_service(self):
        """Restart klipper service"""
        return self._run_command("sudo systemctl stop klipper.service")

    @QtCore.pyqtSlot(name="restart_moonraker_service")
    def restart_moonraker_service(self):
        """Restart moonraker service"""
        return self._run_command("sudo systemctl restart moonraker.service")

    def check_service_state(self, service_name: str):
        """Check service status

        Args:
            service_name (str): service name

        Returns:
            _type_: output of the command `systemctl is-active <service name>`
        """
        if service_name is None:
            return None
        return self._run_command(f"systemctl is-active {service_name}")

    def _run_command(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logging.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logging.error(
                "Caught exception (exit code %d) failed to run command: %s \nStderr: %s",
                e.returncode,
                command,
                e.stderr.strip(),
            )
            raise
        except (
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            logging.error("Caught exception failed to run command %s", command)
