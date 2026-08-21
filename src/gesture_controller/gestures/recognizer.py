from __future__ import annotations

from typing import Sequence

from gesture_controller.gestures.models import GestureMode
from gesture_controller.hand_tracking.landmarks import (
    FingerStates,
    Point2D,
    get_finger_states,
)


class GestureRecognizer:

    def __init__(self, finger_open_margin: float = 0.015) -> None:
        self.finger_open_margin = finger_open_margin

    def recognize(self, points: Sequence[Point2D]) -> GestureMode:
        finger_states = get_finger_states(
            points,
            margin=self.finger_open_margin,
        )

        return self.recognize_from_finger_states(finger_states)

    @staticmethod
    def recognize_from_finger_states(
        finger_states: FingerStates,
    ) -> GestureMode:
        is_volume_gesture = (
            finger_states.middle
            and not finger_states.index
            and not finger_states.ring
            and not finger_states.pinky
        )

        if is_volume_gesture:
            return GestureMode.VOLUME

        is_brightness_gesture = (
            finger_states.index
            and not finger_states.middle
            and not finger_states.ring
            and not finger_states.pinky
        )

        if is_brightness_gesture:
            return GestureMode.BRIGHTNESS

        return GestureMode.NONE