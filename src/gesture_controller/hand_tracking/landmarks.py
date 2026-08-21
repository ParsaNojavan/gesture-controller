from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Sequence


WRIST = 0

THUMB_CMC = 1
THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4

INDEX_MCP = 5
INDEX_PIP = 6
INDEX_DIP = 7
INDEX_TIP = 8

MIDDLE_MCP = 9
MIDDLE_PIP = 10
MIDDLE_DIP = 11
MIDDLE_TIP = 12

RING_MCP = 13
RING_PIP = 14
RING_DIP = 15
RING_TIP = 16

PINKY_MCP = 17
PINKY_PIP = 18
PINKY_DIP = 19
PINKY_TIP = 20

THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12


@dataclass(frozen=True)
class Point2D:

    x: float
    y: float


def landmarks_to_points(landmarks: Sequence) -> list[Point2D]:

    return [
        Point2D(
            x=landmark.x,
            y=landmark.y,
        )
        for landmark in landmarks
    ]


def distance_between(
    points: Sequence[Point2D],
    first_index: int,
    second_index: int,
) -> float:

    first = points[first_index]
    second = points[second_index]

    return sqrt(
        (second.x - first.x) ** 2
        + (second.y - first.y) ** 2
    )


def is_finger_open(
    points: Sequence[Point2D],
    tip_index: int,
    pip_index: int,
    margin: float = 0.015,
) -> bool:

    tip = points[tip_index]
    pip = points[pip_index]

    return tip.y < (pip.y - margin)


@dataclass(frozen=True)
class FingerStates:

    index: bool
    middle: bool
    ring: bool
    pinky: bool


def get_finger_states(
    points: Sequence[Point2D],
    margin: float = 0.015,
) -> FingerStates:

    return FingerStates(
        index=is_finger_open(
            points,
            INDEX_TIP,
            INDEX_PIP,
            margin,
        ),
        middle=is_finger_open(
            points,
            MIDDLE_TIP,
            MIDDLE_PIP,
            margin,
        ),
        ring=is_finger_open(
            points,
            RING_TIP,
            RING_PIP,
            margin,
        ),
        pinky=is_finger_open(
            points,
            PINKY_TIP,
            PINKY_PIP,
            margin,
        ),
    )

def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))

def map_distance_to_percentage(
    distance: float,
    minimum_distance: float = 0.03,
    maximum_distance: float = 0.30,
) -> float:
    
    if maximum_distance <= minimum_distance:
        raise ValueError(
            "maximum_distance must be greater than minimum_distance"
        )

    normalized = (
        (distance - minimum_distance)
        / (maximum_distance - minimum_distance)
    )

    normalized = clamp(normalized, 0.0, 1.0)

    return normalized * 100.0