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

HOME_DIR = os.path.expanduser("~/")
WORKING_DIR = os.getcwd()
DEFAULT_CONFIGFILE_PATH = pathlib.Path(HOME_DIR, "printer_data", "config")
FALLBACK_CONFIGFILE_PATH = pathlib.Path(WORKING_DIR)

T = typing.TypeVar("T")
indentation_size = 4


class Sentinel(enum.Enum):
    MISSING = object


class ConfigError(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
        self.msg = msg


class BlocksScreenConfig:
    config = configparser.ConfigParser(
        allow_no_value=True,
        # interpolation=configparser.ExtendedInterpolation(),
        # delimiters=(":"),
        # inline_comment_prefixes=("#"),
        # comment_prefixes=("#", "#~#"),
        # empty_lines_in_values=True,
    )

    update_pending: bool = False

    _instance = None

    # def __new__(
    #     cls, *args, **kwargs
    # ) -> BlocksScreenConfig:  # Singleton pattern
    #     if not cls._instance:
    #         cls._instance = super(BlocksScreenConfig, cls).__new__(cls)
    #     return cls._instance

    def __init__(
        self, configfile: typing.Union[str, pathlib.Path], section: str
    ) -> None:
        self.configfile = pathlib.Path(configfile)
        self.section = section
        self.raw_config: typing.List[str] = []
        self.raw_dict_config: typing.Dict = {}
        self.file_lock = threading.Lock()  # Thread safety for future work

    def __getitem__(self, key: str) -> BlocksScreenConfig:
        return self.get_section(key)

    def __contains__(self, key):
        return key in self.config

    def sections(self) -> typing.List[str]:
        return self.config.sections()

    def get_section(
        self, section: str, fallback: typing.Optional[T] = None
    ) -> BlocksScreenConfig:
        if not self.config.has_section(section):
            raise configparser.NoSectionError(
                f"No section with name: {section}"
            )
        return BlocksScreenConfig(self.configfile, section)

    def get_options(self) -> list:
        return self.config.options(self.section)

    def has_section(self, section: str) -> bool:
        return bool(self.config.has_section(section))

    def has_option(self, option: str) -> bool:
        return bool(self.config.has_option(self.section, option))

    def get(
        self,
        option: str,
        parser: type = str,
        default: typing.Union[Sentinel, str, T] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, str]:
        return parser(
            self.config.get(
                section=self.section, option=option, fallback=default
            )
        )

    def getint(
        self,
        option: str,
        default: typing.Union[Sentinel, int] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, int]:
        return self.config.getint(
            section=self.section, option=option, fallback=default
        )

    def getfloat(
        self,
        option: str,
        default: typing.Union[Sentinel, float] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, float]:
        return self.config.getfloat(
            section=self.section, option=option, fallback=default
        )

    def getboolean(
        self,
        option: str,
        default: typing.Union[Sentinel, bool] = Sentinel.MISSING,
    ) -> typing.Union[Sentinel, bool]:
        return self.config.getboolean(
            section=self.section, option=option, fallback=default
        )

    def _find_section_index(self, section: str) -> int:
        try:
            return self.raw_config.index("[" + section + "]")
        except ValueError as e:
            raise configparser.Error(
                f'Section "{section}" does not exist: {e}'
            )

    def _find_section_limits(self, section: str) -> typing.Tuple:
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
            logging.error(f'Section "{section}" already exists. {e}')
        except configparser.Error as e:
            logging.error(
                f'Unable to add "{section}" section to configuration: {e}'
            )

    def add_option(
        self,
        section: str,
        option: str,
        value: typing.Union[str, None] = None,
    ) -> None:
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
            logging.error(f"Option {option} already present on {section}: {e}")
        except configparser.Error as e:
            logging.error(
                f'Unable to add "{option}" option to section "{section}": {e} '
            )

    def save_configuration(self) -> None:
        try:
            if not self.update_pending:
                return
            with self.file_lock:
                self.configfile.write_text(
                    "\n".join(self.raw_config), encoding="utf-8"
                )
                sio = io.StringIO()
                sio.writelines(self.raw_config)
                self.config.write(sio)
                sio.close()
        except Exception as e:
            logging.error(
                f"ERROR: Unable to save new configuration, something went wrong while saving updated configuration. {e}"
            )
        finally:
            self.update_pending = False


    def load_config(self):
        try:
            self.raw_config.clear()
            self.config.clear()  # Reset configparser
            self.raw_config, self.raw_dict_config = self._parse_file()
            if self.raw_config:
                self.config.read_file(self.raw_config)
        except Exception as e:
            raise configparser.Error(f"Error loading configuration file: {e}")

    def _parse_file(self) -> typing.Tuple[typing.List[str], typing.Dict]:
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
                line = re.sub(r"\s*([:=])\s*", r"\1", line)
                line = re.sub(r"=", r":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
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
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    try:
        config_object = BlocksScreenConfig(
            configfile=configfile, section="server"
        )
        config_object.load_config()
        if not config_object.has_section("server"):
            raise ConfigError("Section [server] is missing from configuration")
    except ConfigError:
        logging.error("Error loading configuration file for the application.")
    return BlocksScreenConfig(configfile=configfile, section="server")
