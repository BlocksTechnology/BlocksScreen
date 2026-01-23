#
# System management
#
import logging
import shlex
import subprocess
import typing

from PyQt6 import QtCore


class SystemManager(QtCore.QObject):
    service_restart: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="service-restart"
    )

    def __init__(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()

    @QtCore.pyqtSlot(name="host-restart")
    def host_restart(self):
        """Reboot host controller"""
        return self._run_command("sudo reboot now")

    @QtCore.pyqtSlot(name="host-shutdown")
    def host_shutdown(self):
        """Shutdown host controller"""
        return self._run_command("sudo shutdown now")

    @QtCore.pyqtSlot(name="klipper-service-restart")
    def klipper_service_restart(self):
        """Restart klipper service"""
        return self._run_command("sudo systemctl restart klipper.service")

    @QtCore.pyqtSlot(name="moonraker-service-restart")
    def moonraker_service_restart(self):
        """Restart moonraker service"""
        return self._run_command("sudo systemctl restart moonraker.service")

    def check_service_state(self, service_name: str):
        """Check service status

        Args:
            service_name (str): service name

        Return:
            typing.Literal : The output of the command `systemctl is-active {service_name}`
        """

        if service_name:
            return "invalid"
        return self._run_command("systemctl is-active %s", service_name)

    def _command_helper(self, command: str) -> str:
        """Run shell command

        Args:
            str: Command to be executed

        Returns:
            str: Complete command output
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
            raise RuntimeError("Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logging.error(
                "Caught exception (exit code %d) failed to run command %s \n Stderr: %s",
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
            logging.error("Caught exception, failed to run command %s", command)
