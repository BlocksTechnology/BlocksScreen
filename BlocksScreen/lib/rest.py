import tornado
from urllib3.util.url import Url
import pydantic
import fastapi

import asyncio
import multiprocessing

import concurrent.futures
import functools
import inspect
import time
import logging
import typing
import tornado.concurrent

from fastapi import FastAPI, WebSocket

from PyQt6 import QtCore
import tornado.websocket


class WebSocketClient(tornado.websocket.WebSocketClientConnection):
    url = "ws://192.168.1.165:7125"
    port = 7125

    def __init__(self) -> None:
        # super(WebSocketClient, self).__init__( )
        self.connect()

        tornado.ioloop.IOLoop.current().start()

    def connect(self):
        tornado.websocket.websocket_connect(
            self.url,
            callback=self.on_connect,
        )

    def on_connect(self, future):
        self.connection = future.results()

    def on_message(self, message):
        print(message)

    def on_close(self):
        print("websocket closed ")


# if __name__ == "__main__":
#     client = WebSocketClient()

# class WebSocketClientFastAPI(FastAPI): 
    
#     def __init__(self, *args, **kwargs): 
#         super(WebSocketClientFastAPI, self).__init__()
    
        
#     @FastAPI.websocket("/ws")
#     async def websocket_endspoint(websocket:WebSocket): 
#         await websocket.accept()
#         try:
#             while True:
#                 data = await websocket.receive_text()
#                 # Process data and interact with Klipper
#                 response = {"status": "success", "data": data}
#                 await websocket.send_json(response)

#         except Exception as e:
#             await websocket.close()


# if __name__ == "__main__": 
    
#     eb = WebSocketClientFastAPI()


import asyncio
import uvicorn

async def app(scope, receive, send):
    ...

async def main():
    config = uvicorn.Config("rest:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())