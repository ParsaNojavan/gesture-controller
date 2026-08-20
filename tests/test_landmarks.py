import pytest

from gesture_controller.hand_tracking.landmarks import (
    INDEX_PIP,
    INDEX_TIP,
    MIDDLE_PIP,
    MIDDLE_TIP,
    Point2D,
    distance_between,
    is_finger_open,
)


def create_points() -> list[Point2D]:

    return [
        Point2D(x=0.5, y=0.5)
        for _ in range(21)
    ]


def test_distance_between_two_points():
    points = create_points()

    points[0] = Point2D(x=0.0, y=0.0)
    points[1] = Point2D(x=0.3, y=0.4)

    distance = distance_between(
        points,
        first_index=0,
        second_index=1,
    )

    assert distance == pytest.approx(0.5)


def test_finger_is_open_when_tip_is_above_pip():
    points = create_points()

    points[INDEX_PIP] = Point2D(x=0.5, y=0.5)
    points[INDEX_TIP] = Point2D(x=0.5, y=0.3)

    assert is_finger_open(
        points,
        tip_index=INDEX_TIP,
        pip_index=INDEX_PIP,
    ) is True


def test_finger_is_closed_when_tip_is_below_pip():
    points = create_points()

    points[MIDDLE_PIP] = Point2D(x=0.5, y=0.5)
    points[MIDDLE_TIP] = Point2D(x=0.5, y=0.6)

    assert is_finger_open(
        points,
        tip_index=MIDDLE_TIP,
        pip_index=MIDDLE_PIP,
    ) is False


def test_finger_is_closed_when_tip_is_too_close_to_pip():
    points = create_points()

    points[INDEX_PIP] = Point2D(x=0.5, y=0.5)

    points[INDEX_TIP] = Point2D(x=0.5, y=0.49)

    assert is_finger_open(
        points,
        tip_index=INDEX_TIP,
        pip_index=INDEX_PIP,
    ) is False
