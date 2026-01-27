#
# System management
#
import logging
import os
import shlex
import subprocess
import typing

from PyQt6 import QtCore


class SystemManager(QtCore.QObject):
    service_restart: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="service-restart"
    )

    def __init__(self, parent: QtCore.QObject | None) -> None:
        if parent:
            super().__init__(parent)
        else:
            super().__init__()

    @QtCore.pyqtSlot(name="host-restart")
    def host_restart(self):
        """Reboot host controller"""
        return self._command_helper("reboot now")

    @QtCore.pyqtSlot(name="host-shutdown")
    def host_shutdown(self):
        """Shutdown host controller"""
        return self._command_helper("shutdown now")

    @QtCore.pyqtSlot(name="klipper-service-restart")  # ignore
    def klipper_service_restart(self):
        """Restart klipper service"""
        return self._command_helper("systemctl --user restart klipper.service")

    @QtCore.pyqtSlot(name="moonraker-service-restart")
    def moonraker_service_restart(self):
        """Restart moonraker service"""
        return self._command_helper("systemctl --user restart moonraker.service")

    def check_service_state(self, service_name: str):
        """Check service status
        Args:
            service_name (str): service name
        Return:
            typing.Literal : The output of the command `systemctl is-active`
        """

        if service_name:
            return "invalid"
        return self._command_helper(
            f"systemctl --user is-active {shlex.quote(service_name)}"
        )  # TODO: JUST PARSE THE CORRECT OUTPUT OF THE COMMAND

    def _command_helper(self, command: str) -> str:
        """Run shell command
        Args:
            str: Command execute
        Returns:
            str: Command output
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


class CommandHelper:
    def __init__(self) -> None:
        self.stdout: int = subprocess.PIPE
        self.stderr: int = subprocess.PIPE
        self.proc: subprocess.Popen[str] | None = None
        self.running = False
        self.returncode = None
        self.pid = None
        self.cwd = os.path.expanduser()

    def _restore(self) -> None:
        self.stdout = subprocess.PIPE
        self.stderr = subprocess.PIPE
        self.running = self.returncode = self.pid = None

    def __call__(self, args: str) -> None:
        try:
            self.proc: subprocess.Popen[str] = subprocess.Popen(
                args=shlex.split(args),
                stdout=self.stdout,
                stderr=self.stderr,
                shell=False,
                text=True,
                cwd=os.getcwd(),
            )
            with self.proc as p:
                self.running = True
                self.stdout, self.stderr = p.communicate(timeout=10)
                self.pid = p.pid
                self.returncode = p.returncode
                self.running = False
        except ValueError:
            logging.error("Command <command> failed malformed command call ")
        except subprocess.TimeoutExpired:
            self.proc.kill()
            logging.error("Command <command> failed: timeout")
            self.stdout, self.stderr = self.proc.communicate()
        except subprocess.SubprocessError as e:
            logging.error("Command <command> failed: %s ", e)
