from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..rumble_joycon import RumbleJoyCon


class BaseEngine:

    def __init__(self, joycon: 'RumbleJoyCon') -> None:
        self._joycon = joycon

    def update(self, value: Any) -> None:
        pass
