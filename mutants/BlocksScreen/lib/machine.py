#
# Machine manager
#
import logging
import shlex
import subprocess  # nosec: B404
import typing

from PyQt6 import QtCore

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


class MachineControl(QtCore.QObject):
    service_restart = QtCore.pyqtSignal(str, name="service-restart")

    def __init__(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMachineControlǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁMachineControlǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁMachineControlǁ__init____mutmut_orig(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super(MachineControl, self).__init__(parent)
        self.setObjectName("MachineControl")

    def xǁMachineControlǁ__init____mutmut_1(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super(MachineControl, self).__init__(None)
        self.setObjectName("MachineControl")

    def xǁMachineControlǁ__init____mutmut_2(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super(None, self).__init__(parent)
        self.setObjectName("MachineControl")

    def xǁMachineControlǁ__init____mutmut_3(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super(MachineControl, None).__init__(parent)
        self.setObjectName("MachineControl")

    def xǁMachineControlǁ__init____mutmut_4(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super(self).__init__(parent)
        self.setObjectName("MachineControl")

    def xǁMachineControlǁ__init____mutmut_5(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super(MachineControl, ).__init__(parent)
        self.setObjectName("MachineControl")

    def xǁMachineControlǁ__init____mutmut_6(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super(MachineControl, self).__init__(parent)
        self.setObjectName(None)

    def xǁMachineControlǁ__init____mutmut_7(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super(MachineControl, self).__init__(parent)
        self.setObjectName("XXMachineControlXX")

    def xǁMachineControlǁ__init____mutmut_8(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super(MachineControl, self).__init__(parent)
        self.setObjectName("machinecontrol")

    def xǁMachineControlǁ__init____mutmut_9(self, parent: typing.Optional["QtCore.QObject"]) -> None:
        super(MachineControl, self).__init__(parent)
        self.setObjectName("MACHINECONTROL")
    
    xǁMachineControlǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMachineControlǁ__init____mutmut_1': xǁMachineControlǁ__init____mutmut_1, 
        'xǁMachineControlǁ__init____mutmut_2': xǁMachineControlǁ__init____mutmut_2, 
        'xǁMachineControlǁ__init____mutmut_3': xǁMachineControlǁ__init____mutmut_3, 
        'xǁMachineControlǁ__init____mutmut_4': xǁMachineControlǁ__init____mutmut_4, 
        'xǁMachineControlǁ__init____mutmut_5': xǁMachineControlǁ__init____mutmut_5, 
        'xǁMachineControlǁ__init____mutmut_6': xǁMachineControlǁ__init____mutmut_6, 
        'xǁMachineControlǁ__init____mutmut_7': xǁMachineControlǁ__init____mutmut_7, 
        'xǁMachineControlǁ__init____mutmut_8': xǁMachineControlǁ__init____mutmut_8, 
        'xǁMachineControlǁ__init____mutmut_9': xǁMachineControlǁ__init____mutmut_9
    }
    xǁMachineControlǁ__init____mutmut_orig.__name__ = 'xǁMachineControlǁ__init__'

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
        args = [service_name]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMachineControlǁcheck_service_state__mutmut_orig'), object.__getattribute__(self, 'xǁMachineControlǁcheck_service_state__mutmut_mutants'), args, kwargs, self)

    def xǁMachineControlǁcheck_service_state__mutmut_orig(self, service_name: str):
        """Check service status

        Args:
            service_name (str): service name

        Returns:
            _type_: output of the command `systemctl is-active <service name>`
        """
        if service_name is None:
            return None
        return self._run_command(f"systemctl is-active {service_name}")

    def xǁMachineControlǁcheck_service_state__mutmut_1(self, service_name: str):
        """Check service status

        Args:
            service_name (str): service name

        Returns:
            _type_: output of the command `systemctl is-active <service name>`
        """
        if service_name is not None:
            return None
        return self._run_command(f"systemctl is-active {service_name}")

    def xǁMachineControlǁcheck_service_state__mutmut_2(self, service_name: str):
        """Check service status

        Args:
            service_name (str): service name

        Returns:
            _type_: output of the command `systemctl is-active <service name>`
        """
        if service_name is None:
            return None
        return self._run_command(None)
    
    xǁMachineControlǁcheck_service_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMachineControlǁcheck_service_state__mutmut_1': xǁMachineControlǁcheck_service_state__mutmut_1, 
        'xǁMachineControlǁcheck_service_state__mutmut_2': xǁMachineControlǁcheck_service_state__mutmut_2
    }
    xǁMachineControlǁcheck_service_state__mutmut_orig.__name__ = 'xǁMachineControlǁcheck_service_state'

    def _run_command(self, command: str):
        args = [command]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMachineControlǁ_run_command__mutmut_orig'), object.__getattribute__(self, 'xǁMachineControlǁ_run_command__mutmut_mutants'), args, kwargs, self)

    def xǁMachineControlǁ_run_command__mutmut_orig(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_1(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = None
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_2(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(None)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_3(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = None
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_4(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                None, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_5(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=None, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_6(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=None, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_7(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=None, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_8(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=None
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_9(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_10(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_11(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_12(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_13(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_14(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=False, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_15(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=False, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_16(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=False, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_17(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=6
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_18(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" - p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_19(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() - "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_20(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "XX\nXX" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_21(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error(None, command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_22(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", None, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_23(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, None)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_24(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error(command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_25(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_26(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, )
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_27(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("XXFailed to parse command string '%s': '%s'XX", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_28(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_29(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("FAILED TO PARSE COMMAND STRING '%S': '%S'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_30(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(None) from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_31(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
                None,
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_32(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
                "Caught exception (exit code %d) failed to run command: %s \nStderr: %s",
                None,
                command,
                e.stderr.strip(),
            )
            raise
        except (
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_33(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
                "Caught exception (exit code %d) failed to run command: %s \nStderr: %s",
                e.returncode,
                None,
                e.stderr.strip(),
            )
            raise
        except (
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_34(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
                "Caught exception (exit code %d) failed to run command: %s \nStderr: %s",
                e.returncode,
                command,
                None,
            )
            raise
        except (
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_35(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_36(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
                "Caught exception (exit code %d) failed to run command: %s \nStderr: %s",
                command,
                e.stderr.strip(),
            )
            raise
        except (
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_37(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
                "Caught exception (exit code %d) failed to run command: %s \nStderr: %s",
                e.returncode,
                e.stderr.strip(),
            )
            raise
        except (
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_38(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
                "Caught exception (exit code %d) failed to run command: %s \nStderr: %s",
                e.returncode,
                command,
                )
            raise
        except (
            subprocess.SubprocessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_39(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
                "XXCaught exception (exit code %d) failed to run command: %s \nStderr: %sXX",
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_40(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
                "caught exception (exit code %d) failed to run command: %s \nstderr: %s",
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_41(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
                "CAUGHT EXCEPTION (EXIT CODE %D) FAILED TO RUN COMMAND: %S \nSTDERR: %S",
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
            logger.error("Caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_42(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error(None, command)

    def xǁMachineControlǁ_run_command__mutmut_43(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", None)

    def xǁMachineControlǁ_run_command__mutmut_44(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error(command)

    def xǁMachineControlǁ_run_command__mutmut_45(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("Caught exception failed to run command %s", )

    def xǁMachineControlǁ_run_command__mutmut_46(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("XXCaught exception failed to run command %sXX", command)

    def xǁMachineControlǁ_run_command__mutmut_47(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("caught exception failed to run command %s", command)

    def xǁMachineControlǁ_run_command__mutmut_48(self, command: str):
        """Runs a shell command.

        Args:
            command (type: string): The command to be executed .

        Returns:
            type: The complete output that resulted from the command.

        """
        try:
            # Split command into a list of strings
            cmd = shlex.split(command)
            p = subprocess.run(  # nosec: B603
                cmd, check=True, capture_output=True, text=True, timeout=5
            )
            return p.stdout.strip() + "\n" + p.stderr.strip()
        except ValueError as e:
            logger.error("Failed to parse command string '%s': '%s'", command, e)
            raise RuntimeError(f"Invalid command format: {e}") from e
        except subprocess.CalledProcessError as e:
            logger.error(
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
            logger.error("CAUGHT EXCEPTION FAILED TO RUN COMMAND %S", command)
    
    xǁMachineControlǁ_run_command__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMachineControlǁ_run_command__mutmut_1': xǁMachineControlǁ_run_command__mutmut_1, 
        'xǁMachineControlǁ_run_command__mutmut_2': xǁMachineControlǁ_run_command__mutmut_2, 
        'xǁMachineControlǁ_run_command__mutmut_3': xǁMachineControlǁ_run_command__mutmut_3, 
        'xǁMachineControlǁ_run_command__mutmut_4': xǁMachineControlǁ_run_command__mutmut_4, 
        'xǁMachineControlǁ_run_command__mutmut_5': xǁMachineControlǁ_run_command__mutmut_5, 
        'xǁMachineControlǁ_run_command__mutmut_6': xǁMachineControlǁ_run_command__mutmut_6, 
        'xǁMachineControlǁ_run_command__mutmut_7': xǁMachineControlǁ_run_command__mutmut_7, 
        'xǁMachineControlǁ_run_command__mutmut_8': xǁMachineControlǁ_run_command__mutmut_8, 
        'xǁMachineControlǁ_run_command__mutmut_9': xǁMachineControlǁ_run_command__mutmut_9, 
        'xǁMachineControlǁ_run_command__mutmut_10': xǁMachineControlǁ_run_command__mutmut_10, 
        'xǁMachineControlǁ_run_command__mutmut_11': xǁMachineControlǁ_run_command__mutmut_11, 
        'xǁMachineControlǁ_run_command__mutmut_12': xǁMachineControlǁ_run_command__mutmut_12, 
        'xǁMachineControlǁ_run_command__mutmut_13': xǁMachineControlǁ_run_command__mutmut_13, 
        'xǁMachineControlǁ_run_command__mutmut_14': xǁMachineControlǁ_run_command__mutmut_14, 
        'xǁMachineControlǁ_run_command__mutmut_15': xǁMachineControlǁ_run_command__mutmut_15, 
        'xǁMachineControlǁ_run_command__mutmut_16': xǁMachineControlǁ_run_command__mutmut_16, 
        'xǁMachineControlǁ_run_command__mutmut_17': xǁMachineControlǁ_run_command__mutmut_17, 
        'xǁMachineControlǁ_run_command__mutmut_18': xǁMachineControlǁ_run_command__mutmut_18, 
        'xǁMachineControlǁ_run_command__mutmut_19': xǁMachineControlǁ_run_command__mutmut_19, 
        'xǁMachineControlǁ_run_command__mutmut_20': xǁMachineControlǁ_run_command__mutmut_20, 
        'xǁMachineControlǁ_run_command__mutmut_21': xǁMachineControlǁ_run_command__mutmut_21, 
        'xǁMachineControlǁ_run_command__mutmut_22': xǁMachineControlǁ_run_command__mutmut_22, 
        'xǁMachineControlǁ_run_command__mutmut_23': xǁMachineControlǁ_run_command__mutmut_23, 
        'xǁMachineControlǁ_run_command__mutmut_24': xǁMachineControlǁ_run_command__mutmut_24, 
        'xǁMachineControlǁ_run_command__mutmut_25': xǁMachineControlǁ_run_command__mutmut_25, 
        'xǁMachineControlǁ_run_command__mutmut_26': xǁMachineControlǁ_run_command__mutmut_26, 
        'xǁMachineControlǁ_run_command__mutmut_27': xǁMachineControlǁ_run_command__mutmut_27, 
        'xǁMachineControlǁ_run_command__mutmut_28': xǁMachineControlǁ_run_command__mutmut_28, 
        'xǁMachineControlǁ_run_command__mutmut_29': xǁMachineControlǁ_run_command__mutmut_29, 
        'xǁMachineControlǁ_run_command__mutmut_30': xǁMachineControlǁ_run_command__mutmut_30, 
        'xǁMachineControlǁ_run_command__mutmut_31': xǁMachineControlǁ_run_command__mutmut_31, 
        'xǁMachineControlǁ_run_command__mutmut_32': xǁMachineControlǁ_run_command__mutmut_32, 
        'xǁMachineControlǁ_run_command__mutmut_33': xǁMachineControlǁ_run_command__mutmut_33, 
        'xǁMachineControlǁ_run_command__mutmut_34': xǁMachineControlǁ_run_command__mutmut_34, 
        'xǁMachineControlǁ_run_command__mutmut_35': xǁMachineControlǁ_run_command__mutmut_35, 
        'xǁMachineControlǁ_run_command__mutmut_36': xǁMachineControlǁ_run_command__mutmut_36, 
        'xǁMachineControlǁ_run_command__mutmut_37': xǁMachineControlǁ_run_command__mutmut_37, 
        'xǁMachineControlǁ_run_command__mutmut_38': xǁMachineControlǁ_run_command__mutmut_38, 
        'xǁMachineControlǁ_run_command__mutmut_39': xǁMachineControlǁ_run_command__mutmut_39, 
        'xǁMachineControlǁ_run_command__mutmut_40': xǁMachineControlǁ_run_command__mutmut_40, 
        'xǁMachineControlǁ_run_command__mutmut_41': xǁMachineControlǁ_run_command__mutmut_41, 
        'xǁMachineControlǁ_run_command__mutmut_42': xǁMachineControlǁ_run_command__mutmut_42, 
        'xǁMachineControlǁ_run_command__mutmut_43': xǁMachineControlǁ_run_command__mutmut_43, 
        'xǁMachineControlǁ_run_command__mutmut_44': xǁMachineControlǁ_run_command__mutmut_44, 
        'xǁMachineControlǁ_run_command__mutmut_45': xǁMachineControlǁ_run_command__mutmut_45, 
        'xǁMachineControlǁ_run_command__mutmut_46': xǁMachineControlǁ_run_command__mutmut_46, 
        'xǁMachineControlǁ_run_command__mutmut_47': xǁMachineControlǁ_run_command__mutmut_47, 
        'xǁMachineControlǁ_run_command__mutmut_48': xǁMachineControlǁ_run_command__mutmut_48
    }
    xǁMachineControlǁ_run_command__mutmut_orig.__name__ = 'xǁMachineControlǁ_run_command'
