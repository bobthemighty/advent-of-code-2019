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
class Move:

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


class Position:

    def __init__(self):
        self.current_pos = Point.origin()
        self.history = [self.current_pos]

    def apply(self, move: Move):
        points = move.points_from(self.current_pos)
        self.history += points
        self.current_pos = points[-1]

def test_empty_path():
    pos = Position()
    assert pos.history == [Point.origin()]


@pytest.mark.parametrize(
    "move, result",
    [
        (Move(Direction.Right, 3), [(0, 0), (1, 0), (2, 0), (3, 0)]),
        (Move(Direction.Left, 2), [(0, 0), (-1, 0), (-2, 0)]),
        (Move(Direction.Up, 1), [(0, 0), (0, 1)]),
        (Move(Direction.Down, 4), [(0, 0), (0, -1), (0, -2), (0, -3), (0, -4)]),
    ],
)
def test_single_move(move, result):
    pos = Position()
    pos.apply(move)
    assert pos.history == [Point(*p) for p in result]
