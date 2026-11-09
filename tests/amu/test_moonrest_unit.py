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
        with patch.object(rest, "post_request", return_value={"result": spool_data}):
            assert rest.get_spool(42) == spool_data

    def test_returns_non_on_http_error(self, rest) -> None:
        with patch.object(rest, "post_request", return_value=None):
            assert rest.get_spool(42) is None

    def test_returns_none_on_missing_result_key(self, rest):
        with patch.object(rest, "post_request", return_value={"something": "else"}):
            assert rest.get_spool(42) is None

    # /server/spoolman/spool/{id} is a 404; only the proxy route exists.
    def test_goes_through_the_proxy(self, rest) -> None:
        with patch.object(rest, "post_request", return_value=None) as mock_post:
            rest.get_spool(7)
        mock_post.assert_called_once_with(
            "server/spoolman/proxy",
            json={
                "request_method": "GET",
                "path": "/v1/spool/7",
                "use_v2_response": False,
            },
        )
