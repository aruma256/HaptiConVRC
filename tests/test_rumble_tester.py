from unittest.mock import Mock, call
from hapticonvrc.rumble_tester import RumbleTester


def test_send_test_values():
    rumble_tester = RumbleTester("/test_address")
    rumble_tester.osc_client = mock_osc_client = Mock()

    rumble_tester.send_test_values()

    expected_calls = [call("/test_address", 1.)] * 100
    expected_calls += [call("/test_address", 0.)]
    mock_osc_client.send_message.assert_has_calls(expected_calls)
    assert mock_osc_client.send_message.call_count == 101
