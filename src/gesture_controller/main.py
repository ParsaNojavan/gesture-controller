from pathlib import Path
import time

import cv2

from gesture_controller.camera.webcam import Webcam
from gesture_controller.hand_tracking.drawing import draw_hand_landmarks
from gesture_controller.hand_tracking.tracker import HandTracker
from gesture_controller.gestures.models import GestureMode
from gesture_controller.gestures.recognizer import GestureRecognizer
from gesture_controller.hand_tracking.landmarks import (
    landmarks_to_points,
)
from gesture_controller.hand_tracking.landmarks import (
    THUMB_TIP, INDEX_TIP, MIDDLE_TIP,
    distance_between, landmarks_to_points,
    map_distance_to_percentage,
)
from gesture_controller.utils.smoothing import ValueSmoother


WINDOW_NAME = "Gesture System Controller"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "assets" / "hand_landmarker.task"


def main() -> None:
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    start_time = time.perf_counter()
    last_frame_time = start_time

    gesture_recognizer = GestureRecognizer()
    volume_smoother = ValueSmoother(alpha=0.25)
    brightness_smoother = ValueSmoother(alpha=0.25)
    
    try:
        with (Webcam(
                camera_index=0,
                width=640,
                height=480,
                mirror=True,
            ) as webcam,
            HandTracker(
                model_path=MODEL_PATH,
                num_hands=1,
            ) as hand_tracker,
        ):


            while True:
                frame = webcam.read()

                timestamp_ms = int(
                    (time.perf_counter() - start_time) * 1000
                )

                detection_result = hand_tracker.detect(
                    frame_bgr=frame,
                    timestamp_ms=timestamp_ms,
                )

                gesture_mode = GestureMode.NONE
                percentage = None

                if detection_result.hands:
                    first_hand = detection_result.hands[0]

                    points = landmarks_to_points(first_hand)
                    gesture_mode = gesture_recognizer.recognize(points)

                    percentage: float | None = None

                    if gesture_mode == GestureMode.VOLUME:
                        distance = distance_between(
                            points,
                            first_index=THUMB_TIP,
                            second_index=MIDDLE_TIP
                        )

                        raw_percentage = map_distance_to_percentage(distance)
                        percentage = volume_smoother.update(raw_percentage)

                    elif gesture_mode == GestureMode.BRIGHTNESS:
                        distance = distance_between(
                            points,
                            first_index=THUMB_TIP,
                            second_index=INDEX_TIP
                        )

                        raw_percentage = map_distance_to_percentage(distance)
                        percentage = brightness_smoother.update(raw_percentage)

                    draw_hand_landmarks(
                        frame,
                        first_hand,
                        show_indices=True,
                    )

                    if gesture_mode == GestureMode.VOLUME:
                        gesture_text = "MODE: VOLUME"
                        gesture_color = (255, 100, 0)

                    elif gesture_mode == GestureMode.BRIGHTNESS:
                        gesture_text = "MODE: BRIGHTNESS"
                        gesture_color = (0, 255, 255)

                    else:
                        gesture_text = "MODE: INACTIVE"
                        gesture_color = (0, 0, 255)

                    cv2.putText(
                        frame,
                        gesture_text,
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        gesture_color,
                        2,
                    )

                    if percentage is not None:
                        percentage_text = f"VALUE: {percentage:.0f}%"

                        cv2.putText(
                            frame,
                            percentage_text,
                            (30, 85),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            gesture_color,
                            2,
                        )

                else:
                    cv2.putText(
                        frame,
                        "No hand detected",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2,
                    ) 
                    
                last_frame_time = time.perf_counter()

                # cv2.putText(
                #     frame,
                #     "Webcam is working",
                #     (30, 50),
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     1,
                #     (0, 255, 0),
                #     2,
                # )

                cv2.putText(
                    frame,
                    "Press ESC or Q to exit",
                    (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

                cv2.imshow(WINDOW_NAME, frame)

                key = cv2.waitKey(1) & 0xFF

                if key in (27, ord("q")):
                    break

    except RuntimeError as error:
        print(f"Camera error: {error}")

    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
