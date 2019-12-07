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

    @property
    def distance(self):
        return abs(self.x) + abs(self.y)

    def __lt__(self, other):
        return self.distance < other.distance


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

    def closest_intersection(self, other):
        a = set(self[1:])
        b = set(other[1:])
        return min(a.intersection(b))


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

    assert a.closest_intersection(b) == Point(3, 3)


@pytest.mark.parametrize("a, b, expected",[
    ('R75,D30,R83,U83,L12,D49,R71,U7,L72',
     'U62,R66,U55,R34,D71,R55,D58,R83',
     159
    ),
    ('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
     'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
     135
    )
])
def test_examples(a, b, expected):
   path_a = Path(a.split(','))
   path_b = Path(b.split(','))

   crossing = path_a.closest_intersection(path_b)
   assert crossing.distance == expected
