import sys
import subprocess
import logging
import typing
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

logging.basicConfig(
    filename="/home/bugo/logs/wifisep.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
_logger = logging.getLogger(__name__)


class MachineControl(QObject):

    service_restart = pyqtSignal(str, name="service-restart")

    def __init__(self, parent: typing.Optional["QObject"] = ...) -> None:
        super(MachineControl, self).__init__(parent)
        self.setObjectName("MachineControl")

    @pyqtSlot(name="machine_restart")
    def machine_restart(self):
        return self._run_command("sudo reboot now")

    @pyqtSlot(name="machine_shutdown")
    def machine_shutdown(self):
        return self._run_command("sudo shutdown now")

    @pyqtSlot(name="restart_klipper_service")
    def restart_klipper_service(self):
        # self.service_restart.emit("restart-klipper-service")
        return self._run_command("sudo systemctl stop klipper.service")

    @pyqtSlot(name="restart_moonraker_service")
    def restart_moonraker_service(self):
        # self.service_restart.emit("restart-moonraker-service")
        return self._run_command("sudo systemctl restart moonraker.service")

    def restart_bo_service(self):
        # TODO: REstart Blocks Screen srvice, implement it later on
        pass

    def check_service_state(self, service_name: str):
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
            # * Old way, it didn't let me use grep commands or use | on the command
            # cmd = shlex.split(command,posix=False)
            # exec = cmd[0]
            # exec_options = cmd[1:]
            # output = subprocess.run(
            #     ([exec] + exec_options), capture_output=True)
            p = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            output, e = p.communicate()
            return output
        except subprocess.SubprocessError:
            _logger.error("Error running commas : %s", command)
