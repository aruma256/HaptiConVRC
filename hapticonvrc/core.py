from threading import Thread
import time

from .osc_value_provider import OSCValueProvider
from .rumble_config import RumbleConfig
from .rumble_controller import RumbleController


class Core:
    def __init__(self) -> None:
        self.view = None
        self.rumble_config = RumbleConfig()
        self._rumble_controller = RumbleController(self.rumble_config)

    def connect_controller(self, side: str) -> None:
        self._rumble_controller.connect(side)

    def start_osc_server(self) -> None:
        self.value_provider = OSCValueProvider()
        self.value_provider.start()
        Thread(target=self._run, daemon=True).start()

    def _run(self) -> None:
        while True:
            left, right = self.value_provider.get_latest_values()
            self._rumble_controller.update(left, right)
            if self.view:
                self.view.on_position_updated(left)
            time.sleep(0.06)
