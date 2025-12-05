#
# Machine manager
#
import logging
import subprocess
import typing

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class MachineControl(QObject):
    service_restart = pyqtSignal(str, name="service-restart")

    def __init__(self, parent: typing.Optional["QObject"]) -> None:
        super(MachineControl, self).__init__(parent)
        self.setObjectName("MachineControl")

    @pyqtSlot(name="machine_restart")
    def machine_restart(self):
        """Reboot machine"""
        return self._run_command("sudo reboot now")

    @pyqtSlot(name="machine_shutdown")
    def machine_shutdown(self):
        """Shutdown machine"""
        return self._run_command("sudo shutdown now")

    @pyqtSlot(name="restart_klipper_service")
    def restart_klipper_service(self):
        """Restart klipper service"""
        return self._run_command("sudo systemctl stop klipper.service")

    @pyqtSlot(name="restart_moonraker_service")
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

    def _run_command(self, command):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            p = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            output, _ = p.communicate()
            return output
        except subprocess.SubprocessError:
            logging.error("Error running commas : %s", command)
