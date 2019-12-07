from enum import Enum
from dataclasses import dataclass
from typing import List

import pytest

from wire import Wire, Point


def test_empty_path():
    path = Wire()
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
    path = Wire()
    path.add_segment(direction, distance)
    assert path == [Point(*p) for p in result]


def test_multi_moves():
    path = Wire()
    path.add_segment("R", 1)
    path.add_segment("U", 1)
    path.add_segment("D", 1)
    path.add_segment("L", 1)

    assert path == [Point(*p) for p in [(0, 0), (1, 0), (1, 1), (1, 0), (0, 0)]]

    assert path == Wire(['R1', 'U1', 'D1', 'L1'])


def test_intersections():
    a = Wire(['R8','U5','L5','D3'])
    b = Wire(['U7','R6','D4','L4'])

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
   path_a = Wire(a.split(','))
   path_b = Wire(b.split(','))

   crossing = path_a.closest_intersection(path_b)
   assert crossing.distance == expected
