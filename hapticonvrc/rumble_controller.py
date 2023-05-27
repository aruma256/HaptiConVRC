import random

from .jcon import Jcon
from .rumble_config import RumbleConfig


class RumbleController:
    def __init__(self, rumble_config: RumbleConfig) -> None:
        self._jcon_L = None
        self._jcon_R = None
        self._prev_left = None
        self._prev_right = None
        self.config = rumble_config

    def _get_jcon(self, side) -> Jcon:
        assert side in {"L", "R"}
        return Jcon(side)

    def connect(self, side: str) -> bool:
        jcon = self._get_jcon(side)
        if jcon.connect():
            if side == "L":
                self._jcon_L = jcon
            else:
                self._jcon_R = jcon
            return True
        else:
            return False

    def update(self, left: float, right: float) -> None:
        if self._jcon_L:
            if left == 0:
                left_rumble_level = 0
            elif self._prev_left == 0 and left > 0:
                left_rumble_level = self.config.l_level_on_start
            else:
                left_rumble_level = random.choice(
                    range(0, self.config.l_level_on_move_max + 1)
                )
            self._jcon_L.send_rumble(left_rumble_level)
            self._prev_left = left
        if self._jcon_R:
            if right == 0:
                right_rumble_level = 0
            elif self._prev_right == 0 and right > 0:
                right_rumble_level = self.config.r_level_on_start
            else:
                right_rumble_level = random.choice(
                    range(0, self.config.r_level_on_move_max + 1)
                )
            self._jcon_R.send_rumble(right_rumble_level)
            self._prev_right = right
