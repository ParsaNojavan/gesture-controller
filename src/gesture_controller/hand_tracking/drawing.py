import cv2


HAND_CONNECTIONS = [
    # Thumb
    (0, 1), (1, 2), (2, 3), (3, 4),

    # Index finger
    (0, 5), (5, 6), (6, 7), (7, 8),

    # Middle finger
    (5, 9), (9, 10), (10, 11), (11, 12),

    # Ring finger
    (9, 13), (13, 14), (14, 15), (15, 16),

    # Pinky finger
    (13, 17), (17, 18), (18, 19), (19, 20),

    # Palm
    (0, 17),
]


def draw_hand_landmarks(
    image,
    landmarks,
    show_indices: bool = False,
) -> None:

    height, width, _ = image.shape

    for start_index, end_index in HAND_CONNECTIONS:
        start = landmarks[start_index]
        end = landmarks[end_index]

        start_point = (
            int(start.x * width),
            int(start.y * height),
        )

        end_point = (
            int(end.x * width),
            int(end.y * height),
        )

        cv2.line(
            image,
            start_point,
            end_point,
            (255, 0, 0),
            2,
        )

    for index, landmark in enumerate(landmarks):
        x = int(landmark.x * width)
        y = int(landmark.y * height)

        cv2.circle(
            image,
            (x, y),
            5,
            (0, 255, 0),
            -1,
        )

        if show_indices:
            cv2.putText(
                image,
                str(index),
                (x + 5, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (255, 255, 255),
                1,
            )
