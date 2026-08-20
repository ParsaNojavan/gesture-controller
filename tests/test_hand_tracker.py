from gesture_controller.hand_tracking.tracker import (
    HandDetectionResult,
)


def test_hand_detection_result_defaults_to_list_of_hands():
    result = HandDetectionResult(hands=[])

    assert result.hands == []
