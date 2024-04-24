from PyQt6.QtCore import QEvent


class WebSocketConnectingEvent(QEvent):
    """WebSocketConnectingEvent Event for websocket connecting to Moonraker

    Args:
        QEvent (_type_): QEvent type argument
    """

    wb_connecting_event_type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        raise NotImplementedError
        super(WebSocketConnectingEvent, self).__init__(
            WebSocketConnectingEvent.wb_connecting_event_type
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs
    @staticmethod
    def type() -> QEvent.Type:
        return QEvent.Type(WebSocketConnectingEvent.wb_connecting_event_type)


class WebSocketMessageReceivedEvent(QEvent):
    """WebSocketMessageReceivedEvent Event for message received from Moonrakers websocket

    Args:
        QEvent (_type_): QEvent type argument
    """

    message_event_type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, packet, method, params):
        super(WebSocketMessageReceivedEvent, self).__init__(
            self.message_event_type,
        )
        self.data = data
        self.packet = packet
        self.method = method
        self.params = params
        

    @staticmethod
    def type() -> QEvent.Type:
        return QEvent.Type(WebSocketMessageReceivedEvent.message_event_type)


class WebSocketOpenEvent(QEvent):
    """WebSocketOpenEvent Event for websocket connection to Moonraker

    Args:
        QEvent (_type_): QEvent type argument
    """

    wb_open_event_type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        super(WebSocketOpenEvent, self).__init__(WebSocketOpenEvent.wb_open_event_type)
        self.data = data
        self.args = args
        self.kwargs = kwargs

    
    @staticmethod
    def type() -> QEvent.Type:
        return QEvent.Type(WebSocketOpenEvent.wb_open_event_type)

class WebSocketErrorEvent(QEvent):
    """WebSocketErrorEvent Event for websocket error

    Args:
        QEvent (_type_): QEvent type argument
    """

    wb_error_event_type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        super(WebSocketErrorEvent, self).__init__(
            WebSocketErrorEvent.wb_error_event_type
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs


class WebSocketDisconnectEvent(QEvent):
    """WebSocketDisconnectEvent Event for websocket diconnection to Moonraker

    Args:
        QEvent (__type__): QEvent type argument
    """

    wb_disconnect_event_type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        super(WebSocketDisconnectEvent, self).__init__(
            WebSocketDisconnectEvent.wb_disconnect_event_type
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs

class KlippyShudownEvent(QEvent):
    
    kp_shutdown_event_type = QEvent.Type(QEvent.registerEventType())
    def __init__(self, data):
        super(KlippyShudownEvent, self).__init__(
            KlippyShudownEvent.kp_shutdown_event_type
        )
        self.data = data
    @staticmethod
    def type()-> QEvent.Type:
        return QEvent.Type(KlippyShudownEvent.kp_shutdown_event_type)


class KlippyReadyEvent(QEvent):
    """KlipperConnectEvent Event to klipper connection

    Args:
        QEvent (_type_): QEvent type argument
    """

    kp_ready_event_type = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, *args, **kwargs):
        super(KlippyReadyEvent, self).__init__(
            KlippyReadyEvent.kp_ready_event_type
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs
    @staticmethod
    def type() -> QEvent.Type:
        return QEvent.Type(KlippyReadyEvent.kp_ready_event_type)

class KlippyDisconnectedEvent(QEvent):
    """KlippyDisconnecedEvent Event for klippy state disconnected

    Args:
        QEvent (_type_): _description_

    Returns:
        _type_: _description_
    """
    kp_disconnected_event_type = QEvent.Type(QEvent.registerEventType())
    def __init__(self, data, *args, **kwargs):
        super(KlippyDisconnectedEvent, self).__init__(
            KlippyDisconnectedEvent.kp_disconnected_event_type
        )
        self.data = data
        self.args = args
        self.kwargs = kwargs
        
    @staticmethod
    def type()->QEvent.Type:
        return QEvent.Type(KlippyDisconnectedEvent.kp_disconnected_event_type)

class ReceivedFileDataEvent(QEvent):
    """ReceivedFileDataEvent Event for file related messages received 

    Args:
        QEvent (_type_): QEvent type argument
    """

    file_data_event = QEvent.Type(QEvent.registerEventType())

    def __init__(self, data, method, params):
        super(ReceivedFileDataEvent, self).__init__(
            self.file_data_event,
        )
        self.data = data
        self.method = method
        self.params = params
        

    @staticmethod
    def type() -> QEvent.Type:
        return QEvent.Type(ReceivedFileDataEvent.file_data_event)
