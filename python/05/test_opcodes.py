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
    prog = Computer([3,0,4,0,99])
    prog.run([66])

    assert prog.output == [66]

def test_immediate_multiply():
    prog = Computer([1002,4,3,4,33])
    prog.run()

    assert prog.value == 99

def test_is_equal_to_eight():
    prog = Computer([3,9,8,9,10,9,4,9,99,-1,8])

    prog.run([8])
    prog.run([9])
    assert prog.output == [1, 0]


def test_less_than_eight():
    tape = [3,9,7,9,10,9,4,9,99,-1,8]

    prog = Computer(tape)

    prog.run([7])
    prog.run([8])
    prog.run([9])

    assert prog.output == [1, 0, 0]

def test_is_non_zero_positional():
    prog = Computer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
    prog.run([0])
    prog.run([1])
    prog.run([0])

    assert prog.output == [0, 1, 0]


def test_is_non_zero_immediate():
    prog = Computer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
    prog.run([0])
    prog.run([1])
    prog.run([0])

    assert prog.output == [0, 1, 0]

def test_cmp_to_8():
    prog = Computer([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])

    prog.run([7])
    prog.run([8])
    prog.run([9])

    assert prog.output == [999, 1000, 1001]
