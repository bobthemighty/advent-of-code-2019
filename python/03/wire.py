from dataclasses import dataclass
from typing import List


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


class Wire(list):
    def __init__(self, segments=None):
        self.append(Point.origin())
        if segments:
            for seg in segments:
                self.add_segment(seg[0], int(seg[1:]))

    def add_segment(self, direction, distance):
        self += line_segment(self.endpoint, direction, distance)

    @property
    def endpoint(self):
        return self[-1]

    def closest_intersection(self, other):
        a = set(self[1:])
        b = set(other[1:])
        return min(a.intersection(b))


