from threading import Thread
from time import sleep
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..rumble_joycon import RumbleJoyCon


class BaseEngine:

    def __init__(self, joycon: 'RumbleJoyCon') -> None:
        self._amp_max = 12
        self._joycon = joycon
        self._show_level = False
        self._thread = Thread(target=self._loop, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def _loop(self):
        try:
            while True:
                amp = self._get_current_amp()
                amp_level = self._to_amp_level(amp)
                if amp_level:
                    self._joycon.send_rumble(amp_level)
                sleep(0.01)
        except OSError:
            print('JoyConとの接続が切れました。JoyConがスリープ状態になった可能性があります。')
            print('JoyConのボタンを押し再接続してから、HaptiConVRCを再実行してください。')

    def set_amp_max(self, amp: int) -> None:
        if not (0 <= amp <= 12):
            print('amp_maxは0以上12以下の整数にしてください')
        amp = min(amp, 12)
        amp = max(amp, 0)
        self._amp_max = amp

    def _to_amp_level(self, amp: float) -> int:
        assert 0 <= amp <= 1
        MAX = self._amp_max - 1
        return int(amp * MAX)

    def _get_current_amp(self) -> float:
        raise RuntimeError()

    def update(self, value: Any) -> None:
        pass
