"""Helpers for the callback replies of ``MoonAPI`` requests."""

# -1: websocket closed; 503: Moonraker failing pending requests when Klippy disconnects
_DISCONNECT_CODES = frozenset({-1, 503})


def reply_error(reply: object) -> dict | None:
    """Return the error of a ``send_request`` callback reply, or None on success."""
    if not isinstance(reply, dict) or reply.get("error") is None:
        return None
    error = reply["error"]
    return error if isinstance(error, dict) else {"message": str(error)}


def is_disconnect_error(error: dict | None) -> bool:
    """True if a reply error means the link to Klipper was lost, not a command failure."""
    return error is not None and error.get("code") in _DISCONNECT_CODES
