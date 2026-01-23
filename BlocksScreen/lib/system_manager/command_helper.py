import shlex
import sys
import os
import typing
import platform


OS_TYPES = typing.Literal["windows", "unix", "mac"]


class CommandHelper:
    os_type: OS_TYPES

    def __init__(self) -> None:
        self.os_type: OS_TYPES = sys.platform

        print(self.os_type)

    # def get_os_type(self) -> OS_TYPE:
    #     """Get system type"""
    #     return sys.platform

    # def _run_command(self, command: str)


if __name__ == "__main__":
    cm = CommandHelper()
