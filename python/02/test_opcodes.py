ADD = 1
MULT = 2
HALT = 99

def operator(opcode):
    if opcode == ADD:
        return lambda a, b : a + b
    elif opcode == MULT:
        return lambda a, b : a * b
    elif opcode == HALT:
        raise StopIteration()

    raise ValueError('Unrecognised opcode %s' % opcode)

def operands(tape, head):
    # pointers to operands a, b and result
    pA, pB, pR = tape[head+1:head+4]
    a = tape[pA]
    b = tape[pB]
    return a, b, pR

def run(tape):
    head = 0

    while True:
        try:
            op = operator(tape[head])
            a, b, pResult = operands(tape, head)
            tape[pResult] = op(a, b)
            head += 4
        except StopIteration:
            return tape[pResult]


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

if __name__ == "__main__":
    input = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,9,19,23,1,23,5,27,2,27,10,31,1,6,31,35,1,6,35,39,2,9,39,43,1,6,43,47,1,47,5,51,1,51,13,55,1,55,13,59,1,59,5,63,2,63,6,67,1,5,67,71,1,71,13,75,1,10,75,79,2,79,6,83,2,9,83,87,1,5,87,91,1,91,5,95,2,9,95,99,1,6,99,103,1,9,103,107,2,9,107,111,1,111,6,115,2,9,115,119,1,119,6,123,1,123,9,127,2,127,13,131,1,131,9,135,1,10,135,139,2,139,10,143,1,143,5,147,2,147,6,151,1,151,5,155,1,2,155,159,1,6,159,0,99,2,0,14,0]

    input[1] = 12
    input[2] = 2

    print(run(input))


