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
