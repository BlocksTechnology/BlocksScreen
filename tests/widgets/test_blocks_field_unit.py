"""Unit tests for BlocksField Toggle mode."""

import pytest

from BlocksScreen.lib.utils.blocks_field import BlocksField


@pytest.fixture
def toggle(qtbot):
    field = BlocksField(None, "Enabled:", editable="Toggle")
    qtbot.addWidget(field)
    return field


def test_set_checked_does_not_emit_on_edit(toggle, qtbot):
    with qtbot.assertNotEmitted(toggle.on_edit):
        toggle.set_checked(True)
        toggle.set_right_text("off")
    assert not toggle.is_checked()


@pytest.mark.parametrize(
    ("text", "checked"), [("yes", True), ("On", True), ("1", True), ("no", False)]
)
def test_set_right_text_reads_config_booleans(toggle, text, checked):
    toggle.set_right_text(text)
    assert toggle.is_checked() is checked
