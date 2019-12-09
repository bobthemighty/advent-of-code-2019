from asyncio import Queue, gather
import fileinput
from opcodes import Computer
from operator import itemgetter
from itertools import permutations

import pytest

pytestmark = pytest.mark.asyncio

class AmplifierArray:

    def __init__(self, tape):
        self.array = [Computer(tape) for i in range(0, 5)]
        self.tasks = []

    async def run(self, phases):
        next_queue = Queue()
        await next_queue.put(0)

        for computer, phase in zip(self.array, phases):
            self.tasks.append(computer.run(next_queue))
            await next_queue.put(phase)
            next_queue = computer.output
        await gather(*self.tasks)
        return await next_queue.get()


async def test_43210():
    amp = AmplifierArray([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0])
    assert await amp.run([4,3,2,1,0]) == 43210

async def test_54321():
    amp = AmplifierArray([3,23,3,24,1002,24,10,24,1002,23,-1,23,
101,5,23,23,1,24,23,23,4,23,99,0,0])
    assert await amp.run([0,1,2,3,4]) == 54321

async def test_65210():
    amp = AmplifierArray([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
    assert await amp.run([1,0,4,3,2]) == 65210


if __name__ == "__main__":


    [line] = fileinput.input()
    tape = [int(x) for x in line.split(',')]

    amp = AmplifierArray(tape)
    candidates = permutations([0,1,2,3,4])

    print(max(
        ((candidate, amp.run(candidate)) for candidate in candidates),
        key=itemgetter(1)
    ))
