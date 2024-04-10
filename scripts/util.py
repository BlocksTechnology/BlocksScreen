#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals, annotations
import threading
import logging
import time
import re


class URLTYPE(object):
    _prefix_type = ["ws://", "wss://", "http://", "https://"]
    link_type = ['rest', 'websocket']

    def __init__(self, host: str, port=None, type: str = 'rest'):
        # self._prefix:str =
        if isinstance(port, int) is False and port is not None:
            raise AttributeError(
                "If port is specified it can only be an integer")

        if type not in self.link_type:
            raise AttributeError(f"Url type can only be of: {self.link_type}")

        self._websocket_suffix: str = "/websocket"

        self._host: str = host
        self._port = port
        self._type = type.lower()
        self._build_url
        # self._url = self._prefix_type[self._type] + self._host + ":" + str(self._port) + self._websocket_suffix

    def _build_url(self):
        if self._type is 'rest':
            self._url = self.link_type[2] + self._host if self._host.endswith(
                '.com') else self.link_type[2] + self._host + ".com"

        if self._type is 'websocket':
            self._url = self.link_type[0] + self._host + \
                ":" + str(self._port) + self._websocket_suffix

    def type(self) -> str:
        return self.__class__.__name__

    @property
    def url_link(self):
        return self._url

    @url_link.setter
    def url_link(self, host, port, type):
        if self._type is 'rest':
            if port is None:
                self._url = self.link_type[2] + host if host.endswith(
                    '.com') else self.link_type[2] + host + ".com"
            else:
                self._url = self.link_type[2] + host + ":" + port if host.endswith(
                    '.com') else self.link_type[2] + host + ":" + port + ".com"

        if self._type is 'websocket':
            self._url = self.link_type[0] + self._host + \
                ":" + str(self._port) + self._websocket_suffix

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f'{cls}(host = {self._host}, port= {self._port}, type= {self._type})'

    def __str__(self) -> str:
        return self._url


class RepeatedTimer(threading.Thread):
    def __init__(self, timeout, function, nameThread=None, *args, **kwargs):
        super(RepeatedTimer, self).__init__(daemon=True)
        self.name = "RepeatedTimer"
        self._timeout = timeout
        self._function = function
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
                self._timer.daemon = True
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
        if callable(self._function):  # and self.stopEvent.is_set() is False:
            self._function(*self._args, **self._kwargs)

    def stopTimer(self):
        # self._timer.cancel()
        if self.running :
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
