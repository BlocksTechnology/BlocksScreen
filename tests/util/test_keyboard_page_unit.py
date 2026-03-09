"""Unit tests for CustomQwertyKeyboard (keyboardPage.py).

Tests cover layout switching, value insertion, signal emission,
the dedicated dot button, and layout array length invariants.
"""

import sys
import types
from pathlib import Path

import pytest
from PyQt6 import QtCore, QtWidgets

# BlocksScreen/ must be on sys.path so ``from lib.utils...`` resolves
# (matching the runtime import style used inside the package).
_bs_dir = str(Path(__file__).resolve().parent.parent / "BlocksScreen")
if _bs_dir not in sys.path:
    sys.path.insert(0, _bs_dir)

# Stub ``lib.utils.icon_button`` to avoid loading Qt resource files.
_icon_stub = types.ModuleType("lib.utils.icon_button")
_icon_stub.IconButton = QtWidgets.QPushButton  # type: ignore[attr-defined]
sys.modules.setdefault("lib.utils.icon_button", _icon_stub)

# Force-reload the real module — the network conftest registers a stub
# that lacks the layout constants we need.
for _key in [
    "lib.panels.widgets.keyboardPage",
    "BlocksScreen.lib.panels.widgets.keyboardPage",
]:
    sys.modules.pop(_key, None)

from BlocksScreen.lib.panels.widgets.keyboardPage import (  # noqa: E402
    _LOWERCASE, _NUM_KEYS, _NUMBERS, _SYMBOLS, _UPPERCASE,
    CustomQwertyKeyboard)


@pytest.fixture()
def keyboard(qtbot):
    """Create a keyboard widget with IconButton mocked out."""
    kb = CustomQwertyKeyboard(parent=None)
    qtbot.addWidget(kb)
    return kb


class TestLayoutArrayLengths:
    """Guard against the off-by-one bug that hid the dot key."""

    def test_lowercase_has_26_keys(self):
        assert len(_LOWERCASE) == _NUM_KEYS

    def test_uppercase_has_26_keys(self):
        assert len(_UPPERCASE) == _NUM_KEYS

    def test_numbers_has_26_keys(self):
        assert len(_NUMBERS) == _NUM_KEYS

    def test_symbols_has_26_keys(self):
        assert len(_SYMBOLS) == _NUM_KEYS


class TestDefaultLayout:
    """Keyboard starts in lowercase."""

    def test_initial_layout_is_lowercase(self, keyboard):
        texts = [btn.text() for btn in keyboard._key_buttons]
        assert texts == _LOWERCASE

    def test_shift_button_says_shift(self, keyboard):
        assert keyboard.K_shift.text() == "⇧"


class TestLayoutSwitching:
    """Layout changes based on shift/keychange toggle state."""

    def test_shift_gives_uppercase(self, keyboard):
        keyboard.K_shift.setChecked(True)
        keyboard.handle_keyboard_layout()
        texts = [btn.text() for btn in keyboard._key_buttons]
        assert texts == _UPPERCASE

    def test_keychange_gives_numbers(self, keyboard):
        keyboard.K_keychange.setChecked(True)
        keyboard.handle_keyboard_layout()
        texts = [btn.text() for btn in keyboard._key_buttons]
        assert texts == _NUMBERS

    def test_keychange_shift_gives_symbols(self, keyboard):
        keyboard.K_keychange.setChecked(True)
        keyboard.K_shift.setChecked(True)
        keyboard.handle_keyboard_layout()
        texts = [btn.text() for btn in keyboard._key_buttons]
        assert texts == _SYMBOLS

    def test_shift_label_changes_to_hash_in_number_mode(self, keyboard):
        keyboard.K_keychange.setChecked(True)
        keyboard.handle_keyboard_layout()
        assert keyboard.K_shift.text() == "#+="

    def test_symbolsrun_returns_to_lowercase(self, keyboard):
        """After symbols, pressing shift should reset to lowercase."""
        keyboard.K_keychange.setChecked(True)
        keyboard.K_shift.setChecked(True)
        keyboard.handle_keyboard_layout()
        assert keyboard.symbolsrun is True

        keyboard.K_keychange.setChecked(False)
        keyboard.K_shift.setChecked(True)
        keyboard.handle_keyboard_layout()

        texts = [btn.text() for btn in keyboard._key_buttons]
        assert texts == _LOWERCASE
        assert keyboard.symbolsrun is False
        assert keyboard.K_shift.isChecked() is False


class TestValueInsertion:
    """Character insertion, deletion, and submission."""

    def test_typing_characters(self, keyboard):
        keyboard.value_inserted("h")
        keyboard.value_inserted("i")
        assert keyboard.current_value == "hi"
        assert keyboard.inserted_value.text() == "hi"

    def test_space_inserts_space(self, keyboard):
        keyboard.value_inserted("a")
        keyboard.value_inserted(" ")
        assert keyboard.current_value == "a "

    def test_clear_deletes_last_char(self, keyboard):
        keyboard.value_inserted("a")
        keyboard.value_inserted("b")
        keyboard.value_inserted("clear")
        assert keyboard.current_value == "a"

    def test_clear_on_single_char_empties(self, keyboard):
        keyboard.value_inserted("x")
        keyboard.value_inserted("clear")
        assert keyboard.current_value == ""

    def test_clear_on_empty_stays_empty(self, keyboard):
        keyboard.value_inserted("clear")
        assert keyboard.current_value == ""

    def test_ampersand_conversion(self, keyboard):
        keyboard.value_inserted("&&")
        assert keyboard.current_value == "&"

    def test_enter_emits_and_resets(self, keyboard, qtbot):
        keyboard.value_inserted("p")
        keyboard.value_inserted("w")

        with qtbot.waitSignal(keyboard.value_selected, timeout=1000) as sig:
            keyboard.value_inserted("enter")

        assert sig.args == ["pw"]
        assert keyboard.current_value == ""
        assert keyboard.inserted_value.text() == ""


class TestSetValue:
    """Pre-filling the keyboard input field."""

    def test_set_value_prefills(self, keyboard):
        keyboard.set_value("pre-filled")
        assert keyboard.current_value == "pre-filled"
        assert keyboard.inserted_value.text() == "pre-filled"

    def test_set_value_then_type(self, keyboard):
        keyboard.set_value("abc")
        keyboard.value_inserted("d")
        assert keyboard.current_value == "abcd"


class TestDotButton:
    """Dedicated dot button is always accessible regardless of layout."""

    def test_dot_button_exists(self, keyboard):
        assert hasattr(keyboard, "K_dot")
        assert keyboard.K_dot.text() == "."

    def test_dot_click_inserts_dot(self, keyboard, qtbot):
        qtbot.mouseClick(keyboard.K_dot, QtCore.Qt.MouseButton.LeftButton)
        assert keyboard.current_value == "."

    def test_dot_always_visible_across_layouts(self, keyboard):
        """The dot button is independent of layout switching."""
        for checked_kc, checked_sh in [
            (False, False),
            (False, True),
            (True, False),
            (True, True),
        ]:
            keyboard.K_keychange.setChecked(checked_kc)
            keyboard.K_shift.setChecked(checked_sh)
            keyboard.handle_keyboard_layout()
            assert keyboard.K_dot.text() == "."


class TestButtonClicks:
    """Clicking buttons triggers the correct value insertion."""

    def test_key_button_click_inserts_text(self, keyboard, qtbot):
        first_btn = keyboard._key_buttons[0]
        assert first_btn.text() == "q"
        qtbot.mouseClick(first_btn, QtCore.Qt.MouseButton.LeftButton)
        assert keyboard.current_value == "q"

    def test_space_button_click(self, keyboard, qtbot):
        qtbot.mouseClick(keyboard.K_space, QtCore.Qt.MouseButton.LeftButton)
        assert keyboard.current_value == " "

    def test_delete_button_click(self, keyboard, qtbot):
        keyboard.value_inserted("x")
        qtbot.mouseClick(keyboard.k_delete, QtCore.Qt.MouseButton.LeftButton)
        assert keyboard.current_value == ""

    def test_back_button_emits_signal(self, keyboard, qtbot):
        with qtbot.waitSignal(keyboard.request_back, timeout=1000):
            qtbot.mouseClick(
                keyboard.numpad_back_btn, QtCore.Qt.MouseButton.LeftButton
            )
