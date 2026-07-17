"""Unit tests for updater.components"""

import sys
import logging
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from updater.components import load_components

BUNDLE_YAML = """
poll_interval_minutes: 1440
components:
  - name: klipper
    type: git
    path: ~/klipper
    service: klipper.service
    reset_mode: hard
    order: 1
  - name: blockscreen
    type: git
    path: ~/BlocksScreen
    service: BlocksScreen.service
    reset_mode: hard
    order: 99
"""

OVERRIDE_YAML = """
components:
    - name: klipper
      path: ~/costum_klipper
    - name: my-plugin
      type: git
      path: ~/my-plugin
      service: my-plugin.service
      reset_mode: hard
      order: 5
"""


def _mock_load(bundled: str, override: str | None = None):
    import updater.components as mod

    bundled_path = Path(mod.__file__).parent / "components.yaml"

    def fake_open(path, *a, **kw):
        if Path(path) == bundled_path:
            return mock_open(read_data=bundled)()
        if override is not None:
            return mock_open(read_data=override)()
        raise FileNotFoundError(path)

    return fake_open


class TestLoadComponents:
    def test_load_return_sorted_by_order(self):
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML)),
            patch("pathlib.Path.exists", return_value=False),
            patch("pathlib.Path.is_dir", return_value=True),
        ):
            components, poll = load_components()
        names = [c.name for c in components]
        assert names.index("klipper") < names.index("blockscreen")

    def test_load_components_returns_poll_interval(self):
        """load_components() second element is poll interval in seconds."""
        with patch("builtins.open", mock_open(read_data=BUNDLE_YAML)):
            _, poll = load_components()
        assert poll == 1440 * 60.0  # 1440 minutes → seconds

    def test_missing_override_file_silently_ignored(self):
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML)),
            patch("pathlib.Path.exists", return_value=False),
            patch("pathlib.Path.is_dir", return_value=True),
        ):
            components, poll = load_components()
        assert len(components) >= 2

    def test_override_permission_error_skipped(self, caplog):
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML)),
            patch("pathlib.Path.exists", side_effect=PermissionError("denied")),
            patch("pathlib.Path.is_dir", return_value=True),
            caplog.at_level(logging.WARNING, logger="updater.components"),
        ):
            components, poll = load_components()
        assert len(components) >= 2
        assert any("Cannot access override path" in r.message for r in caplog.records)

    def test_autoinjected_system_apt_has_kernel_guard(self):
        # No apt component in YAML -> auto-injected 'system' keeps the guard.
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML)),
            patch("pathlib.Path.exists", return_value=False),
            patch("pathlib.Path.is_dir", return_value=True),
        ):
            components, _ = load_components()
        apt = next(c for c in components if c.kind == "apt")
        assert apt.apt_exclude == (
            "^linux-image",
            "^linux-headers",
            "^raspberrypi-",
            "^firmware-",
        )

    def test_configured_apt_without_exclude_still_guards_kernel(self):
        # Brick guard: an override apt component omitting apt_exclude must not lift the kernel exclusion.
        override = "components:\n  - name: system\n    type: apt\n    order: 1\n"
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML, override)),
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat", return_value=self._safe_stat_mock()),
            patch("pathlib.Path.is_dir", return_value=True),
        ):
            components, _ = load_components()
        apt = next(c for c in components if c.kind == "apt")
        for pat in ("^linux-image", "^linux-headers", "^raspberrypi-", "^firmware-"):
            assert pat in apt.apt_exclude

    def _safe_stat_mock(self):
        mock_stat = MagicMock()
        mock_stat.st_mode = 0o100600
        return mock_stat


class TestYamlMerge:
    def _safe_stat_mock(self):
        """Return a mock stat result for safe (owner-only) file permissions."""
        mock_stat = MagicMock()
        mock_stat.st_mode = 0o100600  # Regular file, owner-only
        return mock_stat

    def test_overrides_path_by_name(self):
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML, OVERRIDE_YAML)),
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat", return_value=self._safe_stat_mock()),
            patch("pathlib.Path.is_dir", return_value=True),
        ):
            components, poll = load_components()
        klipper = next(c for c in components if c.name == "klipper")
        assert str(klipper.path).endswith("costum_klipper")
        assert klipper.service == "klipper.service"

    def test_appends_new_component(self):
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML, OVERRIDE_YAML)),
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat", return_value=self._safe_stat_mock()),
            patch("pathlib.Path.is_dir", return_value=True),
        ):
            components, poll = load_components()
        assert any(c.name == "my-plugin" for c in components)

    def test_keeps_bundled_fields_not_in_override(self):
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML, OVERRIDE_YAML)),
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat", return_value=self._safe_stat_mock()),
            patch("pathlib.Path.is_dir", return_value=True),
        ):
            components, poll = load_components()
        klipper = next(c for c in components if c.name == "klipper")
        assert klipper.kind == "git"
        assert klipper.reset_mode == "hard"

    def test_syntax_error_falls_back_to_bundled(self, caplog):
        invalid_yaml = "key: [unclosed"
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML, invalid_yaml)),
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat", return_value=self._safe_stat_mock()),
            patch("pathlib.Path.is_dir", return_value=True),
            caplog.at_level(logging.ERROR, logger="updater.components"),
        ):
            components, poll = load_components()
        names = [c.name for c in components]
        assert "klipper" in names
        assert "my-plugin" not in names


class TestValidation:
    def test_invalid_component_skipped_with_warning(self, caplog):
        bad_yaml = """
components:
    - name: bad
      type: git
      path: /etc/passwd
      service: bad.service
      order: 10
"""
        with (
            patch("builtins.open", _mock_load(bad_yaml)),
            patch("pathlib.Path.exists", return_value=True),
            caplog.at_level(logging.WARNING, logger="updater.components"),
        ):
            components, poll = load_components()
        assert not any(c.name == "bad" for c in components)
        assert any("bad" in r.message for r in caplog.records)

    def test_path_outside_home_rejected(self):
        outside_yaml = """
components:
    - name: outside
      type: git
      path: /etc/outside
      service: outside.service
      order: 10
"""
        with (
            patch("builtins.open", _mock_load(outside_yaml)),
            patch("pathlib.Path.exists", return_value=False),
        ):
            components, poll = load_components()
        assert not any(c.name == "outside" for c in components)

    def test_service_name_with_slash_rejected(self):
        bad_yaml = """
components:
    - name: bad
      type: git
      path: ~/bad
      service: ../bad.service
      order: 10
"""
        with (
            patch("builtins.open", _mock_load(bad_yaml)),
            patch("pathlib.Path.exists", return_value=False),
        ):
            components, poll = load_components()
        assert not any(c.name == "bad" for c in components)

    def test_service_name_with_shell_metachar_rejected(self):
        for metachar in [";", "&", "|", "$", "`"]:
            bad_yaml = f"""
components:
  - name: bad
    type: git
    path: ~/bad
    service: bad{metachar}cmd.service
    order: 10
"""
            with (
                patch("builtins.open", _mock_load(bad_yaml)),
                patch("pathlib.Path.exists", return_value=False),
            ):
                components, poll = load_components()
            assert not any(c.name == "bad" for c in components), (
                f"metachar {metachar!r} not rejected"
            )

    def test_service_name_valid_pattern_accepted(self):
        good_yaml = """
components:
    - name: my-plugin
      type: git
      path: ~/my-plugin
      service: my-plugin.service
      order: 5
"""
        with (
            patch("builtins.open", _mock_load(good_yaml)),
            patch("pathlib.Path.exists", return_value=False),
            patch("pathlib.Path.is_dir", return_value=True),
        ):
            components, poll = load_components()
        assert any(c.name == "my-plugin" for c in components)

    def test_restart_klipper_flag_parsed(self):
        yaml_text = """
components:
    - name: cfg
      type: git
      path: ~/cfg
      branch: master
      order: 10
      restart_klipper: true
"""
        with (
            patch("builtins.open", _mock_load(yaml_text)),
            patch("pathlib.Path.exists", return_value=False),
        ):
            components, _ = load_components()
        cfg = next(c for c in components if c.name == "cfg")
        assert cfg.restart_klipper is True

    def test_invalid_branch_name_skipped(self, caplog):
        bad_yaml = """
components:
    - name: bad
      type: git
      path: ~/bad
      branch: "bad branch!"
      order: 10
"""
        with (
            patch("builtins.open", _mock_load(bad_yaml)),
            patch("pathlib.Path.exists", return_value=False),
            caplog.at_level(logging.WARNING, logger="updater.components"),
        ):
            components, poll = load_components()
        assert not any(c.name == "bad" for c in components)
        assert any("bad" in r.message for r in caplog.records)

    def test_invalid_version_skipped(self, caplog):
        bad_yaml = """
components:
    - name: bad
      type: git
      path: ~/bad
      version: "bad version!"
      order: 10
"""
        with (
            patch("builtins.open", _mock_load(bad_yaml)),
            patch("pathlib.Path.exists", return_value=False),
            caplog.at_level(logging.WARNING, logger="updater.components"),
        ):
            components, poll = load_components()
        assert not any(c.name == "bad" for c in components)
        assert any("bad" in r.message for r in caplog.records)


class TestYamlBootstrap:
    def test_yaml_missing_returns_empty_list(self, caplog):
        with (
            patch.dict(sys.modules, {"yaml": None}),
            caplog.at_level(logging.ERROR, logger="updater.components"),
        ):
            components, poll = load_components()
        assert components == []
        assert poll == 1440 * 60.0  # default poll interval
        assert any("not installed" in r.message for r in caplog.records)


class TestOverridePermissions:
    def test_override_skipped_when_world_writable(self, caplog):
        """Override file with mode 0o622 (world-writable) is skipped."""
        mock_stat = MagicMock()
        mock_stat.st_mode = 0o100622  # Regular file, world-writable
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML)),
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat", return_value=mock_stat),
            patch("pathlib.Path.is_dir", return_value=True),
            caplog.at_level(logging.WARNING, logger="updater.components"),
        ):
            components, poll = load_components()
        # Should only have bundled components, no override merged
        names = [c.name for c in components]
        assert "klipper" in names
        assert "blockscreen" in names
        assert any("writable by group/others" in r.message for r in caplog.records)

    def test_override_skipped_when_group_writable(self, caplog):
        """Override file with mode 0o620 (group-writable) is skipped."""
        mock_stat = MagicMock()
        mock_stat.st_mode = 0o100620  # Regular file, group-writable
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML)),
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat", return_value=mock_stat),
            patch("pathlib.Path.is_dir", return_value=True),
            caplog.at_level(logging.WARNING, logger="updater.components"),
        ):
            components, poll = load_components()
        assert any("writable by group/others" in r.message for r in caplog.records)

    def test_override_loaded_with_safe_permissions(self):
        """Override file with mode 0o600 (owner-only) is loaded."""
        mock_stat = MagicMock()
        mock_stat.st_mode = 0o100600  # Regular file, owner-only
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML, OVERRIDE_YAML)),
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat", return_value=mock_stat),
            patch("pathlib.Path.is_dir", return_value=True),
        ):
            components, poll = load_components()
        # Should have merged components from override
        assert any(c.name == "my-plugin" for c in components)
        klipper = next(c for c in components if c.name == "klipper")
        assert str(klipper.path).endswith("costum_klipper")

    def test_override_skipped_when_stat_fails(self, caplog):
        """Override file that cannot be stat'd is skipped."""
        with (
            patch("builtins.open", _mock_load(BUNDLE_YAML)),
            patch("pathlib.Path.exists", return_value=True),
            patch("pathlib.Path.stat", side_effect=OSError("Permission denied")),
            patch("pathlib.Path.is_dir", return_value=True),
            caplog.at_level(logging.WARNING, logger="updater.components"),
        ):
            components, poll = load_components()
        assert any("Cannot stat override path" in r.message for r in caplog.records)


class TestProvisionConfig:
    """install_if_missing + url validation in _validate_component."""

    def _base(self, **extra):
        data = {"name": "newcomp", "type": "git", "path": "~/newcomp"}
        data.update(extra)
        return data

    def test_valid_url_and_flag_parsed(self):
        from updater.components import _validate_component

        cfg = _validate_component(
            self._base(url="https://github.com/x/y", install_if_missing=True)
        )
        assert cfg is not None
        assert cfg.url == "https://github.com/x/y"
        assert cfg.install_if_missing is True

    def test_non_https_url_dropped(self, caplog):
        from updater.components import _validate_component

        with caplog.at_level(logging.WARNING, logger="updater.components"):
            cfg = _validate_component(self._base(url="git@github.com:x/y"))
        assert cfg is not None
        assert cfg.url is None

    def test_flag_without_url_disabled(self, caplog):
        from updater.components import _validate_component

        with caplog.at_level(logging.WARNING, logger="updater.components"):
            cfg = _validate_component(self._base(install_if_missing=True))
        assert cfg is not None
        assert cfg.install_if_missing is False

    def test_defaults_when_absent(self):
        from updater.components import _validate_component

        cfg = _validate_component(self._base())
        assert cfg is not None
        assert cfg.url is None
        assert cfg.install_if_missing is False


def test_invalid_reset_mode_coerced_to_hard(caplog):
    bad_yaml = """
components:
    - name: klipper
      type: git
      path: ~/klipper
      reset_mode: Hard
      order: 10
"""
    with (
        patch("builtins.open", _mock_load(bad_yaml)),
        patch("pathlib.Path.exists", return_value=False),
        caplog.at_level(logging.WARNING, logger="updater.components"),
    ):
        configs, _ = load_components()
    assert configs[-1].reset_mode == "hard"  # typo must not become the soft path
    assert any("invalid reset_mode" in r.message for r in caplog.records)


def test_non_dict_component_entry_skipped(caplog):
    bad_yaml = """
components:
    - just-a-string
    - name: klipper
      type: git
      path: ~/klipper
      order: 10
"""
    with (
        patch("builtins.open", _mock_load(bad_yaml)),
        patch("pathlib.Path.exists", return_value=False),
        caplog.at_level(logging.WARNING, logger="updater.components"),
    ):
        configs, _ = load_components()
    assert [c.name for c in configs if c.kind == "git"] == ["klipper"]
