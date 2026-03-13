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
import logging
import pathlib
import re
import threading
from typing import Any

from helper_methods import check_file_on_path

logger = logging.getLogger(__name__)

DEFAULT_CONFIGFILE_PATH = pathlib.Path.home() / "printer_data" / "config"
FALLBACK_CONFIGFILE_PATH = pathlib.Path.cwd()

_RE_SECTION = re.compile(r"^\s*\[([^]]+)\]")
_RE_OPTION = re.compile(r"^(\w+)[=:]")
_RE_INLINE_COMMENT = re.compile(r"(?<=\w)\s+[#;]")
_RE_SEP_NORMALIZE = re.compile(r"\s*[:=]\s*")


class Sentinel(enum.Enum):
    """Sentinel value to signify missing condition, absence of value"""

    MISSING = object()


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

    def __init__(self, configfile: str | pathlib.Path, section: str) -> None:
        """Initialise with the path to the config file and the default section name."""
        self.configfile = pathlib.Path(configfile)
        self.section = section
        self.config = configparser.ConfigParser(
            allow_no_value=True,
            comment_prefixes=("#", ";"),
            inline_comment_prefixes=None,  # handled manually in _parse_file
        )
        self.update_pending: bool = False
        self.raw_config: list[str] = []
        # RLock: update_option calls add_section/add_option while holding the lock
        self.file_lock = threading.RLock()

    def __getitem__(self, key: str) -> BlocksScreenConfig | None:
        """Return a :class:`BlocksScreenConfig` for *key* section (same as ``get_section``)."""
        return self.get_section(key)

    def __contains__(self, key: str) -> bool:
        """Return True if *key* is a section in the underlying ConfigParser."""
        return key in self.config

    def sections(self) -> list[str]:
        """Returns list of all sections"""
        return self.config.sections()

    def get_section(
        self, section: str, fallback: BlocksScreenConfig | None = None
    ) -> BlocksScreenConfig | None:
        """Return a section-scoped view sharing this instance's parsed ConfigParser.

        The returned view's read methods (get, has_option, getint, …) operate on
        the same data as the parent.  Write operations (add_option, update_option,
        save_configuration) should still be called on the root object.
        """
        if not self.config.has_section(section):
            return fallback
        view = BlocksScreenConfig(self.configfile, section)
        view.config = self.config  # share — reads see the actual parsed data
        view.raw_config = self.raw_config  # share — _find_section_* helpers work
        view.file_lock = self.file_lock  # share — thread safety consistent
        return view

    def get_options(self) -> list[str]:
        """Get section options"""
        return self.config.options(self.section)

    def has_section(self, section: str) -> bool:
        """Check if config file has a section

        Args:
            section (str): section name

        Returns:
            bool: true if section exists, false otherwise
        """
        return self.config.has_section(section)

    def has_option(self, option: str) -> bool:
        """Check if section has a option

        Args:
            option (str): option name

        Returns:
            bool: true if section exists, false otherwise
        """
        return self.config.has_option(self.section, option)

    def get(
        self,
        option: str,
        parser: type = str,
        default: Any = Sentinel.MISSING,
    ) -> Any:
        """Get option value.

        Args:
            option (str): option name
            parser (type, optional): int, float, or str. Defaults to str.
                Do **not** pass ``bool`` — use :meth:`getboolean` instead.
                ``get(parser=bool)`` is intercepted and delegated to
                ``getboolean`` to avoid the ``bool("false") == True`` pitfall.
            default: Returned as-is when the option is absent.
                Defaults to Sentinel.MISSING (raises if option not found).

        Returns:
            Any: Parsed option value, or *default* if the option is absent.
        """
        if parser is bool:
            return self.getboolean(option, default=default)
        try:
            return parser(self.config.get(section=self.section, option=option))
        except (configparser.NoOptionError, configparser.NoSectionError):
            if default is Sentinel.MISSING:
                raise
            return default

    def getint(
        self,
        option: str,
        default: Sentinel | int = Sentinel.MISSING,
    ) -> int:
        """Get option value as int.

        Args:
            option (str): option name
            default (int, optional): returned as-is when absent. Raises if omitted.

        Returns:
            int: parsed value, or *default* if absent.
        """
        if default is Sentinel.MISSING:
            return self.config.getint(section=self.section, option=option)
        return self.config.getint(section=self.section, option=option, fallback=default)

    def getfloat(
        self,
        option: str,
        default: Sentinel | float = Sentinel.MISSING,
    ) -> float:
        """Get option value as float.

        Args:
            option (str): option name
            default (float, optional): returned as-is when absent. Raises if omitted.

        Returns:
            float: parsed value, or *default* if absent.
        """
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
        """Get option value as bool.

        Args:
            option (str): option name
            default (bool, optional): returned as-is when absent. Raises if omitted.

        Returns:
            bool: parsed value, or *default* if absent.
        """
        if default is Sentinel.MISSING:
            return self.config.getboolean(section=self.section, option=option)
        return self.config.getboolean(
            section=self.section, option=option, fallback=default
        )

    def _find_section_index(self, section: str) -> int:
        """Return the index of the ``[section]`` header line in ``raw_config``."""
        try:
            return self.raw_config.index(f"[{section}]")
        except ValueError as e:
            raise configparser.Error(f'Section "{section}" does not exist: {e}')

    def _find_section_limits(self, section: str) -> tuple[int, int]:
        """Return ``(start_index, end_index)`` of *section* in ``raw_config``."""
        try:
            section_start = self._find_section_index(section)
            buffer = self.raw_config[section_start:]
            section_end = buffer.index("")
            return (section_start, section_end + section_start)
        except (configparser.Error, ValueError) as e:
            raise configparser.Error(
                f'Error while finding section "{section}" limits on local tracking: {e}'
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
                if self.raw_config and self.raw_config[-1].strip() != "":
                    self.raw_config.append("")
                self.raw_config.extend([sec_string, ""])
                self.config.add_section(section)
                self.update_pending = True
        except configparser.DuplicateSectionError as e:
            logger.error('Section "%s" already exists. %s', section, e)
        except configparser.Error as e:
            logger.error('Unable to add "%s" section to configuration: %s', section, e)

    def add_option(
        self,
        section: str,
        option: str,
        value: str | None = None,
    ) -> None:
        """Add option with a value to a section.

        Args:
            section (str): section name
            option (str): option name
            value (str | None, optional): value for the option. ``None`` writes
                a value-less option (``allow_no_value=True``). Defaults to None.
        """
        try:
            with self.file_lock:
                _, section_end = self._find_section_limits(section)
                raw_line = f"{option}: {value}" if value is not None else f"{option}:"
                self.raw_config.insert(section_end, raw_line)
                self.config.set(section, option, value)
                self.update_pending = True
        except configparser.DuplicateOptionError as e:
            logger.error("Option %s already present on %s: %s", option, section, e)
        except configparser.Error as e:
            logger.error(
                'Unable to add "%s" option to section "%s": %s', option, section, e
            )

    def update_option(
        self,
        section: str,
        option: str,
        value: Any,
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
                'Unable to update option "%s" in section "%s": %s',
                option,
                section,
                e,
                exc_info=True,
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
        """Save the configuration to file.

        ``update_pending`` is only cleared on a successful write so that a
        caller can detect a failed save and retry.
        """
        try:
            with self.file_lock:
                if not self.update_pending:
                    return
                self.configfile.write_text("\n".join(self.raw_config), encoding="utf-8")
                self.update_pending = False
        except Exception as e:
            logger.error(
                "Unable to save configuration to %s: %s",
                self.configfile,
                e,
                exc_info=True,
            )

    def load_config(self) -> None:
        """Load configuration file.

        Updates ``raw_config`` in-place so that existing section-view objects
        (which share the same list reference) remain valid after a reload.
        """
        try:
            new_raw = self._parse_file()  # can raise without corrupting state
            self.config.clear()
            self.raw_config.clear()
            self.raw_config.extend(new_raw)
            if self.raw_config:
                self.config.read_file(self.raw_config)
        except Exception as e:
            raise configparser.Error(f"Error loading configuration file: {e}") from e

    def _parse_file(self) -> list[str]:
        """Read and normalise the config file into a raw line list.

        Strips comments, normalises only the **first** ``=``/``:`` separator
        to ``: `` (preserving values that contain colons, e.g. URLs or hex
        colours), deduplicates sections/options, and ensures the buffer ends
        with an empty line.

        Returns:
            Normalised list of config lines.
        """
        buffer: list[str] = []
        seen: dict[str, set[str]] = {}  # section → set of seen option names
        curr_sec: str | None = None
        try:
            with self.file_lock:
                text = self.configfile.read_text(encoding="utf-8")
            for raw in text.splitlines():
                line = raw.strip()
                if not line or line.startswith(("#", ";")):
                    continue
                # Strip inline comments (delimiter must be preceded by a word char,
                # so values like `color: #ff0000` are not affected).
                m = _RE_INLINE_COMMENT.search(line)
                if m:
                    line = line[: m.start()].rstrip()
                    if not line:
                        continue

                # --- Section header ---
                # Checked before separator normalisation so that a colon inside
                # a section name (e.g. `[a:b]`) is never mangled.
                m_sec = _RE_SECTION.match(line)
                if m_sec:
                    sec_name = m_sec.group(1)
                    if sec_name in seen:
                        continue  # duplicate section — skip
                    if buffer:
                        buffer.append("")  # blank separator before each new section
                    seen[sec_name] = set()
                    curr_sec = sec_name
                    buffer.append(line)
                    continue  # header fully handled — do not try to parse as option

                # --- Option line ---
                # Normalise only the *first* separator so that values containing
                # additional ':' or '=' characters (URLs, tokens, regex …) are
                # preserved verbatim.
                line = _RE_SEP_NORMALIZE.sub(": ", line, count=1)
                m_opt = _RE_OPTION.match(line)
                if m_opt and curr_sec is not None:
                    opt_name = m_opt.group(1)
                    if opt_name in seen[curr_sec]:
                        continue  # duplicate option — skip
                    seen[curr_sec].add(opt_name)
                    buffer.append(line)
                # Lines matching neither pattern are silently dropped
                # (they cannot be round-tripped through configparser anyway).

            if not buffer or buffer[-1] != "":
                buffer.append("")
            return buffer
        except Exception as e:
            raise configparser.Error(
                f"Unexpected error while parsing configuration file: {e}"
            ) from e


def get_configparser() -> BlocksScreenConfig:
    """Loads configuration from file and returns that configuration"""
    wanted_target = DEFAULT_CONFIGFILE_PATH / "BlocksScreen.cfg"
    fallback = FALLBACK_CONFIGFILE_PATH / "BlocksScreen.cfg"
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
