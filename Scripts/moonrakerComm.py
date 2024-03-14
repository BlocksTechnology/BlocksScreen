#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals, annotations
import threading
import json
import logging
import sys
import websocket
import json
from time import monotonic as monotonic_time
from threading import Timer

import json
from util import RepeatedTimer
from moonrest import MoonRest


# My Logger object
logging.basicConfig(format="'%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s",
                    filename=r"E:\gitHub\Blocks_Screen\logFile.log", encoding="utf-8", level=logging.DEBUG)
_logger = logging.getLogger(__name__)

# TODO: make host, port and websocket name not static but a argument that can be feed in the class
class MoonWebSocket(threading.Thread):   
     
    connected = False
    connecting = True
    callback_table={}
    _reconnect_count=0
    max_retries=3
    timeout=3
    
    def __init__(self, moonRest):
        # * Both lines bellow are the same shit i guess
        super(MoonWebSocket, self).__init__()
        self.daemon = True
        self.host: str=None
        self.port: int = None
        self.ws: websocket.WebSocketApp = None
        self._callback = None
        self._wst= None
        self._request_id= 0
        
        self._moonRest = moonRest
        
        self._retry_timer: RepeatedTimer =  None
        # ! Websocket options
        websocket.enableTrace(True)
        websocket.setdefaulttimeout(self.timeout)
        
        # Events
        self.connectEvent = threading.Event()
        self.connectingEvent = threading.Event()
        self.disconnectEvent = threading.Event()
    
    def retry(self):
        _logger.info("Retrying connection.")
        
        self._reconnect_count = 0
        self.try_connection()
        
    # TODO: isinstance for each type
    def try_connection(self):
        self.connecting = True
        self.connectEvent.set()
        self._retry_timer = RepeatedTimer(self.timeout, self.reconnect)
        return self.connect()
        
    def reconnect(self):    
        if self.connected:
            return True
        
        if self._reconnect_count >= self.max_retries:
            self._retry_timer.stopTimer()
            _logger.debug("Max number of connection retries reached.")
            _logger.info("Could not connect to moonraker.")
            return False
        _logger.info("Retrying connection to moonraker websocket.")
                    
        return self.connect() # OR in the future maybe an event or something, a callback for example 

    def connect(self):
        if self.connected:
            _logger.debug("Connection already established.")
            return True
        self._reconnect_count += 1
        _logger.debug(f"Connect try number:{self._reconnect_count}")
        
        # Request oneshot token
        # TODO Handle if i cannot connect to moonraker, request server.info and see if i get a result
        try:
            _oneshot_token = self._moonRest.get_oneshot_token()
            
        except Exception as e:
            _logger.debug("Unable to get oneshot token")
            return False
        print(_oneshot_token)
        self.ws = websocket.WebSocketApp(
            f"ws://localhost:7125/websocket?token={_oneshot_token}",
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            on_message=self.on_message
        )
        
        _kwargs = {'reconnect' : self.timeout}
        self._wst = threading.Thread(name="websocket.run_forever",
                                     target=self.ws.run_forever, 
                                     daemon=True)#, kwargs=_kwargs)             
        try:
            _logger.info("Starting websocket.")
            _logger.debug(self.ws.url)
            self._wst.start()
        except Exception as e:
            _logger.info(e, exc_info=True)
            _logger.debug(f"Error starting websocket: {e}")
            return False
        return True
    
    # TODO: messages from *args, and pass it to other variables.
    def disconnect(self):
        # TODO: Handle disconnect or close state 
        self.ws.close() 
        # _logger.info("Socket disconnected:")

    def on_message(self, *args): # ws, message):
        # TODO: Handle receiving message from websocket
        # First argument is ws second is message
        _message = args[1] if len(args) == 2 else args[0]
        _logger.debug(f"Message received from websocket: {_message}")
        
    
    def on_error(self, *args):# ws, error):
        # First argument is ws second is error message 
        _error = args[1] if len(args) == 2 else args[0]
        # TODO: Handle error messages
        # _logger.info(f"Websocket error:{_error}")
        # if self.connecting is True:
        # print("GO teheh")
        # print("ERROR" + str(self._retry_timer.is_alive()))
        
        self.connected = False
        
    def on_close(self, *args):
        # First argument is ws, second is close status code, third is close message
        _close_status_code = args[1] if len(args) == 3 else None
        _close_message = args[2] if len(args) == 3 else None
        # _close_status_code, _close_message = args[1],args[2] if len(args) == 3 else None, None
        self.connected = False
        self.ws.keep_running = False
        # self.reconnect()
        
        _logger.info(f"Websocket closed, code: {_close_status_code}, message: {_close_message}")

    def on_open(self, *args):
        # TODO: Handle initial connection as per moonraker api documentation
        _ws = args[0] if len(args) == 1 else None
        _logger.info(f"Connection to websocket made on {_ws}")
        self.connecting=False
        self.connected = True


        
    def send_request(self, method:str, params: dict={}):
        if not self.connected:
            return False
        self._request_id+=1
        packet = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params, 
            "id": self._request_id
        }
        self.ws.send(json.dumps(packet))
        _logger.debug(f"Sending method:{method} , id: {self._request_id}")
        return True
    
    

class MoonAPI():
    def __init__(self):
        pass
        

        
        
##############################################################################
if __name__ == "__main__":
    try:    
        _api = MoonRest()
        wb = MoonWebSocket(moonRest=_api)
        wb.start()

        wb.try_connection()
        

        while wb.is_alive:
            if wb._request_id == 0:
                # wb.send_request("access.oneshot_token")
                wb.send_request("access.get_api_key")
            if wb._request_id == 1:
                wb.send_request(method="server.info")
                
            if wb._request_id == 2:
                wb.send_request(method="access.info")
            # _this_time = time.monotonic()
            # _current = _this_time - _inital_time
            # if _current > 2:
            #     wb.disconnect()
            # for thread in threading.enumerate():
            #     print(thread.name)
            wb.join(0.5)
    except KeyboardInterrupt:
        sys.exit(1)
        
        
# ! Can also connect to the moonraker using Unix Socket connection instead of websocket.
