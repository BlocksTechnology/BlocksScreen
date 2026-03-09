"""Unit tests for EntryListModel.reconcile() — locks behaviour before refactoring."""

import pytest
from PyQt6 import QtWidgets

from BlocksScreen.lib.utils.list_model import EntryListModel, ListItem


def _item(text, right_text=""):
    return ListItem(text=text, right_text=right_text)


def _key(i):
    return i.text


@pytest.fixture
def model(qapp):
    m = EntryListModel()
    yield m
    m.deleteLater()


class TestReconcile:
    def test_empty_to_items(self, model):
        model.reconcile([_item("A"), _item("B"), _item("C")], _key)
        assert model.rowCount() == 3

    def test_removes_stale(self, model):
        model.reconcile(
            [_item("A"), _item("B"), _item("C"), _item("D"), _item("E")], _key
        )
        model.reconcile([_item("A"), _item("C")], _key)
        assert model.rowCount() == 2
        assert model.entries[0].text == "A"
        assert model.entries[1].text == "C"

    def test_preserves_order(self, model):
        model.reconcile([_item("A"), _item("B"), _item("C")], _key)
        model.reconcile([_item("C"), _item("B"), _item("A")], _key)
        assert [e.text for e in model.entries] == ["C", "B", "A"]

    def test_update_in_place(self, model):
        model.reconcile([_item("A")], _key)
        updated = _item("A", right_text="new")
        model.reconcile([updated], _key)
        assert model.entries[0].right_text == "new"
        assert model.rowCount() == 1

    def test_no_change_is_noop(self, model):
        items = [_item("A"), _item("B")]
        model.reconcile(items, _key)
        model.reconcile(items, _key)
        assert model.rowCount() == 2

    def test_batch_reset_large_stale(self, model):
        """More than 50% stale triggers batch reset path."""
        model.reconcile([_item(str(i)) for i in range(10)], _key)
        model.reconcile([_item("0"), _item("1")], _key)
        assert model.rowCount() == 2

    def test_add_new_items_to_existing(self, model):
        model.reconcile([_item("A")], _key)
        model.reconcile([_item("A"), _item("B"), _item("C")], _key)
        assert model.rowCount() == 3
        assert [e.text for e in model.entries] == ["A", "B", "C"]

    def test_complete_replacement(self, model):
        model.reconcile([_item("A"), _item("B")], _key)
        model.reconcile([_item("X"), _item("Y")], _key)
        assert model.rowCount() == 2
        assert [e.text for e in model.entries] == ["X", "Y"]

    def test_empty_desired_clears_all(self, model):
        model.reconcile([_item("A"), _item("B"), _item("C")], _key)
        model.reconcile([], _key)
        assert model.rowCount() == 0
