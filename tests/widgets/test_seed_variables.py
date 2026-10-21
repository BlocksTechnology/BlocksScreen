"""_seed_variables: repo variables.cfg keys reach Klipper via SAVE_VARIABLE, once each."""

import ast
import shlex
from unittest.mock import MagicMock

import pytest

from .test_sigterm_shutdown import _load_entry_module


@pytest.fixture(scope="module")
def entry_mod():
    return _load_entry_module()


def _seed(entry_mod, defaults: dict[str, str]):
    window = MagicMock()
    manager = MagicMock()
    manager.variable_defaults.return_value = defaults
    entry_mod._seed_variables(window, manager)
    on_update = window.printer.save_variables_update.connect.call_args.args[0]
    return on_update, window.run_gcode_signal.emit


def test_only_missing_keys_are_saved(entry_mod):
    on_update, emit = _seed(entry_mod, {"etemp": "0", "printcore_type": "'Standard'"})
    on_update({"variables": {"etemp": 5}})
    emit.assert_called_once_with(
        "SAVE_VARIABLE VARIABLE=printcore_type VALUE=" + shlex.quote("'Standard'")
    )


def test_value_survives_klipper_param_parsing(entry_mod):
    on_update, emit = _seed(entry_mod, {"material_type": "'PLA #1'"})
    on_update({"variables": {}})
    # Klipper splits extended params with posix shlex and '#;' commenters
    lex = shlex.shlex(emit.call_args.args[0].split(" ", 1)[1], posix=True)
    lex.whitespace_split = True
    lex.commenters = "#;"
    params = dict(arg.split("=", 1) for arg in lex)
    assert ast.literal_eval(params["VALUE"]) == "PLA #1"


def test_key_is_sent_once_even_before_klipper_reports_it(entry_mod):
    on_update, emit = _seed(entry_mod, {"heating": "False"})
    on_update({"variables": {}})
    on_update({"variables": {"etemp": 0}})
    assert emit.call_count == 1


def test_update_without_variables_is_ignored(entry_mod):
    on_update, emit = _seed(entry_mod, {"heating": "False"})
    on_update({})
    emit.assert_not_called()
