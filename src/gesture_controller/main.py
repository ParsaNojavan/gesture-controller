from pathlib import Path
import time

import cv2

from gesture_controller.camera.webcam import Webcam
from gesture_controller.hand_tracking.drawing import draw_hand_landmarks
from gesture_controller.hand_tracking.tracker import HandTracker


WINDOW_NAME = "Gesture System Controller"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "assets" / "hand_landmarker.task"


def main() -> None:
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    start_time = time.perf_counter()
    last_frame_time = start_time
    
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

                if detection_result.hands:
                    first_hand = detection_result.hands[0]

                    draw_hand_landmarks(
                        frame,
                        first_hand,
                        show_indices=True,
                    )

                    cv2.putText(
                        frame,
                        "Hand detected",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
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

                cv2.putText(
                    frame,
                    "Webcam is working",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

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
