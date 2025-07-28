import logging
from typing import Type

import requests
from requests import Request, Response


class UncallableError(Exception):
    """Raised when a method is not callable"""

    def __init__(self, message="Unable to call method", errors=None):
        super(UncallableError, self).__init__(message, errors)
        self.errors = errors
        self.message = message


class MoonRest:
    """MoonRest Basic API for sending end posting requests to MoonrakerAPI

    - Credit goes to from Klipper Screen project
        https://github.com/KlipperScreen/KlipperScreen
        https://github.com/KlipperScreen/KlipperScreen/blob/a32d1d8e8085724068ac6a43adbba9757228aebb/ks_includes/KlippyRest.py

    Raises:
        UncallableError: An error occurred when the request type invalid
    """

    timeout = 3

    # TODO: The ip and port need to come from a configfile

    # def __init__(self, ip="localhost", port="7125", api_key=False):
    def __init__(self, ip="192.168.1.68", port="7125", api_key=False):
        self._ip = ip
        self._port = port
        self._api_key = api_key

    @property
    def build_endpoint(self):
        # TODO: Need to also account for if the port is https
        return f"http://{self._ip}:{self._port}"

    def get_oneshot_token(self):
        """Requests Moonraker API for a oneshot token to be used on
        API key authentication

        Returns:
            str: A oneshot token
        """
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
        """GET MoonrakerAPI /server/info

        Returns:
            dict: server info from Moonraker
        """
        return self.get_request(method="server/info")

    def firmware_restart(self):
        """firmware_restart
            POST to /printer/firmware_restart to firmware restart Klipper

        Returns:
            str: Returns an 'ok' from Moonraker
        """
        return self.post_request(method="printer/firmware_restart")

    def delete_request(self):
        # TODO: Create a delete request, so the user is able to delete files from the pi, can also be made with websockets
        pass

    def post_request(self, method, data=None, json=None, json_response=True):
        return self._request(
            request_type="post",
            method=method,
            data=data,
            json=json,
            json_response=json_response,
        )

    def get_request(self, method, json=True, timeout=timeout):
        return self._request(
            request_type="get",
            method=method,
            json_response=json,
            timeout=timeout,
        )

    def _request(
        self,
        request_type,
        method,
        data=None,
        json=None,
        json_response=True,
        timeout=timeout,
    ):
        # TODO: Need to check if the header is actually correct or not
        # TEST: Test the reliability of this
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
                    return (
                        response.json() if json_response else response.content
                    )

        except Exception as e:
            logging.info(f"Unexpected error while sending HTTP request: {e}")

    # Blocking HTTP Client
    # class MoonRestClientBlocking(tornado.httpclient.HTTPClient):
    ...

    # def __init__(self, async_client_class: AsyncHTTPClient | None = None, **kwargs: logging.Any) -> None:
    #     super(MoonRestClientBlocking, self).__init__(async_client_class, **kwargs)


# ASYNC HTTP Client
# class MoonRestClientNonBlocking(tornado.httpclient.AsyncHTTPClient): ...
