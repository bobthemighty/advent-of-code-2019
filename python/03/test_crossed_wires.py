from enum import Enum
from dataclasses import dataclass
from typing import List

import pytest


@dataclass(eq=True, frozen=True)
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


VECTORS = {"U": Point(0, 1), "L": Point(-1, 0), "D": Point(0, -1), "R": Point(1, 0)}


def line_segment(origin, direction, distance):
    v = VECTORS[direction]
    return [origin + (v * d) for d in range(1, distance + 1)]


class Path(list):
    def __init__(self, segments=None):
        self.append(Point.origin())
        if segments:
            for seg in segments:
                self.add_segment(seg[0], int(seg[1:]))

    def add_segment(self, direction, distance):
        self += line_segment(self.current_pos, direction, distance)

    @property
    def current_pos(self):
        return self[-1]

    def crosses(self, other):
        a = set(self[1:])
        b = set(other[1:])
        return list(a.intersection(b))


def test_empty_path():
    path = Path()
    assert path == [Point.origin()]


@pytest.mark.parametrize(
    "direction, distance, result",
    [
        ("R", 3, [(0, 0), (1, 0), (2, 0), (3, 0)]),
        ("L", 2, [(0, 0), (-1, 0), (-2, 0)]),
        ("U", 1, [(0, 0), (0, 1)]),
        ("D", 4, [(0, 0), (0, -1), (0, -2), (0, -3), (0, -4)]),
    ],
)
def test_single_move(direction, distance, result):
    path = Path()
    path.add_segment(direction, distance)
    assert path == [Point(*p) for p in result]


def test_multi_moves():
    path = Path()
    path.add_segment("R", 1)
    path.add_segment("U", 1)
    path.add_segment("D", 1)
    path.add_segment("L", 1)

    assert path == [Point(*p) for p in [(0, 0), (1, 0), (1, 1), (1, 0), (0, 0)]]

    assert path == Path(['R1', 'U1', 'D1', 'L1'])


def test_intersections():
    a = Path(['R8','U5','L5','D3'])
    b = Path(['U7','R6','D4','L4'])

    assert a.crosses(b) == [Point(3, 3), Point(6, 5)]
