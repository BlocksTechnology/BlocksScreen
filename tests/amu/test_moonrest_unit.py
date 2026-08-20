"""Unit tests for BlocksScreen.lib.moonrest"""

from unittest.mock import patch
import pytest
from BlocksScreen.lib.moonrest import MoonRest


@pytest.fixture
def rest():
    """MoonRest instance poiting at localhost"""
    return MoonRest(host="localhost", port=7125)


class TestGetSpool:
    def test_return_spool_dict_on_sucess(self, rest) -> None:
        spool_data = {
            "id": 42,
            "filament": {"name": "PLA", "color_hex": "ff0000"},
            "used_weight": 50.0,
            "remaining_weight": 200.0,
        }
        with patch.object(rest, "get_request", return_value={"result": spool_data}):
            assert rest.get_spool(42) == spool_data

    def test_returns_non_on_http_error(self, rest) -> None:
        with patch.object(rest, "get_request", return_value=None):
            assert rest.get_spool(42) is None

    def test_returns_none_on_missing_result_key(self, rest):
        with patch.object(rest, "get_request", return_value={"something": "else"}):
            assert rest.get_spool(42) is None

    def test_calls_correct_endpoint(self, rest) -> None:
        with patch.object(rest, "get_request", return_value=None) as mock_get:
            rest.get_spool(7)
        mock_get.assert_called_once_with("server/spoolman/spool/7")


class TestSetSpoolUsedWeight:
    def test_returns_true_on_sucess(self, rest) -> None:
        with patch.object(rest, "post_request", return_value={"result": "ok"}):
            assert rest.set_spool_used_weight(42, 75.5)

    def test_returns_false_on_error(self, rest) -> None:
        with patch.object(rest, "post_request", return_value={"result": "ok"}):
            assert rest.set_spool_used_weight(42, 75.5)

    def test_calls_correct_endpoint(self, rest) -> None:
        with patch.object(rest, "post_request", return_value=None) as mock_post:
            rest.set_spool_used_weight(5, 100.0)
        mock_post.assert_called_once_with(
            "server/spoolman/spool/5", json={"used_weight": 100.0}
        )
