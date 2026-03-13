"""Unit tests for BlocksScreen/configfile.py

Covers: parsing, read methods, get_section views, add/update/save, get_configparser factory,
comment handling, and thread-safety (RLock reentrancy).
"""

from __future__ import annotations

import configparser
import logging
import pathlib
import sys
import textwrap
import threading

import pytest

# configfile.py lives in BlocksScreen/ and imports helper_methods from the same dir;
# both resolve when BlocksScreen/ is on sys.path.
_BLOCKSSCREEN = pathlib.Path(__file__).parent.parent.parent / "BlocksScreen"
if str(_BLOCKSSCREEN) not in sys.path:
    sys.path.insert(0, str(_BLOCKSSCREEN))

# tests/network/conftest.py installs a mock at sys.modules["configfile"] for network
# tests. Popping it here is safe — network modules already bound the mock's symbols
# at their own import time and won't re-import.
sys.modules.pop("configfile", None)

import configfile as cfmod  # noqa: E402
from configfile import BlocksScreenConfig, ConfigError, Sentinel, get_configparser  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_cfg(tmp_path: pathlib.Path, content: str, section: str = "server") -> BlocksScreenConfig:
    """Write *content* to a temp file, load it, and return the config object."""
    cfg_file = tmp_path / "test.cfg"
    cfg_file.write_text(textwrap.dedent(content).strip(), encoding="utf-8")
    cfg = BlocksScreenConfig(cfg_file, section)
    cfg.load_config()
    return cfg


# ---------------------------------------------------------------------------
# Sentinel
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSentinel:
    def test_missing_value_is_an_instance_not_the_class(self):
        assert Sentinel.MISSING.value is not object
        assert isinstance(Sentinel.MISSING.value, object)

    def test_missing_is_an_enum_member(self):
        assert isinstance(Sentinel.MISSING, Sentinel)


# ---------------------------------------------------------------------------
# Parsing (_parse_file via load_config)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParsing:
    def test_basic_section_and_option(self, tmp_path):
        cfg = _make_cfg(tmp_path, """
            [server]
            host: localhost
        """)
        assert cfg.has_section("server")
        assert cfg.get("host") == "localhost"

    def test_equals_separator_normalised_to_colon(self, tmp_path):
        cfg = _make_cfg(tmp_path, """
            [server]
            host = localhost
        """)
        assert cfg.get("host") == "localhost"

    def test_full_line_hash_comment_ignored(self, tmp_path):
        cfg = _make_cfg(tmp_path, """
            # this is a comment
            [server]
            host: localhost
        """)
        assert cfg.has_section("server")
        assert not cfg.has_section("# this is a comment")

    def test_full_line_semicolon_comment_ignored(self, tmp_path):
        cfg = _make_cfg(tmp_path, """
            ; this is also a comment
            [server]
            host: localhost
        """)
        assert cfg.has_section("server")
        assert not cfg.has_section("; this is also a comment")

    def test_inline_hash_comment_stripped(self, tmp_path):
        cfg = _make_cfg(tmp_path, """
            [server]
            host: localhost  # inline comment
        """)
        assert cfg.get("host") == "localhost"

    def test_inline_semicolon_comment_stripped(self, tmp_path):
        cfg = _make_cfg(tmp_path, """
            [server]
            host: localhost  ; inline comment
        """)
        assert cfg.get("host") == "localhost"

    def test_hash_in_value_without_leading_space_preserved(self, tmp_path):
        """#ff0000 has no space before # so must not be stripped as a comment."""
        cfg = _make_cfg(tmp_path, """
            [server]
            color: #ff0000
        """)
        assert cfg.get("color") == "#ff0000"

    def test_duplicate_section_uses_first_occurrence(self, tmp_path):
        cfg = _make_cfg(tmp_path, """
            [server]
            host: first
            [server]
            host: second
        """)
        assert cfg.get("host") == "first"

    def test_duplicate_option_uses_first_occurrence(self, tmp_path):
        cfg = _make_cfg(tmp_path, """
            [server]
            host: first
            host: second
        """)
        assert cfg.get("host") == "first"

    def test_multiple_sections_all_loaded(self, tmp_path):
        cfg = _make_cfg(tmp_path, """
            [server]
            host: localhost
            [display]
            width: 800
        """)
        assert cfg.has_section("server")
        assert cfg.has_section("display")

    def test_raw_config_always_ends_with_empty_line(self, tmp_path):
        cfg = _make_cfg(tmp_path, """
            [server]
            host: localhost
        """)
        assert cfg.raw_config[-1] == ""

    def test_load_config_resets_previous_state(self, tmp_path):
        cfg_file = tmp_path / "test.cfg"
        cfg_file.write_text("[server]\nhost: localhost\n", encoding="utf-8")
        cfg = BlocksScreenConfig(cfg_file, "server")
        cfg.load_config()
        assert cfg.get("host") == "localhost"

        cfg_file.write_text("[server]\nhost: remotehost\n", encoding="utf-8")
        cfg.load_config()
        assert cfg.get("host") == "remotehost"

    def test_value_with_embedded_colon_preserved(self, tmp_path):
        """Values containing ':' after the key separator must not be mangled (e.g. URLs)."""
        cfg = _make_cfg(tmp_path, """
            [server]
            url: http://localhost:7125
        """)
        assert cfg.get("url") == "http://localhost:7125"

    def test_value_with_embedded_equals_preserved(self, tmp_path):
        """Values containing '=' after the key separator must not be mangled (e.g. tokens)."""
        cfg = _make_cfg(tmp_path, """
            [server]
            token: abc=def==ghi
        """)
        assert cfg.get("token") == "abc=def==ghi"

    def test_section_name_with_colon_preserved(self, tmp_path):
        """Section names containing ':' must not be mangled by separator normalisation."""
        cfg = _make_cfg(tmp_path, """
            [fan:heater_fan]
            pin: PA8
        """, section="fan:heater_fan")
        assert cfg.has_section("fan:heater_fan")
        assert cfg.get("pin") == "PA8"


# ---------------------------------------------------------------------------
# Read methods (get, getint, getfloat, getboolean, sections, get_options)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestReadMethods:
    @pytest.fixture
    def cfg(self, tmp_path):
        return _make_cfg(tmp_path, """
            [server]
            host: localhost
            port: 7125
            ratio: 1.5
            enabled: true
        """)

    def test_has_section_present(self, cfg):
        assert cfg.has_section("server") is True

    def test_has_section_absent(self, cfg):
        assert cfg.has_section("missing") is False

    def test_has_option_present(self, cfg):
        assert cfg.has_option("host") is True

    def test_has_option_absent(self, cfg):
        assert cfg.has_option("missing") is False

    def test_get_returns_string(self, cfg):
        assert cfg.get("host") == "localhost"

    def test_get_returns_default_when_absent(self, cfg):
        assert cfg.get("missing", default="fallback") == "fallback"

    def test_get_with_int_parser(self, cfg):
        assert cfg.get("port", parser=int) == 7125

    def test_get_with_bool_parser_false_value(self, tmp_path):
        """get(parser=bool) must not treat 'false' as True (bool('false') pitfall)."""
        cfg = _make_cfg(tmp_path, """
            [server]
            host: localhost
            flag: false
        """)
        assert cfg.get("flag", parser=bool) is False

    def test_get_with_bool_parser_true_value(self, tmp_path):
        cfg = _make_cfg(tmp_path, """
            [server]
            host: localhost
            flag: true
        """)
        assert cfg.get("flag", parser=bool) is True

    def test_getint(self, cfg):
        assert cfg.getint("port") == 7125

    def test_getint_default_when_absent(self, cfg):
        assert cfg.getint("missing", default=42) == 42

    def test_getfloat(self, cfg):
        assert cfg.getfloat("ratio") == pytest.approx(1.5)

    def test_getfloat_default_when_absent(self, cfg):
        assert cfg.getfloat("missing", default=0.5) == pytest.approx(0.5)

    def test_getboolean_true(self, cfg):
        assert cfg.getboolean("enabled") is True

    def test_getboolean_default_when_absent(self, cfg):
        assert cfg.getboolean("missing", default=False) is False

    def test_sections_returns_list_of_names(self, cfg):
        assert "server" in cfg.sections()

    def test_get_options_returns_option_names(self, cfg):
        opts = cfg.get_options()
        assert "host" in opts
        assert "port" in opts

    def test_get_default_returned_as_is_not_parsed(self, cfg):
        """When the option is absent the default is returned without passing through parser.
        Previously parser(default) was called — int('N/A') would raise ValueError."""
        result = cfg.get("missing", parser=int, default="N/A")
        assert result == "N/A"

    def test_getint_raises_when_absent_no_default(self, cfg):
        """getint() with no default must raise, not silently return Sentinel.MISSING."""
        with pytest.raises((configparser.NoOptionError, configparser.NoSectionError)):
            cfg.getint("missing")

    def test_getfloat_raises_when_absent_no_default(self, cfg):
        """getfloat() with no default must raise, not silently return Sentinel.MISSING."""
        with pytest.raises((configparser.NoOptionError, configparser.NoSectionError)):
            cfg.getfloat("missing")

    def test_getboolean_raises_when_absent_no_default(self, cfg):
        """getboolean() with no default must raise, not silently return Sentinel.MISSING."""
        with pytest.raises((configparser.NoOptionError, configparser.NoSectionError)):
            cfg.getboolean("missing")


# ---------------------------------------------------------------------------
# get_section / __getitem__ / __contains__
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetSection:
    @pytest.fixture
    def cfg(self, tmp_path):
        return _make_cfg(tmp_path, """
            [server]
            host: localhost
            [display]
            width: 800
        """)

    def test_view_reads_actual_values(self, cfg):
        view = cfg.get_section("server")
        assert view is not None
        assert view.get("host") == "localhost"

    def test_view_shares_the_configparser_instance(self, cfg):
        view = cfg.get_section("display")
        assert view.config is cfg.config

    def test_view_uses_correct_section(self, cfg):
        view = cfg.get_section("display")
        assert view.section == "display"
        assert view.getint("width") == 800

    def test_returns_none_when_section_missing(self, cfg):
        assert cfg.get_section("nonexistent") is None

    def test_returns_custom_fallback_when_section_missing(self, cfg):
        sentinel = object()
        assert cfg.get_section("nonexistent", fallback=sentinel) is sentinel

    def test_getitem_returns_working_view(self, cfg):
        view = cfg["server"]
        assert view is not None
        assert view.get("host") == "localhost"

    def test_getitem_returns_none_for_missing_section(self, cfg):
        assert cfg["nonexistent"] is None

    def test_contains_returns_true_for_existing_section(self, cfg):
        assert "server" in cfg

    def test_contains_returns_false_for_missing_section(self, cfg):
        assert "nonexistent" not in cfg

    def test_view_raw_config_stays_valid_after_reload(self, tmp_path):
        """load_config must update raw_config in-place so existing views remain valid."""
        cfg_file = tmp_path / "test.cfg"
        cfg_file.write_text("[server]\nhost: first\n[display]\nwidth: 800\n", encoding="utf-8")
        cfg = BlocksScreenConfig(cfg_file, "server")
        cfg.load_config()
        view = cfg.get_section("display")
        assert view is not None
        assert view.raw_config is cfg.raw_config  # same list object

        # Reload with new content — view must reflect the updated list
        cfg_file.write_text("[server]\nhost: second\n[display]\nwidth: 1024\n", encoding="utf-8")
        cfg.load_config()
        assert view.raw_config is cfg.raw_config  # still the same list object
        assert any("1024" in line for line in view.raw_config)


# ---------------------------------------------------------------------------
# add_section
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAddSection:
    @pytest.fixture
    def cfg(self, tmp_path):
        return _make_cfg(tmp_path, """
            [server]
            host: localhost
        """)

    def test_section_becomes_visible_after_add(self, cfg):
        cfg.add_section("display")
        assert cfg.has_section("display")

    def test_section_header_appears_in_raw_config(self, cfg):
        cfg.add_section("display")
        assert "[display]" in cfg.raw_config

    def test_sets_update_pending(self, cfg):
        cfg.add_section("display")
        assert cfg.update_pending is True

    def test_raw_config_ends_with_empty_line_after_add(self, cfg):
        cfg.add_section("display")
        assert cfg.raw_config[-1] == ""

    def test_duplicate_section_logs_error_not_raises(self, cfg, caplog):
        with caplog.at_level(logging.ERROR):
            cfg.add_section("server")  # already exists
        assert "already exists" in caplog.text.lower()

    def test_duplicate_section_does_not_raise(self, cfg):
        cfg.add_section("server")  # must not propagate an exception


# ---------------------------------------------------------------------------
# add_option
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAddOption:
    @pytest.fixture
    def cfg(self, tmp_path):
        return _make_cfg(tmp_path, """
            [server]
            host: localhost
        """)

    def test_option_becomes_visible_after_add(self, cfg):
        cfg.add_option("server", "port", "7125")
        assert cfg.has_option("port")

    def test_added_option_is_readable(self, cfg):
        cfg.add_option("server", "port", "7125")
        assert cfg.getint("port") == 7125

    def test_option_line_appears_in_raw_config(self, cfg):
        cfg.add_option("server", "port", "7125")
        assert any("port: 7125" in line for line in cfg.raw_config)

    def test_sets_update_pending(self, cfg):
        cfg.add_option("server", "port", "7125")
        assert cfg.update_pending is True

    def test_option_inserted_before_section_separator(self, cfg):
        cfg.add_option("server", "port", "7125")
        port_idx = next(i for i, l in enumerate(cfg.raw_config) if "port" in l)
        assert cfg.raw_config[port_idx + 1] == ""

    def test_none_value_writes_valueless_option_line(self, cfg):
        """add_option(value=None) must write 'flag:' not 'flag: None'."""
        cfg.add_option("server", "flag", None)
        assert not any("None" in line for line in cfg.raw_config)
        assert any(line.strip() == "flag:" for line in cfg.raw_config)

    def test_none_value_option_is_readable(self, cfg):
        """Value-less options must be detectable via has_option after add."""
        cfg.add_option("server", "flag", None)
        assert cfg.has_option("flag")


# ---------------------------------------------------------------------------
# update_option
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestUpdateOption:
    @pytest.fixture
    def cfg(self, tmp_path):
        return _make_cfg(tmp_path, """
            [server]
            host: localhost
            port: 7125
        """)

    def test_updates_existing_option_value(self, cfg):
        cfg.update_option("server", "host", "remotehost")
        assert cfg.get("host") == "remotehost"

    def test_updated_value_reflected_in_raw_config(self, cfg):
        cfg.update_option("server", "host", "remotehost")
        assert any("host: remotehost" in line for line in cfg.raw_config)

    def test_old_value_absent_from_raw_config(self, cfg):
        cfg.update_option("server", "host", "remotehost")
        assert not any("host: localhost" in line for line in cfg.raw_config)

    def test_sets_update_pending(self, cfg):
        cfg.update_option("server", "host", "remotehost")
        assert cfg.update_pending is True

    def test_creates_missing_option(self, cfg):
        cfg.update_option("server", "timeout", "30")
        assert cfg.get("timeout") == "30"

    def test_creates_missing_section_and_option(self, cfg):
        cfg.update_option("display", "width", "800")
        assert cfg.has_section("display")
        view = cfg.get_section("display")
        assert view.get("width") == "800"

    def test_reentrancy_does_not_deadlock(self, tmp_path):
        """update_option calls add_section/add_option while holding the RLock — must not deadlock."""
        cfg = _make_cfg(tmp_path, "[server]\nhost: localhost\n")
        cfg.update_option("brandnew", "key", "value")
        assert cfg.has_section("brandnew")
        assert cfg.get_section("brandnew").get("key") == "value"


# ---------------------------------------------------------------------------
# save_configuration
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSaveConfiguration:
    def test_writes_updated_value_to_file(self, tmp_path):
        cfg_file = tmp_path / "test.cfg"
        cfg_file.write_text("[server]\nhost: localhost\n", encoding="utf-8")
        cfg = BlocksScreenConfig(cfg_file, "server")
        cfg.load_config()
        cfg.update_option("server", "host", "newhost")
        cfg.save_configuration()
        assert "host: newhost" in cfg_file.read_text(encoding="utf-8")

    def test_clears_update_pending_after_save(self, tmp_path):
        cfg_file = tmp_path / "test.cfg"
        cfg_file.write_text("[server]\nhost: localhost\n", encoding="utf-8")
        cfg = BlocksScreenConfig(cfg_file, "server")
        cfg.load_config()
        cfg.update_option("server", "host", "newhost")
        cfg.save_configuration()
        assert cfg.update_pending is False

    def test_skips_write_when_not_pending(self, tmp_path):
        original = "[server]\nhost: localhost\n"
        cfg_file = tmp_path / "test.cfg"
        cfg_file.write_text(original, encoding="utf-8")
        cfg = BlocksScreenConfig(cfg_file, "server")
        cfg.load_config()
        assert cfg.update_pending is False
        cfg.save_configuration()
        assert cfg_file.read_text(encoding="utf-8") == original

    def test_pending_preserved_when_write_fails(self, tmp_path):
        """A failed write must leave update_pending True so the caller can retry."""
        cfg_file = tmp_path / "test.cfg"
        cfg_file.write_text("[server]\nhost: localhost\n", encoding="utf-8")
        cfg = BlocksScreenConfig(cfg_file, "server")
        cfg.load_config()
        cfg.update_pending = True
        cfg.configfile = pathlib.Path("/nonexistent_dir/file.cfg")
        cfg.save_configuration()
        assert cfg.update_pending is True


# ---------------------------------------------------------------------------
# get_configparser factory
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetConfigparser:
    def test_loads_from_fallback_path(self, tmp_path, monkeypatch):
        cfg_file = tmp_path / "BlocksScreen.cfg"
        cfg_file.write_text("[server]\nhost: localhost\n", encoding="utf-8")

        monkeypatch.setattr(cfmod, "DEFAULT_CONFIGFILE_PATH", tmp_path / "nonexistent")
        monkeypatch.setattr(cfmod, "FALLBACK_CONFIGFILE_PATH", tmp_path)

        cfg = get_configparser()
        assert cfg.has_section("server")

    def test_raises_config_error_when_server_section_missing(self, tmp_path, monkeypatch):
        cfg_file = tmp_path / "BlocksScreen.cfg"
        cfg_file.write_text("[display]\nwidth: 800\n", encoding="utf-8")

        monkeypatch.setattr(cfmod, "DEFAULT_CONFIGFILE_PATH", tmp_path / "nonexistent")
        monkeypatch.setattr(cfmod, "FALLBACK_CONFIGFILE_PATH", tmp_path)

        with pytest.raises(ConfigError, match=r"\[server\]"):
            get_configparser()


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestThreadSafety:
    def test_concurrent_updates_do_not_corrupt_state(self, tmp_path):
        cfg_file = tmp_path / "test.cfg"
        cfg_file.write_text("[server]\nhost: localhost\n", encoding="utf-8")
        cfg = BlocksScreenConfig(cfg_file, "server")
        cfg.load_config()

        errors: list[Exception] = []

        def updater(value: str) -> None:
            try:
                cfg.update_option("server", "host", value)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=updater, args=(f"host{i}",)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert cfg.has_option("host")


# ---------------------------------------------------------------------------
# Bug fixes (regression tests)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEdgeCases:
    def test_parse_empty_file_does_not_crash(self, tmp_path):
        """Empty (or comment-only) file must not raise IndexError."""
        cfg_file = tmp_path / "test.cfg"
        cfg_file.write_text("# only a comment\n", encoding="utf-8")
        cfg = BlocksScreenConfig(cfg_file, "server")
        cfg.load_config()  # must not raise
        assert cfg.raw_config == [""]

    def test_parse_completely_empty_file_does_not_crash(self, tmp_path):
        cfg_file = tmp_path / "test.cfg"
        cfg_file.write_text("", encoding="utf-8")
        cfg = BlocksScreenConfig(cfg_file, "server")
        cfg.load_config()
        assert cfg.raw_config == [""]

    def test_get_missing_option_without_default_raises(self, tmp_path):
        """get() with no default must raise NoOptionError, not silently return Sentinel.MISSING."""
        cfg = _make_cfg(tmp_path, "[server]\nhost: localhost\n")
        with pytest.raises(configparser.NoOptionError):
            cfg.get("nonexistent")

    def test_load_config_missing_file_raises(self, tmp_path):
        """load_config on a non-existent file must raise configparser.Error, not crash silently."""
        cfg = BlocksScreenConfig(tmp_path / "nonexistent.cfg", "server")
        with pytest.raises(configparser.Error):
            cfg.load_config()

    def test_save_configuration_toctou_safe(self, tmp_path):
        """update_pending check and file write happen atomically under the lock."""
        cfg_file = tmp_path / "test.cfg"
        cfg_file.write_text("[server]\nhost: localhost\n", encoding="utf-8")
        cfg = BlocksScreenConfig(cfg_file, "server")
        cfg.load_config()
        cfg.update_option("server", "host", "newhost")

        errors: list[Exception] = []

        def saver() -> None:
            try:
                cfg.save_configuration()
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=saver) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert "host: newhost" in cfg_file.read_text(encoding="utf-8")
