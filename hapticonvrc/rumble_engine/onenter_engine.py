from typing import Any, TYPE_CHECKING

from .base_engine import BaseEngine

if TYPE_CHECKING:
    from ..rumble_joycon import RumbleJoyCon


class OnEnterEngine(BaseEngine):

    def __init__(self, joycon: 'RumbleJoyCon') -> None:
        super().__init__(joycon)

    def update(self, value: bool) -> None:
        if value:
            self._joycon.send_rumble()
