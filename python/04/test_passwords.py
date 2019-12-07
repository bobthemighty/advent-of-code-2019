import pytest

def pairs(password):
    return [
        (password[i], password[i+1])
        for i in range(0, 6, 2)
    ]

def is_valid(password):
    has_pair = False
    for a,b in pairs(password):
        print(a,b)
        if b > a:
            return False
        if a == b:
            has_pair = True
    return has_pair

@pytest.mark.parametrize('password,matches',[
    ('111111', True),
    ('223450', False),
    ('123789', False)
])
def test_examples(password, matches):
    assert is_valid(password) == matches
