from opcodes import run, Computer

def test_one_add_one():
    assert run([1,0,0,0,99]) == 2

def test_three_times_two():
    assert run([2,3,0,3,99]) == 6

def test_ninety_nine_squared():
    assert run([2, 4, 4, 5, 99, 0]) == 9801

def test_two_step_program():
    assert run([
        1, 1, 1, 4,   # set pos 4 to (1 + 1)
        99, 5, 6, 0,  # multiply 5 + 6 into pos 0
        99
    ]) == 30

def test_echo():
    prog = Computer([3,0,4,0,99], [66])
    prog.run()

    assert prog.output == [66]
