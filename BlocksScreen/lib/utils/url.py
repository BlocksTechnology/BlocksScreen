
class URLTYPE(object):
    _prefix_type = ["ws://", "wss://", "http://", "https://"]
    link_type = ["rest", "websocket"]

    def __init__(self, host: str, port=None, type: str = "rest"):
        # self._prefix:str =
        if isinstance(port, int) is False and port is not None:
            raise AttributeError("If port is specified it can only be an integer")

        if type not in self.link_type:
            raise AttributeError(f"Url type can only be of: {self.link_type}")

        self._websocket_suffix: str = "/websocket"

        self._host: str = host
        self._port = port
        self._type = type.lower()
        self._build_url
        # self._url = self._prefix_type[self._type] + self._host + ":" + str(self._port) + self._websocket_suffix

    def _build_url(self) -> None:
        if self._type == "rest":
            self._url = (
                self.link_type[2] + self._host
                if self._host.endswith(".com")
                else self.link_type[2] + self._host + ".com"
            )

        if self._type == "websocket":
            self._url = (
                self.link_type[0]
                + self._host
                + ":"
                + str(self._port)
                + self._websocket_suffix
            )

    def type(self) -> str:
        return self.__class__.__name__

    @property
    def url_link(self):
        return self._url

    @url_link.setter
    def url_link(self, host, port, type):
        if self._type == "rest":
            if port is None:
                self._url = (
                    self.link_type[2] + host
                    if host.endswith(".com")
                    else self.link_type[2] + host + ".com"
                )
            else:
                self._url = (
                    self.link_type[2] + host + ":" + port
                    if host.endswith(".com")
                    else self.link_type[2] + host + ":" + port + ".com"
                )

        if self._type == "websocket":
            self._url = (
                self.link_type[0]
                + self._host
                + ":"
                + str(self._port)
                + self._websocket_suffix
            )

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}(host = {self._host}, port= {self._port}, type= {self._type})"

    def __str__(self) -> str:
        return self._url