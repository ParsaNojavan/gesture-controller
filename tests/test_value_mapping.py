import pytest

from gesture_controller.hand_tracking.landmarks import (
    map_distance_to_percentage,
)


def test_minimum_distance_maps_to_zero_percent():
    result = map_distance_to_percentage(
        distance=0.03,
        minimum_distance=0.03,
        maximum_distance=0.30,
    )

    assert result == pytest.approx(0.0)


def test_middle_distance_maps_to_fifty_percent():
    result = map_distance_to_percentage(
        distance=0.165,
        minimum_distance=0.03,
        maximum_distance=0.30,
    )

    assert result == pytest.approx(50.0)


def test_maximum_distance_maps_to_hundred_percent():
    result = map_distance_to_percentage(
        distance=0.30,
        minimum_distance=0.03,
        maximum_distance=0.30,
    )

    assert result == pytest.approx(100.0)


def test_distance_below_minimum_is_clamped():
    result = map_distance_to_percentage(
        distance=0.0,
        minimum_distance=0.03,
        maximum_distance=0.30,
    )

    assert result == pytest.approx(0.0)


def test_distance_above_maximum_is_clamped():
    result = map_distance_to_percentage(
        distance=1.0,
        minimum_distance=0.03,
        maximum_distance=0.30,
    )

    assert result == pytest.approx(100.0)


def test_invalid_distance_range_raises_error():
    with pytest.raises(ValueError):
        map_distance_to_percentage(
            distance=0.1,
            minimum_distance=0.3,
            maximum_distance=0.03,
        )
