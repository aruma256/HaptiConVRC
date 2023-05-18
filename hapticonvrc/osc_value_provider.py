from threading import Thread

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


class OSCValueProvider:
    def __init__(self, ip="127.0.0.1", port=9001) -> None:
        self._ip = ip
        self._port = port
        self._thread = None
        self.left = None
        self.right = None

    def _osc_handler(self, address: str, value: float) -> None:
        if address.endswith("L"):
            self.left = value
        elif address.endswith("R"):
            self.right = value

    def start(self) -> None:
        dispatcher = Dispatcher()
        dispatcher.map(
            "/avatar/parameters/Contact/Tail/*",
            self._osc_handler,
        )
        server = BlockingOSCUDPServer((self._ip, self._port), dispatcher)
        self._thread = Thread(target=server.serve_forever, daemon=True)
        self._thread.start()

    def get_latest_values(self) -> tuple[float | None, float | None]:
        return (self.left, self.right)
