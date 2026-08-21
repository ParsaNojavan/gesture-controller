import pytest

from gesture_controller.utils.smoothing import ValueSmoother


def test_first_value_is_returned_directly():
    smoother = ValueSmoother(alpha=0.25)

    result = smoother.update(80.0)

    assert result == pytest.approx(80.0)


def test_second_value_is_smoothed():
    smoother = ValueSmoother(alpha=0.25)

    smoother.update(0.0)
    result = smoother.update(100.0)

    # 0.25 * 100 + 0.75 * 0 = 25
    assert result == pytest.approx(25.0)


def test_reset_clears_previous_value():
    smoother = ValueSmoother(alpha=0.25)

    smoother.update(20.0)
    smoother.reset()

    assert smoother.value is None


def test_invalid_alpha_raises_error():
    with pytest.raises(ValueError):
        ValueSmoother(alpha=0.0)

    with pytest.raises(ValueError):
        ValueSmoother(alpha=1.5)
