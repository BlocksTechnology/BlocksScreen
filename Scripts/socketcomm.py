#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals, annotations
import threading
import json
import logging
import sys
import rel 
import websocket
import json
from time import monotonic as monotonic_time
from PyQt6.QtCore import QTimer, QUrl, QThread
from threading import Timer


# My Logger object
_logger = logging.getLogger(__name__)
# Writes my logs to a file defines the format of the log and all that
logging.basicConfig(format="'%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s",
                    filename=r"E:\gitHub\Blocks_Screen\logFile.log", encoding="utf-8", level=logging.DEBUG)
class URLTYPE(object):
    _prefix_type = ["ws://", "wss://"]
    def __init__(self, host:str, port:int, wstype=0):
        # self._prefix:str = 
        self._suffix:str = "/websocket"
        self._host:str = host
        self._port:int = port
        self._wstype= wstype
        
    def __str__(self):
        return self._prefix_type[self._wstype] + self._host + ":" + str(self._port) + self._suffix
        
    def type(self) -> URLTYPE:
        raise "urltype"
    
    def __repr__(self):
        print(self._prefix_type[self._wstype] + self._host + ":" + str(self._port) + self._suffix)
    
    def setWsType(self, type: int = 0):
        if type < 0 or type > 1:
            raise AttributeError
        self._wstype = type
    
    def setWsHost(self, host: str):
        if not isinstance(host, str):
            raise AttributeError
        self._host = host
    
    def setWsPort(self, port: int):
        if not isinstance(port, int):
            raise AttributeError
        self._port = port
    
# TODO: make host, port and websocket name not static but a argument that can be feed in the class
class SocketComm(threading.Thread):    
    connected = False
    connecting = True
    callback_table={}
    _reconnect_count=0
    max_retries=3
    timeout=3
    
    def __init__(self, *args):
        # * Both lines bellow are the same shit i guess
        super(SocketComm, self).__init__()
        self.daemon = True
        self.host: str=None
        self.port: int = None
        self.ws: websocket.WebSocketApp = None
        self._callback = None
        self._wst= None
        self._request_id= 0
        
        self._retry_timer = threading.Timer(self.timeout, self.reconnect)#.start()# Can also args and kwargs
        self._retry_timer.name= "Wb-ConRetry-Timer"
        
        # self._connectionErrorEvent = threading.Event()
        # ! Websocket options
        websocket.enableTrace(True)
        websocket.setdefaulttimeout(self.timeout)
        
        # Events
        self.connectEvent = threading.Event()
        self.disconnectEvent = threading.Event()
    
    def retry(self):
        logging.info("Retrying connection.")
        self._reconnect_count = 0
        self.try_connection()
        
    # TODO: isinstance for each type
    def try_connection(self):
        self._reconnect_count += 1
        self.connecting = True
        return self.connect()
        
    def reconnect(self):
        if self.connected:
            return True
        
        if self._reconnect_count > self.max_retries:
            logging.info("Retrying connection to websocket")
            try:
                self._retry_timer.start()
            except Exception as e:
                logging.debug(e, exc_info=True)
                logging.info(f"Error while starting timeout connection to websocket: {e}")

        return self.connect()
    
    def connect(self):
        if self.connected:
            logging.debug("Connection already established.")
            return True
        # self.url = URLTYPE(host="localhost", port=7125, wstype=0)
        
        logging.debug(f"Connect try number:{self._reconnect_count}")
        self.ws = websocket.WebSocketApp(
            "ws://localhost:7125/websocket",
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
            logging.info("Starting websocket.")
            self._wst.start()
        except Exception as e:
            logging.info(e, exc_info=True)
            logging.debug(f"Error starting websocket: {e}")
            return False
        return True
    
    # TODO: messages from *args, and pass it to other variables.
    def disconnect(self):
        # TODO: Handle disconnect or close state 
        self.ws.close() 
        # logging.info("Socket disconnected:")

    def on_message(self, *args): # ws, message):
        # TODO: Handle receiving message from websocket
        # First argument is ws second is message
        _message = args[1] if len(args) == 2 else args[0]
        logging.debug(f"Message received from websocket: {_message}")
        
    
    def on_error(self, *args):# ws, error):
        # First argument is ws second is error message 
        _error = args[1] if len(args) == 2 else args[0]
        # TODO: Handle error messages
        logging.info(f"Websocket error:{_error}")
        self.connected = False
        
    def on_close(self, close_status_code = "Empty", close_msg = "Empty"): #ws, close_status_code, close_message):
        # First argument is ws, second is close status code, third is close message
        
        # print(close_status_code)

        # _close_status_code, _close_message = args[0],args[1] if len(args) == 2 else None, None
        # logging.info(f"Websocket closed, code: {_close_status_code}, message: {_close_message}")
        self.connected = False
        self.ws.keep_running = False
        # self.reconnect()
        logging.info("Websocket closed.")

    def on_open(self, *args):
        # TODO: Handle initial connection as per moonraker api documentation
        _ws = args[0] if len(args) == 1 else None
        logging.info(f"Connection to websocket made on {_ws}")
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
        logging.debug(f"Sending method:{method} , id: {self._request_id}")
        return True
    
    
    
##############################################################################
if __name__ == "__main__":
    try:    
        
        wb = SocketComm()
        wb.start()
        
        wb.try_connection()

        while wb.is_alive:
            # if wb._request_id == 0:
                # wb.send_request(method="server.info")
            # _this_time = time.monotonic()
            # _current = _this_time - _inital_time
            # if _current > 2:
            #     wb.disconnect()
            wb.join(0.5)
    except KeyboardInterrupt:
        sys.exit(1)
        
        
# ! Can also connect to the moonraker using Unix Socket connection instead of websocket.