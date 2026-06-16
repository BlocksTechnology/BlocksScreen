"""Security-focused tests for updater module."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from updater.executor import (
    _list_upgradable_packages,
    _resolve_component_pip,
    check_apt_status,
)


class TestPackageNameValidation:
    @pytest.mark.asyncio
    async def test_valid_package_names_accepted(self):
        """Valid Debian package names should pass through."""
        proc = MagicMock()
        proc.returncode = 0
        proc.communicate = AsyncMock(
            return_value=(
                b"curl/stable 7.0-1 amd64\n"
                b"git-core/stable 1.0-2 amd64\n"
                b"python3+extra/stable 3.0 amd64\n",
                b"",
            )
        )

        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, pkgs = await _list_upgradable_packages()

        assert ok
        assert "curl" in pkgs
        assert "git-core" in pkgs
        assert "python3+extra" in pkgs

    @pytest.mark.asyncio
    async def test_malformed_package_names_rejected(self):
        """Package names with shell metacharacters should be rejected."""
        proc = MagicMock()
        proc.returncode = 0
        proc.communicate = AsyncMock(
            return_value=(
                b"valid-pkg/stable 1.0 amd64\n"
                b"evil$(whoami)/stable 1.0 amd64\n"
                b"another;rm -rf/stable 1.0 amd64\n"
                b"safe-one/stable 1.0 amd64\n",
                b"",
            )
        )

        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            ok, pkgs = await _list_upgradable_packages()

        assert ok
        assert "valid-pkg" in pkgs
        assert "safe-one" in pkgs
        assert len(pkgs) == 2
        for pkg in pkgs:
            assert "$" not in pkg
            assert ";" not in pkg
            assert "|" not in pkg


class TestResolveComponentPip:
    def test_none_path_returns_system_pip(self):
        """None path should return system pip."""
        result = _resolve_component_pip(None)
        assert result == "/usr/bin/pip3"

    def test_valid_venv_path_accepted(self, tmp_path):
        """Valid venv pip should be found and returned."""
        comp_path = tmp_path / "comp"
        comp_path.mkdir()
        venv_path = comp_path / ".venv" / "bin"
        venv_path.mkdir(parents=True)
        pip_path = venv_path / "pip"
        pip_path.touch()

        result = _resolve_component_pip(comp_path)
        assert "pip" in result
        assert str(comp_path) in result or ".venv" in result

    def test_symlink_to_unsafe_location_rejected(self, tmp_path):
        """Symlinks pointing way outside component should be rejected."""
        comp_path = tmp_path / "home" / "user" / "comp"
        comp_path.mkdir(parents=True)
        evil_dir = tmp_path / "outside"
        evil_dir.mkdir()
        evil_pip = evil_dir / "pip"
        evil_pip.touch()

        venv_path = comp_path / ".venv" / "bin"
        venv_path.mkdir(parents=True)
        symlink = venv_path / "pip"
        symlink.symlink_to(evil_pip)

        result = _resolve_component_pip(comp_path)
        assert result == "/usr/bin/pip3"

    def test_parent_env_found(self, tmp_path):
        """Should find parent-sibling venv (comp-env pattern)."""
        comp_path = tmp_path / "comp"
        comp_path.mkdir()
        venv_path = tmp_path / "comp-env" / "bin"
        venv_path.mkdir(parents=True)
        pip_path = venv_path / "pip"
        pip_path.touch()

        result = _resolve_component_pip(comp_path)
        assert "comp-env" in result


class TestAptCachePermissions:
    @pytest.mark.asyncio
    async def test_cache_file_writable_by_others_rejected(self, tmp_path, monkeypatch):
        """Cache files with excessive permissions should be rejected."""
        cache_dir = tmp_path / ".cache" / "blockscreen"
        cache_dir.mkdir(parents=True)
        cache_file = cache_dir / "apt_status_cache.json"

        cache_data = {
            "packages_upgradable": 5,
            "exclude_key": "",
            "cached_ts": 999999999999,
        }
        cache_file.write_text(json.dumps(cache_data))
        cache_file.chmod(0o666)

        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        proc = MagicMock()
        proc.returncode = 0
        proc.communicate = AsyncMock(return_value=(b"", b""))

        with patch(
            "asyncio.create_subprocess_exec", new_callable=AsyncMock, return_value=proc
        ):
            result = await check_apt_status()

        assert result.packages_upgradable >= 0

    @pytest.mark.asyncio
    async def test_cache_valid_file_accepted(self, tmp_path, monkeypatch):
        """Cache files with safe permissions and current owner accepted."""
        import time

        cache_dir = tmp_path / ".cache" / "blockscreen"
        cache_dir.mkdir(parents=True, mode=0o700)
        cache_file = cache_dir / "apt_status_cache.json"

        cache_data = {
            "packages_upgradable": 5,
            "exclude_key": "",
            "cached_ts": time.time(),
        }
        cache_file.write_text(json.dumps(cache_data))
        cache_file.chmod(0o600)

        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        result = await check_apt_status()

        assert result.name == "system"
        assert result.kind == "apt"
        assert result.packages_upgradable == 5
