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

import requests
from requests import Request, Response

logger = logging.getLogger(__name__)
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


class UncallableError(Exception):
    """Raised when a method is not callable"""

    def __init__(self, message="Unable to call method", errors=None):
        args = [message, errors]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁUncallableErrorǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁUncallableErrorǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁUncallableErrorǁ__init____mutmut_orig(self, message="Unable to call method", errors=None):
        super(UncallableError, self).__init__(message, errors)
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_1(self, message="XXUnable to call methodXX", errors=None):
        super(UncallableError, self).__init__(message, errors)
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_2(self, message="unable to call method", errors=None):
        super(UncallableError, self).__init__(message, errors)
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_3(self, message="UNABLE TO CALL METHOD", errors=None):
        super(UncallableError, self).__init__(message, errors)
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_4(self, message="Unable to call method", errors=None):
        super(UncallableError, self).__init__(None, errors)
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_5(self, message="Unable to call method", errors=None):
        super(UncallableError, self).__init__(message, None)
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_6(self, message="Unable to call method", errors=None):
        super(UncallableError, self).__init__(errors)
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_7(self, message="Unable to call method", errors=None):
        super(UncallableError, self).__init__(message, )
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_8(self, message="Unable to call method", errors=None):
        super(None, self).__init__(message, errors)
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_9(self, message="Unable to call method", errors=None):
        super(UncallableError, None).__init__(message, errors)
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_10(self, message="Unable to call method", errors=None):
        super(self).__init__(message, errors)
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_11(self, message="Unable to call method", errors=None):
        super(UncallableError, ).__init__(message, errors)
        self.errors = errors
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_12(self, message="Unable to call method", errors=None):
        super(UncallableError, self).__init__(message, errors)
        self.errors = None
        self.message = message

    def xǁUncallableErrorǁ__init____mutmut_13(self, message="Unable to call method", errors=None):
        super(UncallableError, self).__init__(message, errors)
        self.errors = errors
        self.message = None
    
    xǁUncallableErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁUncallableErrorǁ__init____mutmut_1': xǁUncallableErrorǁ__init____mutmut_1, 
        'xǁUncallableErrorǁ__init____mutmut_2': xǁUncallableErrorǁ__init____mutmut_2, 
        'xǁUncallableErrorǁ__init____mutmut_3': xǁUncallableErrorǁ__init____mutmut_3, 
        'xǁUncallableErrorǁ__init____mutmut_4': xǁUncallableErrorǁ__init____mutmut_4, 
        'xǁUncallableErrorǁ__init____mutmut_5': xǁUncallableErrorǁ__init____mutmut_5, 
        'xǁUncallableErrorǁ__init____mutmut_6': xǁUncallableErrorǁ__init____mutmut_6, 
        'xǁUncallableErrorǁ__init____mutmut_7': xǁUncallableErrorǁ__init____mutmut_7, 
        'xǁUncallableErrorǁ__init____mutmut_8': xǁUncallableErrorǁ__init____mutmut_8, 
        'xǁUncallableErrorǁ__init____mutmut_9': xǁUncallableErrorǁ__init____mutmut_9, 
        'xǁUncallableErrorǁ__init____mutmut_10': xǁUncallableErrorǁ__init____mutmut_10, 
        'xǁUncallableErrorǁ__init____mutmut_11': xǁUncallableErrorǁ__init____mutmut_11, 
        'xǁUncallableErrorǁ__init____mutmut_12': xǁUncallableErrorǁ__init____mutmut_12, 
        'xǁUncallableErrorǁ__init____mutmut_13': xǁUncallableErrorǁ__init____mutmut_13
    }
    xǁUncallableErrorǁ__init____mutmut_orig.__name__ = 'xǁUncallableErrorǁ__init__'


class MoonRest:
    """MoonRest Basic API for sending end posting requests to MoonrakerAPI

    Raises:
        UncallableError: An error occurred when the request type invalid
    """

    timeout = 3

    def __init__(self, host: str = "localhost", port: int = 7125, api_key=False):
        args = [host, port, api_key]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMoonRestǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁMoonRestǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁMoonRestǁ__init____mutmut_orig(self, host: str = "localhost", port: int = 7125, api_key=False):
        self._host = host
        self._port = port
        self._api_key = api_key

    def xǁMoonRestǁ__init____mutmut_1(self, host: str = "XXlocalhostXX", port: int = 7125, api_key=False):
        self._host = host
        self._port = port
        self._api_key = api_key

    def xǁMoonRestǁ__init____mutmut_2(self, host: str = "LOCALHOST", port: int = 7125, api_key=False):
        self._host = host
        self._port = port
        self._api_key = api_key

    def xǁMoonRestǁ__init____mutmut_3(self, host: str = "localhost", port: int = 7126, api_key=False):
        self._host = host
        self._port = port
        self._api_key = api_key

    def xǁMoonRestǁ__init____mutmut_4(self, host: str = "localhost", port: int = 7125, api_key=True):
        self._host = host
        self._port = port
        self._api_key = api_key

    def xǁMoonRestǁ__init____mutmut_5(self, host: str = "localhost", port: int = 7125, api_key=False):
        self._host = None
        self._port = port
        self._api_key = api_key

    def xǁMoonRestǁ__init____mutmut_6(self, host: str = "localhost", port: int = 7125, api_key=False):
        self._host = host
        self._port = None
        self._api_key = api_key

    def xǁMoonRestǁ__init____mutmut_7(self, host: str = "localhost", port: int = 7125, api_key=False):
        self._host = host
        self._port = port
        self._api_key = None
    
    xǁMoonRestǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMoonRestǁ__init____mutmut_1': xǁMoonRestǁ__init____mutmut_1, 
        'xǁMoonRestǁ__init____mutmut_2': xǁMoonRestǁ__init____mutmut_2, 
        'xǁMoonRestǁ__init____mutmut_3': xǁMoonRestǁ__init____mutmut_3, 
        'xǁMoonRestǁ__init____mutmut_4': xǁMoonRestǁ__init____mutmut_4, 
        'xǁMoonRestǁ__init____mutmut_5': xǁMoonRestǁ__init____mutmut_5, 
        'xǁMoonRestǁ__init____mutmut_6': xǁMoonRestǁ__init____mutmut_6, 
        'xǁMoonRestǁ__init____mutmut_7': xǁMoonRestǁ__init____mutmut_7
    }
    xǁMoonRestǁ__init____mutmut_orig.__name__ = 'xǁMoonRestǁ__init__'

    @property
    def build_endpoint(self):
        """Build connection endpoint"""
        return f"http://{self._host}:{self._port}"

    def get_oneshot_token(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMoonRestǁget_oneshot_token__mutmut_orig'), object.__getattribute__(self, 'xǁMoonRestǁget_oneshot_token__mutmut_mutants'), args, kwargs, self)

    def xǁMoonRestǁget_oneshot_token__mutmut_orig(self):
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

    def xǁMoonRestǁget_oneshot_token__mutmut_1(self):
        """Requests Moonraker API for a oneshot token to be used on
        API key authentication

        Returns:
            str: A oneshot token
        """
        # Response data is generally an object itself, however for some requests this may simply be an "ok" string.
        response = None
        if response is None:
            return None
        return (
            response["result"]
            if isinstance(response, dict) and "result" in response
            else None
        )

    def xǁMoonRestǁget_oneshot_token__mutmut_2(self):
        """Requests Moonraker API for a oneshot token to be used on
        API key authentication

        Returns:
            str: A oneshot token
        """
        # Response data is generally an object itself, however for some requests this may simply be an "ok" string.
        response = self.get_request(method=None)
        if response is None:
            return None
        return (
            response["result"]
            if isinstance(response, dict) and "result" in response
            else None
        )

    def xǁMoonRestǁget_oneshot_token__mutmut_3(self):
        """Requests Moonraker API for a oneshot token to be used on
        API key authentication

        Returns:
            str: A oneshot token
        """
        # Response data is generally an object itself, however for some requests this may simply be an "ok" string.
        response = self.get_request(method="XXaccess/oneshot_tokenXX")
        if response is None:
            return None
        return (
            response["result"]
            if isinstance(response, dict) and "result" in response
            else None
        )

    def xǁMoonRestǁget_oneshot_token__mutmut_4(self):
        """Requests Moonraker API for a oneshot token to be used on
        API key authentication

        Returns:
            str: A oneshot token
        """
        # Response data is generally an object itself, however for some requests this may simply be an "ok" string.
        response = self.get_request(method="ACCESS/ONESHOT_TOKEN")
        if response is None:
            return None
        return (
            response["result"]
            if isinstance(response, dict) and "result" in response
            else None
        )

    def xǁMoonRestǁget_oneshot_token__mutmut_5(self):
        """Requests Moonraker API for a oneshot token to be used on
        API key authentication

        Returns:
            str: A oneshot token
        """
        # Response data is generally an object itself, however for some requests this may simply be an "ok" string.
        response = self.get_request(method="access/oneshot_token")
        if response is not None:
            return None
        return (
            response["result"]
            if isinstance(response, dict) and "result" in response
            else None
        )

    def xǁMoonRestǁget_oneshot_token__mutmut_6(self):
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
            response["XXresultXX"]
            if isinstance(response, dict) and "result" in response
            else None
        )

    def xǁMoonRestǁget_oneshot_token__mutmut_7(self):
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
            response["RESULT"]
            if isinstance(response, dict) and "result" in response
            else None
        )

    def xǁMoonRestǁget_oneshot_token__mutmut_8(self):
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
            if isinstance(response, dict) or "result" in response
            else None
        )

    def xǁMoonRestǁget_oneshot_token__mutmut_9(self):
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
            if isinstance(response, dict) and "XXresultXX" in response
            else None
        )

    def xǁMoonRestǁget_oneshot_token__mutmut_10(self):
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
            if isinstance(response, dict) and "RESULT" in response
            else None
        )

    def xǁMoonRestǁget_oneshot_token__mutmut_11(self):
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
            if isinstance(response, dict) and "result" not in response
            else None
        )
    
    xǁMoonRestǁget_oneshot_token__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMoonRestǁget_oneshot_token__mutmut_1': xǁMoonRestǁget_oneshot_token__mutmut_1, 
        'xǁMoonRestǁget_oneshot_token__mutmut_2': xǁMoonRestǁget_oneshot_token__mutmut_2, 
        'xǁMoonRestǁget_oneshot_token__mutmut_3': xǁMoonRestǁget_oneshot_token__mutmut_3, 
        'xǁMoonRestǁget_oneshot_token__mutmut_4': xǁMoonRestǁget_oneshot_token__mutmut_4, 
        'xǁMoonRestǁget_oneshot_token__mutmut_5': xǁMoonRestǁget_oneshot_token__mutmut_5, 
        'xǁMoonRestǁget_oneshot_token__mutmut_6': xǁMoonRestǁget_oneshot_token__mutmut_6, 
        'xǁMoonRestǁget_oneshot_token__mutmut_7': xǁMoonRestǁget_oneshot_token__mutmut_7, 
        'xǁMoonRestǁget_oneshot_token__mutmut_8': xǁMoonRestǁget_oneshot_token__mutmut_8, 
        'xǁMoonRestǁget_oneshot_token__mutmut_9': xǁMoonRestǁget_oneshot_token__mutmut_9, 
        'xǁMoonRestǁget_oneshot_token__mutmut_10': xǁMoonRestǁget_oneshot_token__mutmut_10, 
        'xǁMoonRestǁget_oneshot_token__mutmut_11': xǁMoonRestǁget_oneshot_token__mutmut_11
    }
    xǁMoonRestǁget_oneshot_token__mutmut_orig.__name__ = 'xǁMoonRestǁget_oneshot_token'

    def get_server_info(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMoonRestǁget_server_info__mutmut_orig'), object.__getattribute__(self, 'xǁMoonRestǁget_server_info__mutmut_mutants'), args, kwargs, self)

    def xǁMoonRestǁget_server_info__mutmut_orig(self):
        """GET MoonrakerAPI /server/info

        Returns:
            dict: server info from Moonraker
        """
        return self.get_request(method="server/info")

    def xǁMoonRestǁget_server_info__mutmut_1(self):
        """GET MoonrakerAPI /server/info

        Returns:
            dict: server info from Moonraker
        """
        return self.get_request(method=None)

    def xǁMoonRestǁget_server_info__mutmut_2(self):
        """GET MoonrakerAPI /server/info

        Returns:
            dict: server info from Moonraker
        """
        return self.get_request(method="XXserver/infoXX")

    def xǁMoonRestǁget_server_info__mutmut_3(self):
        """GET MoonrakerAPI /server/info

        Returns:
            dict: server info from Moonraker
        """
        return self.get_request(method="SERVER/INFO")
    
    xǁMoonRestǁget_server_info__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMoonRestǁget_server_info__mutmut_1': xǁMoonRestǁget_server_info__mutmut_1, 
        'xǁMoonRestǁget_server_info__mutmut_2': xǁMoonRestǁget_server_info__mutmut_2, 
        'xǁMoonRestǁget_server_info__mutmut_3': xǁMoonRestǁget_server_info__mutmut_3
    }
    xǁMoonRestǁget_server_info__mutmut_orig.__name__ = 'xǁMoonRestǁget_server_info'

    def get_spool(self, spool_id: int) -> dict | None:
        args = [spool_id]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMoonRestǁget_spool__mutmut_orig'), object.__getattribute__(self, 'xǁMoonRestǁget_spool__mutmut_mutants'), args, kwargs, self)

    def xǁMoonRestǁget_spool__mutmut_orig(self, spool_id: int) -> dict | None:
        """GET /server/spoolman/spool/{spool_id} via Moonraker

        Returns spool dict on success, None on HTTP/network/JSON error.
        """
        response = self.get_request(f"server/spoolman/spool/{spool_id}")
        if not isinstance(response, dict):
            return None
        return response.get("result")

    def xǁMoonRestǁget_spool__mutmut_1(self, spool_id: int) -> dict | None:
        """GET /server/spoolman/spool/{spool_id} via Moonraker

        Returns spool dict on success, None on HTTP/network/JSON error.
        """
        response = None
        if not isinstance(response, dict):
            return None
        return response.get("result")

    def xǁMoonRestǁget_spool__mutmut_2(self, spool_id: int) -> dict | None:
        """GET /server/spoolman/spool/{spool_id} via Moonraker

        Returns spool dict on success, None on HTTP/network/JSON error.
        """
        response = self.get_request(None)
        if not isinstance(response, dict):
            return None
        return response.get("result")

    def xǁMoonRestǁget_spool__mutmut_3(self, spool_id: int) -> dict | None:
        """GET /server/spoolman/spool/{spool_id} via Moonraker

        Returns spool dict on success, None on HTTP/network/JSON error.
        """
        response = self.get_request(f"server/spoolman/spool/{spool_id}")
        if isinstance(response, dict):
            return None
        return response.get("result")

    def xǁMoonRestǁget_spool__mutmut_4(self, spool_id: int) -> dict | None:
        """GET /server/spoolman/spool/{spool_id} via Moonraker

        Returns spool dict on success, None on HTTP/network/JSON error.
        """
        response = self.get_request(f"server/spoolman/spool/{spool_id}")
        if not isinstance(response, dict):
            return None
        return response.get(None)

    def xǁMoonRestǁget_spool__mutmut_5(self, spool_id: int) -> dict | None:
        """GET /server/spoolman/spool/{spool_id} via Moonraker

        Returns spool dict on success, None on HTTP/network/JSON error.
        """
        response = self.get_request(f"server/spoolman/spool/{spool_id}")
        if not isinstance(response, dict):
            return None
        return response.get("XXresultXX")

    def xǁMoonRestǁget_spool__mutmut_6(self, spool_id: int) -> dict | None:
        """GET /server/spoolman/spool/{spool_id} via Moonraker

        Returns spool dict on success, None on HTTP/network/JSON error.
        """
        response = self.get_request(f"server/spoolman/spool/{spool_id}")
        if not isinstance(response, dict):
            return None
        return response.get("RESULT")
    
    xǁMoonRestǁget_spool__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMoonRestǁget_spool__mutmut_1': xǁMoonRestǁget_spool__mutmut_1, 
        'xǁMoonRestǁget_spool__mutmut_2': xǁMoonRestǁget_spool__mutmut_2, 
        'xǁMoonRestǁget_spool__mutmut_3': xǁMoonRestǁget_spool__mutmut_3, 
        'xǁMoonRestǁget_spool__mutmut_4': xǁMoonRestǁget_spool__mutmut_4, 
        'xǁMoonRestǁget_spool__mutmut_5': xǁMoonRestǁget_spool__mutmut_5, 
        'xǁMoonRestǁget_spool__mutmut_6': xǁMoonRestǁget_spool__mutmut_6
    }
    xǁMoonRestǁget_spool__mutmut_orig.__name__ = 'xǁMoonRestǁget_spool'

    def set_spool_used_weight(self, spool_id: int, weight: float) -> bool:
        args = [spool_id, weight]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMoonRestǁset_spool_used_weight__mutmut_orig'), object.__getattribute__(self, 'xǁMoonRestǁset_spool_used_weight__mutmut_mutants'), args, kwargs, self)

    def xǁMoonRestǁset_spool_used_weight__mutmut_orig(self, spool_id: int, weight: float) -> bool:
        """POST /server/spoolman/spool/{spool_id} to update used_weight.

        Returns True on sucess, False on any error.
        """
        response = self.post_request(
            f"server/spoolman/spool/{spool_id}", json={"used_weight": weight}
        )
        return response is not None

    def xǁMoonRestǁset_spool_used_weight__mutmut_1(self, spool_id: int, weight: float) -> bool:
        """POST /server/spoolman/spool/{spool_id} to update used_weight.

        Returns True on sucess, False on any error.
        """
        response = None
        return response is not None

    def xǁMoonRestǁset_spool_used_weight__mutmut_2(self, spool_id: int, weight: float) -> bool:
        """POST /server/spoolman/spool/{spool_id} to update used_weight.

        Returns True on sucess, False on any error.
        """
        response = self.post_request(
            None, json={"used_weight": weight}
        )
        return response is not None

    def xǁMoonRestǁset_spool_used_weight__mutmut_3(self, spool_id: int, weight: float) -> bool:
        """POST /server/spoolman/spool/{spool_id} to update used_weight.

        Returns True on sucess, False on any error.
        """
        response = self.post_request(
            f"server/spoolman/spool/{spool_id}", json=None
        )
        return response is not None

    def xǁMoonRestǁset_spool_used_weight__mutmut_4(self, spool_id: int, weight: float) -> bool:
        """POST /server/spoolman/spool/{spool_id} to update used_weight.

        Returns True on sucess, False on any error.
        """
        response = self.post_request(
            json={"used_weight": weight}
        )
        return response is not None

    def xǁMoonRestǁset_spool_used_weight__mutmut_5(self, spool_id: int, weight: float) -> bool:
        """POST /server/spoolman/spool/{spool_id} to update used_weight.

        Returns True on sucess, False on any error.
        """
        response = self.post_request(
            f"server/spoolman/spool/{spool_id}", )
        return response is not None

    def xǁMoonRestǁset_spool_used_weight__mutmut_6(self, spool_id: int, weight: float) -> bool:
        """POST /server/spoolman/spool/{spool_id} to update used_weight.

        Returns True on sucess, False on any error.
        """
        response = self.post_request(
            f"server/spoolman/spool/{spool_id}", json={"XXused_weightXX": weight}
        )
        return response is not None

    def xǁMoonRestǁset_spool_used_weight__mutmut_7(self, spool_id: int, weight: float) -> bool:
        """POST /server/spoolman/spool/{spool_id} to update used_weight.

        Returns True on sucess, False on any error.
        """
        response = self.post_request(
            f"server/spoolman/spool/{spool_id}", json={"USED_WEIGHT": weight}
        )
        return response is not None

    def xǁMoonRestǁset_spool_used_weight__mutmut_8(self, spool_id: int, weight: float) -> bool:
        """POST /server/spoolman/spool/{spool_id} to update used_weight.

        Returns True on sucess, False on any error.
        """
        response = self.post_request(
            f"server/spoolman/spool/{spool_id}", json={"used_weight": weight}
        )
        return response is None
    
    xǁMoonRestǁset_spool_used_weight__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMoonRestǁset_spool_used_weight__mutmut_1': xǁMoonRestǁset_spool_used_weight__mutmut_1, 
        'xǁMoonRestǁset_spool_used_weight__mutmut_2': xǁMoonRestǁset_spool_used_weight__mutmut_2, 
        'xǁMoonRestǁset_spool_used_weight__mutmut_3': xǁMoonRestǁset_spool_used_weight__mutmut_3, 
        'xǁMoonRestǁset_spool_used_weight__mutmut_4': xǁMoonRestǁset_spool_used_weight__mutmut_4, 
        'xǁMoonRestǁset_spool_used_weight__mutmut_5': xǁMoonRestǁset_spool_used_weight__mutmut_5, 
        'xǁMoonRestǁset_spool_used_weight__mutmut_6': xǁMoonRestǁset_spool_used_weight__mutmut_6, 
        'xǁMoonRestǁset_spool_used_weight__mutmut_7': xǁMoonRestǁset_spool_used_weight__mutmut_7, 
        'xǁMoonRestǁset_spool_used_weight__mutmut_8': xǁMoonRestǁset_spool_used_weight__mutmut_8
    }
    xǁMoonRestǁset_spool_used_weight__mutmut_orig.__name__ = 'xǁMoonRestǁset_spool_used_weight'

    def firmware_restart(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMoonRestǁfirmware_restart__mutmut_orig'), object.__getattribute__(self, 'xǁMoonRestǁfirmware_restart__mutmut_mutants'), args, kwargs, self)

    def xǁMoonRestǁfirmware_restart__mutmut_orig(self):
        """firmware_restart
            POST to /printer/firmware_restart to firmware restart Klipper

        Returns:
            str: Returns an 'ok' from Moonraker
        """
        return self.post_request(method="printer/firmware_restart")

    def xǁMoonRestǁfirmware_restart__mutmut_1(self):
        """firmware_restart
            POST to /printer/firmware_restart to firmware restart Klipper

        Returns:
            str: Returns an 'ok' from Moonraker
        """
        return self.post_request(method=None)

    def xǁMoonRestǁfirmware_restart__mutmut_2(self):
        """firmware_restart
            POST to /printer/firmware_restart to firmware restart Klipper

        Returns:
            str: Returns an 'ok' from Moonraker
        """
        return self.post_request(method="XXprinter/firmware_restartXX")

    def xǁMoonRestǁfirmware_restart__mutmut_3(self):
        """firmware_restart
            POST to /printer/firmware_restart to firmware restart Klipper

        Returns:
            str: Returns an 'ok' from Moonraker
        """
        return self.post_request(method="PRINTER/FIRMWARE_RESTART")
    
    xǁMoonRestǁfirmware_restart__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMoonRestǁfirmware_restart__mutmut_1': xǁMoonRestǁfirmware_restart__mutmut_1, 
        'xǁMoonRestǁfirmware_restart__mutmut_2': xǁMoonRestǁfirmware_restart__mutmut_2, 
        'xǁMoonRestǁfirmware_restart__mutmut_3': xǁMoonRestǁfirmware_restart__mutmut_3
    }
    xǁMoonRestǁfirmware_restart__mutmut_orig.__name__ = 'xǁMoonRestǁfirmware_restart'

    def post_request(self, method, data=None, json=None, json_response=True):
        args = [method, data, json, json_response]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMoonRestǁpost_request__mutmut_orig'), object.__getattribute__(self, 'xǁMoonRestǁpost_request__mutmut_mutants'), args, kwargs, self)

    def xǁMoonRestǁpost_request__mutmut_orig(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="post",
            method=method,
            data=data,
            json=json,
            json_response=json_response,
        )

    def xǁMoonRestǁpost_request__mutmut_1(self, method, data=None, json=None, json_response=False):
        """POST request"""
        return self._request(
            request_type="post",
            method=method,
            data=data,
            json=json,
            json_response=json_response,
        )

    def xǁMoonRestǁpost_request__mutmut_2(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type=None,
            method=method,
            data=data,
            json=json,
            json_response=json_response,
        )

    def xǁMoonRestǁpost_request__mutmut_3(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="post",
            method=None,
            data=data,
            json=json,
            json_response=json_response,
        )

    def xǁMoonRestǁpost_request__mutmut_4(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="post",
            method=method,
            data=None,
            json=json,
            json_response=json_response,
        )

    def xǁMoonRestǁpost_request__mutmut_5(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="post",
            method=method,
            data=data,
            json=None,
            json_response=json_response,
        )

    def xǁMoonRestǁpost_request__mutmut_6(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="post",
            method=method,
            data=data,
            json=json,
            json_response=None,
        )

    def xǁMoonRestǁpost_request__mutmut_7(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            method=method,
            data=data,
            json=json,
            json_response=json_response,
        )

    def xǁMoonRestǁpost_request__mutmut_8(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="post",
            data=data,
            json=json,
            json_response=json_response,
        )

    def xǁMoonRestǁpost_request__mutmut_9(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="post",
            method=method,
            json=json,
            json_response=json_response,
        )

    def xǁMoonRestǁpost_request__mutmut_10(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="post",
            method=method,
            data=data,
            json_response=json_response,
        )

    def xǁMoonRestǁpost_request__mutmut_11(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="post",
            method=method,
            data=data,
            json=json,
            )

    def xǁMoonRestǁpost_request__mutmut_12(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="XXpostXX",
            method=method,
            data=data,
            json=json,
            json_response=json_response,
        )

    def xǁMoonRestǁpost_request__mutmut_13(self, method, data=None, json=None, json_response=True):
        """POST request"""
        return self._request(
            request_type="POST",
            method=method,
            data=data,
            json=json,
            json_response=json_response,
        )
    
    xǁMoonRestǁpost_request__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMoonRestǁpost_request__mutmut_1': xǁMoonRestǁpost_request__mutmut_1, 
        'xǁMoonRestǁpost_request__mutmut_2': xǁMoonRestǁpost_request__mutmut_2, 
        'xǁMoonRestǁpost_request__mutmut_3': xǁMoonRestǁpost_request__mutmut_3, 
        'xǁMoonRestǁpost_request__mutmut_4': xǁMoonRestǁpost_request__mutmut_4, 
        'xǁMoonRestǁpost_request__mutmut_5': xǁMoonRestǁpost_request__mutmut_5, 
        'xǁMoonRestǁpost_request__mutmut_6': xǁMoonRestǁpost_request__mutmut_6, 
        'xǁMoonRestǁpost_request__mutmut_7': xǁMoonRestǁpost_request__mutmut_7, 
        'xǁMoonRestǁpost_request__mutmut_8': xǁMoonRestǁpost_request__mutmut_8, 
        'xǁMoonRestǁpost_request__mutmut_9': xǁMoonRestǁpost_request__mutmut_9, 
        'xǁMoonRestǁpost_request__mutmut_10': xǁMoonRestǁpost_request__mutmut_10, 
        'xǁMoonRestǁpost_request__mutmut_11': xǁMoonRestǁpost_request__mutmut_11, 
        'xǁMoonRestǁpost_request__mutmut_12': xǁMoonRestǁpost_request__mutmut_12, 
        'xǁMoonRestǁpost_request__mutmut_13': xǁMoonRestǁpost_request__mutmut_13
    }
    xǁMoonRestǁpost_request__mutmut_orig.__name__ = 'xǁMoonRestǁpost_request'

    def get_request(self, method, json=True, timeout=timeout):
        args = [method, json, timeout]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMoonRestǁget_request__mutmut_orig'), object.__getattribute__(self, 'xǁMoonRestǁget_request__mutmut_mutants'), args, kwargs, self)

    def xǁMoonRestǁget_request__mutmut_orig(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            request_type="get",
            method=method,
            json_response=json,
            timeout=timeout,
        )

    def xǁMoonRestǁget_request__mutmut_1(self, method, json=False, timeout=timeout):
        """GET request"""
        return self._request(
            request_type="get",
            method=method,
            json_response=json,
            timeout=timeout,
        )

    def xǁMoonRestǁget_request__mutmut_2(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            request_type=None,
            method=method,
            json_response=json,
            timeout=timeout,
        )

    def xǁMoonRestǁget_request__mutmut_3(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            request_type="get",
            method=None,
            json_response=json,
            timeout=timeout,
        )

    def xǁMoonRestǁget_request__mutmut_4(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            request_type="get",
            method=method,
            json_response=None,
            timeout=timeout,
        )

    def xǁMoonRestǁget_request__mutmut_5(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            request_type="get",
            method=method,
            json_response=json,
            timeout=None,
        )

    def xǁMoonRestǁget_request__mutmut_6(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            method=method,
            json_response=json,
            timeout=timeout,
        )

    def xǁMoonRestǁget_request__mutmut_7(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            request_type="get",
            json_response=json,
            timeout=timeout,
        )

    def xǁMoonRestǁget_request__mutmut_8(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            request_type="get",
            method=method,
            timeout=timeout,
        )

    def xǁMoonRestǁget_request__mutmut_9(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            request_type="get",
            method=method,
            json_response=json,
            )

    def xǁMoonRestǁget_request__mutmut_10(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            request_type="XXgetXX",
            method=method,
            json_response=json,
            timeout=timeout,
        )

    def xǁMoonRestǁget_request__mutmut_11(self, method, json=True, timeout=timeout):
        """GET request"""
        return self._request(
            request_type="GET",
            method=method,
            json_response=json,
            timeout=timeout,
        )
    
    xǁMoonRestǁget_request__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMoonRestǁget_request__mutmut_1': xǁMoonRestǁget_request__mutmut_1, 
        'xǁMoonRestǁget_request__mutmut_2': xǁMoonRestǁget_request__mutmut_2, 
        'xǁMoonRestǁget_request__mutmut_3': xǁMoonRestǁget_request__mutmut_3, 
        'xǁMoonRestǁget_request__mutmut_4': xǁMoonRestǁget_request__mutmut_4, 
        'xǁMoonRestǁget_request__mutmut_5': xǁMoonRestǁget_request__mutmut_5, 
        'xǁMoonRestǁget_request__mutmut_6': xǁMoonRestǁget_request__mutmut_6, 
        'xǁMoonRestǁget_request__mutmut_7': xǁMoonRestǁget_request__mutmut_7, 
        'xǁMoonRestǁget_request__mutmut_8': xǁMoonRestǁget_request__mutmut_8, 
        'xǁMoonRestǁget_request__mutmut_9': xǁMoonRestǁget_request__mutmut_9, 
        'xǁMoonRestǁget_request__mutmut_10': xǁMoonRestǁget_request__mutmut_10, 
        'xǁMoonRestǁget_request__mutmut_11': xǁMoonRestǁget_request__mutmut_11
    }
    xǁMoonRestǁget_request__mutmut_orig.__name__ = 'xǁMoonRestǁget_request'

    def _request(
        self,
        request_type,
        method,
        data=None,
        json=None,
        json_response=True,
        timeout=timeout,
    ):
        args = [request_type, method, data, json, json_response, timeout]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁMoonRestǁ_request__mutmut_orig'), object.__getattribute__(self, 'xǁMoonRestǁ_request__mutmut_mutants'), args, kwargs, self)

    def xǁMoonRestǁ_request__mutmut_orig(
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

    def xǁMoonRestǁ_request__mutmut_1(
        self,
        request_type,
        method,
        data=None,
        json=None,
        json_response=False,
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

    def xǁMoonRestǁ_request__mutmut_2(
        self,
        request_type,
        method,
        data=None,
        json=None,
        json_response=True,
        timeout=timeout,
    ):
        _url = None
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

    def xǁMoonRestǁ_request__mutmut_3(
        self,
        request_type,
        method,
        data=None,
        json=None,
        json_response=True,
        timeout=timeout,
    ):
        _url = f"{self.build_endpoint}/{method}"
        _headers = None
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

    def xǁMoonRestǁ_request__mutmut_4(
        self,
        request_type,
        method,
        data=None,
        json=None,
        json_response=True,
        timeout=timeout,
    ):
        _url = f"{self.build_endpoint}/{method}"
        _headers = {"XXx-api-keyXX": self._api_key} if self._api_key else {}
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

    def xǁMoonRestǁ_request__mutmut_5(
        self,
        request_type,
        method,
        data=None,
        json=None,
        json_response=True,
        timeout=timeout,
    ):
        _url = f"{self.build_endpoint}/{method}"
        _headers = {"X-API-KEY": self._api_key} if self._api_key else {}
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

    def xǁMoonRestǁ_request__mutmut_6(
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
            if hasattr(None, request_type):
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

    def xǁMoonRestǁ_request__mutmut_7(
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
            if hasattr(requests, None):
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

    def xǁMoonRestǁ_request__mutmut_8(
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
            if hasattr(request_type):
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

    def xǁMoonRestǁ_request__mutmut_9(
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
            if hasattr(requests, ):
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

    def xǁMoonRestǁ_request__mutmut_10(
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
                _request_method: Request = None
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

    def xǁMoonRestǁ_request__mutmut_11(
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
                _request_method: Request = getattr(None, request_type)
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

    def xǁMoonRestǁ_request__mutmut_12(
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
                _request_method: Request = getattr(requests, None)
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

    def xǁMoonRestǁ_request__mutmut_13(
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
                _request_method: Request = getattr(request_type)
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

    def xǁMoonRestǁ_request__mutmut_14(
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
                _request_method: Request = getattr(requests, )
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

    def xǁMoonRestǁ_request__mutmut_15(
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
                if callable(_request_method):
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

    def xǁMoonRestǁ_request__mutmut_16(
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
                if not callable(None):
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

    def xǁMoonRestǁ_request__mutmut_17(
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
                        None,
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

    def xǁMoonRestǁ_request__mutmut_18(
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
                        None,
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

    def xǁMoonRestǁ_request__mutmut_19(
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

    def xǁMoonRestǁ_request__mutmut_20(
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

    def xǁMoonRestǁ_request__mutmut_21(
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
                        "XXInvalid request methodXX",
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

    def xǁMoonRestǁ_request__mutmut_22(
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
                        "invalid request method",
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

    def xǁMoonRestǁ_request__mutmut_23(
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
                        "INVALID REQUEST METHOD",
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

    def xǁMoonRestǁ_request__mutmut_24(
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

                response = None
                if isinstance(response, Response):
                    response.raise_for_status()
                    return response.json() if json_response else response.content

        except Exception as e:
            logger.info(f"Unexpected error while sending HTTP request: {e}")

    def xǁMoonRestǁ_request__mutmut_25(
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
                    None,
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

    def xǁMoonRestǁ_request__mutmut_26(
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
                    json=None,
                    data=data,
                    headers=_headers,
                    timeout=timeout,
                )
                if isinstance(response, Response):
                    response.raise_for_status()
                    return response.json() if json_response else response.content

        except Exception as e:
            logger.info(f"Unexpected error while sending HTTP request: {e}")

    def xǁMoonRestǁ_request__mutmut_27(
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
                    data=None,
                    headers=_headers,
                    timeout=timeout,
                )
                if isinstance(response, Response):
                    response.raise_for_status()
                    return response.json() if json_response else response.content

        except Exception as e:
            logger.info(f"Unexpected error while sending HTTP request: {e}")

    def xǁMoonRestǁ_request__mutmut_28(
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
                    headers=None,
                    timeout=timeout,
                )
                if isinstance(response, Response):
                    response.raise_for_status()
                    return response.json() if json_response else response.content

        except Exception as e:
            logger.info(f"Unexpected error while sending HTTP request: {e}")

    def xǁMoonRestǁ_request__mutmut_29(
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
                    timeout=None,
                )
                if isinstance(response, Response):
                    response.raise_for_status()
                    return response.json() if json_response else response.content

        except Exception as e:
            logger.info(f"Unexpected error while sending HTTP request: {e}")

    def xǁMoonRestǁ_request__mutmut_30(
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

    def xǁMoonRestǁ_request__mutmut_31(
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
                    data=data,
                    headers=_headers,
                    timeout=timeout,
                )
                if isinstance(response, Response):
                    response.raise_for_status()
                    return response.json() if json_response else response.content

        except Exception as e:
            logger.info(f"Unexpected error while sending HTTP request: {e}")

    def xǁMoonRestǁ_request__mutmut_32(
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
                    headers=_headers,
                    timeout=timeout,
                )
                if isinstance(response, Response):
                    response.raise_for_status()
                    return response.json() if json_response else response.content

        except Exception as e:
            logger.info(f"Unexpected error while sending HTTP request: {e}")

    def xǁMoonRestǁ_request__mutmut_33(
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
                    timeout=timeout,
                )
                if isinstance(response, Response):
                    response.raise_for_status()
                    return response.json() if json_response else response.content

        except Exception as e:
            logger.info(f"Unexpected error while sending HTTP request: {e}")

    def xǁMoonRestǁ_request__mutmut_34(
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
                    )
                if isinstance(response, Response):
                    response.raise_for_status()
                    return response.json() if json_response else response.content

        except Exception as e:
            logger.info(f"Unexpected error while sending HTTP request: {e}")

    def xǁMoonRestǁ_request__mutmut_35(
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
            logger.info(None)
    
    xǁMoonRestǁ_request__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁMoonRestǁ_request__mutmut_1': xǁMoonRestǁ_request__mutmut_1, 
        'xǁMoonRestǁ_request__mutmut_2': xǁMoonRestǁ_request__mutmut_2, 
        'xǁMoonRestǁ_request__mutmut_3': xǁMoonRestǁ_request__mutmut_3, 
        'xǁMoonRestǁ_request__mutmut_4': xǁMoonRestǁ_request__mutmut_4, 
        'xǁMoonRestǁ_request__mutmut_5': xǁMoonRestǁ_request__mutmut_5, 
        'xǁMoonRestǁ_request__mutmut_6': xǁMoonRestǁ_request__mutmut_6, 
        'xǁMoonRestǁ_request__mutmut_7': xǁMoonRestǁ_request__mutmut_7, 
        'xǁMoonRestǁ_request__mutmut_8': xǁMoonRestǁ_request__mutmut_8, 
        'xǁMoonRestǁ_request__mutmut_9': xǁMoonRestǁ_request__mutmut_9, 
        'xǁMoonRestǁ_request__mutmut_10': xǁMoonRestǁ_request__mutmut_10, 
        'xǁMoonRestǁ_request__mutmut_11': xǁMoonRestǁ_request__mutmut_11, 
        'xǁMoonRestǁ_request__mutmut_12': xǁMoonRestǁ_request__mutmut_12, 
        'xǁMoonRestǁ_request__mutmut_13': xǁMoonRestǁ_request__mutmut_13, 
        'xǁMoonRestǁ_request__mutmut_14': xǁMoonRestǁ_request__mutmut_14, 
        'xǁMoonRestǁ_request__mutmut_15': xǁMoonRestǁ_request__mutmut_15, 
        'xǁMoonRestǁ_request__mutmut_16': xǁMoonRestǁ_request__mutmut_16, 
        'xǁMoonRestǁ_request__mutmut_17': xǁMoonRestǁ_request__mutmut_17, 
        'xǁMoonRestǁ_request__mutmut_18': xǁMoonRestǁ_request__mutmut_18, 
        'xǁMoonRestǁ_request__mutmut_19': xǁMoonRestǁ_request__mutmut_19, 
        'xǁMoonRestǁ_request__mutmut_20': xǁMoonRestǁ_request__mutmut_20, 
        'xǁMoonRestǁ_request__mutmut_21': xǁMoonRestǁ_request__mutmut_21, 
        'xǁMoonRestǁ_request__mutmut_22': xǁMoonRestǁ_request__mutmut_22, 
        'xǁMoonRestǁ_request__mutmut_23': xǁMoonRestǁ_request__mutmut_23, 
        'xǁMoonRestǁ_request__mutmut_24': xǁMoonRestǁ_request__mutmut_24, 
        'xǁMoonRestǁ_request__mutmut_25': xǁMoonRestǁ_request__mutmut_25, 
        'xǁMoonRestǁ_request__mutmut_26': xǁMoonRestǁ_request__mutmut_26, 
        'xǁMoonRestǁ_request__mutmut_27': xǁMoonRestǁ_request__mutmut_27, 
        'xǁMoonRestǁ_request__mutmut_28': xǁMoonRestǁ_request__mutmut_28, 
        'xǁMoonRestǁ_request__mutmut_29': xǁMoonRestǁ_request__mutmut_29, 
        'xǁMoonRestǁ_request__mutmut_30': xǁMoonRestǁ_request__mutmut_30, 
        'xǁMoonRestǁ_request__mutmut_31': xǁMoonRestǁ_request__mutmut_31, 
        'xǁMoonRestǁ_request__mutmut_32': xǁMoonRestǁ_request__mutmut_32, 
        'xǁMoonRestǁ_request__mutmut_33': xǁMoonRestǁ_request__mutmut_33, 
        'xǁMoonRestǁ_request__mutmut_34': xǁMoonRestǁ_request__mutmut_34, 
        'xǁMoonRestǁ_request__mutmut_35': xǁMoonRestǁ_request__mutmut_35
    }
    xǁMoonRestǁ_request__mutmut_orig.__name__ = 'xǁMoonRestǁ_request'
