"""Unit tests for ConfigPage section visibility and timeout validation."""

import importlib.util
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PyQt6 import QtCore, QtWidgets

# conftest mocks "configfile", so load the real one under another name
_spec = importlib.util.spec_from_file_location(
    "_real_configfile",
    Path(__file__).resolve().parents[2] / "BlocksScreen" / "configfile.py",
)
_configfile = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_configfile)

_SERVER = "[server]\nhost: localhost\n"
_KEY = ("screensaver", "timeout")


class _FakeInput(QtWidgets.QWidget):
    request_back = QtCore.pyqtSignal()
    value_selected = QtCore.pyqtSignal(str)

    def __getattr__(self, name):
        return MagicMock()


@pytest.fixture
def make_page(qtbot, monkeypatch, tmp_path):
    from BlocksScreen.lib.panels.widgets.UtilitiesTab import configPage

    def make(text):
        path = tmp_path / "BlocksScreen.cfg"
        path.write_text(text)
        cfg = _configfile.BlocksScreenConfig(path, "server")
        cfg.load_config()
        monkeypatch.setattr(configPage, "get_configparser", lambda: cfg)
        monkeypatch.setattr(configPage, "CustomNumpad", _FakeInput)
        monkeypatch.setattr(configPage, "CustomQwertyKeyboard", _FakeInput)
        page = configPage.ConfigPage(None)
        qtbot.addWidget(page)
        return page, path

    return make


def _sections(page):
    return [section for section, _ in page._visible_sections()]


def test_only_server_shown_by_default(make_page):
    page, _ = make_page(_SERVER + "[screensaver]\ntimeout: 300000\n")
    assert _sections(page) == ["server"]


@pytest.mark.parametrize("value", ["true", "yes", "on", "1"])
def test_shown_true_shows_section(make_page, value):
    page, _ = make_page(_SERVER + f"[screensaver]\nshown: {value}\ntimeout: 1\n")
    assert _sections(page) == ["server", "screensaver"]


def test_shown_false_hides_server(make_page):
    page, _ = make_page("[server]\nshown: false\nhost: localhost\n")
    assert _sections(page) == []


def test_invalid_shown_uses_default(make_page):
    page, _ = make_page(_SERVER + "[screensaver]\nshown: maybe\ntimeout: 1\n")
    assert _sections(page) == ["server"]


@pytest.mark.parametrize(
    ("text", "valid"),
    [("1", True), ("120", True), ("0", False), ("121", False), ("abc", False)],
)
def test_timeout_validation(make_page, text, valid):
    page, _ = make_page(_SERVER)
    assert page._is_valid(*_KEY, text) is valid


def test_invalid_timeout_reverts_and_valid_one_saves(make_page):
    from BlocksScreen.lib.panels.widgets.UtilitiesTab.configPage import BlocksField

    page, path = make_page(_SERVER + "[screensaver]\nshown: true\ntimeout: 300000\n")
    field = next(f for f in page.findChildren(BlocksField) if f.text() == "5")

    field.set_right_text("0")
    page._stage_option(*_KEY, field)
    assert field.text() == "5"
    assert not page._pending

    field.set_right_text("10")
    page._stage_option(*_KEY, field)
    page._save_pending()
    assert "timeout: 600000" in path.read_text()
