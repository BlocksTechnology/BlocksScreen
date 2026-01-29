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
import os
from typing import Optional

import requests
from helper_methods import sha256_checksum
from requests import Request, Response


class UncallableError(Exception):
    """Raised when a method is not callable"""

    def __init__(self, message="Unable to call method", errors=None):
        super(UncallableError, self).__init__(message, errors)
        self.errors = errors
        self.message = message


class MoonRest:
    """MoonRest Basic API for sending end posting requests to MoonrakerAPI

    Raises:
        UncallableError: An error occurred when the request type invalid
    """

    timeout = 3

    def __init__(self, host: str = "localhost", port: int = 7125, api_key=False):
        self._host = host
        self._port = port
        self._api_key = api_key

    @property
    def build_endpoint(self):
        """Build connection endpoint"""
        return f"http://{self._host}:{self._port}"

    def get_oneshot_token(self):
        """`GET MoonrakerAPI` Requests Moonraker API for a oneshot token to be used on
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

    def get_download_file(self, root: str, filename: str):
        """`GET MoonrakerAPI` /server/files
        Retrieves file `filename` at root `root`. The `filename` must include the relative path if it is not in the root folder

        Returns:
            dict: contents of the requested file from Moonraker

        """
        if root == "":
            return self.get_request(method=f"server/files/{filename}")
        return self.get_request(method=f"server/files/{root}/{filename}")

    def get_printer_info(self):
        """`GET MoonrakerAPI` /printer/info
        Get Klippy host information

        Returns:
            dict: printer info from Moonraker
        """
        return self.get_request(method="printer/info")

    def get_server_info(self):
        """`GET MoonrakerAPI` /server/info
        Query Server Info

        Returns:
            dict: server info from Moonraker
        """
        return self.get_request(method="server/info")

    def get_dir_information(self, directory: str = "", extended: bool = False) -> dict:
        """`GET MoonrakerAPI` /server/files/directory?path=`directory`&extended=`extended`
        Returns a list of files and subdirectories given a supplied path. Unlike `/server/files/list`, this command does not walk through subdirectories.
        This request will return all files in a directory, including files in the gcodes root that do not have a valid gcode extension.

        Args:
            directory (str): Path to the directory.The first part must be a registered root
            extended (str): When set to true metadata will be included in the response for gcode file.Default is set to False
        Returns:
            dict: Returns a list of files and subdirectories given a supplied path.
            Unlike /server/files/list,this command does not walk through subdirectories.
            This request will return all files in a directory,
            including files in the gcodes root that do not have a valid gcode extension
        """
        if not isinstance(directory, str):
            return False
        return self.get_request(
            method=f"/server/files/directory?path={directory}&extended={extended}"
        )

    def get_avaliable_files(self, root: str = "gcodes") -> dict:
        """`GET MoonrakerAPI` /server/files/list?root={root}
        Walks through a directory and fetches all detected files. File names include a path relative to the specified `root`.
        `Note:` The gcodes root will only return files with valid gcode file extensions.

        Args:
            root (str): The name of the root from which a file list should be returned
        Returns:
            dict: The result is an array of File Info objects:
        """
        if not isinstance(root, str):
            return False
        return self.get_request(method=f"/server/files/directory?root={root}")

    def post_upload_file(
        self,
        full_path: str,
        root: Optional[str] = "gcodes",
        path: Optional[str] = "",
    ) -> Response:
        """`POST MoonrakerAPI` /server/files/upload
        Upload a file with `full_path`  to the moonraker server

        Args:
            root (str): The root location in which to upload the file. Currently this may only be gcodes or config. Default is gcodes
            filename (str): name of the file
            path (str): An optional path, relative to the root, indicating a subfolder in which to save the file. If the subfolder does not exist it will be created
        Returns:
            str:  Successful uploads will respond with a 201 response code and set the Location response header to the full path of the uploaded file
        """
        if not isinstance(full_path, str):
            return False

        with open(full_path, "rb") as f:
            file = {
                "file": (os.path.basename(full_path), f, "application/octet-stream")
            }
            data = {
                "root": root,
                "path": path,
                "checksum": sha256_checksum(filepath=full_path),
            }
            return self.post_request(
                method="server/files/upload", files=file, data=data
            )

    def post_create_directory(self, new_dir: str, root: Optional[str] = "gcodes"):
        """`POST MoonrakerAPI` /server/files/directory
        Creates a directory at the specified path

        Args:
            new_dir (str):    The path to the directory to create, including its root. Note that the parent directory must exist. Default is "gcodes"
            root (Optional[str]): The root location in which to upload the file. Currently this may only be gcodes or config. Default is gcodes
        Returns:
            item (dict):  An Item Details object describing the directory created.
            action	(str):    A description of the action taken by the host. Will always be create_dir for this request.

        """
        data = {"path": f"{root}/{new_dir}"}
        return self.post_request(method="server/files/directory", json=data)

    def firmware_restart(self):
        """`POST MoonrakerAPI` /printer/firmware_restart
        Firmware restart to Klipper

        Returns:
            str: Returns an 'ok' from Moonraker
        """
        return self.post_request(method="printer/firmware_restart")

    def post_request(
        self, method, data=None, json=None, json_response=True, files=None
    ):
        """POST request"""
        return self._request(
            request_type="post",
            method=method,
            data=data,
            json=json,
            json_response=json_response,
            file=files,
        )

    def get_request(self, method, json=True, timeout=timeout):
        """GET request"""
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
        file=None,
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
                    files=file,
                )
                if isinstance(response, Response):
                    response.raise_for_status()
                    return response.json() if json_response else response.content

        except Exception as e:
            logging.info(f"Unexpected error while sending HTTP request: {e}")
