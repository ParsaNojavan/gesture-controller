from __future__ import annotations


class ChangeFilter:

    def __init__(
        self,
        minimum_change: float = 1.0,
    ) -> None:
        if minimum_change < 0.0:
            raise ValueError("minimum_change cannot be negative")

        self.minimum_change = minimum_change
        self._last_value: float | None = None

    def should_update(self, value: float) -> bool:
        if self._last_value is None:
            self._last_value = value
            return True

        if abs(value - self._last_value) < self.minimum_change:
            return False

        self._last_value = value
        return True

    def reset(self) -> None:
        self._last_value = None
