from .jcon import Jcon


class RumbleController:
    def __init__(self) -> None:
        self._jcon_L = None
        self._jcon_R = None

    def start(self) -> None:
        self._jcon_L = Jcon("L")
        self._jcon_L.connect()
        self._jcon_R = Jcon("R")
        self._jcon_R.connect()

    def update(self, pos: float) -> None:
        assert self._jcon_L and self._jcon_R
        if pos > 0:
            rumble_level = round(pos * 3.3 * 10)
            self._jcon_L.send_rumble(min(rumble_level, 11))
            self._jcon_R.send_rumble(0)
            print("Left", rumble_level)
        elif pos < 0:
            pos = abs(pos)
            rumble_level = round(pos * 3.3 * 10)
            self._jcon_L.send_rumble(0)
            self._jcon_R.send_rumble(min(rumble_level, 11))
            print("Right", rumble_level)
        else:
            self._jcon_L.send_rumble(0)
            self._jcon_R.send_rumble(0)
