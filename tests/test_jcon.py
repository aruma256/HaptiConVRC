# Written with ChatGPT

from unittest.mock import Mock, patch

import pytest

from hapticonvrc.jcon import Jcon


VENDOR_ID = 1406
PRODUCT_ID_L = 8198


class TestJcon:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.jcon = Jcon("L")
        self.jcon._device = Mock()

    def test_init(self):
        with pytest.raises(AssertionError):
            Jcon("X")
        Jcon("L")
        Jcon("R")

    @patch('hid.device')
    def test_connect(self, mock_hid_device):
        mock_hid_device.return_value = self.jcon._device
        self.jcon.connect()
        mock_hid_device.assert_called_once()
        self.jcon._device.open.assert_called_once_with(1406, 8198)

    @pytest.mark.parametrize('rumble_level, expected_packet', [
        (11, [0x10, 0] + [1, 0, 0b100, 0] * 2),  # max rumble level
        (5, [0x10, 0] + [1, 0, 0b011100, 0] * 2),  # half rumble level
        (0, [0x10, 0] + [1, 0, 0b110000, 0] * 2),  # min rumble level
    ])
    def test_send_rumble(self, rumble_level, expected_packet):
        self.jcon.send_rumble(rumble_level)
        self.jcon._device.write.assert_called_once_with(expected_packet)

    def test_get_packet_id(self):
        assert self.jcon._get_packet_id() == 0
        assert self.jcon._get_packet_id() == 1
        self.jcon._packet_id = 15
        assert self.jcon._get_packet_id() == 15
        assert self.jcon._get_packet_id() == 0
