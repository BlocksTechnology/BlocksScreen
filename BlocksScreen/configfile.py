# Config file helper
#
# Copyright (C) 2020 Eric Callahan <arksine.code@gmail.com>
# Copyright (C) 2025 Hugo Costa <h.costa@blockstec.com>
#
# Based on the work of Eric Callahan:
# https://github.com/Arksine/moonraker/blob/master/moonraker/confighelper.py
#
# This file is distributed under the terms of the GNU General Public License v3.
# See https://www.gnu.org/licenses/gpl-3.0.html for details.

from __future__ import annotations
import configparser
import enum
import os
import pathlib
import re
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


class BlocksScreenConfig:
    config = configparser.ConfigParser(
        allow_no_value=True,
        interpolation=configparser.ExtendedInterpolation(),
        delimiters=(":"),
        # inline_comment_prefixes=("#"),
        comment_prefixes=("#", "#~#"),
        empty_lines_in_values=True,
    )

    def __init__(
        self, configfile: typing.Union[str, pathlib.Path], section: str
    ) -> None:
        self.configfile = pathlib.Path(configfile)
        self.section = section
        self.raw_config: typing.List[str] = []

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
        default: typing.Union[Sentinel, str] = Sentinel.MISSING,
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

    def load_config(self):
        try:
            self.raw_config.clear()
            self.config.clear()  # Reset the configparser

            self.raw_config = self._parse_file()
            if self.raw_config:
                self.config.read_file(self.raw_config)
        except Exception as e:
            raise configparser.Error(f"Error loading configuration file: {e}")

    def _parse_file(self) -> typing.List[str]:
        buffer = []
        dict_buff: typing.Dict = {}
        curr_sec: typing.Union[Sentinel, str] = Sentinel.MISSING
        try:
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
                line = re.sub(r"=", ":", line)
                # find the beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    sec_name = re.sub(r"[\[*\]]", r"", line)
                    if sec_name not in dict_buff.keys():
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
            return buffer
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            )
