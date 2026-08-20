import cv2

from gesture_controller.camera.webcam import Webcam


WINDOW_NAME = "Gesture System Controller"


def main() -> None:
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

    try:
        with Webcam(
            camera_index=0,
            width=640,
            height=480,
            mirror=True,
        ) as webcam:


            while True:
                frame = webcam.read()

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
