from threading import Thread
from time import sleep
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..rumble_joycon import RumbleJoyCon


class BaseEngine:

    def __init__(self, joycon: 'RumbleJoyCon') -> None:
        self._joycon = joycon
        self._thread = Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self):
        while True:
            amp = self._get_current_amp()
            if amp:
                self._joycon.send_rumble(amp)
            sleep(0.01)

    def _get_current_amp(self) -> float:
        raise RuntimeError()

    def update(self, value: Any) -> None:
        pass
