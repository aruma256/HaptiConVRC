from hapticonvrc.rumble_config import RumbleConfig


def test_rumble_config():
    config = RumbleConfig()

    assert config.l_level_on_start == 10
    assert config.l_level_on_move_max == 9
    assert config.r_level_on_start == 11
    assert config.r_level_on_move_max == 10

    config.l_level_on_start = 1
    config.l_level_on_move_max = 2
    config.r_level_on_start = 3
    config.r_level_on_move_max = 4

    assert config.l_level_on_start == 1
    assert config.l_level_on_move_max == 2
    assert config.r_level_on_start == 3
    assert config.r_level_on_move_max == 4
