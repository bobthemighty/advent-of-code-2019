from asyncio import Queue
from collections import namedtuple

POSITION=0
IMMEDIATE=1

ADD = 1
MULT = 2
STOR = 3
OUT = 4
JIT = 5
JIF = 6
LT = 7
EQ = 8
HALT = 99

operator = namedtuple('_operator', 'opcode,a,b,c')

class Computer:

    def __init__(self, program):
        self.output = Queue()
        self.program = program.copy()
        self.funcs = {
            ADD: self._binop(lambda a,b : a + b),
            MULT: self._binop(lambda a, b: a * b),
            HALT: self._halt,
            STOR: self._store,
            OUT: self._output,
            JIT: self._jmp(True),
            JIF: self._jmp(False),
            EQ: self._binop(lambda a, b: 1 if a == b else 0),
            LT: self._binop(lambda a, b: 1 if a < b else 0)
        }

    def _reset(self):
        self.tape = self.program.copy()
        self.head = 0
        self.value = None

    async def run(self, input=None):
        self._reset()
        self._input = input or Queue()
        while True:
            try:
                op  = self._parse_op()
                await self.funcs[op.opcode](op)
            except StopIteration:
                break

    def _parse_op(self):
        code = self._next()
        op = code % 100
        code -= op

        mode1 = code % 1000
        code -= mode1

        mode2 = code % 10000
        code -= mode2

        mode3 = code % 100000
        code -= mode3

        return operator(op, mode1 and 1 or 0, mode2 and 1 or 0, mode3 and 1 or 0)


    def _next(self, mode=IMMEDIATE):
        v = self.tape[self.head]
        self.head += 1
        if mode == POSITION:
            return self.tape[v]
        return v

    def _halt(self, _):
        raise StopIteration()

    async def _store(self, _):
        print(f'{self}: waiting for input')
        v = await self._input.get()
        print(f'{self}: received input {v}')
        out = self._next()
        self.tape[out] = v

    async def _output(self, op):
        v = self._next(op.a)
        print(f'{self}: sending value {v}')
        await self.output.put(v)

    def _jmp(self, v):
        async def f(op):
            a = self._next(op.a)
            b = self._next(op.b)
            if bool(a) == v:
                self.head = b
        return f

    def _binop(self, f):
        async def _f(op) :
            a = self._next(op.a)
            b = self._next(op.b)
            out = self._next()
            self.tape[out] = f(a, b)
            self.value = self.tape[out]
        return _f


async def run(tape):
    cmp = Computer(tape)

    await cmp.run()
    return cmp.value
