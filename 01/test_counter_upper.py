import pytest
import fileinput
from math import floor

def required(mass):
    return floor(mass /3) - 2

def _total_required(m):
    while (m := required(m)) > 0:
        yield m

def total_required(mass):
    return sum(_total_required(mass))

def counter_upper(masses):
    return sum(total_required(m) for m in masses)

@pytest.mark.parametrize("val,expected", [(12, 2), (14, 2), (1969, 966), (100756, 50346)])
def test_counter_upper(val, expected):
    assert total_required(val) == expected


def read_file():
    print(
        counter_upper(int(v) for v in fileinput.input())
    )

if __name__ == "__main__":
    read_file()
