# Written with ChatGPT

from unittest.mock import Mock

from hapticonvrc.tail_tracker import TailTracker


def test_tail_tracker_initialized():
    osc_value_provider = Mock()
    tracker = TailTracker(osc_value_provider)

    assert not tracker.initialized()

    osc_value_provider.get_latest_values.return_value = (-1.0, 1.5)
    tracker.update()

    assert tracker.initialized()


def test_tail_tracker_update():
    osc_value_provider = Mock()
    tracker = TailTracker(osc_value_provider)

    assert not tracker.initialized()

    osc_value_provider.get_latest_values.return_value = (-1.0, None)
    tracker.update()

    assert not tracker.initialized()

    osc_value_provider.get_latest_values.return_value = (-1.0, 1.5)
    tracker.update()

    assert tracker.initialized()
    assert tracker.get_position() == -2.5


def test_tail_tracker_position():
    osc_value_provider = Mock()
    tracker = TailTracker(osc_value_provider)

    osc_value_provider.get_latest_values.return_value = (-1.0, 1.5)
    tracker.update()

    assert tracker.get_position() == -2.5
