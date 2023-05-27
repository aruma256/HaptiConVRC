from unittest.mock import Mock, patch

import pytest

from hapticonvrc.rumble_config import RumbleConfig
from hapticonvrc.rumble_controller import RumbleController


def test_connect_l():
    controller = RumbleController(RumbleConfig())
    jcon = Mock()
    controller._get_jcon = lambda side: jcon

    controller.connect("L")
    assert controller._jcon_L == jcon
    assert jcon.connect.called_once()


def test_connect_r():
    controller = RumbleController(RumbleConfig())
    jcon = Mock()
    controller._get_jcon = lambda side: jcon

    controller.connect("R")
    assert controller._jcon_R == jcon
    assert jcon.connect.called_once()


@pytest.mark.parametrize('prev_left, current_left, expected_rumble', [
    (0., 0., 0),
    (1., 0., 0),
    (0., 1., 10),
    (1., 1., 3)
])
@patch('random.choice')
def test_update_left(mock_choice,
                     prev_left,
                     current_left,
                     expected_rumble):
    mock_choice.return_value = 3
    controller = RumbleController(RumbleConfig())
    jcon = Mock()
    controller._jcon_L = jcon

    controller._prev_left = prev_left
    controller.update(current_left, 0.)
    jcon.send_rumble.assert_called_once_with(expected_rumble)
    assert controller._prev_left == current_left
    jcon.reset_mock()


@pytest.mark.parametrize('prev_right, current_right, expected_rumble', [
    (0., 0., 0),
    (1., 0., 0),
    (0., 1., 11),
    (1., 1., 3)
])
@patch('random.choice')
def test_update_right(mock_choice, prev_right, current_right, expected_rumble):
    mock_choice.return_value = 3
    controller = RumbleController(RumbleConfig())
    jcon = Mock()
    controller._jcon_R = jcon

    controller._prev_right = prev_right
    controller.update(0., current_right)
    jcon.send_rumble.assert_called_once_with(expected_rumble)
    assert controller._prev_right == current_right
    jcon.reset_mock()
