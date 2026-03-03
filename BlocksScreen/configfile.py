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


class Sentinel(enum.Enum):
    """Sentinel value to signify missing condition, absence of value"""

    MISSING = object


class ConfigError(Exception):
    """Exception raised when Configfile errors exist"""

    def __init__(self, msg) -> None:
        """Store the error message on both the exception and the ``msg`` attribute."""
        super().__init__(msg)
        self.msg = msg


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
        """Initialise with the path to the config file and the default section name."""
        self.configfile = pathlib.Path(configfile)
        self.section = section
        self.raw_config: typing.List[str] = []
        self.raw_dict_config: typing.Dict = {}
        self.file_lock = threading.Lock()  # Thread safety for future work

    def __getitem__(self, key: str) -> BlocksScreenConfig:
        """Return a :class:`BlocksScreenConfig` for *key* section (same as ``get_section``)."""
        return self.get_section(key)

    def __contains__(self, key):
        """Return True if *key* is a section in the underlying ConfigParser."""
        return key in self.config

    def sections(self) -> typing.List[str]:
        """Returns list of all sections"""
        return self.config.sections()

    def get_section(
        self, section: str, fallback: typing.Optional[T] = None
    ) -> BlocksScreenConfig:
        """Get configfile section"""
        if not self.config.has_section(section):
            raise configparser.NoSectionError(f"No section with name: {section}")
        return BlocksScreenConfig(self.configfile, section)

    def get_options(self) -> list:
        """Get section options"""
        return self.config.options(self.section)

    def has_section(self, section: str) -> bool:
        """Check if config file has a section

        Args:
            section (str): section name

        Returns:
            bool: true if section exists, false otherwise
        """
        return bool(self.config.has_section(section))

    def has_option(self, option: str) -> bool:
        """Check if section has a option

        Args:
            option (str): option name

        Returns:
            bool: true if section exists, false otherwise
        """
        return bool(self.config.has_option(self.section, option))

    def get(
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

    def getint(
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

    def getfloat(
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

    def getboolean(
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

    def _find_section_index(self, section: str) -> int:
        """Return the index of the ``[section]`` header line in ``raw_config``."""
        try:
            return self.raw_config.index("[" + section + "]")
        except ValueError as e:
            raise configparser.Error(f'Section "{section}" does not exist: {e}')

    def _find_section_limits(self, section: str) -> typing.Tuple:
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

    def _find_option_index(
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

    def add_section(self, section: str) -> None:
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

    def add_option(
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

    def update_option(
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
            logging.error(
                f'Unable to update option "{option}" in section "{section}": {e}'
            )

    def _find_option_line_index(self, section: str, option: str) -> int:
        """Find the index of an option line within a specific section."""
        start, end = self._find_section_limits(section)
        opt_regex = re.compile(rf"^\s*{re.escape(option)}\s*[:=]")
        for i in range(start + 1, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def save_configuration(self) -> None:
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

    def load_config(self):
        """Load configuration file"""
        try:
            self.raw_config.clear()
            self.config.clear()  # Reset configparser
            self.raw_config, self.raw_dict_config = self._parse_file()
            if self.raw_config:
                self.config.read_file(self.raw_config)
        except Exception as e:
            raise configparser.Error(f"Error loading configuration file: {e}")

    def _parse_file(self) -> typing.Tuple[typing.List[str], typing.Dict]:
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


def get_configparser() -> BlocksScreenConfig:
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
