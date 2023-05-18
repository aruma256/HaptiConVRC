from .osc_value_provider import OSCValueProvider


class TailTracker:
    def __init__(self, osc_value_provider: OSCValueProvider) -> None:
        self._osc_value_provider = osc_value_provider
        self._initialized = False
        self._position = 0.

    def initialized(self) -> bool:
        return self._initialized

    def update(self) -> None:
        left, right = self._osc_value_provider.get_latest_values()
        if left is not None and right is not None:
            self._initialized = True
            self._position = left - right

    def get_position(self) -> float:
        assert self.initialized()
        return self._position
