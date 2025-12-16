"""Collection of all custom events used by the application"""

import typing
from PyQt6.QtCore import QEvent


class WebSocketConnecting(QEvent):
    """Connecting event for websocket

    Args:
        data (any): Data or message to pass onto the event
    """

    WebsocketConnectingEvent = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        super(WebSocketConnecting, self).__init__(
            WebSocketConnecting.WebsocketConnectingEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(WebSocketMessageReceived, self).__init__(
            WebSocketMessageReceived.WebsocketMessageReceivedEvent
        )
        self.method = method
        self.data = data
        self.metadata = metadata

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
        super(WebSocketOpen, self).__init__(WebSocketOpen.WebsocketOpenEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(WebSocketError, self).__init__(WebSocketError.WebsocketErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(WebSocketDisconnected, self).__init__(
            WebSocketDisconnected.WebsocketDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(WebSocketClose, self).__init__(WebSocketClose.WebsocketCloseEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        QEvent.__instancecheck__(self)
        super(KlippyShutdown, self).__init__(KlippyShutdown.KlippyShutdownEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(KlippyReady, self).__init__(KlippyReady.KlippyReadyEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(KlippyDisconnected, self).__init__(
            KlippyDisconnected.KlippyDisconnectedEvent
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(KlippyError, self).__init__(KlippyError.KlippyErrorEvent)
        self.data = data
        self.message = message

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
    ):  # Positional-only arguments "data", "method", "params", these need to be inserted in order or it wont work
        super(ReceivedFileData, self).__init__(ReceivedFileData.ReceivedFileDataEvent)
        self.data = data
        self.method = method
        self.params = params
        self.args = args
        self.kwargs = kwargs

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
        super(PrintStart, self).__init__(PrintStart.PrintStartEvent)
        self.file = filename
        self.file_metadata = kwargs
        self.kwargs = kwargs

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
        super(PrintComplete, self).__init__(PrintComplete.PrintCompleteEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(PrintPause, self).__init__(PrintPause.PrintPauseEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(PrintResume, self).__init__(PrintResume.PrintResumeEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(PrintCancelled, self).__init__(PrintCancelled.PrintCancelledEvent)

        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(PrintError, self).__init__(PrintError.PrintErrorEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(NetworkAdded, self).__init__(NetworkAdded.NetworkAddedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(NetworkDeleted, self).__init__(NetworkDeleted.NetworkDeletedEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

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
        super(NetworkScan, self).__init__(NetworkScan.NetworkScanEvent)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def type() -> QEvent.Type:
        """Return event type"""
        return QEvent.Type(NetworkScan.NetworkScanEvent)
