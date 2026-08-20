from __future__ import annotations

import cv2


class Webcam:

    def __init__(
        self,
        camera_index: int = 0,
        width: int | None = None,
        height: int | None = None,
        mirror: bool = True,
    ) -> None:
        self.camera_index = camera_index
        self.mirror = mirror

        self._capture = cv2.VideoCapture(camera_index)

        if not self._capture.isOpened():
            raise RuntimeError(
                f"Could not open camera at index {camera_index}."
            )
        
        if width is not None:
            self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)

        if height is not None:
            self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):

        success, frame = self._capture.read()

        if not success or frame is None:
            raise RuntimeError("Could not read frame from webcam.")

        if self.mirror:
            frame = cv2.flip(frame, 1)

        return frame

    def release(self) -> None:

        if self._capture.isOpened():
            self._capture.release()

    def __enter__(self) -> Webcam:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.release()
