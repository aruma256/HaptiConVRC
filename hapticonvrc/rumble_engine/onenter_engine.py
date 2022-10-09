from typing import Any, TYPE_CHECKING

from .base_engine import BaseEngine

if TYPE_CHECKING:
    from ..rumble_joycon import RumbleJoyCon


class OnEnterEngine(BaseEngine):

    def __init__(self, joycon: 'RumbleJoyCon') -> None:
        self._current_value = False
        super().__init__(joycon)

    def _get_current_amp(self):
        res = int(self._current_value)
        self._current_value = False
        return res

    def update(self, value: bool) -> None:
        self._current_value = True
