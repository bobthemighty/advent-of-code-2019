from enum import Enum
from dataclasses import dataclass
from typing import List

class Direction(Enum):
    Up = 'U'
    Down = 'D'
    Left = 'L'
    Right = 'R'


@dataclass
class Move:

    direction: Direction
    distance: int

def points_in_path(moves: List[Move]):
    return [0]

def test_empty_path():
    assert points_in_path([]) == [0]
