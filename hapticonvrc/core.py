from threading import Thread
import time

from .osc_value_provider import OSCValueProvider
from .rumble_controller import RumbleController
from .tail_tracker import TailTracker


class Core:
    def __init__(self) -> None:
        self.view = None

    def connect_controllers(self) -> None:
        self._rumble_controller = RumbleController()
        self._rumble_controller.start()

    def start_tail_tracker(self) -> None:
        value_provider = OSCValueProvider()
        value_provider.start()
        self._tail_tracker = TailTracker(value_provider)
        Thread(target=self._run, daemon=True).start()

    def _run(self) -> None:
        while True:
            self._tail_tracker.update()
            current_position = self._tail_tracker._position
            self._rumble_controller.update(current_position)
            if self.view:
                self.view.on_position_updated(current_position)
            time.sleep(0.06)
