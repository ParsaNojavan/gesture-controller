class ValueSmoother:

    def __init__(
        self,
        alpha: float = 0.25,
        initial_value: float | None = None,
    ) -> None:
        if not 0.0 < alpha <= 1.0:
            raise ValueError("alpha must be in the range (0, 1]")

        self.alpha = alpha
        self._value = initial_value

    @property
    def value(self) -> float | None:
        return self._value

    def update(self, new_value: float) -> float:
        if self._value is None:
            self._value = new_value
        else:
            self._value = (
                self.alpha * new_value
                + (1.0 - self.alpha) * self._value
            )

        return self._value

    def reset(self, value: float | None = None) -> None:
        self._value = value