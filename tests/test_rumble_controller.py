# Written with ChatGPT


from unittest.mock import Mock
from hapticonvrc.jcon import Jcon
from hapticonvrc.rumble_controller import RumbleController


class TestRumbleController:
    def test_update_with_positive_pos(self):
        controller = RumbleController()
        controller._jcon_L = jcon_L = Mock(spec=Jcon)
        controller._jcon_R = jcon_R = Mock(spec=Jcon)

        controller.update(10 / 10 / 3.3)
        jcon_L.send_rumble.assert_called_with(10)
        jcon_R.send_rumble.assert_called_with(0)

        controller.update(12 / 10 / 3.3)
        jcon_L.send_rumble.assert_called_with(11)
        jcon_R.send_rumble.assert_called_with(0)

    def test_update_with_negative_pos(self):
        controller = RumbleController()
        controller._jcon_L = jcon_L = Mock(spec=Jcon)
        controller._jcon_R = jcon_R = Mock(spec=Jcon)

        controller.update(-10 / 10 / 3.3)
        jcon_L.send_rumble.assert_called_with(0)
        jcon_R.send_rumble.assert_called_with(10)

        controller.update(-12 / 10 / 3.3)
        jcon_L.send_rumble.assert_called_with(0)
        jcon_R.send_rumble.assert_called_with(11)

    def test_update_with_zero_pos(self):
        controller = RumbleController()
        controller._jcon_L = jcon_L = Mock(spec=Jcon)
        controller._jcon_R = jcon_R = Mock(spec=Jcon)

        controller.update(0)
        jcon_L.send_rumble.assert_called_with(0)
        jcon_R.send_rumble.assert_called_with(0)
