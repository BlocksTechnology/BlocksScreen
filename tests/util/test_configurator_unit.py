"""Unit tests for BlocksScreen.tools.configuration_manager.

Tests module-level functions and ConfigManager methods using tmp_path
for all filesystem operations, no Qt dependencies needed.
"""

import configparser
import hashlib
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import threading
from unittest.mock import MagicMock, patch

import pytest

# configurator.py imports top-level packages (`from devices...`) the way the
# app runs it, with BlocksScreen/ on sys.path. Appended so the `BlocksScreen`
# package isn't shadowed by the BlocksScreen/BlocksScreen.py entry script.
_BS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "BlocksScreen")
)
if _BS_DIR not in sys.path:
    sys.path.append(_BS_DIR)

from BlocksScreen.tools.configuration_manager.configurator import (  # noqa: E402
    SV_CONFIG_MARKER,
    ConfigManager,
    check_broken_symlinks,
    copy_file_simple,
    ensure_dir,
    get_file_checksum,
    is_git_repo,
    resolve_symlink,
)


# =========================================================================
# Helpers
# =========================================================================


def _write(path: pathlib.Path, content: str) -> pathlib.Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _make_manager(tmp_path: pathlib.Path, **attrs) -> ConfigManager:
    """Create a ConfigManager bypassing the heavy __init__ side effects.

    Builds repo / config / backup dirs underneath tmp_path.
    Override any attribute via **attrs.
    """
    repo = tmp_path / "repo"
    config_dir = tmp_path / "config"
    backup = tmp_path / "backup"
    repo.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)
    backup.mkdir(parents=True, exist_ok=True)

    mock_cfg = MagicMock()
    mock_section = MagicMock()
    mock_section.get.side_effect = (
        lambda key, default="": {
            "config_repo": str(repo),
            "config_dir": str(config_dir),
            "backup_dir": str(backup),
            "variant": "RF50",
        }.get(key, default)
    )
    mock_cfg.get_section.return_value = mock_section

    inst = object.__new__(ConfigManager)
    inst.config = mock_section
    inst.mergeLock = threading.Lock()
    inst.repo = repo
    inst.config_dir = config_dir
    inst.backup_dir = backup
    inst.config_variant = "RF50"
    inst.cpy_files = ["printer.cfg", "variables.cfg", "BlocksScreen.cfg"]
    inst.repo_fi_name = {}
    inst.repo_fi_relpath = {}
    inst.config_fi_name = {}
    inst.config_fi_relpath = {}

    for k, v in attrs.items():
        setattr(inst, k, v)

    return inst


@pytest.fixture
def mock_home(tmp_path, monkeypatch):
    """Make Path.home() point inside tmp_path so relative_to(home) works."""
    home = tmp_path / "home" / "user"
    home.mkdir(parents=True)
    monkeypatch.setattr(pathlib.Path, "home", lambda _cls: home)
    return home


# =========================================================================
# Module-level helpers
# =========================================================================


class TestIsGitRepo:
    def test_not_exist(self, tmp_path):
        assert is_git_repo(tmp_path / "nope") is False

    def test_is_not_a_dir(self, tmp_path):
        f = _write(tmp_path / "file.txt", "hi")
        assert is_git_repo(f) is False

    def test_dir_no_git(self, tmp_path):
        d = tmp_path / "plain_dir"
        d.mkdir()
        assert is_git_repo(d) is False

    def test_is_git(self, tmp_path):
        d = tmp_path / "myrepo"
        d.mkdir()
        subprocess.run(["git", "init"], cwd=str(d), capture_output=True)
        assert is_git_repo(d) is True


class TestEnsureDir:
    def test_creates(self, tmp_path):
        target = tmp_path / "a" / "b"
        result = ensure_dir(target)
        assert result == target
        assert target.is_dir()

    def test_already_exists(self, tmp_path):
        target = tmp_path / "exists"
        target.mkdir()
        result = ensure_dir(target)
        assert result == target

    def test_returns_path_even_on_failure(self, tmp_path):
        target = tmp_path / "sub" / "file.txt"
        target.parent.mkdir()
        target.write_text("x")
        result = ensure_dir(target)
        assert result == target


class TestCheckBrokenSymlinks:
    def test_empty_dir(self, tmp_path):
        assert check_broken_symlinks(tmp_path) == []

    def test_no_symlinks(self, tmp_path):
        _write(tmp_path / "a.cfg", "a")
        assert check_broken_symlinks(tmp_path) == []

    def test_valid_symlink(self, tmp_path):
        real = _write(tmp_path / "real.txt", "content")
        link = tmp_path / "link.txt"
        link.symlink_to(real)
        broken = check_broken_symlinks(tmp_path)
        assert link not in broken

    def test_broken_symlink(self, tmp_path):
        link = tmp_path / "broken"
        link.symlink_to(tmp_path / "ghost")
        broken = check_broken_symlinks(tmp_path)
        assert link in broken
        assert len(broken) == 1

    def test_mixed(self, tmp_path):
        real = _write(tmp_path / "real.txt", "ok")
        valid = tmp_path / "valid_link"
        valid.symlink_to(real)
        broken = tmp_path / "broken_link"
        broken.symlink_to(tmp_path / "nowhere")
        result = check_broken_symlinks(tmp_path)
        assert valid not in result
        assert broken in result

    def test_not_exist(self, tmp_path):
        assert check_broken_symlinks(tmp_path / "ghost") == []


class TestResolveSymlink:
    def test_symlink_found(self, tmp_path):
        real = _write(tmp_path / "source.cfg", "x")
        link = tmp_path / "configs" / "source.cfg"
        link.parent.mkdir()
        link.symlink_to(real)
        assert resolve_symlink(real, link.parent) is True

    def test_symlink_not_found(self, tmp_path):
        real = tmp_path / "source.cfg"
        real.touch()
        target = tmp_path / "configs"
        target.mkdir()
        assert resolve_symlink(real, target) is False

    def test_target_not_a_dir(self, tmp_path):
        f = _write(tmp_path / "file.txt", "x")
        assert resolve_symlink(f, tmp_path / "ghost") is False

    def test_different_file_with_same_resolved_path(self, tmp_path):
        real = _write(tmp_path / "original.cfg", "content")
        deep = tmp_path / "sub" / "original.cfg"
        deep.parent.mkdir()
        deep.symlink_to(real)
        assert resolve_symlink(real, tmp_path) is True


class TestGetFileChecksum:
    def test_file_exists(self, tmp_path):
        f = _write(tmp_path / "a.cfg", "hello world")
        h = get_file_checksum(f)
        assert isinstance(h, str)
        assert len(h) == 64
        assert h == hashlib.sha256(b"hello world").hexdigest()

    def test_file_not_found(self, tmp_path):
        assert get_file_checksum(tmp_path / "ghost") == ""

    def test_identical_files_same_checksum(self, tmp_path):
        a = _write(tmp_path / "a.cfg", "same")
        b = _write(tmp_path / "b.cfg", "same")
        assert get_file_checksum(a) == get_file_checksum(b)

    def test_different_files_different_checksum(self, tmp_path):
        a = _write(tmp_path / "a.cfg", "foo")
        b = _write(tmp_path / "b.cfg", "bar")
        assert get_file_checksum(a) != get_file_checksum(b)

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.cfg"
        f.touch()
        h = get_file_checksum(f)
        assert h == hashlib.sha256(b"").hexdigest()


class TestCopyFileSimple:
    def test_copies_to_dir(self, tmp_path):
        src = _write(tmp_path / "src.cfg", "content")
        dest = tmp_path / "output"
        dest.mkdir()
        result = copy_file_simple(src, dest)
        assert (dest / "src.cfg").is_file()
        assert (dest / "src.cfg").read_text() == "content"
        assert result == str(dest / "src.cfg")

    def test_src_missing(self, tmp_path):
        src = tmp_path / "ghost.cfg"
        dest = tmp_path / "out"
        dest.mkdir()
        with pytest.raises(FileNotFoundError):
            copy_file_simple(src, dest)

    def test_copies_to_file_path(self, tmp_path):
        src = _write(tmp_path / "src.cfg", "data")
        dest = tmp_path / "output"
        dest.mkdir()
        copy_file_simple(src, dest / "renamed.cfg")
        assert (dest / "renamed.cfg").is_file()


# =========================================================================
# _build_file_index
# =========================================================================


class TestBuildFileIndex:
    def test_empty(self, tmp_path):
        mgr = _make_manager(tmp_path)
        n, r = mgr._build_file_index(tmp_path / "nonexistent")
        assert n == {}
        assert r == {}

    def test_flat_files(self, tmp_path):
        mgr = _make_manager(tmp_path)
        _write(tmp_path / "a.cfg", "a")
        _write(tmp_path / "b.cfg", "b")
        n, r = mgr._build_file_index(tmp_path)
        assert set(n.keys()) == {"a.cfg", "b.cfg"}
        assert set(r.keys()) == {"a.cfg", "b.cfg"}

    def test_subdirectory(self, tmp_path):
        mgr = _make_manager(tmp_path)
        _write(tmp_path / "sub" / "deep.cfg", "x")
        n, r = mgr._build_file_index(tmp_path)
        assert "deep.cfg" in n
        assert "sub/deep.cfg" in r

    def test_duplicate_filenames(self, tmp_path):
        mgr = _make_manager(tmp_path)
        _write(tmp_path / "a.cfg", "v1")
        _write(tmp_path / "sub" / "a.cfg", "v2")
        n, r = mgr._build_file_index(tmp_path)
        assert len(n["a.cfg"]) == 2
        assert "a.cfg" in r
        assert "sub/a.cfg" in r

    def test_ignores_git(self, tmp_path):
        mgr = _make_manager(tmp_path)
        (tmp_path / ".git").mkdir()
        _write(tmp_path / ".git" / "config", "[core]")
        _write(tmp_path / "real.cfg", "ok")
        n, r = mgr._build_file_index(tmp_path)
        assert "config" not in n
        assert "real.cfg" in n

    def test_ignores_directories(self, tmp_path):
        mgr = _make_manager(tmp_path)
        _write(tmp_path / "sub" / "file.cfg", "x")
        n, r = mgr._build_file_index(tmp_path)
        assert "sub" not in n
        assert "sub/file.cfg" in r


# =========================================================================
# _get_missing_symlinks
# =========================================================================


class TestGetMissingSymlinks:
    def test_all_present(self, tmp_path):
        mgr = _make_manager(tmp_path)
        repo = mgr.repo
        cfg_dir = mgr.config_dir
        src = _write(repo / "printer.cfg", "x")
        (cfg_dir / "printer.cfg").symlink_to(src)
        mgr.cpy_files = []
        result = mgr._get_missing_symlinks(cfg_dir, repo)
        assert result == []

    def test_some_missing(self, tmp_path):
        mgr = _make_manager(tmp_path)
        repo = mgr.repo
        cfg_dir = mgr.config_dir
        src_a = _write(repo / "a.cfg", "a")
        _write(repo / "b.cfg", "b")
        (cfg_dir / "a.cfg").symlink_to(src_a)
        mgr.cpy_files = []
        result = mgr._get_missing_symlinks(cfg_dir, repo)
        assert len(result) == 1
        assert result[0].name == "b.cfg"

    def test_none_present(self, tmp_path):
        mgr = _make_manager(tmp_path)
        repo = mgr.repo
        cfg_dir = mgr.config_dir
        _write(repo / "a.cfg", "a")
        _write(repo / "b.cfg", "b")
        mgr.cpy_files = []
        result = mgr._get_missing_symlinks(cfg_dir, repo)
        assert len(result) == 2

    def test_excludes_copy_files(self, tmp_path):
        mgr = _make_manager(tmp_path)
        repo = mgr.repo
        cfg_dir = mgr.config_dir
        _write(repo / "printer.cfg", "x")
        _write(repo / "variables.cfg", "y")
        _write(repo / "other.cfg", "z")
        mgr.cpy_files = ["printer.cfg", "variables.cfg"]
        result = mgr._get_missing_symlinks(cfg_dir, repo)
        names = [p.name for p in result]
        assert "printer.cfg" not in names
        assert "variables.cfg" not in names
        assert "other.cfg" in names

    def test_excludes_git(self, tmp_path):
        mgr = _make_manager(tmp_path)
        repo = mgr.repo
        cfg_dir = mgr.config_dir
        (repo / ".git").mkdir()
        _write(repo / ".git" / "head.cfg", "x")
        _write(repo / "real.cfg", "y")
        mgr.cpy_files = []
        result = mgr._get_missing_symlinks(cfg_dir, repo)
        assert any(p.name == "real.cfg" for p in result)
        assert not any(".git" in p.parts for p in result)

    def test_root_not_exist(self, tmp_path):
        mgr = _make_manager(tmp_path)
        repo = mgr.repo
        with pytest.raises(NotADirectoryError):
            mgr._get_missing_symlinks(tmp_path / "ghost", repo)

    def test_repo_not_exist(self, tmp_path):
        mgr = _make_manager(tmp_path)
        cfg_dir = mgr.config_dir
        with pytest.raises(NotADirectoryError):
            mgr._get_missing_symlinks(cfg_dir, tmp_path / "ghost")


# =========================================================================
# _symlink_config
# =========================================================================


class TestSymlinkConfig:
    def test_creates_symlinks(self, tmp_path, mock_home):
        mgr = _make_manager(tmp_path)
        mgr.config_dir = mock_home / "config"
        mgr.config_dir.mkdir(parents=True, exist_ok=True)
        src = _write(mock_home / "repo" / "a.cfg", "x")
        mgr._symlink_config([src])
        target = mgr.config_dir / "a.cfg"
        assert target.is_symlink()
        assert target.resolve() == src.resolve()

    def test_skips_existing_valid(self, tmp_path, mock_home):
        mgr = _make_manager(tmp_path)
        mgr.config_dir = mock_home / "config"
        mgr.config_dir.mkdir(parents=True, exist_ok=True)
        src = _write(mock_home / "repo" / "a.cfg", "x")
        existing = mgr.config_dir / "a.cfg"
        existing.symlink_to(src)
        mgr._symlink_config([src])
        assert existing.is_symlink()
        assert existing.resolve() == src.resolve()

    def test_creates_parent_dirs(self, tmp_path, mock_home):
        mgr = _make_manager(tmp_path)
        mgr.config_dir = mock_home / "config"
        mgr.config_dir.mkdir(parents=True, exist_ok=True)
        src = _write(mock_home / "repo" / "sub" / "deep.cfg", "x")
        mgr._symlink_config([src])
        target = mgr.config_dir / "sub" / "deep.cfg"
        assert target.is_symlink()
        assert target.resolve() == src.resolve()


# =========================================================================
# merge_cfg — configparser merge (no marker, variables.cfg style)
# =========================================================================


class TestMergeCfgParser:
    def test_all_options_present_no_change(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "vars.cfg", "[global]\nopt_a: 1\nopt_b: 2\n")
        tgt = _write(tmp_path / "vars_target.cfg", "[global]\nopt_a: 1\nopt_b: 2\n")
        assert mgr.merge_cfg(src, tgt) is True
        result = configparser.ConfigParser()
        result.read_string(tgt.read_text())
        assert result.get("global", "opt_a") == "1"
        assert result.get("global", "opt_b") == "2"

    def test_adds_missing_option(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "vars.cfg", "[global]\nopt_a: 1\nopt_b: 2\n")
        tgt = _write(tmp_path / "vars_target.cfg", "[global]\nopt_a: 1\n")
        assert mgr.merge_cfg(src, tgt) is True
        result = configparser.ConfigParser()
        result.read_string(tgt.read_text())
        assert result.get("global", "opt_a") == "1"
        assert result.get("global", "opt_b") == "2"

    def test_keeps_existing_value(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "vars.cfg", "[global]\nopt_a: from_repo\n")
        tgt = _write(tmp_path / "vars_target.cfg", "[global]\nopt_a: user_value\n")
        assert mgr.merge_cfg(src, tgt) is True
        result = configparser.ConfigParser()
        result.read_string(tgt.read_text())
        assert result.get("global", "opt_a") == "user_value"

    def test_multiple_sections(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(
            tmp_path / "vars.cfg",
            "[section_a]\nkey_a: repo_a\n[section_b]\nkey_b: repo_b\n",
        )
        tgt = _write(
            tmp_path / "vars_target.cfg",
            "[section_a]\nkey_a: existing_a\n",
        )
        assert mgr.merge_cfg(src, tgt) is True
        result = configparser.ConfigParser()
        result.read_string(tgt.read_text())
        assert result.get("section_a", "key_a") == "existing_a"
        assert result.get("section_b", "key_b") == "repo_b"

    def test_target_not_exist_fails(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "vars.cfg", "[g]\nk: v\n")
        tgt = tmp_path / "vars_ghost.cfg"
        assert mgr.merge_cfg(src, tgt) is False

    def test_target_empty(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "vars.cfg", "[g]\nk: v\n")
        tgt = tmp_path / "vars_target.cfg"
        tgt.parent.mkdir(parents=True, exist_ok=True)
        tgt.touch()
        assert mgr.merge_cfg(src, tgt) is True
        result = configparser.ConfigParser()
        result.read_string(tgt.read_text())
        assert result.get("g", "k") == "v"

    def test_empty_string_value(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "vars.cfg", "[g]\nk:\n")
        tgt = _write(tmp_path / "vars_target.cfg", "[g]\n")
        assert mgr.merge_cfg(src, tgt) is True
        result = configparser.ConfigParser()
        result.read_string(tgt.read_text())
        assert result.get("g", "k") == ""

    def test_src_no_sections(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "vars.cfg", "# just a comment\n")
        tgt = _write(tmp_path / "vars_target.cfg", "[g]\nk: v\n")
        assert mgr.merge_cfg(src, tgt) is True
        result = configparser.ConfigParser()
        result.read_string(tgt.read_text())
        assert result.get("g", "k") == "v"

    def test_src_empty_file(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = tmp_path / "vars.cfg"
        src.parent.mkdir(parents=True, exist_ok=True)
        src.touch()
        tgt = _write(tmp_path / "vars_target.cfg", "[g]\nk: v\n")
        assert mgr.merge_cfg(src, tgt) is True


# =========================================================================
# merge_cfg — marker-aware (printer.cfg, SAVE_CONFIG)
# =========================================================================


class TestMergeCfgMarker:
    def test_target_has_marker_preserved(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(
            tmp_path / "src_printer.cfg",
            "[stepper_x]\nstep_pin: PC2\n[extruder]\nheater_pin: PA2\n",
        )
        tgt = _write(
            tmp_path / "tgt_printer.cfg",
            "[stepper_x]\nstep_pin: PC2\n"
            + SV_CONFIG_MARKER + "\n"
            + "#*# saved_value: 123\n",
        )
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is True
        merged = tgt.read_text()
        assert "[extruder]" in merged
        assert SV_CONFIG_MARKER in merged
        assert "#*# saved_value: 123" in merged

    def test_target_no_marker_copies_source(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(
            tmp_path / "src_printer.cfg",
            "[section]\nopt: from_repo\n",
        )
        tgt = _write(
            tmp_path / "tgt_printer.cfg",
            "[section]\nopt: from_target\n",
        )
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is True
        result = configparser.ConfigParser()
        result.read_string(tgt.read_text())
        assert result.get("section", "opt") == "from_repo"

    def test_src_with_marker_target_also_with_marker(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(
            tmp_path / "src_printer.cfg",
            "[header]\nval: 1\n"
            + SV_CONFIG_MARKER + "\n"
            + "#*# repo_saved: a\n",
        )
        tgt = _write(
            tmp_path / "tgt_printer.cfg",
            "[header]\nval: 1\n"
            + SV_CONFIG_MARKER + "\n"
            + "#*# target_saved: b\n",
        )
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is True
        merged = tgt.read_text()
        assert "#*# repo_saved: a" in merged
        assert "#*# target_saved: b" in merged

    def test_marker_at_start_of_target(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "src_printer.cfg", "[header]\nval: 1\n")
        tgt = _write(
            tmp_path / "tgt_printer.cfg",
            SV_CONFIG_MARKER + "\n#*# preserved: yes\n",
        )
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is True
        merged = tgt.read_text()
        assert merged.startswith("[header]")
        assert SV_CONFIG_MARKER in merged
        assert "#*# preserved: yes" in merged

    def test_marker_only_no_save_block(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "src_printer.cfg", "[header]\nval: 1\n")
        tgt = _write(
            tmp_path / "tgt_printer.cfg",
            SV_CONFIG_MARKER + "\n",
        )
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is True
        merged = tgt.read_text()
        assert SV_CONFIG_MARKER in merged
        assert merged.strip().endswith(SV_CONFIG_MARKER)

    def test_no_marker_argument_uses_configparser(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "src.cfg", "[g]\nk: repo_val\n")
        tgt = _write(tmp_path / "tgt.cfg", "[g]\nk: tgt_val\n")
        assert mgr.merge_cfg(src, tgt) is True
        result = configparser.ConfigParser()
        result.read_string(tgt.read_text())
        assert result.get("g", "k") == "tgt_val"

    def test_marker_provided_but_target_missing_fails(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "src_printer.cfg", "[g]\nk: v\n")
        tgt = tmp_path / "tgt_ghost.cfg"
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is False

    def test_multiple_markers_first_used(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(tmp_path / "src_printer.cfg", "[header]\n")
        tgt = _write(
            tmp_path / "tgt_printer.cfg",
            "[g]\nk: v\n"
            + SV_CONFIG_MARKER + "\n"
            + "#*# a: 1\n"
            + SV_CONFIG_MARKER + "\n"
            + "#*# b: 2\n",
        )
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is True
        merged = tgt.read_text()
        idx = merged.index(SV_CONFIG_MARKER)
        after_first_marker = merged[idx:]
        assert "#*# a: 1" in after_first_marker
        assert "#*# b: 2" in after_first_marker

    def test_src_has_marker_target_does_not(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(
            tmp_path / "src_printer.cfg",
            "[header]\nval: 1\n"
            + SV_CONFIG_MARKER + "\n"
            + "#*# saved: val\n",
        )
        tgt = _write(
            tmp_path / "tgt_printer.cfg",
            "[header]\nval: 1\n",
        )
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is True
        merged = tgt.read_text()
        # target has no SAVE_CONFIG yet — copy source verbatim, preserving everything
        assert "[header]" in merged
        assert SV_CONFIG_MARKER in merged
        assert "#*# saved: val" in merged


    def test_mcu_section_preserved_from_target(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(
            tmp_path / "src_printer.cfg",
            "[stepper_x]\nstep_pin: PC2\n"
            "[mcu]\nserial: /dev/ttyACM0\n"
            "[extruder]\nheater_pin: PA2\n",
        )
        tgt = _write(
            tmp_path / "tgt_printer.cfg",
            "[stepper_x]\nstep_pin: PC2\n"
            "[mcu]\nserial: /dev/ttyACM1\n"
            "[extruder]\nheater_pin: PA2\n"
            + SV_CONFIG_MARKER + "\n"
            + "#*# saved: val\n",
        )
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is True
        merged = tgt.read_text()
        assert "[mcu]" in merged
        assert "serial: /dev/ttyACM1" in merged
        assert "serial: /dev/ttyACM0" not in merged
        assert SV_CONFIG_MARKER in merged

    def test_mcu_removed_when_missing_in_source(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(
            tmp_path / "src_printer.cfg",
            "[stepper_x]\nstep_pin: PC2\n"
            "[extruder]\nheater_pin: PA2\n",
        )
        tgt = _write(
            tmp_path / "tgt_printer.cfg",
            "[stepper_x]\nstep_pin: PC2\n"
            "[mcu pi]\nserial: /tmp/klipper_host_mcu\n"
            "[extruder]\nheater_pin: PA2\n"
            + SV_CONFIG_MARKER + "\n"
            + "#*# saved: val\n",
        )
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is True
        merged = tgt.read_text()
        assert "[mcu pi]" not in merged
        assert "/tmp/klipper_host_mcu" not in merged
        assert SV_CONFIG_MARKER in merged

    def test_multiple_mcu_sections_match_by_name(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(
            tmp_path / "src_printer.cfg",
            "[mcu]\nserial: /dev/ttyACM0\n"
            "[mcu Toolhead]\ncanbus_uuid: abc\n",
        )
        tgt = _write(
            tmp_path / "tgt_printer.cfg",
            "[mcu]\nserial: /dev/ttyACM1\n"
            "[mcu Toolhead]\ncanbus_uuid: def\n"
            "[mcu pi]\nserial: /tmp/klipper_host_mcu\n"
            + SV_CONFIG_MARKER + "\n"
            + "#*# saved: val\n",
        )
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is True
        merged = tgt.read_text()
        assert "[mcu]" in merged
        assert "[mcu Toolhead]" in merged
        assert "[mcu pi]" not in merged
        assert "serial: /dev/ttyACM1" in merged
        assert "canbus_uuid: def" in merged

    def test_mcu_preserves_all_target_options(self, tmp_path):
        mgr = _make_manager(tmp_path)
        src = _write(
            tmp_path / "src_printer.cfg",
            "[mcu]\nserial: /dev/ttyACM0\nbaud: 250000\n"
            "[mcu Toolhead]\ncanbus_uuid: 123\n",
        )
        tgt = _write(
            tmp_path / "tgt_printer.cfg",
            "[mcu]\nserial: /dev/ttyACM1\n"
            "[mcu Toolhead]\ncanbus_uuid: 456\n"
            "[mcu pi]\nserial: /tmp/klipper_host_mcu\n"
            + SV_CONFIG_MARKER + "\n"
            + "#*# saved: val\n",
        )
        assert mgr.merge_cfg(src, target_file=tgt, marker=SV_CONFIG_MARKER) is True
        merged = tgt.read_text()
        assert "[mcu]" in merged
        assert "[mcu Toolhead]" in merged
        assert "[mcu pi]" not in merged
        assert "serial: /dev/ttyACM1" in merged
        assert "serial: /dev/ttyACM0" not in merged
        assert "canbus_uuid: 456" in merged
        assert "canbus_uuid: 123" not in merged
        assert "/tmp/klipper_host_mcu" not in merged


# =========================================================================
# _cpy_cfg_files
# =========================================================================


class TestCpyCfgFiles:
    def test_no_cpy_files_returns_immediately(self, tmp_path):
        mgr = _make_manager(tmp_path, cpy_files=[])
        mgr._cpy_cfg_files()

    def test_file_not_in_repo_skipped(self, tmp_path, caplog):
        caplog.set_level(logging.INFO)
        mgr = _make_manager(tmp_path, cpy_files=["missing.cfg"])
        mgr.repo_fi_name = {}
        mgr._cpy_cfg_files()
        assert "not exist in repository" in caplog.text

    def test_file_not_in_config_copied(self, tmp_path, mock_home):
        mgr = _make_manager(tmp_path, cpy_files=["printer.cfg"])
        mgr.config_dir = mock_home / "config"
        mgr.config_dir.mkdir(parents=True, exist_ok=True)
        src = _write(mgr.repo / "printer.cfg", "content")
        # The method uses relative_to(home) — put repo under home too
        home = mock_home
        mgr.repo = home / "repo"
        mgr.repo.mkdir(parents=True, exist_ok=True)
        src = _write(mgr.repo / "printer.cfg", "content")
        mgr.repo_fi_name = {"printer.cfg": [src]}
        mgr.config_fi_name = {}
        mgr._cpy_cfg_files()
        target = mgr.config_dir / "printer.cfg"
        assert target.is_file()
        assert target.read_text() == "content"

    def test_file_identical_skipped(self, tmp_path):
        mgr = _make_manager(tmp_path, cpy_files=["printer.cfg"])
        src = _write(mgr.repo / "printer.cfg", "same")
        tgt = _write(mgr.config_dir / "printer.cfg", "same")
        mgr.repo_fi_name = {"printer.cfg": [src]}
        mgr.config_fi_name = {"printer.cfg": [tgt]}
        mgr._cpy_cfg_files()
        assert tgt.read_text() == "same"

    def test_printer_cfg_differs_merge_called(self, tmp_path):
        mgr = _make_manager(tmp_path, cpy_files=["printer.cfg"])
        src = _write(mgr.repo / "printer.cfg", "[header]\nopt: repo\n")
        tgt = _write(
            mgr.config_dir / "printer.cfg",
            "[header]\nopt: target\n"
            + SV_CONFIG_MARKER + "\n"
            + "#*# user: saved\n",
        )
        mgr.repo_fi_name = {"printer.cfg": [src]}
        mgr.config_fi_name = {"printer.cfg": [tgt]}
        mgr._cpy_cfg_files()
        merged = tgt.read_text()
        assert "[header]" in merged
        assert SV_CONFIG_MARKER in merged
        assert "#*# user: saved" in merged

    def test_variables_cfg_differs_merge_called(self, tmp_path):
        mgr = _make_manager(tmp_path, cpy_files=["variables.cfg"])
        src = _write(mgr.repo / "variables.cfg", "[g]\nopt_a: repo\nopt_b: repo\n")
        tgt = _write(mgr.config_dir / "variables.cfg", "[g]\nopt_a: existing\n")
        mgr.repo_fi_name = {"variables.cfg": [src]}
        mgr.config_fi_name = {"variables.cfg": [tgt]}
        mgr._cpy_cfg_files()
        result = configparser.ConfigParser()
        result.read_string(tgt.read_text())
        assert result.get("g", "opt_a") == "existing"
        assert result.get("g", "opt_b") == "repo"


# =========================================================================
# sync — smoke test
# =========================================================================


class TestSync:
    def test_sync_roundtrip(self, tmp_path, mock_home):
        mgr = _make_manager(tmp_path)
        mgr.config_dir = mock_home / "config"
        mgr.config_dir.mkdir(parents=True, exist_ok=True)
        mgr.repo = mock_home / "repo"
        mgr.repo.mkdir(parents=True, exist_ok=True)
        _write(mgr.repo / "printer.cfg", "[g]\nk: repo\n")
        _write(mgr.repo / "other.cfg", "[g]\no: v\n")
        mgr.repo_fi_name, mgr.repo_fi_relpath = mgr._build_file_index(mgr.repo)
        mgr.config_fi_name, mgr.config_fi_relpath = mgr._build_file_index(
            mgr.config_dir
        )
        mgr.sync()

    def test_sync_handles_missing_repo(self, tmp_path, caplog):
        caplog.set_level(logging.ERROR)
        mgr = _make_manager(tmp_path)
        mgr.repo = tmp_path / "ghost_repo"
        mgr.sync()
        assert len(caplog.records) > 0
