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


@dataclass
class Step:

    direction: Direction
    distance: int

    def vector(self):
        if self.direction == Direction.Up:
            return Point(0, 1)
        if self.direction == Direction.Down:
            return Point(0, -1)
        if self.direction == Direction.Left:
            return Point(-1, 0)
        if self.direction == Direction.Right:
            return Point(1, 0)

    def points_from(self, p: Point):
       v = self.vector()
       return [p + (v * d) for d in range(1, self.distance + 1)] 


class Path(list):

    def __init__(self):
        self.append(Point.origin())

    def apply(self, move: Step):
        points = move.points_from(self.current_pos)
        self += points

    @property
    def current_pos(self):
        return self[-1]


def test_empty_path():
    path = Path()
    assert path == [Point.origin()]


@pytest.mark.parametrize(
    "move, result",
    [
        (Step(Direction.Right, 3), [(0, 0), (1, 0), (2, 0), (3, 0)]),
        (Step(Direction.Left, 2), [(0, 0), (-1, 0), (-2, 0)]),
        (Step(Direction.Up, 1), [(0, 0), (0, 1)]),
        (Step(Direction.Down, 4), [(0, 0), (0, -1), (0, -2), (0, -3), (0, -4)]),
    ],
)
def test_single_move(move, result):
    path = Path()
    path.apply(move)
    assert path == [Point(*p) for p in result]
