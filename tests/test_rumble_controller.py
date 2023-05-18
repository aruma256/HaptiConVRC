# Written with ChatGPT


from unittest.mock import Mock, patch

from hapticonvrc.rumble_controller import RumbleController


def test_connect_l():
    controller = RumbleController()
    jcon = Mock()
    controller._get_jcon = lambda side: jcon

    controller.connect("L")
    assert controller._jcon_L == jcon
    assert jcon.connect.called_once()


def test_connect_r():
    controller = RumbleController()
    jcon = Mock()
    controller._get_jcon = lambda side: jcon

    controller.connect("R")
    assert controller._jcon_R == jcon
    assert jcon.connect.called_once()


@patch('random.choice')
def test_update_left(mock_choice):
    mock_choice.return_value = 3
    controller = RumbleController()
    jcon = Mock()
    controller._jcon_L = jcon

    # 1. -> 0.
    controller._prev_left = 1.
    controller.update(0., None)
    jcon.send_rumble.assert_called_once_with(0)
    assert controller._prev_left == 0.
    jcon.reset_mock()

    # 0. -> 1.
    controller._prev_left = 0.
    controller.update(1., None)
    jcon.send_rumble.assert_called_once_with(11)
    assert controller._prev_left == 1.
    jcon.reset_mock()

    # 1. -> 1.
    controller._prev_left = 1.
    controller.update(1., None)
    jcon.send_rumble.assert_called_once_with(3)
    assert controller._prev_left == 1.
    jcon.reset_mock()


@patch('random.choice')
def test_update_right(mock_choice):
    mock_choice.return_value = 3
    controller = RumbleController()
    jcon = Mock()
    controller._jcon_R = jcon

    # 1. -> 0.
    controller._prev_right = 1.
    controller.update(None, 0.)
    jcon.send_rumble.assert_called_once_with(0)
    assert controller._prev_right == 0.
    jcon.reset_mock()

    # 0. -> 1.
    controller._prev_right = 0.
    controller.update(None, 1.)
    jcon.send_rumble.assert_called_once_with(11)
    assert controller._prev_right == 1.
    jcon.reset_mock()

    # 1. -> 1.
    controller._prev_right = 1.
    controller.update(None, 1.)
    jcon.send_rumble.assert_called_once_with(3)
    assert controller._prev_right == 1.
    jcon.reset_mock()
