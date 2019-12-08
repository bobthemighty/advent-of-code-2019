ADD = 1
MULT = 2
STOR = 3
OUT = 4
HALT = 99

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


    def _next(self):
        v = self.tape[self.head]
        self.head += 1
        return v

    def _exec(self):
        op = self._next()
        self.funcs[op]()

    def _halt(self):
        raise StopIteration()

    def _store(self):
        v = self._input.pop()
        out = self._next()
        self.tape[out] = v

    def _output(self):
        v = self._deref()
        self.output.append(v)

    def _deref(self):
        p = self._next()
        return self.tape[p]

    def _binop(self, f):
        def _f() :
            a = self._deref()
            b = self._deref()
            out = self._next()
            self.tape[out] = f(a, b)
            self.value = self.tape[out]
        return _f


def run(tape):
    cmp = Computer(tape)

    cmp.run()
    return cmp.value
