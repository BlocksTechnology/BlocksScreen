"""Unit tests for moonrakerComm exception types."""

from BlocksScreen.lib.moonrakerComm import OneShotTokenError


class TestOneShotTokenError:
    def test_str_carries_message(self):
        # A super(OneShotTokenError).__init__ regression left str(exc) empty.
        exc = OneShotTokenError("token fetch failed")
        assert str(exc) == "token fetch failed"
        assert exc.message == "token fetch failed"

    def test_default_message(self):
        exc = OneShotTokenError()
        assert str(exc) == "Unable to get oneshot token"

    def test_errors_attribute_kept(self):
        exc = OneShotTokenError("boom", errors={"code": 401})
        assert exc.errors == {"code": 401}
