import pytest

def read(password, i):
    if i == 0:
        return -1, int(password[0])
    if i == 6:
        return int(password[5]), 11
    return int(password[i - 1]), int(password[i])


def is_valid(password):
    has_pair = False
    repetitions = 1

    for i in range(0, 7):
        a, b = read(password, i)

        if a > b:
            return False
        if a == b:
            repetitions += 1
        else:
            has_pair = has_pair or repetitions == 2
            repetitions = 1

    return has_pair


@pytest.mark.parametrize(
    "password,matches", [("112233", True), ("123444", False), ('111122', True)]
)
def test_examples(password, matches):
    assert is_valid(password) == matches


if __name__ == "__main__":
    print(len([p for p in range(109165, 576724) if is_valid(str(p))]))
