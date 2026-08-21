import pytest

from gesture_controller.utils.change_filter import ChangeFilter


def test_first_value_should_update():
    change_filter = ChangeFilter(minimum_change=2.0)

    assert change_filter.should_update(50.0) is True


def test_small_changes_are_ignored():
    change_filter = ChangeFilter(minimum_change=2.0)

    change_filter.should_update(50.0)

    assert change_filter.should_update(51.0) is False


def test_large_changes_are_accepted():
    change_filter = ChangeFilter(minimum_change=2.0)

    change_filter.should_update(50.0)

    assert change_filter.should_update(53.0) is True


def test_negative_minimum_change_is_invalid():
    with pytest.raises(ValueError):
        ChangeFilter(minimum_change=-1.0)
