from enum import Enum
from dataclasses import dataclass
from typing import List

import pytest


@dataclass
class Point:
    x: int
    y: int

    @classmethod
    def origin(cls):
        return Point(0, 0)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, num: int):
        return Point(self.x * num, self.y * num)

class Direction(Enum):
    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"

VECTORS = {
    Direction.Up: Point(0, 1),
    Direction.Left: Point(-1, 0),
    Direction.Down: Point(0, -1),
    Direction.Right: Point(1, 0)
}


def line_segment(origin, direction, distance):
    v = VECTORS[direction]
    return [
        origin + (v * d) for d in range(1, distance + 1)
    ]


class Path(list):

    def __init__(self):
        self.append(Point.origin())

    def add_segment(self, direction, distance):
        self += line_segment(self.current_pos, direction, distance)

    @property
    def current_pos(self):
        return self[-1]


def test_empty_path():
    path = Path()
    assert path == [Point.origin()]


@pytest.mark.parametrize(
    "direction, distance, result",
    [
        (Direction.Right, 3, [(0, 0), (1, 0), (2, 0), (3, 0)]),
        (Direction.Left, 2, [(0, 0), (-1, 0), (-2, 0)]),
        (Direction.Up, 1, [(0, 0), (0, 1)]),
        (Direction.Down, 4, [(0, 0), (0, -1), (0, -2), (0, -3), (0, -4)]),
    ],
)
def test_single_move(direction, distance, result):
    path = Path()
    path.add_segment(direction, distance)
    assert path == [Point(*p) for p in result]
