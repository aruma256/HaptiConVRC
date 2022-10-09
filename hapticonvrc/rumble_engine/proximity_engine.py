import math
import random
from typing import Any, TYPE_CHECKING

from .base_engine import BaseEngine

if TYPE_CHECKING:
    from ..rumble_joycon import RumbleJoyCon


class ProximityEngine(BaseEngine):

    def __init__(self, joycon: 'RumbleJoyCon') -> None:
        self._prev = 0
        self._latest = 0
        super().__init__(joycon)

    def _get_current_amp(self) -> float:
        diff = abs(self._latest - self._prev)
        if not diff:
            return 0
        rand = math.exp(-(10 * random.random())**2)
        amp = min(rand + diff*5, 1)
        self._prev = self._latest
        return amp

    def update(self, value: float) -> None:
        self._latest = value
