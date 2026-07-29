"""Collection of all custom events used by the application"""

import typing
from PyQt6.QtCore import QEvent
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


class WebSocketConnecting(QEvent):
    """Connecting event for websocket

    Args:
        data (any): Data or message to pass onto the event
    """

    WebsocketConnectingEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁWebSocketConnectingǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁWebSocketConnectingǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁWebSocketConnectingǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(WebSocketConnecting, self).__init__(
            WebSocketConnecting.WebsocketConnectingEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketConnectingǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(WebSocketConnecting, self).__init__(
            None
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketConnectingǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(
            WebSocketConnecting.WebsocketConnectingEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketConnectingǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(WebSocketConnecting, None).__init__(
            WebSocketConnecting.WebsocketConnectingEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketConnectingǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(
            WebSocketConnecting.WebsocketConnectingEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketConnectingǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(WebSocketConnecting, ).__init__(
            WebSocketConnecting.WebsocketConnectingEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketConnectingǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(WebSocketConnecting, self).__init__(
            WebSocketConnecting.WebsocketConnectingEvent
        )
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketConnectingǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(WebSocketConnecting, self).__init__(
            WebSocketConnecting.WebsocketConnectingEvent
        )
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁWebSocketConnectingǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(WebSocketConnecting, self).__init__(
            WebSocketConnecting.WebsocketConnectingEvent
        )
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁWebSocketConnectingǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁWebSocketConnectingǁ__init____mutmut_1': xǁWebSocketConnectingǁ__init____mutmut_1, 
        'xǁWebSocketConnectingǁ__init____mutmut_2': xǁWebSocketConnectingǁ__init____mutmut_2, 
        'xǁWebSocketConnectingǁ__init____mutmut_3': xǁWebSocketConnectingǁ__init____mutmut_3, 
        'xǁWebSocketConnectingǁ__init____mutmut_4': xǁWebSocketConnectingǁ__init____mutmut_4, 
        'xǁWebSocketConnectingǁ__init____mutmut_5': xǁWebSocketConnectingǁ__init____mutmut_5, 
        'xǁWebSocketConnectingǁ__init____mutmut_6': xǁWebSocketConnectingǁ__init____mutmut_6, 
        'xǁWebSocketConnectingǁ__init____mutmut_7': xǁWebSocketConnectingǁ__init____mutmut_7, 
        'xǁWebSocketConnectingǁ__init____mutmut_8': xǁWebSocketConnectingǁ__init____mutmut_8
    }
    xǁWebSocketConnectingǁ__init____mutmut_orig.__name__ = 'xǁWebSocketConnectingǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(WebSocketConnecting.WebsocketConnectingEvent)


class WebSocketMessageReceived(QEvent):
    """Message received event from websocket

    Args:
        data (any): Data or message to pass onto the event
    """

    WebsocketMessageReceivedEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(
        self,
        method: typing.Optional[str] = None,
        data: typing.Optional[dict] = None,
        metadata: typing.Optional[dict] = None,
    ):
        args = [method, data, metadata]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁWebSocketMessageReceivedǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁWebSocketMessageReceivedǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁWebSocketMessageReceivedǁ__init____mutmut_orig(
        self,
        method: typing.Optional[str] = None,
        data: typing.Optional[dict] = None,
        metadata: typing.Optional[dict] = None,
    ):
        super(WebSocketMessageReceived, self).__init__(
            WebSocketMessageReceived.WebsocketMessageReceivedEvent
        )
        self.method = method
        self.data = data
        self.metadata = metadata

    def xǁWebSocketMessageReceivedǁ__init____mutmut_1(
        self,
        method: typing.Optional[str] = None,
        data: typing.Optional[dict] = None,
        metadata: typing.Optional[dict] = None,
    ):
        super(WebSocketMessageReceived, self).__init__(
            None
        )
        self.method = method
        self.data = data
        self.metadata = metadata

    def xǁWebSocketMessageReceivedǁ__init____mutmut_2(
        self,
        method: typing.Optional[str] = None,
        data: typing.Optional[dict] = None,
        metadata: typing.Optional[dict] = None,
    ):
        super(None, self).__init__(
            WebSocketMessageReceived.WebsocketMessageReceivedEvent
        )
        self.method = method
        self.data = data
        self.metadata = metadata

    def xǁWebSocketMessageReceivedǁ__init____mutmut_3(
        self,
        method: typing.Optional[str] = None,
        data: typing.Optional[dict] = None,
        metadata: typing.Optional[dict] = None,
    ):
        super(WebSocketMessageReceived, None).__init__(
            WebSocketMessageReceived.WebsocketMessageReceivedEvent
        )
        self.method = method
        self.data = data
        self.metadata = metadata

    def xǁWebSocketMessageReceivedǁ__init____mutmut_4(
        self,
        method: typing.Optional[str] = None,
        data: typing.Optional[dict] = None,
        metadata: typing.Optional[dict] = None,
    ):
        super(self).__init__(
            WebSocketMessageReceived.WebsocketMessageReceivedEvent
        )
        self.method = method
        self.data = data
        self.metadata = metadata

    def xǁWebSocketMessageReceivedǁ__init____mutmut_5(
        self,
        method: typing.Optional[str] = None,
        data: typing.Optional[dict] = None,
        metadata: typing.Optional[dict] = None,
    ):
        super(WebSocketMessageReceived, ).__init__(
            WebSocketMessageReceived.WebsocketMessageReceivedEvent
        )
        self.method = method
        self.data = data
        self.metadata = metadata

    def xǁWebSocketMessageReceivedǁ__init____mutmut_6(
        self,
        method: typing.Optional[str] = None,
        data: typing.Optional[dict] = None,
        metadata: typing.Optional[dict] = None,
    ):
        super(WebSocketMessageReceived, self).__init__(
            WebSocketMessageReceived.WebsocketMessageReceivedEvent
        )
        self.method = None
        self.data = data
        self.metadata = metadata

    def xǁWebSocketMessageReceivedǁ__init____mutmut_7(
        self,
        method: typing.Optional[str] = None,
        data: typing.Optional[dict] = None,
        metadata: typing.Optional[dict] = None,
    ):
        super(WebSocketMessageReceived, self).__init__(
            WebSocketMessageReceived.WebsocketMessageReceivedEvent
        )
        self.method = method
        self.data = None
        self.metadata = metadata

    def xǁWebSocketMessageReceivedǁ__init____mutmut_8(
        self,
        method: typing.Optional[str] = None,
        data: typing.Optional[dict] = None,
        metadata: typing.Optional[dict] = None,
    ):
        super(WebSocketMessageReceived, self).__init__(
            WebSocketMessageReceived.WebsocketMessageReceivedEvent
        )
        self.method = method
        self.data = data
        self.metadata = None
    
    xǁWebSocketMessageReceivedǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁWebSocketMessageReceivedǁ__init____mutmut_1': xǁWebSocketMessageReceivedǁ__init____mutmut_1, 
        'xǁWebSocketMessageReceivedǁ__init____mutmut_2': xǁWebSocketMessageReceivedǁ__init____mutmut_2, 
        'xǁWebSocketMessageReceivedǁ__init____mutmut_3': xǁWebSocketMessageReceivedǁ__init____mutmut_3, 
        'xǁWebSocketMessageReceivedǁ__init____mutmut_4': xǁWebSocketMessageReceivedǁ__init____mutmut_4, 
        'xǁWebSocketMessageReceivedǁ__init____mutmut_5': xǁWebSocketMessageReceivedǁ__init____mutmut_5, 
        'xǁWebSocketMessageReceivedǁ__init____mutmut_6': xǁWebSocketMessageReceivedǁ__init____mutmut_6, 
        'xǁWebSocketMessageReceivedǁ__init____mutmut_7': xǁWebSocketMessageReceivedǁ__init____mutmut_7, 
        'xǁWebSocketMessageReceivedǁ__init____mutmut_8': xǁWebSocketMessageReceivedǁ__init____mutmut_8
    }
    xǁWebSocketMessageReceivedǁ__init____mutmut_orig.__name__ = 'xǁWebSocketMessageReceivedǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(WebSocketMessageReceived.WebsocketMessageReceivedEvent)


class WebSocketOpen(QEvent):
    """Open event for websocket

    Args:
        data (any): Data or message to pass onto the event
    """

    WebsocketOpenEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁWebSocketOpenǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁWebSocketOpenǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁWebSocketOpenǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(WebSocketOpen, self).__init__(WebSocketOpen.WebsocketOpenEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketOpenǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(WebSocketOpen, self).__init__(None)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketOpenǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(WebSocketOpen.WebsocketOpenEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketOpenǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(WebSocketOpen, None).__init__(WebSocketOpen.WebsocketOpenEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketOpenǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(WebSocketOpen.WebsocketOpenEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketOpenǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(WebSocketOpen, ).__init__(WebSocketOpen.WebsocketOpenEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketOpenǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(WebSocketOpen, self).__init__(WebSocketOpen.WebsocketOpenEvent)
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketOpenǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(WebSocketOpen, self).__init__(WebSocketOpen.WebsocketOpenEvent)
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁWebSocketOpenǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(WebSocketOpen, self).__init__(WebSocketOpen.WebsocketOpenEvent)
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁWebSocketOpenǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁWebSocketOpenǁ__init____mutmut_1': xǁWebSocketOpenǁ__init____mutmut_1, 
        'xǁWebSocketOpenǁ__init____mutmut_2': xǁWebSocketOpenǁ__init____mutmut_2, 
        'xǁWebSocketOpenǁ__init____mutmut_3': xǁWebSocketOpenǁ__init____mutmut_3, 
        'xǁWebSocketOpenǁ__init____mutmut_4': xǁWebSocketOpenǁ__init____mutmut_4, 
        'xǁWebSocketOpenǁ__init____mutmut_5': xǁWebSocketOpenǁ__init____mutmut_5, 
        'xǁWebSocketOpenǁ__init____mutmut_6': xǁWebSocketOpenǁ__init____mutmut_6, 
        'xǁWebSocketOpenǁ__init____mutmut_7': xǁWebSocketOpenǁ__init____mutmut_7, 
        'xǁWebSocketOpenǁ__init____mutmut_8': xǁWebSocketOpenǁ__init____mutmut_8
    }
    xǁWebSocketOpenǁ__init____mutmut_orig.__name__ = 'xǁWebSocketOpenǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(WebSocketOpen.WebsocketOpenEvent)


class WebSocketError(QEvent):
    """Error event for websocket

    Args:
        data (any): Data or message to pass onto the event
    """

    WebsocketErrorEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁWebSocketErrorǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁWebSocketErrorǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁWebSocketErrorǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(WebSocketError, self).__init__(WebSocketError.WebsocketErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketErrorǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(WebSocketError, self).__init__(None)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketErrorǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(WebSocketError.WebsocketErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketErrorǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(WebSocketError, None).__init__(WebSocketError.WebsocketErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketErrorǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(WebSocketError.WebsocketErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketErrorǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(WebSocketError, ).__init__(WebSocketError.WebsocketErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketErrorǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(WebSocketError, self).__init__(WebSocketError.WebsocketErrorEvent)
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketErrorǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(WebSocketError, self).__init__(WebSocketError.WebsocketErrorEvent)
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁWebSocketErrorǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(WebSocketError, self).__init__(WebSocketError.WebsocketErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁWebSocketErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁWebSocketErrorǁ__init____mutmut_1': xǁWebSocketErrorǁ__init____mutmut_1, 
        'xǁWebSocketErrorǁ__init____mutmut_2': xǁWebSocketErrorǁ__init____mutmut_2, 
        'xǁWebSocketErrorǁ__init____mutmut_3': xǁWebSocketErrorǁ__init____mutmut_3, 
        'xǁWebSocketErrorǁ__init____mutmut_4': xǁWebSocketErrorǁ__init____mutmut_4, 
        'xǁWebSocketErrorǁ__init____mutmut_5': xǁWebSocketErrorǁ__init____mutmut_5, 
        'xǁWebSocketErrorǁ__init____mutmut_6': xǁWebSocketErrorǁ__init____mutmut_6, 
        'xǁWebSocketErrorǁ__init____mutmut_7': xǁWebSocketErrorǁ__init____mutmut_7, 
        'xǁWebSocketErrorǁ__init____mutmut_8': xǁWebSocketErrorǁ__init____mutmut_8
    }
    xǁWebSocketErrorǁ__init____mutmut_orig.__name__ = 'xǁWebSocketErrorǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(WebSocketError.WebsocketErrorEvent)


class WebSocketDisconnected(QEvent):
    """Disconnected event for websocket

    Args:
        data (Any): Data or message to pass onto the event
    """

    WebsocketDisconnectedEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁWebSocketDisconnectedǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁWebSocketDisconnectedǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁWebSocketDisconnectedǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(WebSocketDisconnected, self).__init__(
            WebSocketDisconnected.WebsocketDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketDisconnectedǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(WebSocketDisconnected, self).__init__(
            None
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketDisconnectedǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(
            WebSocketDisconnected.WebsocketDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketDisconnectedǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(WebSocketDisconnected, None).__init__(
            WebSocketDisconnected.WebsocketDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketDisconnectedǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(
            WebSocketDisconnected.WebsocketDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketDisconnectedǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(WebSocketDisconnected, ).__init__(
            WebSocketDisconnected.WebsocketDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketDisconnectedǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(WebSocketDisconnected, self).__init__(
            WebSocketDisconnected.WebsocketDisconnectedEvent
        )
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketDisconnectedǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(WebSocketDisconnected, self).__init__(
            WebSocketDisconnected.WebsocketDisconnectedEvent
        )
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁWebSocketDisconnectedǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(WebSocketDisconnected, self).__init__(
            WebSocketDisconnected.WebsocketDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁWebSocketDisconnectedǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁWebSocketDisconnectedǁ__init____mutmut_1': xǁWebSocketDisconnectedǁ__init____mutmut_1, 
        'xǁWebSocketDisconnectedǁ__init____mutmut_2': xǁWebSocketDisconnectedǁ__init____mutmut_2, 
        'xǁWebSocketDisconnectedǁ__init____mutmut_3': xǁWebSocketDisconnectedǁ__init____mutmut_3, 
        'xǁWebSocketDisconnectedǁ__init____mutmut_4': xǁWebSocketDisconnectedǁ__init____mutmut_4, 
        'xǁWebSocketDisconnectedǁ__init____mutmut_5': xǁWebSocketDisconnectedǁ__init____mutmut_5, 
        'xǁWebSocketDisconnectedǁ__init____mutmut_6': xǁWebSocketDisconnectedǁ__init____mutmut_6, 
        'xǁWebSocketDisconnectedǁ__init____mutmut_7': xǁWebSocketDisconnectedǁ__init____mutmut_7, 
        'xǁWebSocketDisconnectedǁ__init____mutmut_8': xǁWebSocketDisconnectedǁ__init____mutmut_8
    }
    xǁWebSocketDisconnectedǁ__init____mutmut_orig.__name__ = 'xǁWebSocketDisconnectedǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(WebSocketDisconnected.WebsocketDisconnectedEvent)


class WebSocketClose(QEvent):
    """Close event for websocket

    Args:
        data (any): Data or message to pass onto the event

    """

    WebsocketCloseEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁWebSocketCloseǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁWebSocketCloseǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁWebSocketCloseǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(WebSocketClose, self).__init__(WebSocketClose.WebsocketCloseEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketCloseǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(WebSocketClose, self).__init__(None)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketCloseǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(WebSocketClose.WebsocketCloseEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketCloseǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(WebSocketClose, None).__init__(WebSocketClose.WebsocketCloseEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketCloseǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(WebSocketClose.WebsocketCloseEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketCloseǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(WebSocketClose, ).__init__(WebSocketClose.WebsocketCloseEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketCloseǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(WebSocketClose, self).__init__(WebSocketClose.WebsocketCloseEvent)
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁWebSocketCloseǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(WebSocketClose, self).__init__(WebSocketClose.WebsocketCloseEvent)
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁWebSocketCloseǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(WebSocketClose, self).__init__(WebSocketClose.WebsocketCloseEvent)
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁWebSocketCloseǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁWebSocketCloseǁ__init____mutmut_1': xǁWebSocketCloseǁ__init____mutmut_1, 
        'xǁWebSocketCloseǁ__init____mutmut_2': xǁWebSocketCloseǁ__init____mutmut_2, 
        'xǁWebSocketCloseǁ__init____mutmut_3': xǁWebSocketCloseǁ__init____mutmut_3, 
        'xǁWebSocketCloseǁ__init____mutmut_4': xǁWebSocketCloseǁ__init____mutmut_4, 
        'xǁWebSocketCloseǁ__init____mutmut_5': xǁWebSocketCloseǁ__init____mutmut_5, 
        'xǁWebSocketCloseǁ__init____mutmut_6': xǁWebSocketCloseǁ__init____mutmut_6, 
        'xǁWebSocketCloseǁ__init____mutmut_7': xǁWebSocketCloseǁ__init____mutmut_7, 
        'xǁWebSocketCloseǁ__init____mutmut_8': xǁWebSocketCloseǁ__init____mutmut_8
    }
    xǁWebSocketCloseǁ__init____mutmut_orig.__name__ = 'xǁWebSocketCloseǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(WebSocketClose.WebsocketCloseEvent)


class KlippyShutdown(QEvent):
    """Event for Klipper Shutdown

    Args:
        data (any): Data or message to pass onto the event
    """

    KlippyShutdownEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁKlippyShutdownǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁKlippyShutdownǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁKlippyShutdownǁ__init____mutmut_orig(self, data, *args, **kwargs):
        QEvent.__instancecheck__(self)
        super(KlippyShutdown, self).__init__(KlippyShutdown.KlippyShutdownEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyShutdownǁ__init____mutmut_1(self, data, *args, **kwargs):
        QEvent.__instancecheck__(None)
        super(KlippyShutdown, self).__init__(KlippyShutdown.KlippyShutdownEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyShutdownǁ__init____mutmut_2(self, data, *args, **kwargs):
        QEvent.__instancecheck__(self)
        super(KlippyShutdown, self).__init__(None)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyShutdownǁ__init____mutmut_3(self, data, *args, **kwargs):
        QEvent.__instancecheck__(self)
        super(None, self).__init__(KlippyShutdown.KlippyShutdownEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyShutdownǁ__init____mutmut_4(self, data, *args, **kwargs):
        QEvent.__instancecheck__(self)
        super(KlippyShutdown, None).__init__(KlippyShutdown.KlippyShutdownEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyShutdownǁ__init____mutmut_5(self, data, *args, **kwargs):
        QEvent.__instancecheck__(self)
        super(self).__init__(KlippyShutdown.KlippyShutdownEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyShutdownǁ__init____mutmut_6(self, data, *args, **kwargs):
        QEvent.__instancecheck__(self)
        super(KlippyShutdown, ).__init__(KlippyShutdown.KlippyShutdownEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyShutdownǁ__init____mutmut_7(self, data, *args, **kwargs):
        QEvent.__instancecheck__(self)
        super(KlippyShutdown, self).__init__(KlippyShutdown.KlippyShutdownEvent)
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyShutdownǁ__init____mutmut_8(self, data, *args, **kwargs):
        QEvent.__instancecheck__(self)
        super(KlippyShutdown, self).__init__(KlippyShutdown.KlippyShutdownEvent)
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁKlippyShutdownǁ__init____mutmut_9(self, data, *args, **kwargs):
        QEvent.__instancecheck__(self)
        super(KlippyShutdown, self).__init__(KlippyShutdown.KlippyShutdownEvent)
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁKlippyShutdownǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁKlippyShutdownǁ__init____mutmut_1': xǁKlippyShutdownǁ__init____mutmut_1, 
        'xǁKlippyShutdownǁ__init____mutmut_2': xǁKlippyShutdownǁ__init____mutmut_2, 
        'xǁKlippyShutdownǁ__init____mutmut_3': xǁKlippyShutdownǁ__init____mutmut_3, 
        'xǁKlippyShutdownǁ__init____mutmut_4': xǁKlippyShutdownǁ__init____mutmut_4, 
        'xǁKlippyShutdownǁ__init____mutmut_5': xǁKlippyShutdownǁ__init____mutmut_5, 
        'xǁKlippyShutdownǁ__init____mutmut_6': xǁKlippyShutdownǁ__init____mutmut_6, 
        'xǁKlippyShutdownǁ__init____mutmut_7': xǁKlippyShutdownǁ__init____mutmut_7, 
        'xǁKlippyShutdownǁ__init____mutmut_8': xǁKlippyShutdownǁ__init____mutmut_8, 
        'xǁKlippyShutdownǁ__init____mutmut_9': xǁKlippyShutdownǁ__init____mutmut_9
    }
    xǁKlippyShutdownǁ__init____mutmut_orig.__name__ = 'xǁKlippyShutdownǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return KlippyShutdown.KlippyShutdownEvent

    # def __instancecheck__(self, instance: Any) -> bool:
    #     return True if self.KlippyShutdownEvent in QEvent.Type else False
    # return True

    # return super().__instancecheck__(instance)


class KlippyReady(QEvent):
    """Klipper ready event

    Args:
        data (any): Data or message to pass onto the event
    """

    KlippyReadyEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁKlippyReadyǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁKlippyReadyǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁKlippyReadyǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(KlippyReady, self).__init__(KlippyReady.KlippyReadyEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyReadyǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(KlippyReady, self).__init__(None)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyReadyǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(KlippyReady.KlippyReadyEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyReadyǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(KlippyReady, None).__init__(KlippyReady.KlippyReadyEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyReadyǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(KlippyReady.KlippyReadyEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyReadyǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(KlippyReady, ).__init__(KlippyReady.KlippyReadyEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyReadyǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(KlippyReady, self).__init__(KlippyReady.KlippyReadyEvent)
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyReadyǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(KlippyReady, self).__init__(KlippyReady.KlippyReadyEvent)
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁKlippyReadyǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(KlippyReady, self).__init__(KlippyReady.KlippyReadyEvent)
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁKlippyReadyǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁKlippyReadyǁ__init____mutmut_1': xǁKlippyReadyǁ__init____mutmut_1, 
        'xǁKlippyReadyǁ__init____mutmut_2': xǁKlippyReadyǁ__init____mutmut_2, 
        'xǁKlippyReadyǁ__init____mutmut_3': xǁKlippyReadyǁ__init____mutmut_3, 
        'xǁKlippyReadyǁ__init____mutmut_4': xǁKlippyReadyǁ__init____mutmut_4, 
        'xǁKlippyReadyǁ__init____mutmut_5': xǁKlippyReadyǁ__init____mutmut_5, 
        'xǁKlippyReadyǁ__init____mutmut_6': xǁKlippyReadyǁ__init____mutmut_6, 
        'xǁKlippyReadyǁ__init____mutmut_7': xǁKlippyReadyǁ__init____mutmut_7, 
        'xǁKlippyReadyǁ__init____mutmut_8': xǁKlippyReadyǁ__init____mutmut_8
    }
    xǁKlippyReadyǁ__init____mutmut_orig.__name__ = 'xǁKlippyReadyǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(KlippyReady.KlippyReadyEvent)


class KlippyDisconnected(QEvent):
    """Klipper disconnected event

    Args:
        data (any): Data or message to pass onto the event
    """

    KlippyDisconnectedEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁKlippyDisconnectedǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁKlippyDisconnectedǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁKlippyDisconnectedǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(KlippyDisconnected, self).__init__(
            KlippyDisconnected.KlippyDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyDisconnectedǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(KlippyDisconnected, self).__init__(
            None
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyDisconnectedǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(
            KlippyDisconnected.KlippyDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyDisconnectedǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(KlippyDisconnected, None).__init__(
            KlippyDisconnected.KlippyDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyDisconnectedǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(
            KlippyDisconnected.KlippyDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyDisconnectedǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(KlippyDisconnected, ).__init__(
            KlippyDisconnected.KlippyDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyDisconnectedǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(KlippyDisconnected, self).__init__(
            KlippyDisconnected.KlippyDisconnectedEvent
        )
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁKlippyDisconnectedǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(KlippyDisconnected, self).__init__(
            KlippyDisconnected.KlippyDisconnectedEvent
        )
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁKlippyDisconnectedǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(KlippyDisconnected, self).__init__(
            KlippyDisconnected.KlippyDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁKlippyDisconnectedǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁKlippyDisconnectedǁ__init____mutmut_1': xǁKlippyDisconnectedǁ__init____mutmut_1, 
        'xǁKlippyDisconnectedǁ__init____mutmut_2': xǁKlippyDisconnectedǁ__init____mutmut_2, 
        'xǁKlippyDisconnectedǁ__init____mutmut_3': xǁKlippyDisconnectedǁ__init____mutmut_3, 
        'xǁKlippyDisconnectedǁ__init____mutmut_4': xǁKlippyDisconnectedǁ__init____mutmut_4, 
        'xǁKlippyDisconnectedǁ__init____mutmut_5': xǁKlippyDisconnectedǁ__init____mutmut_5, 
        'xǁKlippyDisconnectedǁ__init____mutmut_6': xǁKlippyDisconnectedǁ__init____mutmut_6, 
        'xǁKlippyDisconnectedǁ__init____mutmut_7': xǁKlippyDisconnectedǁ__init____mutmut_7, 
        'xǁKlippyDisconnectedǁ__init____mutmut_8': xǁKlippyDisconnectedǁ__init____mutmut_8
    }
    xǁKlippyDisconnectedǁ__init____mutmut_orig.__name__ = 'xǁKlippyDisconnectedǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(KlippyDisconnected.KlippyDisconnectedEvent)


class KlippyError(QEvent):
    """Klipper error event

    Args:
        data (any): Data or message to pass onto the event
    """

    KlippyErrorEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, message, *args, **kwargs):
        args = [data, message, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁKlippyErrorǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁKlippyErrorǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁKlippyErrorǁ__init____mutmut_orig(self, data, message, *args, **kwargs):
        super(KlippyError, self).__init__(KlippyError.KlippyErrorEvent)
        self.data = data
        self.message = message

    def xǁKlippyErrorǁ__init____mutmut_1(self, data, message, *args, **kwargs):
        super(KlippyError, self).__init__(None)
        self.data = data
        self.message = message

    def xǁKlippyErrorǁ__init____mutmut_2(self, data, message, *args, **kwargs):
        super(None, self).__init__(KlippyError.KlippyErrorEvent)
        self.data = data
        self.message = message

    def xǁKlippyErrorǁ__init____mutmut_3(self, data, message, *args, **kwargs):
        super(KlippyError, None).__init__(KlippyError.KlippyErrorEvent)
        self.data = data
        self.message = message

    def xǁKlippyErrorǁ__init____mutmut_4(self, data, message, *args, **kwargs):
        super(self).__init__(KlippyError.KlippyErrorEvent)
        self.data = data
        self.message = message

    def xǁKlippyErrorǁ__init____mutmut_5(self, data, message, *args, **kwargs):
        super(KlippyError, ).__init__(KlippyError.KlippyErrorEvent)
        self.data = data
        self.message = message

    def xǁKlippyErrorǁ__init____mutmut_6(self, data, message, *args, **kwargs):
        super(KlippyError, self).__init__(KlippyError.KlippyErrorEvent)
        self.data = None
        self.message = message

    def xǁKlippyErrorǁ__init____mutmut_7(self, data, message, *args, **kwargs):
        super(KlippyError, self).__init__(KlippyError.KlippyErrorEvent)
        self.data = data
        self.message = None
    
    xǁKlippyErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁKlippyErrorǁ__init____mutmut_1': xǁKlippyErrorǁ__init____mutmut_1, 
        'xǁKlippyErrorǁ__init____mutmut_2': xǁKlippyErrorǁ__init____mutmut_2, 
        'xǁKlippyErrorǁ__init____mutmut_3': xǁKlippyErrorǁ__init____mutmut_3, 
        'xǁKlippyErrorǁ__init____mutmut_4': xǁKlippyErrorǁ__init____mutmut_4, 
        'xǁKlippyErrorǁ__init____mutmut_5': xǁKlippyErrorǁ__init____mutmut_5, 
        'xǁKlippyErrorǁ__init____mutmut_6': xǁKlippyErrorǁ__init____mutmut_6, 
        'xǁKlippyErrorǁ__init____mutmut_7': xǁKlippyErrorǁ__init____mutmut_7
    }
    xǁKlippyErrorǁ__init____mutmut_orig.__name__ = 'xǁKlippyErrorǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(KlippyError.KlippyErrorEvent)


class ReceivedFileData(QEvent):
    """File related messages received event

    Args:
        data (any): Data or message to pass onto the event
        method (str): The name of the api callback that produced this message
        params (any): Parameters of the received message
    """

    ReceivedFileDataEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(
        self, data, method, params, /, *args, **kwargs
    ):
        args = [data, method, params, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁReceivedFileDataǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁReceivedFileDataǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁReceivedFileDataǁ__init____mutmut_orig(
        self, data, method, params, /, *args, **kwargs
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(ReceivedFileData, self).__init__(ReceivedFileData.ReceivedFileDataEvent)
        self.data = data
        self.method = method
        self.params = params
        self.args = args
        self.kwargs = kwargs

    def xǁReceivedFileDataǁ__init____mutmut_1(
        self, data, method, params, /, *args, **kwargs
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(ReceivedFileData, self).__init__(None)
        self.data = data
        self.method = method
        self.params = params
        self.args = args
        self.kwargs = kwargs

    def xǁReceivedFileDataǁ__init____mutmut_2(
        self, data, method, params, /, *args, **kwargs
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(None, self).__init__(ReceivedFileData.ReceivedFileDataEvent)
        self.data = data
        self.method = method
        self.params = params
        self.args = args
        self.kwargs = kwargs

    def xǁReceivedFileDataǁ__init____mutmut_3(
        self, data, method, params, /, *args, **kwargs
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(ReceivedFileData, None).__init__(ReceivedFileData.ReceivedFileDataEvent)
        self.data = data
        self.method = method
        self.params = params
        self.args = args
        self.kwargs = kwargs

    def xǁReceivedFileDataǁ__init____mutmut_4(
        self, data, method, params, /, *args, **kwargs
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(self).__init__(ReceivedFileData.ReceivedFileDataEvent)
        self.data = data
        self.method = method
        self.params = params
        self.args = args
        self.kwargs = kwargs

    def xǁReceivedFileDataǁ__init____mutmut_5(
        self, data, method, params, /, *args, **kwargs
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(ReceivedFileData, ).__init__(ReceivedFileData.ReceivedFileDataEvent)
        self.data = data
        self.method = method
        self.params = params
        self.args = args
        self.kwargs = kwargs

    def xǁReceivedFileDataǁ__init____mutmut_6(
        self, data, method, params, /, *args, **kwargs
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(ReceivedFileData, self).__init__(ReceivedFileData.ReceivedFileDataEvent)
        self.data = None
        self.method = method
        self.params = params
        self.args = args
        self.kwargs = kwargs

    def xǁReceivedFileDataǁ__init____mutmut_7(
        self, data, method, params, /, *args, **kwargs
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(ReceivedFileData, self).__init__(ReceivedFileData.ReceivedFileDataEvent)
        self.data = data
        self.method = None
        self.params = params
        self.args = args
        self.kwargs = kwargs

    def xǁReceivedFileDataǁ__init____mutmut_8(
        self, data, method, params, /, *args, **kwargs
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(ReceivedFileData, self).__init__(ReceivedFileData.ReceivedFileDataEvent)
        self.data = data
        self.method = method
        self.params = None
        self.args = args
        self.kwargs = kwargs

    def xǁReceivedFileDataǁ__init____mutmut_9(
        self, data, method, params, /, *args, **kwargs
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(ReceivedFileData, self).__init__(ReceivedFileData.ReceivedFileDataEvent)
        self.data = data
        self.method = method
        self.params = params
        self.args = None
        self.kwargs = kwargs

    def xǁReceivedFileDataǁ__init____mutmut_10(
        self, data, method, params, /, *args, **kwargs
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(ReceivedFileData, self).__init__(ReceivedFileData.ReceivedFileDataEvent)
        self.data = data
        self.method = method
        self.params = params
        self.args = args
        self.kwargs = None
    
    xǁReceivedFileDataǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁReceivedFileDataǁ__init____mutmut_1': xǁReceivedFileDataǁ__init____mutmut_1, 
        'xǁReceivedFileDataǁ__init____mutmut_2': xǁReceivedFileDataǁ__init____mutmut_2, 
        'xǁReceivedFileDataǁ__init____mutmut_3': xǁReceivedFileDataǁ__init____mutmut_3, 
        'xǁReceivedFileDataǁ__init____mutmut_4': xǁReceivedFileDataǁ__init____mutmut_4, 
        'xǁReceivedFileDataǁ__init____mutmut_5': xǁReceivedFileDataǁ__init____mutmut_5, 
        'xǁReceivedFileDataǁ__init____mutmut_6': xǁReceivedFileDataǁ__init____mutmut_6, 
        'xǁReceivedFileDataǁ__init____mutmut_7': xǁReceivedFileDataǁ__init____mutmut_7, 
        'xǁReceivedFileDataǁ__init____mutmut_8': xǁReceivedFileDataǁ__init____mutmut_8, 
        'xǁReceivedFileDataǁ__init____mutmut_9': xǁReceivedFileDataǁ__init____mutmut_9, 
        'xǁReceivedFileDataǁ__init____mutmut_10': xǁReceivedFileDataǁ__init____mutmut_10
    }
    xǁReceivedFileDataǁ__init____mutmut_orig.__name__ = 'xǁReceivedFileDataǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(ReceivedFileData.ReceivedFileDataEvent)


class PrintStart(QEvent):
    """Print Job Start event

    Args:
        filename(any): Name of the file currently printing
        **kwargs(dict): File's metadata
    """

    PrintStartEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, filename, *args, **kwargs):
        args = [filename, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPrintStartǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁPrintStartǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁPrintStartǁ__init____mutmut_orig(self, filename, *args, **kwargs):
        super(PrintStart, self).__init__(PrintStart.PrintStartEvent)
        self.file = filename
        self.file_metadata = kwargs
        self.kwargs = kwargs

    def xǁPrintStartǁ__init____mutmut_1(self, filename, *args, **kwargs):
        super(PrintStart, self).__init__(None)
        self.file = filename
        self.file_metadata = kwargs
        self.kwargs = kwargs

    def xǁPrintStartǁ__init____mutmut_2(self, filename, *args, **kwargs):
        super(None, self).__init__(PrintStart.PrintStartEvent)
        self.file = filename
        self.file_metadata = kwargs
        self.kwargs = kwargs

    def xǁPrintStartǁ__init____mutmut_3(self, filename, *args, **kwargs):
        super(PrintStart, None).__init__(PrintStart.PrintStartEvent)
        self.file = filename
        self.file_metadata = kwargs
        self.kwargs = kwargs

    def xǁPrintStartǁ__init____mutmut_4(self, filename, *args, **kwargs):
        super(self).__init__(PrintStart.PrintStartEvent)
        self.file = filename
        self.file_metadata = kwargs
        self.kwargs = kwargs

    def xǁPrintStartǁ__init____mutmut_5(self, filename, *args, **kwargs):
        super(PrintStart, ).__init__(PrintStart.PrintStartEvent)
        self.file = filename
        self.file_metadata = kwargs
        self.kwargs = kwargs

    def xǁPrintStartǁ__init____mutmut_6(self, filename, *args, **kwargs):
        super(PrintStart, self).__init__(PrintStart.PrintStartEvent)
        self.file = None
        self.file_metadata = kwargs
        self.kwargs = kwargs

    def xǁPrintStartǁ__init____mutmut_7(self, filename, *args, **kwargs):
        super(PrintStart, self).__init__(PrintStart.PrintStartEvent)
        self.file = filename
        self.file_metadata = None
        self.kwargs = kwargs

    def xǁPrintStartǁ__init____mutmut_8(self, filename, *args, **kwargs):
        super(PrintStart, self).__init__(PrintStart.PrintStartEvent)
        self.file = filename
        self.file_metadata = kwargs
        self.kwargs = None
    
    xǁPrintStartǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPrintStartǁ__init____mutmut_1': xǁPrintStartǁ__init____mutmut_1, 
        'xǁPrintStartǁ__init____mutmut_2': xǁPrintStartǁ__init____mutmut_2, 
        'xǁPrintStartǁ__init____mutmut_3': xǁPrintStartǁ__init____mutmut_3, 
        'xǁPrintStartǁ__init____mutmut_4': xǁPrintStartǁ__init____mutmut_4, 
        'xǁPrintStartǁ__init____mutmut_5': xǁPrintStartǁ__init____mutmut_5, 
        'xǁPrintStartǁ__init____mutmut_6': xǁPrintStartǁ__init____mutmut_6, 
        'xǁPrintStartǁ__init____mutmut_7': xǁPrintStartǁ__init____mutmut_7, 
        'xǁPrintStartǁ__init____mutmut_8': xǁPrintStartǁ__init____mutmut_8
    }
    xǁPrintStartǁ__init____mutmut_orig.__name__ = 'xǁPrintStartǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(PrintStart.PrintStartEvent)


class PrintComplete(QEvent):
    """Print complete event

    Args:
        data (any): Data or message to pass onto the event
    """

    PrintCompleteEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPrintCompleteǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁPrintCompleteǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁPrintCompleteǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(PrintComplete, self).__init__(PrintComplete.PrintCompleteEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCompleteǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(PrintComplete, self).__init__(None)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCompleteǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(PrintComplete.PrintCompleteEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCompleteǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(PrintComplete, None).__init__(PrintComplete.PrintCompleteEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCompleteǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(PrintComplete.PrintCompleteEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCompleteǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(PrintComplete, ).__init__(PrintComplete.PrintCompleteEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCompleteǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(PrintComplete, self).__init__(PrintComplete.PrintCompleteEvent)
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCompleteǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(PrintComplete, self).__init__(PrintComplete.PrintCompleteEvent)
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁPrintCompleteǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(PrintComplete, self).__init__(PrintComplete.PrintCompleteEvent)
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁPrintCompleteǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPrintCompleteǁ__init____mutmut_1': xǁPrintCompleteǁ__init____mutmut_1, 
        'xǁPrintCompleteǁ__init____mutmut_2': xǁPrintCompleteǁ__init____mutmut_2, 
        'xǁPrintCompleteǁ__init____mutmut_3': xǁPrintCompleteǁ__init____mutmut_3, 
        'xǁPrintCompleteǁ__init____mutmut_4': xǁPrintCompleteǁ__init____mutmut_4, 
        'xǁPrintCompleteǁ__init____mutmut_5': xǁPrintCompleteǁ__init____mutmut_5, 
        'xǁPrintCompleteǁ__init____mutmut_6': xǁPrintCompleteǁ__init____mutmut_6, 
        'xǁPrintCompleteǁ__init____mutmut_7': xǁPrintCompleteǁ__init____mutmut_7, 
        'xǁPrintCompleteǁ__init____mutmut_8': xǁPrintCompleteǁ__init____mutmut_8
    }
    xǁPrintCompleteǁ__init____mutmut_orig.__name__ = 'xǁPrintCompleteǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(PrintComplete.PrintCompleteEvent)


class PrintPause(QEvent):
    """Print pause event

    Args:
        data (any): Data or message to pass onto the event
    """

    PrintPauseEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPrintPauseǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁPrintPauseǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁPrintPauseǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(PrintPause, self).__init__(PrintPause.PrintPauseEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintPauseǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(PrintPause, self).__init__(None)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintPauseǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(PrintPause.PrintPauseEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintPauseǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(PrintPause, None).__init__(PrintPause.PrintPauseEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintPauseǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(PrintPause.PrintPauseEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintPauseǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(PrintPause, ).__init__(PrintPause.PrintPauseEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintPauseǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(PrintPause, self).__init__(PrintPause.PrintPauseEvent)

        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁPrintPauseǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(PrintPause, self).__init__(PrintPause.PrintPauseEvent)

        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁPrintPauseǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(PrintPause, self).__init__(PrintPause.PrintPauseEvent)

        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁPrintPauseǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPrintPauseǁ__init____mutmut_1': xǁPrintPauseǁ__init____mutmut_1, 
        'xǁPrintPauseǁ__init____mutmut_2': xǁPrintPauseǁ__init____mutmut_2, 
        'xǁPrintPauseǁ__init____mutmut_3': xǁPrintPauseǁ__init____mutmut_3, 
        'xǁPrintPauseǁ__init____mutmut_4': xǁPrintPauseǁ__init____mutmut_4, 
        'xǁPrintPauseǁ__init____mutmut_5': xǁPrintPauseǁ__init____mutmut_5, 
        'xǁPrintPauseǁ__init____mutmut_6': xǁPrintPauseǁ__init____mutmut_6, 
        'xǁPrintPauseǁ__init____mutmut_7': xǁPrintPauseǁ__init____mutmut_7, 
        'xǁPrintPauseǁ__init____mutmut_8': xǁPrintPauseǁ__init____mutmut_8
    }
    xǁPrintPauseǁ__init____mutmut_orig.__name__ = 'xǁPrintPauseǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(PrintPause.PrintPauseEvent)


class PrintResume(QEvent):
    """Print Resume event

    Args:
        data (any): Data or message to pass onto the event
    """

    PrintResumeEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPrintResumeǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁPrintResumeǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁPrintResumeǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(PrintResume, self).__init__(PrintResume.PrintResumeEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintResumeǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(PrintResume, self).__init__(None)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintResumeǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(PrintResume.PrintResumeEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintResumeǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(PrintResume, None).__init__(PrintResume.PrintResumeEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintResumeǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(PrintResume.PrintResumeEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintResumeǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(PrintResume, ).__init__(PrintResume.PrintResumeEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintResumeǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(PrintResume, self).__init__(PrintResume.PrintResumeEvent)

        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁPrintResumeǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(PrintResume, self).__init__(PrintResume.PrintResumeEvent)

        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁPrintResumeǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(PrintResume, self).__init__(PrintResume.PrintResumeEvent)

        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁPrintResumeǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPrintResumeǁ__init____mutmut_1': xǁPrintResumeǁ__init____mutmut_1, 
        'xǁPrintResumeǁ__init____mutmut_2': xǁPrintResumeǁ__init____mutmut_2, 
        'xǁPrintResumeǁ__init____mutmut_3': xǁPrintResumeǁ__init____mutmut_3, 
        'xǁPrintResumeǁ__init____mutmut_4': xǁPrintResumeǁ__init____mutmut_4, 
        'xǁPrintResumeǁ__init____mutmut_5': xǁPrintResumeǁ__init____mutmut_5, 
        'xǁPrintResumeǁ__init____mutmut_6': xǁPrintResumeǁ__init____mutmut_6, 
        'xǁPrintResumeǁ__init____mutmut_7': xǁPrintResumeǁ__init____mutmut_7, 
        'xǁPrintResumeǁ__init____mutmut_8': xǁPrintResumeǁ__init____mutmut_8
    }
    xǁPrintResumeǁ__init____mutmut_orig.__name__ = 'xǁPrintResumeǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(PrintResume.PrintResumeEvent)


class PrintCancelled(QEvent):
    """Print cancelled event

    Args:
        data (any): Data or message to pass onto the event
    """

    PrintCancelledEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPrintCancelledǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁPrintCancelledǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁPrintCancelledǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(PrintCancelled, self).__init__(PrintCancelled.PrintCancelledEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCancelledǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(PrintCancelled, self).__init__(None)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCancelledǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(PrintCancelled.PrintCancelledEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCancelledǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(PrintCancelled, None).__init__(PrintCancelled.PrintCancelledEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCancelledǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(PrintCancelled.PrintCancelledEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCancelledǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(PrintCancelled, ).__init__(PrintCancelled.PrintCancelledEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCancelledǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(PrintCancelled, self).__init__(PrintCancelled.PrintCancelledEvent)

        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁPrintCancelledǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(PrintCancelled, self).__init__(PrintCancelled.PrintCancelledEvent)

        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁPrintCancelledǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(PrintCancelled, self).__init__(PrintCancelled.PrintCancelledEvent)

        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁPrintCancelledǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPrintCancelledǁ__init____mutmut_1': xǁPrintCancelledǁ__init____mutmut_1, 
        'xǁPrintCancelledǁ__init____mutmut_2': xǁPrintCancelledǁ__init____mutmut_2, 
        'xǁPrintCancelledǁ__init____mutmut_3': xǁPrintCancelledǁ__init____mutmut_3, 
        'xǁPrintCancelledǁ__init____mutmut_4': xǁPrintCancelledǁ__init____mutmut_4, 
        'xǁPrintCancelledǁ__init____mutmut_5': xǁPrintCancelledǁ__init____mutmut_5, 
        'xǁPrintCancelledǁ__init____mutmut_6': xǁPrintCancelledǁ__init____mutmut_6, 
        'xǁPrintCancelledǁ__init____mutmut_7': xǁPrintCancelledǁ__init____mutmut_7, 
        'xǁPrintCancelledǁ__init____mutmut_8': xǁPrintCancelledǁ__init____mutmut_8
    }
    xǁPrintCancelledǁ__init____mutmut_orig.__name__ = 'xǁPrintCancelledǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(PrintCancelled.PrintCancelledEvent)


class PrintError(QEvent):
    """Print error event

    Args:
        data (any): Data or message to pass onto the event
    """

    PrintErrorEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁPrintErrorǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁPrintErrorǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁPrintErrorǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(PrintError, self).__init__(PrintError.PrintErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintErrorǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(PrintError, self).__init__(None)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintErrorǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(PrintError.PrintErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintErrorǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(PrintError, None).__init__(PrintError.PrintErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintErrorǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(PrintError.PrintErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintErrorǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(PrintError, ).__init__(PrintError.PrintErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁPrintErrorǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(PrintError, self).__init__(PrintError.PrintErrorEvent)
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁPrintErrorǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(PrintError, self).__init__(PrintError.PrintErrorEvent)
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁPrintErrorǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(PrintError, self).__init__(PrintError.PrintErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁPrintErrorǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁPrintErrorǁ__init____mutmut_1': xǁPrintErrorǁ__init____mutmut_1, 
        'xǁPrintErrorǁ__init____mutmut_2': xǁPrintErrorǁ__init____mutmut_2, 
        'xǁPrintErrorǁ__init____mutmut_3': xǁPrintErrorǁ__init____mutmut_3, 
        'xǁPrintErrorǁ__init____mutmut_4': xǁPrintErrorǁ__init____mutmut_4, 
        'xǁPrintErrorǁ__init____mutmut_5': xǁPrintErrorǁ__init____mutmut_5, 
        'xǁPrintErrorǁ__init____mutmut_6': xǁPrintErrorǁ__init____mutmut_6, 
        'xǁPrintErrorǁ__init____mutmut_7': xǁPrintErrorǁ__init____mutmut_7, 
        'xǁPrintErrorǁ__init____mutmut_8': xǁPrintErrorǁ__init____mutmut_8
    }
    xǁPrintErrorǁ__init____mutmut_orig.__name__ = 'xǁPrintErrorǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(PrintError.PrintErrorEvent)


class NetworkAdded(QEvent):
    """Network added event

    Args:
        data (any): Data or message to pass onto the event
    """

    NetworkAddedEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkAddedǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁNetworkAddedǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁNetworkAddedǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(NetworkAdded, self).__init__(NetworkAdded.NetworkAddedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkAddedǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(NetworkAdded, self).__init__(None)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkAddedǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(NetworkAdded.NetworkAddedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkAddedǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(NetworkAdded, None).__init__(NetworkAdded.NetworkAddedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkAddedǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(NetworkAdded.NetworkAddedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkAddedǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(NetworkAdded, ).__init__(NetworkAdded.NetworkAddedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkAddedǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(NetworkAdded, self).__init__(NetworkAdded.NetworkAddedEvent)
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkAddedǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(NetworkAdded, self).__init__(NetworkAdded.NetworkAddedEvent)
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁNetworkAddedǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(NetworkAdded, self).__init__(NetworkAdded.NetworkAddedEvent)
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁNetworkAddedǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkAddedǁ__init____mutmut_1': xǁNetworkAddedǁ__init____mutmut_1, 
        'xǁNetworkAddedǁ__init____mutmut_2': xǁNetworkAddedǁ__init____mutmut_2, 
        'xǁNetworkAddedǁ__init____mutmut_3': xǁNetworkAddedǁ__init____mutmut_3, 
        'xǁNetworkAddedǁ__init____mutmut_4': xǁNetworkAddedǁ__init____mutmut_4, 
        'xǁNetworkAddedǁ__init____mutmut_5': xǁNetworkAddedǁ__init____mutmut_5, 
        'xǁNetworkAddedǁ__init____mutmut_6': xǁNetworkAddedǁ__init____mutmut_6, 
        'xǁNetworkAddedǁ__init____mutmut_7': xǁNetworkAddedǁ__init____mutmut_7, 
        'xǁNetworkAddedǁ__init____mutmut_8': xǁNetworkAddedǁ__init____mutmut_8
    }
    xǁNetworkAddedǁ__init____mutmut_orig.__name__ = 'xǁNetworkAddedǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(NetworkAdded.NetworkAddedEvent)


class NetworkDeleted(QEvent):
    """Network deleted event

    Args:
        data (any): Data or message to pass onto the event
    """

    NetworkDeletedEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkDeletedǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁNetworkDeletedǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁNetworkDeletedǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(NetworkDeleted, self).__init__(NetworkDeleted.NetworkDeletedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkDeletedǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(NetworkDeleted, self).__init__(None)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkDeletedǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(NetworkDeleted.NetworkDeletedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkDeletedǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(NetworkDeleted, None).__init__(NetworkDeleted.NetworkDeletedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkDeletedǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(NetworkDeleted.NetworkDeletedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkDeletedǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(NetworkDeleted, ).__init__(NetworkDeleted.NetworkDeletedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkDeletedǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(NetworkDeleted, self).__init__(NetworkDeleted.NetworkDeletedEvent)
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkDeletedǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(NetworkDeleted, self).__init__(NetworkDeleted.NetworkDeletedEvent)
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁNetworkDeletedǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(NetworkDeleted, self).__init__(NetworkDeleted.NetworkDeletedEvent)
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁNetworkDeletedǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkDeletedǁ__init____mutmut_1': xǁNetworkDeletedǁ__init____mutmut_1, 
        'xǁNetworkDeletedǁ__init____mutmut_2': xǁNetworkDeletedǁ__init____mutmut_2, 
        'xǁNetworkDeletedǁ__init____mutmut_3': xǁNetworkDeletedǁ__init____mutmut_3, 
        'xǁNetworkDeletedǁ__init____mutmut_4': xǁNetworkDeletedǁ__init____mutmut_4, 
        'xǁNetworkDeletedǁ__init____mutmut_5': xǁNetworkDeletedǁ__init____mutmut_5, 
        'xǁNetworkDeletedǁ__init____mutmut_6': xǁNetworkDeletedǁ__init____mutmut_6, 
        'xǁNetworkDeletedǁ__init____mutmut_7': xǁNetworkDeletedǁ__init____mutmut_7, 
        'xǁNetworkDeletedǁ__init____mutmut_8': xǁNetworkDeletedǁ__init____mutmut_8
    }
    xǁNetworkDeletedǁ__init____mutmut_orig.__name__ = 'xǁNetworkDeletedǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(NetworkDeleted)


class NetworkScan(QEvent):
    """Network scanned event

    Args:
        data (any): Data or message to pass onto the event
    """

    NetworkScanEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        args = [data, *args]# type: ignore
        kwargs = {**kwargs}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkScanǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁNetworkScanǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁNetworkScanǁ__init____mutmut_orig(self, data, *args, **kwargs):
        super(NetworkScan, self).__init__(NetworkScan.NetworkScanEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkScanǁ__init____mutmut_1(self, data, *args, **kwargs):
        super(NetworkScan, self).__init__(None)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkScanǁ__init____mutmut_2(self, data, *args, **kwargs):
        super(None, self).__init__(NetworkScan.NetworkScanEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkScanǁ__init____mutmut_3(self, data, *args, **kwargs):
        super(NetworkScan, None).__init__(NetworkScan.NetworkScanEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkScanǁ__init____mutmut_4(self, data, *args, **kwargs):
        super(self).__init__(NetworkScan.NetworkScanEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkScanǁ__init____mutmut_5(self, data, *args, **kwargs):
        super(NetworkScan, ).__init__(NetworkScan.NetworkScanEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkScanǁ__init____mutmut_6(self, data, *args, **kwargs):
        super(NetworkScan, self).__init__(NetworkScan.NetworkScanEvent)
        self.data = None
        self.args = args
        self.kwargs = kwargs

    def xǁNetworkScanǁ__init____mutmut_7(self, data, *args, **kwargs):
        super(NetworkScan, self).__init__(NetworkScan.NetworkScanEvent)
        self.data = data
        self.args = None
        self.kwargs = kwargs

    def xǁNetworkScanǁ__init____mutmut_8(self, data, *args, **kwargs):
        super(NetworkScan, self).__init__(NetworkScan.NetworkScanEvent)
        self.data = data
        self.args = args
        self.kwargs = None
    
    xǁNetworkScanǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkScanǁ__init____mutmut_1': xǁNetworkScanǁ__init____mutmut_1, 
        'xǁNetworkScanǁ__init____mutmut_2': xǁNetworkScanǁ__init____mutmut_2, 
        'xǁNetworkScanǁ__init____mutmut_3': xǁNetworkScanǁ__init____mutmut_3, 
        'xǁNetworkScanǁ__init____mutmut_4': xǁNetworkScanǁ__init____mutmut_4, 
        'xǁNetworkScanǁ__init____mutmut_5': xǁNetworkScanǁ__init____mutmut_5, 
        'xǁNetworkScanǁ__init____mutmut_6': xǁNetworkScanǁ__init____mutmut_6, 
        'xǁNetworkScanǁ__init____mutmut_7': xǁNetworkScanǁ__init____mutmut_7, 
        'xǁNetworkScanǁ__init____mutmut_8': xǁNetworkScanǁ__init____mutmut_8
    }
    xǁNetworkScanǁ__init____mutmut_orig.__name__ = 'xǁNetworkScanǁ__init__'

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(NetworkScan.NetworkScanEvent)
