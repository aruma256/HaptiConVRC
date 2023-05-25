from dataclasses import dataclass


@dataclass
class RumbleConfig:
    l_level_on_start: int = 10
    l_level_on_move_max: int = 9
    r_level_on_start: int = 11
    r_level_on_move_max: int = 10
