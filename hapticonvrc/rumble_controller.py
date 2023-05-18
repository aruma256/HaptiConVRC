import random

from .jcon import Jcon


class RumbleController:
    def __init__(self) -> None:
        self._jcon_L = None
        self._jcon_R = None
        self._prev_left = None
        self._prev_right = None

    def _get_jcon(self, side) -> Jcon:
        assert side in {"L", "R"}
        return Jcon(side)

    def connect(self, side: str) -> None:
        jcon = self._get_jcon(side)
        jcon.connect()
        if side == "L":
            self._jcon_L = jcon
        else:
            self._jcon_R = jcon

    def update(self, left: float | None, right: float | None) -> None:
        if self._jcon_L:
            if not left:
                left_rumble_level = 0
            elif not self._prev_left and left:
                left_rumble_level = 11
            else:
                left_rumble_level = random.choice(range(0, 9))
            self._jcon_L.send_rumble(left_rumble_level)
            self._prev_left = left
        if self._jcon_R:
            if not right:
                right_rumble_level = 0
            elif not self._prev_right and right:
                right_rumble_level = 11
            else:
                right_rumble_level = random.choice(range(0, 9))
            self._jcon_R.send_rumble(right_rumble_level)
            self._prev_right = right
