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

"""Klipper-style access to BlocksScreen.cfg."""

from __future__ import annotations

import configparser
import copy
import enum
import functools
import logging
import os
import pathlib
import re
import stat
import tempfile
import threading
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_CONFIGFILE_PATH = pathlib.Path.home() / "printer_data" / "config"
FALLBACK_CONFIGFILE_PATH = pathlib.Path.cwd()
_DEFAULT_CONFIG = DEFAULT_CONFIGFILE_PATH / "BlocksScreen.cfg"
_FALLBACK_CONFIG = FALLBACK_CONFIGFILE_PATH / "BlocksScreen.cfg"

_singleton_lock = threading.Lock()

_RE_SECTION = re.compile(r"^\[([^]]+)\]")
_RE_SEP = re.compile(r"\s*[:=]\s*")
# Moonraker rule: whitespace + '#'/';' starts a comment, a backslash escapes it
_RE_INLINE_COMMENT = re.compile(r"\s+[#;].*$")
_RE_ESCAPE = re.compile(r"(\s)([#;])")
_RE_UNESCAPE = re.compile(r"(\s)\\([#;])")


class Sentinel(enum.Enum):
    """Marks an absent default."""

    MISSING = object()


class ConfigError(Exception):
    """Raised when the configuration file is unusable."""

    def __init__(self, msg: str) -> None:
        """Store *msg* on the exception and as ``msg``."""
        super().__init__(msg)
        self.msg = msg


def _option_line(option: str, value: str | None) -> str:
    """Build an ``option: value`` line, escaping comment chars so it round-trips."""
    if value is None:
        return f"{option}:"
    if "\n" in value or "\r" in value:
        raise ValueError(f'value for "{option}" must be a single line')
    escaped = _RE_ESCAPE.sub(r"\1\\\2", value)
    return f"{option}: {escaped}".rstrip()


def _atomic_write(path: pathlib.Path, text: str) -> None:
    """Write through a temp file and rename so a power cut never truncates *path*."""
    target = path.resolve()  # keep a symlinked config pointing at its target
    fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.")
    tmp_path = pathlib.Path(tmp)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        if target.exists():
            tmp_path.chmod(stat.S_IMODE(target.stat().st_mode))  # mkstemp makes 0600
        tmp_path.replace(target)
    finally:
        tmp_path.unlink(missing_ok=True)


class BlocksScreenConfig:
    """Thread-safe ConfigParser wrapper that mirrors the file in ``raw_config``."""

    def __init__(self, configfile: str | pathlib.Path, section: str) -> None:
        """Bind to *configfile*, reading options from *section*."""
        self.configfile = pathlib.Path(configfile)
        self.section = section
        self.config = configparser.ConfigParser(
            allow_no_value=True,
            interpolation=None,  # as Klipper/Moonraker: '%' in values is literal
            comment_prefixes=("#", ";"),
            inline_comment_prefixes=None,  # stripped in _parse_file
            delimiters=(":",),
        )
        self.update_pending: bool = False
        self.raw_config: list[str] = []
        # RLock: update_option calls add_section/add_option while holding it
        self.file_lock = threading.RLock()

    def __getitem__(self, key: str) -> BlocksScreenConfig | None:
        """Return the view for section *key*, or None."""
        return self.get_section(key)

    def __contains__(self, key: str) -> bool:
        """Return True if *key* is a section."""
        return key in self.config

    def sections(self) -> list[str]:
        """Return all section names."""
        return self.config.sections()

    def get_section(
        self, section: str, fallback: BlocksScreenConfig | None = None
    ) -> BlocksScreenConfig | None:
        """Return a view of *section* sharing this parser; call writes on the root."""
        if not self.config.has_section(section):
            return fallback
        view = copy.copy(self)
        view.section = section
        return view

    def get_options(self) -> list[str]:
        """Return the option names of this section."""
        return self.config.options(self.section)

    def has_section(self, section: str) -> bool:
        """Return True if *section* exists."""
        return self.config.has_section(section)

    def has_option(self, option: str) -> bool:
        """Return True if *option* exists in this section."""
        return self.config.has_option(self.section, option)

    def get(
        self,
        option: str,
        parser: type = str,
        default: Any = Sentinel.MISSING,
    ) -> Any:
        """Return *option* cast by *parser*; *default* comes back unparsed."""
        if parser is bool:
            # bool("false") is True
            return self.getboolean(option, default=default)
        try:
            return parser(self.config.get(section=self.section, option=option))
        except (configparser.NoOptionError, configparser.NoSectionError):
            if default is Sentinel.MISSING:
                raise
            return default

    def getlists(
        self,
        option: str,
        default: Sentinel | list[Any] = Sentinel.MISSING,
        sep: str | tuple[str, ...] = ",",
        parser: type = str,
    ) -> list[Any]:
        """Return *option* split on *sep*, cast by *parser*; empty gives *default*."""
        raw = self.config.get(section=self.section, option=option, fallback=None)
        if not raw:
            return [] if default is Sentinel.MISSING else default
        seps = (sep,) if isinstance(sep, str) else sep
        items = re.split("|".join(map(re.escape, seps)), raw)
        return [parser(item.strip()) for item in items if item.strip()]

    def getint(
        self,
        option: str,
        default: Sentinel | int = Sentinel.MISSING,
    ) -> int:
        """Return *option* as int; *default* when absent, else raise."""
        if default is Sentinel.MISSING:
            return self.config.getint(section=self.section, option=option)
        return self.config.getint(section=self.section, option=option, fallback=default)

    def getfloat(
        self,
        option: str,
        default: Sentinel | float = Sentinel.MISSING,
    ) -> float:
        """Return *option* as float; *default* when absent, else raise."""
        if default is Sentinel.MISSING:
            return self.config.getfloat(section=self.section, option=option)
        return self.config.getfloat(
            section=self.section, option=option, fallback=default
        )

    def getboolean(
        self,
        option: str,
        default: Sentinel | bool = Sentinel.MISSING,
    ) -> bool:
        """Return *option* as bool; *default* when absent, else raise."""
        if default is Sentinel.MISSING:
            return self.config.getboolean(section=self.section, option=option)
        return self.config.getboolean(
            section=self.section, option=option, fallback=default
        )

    def _find_section_index(self, section: str) -> int:
        """Return the index of the ``[section]`` line in ``raw_config``."""
        try:
            return self.raw_config.index(f"[{section}]")
        except ValueError as e:
            raise configparser.Error(f'Section "{section}" does not exist') from e

    def _find_section_limits(self, section: str) -> tuple[int, int]:
        """Return ``(header, closing_blank)`` indexes of *section* in ``raw_config``."""
        try:
            start = self._find_section_index(section)
            return start, self.raw_config.index("", start)
        except (configparser.Error, ValueError) as e:
            raise configparser.Error(f'Cannot locate section "{section}": {e}') from e

    def add_section(self, section: str) -> None:
        """Add an empty *section*; logs instead of raising when it exists."""
        try:
            with self.file_lock:
                self.config.add_section(section)
                if self.raw_config and self.raw_config[-1]:
                    self.raw_config.append("")
                self.raw_config.extend([f"[{section}]", ""])
                self.update_pending = True
        except (configparser.Error, ValueError) as e:
            logger.error('Unable to add section "%s": %s', section, e)

    def add_option(
        self,
        section: str,
        option: str,
        value: str | None = None,
    ) -> None:
        """Add *option* to *section*; None writes a value-less ``option:`` line."""
        try:
            with self.file_lock:
                if self.config.has_option(section, option):
                    raise configparser.DuplicateOptionError(section, option)
                line = _option_line(option, value)
                _, end = self._find_section_limits(section)
                self.config.set(section, option, value)
                self.raw_config.insert(end, line)
                self.update_pending = True
        except (configparser.Error, ValueError) as e:
            logger.error(
                'Unable to add option "%s" to section "%s": %s', option, section, e
            )

    def update_option(
        self,
        section: str,
        option: str,
        value: Any,
    ) -> None:
        """Set *option* in *section*, creating either when missing."""
        try:
            with self.file_lock:
                if not self.config.has_section(section):
                    self.add_section(section)
                if not self.config.has_option(section, option):
                    self.add_option(section, option, str(value))
                    return
                line = _option_line(option, str(value))
                idx = self._find_option_line_index(section, option)
                self.config.set(section, option, str(value))
                self.raw_config[idx] = line
                self.update_pending = True
        except (configparser.Error, ValueError) as e:
            logger.error(
                'Unable to update option "%s" in section "%s": %s', option, section, e
            )

    def _find_option_line_index(self, section: str, option: str) -> int:
        """Return the ``raw_config`` index of *option* inside *section*."""
        start, end = self._find_section_limits(section)
        # optionxform lowercases keys, so match the file's spelling case-insensitively
        opt_regex = re.compile(rf"^{re.escape(option)}(?::|$)", re.IGNORECASE)
        for i in range(start + 1, end):
            if opt_regex.match(self.raw_config[i]):
                return i
        raise configparser.Error(f'Option "{option}" not found in section "{section}"')

    def save_configuration(self) -> None:
        """Write ``raw_config`` atomically; ``update_pending`` stays set on failure."""
        try:
            with self.file_lock:
                if not self.update_pending:
                    return
                _atomic_write(self.configfile, "\n".join(self.raw_config))
                self.update_pending = False
        except OSError as e:
            logger.error(
                "Unable to save configuration to %s: %s",
                self.configfile,
                e,
                exc_info=True,
            )

    def load_config(self) -> None:
        """(Re)load the file, updating ``raw_config`` in place so views stay valid."""
        try:
            new_raw = self._parse_file()
            self.config.clear()
            self.config.read_file(_RE_UNESCAPE.sub(r"\1\2", ln) for ln in new_raw)
            self.raw_config[:] = new_raw
        except (OSError, ValueError, configparser.Error) as e:
            raise configparser.Error(f"Error loading configuration file: {e}") from e

    def _parse_file(self) -> list[str]:
        """Read the file into normalised lines, one blank-ended block per section."""
        with self.file_lock:
            text = self.configfile.read_text(encoding="utf-8")
        blocks: dict[str | None, list[str]] = {None: []}
        opt_index: dict[tuple[str, str], int] = {}
        pending: list[str] = []  # full-line comments, kept with the next line
        sec: str | None = None
        for lineno, line in enumerate(map(str.strip, text.splitlines()), 1):
            if not line:
                continue
            if line[0] in "#;":
                pending.append(line)
                continue
            # before separator handling so '[fan:x]' keeps its colon
            if m_sec := _RE_SECTION.match(line):
                sec = m_sec.group(1)
                if sec in blocks:
                    blocks[sec].extend(pending)  # Klipper merges repeated sections
                else:
                    blocks[sec] = [*pending, f"[{sec}]"]
                pending = []
                continue
            name, *rest = _RE_SEP.split(line, maxsplit=1)
            name = _RE_INLINE_COMMENT.sub("", name)
            if sec is None or not name:
                logger.warning(
                    "%s:%d ignored: no section or option name", self.configfile, lineno
                )
                continue
            opt = name
            if rest:
                # on the value alone, so 'color: #ff0000' is not a comment
                value = _RE_INLINE_COMMENT.sub("", rest[0])
                opt = f"{name}: {value}" if value else f"{name}:"
            block = blocks[sec]
            block.extend(pending)
            pending = []
            key = (sec, self.config.optionxform(name))
            if key in opt_index:
                block[opt_index[key]] = opt  # Klipper: the last duplicate wins
            else:
                opt_index[key] = len(block)
                block.append(opt)
        blocks[sec].extend(pending)
        return [ln for block in blocks.values() if block for ln in (*block, "")] or [""]


@functools.cache
def _load_singleton() -> BlocksScreenConfig:
    """Build the process-wide config; raises are not cached, so callers can retry."""
    configfile = _DEFAULT_CONFIG if _DEFAULT_CONFIG.exists() else _FALLBACK_CONFIG
    config_object = BlocksScreenConfig(configfile=configfile, section="server")
    config_object.load_config()
    if not config_object.has_section("server"):
        logger.error("Error loading configuration file for the application.")
        raise ConfigError("Section [server] is missing from configuration")
    return config_object


def get_configparser() -> BlocksScreenConfig:
    """Return the singleton config, loading it on first call."""
    # functools.cache alone can build twice when two threads race the first call
    with _singleton_lock:
        return _load_singleton()


def reset_configparser() -> None:
    """Drop the singleton; tests only."""
    with _singleton_lock:
        _load_singleton.cache_clear()
