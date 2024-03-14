#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals, annotations
import threading
import logging
import time
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
    
class RepeatedTimer(threading.Thread):
    def __init__(self, timeout, function, nameThread= None, *args, **kwargs):
        super(RepeatedTimer, self).__init__(daemon=True)
        self.name = "RepeatedTimer"
        self._timeout = timeout
        self._function= function
        self._args = args
        self._kwargs = kwargs
        self.running = False
        self.timeoutEvent = threading.Event()
        self.stopEvent = threading.Event()
        self._timer = None
        self.startTimer()
        
        
    def startTimer(self):
        if self.running is False:
            try:
                self._timer = threading.Timer(self._timeout, self._run)
                self._timer.daemon=True
                self._timer.start()
                if self.stopEvent.is_set() is False:
                    self.stopEvent.set()
            except Exception as e:
                logging.debug("RepeatedTimer error while starting the timer.")
            self.running = True
    
    def _run(self):
        self.running = False
        self.startTimer()
        self.stopEvent.wait()         
        if callable(self._function):# and self.stopEvent.is_set() is False:        
            self._function(*self._args, **self._kwargs)

    def stopTimer(self):
        self._timer.cancel()
        self.stopEvent.clear()
        self.running = False
        

    @staticmethod
    def pauseTimer(self):
        # TODO never tested 
        self.stopEvent.clear()
        self.running = False
    @staticmethod
    def resumeTimer(self):
        # TODO: never tested
        self.stopEvent.set()
        self.running = True    

            
if __name__ == "__main__":
    def hey():
        print("JELLO")
        
    t = RepeatedTimer(5, hey)
    