# Config file helper
#
# Copyright (C) 2020 Eric Callahan <arksine.code@gmail.com>
# Copyright (C) 2025 Hugo Costa <h.costa@blockstec.com>
#
# Based on the work of Eric Callahan:
# https://github.com/Arksine/moonraker/blob/master/moonraker/confighelper.py
#
# This file is part of BlocksScreen.
#
# BlocksScreen is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlocksScreen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BlocksScreen. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import annotations

import configparser
import enum
import io
import logging
import os
import pathlib
import re
import threading
import typing

from helper_methods import check_file_on_path

logger = logging.getLogger(__name__)

HOME_DIR = os.path.expanduser("~/")
WORKING_DIR = os.getcwd()
DEFAULT_CONFIGFILE_PATH = pathlib.Path(HOME_DIR, "printer_data", "config")
FALLBACK_CONFIGFILE_PATH = pathlib.Path(WORKING_DIR)

T = typing.TypeVar("T")
indentation_size = 4
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


class Sentinel(enum.Enum):
    """Sentinel value to signify missing condition, absence of value"""

    MISSING = object


class ConfigError(Exception):
    """Exception raised when Configfile errors exist"""

    def __init__(self, msg) -> None:
        args = [msg]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁConfigErrorǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁConfigErrorǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁConfigErrorǁ__init____mutmut_orig(self, msg) -> None:
        """Store the error message on both the exception and the ``msg`` attribute."""
        super().__init__(msg)
        self.msg = msg

    def xǁConfigErrorǁ__init____mutmut_1(self, msg) -> None:
        """Store the error message on both the exception and the ``msg`` attribute."""
        super().__init__(None)
        self.msg = msg

    def xǁConfigErrorǁ__init____mutmut_2(self, msg) -> None:
        """Store the error message on both the exception and the ``msg`` attribute."""
        super().__init__(msg)
        self.msg = None
    
    xǁConfigErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁConfigErrorǁ__init____mutmut_1': xǁConfigErrorǁ__init____mutmut_1, 
        'xǁConfigErrorǁ__init____mutmut_2': xǁConfigErrorǁ__init____mutmut_2
    }
    xǁConfigErrorǁ__init____mutmut_orig.__name__ = 'xǁConfigErrorǁ__init__'


class BlocksScreenConfig:
    """Thread-safe wrapper around :class:`configparser.ConfigParser` with raw-text tracking.

    Maintains a ``raw_config`` list that mirrors the on-disk file so that
    ``add_section``, ``add_option``, and ``update_option`` can write back
    changes without losing comments or formatting.
    """

    config = configparser.ConfigParser(
        allow_no_value=True,
    )
    update_pending: bool = False
    _instance = None

    def __init__(
        self, configfile: typing.Union[str, pathlib.Path], section: str
    ) -> None:
        args = [configfile, section]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁ__init____mutmut_orig(
        self, configfile: typing.Union[str, pathlib.Path], section: str
    ) -> None:
        """Initialise with the path to the config file and the default section name."""
        self.configfile = pathlib.Path(configfile)
        self.section = section
        self.raw_config: typing.List[str] = []
        self.raw_dict_config: typing.Dict = {}
        self.file_lock = threading.Lock()  # Thread safety for future work

    def xǁBlocksScreenConfigǁ__init____mutmut_1(
        self, configfile: typing.Union[str, pathlib.Path], section: str
    ) -> None:
        """Initialise with the path to the config file and the default section name."""
        self.configfile = None
        self.section = section
        self.raw_config: typing.List[str] = []
        self.raw_dict_config: typing.Dict = {}
        self.file_lock = threading.Lock()  # Thread safety for future work

    def xǁBlocksScreenConfigǁ__init____mutmut_2(
        self, configfile: typing.Union[str, pathlib.Path], section: str
    ) -> None:
        """Initialise with the path to the config file and the default section name."""
        self.configfile = pathlib.Path(None)
        self.section = section
        self.raw_config: typing.List[str] = []
        self.raw_dict_config: typing.Dict = {}
        self.file_lock = threading.Lock()  # Thread safety for future work

    def xǁBlocksScreenConfigǁ__init____mutmut_3(
        self, configfile: typing.Union[str, pathlib.Path], section: str
    ) -> None:
        """Initialise with the path to the config file and the default section name."""
        self.configfile = pathlib.Path(configfile)
        self.section = None
        self.raw_config: typing.List[str] = []
        self.raw_dict_config: typing.Dict = {}
        self.file_lock = threading.Lock()  # Thread safety for future work

    def xǁBlocksScreenConfigǁ__init____mutmut_4(
        self, configfile: typing.Union[str, pathlib.Path], section: str
    ) -> None:
        """Initialise with the path to the config file and the default section name."""
        self.configfile = pathlib.Path(configfile)
        self.section = section
        self.raw_config: typing.List[str] = None
        self.raw_dict_config: typing.Dict = {}
        self.file_lock = threading.Lock()  # Thread safety for future work

    def xǁBlocksScreenConfigǁ__init____mutmut_5(
        self, configfile: typing.Union[str, pathlib.Path], section: str
    ) -> None:
        """Initialise with the path to the config file and the default section name."""
        self.configfile = pathlib.Path(configfile)
        self.section = section
        self.raw_config: typing.List[str] = []
        self.raw_dict_config: typing.Dict = None
        self.file_lock = threading.Lock()  # Thread safety for future work

    def xǁBlocksScreenConfigǁ__init____mutmut_6(
        self, configfile: typing.Union[str, pathlib.Path], section: str
    ) -> None:
        """Initialise with the path to the config file and the default section name."""
        self.configfile = pathlib.Path(configfile)
        self.section = section
        self.raw_config: typing.List[str] = []
        self.raw_dict_config: typing.Dict = {}
        self.file_lock = None  # Thread safety for future work
    
    xǁBlocksScreenConfigǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁ__init____mutmut_1': xǁBlocksScreenConfigǁ__init____mutmut_1, 
        'xǁBlocksScreenConfigǁ__init____mutmut_2': xǁBlocksScreenConfigǁ__init____mutmut_2, 
        'xǁBlocksScreenConfigǁ__init____mutmut_3': xǁBlocksScreenConfigǁ__init____mutmut_3, 
        'xǁBlocksScreenConfigǁ__init____mutmut_4': xǁBlocksScreenConfigǁ__init____mutmut_4, 
        'xǁBlocksScreenConfigǁ__init____mutmut_5': xǁBlocksScreenConfigǁ__init____mutmut_5, 
        'xǁBlocksScreenConfigǁ__init____mutmut_6': xǁBlocksScreenConfigǁ__init____mutmut_6
    }
    xǁBlocksScreenConfigǁ__init____mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁ__init__'

    def __getitem__(self, key: str) -> BlocksScreenConfig:
        args = [key]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁ__getitem____mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁ__getitem____mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁ__getitem____mutmut_orig(self, key: str) -> BlocksScreenConfig:
        """Return a :class:`BlocksScreenConfig` for *key* section (same as ``get_section``)."""
        return self.get_section(key)

    def xǁBlocksScreenConfigǁ__getitem____mutmut_1(self, key: str) -> BlocksScreenConfig:
        """Return a :class:`BlocksScreenConfig` for *key* section (same as ``get_section``)."""
        return self.get_section(None)
    
    xǁBlocksScreenConfigǁ__getitem____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁ__getitem____mutmut_1': xǁBlocksScreenConfigǁ__getitem____mutmut_1
    }
    xǁBlocksScreenConfigǁ__getitem____mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁ__getitem__'

    def __contains__(self, key):
        args = [key]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁ__contains____mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁ__contains____mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁ__contains____mutmut_orig(self, key):
        """Return True if *key* is a section in the underlying ConfigParser."""
        return key in self.config

    def xǁBlocksScreenConfigǁ__contains____mutmut_1(self, key):
        """Return True if *key* is a section in the underlying ConfigParser."""
        return key not in self.config
    
    xǁBlocksScreenConfigǁ__contains____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁ__contains____mutmut_1': xǁBlocksScreenConfigǁ__contains____mutmut_1
    }
    xǁBlocksScreenConfigǁ__contains____mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁ__contains__'

    def sections(self) -> typing.List[str]:
        """Returns list of all sections"""
        return self.config.sections()

    def get_section(
        self, section: str, fallback: typing.Optional[T] = None
    ) -> BlocksScreenConfig:
        args = [section, fallback]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁget_section__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁget_section__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁget_section__mutmut_orig(
        self, section: str, fallback: typing.Optional[T] = None
    ) -> BlocksScreenConfig:
        """Get configfile section"""
        if not self.config.has_section(section):
            return fallback
        return BlocksScreenConfig(self.configfile, section)

    def xǁBlocksScreenConfigǁget_section__mutmut_1(
        self, section: str, fallback: typing.Optional[T] = None
    ) -> BlocksScreenConfig:
        """Get configfile section"""
        if self.config.has_section(section):
            return fallback
        return BlocksScreenConfig(self.configfile, section)

    def xǁBlocksScreenConfigǁget_section__mutmut_2(
        self, section: str, fallback: typing.Optional[T] = None
    ) -> BlocksScreenConfig:
        """Get configfile section"""
        if not self.config.has_section(None):
            return fallback
        return BlocksScreenConfig(self.configfile, section)

    def xǁBlocksScreenConfigǁget_section__mutmut_3(
        self, section: str, fallback: typing.Optional[T] = None
    ) -> BlocksScreenConfig:
        """Get configfile section"""
        if not self.config.has_section(section):
            return fallback
        return BlocksScreenConfig(None, section)

    def xǁBlocksScreenConfigǁget_section__mutmut_4(
        self, section: str, fallback: typing.Optional[T] = None
    ) -> BlocksScreenConfig:
        """Get configfile section"""
        if not self.config.has_section(section):
            return fallback
        return BlocksScreenConfig(self.configfile, None)

    def xǁBlocksScreenConfigǁget_section__mutmut_5(
        self, section: str, fallback: typing.Optional[T] = None
    ) -> BlocksScreenConfig:
        """Get configfile section"""
        if not self.config.has_section(section):
            return fallback
        return BlocksScreenConfig(section)

    def xǁBlocksScreenConfigǁget_section__mutmut_6(
        self, section: str, fallback: typing.Optional[T] = None
    ) -> BlocksScreenConfig:
        """Get configfile section"""
        if not self.config.has_section(section):
            return fallback
        return BlocksScreenConfig(self.configfile, )
    
    xǁBlocksScreenConfigǁget_section__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁget_section__mutmut_1': xǁBlocksScreenConfigǁget_section__mutmut_1, 
        'xǁBlocksScreenConfigǁget_section__mutmut_2': xǁBlocksScreenConfigǁget_section__mutmut_2, 
        'xǁBlocksScreenConfigǁget_section__mutmut_3': xǁBlocksScreenConfigǁget_section__mutmut_3, 
        'xǁBlocksScreenConfigǁget_section__mutmut_4': xǁBlocksScreenConfigǁget_section__mutmut_4, 
        'xǁBlocksScreenConfigǁget_section__mutmut_5': xǁBlocksScreenConfigǁget_section__mutmut_5, 
        'xǁBlocksScreenConfigǁget_section__mutmut_6': xǁBlocksScreenConfigǁget_section__mutmut_6
    }
    xǁBlocksScreenConfigǁget_section__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁget_section'

    def get_options(self) -> list:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁget_options__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁget_options__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁget_options__mutmut_orig(self) -> list:
        """Get section options"""
        return self.config.options(self.section)

    def xǁBlocksScreenConfigǁget_options__mutmut_1(self) -> list:
        """Get section options"""
        return self.config.options(None)
    
    xǁBlocksScreenConfigǁget_options__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁget_options__mutmut_1': xǁBlocksScreenConfigǁget_options__mutmut_1
    }
    xǁBlocksScreenConfigǁget_options__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁget_options'

    def has_section(self, section: str) -> bool:
        args = [section]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁhas_section__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁhas_section__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁhas_section__mutmut_orig(self, section: str) -> bool:
        """Check if config file has a section

        Args:
            section (str): section name

        Returns:
            bool: true if section exists, false otherwise
        """
        return bool(self.config.has_section(section))

    def xǁBlocksScreenConfigǁhas_section__mutmut_1(self, section: str) -> bool:
        """Check if config file has a section

        Args:
            section (str): section name

        Returns:
            bool: true if section exists, false otherwise
        """
        return bool(None)

    def xǁBlocksScreenConfigǁhas_section__mutmut_2(self, section: str) -> bool:
        """Check if config file has a section

        Args:
            section (str): section name

        Returns:
            bool: true if section exists, false otherwise
        """
        return bool(self.config.has_section(None))
    
    xǁBlocksScreenConfigǁhas_section__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁhas_section__mutmut_1': xǁBlocksScreenConfigǁhas_section__mutmut_1, 
        'xǁBlocksScreenConfigǁhas_section__mutmut_2': xǁBlocksScreenConfigǁhas_section__mutmut_2
    }
    xǁBlocksScreenConfigǁhas_section__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁhas_section'

    def has_option(self, option: str) -> bool:
        args = [option]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁhas_option__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁhas_option__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁhas_option__mutmut_orig(self, option: str) -> bool:
        """Check if section has a option

        Args:
            option (str): option name

        Returns:
            bool: true if section exists, false otherwise
        """
        return bool(self.config.has_option(self.section, option))

    def xǁBlocksScreenConfigǁhas_option__mutmut_1(self, option: str) -> bool:
        """Check if section has a option

        Args:
            option (str): option name

        Returns:
            bool: true if section exists, false otherwise
        """
        return bool(None)

    def xǁBlocksScreenConfigǁhas_option__mutmut_2(self, option: str) -> bool:
        """Check if section has a option

        Args:
            option (str): option name

        Returns:
            bool: true if section exists, false otherwise
        """
        return bool(self.config.has_option(None, option))

    def xǁBlocksScreenConfigǁhas_option__mutmut_3(self, option: str) -> bool:
        """Check if section has a option

        Args:
            option (str): option name

        Returns:
            bool: true if section exists, false otherwise
        """
        return bool(self.config.has_option(self.section, None))

    def xǁBlocksScreenConfigǁhas_option__mutmut_4(self, option: str) -> bool:
        """Check if section has a option

        Args:
            option (str): option name

        Returns:
            bool: true if section exists, false otherwise
        """
        return bool(self.config.has_option(option))

    def xǁBlocksScreenConfigǁhas_option__mutmut_5(self, option: str) -> bool:
        """Check if section has a option

        Args:
            option (str): option name

        Returns:
            bool: true if section exists, false otherwise
        """
        return bool(self.config.has_option(self.section, ))
    
    xǁBlocksScreenConfigǁhas_option__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁhas_option__mutmut_1': xǁBlocksScreenConfigǁhas_option__mutmut_1, 
        'xǁBlocksScreenConfigǁhas_option__mutmut_2': xǁBlocksScreenConfigǁhas_option__mutmut_2, 
        'xǁBlocksScreenConfigǁhas_option__mutmut_3': xǁBlocksScreenConfigǁhas_option__mutmut_3, 
        'xǁBlocksScreenConfigǁhas_option__mutmut_4': xǁBlocksScreenConfigǁhas_option__mutmut_4, 
        'xǁBlocksScreenConfigǁhas_option__mutmut_5': xǁBlocksScreenConfigǁhas_option__mutmut_5
    }
    xǁBlocksScreenConfigǁhas_option__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁhas_option'

    def get(
        self,
        option: str,
        parser: type = str,
        default: typing.Union[Sentinel, str, T] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, str]:
        args = [option, parser, default]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁget__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁget__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁget__mutmut_orig(
        self,
        option: str,
        parser: type = str,
        default: typing.Union[Sentinel, str, T] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, str]:
        """Get option value

        Args:
            option (str): option name
            parser (type, optional): bool, float, int. Defaults to str.
            default (typing.Union[Sentinel, str, T], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, str]: Requested option. Defaults to the specified default value
        """
        return parser(
            self.config.get(section=self.section, option=option, fallback=default)
        )

    def xǁBlocksScreenConfigǁget__mutmut_1(
        self,
        option: str,
        parser: type = str,
        default: typing.Union[Sentinel, str, T] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, str]:
        """Get option value

        Args:
            option (str): option name
            parser (type, optional): bool, float, int. Defaults to str.
            default (typing.Union[Sentinel, str, T], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, str]: Requested option. Defaults to the specified default value
        """
        return parser(
            None
        )

    def xǁBlocksScreenConfigǁget__mutmut_2(
        self,
        option: str,
        parser: type = str,
        default: typing.Union[Sentinel, str, T] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, str]:
        """Get option value

        Args:
            option (str): option name
            parser (type, optional): bool, float, int. Defaults to str.
            default (typing.Union[Sentinel, str, T], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, str]: Requested option. Defaults to the specified default value
        """
        return parser(
            self.config.get(section=None, option=option, fallback=default)
        )

    def xǁBlocksScreenConfigǁget__mutmut_3(
        self,
        option: str,
        parser: type = str,
        default: typing.Union[Sentinel, str, T] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, str]:
        """Get option value

        Args:
            option (str): option name
            parser (type, optional): bool, float, int. Defaults to str.
            default (typing.Union[Sentinel, str, T], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, str]: Requested option. Defaults to the specified default value
        """
        return parser(
            self.config.get(section=self.section, option=None, fallback=default)
        )

    def xǁBlocksScreenConfigǁget__mutmut_4(
        self,
        option: str,
        parser: type = str,
        default: typing.Union[Sentinel, str, T] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, str]:
        """Get option value

        Args:
            option (str): option name
            parser (type, optional): bool, float, int. Defaults to str.
            default (typing.Union[Sentinel, str, T], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, str]: Requested option. Defaults to the specified default value
        """
        return parser(
            self.config.get(section=self.section, option=option, fallback=None)
        )

    def xǁBlocksScreenConfigǁget__mutmut_5(
        self,
        option: str,
        parser: type = str,
        default: typing.Union[Sentinel, str, T] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, str]:
        """Get option value

        Args:
            option (str): option name
            parser (type, optional): bool, float, int. Defaults to str.
            default (typing.Union[Sentinel, str, T], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, str]: Requested option. Defaults to the specified default value
        """
        return parser(
            self.config.get(option=option, fallback=default)
        )

    def xǁBlocksScreenConfigǁget__mutmut_6(
        self,
        option: str,
        parser: type = str,
        default: typing.Union[Sentinel, str, T] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, str]:
        """Get option value

        Args:
            option (str): option name
            parser (type, optional): bool, float, int. Defaults to str.
            default (typing.Union[Sentinel, str, T], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, str]: Requested option. Defaults to the specified default value
        """
        return parser(
            self.config.get(section=self.section, fallback=default)
        )

    def xǁBlocksScreenConfigǁget__mutmut_7(
        self,
        option: str,
        parser: type = str,
        default: typing.Union[Sentinel, str, T] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, str]:
        """Get option value

        Args:
            option (str): option name
            parser (type, optional): bool, float, int. Defaults to str.
            default (typing.Union[Sentinel, str, T], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, str]: Requested option. Defaults to the specified default value
        """
        return parser(
            self.config.get(section=self.section, option=option, )
        )
    
    xǁBlocksScreenConfigǁget__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁget__mutmut_1': xǁBlocksScreenConfigǁget__mutmut_1, 
        'xǁBlocksScreenConfigǁget__mutmut_2': xǁBlocksScreenConfigǁget__mutmut_2, 
        'xǁBlocksScreenConfigǁget__mutmut_3': xǁBlocksScreenConfigǁget__mutmut_3, 
        'xǁBlocksScreenConfigǁget__mutmut_4': xǁBlocksScreenConfigǁget__mutmut_4, 
        'xǁBlocksScreenConfigǁget__mutmut_5': xǁBlocksScreenConfigǁget__mutmut_5, 
        'xǁBlocksScreenConfigǁget__mutmut_6': xǁBlocksScreenConfigǁget__mutmut_6, 
        'xǁBlocksScreenConfigǁget__mutmut_7': xǁBlocksScreenConfigǁget__mutmut_7
    }
    xǁBlocksScreenConfigǁget__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁget'

    def getint(
        self,
        option: str,
        default: typing.Union[Sentinel, int] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, int]:
        args = [option, default]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁgetint__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁgetint__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁgetint__mutmut_orig(
        self,
        option: str,
        default: typing.Union[Sentinel, int] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, int]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, int], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, int]: Requested option.
        """
        return self.config.getint(section=self.section, option=option, fallback=default)

    def xǁBlocksScreenConfigǁgetint__mutmut_1(
        self,
        option: str,
        default: typing.Union[Sentinel, int] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, int]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, int], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, int]: Requested option.
        """
        return self.config.getint(section=None, option=option, fallback=default)

    def xǁBlocksScreenConfigǁgetint__mutmut_2(
        self,
        option: str,
        default: typing.Union[Sentinel, int] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, int]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, int], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, int]: Requested option.
        """
        return self.config.getint(section=self.section, option=None, fallback=default)

    def xǁBlocksScreenConfigǁgetint__mutmut_3(
        self,
        option: str,
        default: typing.Union[Sentinel, int] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, int]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, int], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, int]: Requested option.
        """
        return self.config.getint(section=self.section, option=option, fallback=None)

    def xǁBlocksScreenConfigǁgetint__mutmut_4(
        self,
        option: str,
        default: typing.Union[Sentinel, int] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, int]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, int], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, int]: Requested option.
        """
        return self.config.getint(option=option, fallback=default)

    def xǁBlocksScreenConfigǁgetint__mutmut_5(
        self,
        option: str,
        default: typing.Union[Sentinel, int] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, int]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, int], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, int]: Requested option.
        """
        return self.config.getint(section=self.section, fallback=default)

    def xǁBlocksScreenConfigǁgetint__mutmut_6(
        self,
        option: str,
        default: typing.Union[Sentinel, int] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, int]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, int], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, int]: Requested option.
        """
        return self.config.getint(section=self.section, option=option, )
    
    xǁBlocksScreenConfigǁgetint__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁgetint__mutmut_1': xǁBlocksScreenConfigǁgetint__mutmut_1, 
        'xǁBlocksScreenConfigǁgetint__mutmut_2': xǁBlocksScreenConfigǁgetint__mutmut_2, 
        'xǁBlocksScreenConfigǁgetint__mutmut_3': xǁBlocksScreenConfigǁgetint__mutmut_3, 
        'xǁBlocksScreenConfigǁgetint__mutmut_4': xǁBlocksScreenConfigǁgetint__mutmut_4, 
        'xǁBlocksScreenConfigǁgetint__mutmut_5': xǁBlocksScreenConfigǁgetint__mutmut_5, 
        'xǁBlocksScreenConfigǁgetint__mutmut_6': xǁBlocksScreenConfigǁgetint__mutmut_6
    }
    xǁBlocksScreenConfigǁgetint__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁgetint'

    def getfloat(
        self,
        option: str,
        default: typing.Union[Sentinel, float] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, float]:
        args = [option, default]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁgetfloat__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁgetfloat__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁgetfloat__mutmut_orig(
        self,
        option: str,
        default: typing.Union[Sentinel, float] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, float]:
        """Get the value for the specified option

        Args:
            option (str): option name
            default (typing.Union[Sentinel, float], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, float]: _description_
        """
        return self.config.getfloat(
            section=self.section, option=option, fallback=default
        )

    def xǁBlocksScreenConfigǁgetfloat__mutmut_1(
        self,
        option: str,
        default: typing.Union[Sentinel, float] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, float]:
        """Get the value for the specified option

        Args:
            option (str): option name
            default (typing.Union[Sentinel, float], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, float]: _description_
        """
        return self.config.getfloat(
            section=None, option=option, fallback=default
        )

    def xǁBlocksScreenConfigǁgetfloat__mutmut_2(
        self,
        option: str,
        default: typing.Union[Sentinel, float] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, float]:
        """Get the value for the specified option

        Args:
            option (str): option name
            default (typing.Union[Sentinel, float], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, float]: _description_
        """
        return self.config.getfloat(
            section=self.section, option=None, fallback=default
        )

    def xǁBlocksScreenConfigǁgetfloat__mutmut_3(
        self,
        option: str,
        default: typing.Union[Sentinel, float] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, float]:
        """Get the value for the specified option

        Args:
            option (str): option name
            default (typing.Union[Sentinel, float], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, float]: _description_
        """
        return self.config.getfloat(
            section=self.section, option=option, fallback=None
        )

    def xǁBlocksScreenConfigǁgetfloat__mutmut_4(
        self,
        option: str,
        default: typing.Union[Sentinel, float] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, float]:
        """Get the value for the specified option

        Args:
            option (str): option name
            default (typing.Union[Sentinel, float], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, float]: _description_
        """
        return self.config.getfloat(
            option=option, fallback=default
        )

    def xǁBlocksScreenConfigǁgetfloat__mutmut_5(
        self,
        option: str,
        default: typing.Union[Sentinel, float] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, float]:
        """Get the value for the specified option

        Args:
            option (str): option name
            default (typing.Union[Sentinel, float], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, float]: _description_
        """
        return self.config.getfloat(
            section=self.section, fallback=default
        )

    def xǁBlocksScreenConfigǁgetfloat__mutmut_6(
        self,
        option: str,
        default: typing.Union[Sentinel, float] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, float]:
        """Get the value for the specified option

        Args:
            option (str): option name
            default (typing.Union[Sentinel, float], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, float]: _description_
        """
        return self.config.getfloat(
            section=self.section, option=option, )
    
    xǁBlocksScreenConfigǁgetfloat__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁgetfloat__mutmut_1': xǁBlocksScreenConfigǁgetfloat__mutmut_1, 
        'xǁBlocksScreenConfigǁgetfloat__mutmut_2': xǁBlocksScreenConfigǁgetfloat__mutmut_2, 
        'xǁBlocksScreenConfigǁgetfloat__mutmut_3': xǁBlocksScreenConfigǁgetfloat__mutmut_3, 
        'xǁBlocksScreenConfigǁgetfloat__mutmut_4': xǁBlocksScreenConfigǁgetfloat__mutmut_4, 
        'xǁBlocksScreenConfigǁgetfloat__mutmut_5': xǁBlocksScreenConfigǁgetfloat__mutmut_5, 
        'xǁBlocksScreenConfigǁgetfloat__mutmut_6': xǁBlocksScreenConfigǁgetfloat__mutmut_6
    }
    xǁBlocksScreenConfigǁgetfloat__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁgetfloat'

    def getboolean(
        self,
        option: str,
        default: typing.Union[Sentinel, bool] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, bool]:
        args = [option, default]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁgetboolean__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁgetboolean__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁgetboolean__mutmut_orig(
        self,
        option: str,
        default: typing.Union[Sentinel, bool] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, bool]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, bool], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, bool]: _description_
        """
        return self.config.getboolean(
            section=self.section, option=option, fallback=default
        )

    def xǁBlocksScreenConfigǁgetboolean__mutmut_1(
        self,
        option: str,
        default: typing.Union[Sentinel, bool] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, bool]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, bool], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, bool]: _description_
        """
        return self.config.getboolean(
            section=None, option=option, fallback=default
        )

    def xǁBlocksScreenConfigǁgetboolean__mutmut_2(
        self,
        option: str,
        default: typing.Union[Sentinel, bool] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, bool]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, bool], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, bool]: _description_
        """
        return self.config.getboolean(
            section=self.section, option=None, fallback=default
        )

    def xǁBlocksScreenConfigǁgetboolean__mutmut_3(
        self,
        option: str,
        default: typing.Union[Sentinel, bool] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, bool]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, bool], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, bool]: _description_
        """
        return self.config.getboolean(
            section=self.section, option=option, fallback=None
        )

    def xǁBlocksScreenConfigǁgetboolean__mutmut_4(
        self,
        option: str,
        default: typing.Union[Sentinel, bool] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, bool]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, bool], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, bool]: _description_
        """
        return self.config.getboolean(
            option=option, fallback=default
        )

    def xǁBlocksScreenConfigǁgetboolean__mutmut_5(
        self,
        option: str,
        default: typing.Union[Sentinel, bool] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, bool]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, bool], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, bool]: _description_
        """
        return self.config.getboolean(
            section=self.section, fallback=default
        )

    def xǁBlocksScreenConfigǁgetboolean__mutmut_6(
        self,
        option: str,
        default: typing.Union[Sentinel, bool] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, bool]:
        """Get option value

        Args:
            option (str): option name
            default (typing.Union[Sentinel, bool], optional): Default value for specified option. Defaults to Sentinel.MISSING.

        Returns:
            typing.Union[Sentinel, bool]: _description_
        """
        return self.config.getboolean(
            section=self.section, option=option, )
    
    xǁBlocksScreenConfigǁgetboolean__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁgetboolean__mutmut_1': xǁBlocksScreenConfigǁgetboolean__mutmut_1, 
        'xǁBlocksScreenConfigǁgetboolean__mutmut_2': xǁBlocksScreenConfigǁgetboolean__mutmut_2, 
        'xǁBlocksScreenConfigǁgetboolean__mutmut_3': xǁBlocksScreenConfigǁgetboolean__mutmut_3, 
        'xǁBlocksScreenConfigǁgetboolean__mutmut_4': xǁBlocksScreenConfigǁgetboolean__mutmut_4, 
        'xǁBlocksScreenConfigǁgetboolean__mutmut_5': xǁBlocksScreenConfigǁgetboolean__mutmut_5, 
        'xǁBlocksScreenConfigǁgetboolean__mutmut_6': xǁBlocksScreenConfigǁgetboolean__mutmut_6
    }
    xǁBlocksScreenConfigǁgetboolean__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁgetboolean'

    def _find_section_index(self, section: str) -> int:
        args = [section]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁ_find_section_index__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁ_find_section_index__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁ_find_section_index__mutmut_orig(self, section: str) -> int:
        """Return the index of the ``[section]`` header line in ``raw_config``."""
        try:
            return self.raw_config.index("[" + section + "]")
        except ValueError as e:
            raise configparser.Error(f'Section "{section}" does not exist: {e}')

    def xǁBlocksScreenConfigǁ_find_section_index__mutmut_1(self, section: str) -> int:
        """Return the index of the ``[section]`` header line in ``raw_config``."""
        try:
            return self.raw_config.index(None)
        except ValueError as e:
            raise configparser.Error(f'Section "{section}" does not exist: {e}')

    def xǁBlocksScreenConfigǁ_find_section_index__mutmut_2(self, section: str) -> int:
        """Return the index of the ``[section]`` header line in ``raw_config``."""
        try:
            return self.raw_config.rindex("[" + section + "]")
        except ValueError as e:
            raise configparser.Error(f'Section "{section}" does not exist: {e}')

    def xǁBlocksScreenConfigǁ_find_section_index__mutmut_3(self, section: str) -> int:
        """Return the index of the ``[section]`` header line in ``raw_config``."""
        try:
            return self.raw_config.index("[" + section - "]")
        except ValueError as e:
            raise configparser.Error(f'Section "{section}" does not exist: {e}')

    def xǁBlocksScreenConfigǁ_find_section_index__mutmut_4(self, section: str) -> int:
        """Return the index of the ``[section]`` header line in ``raw_config``."""
        try:
            return self.raw_config.index("[" - section + "]")
        except ValueError as e:
            raise configparser.Error(f'Section "{section}" does not exist: {e}')

    def xǁBlocksScreenConfigǁ_find_section_index__mutmut_5(self, section: str) -> int:
        """Return the index of the ``[section]`` header line in ``raw_config``."""
        try:
            return self.raw_config.index("XX[XX" + section + "]")
        except ValueError as e:
            raise configparser.Error(f'Section "{section}" does not exist: {e}')

    def xǁBlocksScreenConfigǁ_find_section_index__mutmut_6(self, section: str) -> int:
        """Return the index of the ``[section]`` header line in ``raw_config``."""
        try:
            return self.raw_config.index("[" + section + "XX]XX")
        except ValueError as e:
            raise configparser.Error(f'Section "{section}" does not exist: {e}')

    def xǁBlocksScreenConfigǁ_find_section_index__mutmut_7(self, section: str) -> int:
        """Return the index of the ``[section]`` header line in ``raw_config``."""
        try:
            return self.raw_config.index("[" + section + "]")
        except ValueError as e:
            raise configparser.Error(None)
    
    xǁBlocksScreenConfigǁ_find_section_index__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁ_find_section_index__mutmut_1': xǁBlocksScreenConfigǁ_find_section_index__mutmut_1, 
        'xǁBlocksScreenConfigǁ_find_section_index__mutmut_2': xǁBlocksScreenConfigǁ_find_section_index__mutmut_2, 
        'xǁBlocksScreenConfigǁ_find_section_index__mutmut_3': xǁBlocksScreenConfigǁ_find_section_index__mutmut_3, 
        'xǁBlocksScreenConfigǁ_find_section_index__mutmut_4': xǁBlocksScreenConfigǁ_find_section_index__mutmut_4, 
        'xǁBlocksScreenConfigǁ_find_section_index__mutmut_5': xǁBlocksScreenConfigǁ_find_section_index__mutmut_5, 
        'xǁBlocksScreenConfigǁ_find_section_index__mutmut_6': xǁBlocksScreenConfigǁ_find_section_index__mutmut_6, 
        'xǁBlocksScreenConfigǁ_find_section_index__mutmut_7': xǁBlocksScreenConfigǁ_find_section_index__mutmut_7
    }
    xǁBlocksScreenConfigǁ_find_section_index__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁ_find_section_index'

    def _find_section_limits(self, section: str) -> typing.Tuple:
        args = [section]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁ_find_section_limits__mutmut_orig(self, section: str) -> typing.Tuple:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = self._find_section_index(section)
            buffer = self.raw_config[section_start:]
            section_end = buffer.index("")
            return (section_start, int(section_end + section_start))
        except configparser.Error as e:
            raise configparser.Error(
                f'Error while finding section "{section}" limits on local tracking: {e}'
            )

    def xǁBlocksScreenConfigǁ_find_section_limits__mutmut_1(self, section: str) -> typing.Tuple:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = None
            buffer = self.raw_config[section_start:]
            section_end = buffer.index("")
            return (section_start, int(section_end + section_start))
        except configparser.Error as e:
            raise configparser.Error(
                f'Error while finding section "{section}" limits on local tracking: {e}'
            )

    def xǁBlocksScreenConfigǁ_find_section_limits__mutmut_2(self, section: str) -> typing.Tuple:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = self._find_section_index(None)
            buffer = self.raw_config[section_start:]
            section_end = buffer.index("")
            return (section_start, int(section_end + section_start))
        except configparser.Error as e:
            raise configparser.Error(
                f'Error while finding section "{section}" limits on local tracking: {e}'
            )

    def xǁBlocksScreenConfigǁ_find_section_limits__mutmut_3(self, section: str) -> typing.Tuple:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = self._find_section_index(section)
            buffer = None
            section_end = buffer.index("")
            return (section_start, int(section_end + section_start))
        except configparser.Error as e:
            raise configparser.Error(
                f'Error while finding section "{section}" limits on local tracking: {e}'
            )

    def xǁBlocksScreenConfigǁ_find_section_limits__mutmut_4(self, section: str) -> typing.Tuple:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = self._find_section_index(section)
            buffer = self.raw_config[section_start:]
            section_end = None
            return (section_start, int(section_end + section_start))
        except configparser.Error as e:
            raise configparser.Error(
                f'Error while finding section "{section}" limits on local tracking: {e}'
            )

    def xǁBlocksScreenConfigǁ_find_section_limits__mutmut_5(self, section: str) -> typing.Tuple:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = self._find_section_index(section)
            buffer = self.raw_config[section_start:]
            section_end = buffer.index(None)
            return (section_start, int(section_end + section_start))
        except configparser.Error as e:
            raise configparser.Error(
                f'Error while finding section "{section}" limits on local tracking: {e}'
            )

    def xǁBlocksScreenConfigǁ_find_section_limits__mutmut_6(self, section: str) -> typing.Tuple:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = self._find_section_index(section)
            buffer = self.raw_config[section_start:]
            section_end = buffer.rindex("")
            return (section_start, int(section_end + section_start))
        except configparser.Error as e:
            raise configparser.Error(
                f'Error while finding section "{section}" limits on local tracking: {e}'
            )

    def xǁBlocksScreenConfigǁ_find_section_limits__mutmut_7(self, section: str) -> typing.Tuple:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = self._find_section_index(section)
            buffer = self.raw_config[section_start:]
            section_end = buffer.index("XXXX")
            return (section_start, int(section_end + section_start))
        except configparser.Error as e:
            raise configparser.Error(
                f'Error while finding section "{section}" limits on local tracking: {e}'
            )

    def xǁBlocksScreenConfigǁ_find_section_limits__mutmut_8(self, section: str) -> typing.Tuple:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = self._find_section_index(section)
            buffer = self.raw_config[section_start:]
            section_end = buffer.index("")
            return (section_start, int(None))
        except configparser.Error as e:
            raise configparser.Error(
                f'Error while finding section "{section}" limits on local tracking: {e}'
            )

    def xǁBlocksScreenConfigǁ_find_section_limits__mutmut_9(self, section: str) -> typing.Tuple:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = self._find_section_index(section)
            buffer = self.raw_config[section_start:]
            section_end = buffer.index("")
            return (section_start, int(section_end - section_start))
        except configparser.Error as e:
            raise configparser.Error(
                f'Error while finding section "{section}" limits on local tracking: {e}'
            )

    def xǁBlocksScreenConfigǁ_find_section_limits__mutmut_10(self, section: str) -> typing.Tuple:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = self._find_section_index(section)
            buffer = self.raw_config[section_start:]
            section_end = buffer.index("")
            return (section_start, int(section_end + section_start))
        except configparser.Error as e:
            raise configparser.Error(
                None
            )
    
    xǁBlocksScreenConfigǁ_find_section_limits__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_1': xǁBlocksScreenConfigǁ_find_section_limits__mutmut_1, 
        'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_2': xǁBlocksScreenConfigǁ_find_section_limits__mutmut_2, 
        'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_3': xǁBlocksScreenConfigǁ_find_section_limits__mutmut_3, 
        'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_4': xǁBlocksScreenConfigǁ_find_section_limits__mutmut_4, 
        'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_5': xǁBlocksScreenConfigǁ_find_section_limits__mutmut_5, 
        'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_6': xǁBlocksScreenConfigǁ_find_section_limits__mutmut_6, 
        'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_7': xǁBlocksScreenConfigǁ_find_section_limits__mutmut_7, 
        'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_8': xǁBlocksScreenConfigǁ_find_section_limits__mutmut_8, 
        'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_9': xǁBlocksScreenConfigǁ_find_section_limits__mutmut_9, 
        'xǁBlocksScreenConfigǁ_find_section_limits__mutmut_10': xǁBlocksScreenConfigǁ_find_section_limits__mutmut_10
    }
    xǁBlocksScreenConfigǁ_find_section_limits__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁ_find_section_limits'

    def _find_option_index(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        args = [section, option]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁ_find_option_index__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁ_find_option_index__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_orig(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(section)
            section_buffer = self.raw_config[start:][:end]
            for index in range(len(section_buffer)):
                if "[" + option + "]" in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_1(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = None
            section_buffer = self.raw_config[start:][:end]
            for index in range(len(section_buffer)):
                if "[" + option + "]" in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_2(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(None)
            section_buffer = self.raw_config[start:][:end]
            for index in range(len(section_buffer)):
                if "[" + option + "]" in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_3(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(section)
            section_buffer = None
            for index in range(len(section_buffer)):
                if "[" + option + "]" in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_4(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(section)
            section_buffer = self.raw_config[start:][:end]
            for index in range(None):
                if "[" + option + "]" in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_5(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(section)
            section_buffer = self.raw_config[start:][:end]
            for index in range(len(section_buffer)):
                if "[" + option - "]" in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_6(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(section)
            section_buffer = self.raw_config[start:][:end]
            for index in range(len(section_buffer)):
                if "[" - option + "]" in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_7(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(section)
            section_buffer = self.raw_config[start:][:end]
            for index in range(len(section_buffer)):
                if "XX[XX" + option + "]" in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_8(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(section)
            section_buffer = self.raw_config[start:][:end]
            for index in range(len(section_buffer)):
                if "[" + option + "XX]XX" in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_9(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(section)
            section_buffer = self.raw_config[start:][:end]
            for index in range(len(section_buffer)):
                if "[" + option + "]" not in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_10(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(section)
            section_buffer = self.raw_config[start:][:end]
            for index in range(len(section_buffer)):
                if "[" + option + "]" in section_buffer[index]:
                    return start - index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_11(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(section)
            section_buffer = self.raw_config[start:][:end]
            for index in range(len(section_buffer)):
                if "[" + option + "]" in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                None
            )
        except configparser.Error as e:
            raise configparser.Error(
                f'Unable to find option "{option}" in section "{section}":  {e}'
            )

    def xǁBlocksScreenConfigǁ_find_option_index__mutmut_12(
        self, section: str, option: str
    ) -> typing.Union[Sentinel, int, None]:
        """Return the index of the *option* line within *section* in ``raw_config``."""
        try:
            start, end = self._find_section_limits(section)
            section_buffer = self.raw_config[start:][:end]
            for index in range(len(section_buffer)):
                if "[" + option + "]" in section_buffer[index]:
                    return start + index
            raise configparser.Error(
                f'Cannot find option "{option}" in section "{section}"'
            )
        except configparser.Error as e:
            raise configparser.Error(
                None
            )
    
    xǁBlocksScreenConfigǁ_find_option_index__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁ_find_option_index__mutmut_1': xǁBlocksScreenConfigǁ_find_option_index__mutmut_1, 
        'xǁBlocksScreenConfigǁ_find_option_index__mutmut_2': xǁBlocksScreenConfigǁ_find_option_index__mutmut_2, 
        'xǁBlocksScreenConfigǁ_find_option_index__mutmut_3': xǁBlocksScreenConfigǁ_find_option_index__mutmut_3, 
        'xǁBlocksScreenConfigǁ_find_option_index__mutmut_4': xǁBlocksScreenConfigǁ_find_option_index__mutmut_4, 
        'xǁBlocksScreenConfigǁ_find_option_index__mutmut_5': xǁBlocksScreenConfigǁ_find_option_index__mutmut_5, 
        'xǁBlocksScreenConfigǁ_find_option_index__mutmut_6': xǁBlocksScreenConfigǁ_find_option_index__mutmut_6, 
        'xǁBlocksScreenConfigǁ_find_option_index__mutmut_7': xǁBlocksScreenConfigǁ_find_option_index__mutmut_7, 
        'xǁBlocksScreenConfigǁ_find_option_index__mutmut_8': xǁBlocksScreenConfigǁ_find_option_index__mutmut_8, 
        'xǁBlocksScreenConfigǁ_find_option_index__mutmut_9': xǁBlocksScreenConfigǁ_find_option_index__mutmut_9, 
        'xǁBlocksScreenConfigǁ_find_option_index__mutmut_10': xǁBlocksScreenConfigǁ_find_option_index__mutmut_10, 
        'xǁBlocksScreenConfigǁ_find_option_index__mutmut_11': xǁBlocksScreenConfigǁ_find_option_index__mutmut_11, 
        'xǁBlocksScreenConfigǁ_find_option_index__mutmut_12': xǁBlocksScreenConfigǁ_find_option_index__mutmut_12
    }
    xǁBlocksScreenConfigǁ_find_option_index__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁ_find_option_index'

    def add_section(self, section: str) -> None:
        args = [section]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁadd_section__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁadd_section__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁadd_section__mutmut_orig(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_1(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = None
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_2(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string not in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_3(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        None
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_4(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = None
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_5(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config or config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_6(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[+1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_7(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-2].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_8(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() == "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_9(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "XXXX":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_10(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append(None)
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_11(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("XXXX")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_12(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend(None)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_13(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, "XXXX"])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_14(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = None
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_15(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(None)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_16(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "XX\nXX".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_17(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = None
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_18(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[+1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_19(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-2] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_20(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] == "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_21(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "XXXX":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_22(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append(None)
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_23(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("XXXX")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_24(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(None)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_25(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = None
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_26(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = False
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_27(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(None)
        except configparser.Error as e:
            logger.error(f'Unable to add "{section}" section to configuration: {e}')

    def xǁBlocksScreenConfigǁadd_section__mutmut_28(self, section: str) -> None:
        """Add a section to configuration file

        Args:
            section (str): section name

        Raises:
            configparser.DuplicateSectionError: Exception thrown when section is duplicated
        """
        try:
            with self.file_lock:
                sec_string = f"[{section}]"
                if sec_string in self.raw_config:
                    raise configparser.DuplicateSectionError(
                        f'Section "{sec_string}" already exists'
                    )
                config = self.raw_config
                if config and config[-1].strip() != "":
                    config.append("")
                config.extend([sec_string, ""])
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logger.error(None)
    
    xǁBlocksScreenConfigǁadd_section__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁadd_section__mutmut_1': xǁBlocksScreenConfigǁadd_section__mutmut_1, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_2': xǁBlocksScreenConfigǁadd_section__mutmut_2, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_3': xǁBlocksScreenConfigǁadd_section__mutmut_3, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_4': xǁBlocksScreenConfigǁadd_section__mutmut_4, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_5': xǁBlocksScreenConfigǁadd_section__mutmut_5, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_6': xǁBlocksScreenConfigǁadd_section__mutmut_6, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_7': xǁBlocksScreenConfigǁadd_section__mutmut_7, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_8': xǁBlocksScreenConfigǁadd_section__mutmut_8, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_9': xǁBlocksScreenConfigǁadd_section__mutmut_9, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_10': xǁBlocksScreenConfigǁadd_section__mutmut_10, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_11': xǁBlocksScreenConfigǁadd_section__mutmut_11, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_12': xǁBlocksScreenConfigǁadd_section__mutmut_12, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_13': xǁBlocksScreenConfigǁadd_section__mutmut_13, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_14': xǁBlocksScreenConfigǁadd_section__mutmut_14, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_15': xǁBlocksScreenConfigǁadd_section__mutmut_15, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_16': xǁBlocksScreenConfigǁadd_section__mutmut_16, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_17': xǁBlocksScreenConfigǁadd_section__mutmut_17, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_18': xǁBlocksScreenConfigǁadd_section__mutmut_18, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_19': xǁBlocksScreenConfigǁadd_section__mutmut_19, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_20': xǁBlocksScreenConfigǁadd_section__mutmut_20, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_21': xǁBlocksScreenConfigǁadd_section__mutmut_21, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_22': xǁBlocksScreenConfigǁadd_section__mutmut_22, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_23': xǁBlocksScreenConfigǁadd_section__mutmut_23, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_24': xǁBlocksScreenConfigǁadd_section__mutmut_24, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_25': xǁBlocksScreenConfigǁadd_section__mutmut_25, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_26': xǁBlocksScreenConfigǁadd_section__mutmut_26, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_27': xǁBlocksScreenConfigǁadd_section__mutmut_27, 
        'xǁBlocksScreenConfigǁadd_section__mutmut_28': xǁBlocksScreenConfigǁadd_section__mutmut_28
    }
    xǁBlocksScreenConfigǁadd_section__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁadd_section'

    def add_option(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        args = [section, option, value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁadd_option__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁadd_option__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁadd_option__mutmut_orig(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_1(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = None
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_2(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(None)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_3(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = None
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_4(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = None
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_5(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(None, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_6(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, None)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_7(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_8(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, )
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_9(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = None
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_10(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(None)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_11(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "XX\nXX".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_12(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = None
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_13(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[+1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_14(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-2] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_15(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] == "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_16(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "XXXX":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_17(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append(None)
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_18(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("XXXX")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_19(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(None, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_20(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, None, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_21(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, None)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_22(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_23(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_24(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, )
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_25(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = None
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_26(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = False
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_27(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(None)
        except configparser.Error as e:
            logger.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def xǁBlocksScreenConfigǁadd_option__mutmut_28(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
        """Add option with a value to a section

        Args:
            section (str): section name
            option (str): option name
            value (typing.Union[str, None], optional): value for the specified option. Defaults to None.
        """
        try:
            with self.file_lock:
                section_start, section_end = self._find_section_limits(section)
                config = self.raw_config.copy()
                opt_string = f"{option}: {value}"
                config.insert(section_end, opt_string)
                updated_config = "\n".join(config)
                self.raw_config = updated_config.splitlines()
                if self.raw_config[-1] != "":
                    self.raw_config.append("")
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logger.error(
                None
            )
    
    xǁBlocksScreenConfigǁadd_option__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁadd_option__mutmut_1': xǁBlocksScreenConfigǁadd_option__mutmut_1, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_2': xǁBlocksScreenConfigǁadd_option__mutmut_2, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_3': xǁBlocksScreenConfigǁadd_option__mutmut_3, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_4': xǁBlocksScreenConfigǁadd_option__mutmut_4, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_5': xǁBlocksScreenConfigǁadd_option__mutmut_5, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_6': xǁBlocksScreenConfigǁadd_option__mutmut_6, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_7': xǁBlocksScreenConfigǁadd_option__mutmut_7, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_8': xǁBlocksScreenConfigǁadd_option__mutmut_8, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_9': xǁBlocksScreenConfigǁadd_option__mutmut_9, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_10': xǁBlocksScreenConfigǁadd_option__mutmut_10, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_11': xǁBlocksScreenConfigǁadd_option__mutmut_11, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_12': xǁBlocksScreenConfigǁadd_option__mutmut_12, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_13': xǁBlocksScreenConfigǁadd_option__mutmut_13, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_14': xǁBlocksScreenConfigǁadd_option__mutmut_14, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_15': xǁBlocksScreenConfigǁadd_option__mutmut_15, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_16': xǁBlocksScreenConfigǁadd_option__mutmut_16, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_17': xǁBlocksScreenConfigǁadd_option__mutmut_17, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_18': xǁBlocksScreenConfigǁadd_option__mutmut_18, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_19': xǁBlocksScreenConfigǁadd_option__mutmut_19, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_20': xǁBlocksScreenConfigǁadd_option__mutmut_20, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_21': xǁBlocksScreenConfigǁadd_option__mutmut_21, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_22': xǁBlocksScreenConfigǁadd_option__mutmut_22, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_23': xǁBlocksScreenConfigǁadd_option__mutmut_23, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_24': xǁBlocksScreenConfigǁadd_option__mutmut_24, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_25': xǁBlocksScreenConfigǁadd_option__mutmut_25, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_26': xǁBlocksScreenConfigǁadd_option__mutmut_26, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_27': xǁBlocksScreenConfigǁadd_option__mutmut_27, 
        'xǁBlocksScreenConfigǁadd_option__mutmut_28': xǁBlocksScreenConfigǁadd_option__mutmut_28
    }
    xǁBlocksScreenConfigǁadd_option__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁadd_option'

    def update_option(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        args = [section, option, value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁupdate_option__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁupdate_option__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁupdate_option__mutmut_orig(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_1(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_2(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(None):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_3(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(None)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_4(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_5(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(None, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_6(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, None):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_7(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_8(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, ):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_9(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(None, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_10(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, None, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_11(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, None)
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_12(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_13(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_14(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, )
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_15(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(None))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_16(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = None
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_17(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(None, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_18(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, None)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_19(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_20(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, )
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_21(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = None
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_22(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(None, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_23(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, None, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_24(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, None)
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_25(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_26(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_27(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, )
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_28(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(None))
                self.update_pending = True
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_29(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = None
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_30(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = False
        except Exception as e:
            logger.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def xǁBlocksScreenConfigǁupdate_option__mutmut_31(
        self,
        section: str,
        option: str,
        value: typing.Any,
    ) -> None:
        """Update an existing option's value in both raw tracking and configparser."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)

                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return

                line_idx = self._find_option_line_index(section, option)
                self.raw_config[line_idx] = f"{option}: {value}"
                self.config.set(section, option, str(value))
                self.update_pending = True
        except Exception as e:
            logger.error(
                None
            )
    
    xǁBlocksScreenConfigǁupdate_option__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁupdate_option__mutmut_1': xǁBlocksScreenConfigǁupdate_option__mutmut_1, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_2': xǁBlocksScreenConfigǁupdate_option__mutmut_2, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_3': xǁBlocksScreenConfigǁupdate_option__mutmut_3, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_4': xǁBlocksScreenConfigǁupdate_option__mutmut_4, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_5': xǁBlocksScreenConfigǁupdate_option__mutmut_5, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_6': xǁBlocksScreenConfigǁupdate_option__mutmut_6, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_7': xǁBlocksScreenConfigǁupdate_option__mutmut_7, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_8': xǁBlocksScreenConfigǁupdate_option__mutmut_8, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_9': xǁBlocksScreenConfigǁupdate_option__mutmut_9, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_10': xǁBlocksScreenConfigǁupdate_option__mutmut_10, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_11': xǁBlocksScreenConfigǁupdate_option__mutmut_11, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_12': xǁBlocksScreenConfigǁupdate_option__mutmut_12, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_13': xǁBlocksScreenConfigǁupdate_option__mutmut_13, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_14': xǁBlocksScreenConfigǁupdate_option__mutmut_14, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_15': xǁBlocksScreenConfigǁupdate_option__mutmut_15, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_16': xǁBlocksScreenConfigǁupdate_option__mutmut_16, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_17': xǁBlocksScreenConfigǁupdate_option__mutmut_17, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_18': xǁBlocksScreenConfigǁupdate_option__mutmut_18, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_19': xǁBlocksScreenConfigǁupdate_option__mutmut_19, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_20': xǁBlocksScreenConfigǁupdate_option__mutmut_20, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_21': xǁBlocksScreenConfigǁupdate_option__mutmut_21, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_22': xǁBlocksScreenConfigǁupdate_option__mutmut_22, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_23': xǁBlocksScreenConfigǁupdate_option__mutmut_23, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_24': xǁBlocksScreenConfigǁupdate_option__mutmut_24, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_25': xǁBlocksScreenConfigǁupdate_option__mutmut_25, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_26': xǁBlocksScreenConfigǁupdate_option__mutmut_26, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_27': xǁBlocksScreenConfigǁupdate_option__mutmut_27, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_28': xǁBlocksScreenConfigǁupdate_option__mutmut_28, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_29': xǁBlocksScreenConfigǁupdate_option__mutmut_29, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_30': xǁBlocksScreenConfigǁupdate_option__mutmut_30, 
        'xǁBlocksScreenConfigǁupdate_option__mutmut_31': xǁBlocksScreenConfigǁupdate_option__mutmut_31
    }
    xǁBlocksScreenConfigǁupdate_option__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁupdate_option'

    def _find_option_line_index(self, section: str, option: str) -> int:
        args = [section, option]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_orig(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(start + 1, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_1(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = None
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(start + 1, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_2(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(None)
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(start + 1, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_3(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = None
        for i in range(start + 1, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_4(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(None)
        for i in range(start + 1, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_5(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(rf"^\s*{re.escape(None)}\s*[:=]")
        for i in range(start + 1, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_6(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(None, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_7(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(start + 1, None):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_8(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_9(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(start + 1, ):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_10(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(start - 1, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_11(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(start + 2, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_12(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(start + 1, end):
            if opt_regex.match(None):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_13(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(start + 1, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(None)
    
    xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_1': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_1, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_2': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_2, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_3': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_3, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_4': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_4, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_5': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_5, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_6': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_6, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_7': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_7, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_8': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_8, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_9': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_9, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_10': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_10, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_11': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_11, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_12': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_12, 
        'xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_13': xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_13
    }
    xǁBlocksScreenConfigǁ_find_option_line_index__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁ_find_option_line_index'

    def save_configuration(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁsave_configuration__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁsave_configuration__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_orig(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), encoding="utf-8")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_1(self) -> None:
        """Save teh configuration to file"""
        try:
            if self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), encoding="utf-8")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_2(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text(None, encoding="utf-8")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_3(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), encoding=None)
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_4(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text(encoding="utf-8")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_5(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), )
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_6(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(None), encoding="utf-8")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_7(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("XX\nXX".join(self.raw_config), encoding="utf-8")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_8(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), encoding="XXutf-8XX")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_9(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), encoding="UTF-8")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_10(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), encoding="utf-8")
                sio = None
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_11(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), encoding="utf-8")
                sio = io.StringIO()
                sio.writelines(None)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_12(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), encoding="utf-8")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(None)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_13(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), encoding="utf-8")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                None
            )
        finally:
            self.update_pending = False

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_14(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), encoding="utf-8")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = None

    def xǁBlocksScreenConfigǁsave_configuration__mutmut_15(self) -> None:
        """Save teh configuration to file"""
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text("\n".join(self.raw_config), encoding="utf-8")
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logger.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = True
    
    xǁBlocksScreenConfigǁsave_configuration__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁsave_configuration__mutmut_1': xǁBlocksScreenConfigǁsave_configuration__mutmut_1, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_2': xǁBlocksScreenConfigǁsave_configuration__mutmut_2, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_3': xǁBlocksScreenConfigǁsave_configuration__mutmut_3, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_4': xǁBlocksScreenConfigǁsave_configuration__mutmut_4, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_5': xǁBlocksScreenConfigǁsave_configuration__mutmut_5, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_6': xǁBlocksScreenConfigǁsave_configuration__mutmut_6, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_7': xǁBlocksScreenConfigǁsave_configuration__mutmut_7, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_8': xǁBlocksScreenConfigǁsave_configuration__mutmut_8, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_9': xǁBlocksScreenConfigǁsave_configuration__mutmut_9, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_10': xǁBlocksScreenConfigǁsave_configuration__mutmut_10, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_11': xǁBlocksScreenConfigǁsave_configuration__mutmut_11, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_12': xǁBlocksScreenConfigǁsave_configuration__mutmut_12, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_13': xǁBlocksScreenConfigǁsave_configuration__mutmut_13, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_14': xǁBlocksScreenConfigǁsave_configuration__mutmut_14, 
        'xǁBlocksScreenConfigǁsave_configuration__mutmut_15': xǁBlocksScreenConfigǁsave_configuration__mutmut_15
    }
    xǁBlocksScreenConfigǁsave_configuration__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁsave_configuration'

    def load_config(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁload_config__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁload_config__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁload_config__mutmut_orig(self):
        """Load configuration file"""
        try:
            self.raw_config.clear()
            self.config.clear()  # Reset configparser
            self.raw_config, self.raw_dict_config = self._parse_file()
            if self.raw_config:
                self.config.read_file(self.raw_config)
        except Exception as e:
            raise configparser.Error(f"Error loading configuration file: {e}")

    def xǁBlocksScreenConfigǁload_config__mutmut_1(self):
        """Load configuration file"""
        try:
            self.raw_config.clear()
            self.config.clear()  # Reset configparser
            self.raw_config, self.raw_dict_config = None
            if self.raw_config:
                self.config.read_file(self.raw_config)
        except Exception as e:
            raise configparser.Error(f"Error loading configuration file: {e}")

    def xǁBlocksScreenConfigǁload_config__mutmut_2(self):
        """Load configuration file"""
        try:
            self.raw_config.clear()
            self.config.clear()  # Reset configparser
            self.raw_config, self.raw_dict_config = self._parse_file()
            if self.raw_config:
                self.config.read_file(None)
        except Exception as e:
            raise configparser.Error(f"Error loading configuration file: {e}")

    def xǁBlocksScreenConfigǁload_config__mutmut_3(self):
        """Load configuration file"""
        try:
            self.raw_config.clear()
            self.config.clear()  # Reset configparser
            self.raw_config, self.raw_dict_config = self._parse_file()
            if self.raw_config:
                self.config.read_file(self.raw_config)
        except Exception as e:
            raise configparser.Error(None)
    
    xǁBlocksScreenConfigǁload_config__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁload_config__mutmut_1': xǁBlocksScreenConfigǁload_config__mutmut_1, 
        'xǁBlocksScreenConfigǁload_config__mutmut_2': xǁBlocksScreenConfigǁload_config__mutmut_2, 
        'xǁBlocksScreenConfigǁload_config__mutmut_3': xǁBlocksScreenConfigǁload_config__mutmut_3
    }
    xǁBlocksScreenConfigǁload_config__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁload_config'

    def _parse_file(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksScreenConfigǁ_parse_file__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksScreenConfigǁ_parse_file__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_orig(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_1(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = None
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_2(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = None
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_3(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = None
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_4(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=None)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_5(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=True)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_6(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = None
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_7(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding=None)
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_8(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="XXutf-8XX")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_9(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="UTF-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_10(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = None
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_11(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_12(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    break
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_13(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(None)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_14(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = None
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_15(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(None, line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_16(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", None)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_17(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_18(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", )
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_19(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"XX\s*#\s*(.*)(\s*)XX", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_20(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = None
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_21(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_22(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        break
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_23(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = None
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_24(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(None, r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_25(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", None, line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_26(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", None)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_27(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_28(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_29(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", )
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_30(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"XX\s*([:=])\s*XX", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_31(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"XX\1 XX", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_32(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = None
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_33(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(None, r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_34(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", None, line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_35(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", None)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_36(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_37(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_38(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", )
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_39(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"XX=XX", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_40(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r"XX:XX", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_41(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = None
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_42(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(None)
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_43(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"XX[^\s]*\[([^]]+)\]XX")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_44(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = None  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_45(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(None, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_46(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, None)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_47(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_48(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, )  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_49(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = None
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_50(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(None, r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_51(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", None, line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_52(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", None)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_53(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_54(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_55(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", )
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_56(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"XX[\[*\]]XX", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_57(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"XXXX", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_58(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_59(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                None
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_60(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                ["XXXX"]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_61(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update(None)
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_62(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = None
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_63(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        break
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_64(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = None
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_65(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(None)
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_66(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"XX^(?:\w+)([:*])(?:.*)XX")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_67(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = None
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_68(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(None, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_69(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, None)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_70(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_71(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, )
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_72(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = None
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_73(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(None, maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_74(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=None)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_75(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_76(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", )
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_77(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.rsplit(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_78(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split("XX:XX", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_79(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=2)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_80(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_81(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(None, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_82(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, None).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_83(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get({}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_84(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, ).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_85(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec not in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_86(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = None
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_87(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(None, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_88(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, None)
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_89(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get({})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_90(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, )
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_91(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update(None)
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_92(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update(None)
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_93(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        break
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_94(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(None)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_95(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[+1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_96(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-2] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_97(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] == "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_98(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "XXXX":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_99(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append(None)
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_100(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("XXXX")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
        finally:
            self.file_lock.release()

    def xǁBlocksScreenConfigǁ_parse_file__mutmut_101(self) -> typing.Tuple[typing.List[str], typing.Dict]:
        """Read and normalise the config file into a raw line list and a nested dict.

        Strips comments, normalises ``=`` to ``:`` separators, deduplicates
        sections/options, and ensures the buffer ends with an empty line.

        Returns:
            A tuple of (raw_lines, dict_representation).
        """
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
            self.file_lock.acquire(blocking=False)
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(indentation_size)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1 ", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
                        if buffer:
                            buffer.extend(
                                [""]
                            )  # REFACTOR: Just add some line separation between sections
                        dict_buff.update({sec_name: {}})
                        curr_sec = sec_name
                    else:
                        continue
                option_match = re.compile(r"^(?:\w+)([:*])(?:.*)")
                match_opt = re.match(option_match, line)
                if match_opt:
                    option_name, value = line.split(":", maxsplit=1)
                    if option_name not in dict_buff.get(curr_sec, {}).keys():
                        if curr_sec in dict_buff.keys():
                            section: dict = dict_buff.get(curr_sec, {})
                            section.update({option_name: value})
                            dict_buff.update({curr_sec: section})
                    else:
                        continue
                buffer.append(line)
            if buffer[-1] != "":
                buffer.append("")
            return buffer, dict_buff
        except Exception as e:
            raise configparser.Error(
                None
            )
        finally:
            self.file_lock.release()
    
    xǁBlocksScreenConfigǁ_parse_file__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksScreenConfigǁ_parse_file__mutmut_1': xǁBlocksScreenConfigǁ_parse_file__mutmut_1, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_2': xǁBlocksScreenConfigǁ_parse_file__mutmut_2, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_3': xǁBlocksScreenConfigǁ_parse_file__mutmut_3, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_4': xǁBlocksScreenConfigǁ_parse_file__mutmut_4, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_5': xǁBlocksScreenConfigǁ_parse_file__mutmut_5, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_6': xǁBlocksScreenConfigǁ_parse_file__mutmut_6, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_7': xǁBlocksScreenConfigǁ_parse_file__mutmut_7, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_8': xǁBlocksScreenConfigǁ_parse_file__mutmut_8, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_9': xǁBlocksScreenConfigǁ_parse_file__mutmut_9, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_10': xǁBlocksScreenConfigǁ_parse_file__mutmut_10, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_11': xǁBlocksScreenConfigǁ_parse_file__mutmut_11, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_12': xǁBlocksScreenConfigǁ_parse_file__mutmut_12, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_13': xǁBlocksScreenConfigǁ_parse_file__mutmut_13, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_14': xǁBlocksScreenConfigǁ_parse_file__mutmut_14, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_15': xǁBlocksScreenConfigǁ_parse_file__mutmut_15, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_16': xǁBlocksScreenConfigǁ_parse_file__mutmut_16, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_17': xǁBlocksScreenConfigǁ_parse_file__mutmut_17, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_18': xǁBlocksScreenConfigǁ_parse_file__mutmut_18, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_19': xǁBlocksScreenConfigǁ_parse_file__mutmut_19, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_20': xǁBlocksScreenConfigǁ_parse_file__mutmut_20, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_21': xǁBlocksScreenConfigǁ_parse_file__mutmut_21, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_22': xǁBlocksScreenConfigǁ_parse_file__mutmut_22, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_23': xǁBlocksScreenConfigǁ_parse_file__mutmut_23, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_24': xǁBlocksScreenConfigǁ_parse_file__mutmut_24, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_25': xǁBlocksScreenConfigǁ_parse_file__mutmut_25, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_26': xǁBlocksScreenConfigǁ_parse_file__mutmut_26, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_27': xǁBlocksScreenConfigǁ_parse_file__mutmut_27, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_28': xǁBlocksScreenConfigǁ_parse_file__mutmut_28, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_29': xǁBlocksScreenConfigǁ_parse_file__mutmut_29, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_30': xǁBlocksScreenConfigǁ_parse_file__mutmut_30, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_31': xǁBlocksScreenConfigǁ_parse_file__mutmut_31, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_32': xǁBlocksScreenConfigǁ_parse_file__mutmut_32, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_33': xǁBlocksScreenConfigǁ_parse_file__mutmut_33, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_34': xǁBlocksScreenConfigǁ_parse_file__mutmut_34, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_35': xǁBlocksScreenConfigǁ_parse_file__mutmut_35, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_36': xǁBlocksScreenConfigǁ_parse_file__mutmut_36, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_37': xǁBlocksScreenConfigǁ_parse_file__mutmut_37, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_38': xǁBlocksScreenConfigǁ_parse_file__mutmut_38, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_39': xǁBlocksScreenConfigǁ_parse_file__mutmut_39, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_40': xǁBlocksScreenConfigǁ_parse_file__mutmut_40, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_41': xǁBlocksScreenConfigǁ_parse_file__mutmut_41, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_42': xǁBlocksScreenConfigǁ_parse_file__mutmut_42, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_43': xǁBlocksScreenConfigǁ_parse_file__mutmut_43, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_44': xǁBlocksScreenConfigǁ_parse_file__mutmut_44, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_45': xǁBlocksScreenConfigǁ_parse_file__mutmut_45, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_46': xǁBlocksScreenConfigǁ_parse_file__mutmut_46, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_47': xǁBlocksScreenConfigǁ_parse_file__mutmut_47, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_48': xǁBlocksScreenConfigǁ_parse_file__mutmut_48, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_49': xǁBlocksScreenConfigǁ_parse_file__mutmut_49, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_50': xǁBlocksScreenConfigǁ_parse_file__mutmut_50, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_51': xǁBlocksScreenConfigǁ_parse_file__mutmut_51, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_52': xǁBlocksScreenConfigǁ_parse_file__mutmut_52, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_53': xǁBlocksScreenConfigǁ_parse_file__mutmut_53, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_54': xǁBlocksScreenConfigǁ_parse_file__mutmut_54, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_55': xǁBlocksScreenConfigǁ_parse_file__mutmut_55, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_56': xǁBlocksScreenConfigǁ_parse_file__mutmut_56, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_57': xǁBlocksScreenConfigǁ_parse_file__mutmut_57, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_58': xǁBlocksScreenConfigǁ_parse_file__mutmut_58, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_59': xǁBlocksScreenConfigǁ_parse_file__mutmut_59, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_60': xǁBlocksScreenConfigǁ_parse_file__mutmut_60, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_61': xǁBlocksScreenConfigǁ_parse_file__mutmut_61, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_62': xǁBlocksScreenConfigǁ_parse_file__mutmut_62, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_63': xǁBlocksScreenConfigǁ_parse_file__mutmut_63, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_64': xǁBlocksScreenConfigǁ_parse_file__mutmut_64, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_65': xǁBlocksScreenConfigǁ_parse_file__mutmut_65, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_66': xǁBlocksScreenConfigǁ_parse_file__mutmut_66, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_67': xǁBlocksScreenConfigǁ_parse_file__mutmut_67, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_68': xǁBlocksScreenConfigǁ_parse_file__mutmut_68, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_69': xǁBlocksScreenConfigǁ_parse_file__mutmut_69, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_70': xǁBlocksScreenConfigǁ_parse_file__mutmut_70, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_71': xǁBlocksScreenConfigǁ_parse_file__mutmut_71, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_72': xǁBlocksScreenConfigǁ_parse_file__mutmut_72, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_73': xǁBlocksScreenConfigǁ_parse_file__mutmut_73, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_74': xǁBlocksScreenConfigǁ_parse_file__mutmut_74, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_75': xǁBlocksScreenConfigǁ_parse_file__mutmut_75, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_76': xǁBlocksScreenConfigǁ_parse_file__mutmut_76, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_77': xǁBlocksScreenConfigǁ_parse_file__mutmut_77, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_78': xǁBlocksScreenConfigǁ_parse_file__mutmut_78, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_79': xǁBlocksScreenConfigǁ_parse_file__mutmut_79, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_80': xǁBlocksScreenConfigǁ_parse_file__mutmut_80, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_81': xǁBlocksScreenConfigǁ_parse_file__mutmut_81, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_82': xǁBlocksScreenConfigǁ_parse_file__mutmut_82, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_83': xǁBlocksScreenConfigǁ_parse_file__mutmut_83, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_84': xǁBlocksScreenConfigǁ_parse_file__mutmut_84, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_85': xǁBlocksScreenConfigǁ_parse_file__mutmut_85, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_86': xǁBlocksScreenConfigǁ_parse_file__mutmut_86, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_87': xǁBlocksScreenConfigǁ_parse_file__mutmut_87, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_88': xǁBlocksScreenConfigǁ_parse_file__mutmut_88, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_89': xǁBlocksScreenConfigǁ_parse_file__mutmut_89, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_90': xǁBlocksScreenConfigǁ_parse_file__mutmut_90, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_91': xǁBlocksScreenConfigǁ_parse_file__mutmut_91, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_92': xǁBlocksScreenConfigǁ_parse_file__mutmut_92, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_93': xǁBlocksScreenConfigǁ_parse_file__mutmut_93, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_94': xǁBlocksScreenConfigǁ_parse_file__mutmut_94, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_95': xǁBlocksScreenConfigǁ_parse_file__mutmut_95, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_96': xǁBlocksScreenConfigǁ_parse_file__mutmut_96, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_97': xǁBlocksScreenConfigǁ_parse_file__mutmut_97, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_98': xǁBlocksScreenConfigǁ_parse_file__mutmut_98, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_99': xǁBlocksScreenConfigǁ_parse_file__mutmut_99, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_100': xǁBlocksScreenConfigǁ_parse_file__mutmut_100, 
        'xǁBlocksScreenConfigǁ_parse_file__mutmut_101': xǁBlocksScreenConfigǁ_parse_file__mutmut_101
    }
    xǁBlocksScreenConfigǁ_parse_file__mutmut_orig.__name__ = 'xǁBlocksScreenConfigǁ_parse_file'


def get_configparser() -> BlocksScreenConfig:
    args = []# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_get_configparser__mutmut_orig, x_get_configparser__mutmut_mutants, args, kwargs, None)


def x_get_configparser__mutmut_orig() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_1() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = None
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_2() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(None, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_3() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, None)
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_4() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join("BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_5() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, )
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_6() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "XXBlocksScreen.cfgXX")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_7() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "blocksscreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_8() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BLOCKSSCREEN.CFG")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_9() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = None
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_10() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(None, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_11() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, None)
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_12() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join("BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_13() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, )
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_14() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "XXBlocksScreen.cfgXX")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_15() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "blocksscreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_16() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BLOCKSSCREEN.CFG")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_17() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = None
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_18() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(None, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_19() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, None)
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_20() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path("BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_21() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, )
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_22() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "XXBlocksScreen.cfgXX")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_23() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "blocksscreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_24() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BLOCKSSCREEN.CFG")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_25() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = None
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_26() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=None, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_27() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section=None)
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_28() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_29() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, )
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_30() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="XXserverXX")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_31() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="SERVER")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_32() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_33() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section(None):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_34() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("XXserverXX"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_35() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("SERVER"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_36() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error(None)
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_37() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("XXError loading configuration file for the application.XX")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_38() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_39() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("ERROR LOADING CONFIGURATION FILE FOR THE APPLICATION.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_40() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError(None)
    return config_object


def x_get_configparser__mutmut_41() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("XXSection [server] is missing from configurationXX")
    return config_object


def x_get_configparser__mutmut_42() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("section [server] is missing from configuration")
    return config_object


def x_get_configparser__mutmut_43() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("SECTION [SERVER] IS MISSING FROM CONFIGURATION")
    return config_object

x_get_configparser__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_get_configparser__mutmut_1': x_get_configparser__mutmut_1, 
    'x_get_configparser__mutmut_2': x_get_configparser__mutmut_2, 
    'x_get_configparser__mutmut_3': x_get_configparser__mutmut_3, 
    'x_get_configparser__mutmut_4': x_get_configparser__mutmut_4, 
    'x_get_configparser__mutmut_5': x_get_configparser__mutmut_5, 
    'x_get_configparser__mutmut_6': x_get_configparser__mutmut_6, 
    'x_get_configparser__mutmut_7': x_get_configparser__mutmut_7, 
    'x_get_configparser__mutmut_8': x_get_configparser__mutmut_8, 
    'x_get_configparser__mutmut_9': x_get_configparser__mutmut_9, 
    'x_get_configparser__mutmut_10': x_get_configparser__mutmut_10, 
    'x_get_configparser__mutmut_11': x_get_configparser__mutmut_11, 
    'x_get_configparser__mutmut_12': x_get_configparser__mutmut_12, 
    'x_get_configparser__mutmut_13': x_get_configparser__mutmut_13, 
    'x_get_configparser__mutmut_14': x_get_configparser__mutmut_14, 
    'x_get_configparser__mutmut_15': x_get_configparser__mutmut_15, 
    'x_get_configparser__mutmut_16': x_get_configparser__mutmut_16, 
    'x_get_configparser__mutmut_17': x_get_configparser__mutmut_17, 
    'x_get_configparser__mutmut_18': x_get_configparser__mutmut_18, 
    'x_get_configparser__mutmut_19': x_get_configparser__mutmut_19, 
    'x_get_configparser__mutmut_20': x_get_configparser__mutmut_20, 
    'x_get_configparser__mutmut_21': x_get_configparser__mutmut_21, 
    'x_get_configparser__mutmut_22': x_get_configparser__mutmut_22, 
    'x_get_configparser__mutmut_23': x_get_configparser__mutmut_23, 
    'x_get_configparser__mutmut_24': x_get_configparser__mutmut_24, 
    'x_get_configparser__mutmut_25': x_get_configparser__mutmut_25, 
    'x_get_configparser__mutmut_26': x_get_configparser__mutmut_26, 
    'x_get_configparser__mutmut_27': x_get_configparser__mutmut_27, 
    'x_get_configparser__mutmut_28': x_get_configparser__mutmut_28, 
    'x_get_configparser__mutmut_29': x_get_configparser__mutmut_29, 
    'x_get_configparser__mutmut_30': x_get_configparser__mutmut_30, 
    'x_get_configparser__mutmut_31': x_get_configparser__mutmut_31, 
    'x_get_configparser__mutmut_32': x_get_configparser__mutmut_32, 
    'x_get_configparser__mutmut_33': x_get_configparser__mutmut_33, 
    'x_get_configparser__mutmut_34': x_get_configparser__mutmut_34, 
    'x_get_configparser__mutmut_35': x_get_configparser__mutmut_35, 
    'x_get_configparser__mutmut_36': x_get_configparser__mutmut_36, 
    'x_get_configparser__mutmut_37': x_get_configparser__mutmut_37, 
    'x_get_configparser__mutmut_38': x_get_configparser__mutmut_38, 
    'x_get_configparser__mutmut_39': x_get_configparser__mutmut_39, 
    'x_get_configparser__mutmut_40': x_get_configparser__mutmut_40, 
    'x_get_configparser__mutmut_41': x_get_configparser__mutmut_41, 
    'x_get_configparser__mutmut_42': x_get_configparser__mutmut_42, 
    'x_get_configparser__mutmut_43': x_get_configparser__mutmut_43
}
x_get_configparser__mutmut_orig.__name__ = 'x_get_configparser'
