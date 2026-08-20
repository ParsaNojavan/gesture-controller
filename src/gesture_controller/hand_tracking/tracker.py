from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import mediapipe as mp


@dataclass
class HandDetectionResult:

    hands: list[list]


class HandTracker:

    def __init__(
        self,
        model_path: str | Path,
        num_hands: int = 1,
        min_hand_detection_confidence: float = 0.5,
        min_hand_presence_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        model_path = Path(model_path)

        if not model_path.exists():
            raise FileNotFoundError(
                f"Hand landmarker model was not found: {model_path}"
            )

        base_options = mp.tasks.BaseOptions(
            model_asset_path=str(model_path)
        )

        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=num_hands,
            min_hand_detection_confidence=min_hand_detection_confidence,
            min_hand_presence_confidence=min_hand_presence_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        self._landmarker = (
            mp.tasks.vision.HandLandmarker.create_from_options(
                options
            )
        )

    def detect(
        self,
        frame_bgr,
        timestamp_ms: int,
    ) -> HandDetectionResult:

        frame_rgb = cv2.cvtColor(
            frame_bgr,
            cv2.COLOR_BGR2RGB,
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb,
        )

        result = self._landmarker.detect_for_video(
            mp_image,
            timestamp_ms,
        )

        return HandDetectionResult(
            hands=result.hand_landmarks
        )

    def close(self) -> None:

        self._landmarker.close()

    def __enter__(self) -> HandTracker:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
