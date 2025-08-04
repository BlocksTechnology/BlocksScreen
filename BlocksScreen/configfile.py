# Config file helper
#
# Copyright (C) 2025 Hugo Costa <h.costa@blockstec.com>
#
# Based on the work of Eric Callahan <arksine.code@gmail.com>
# https://github.com/Arksine/moonraker/blob/master/moonraker/confighelper.py
#
# This file may be distributed under the terms of GNU GPLv3 license

import configparser
import enum
import hashlib
import io
import logging
import os
import pathlib
import re
import typing

from helper_methods import *  # check_filepath_permission, check_path_existence

HOME_DIR = os.path.expanduser("~/")
WORKING_DIR = os.getcwd()
DEFAULT_CONFIGFILE_PATH = pathlib.Path(HOME_DIR, "printer_data", "config")
FALLBACK_CONFIGFILE_PATH = pathlib.Path(WORKING_DIR)

T = typing.TypeVar("T")


class Sentinel(enum.Enum):
    # Add Sentinel because `None` can
    # actually be a valid value for an option
    MISSING = object


error = configparser.Error
parsing_error = configparser.ParsingError
no_option_error = configparser.NoOptionError
no_section_error = configparser.NoSectionError
alien_error = configparser.ParsingError


class BlocksScreenConfig:
    def __init__(self, configfile) -> None:
        self.config = configparser.ConfigParser(
            allow_no_value=True, interpolation=None
        )
        self.configfile = pathlib.Path(configfile)
        self.load_config()

    def __getitem__(self, key):
        if not self.config.has_section(key):
            raise no_section_error(f"No section named {key}")

        return BlocksScreenConfig(self.configfile)

    def __contains__(self, key):
        return key in self.config

    def load_config(self):
        try:
            self.config.clear()  # Reset the configparser
            f = self._parse_file()
            if f is not None:
                self.config.read_file(f)
        except (configparser.DuplicateSectionError, configparser.Error):
            return

    def _parse_file(self):
        buffer = []
        sections = []
        options = []
        try:
            f = self.configfile.read_text(encoding="utf-8")
            for line in f.splitlines():
                line = line.strip()
                if not line:
                    continue
                line.expandtabs(4)
                re_match = re.search(r"\s*#\s*(.*)(\s*)", line)
                if re_match:
                    line = line[: re_match.start()]
                    if not line:
                        continue
                # remove leading and trailing white spaces
                line = re.sub(r"\s*([:=])\s*", r"\1", line)
                # find beginning of sections
                section_match = re.compile(r"[^\s]*\[([^]]+)\]")
                match_sec = re.match(section_match, line)  #
                if match_sec:
                    if line not in sections:
                        sections.append(line)
                    else:
                        continue  # Ignore duplicate sections
                option_match = re.compile(r"[:=]")
                match_opt = re.split(option_match, line)[0]
                if match_opt:
                    if match_opt not in options:
                        options.append(match_opt)
                    else:
                        continue  # Ignore duplicate options
                buffer.append(line)
            return buffer
        except Exception as e:
            raise error(
                f"Unexpected error while parsing configuration file: {e}"
            )

    def get(
        self,
        option,
        default: typing.Optional[typing.Union[Sentinel, T]] = Sentinel.MISSING,
    ) -> T: ...

    def getint(
        self,
        option,
        default: typing.Optional[typing.Union[Sentinel, T]] = Sentinel.MISSING,
    ) -> int: ...

    def getfloat(
        self,
        option,
        default: typing.Optional[typing.Union[Sentinel, T]] = Sentinel.MISSING,
    ) -> float: ...

    def getboolean(
        self,
        option,
        default: typing.Optional[typing.Union[Sentinel, T]] = Sentinel.MISSING,
    ) -> bool: ...


def get_configparser() -> BlocksScreenConfig:
    wanted_target = os.path.join(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
    fallback = os.path.join(WORKING_DIR, "BlocksScreen.cfg")
    configfile = (
        wanted_target
        if check_file_on_path(DEFAULT_CONFIGFILE_PATH, "BlocksScreen.cfg")
        else fallback
    )
    return BlocksScreenConfig(configfile=configfile)


if __name__ == "__main__":
    config = get_configparser()
