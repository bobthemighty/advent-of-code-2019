from collections import namedtuple

F=0
A=1
B=2
C=3

POSITION=0
IMMEDIATE=1

ADD = 1
MULT = 2
STOR = 3
OUT = 4
HALT = 99

operator = namedtuple('_operator', 'code,mode')

class Computer:

    def __init__(self, tape, input=None):
        self._input = input.copy() if input else []
        self.output = []
        self.tape = tape.copy()
        self.head = 0
        self.value = None
        self.funcs = {
            ADD: self._binop(lambda a,b : a + b),
            MULT: self._binop(lambda a, b: a * b),
            HALT: self._halt,
            STOR: self._store,
            OUT: self._output
        }

    def run(self):
        while True:
            try:
                self._exec()
            except StopIteration:
                break

    def _parse_op(self):
        code = self._arg(F)
        op = code % 100
        code -= op

        mode1 = code % 1000
        code -= mode1

        mode2 = code % 10000
        code -= mode2

        mode3 = code % 100000
        code -= mode3

        return operator(op, [
            IMMEDIATE, mode1 and 1 or 0, mode2 and 1 or 0, mode3 and 1 or 0
        ])


    def _arg(self, pos, op=None):
        v = self.tape[self.head + pos]
        if op and op.mode[pos] == POSITION:
            return self.tape[v]
        return v

    def _exec(self):
        op = self._parse_op()
        print(op)
        mv = self.funcs[op.code](op)
        self.head += mv


    def _halt(self, _):
        raise StopIteration()

    def _store(self, _):
        v = self._input.pop()
        out = self._arg(A)
        self.tape[out] = v
        return 2

    def _output(self, op):
        v = self._arg(A, op)
        self.output.append(v)
        return 2

    def _binop(self, f):
        def _f(op) :
            a = self._arg(A, op)
            b = self._arg(B, op)
            out = self._arg(C)
            self.tape[out] = f(a, b)
            self.value = self.tape[out]
            return 4
        return _f


def run(tape):
    cmp = Computer(tape)

    cmp.run()
    return cmp.value
