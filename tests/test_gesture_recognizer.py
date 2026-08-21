import pytest

from gesture_controller.gestures.models import GestureMode
from gesture_controller.gestures.recognizer import GestureRecognizer
from gesture_controller.hand_tracking.landmarks import FingerStates


@pytest.fixture
def recognizer() -> GestureRecognizer:

    return GestureRecognizer()


def test_volume_gesture_when_only_middle_finger_is_open(
    recognizer: GestureRecognizer,
):
    finger_states = FingerStates(
        index=False,
        middle=True,
        ring=False,
        pinky=False,
    )

    result = recognizer.recognize_from_finger_states(
        finger_states
    )

    assert result == GestureMode.VOLUME


def test_brightness_gesture_when_only_index_finger_is_open(
    recognizer: GestureRecognizer,
):
    finger_states = FingerStates(
        index=True,
        middle=False,
        ring=False,
        pinky=False,
    )

    result = recognizer.recognize_from_finger_states(
        finger_states
    )

    assert result == GestureMode.BRIGHTNESS


@pytest.mark.parametrize(
    "finger_states",
    [

        FingerStates(
            index=False,
            middle=False,
            ring=False,
            pinky=False,
        ),

        FingerStates(
            index=True,
            middle=True,
            ring=False,
            pinky=False,
        ),

        FingerStates(
            index=True,
            middle=True,
            ring=True,
            pinky=True,
        ),

        FingerStates(
            index=False,
            middle=False,
            ring=True,
            pinky=False,
        ),

        FingerStates(
            index=False,
            middle=False,
            ring=False,
            pinky=True,
        ),
    ],
)
def test_other_hand_states_are_inactive(
    recognizer: GestureRecognizer,
    finger_states: FingerStates,
):
    result = recognizer.recognize_from_finger_states(
        finger_states
    )

    assert result == GestureMode.NONE
