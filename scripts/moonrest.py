# -*- coding: utf-8 -*-
import logging
import requests


# logging.basicConfig(format="'%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s",

#                     filename=r"E:\gitHub\Blocks_Screen\logFile.log", encoding="utf-8", level=logging.DEBUG)
# _logger = logging.getLogger(__name__)
class MoonRest():

    """ MoonRest Basic API for sending end posting requests to MoonrakerAPI
    
        -Credit goes to from Klipper Screen project
            https://github.com/KlipperScreen/KlipperScreen
            https://github.com/KlipperScreen/KlipperScreen/blob/a32d1d8e8085724068ac6a43adbba9757228aebb/ks_includes/KlippyRest.py

        Raises:
            UncallableError: An error ocurred when the request type invalid
    """

    timeout = 3
    def __init__(self, ip="localhost",port="7125", api_key=False ):
        self._ip = ip
        self._port = port
        self._api_key = api_key
        
    @property
    def build_endpoint(self):
        # TODO: Need to also account for if the port is https
        return f"http://{self._ip}:{self._port}"

    def get_oneshot_token(self):
        """get_oneshot_token 
            Requests Moonraker API for a oneshot token to be used on API key authentication

        Returns:
            str: A oneshot token
        """        
        # Response data is generally an object itself, however for some requests this may simply be an "ok" string.
        response = self.get_request(method="access/oneshot_token")
        return response['result'] if 'result' in response else False


    def get_server_info(self):
        """get_server_info 
            GET MoonrakerAPI /server/info

        Returns:
            dict: server info from Moonraker
        """
        return self.get_request(method="server/info")
    
    def upload_file(self):
        # TODO: Create a upload file method, it can only be made using HTTP request.
        pass
    
    def delete_request(self):
        # TODO: Create a delete request, so the user is able to delete files from the pi, can also be made with websockets
        pass

    def post_request(self, method, data=None, json=None, json_response = True):
        return self._request(request_type="post", method=method, data=data, json=json, json_response=json_response)

    def get_request(self, method, json=True, timeout=timeout):
        return self._request(request_type="get", method=method, json_response=json, timeout=timeout)

    def _request(self,request_type, method, data=None,json=None, json_response = True, timeout=timeout):
        _url = f"{self.build_endpoint}/{method}"
        _headers = {"x-api-key": self._api_key} if self._api_key else {}
        logging.debug(f"Sending request {method} to {_url}.")
        try:
            _request_method = getattr(requests, request_type)
            if not callable(_request_method):
                raise UncallableError("Invalid request method", f"Request method '{request_type}' is not callable.")
            
            response = _request_method(_url, json=json, data=data, headers=_headers, timeout=timeout)
            # Check if request was successfull
            response.raise_for_status()

            return response.json() if json_response else response.content

        except Exception as e:
            logging.error(f"Error on http request: {e}")


class UncallableError(Exception):
    def __init__(self, message, errors, *args):
        self.errors = errors
        self.message = message
        
        super(UncallableError, self).__init__(message, errors, *args)
    