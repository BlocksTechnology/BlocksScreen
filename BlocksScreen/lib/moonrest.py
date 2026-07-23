# moonraker rest
#
# Copyright (C) 2025 Hugo Costa <h.costa@blockstec.com>
#
# Based on the work:
# https://github.com/KlipperScreen/KlipperScreen/blob/master/ks_includes/KlippyRest.py
# Copyright (C) KlipperScreen contributors
#
# Modified from the work referenced above
#
# This file is part of BlocksScreen.
#
# BlocksScreen is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlocksScreen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BlocksScreen. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later


import logging
from urllib.parse import quote

import requests
from requests import Request, Response

logger = logging.getLogger(__name__)


class UncallableError(Exception):
    """Raised when a method is not callable"""

    def __init__(self, message="Unable to call method", errors=None):
        super(UncallableError, self).__init__(message, errors)
        self.errors = errors
        self.message = message


class MoonRest:
    """MoonRest API for GET/POST requests to Moonraker."""

    timeout = 3

    def __init__(
        self, host: str = "localhost", port: int = 7125, api_key: str | None = None
    ):
        self._host = host
        self._port = port
        self._api_key: str | None = api_key

    @property
    def build_endpoint(self):
        """Build connection endpoint"""
        return f"http://{self._host}:{self._port}"

    def get_oneshot_token(self):
        """Request oneshot token from Moonraker for API key authentication."""
        # Response data is generally an object itself, however for some requests this may simply be an "ok" string.
        response = self.get_request(method="access/oneshot_token")
        if response is None:
            return None
        return (
            response["result"]
            if isinstance(response, dict) and "result" in response
            else None
        )

    def get_server_info(self):
        """Fetch server info from Moonraker."""
        return self.get_request(method="server/info")

    def get_spool(self, spool_id: int) -> dict | None:
        """Fetch spool info from Moonraker; None on any error."""
        response = self.get_request(f"server/spoolman/spool/{spool_id}")
        if not isinstance(response, dict):
            return None
        return response.get("result")

    def set_spool_used_weight(self, spool_id: int, weight: float) -> bool:
        """Update spool used_weight via Moonraker; True on success."""
        response = self.post_request(
            f"server/spoolman/spool/{spool_id}", json={"used_weight": weight}
        )
        return response is not None

    def firmware_restart(self):
        """POST firmware_restart to Moonraker."""
        return self.post_request(method="printer/firmware_restart")

    def post_request(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="post",
            method=method,
            data=data,
            json=json,
            json_response=json_response,
        )

    def get_request(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            request_type="get",
            method=method,
            json_response=json,
            timeout=timeout,
        )

    def get_gcode_header(self, rel_path: str, max_bytes: int = 131072) -> bytes | None:
        """GET the first *max_bytes* of a gcode file (embedded-thumbnail parse)."""
        url = f"{self.build_endpoint}/server/files/gcodes/{quote(rel_path)}"
        headers = {"Range": f"bytes=0-{max_bytes - 1}"}
        if self._api_key:
            headers["x-api-key"] = self._api_key
        try:
            with requests.get(
                url, headers=headers, stream=True, timeout=self.timeout
            ) as resp:
                resp.raise_for_status()
                data = bytearray()
                for chunk in resp.iter_content(chunk_size=65536):
                    data.extend(chunk)
                    if len(data) >= max_bytes:
                        break
                return bytes(data)
        except Exception as exc:
            logger.info("gcode header fetch failed for %s: %s", rel_path, exc)
            return None

    def _request(
        self,
        request_type,
        method,
        data=None,
        json=None,
        json_response=True,
        timeout=timeout,
    ):
        _url = f"{self.build_endpoint}/{method}"
        _headers = {"x-api-key": self._api_key} if self._api_key else {}
        try:
            if hasattr(requests, request_type):
                _request_method: Request = getattr(requests, request_type)
                if not callable(_request_method):
                    raise UncallableError(
                        "Invalid request method",
                        f"Request method '{request_type}' is not callable.",
                    )

                response = _request_method(
                    _url,
                    json=json,
                    data=data,
                    headers=_headers,
                    timeout=timeout,
                )
                if isinstance(response, Response):
                    response.raise_for_status()
                    return response.json() if json_response else response.content

        except Exception as e:
            logger.info(f"Unexpected error while sending HTTP request: {e}")
