from asyncio import Queue, gather, run
import fileinput
from opcodes import Computer
from operator import itemgetter
from itertools import permutations

import pytest

pytestmark = pytest.mark.asyncio

class AmplifierArray:

    def __init__(self, tape):
        self.array = [Computer(tape) for i in range(0, 5)]

    async def run(self, phases):
        tasks = []
        first_queue = next_queue = self.array[-1].output
        for computer, phase in zip(self.array, phases):
            tasks.append(computer.run(next_queue))
            await next_queue.put(phase)
            next_queue = computer.output
        await first_queue.put(0)
        await gather(*tasks)
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

async def test_139629729():
    amp = AmplifierArray([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5])
    assert await amp.run([9,8,7,6,5]) == 139629729

async def test_18216():
    amp = AmplifierArray([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10])
    assert await amp.run([9,7,8,5,6]) == 18216

async def test_acceptance():
    tape = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    candidates = permutations([5, 6, 7, 8, 9])

    tasks = [AmplifierArray(tape).run(candidate) for candidate in candidates]
    results = await gather(*tasks)

    return max(results)


async def amax(aiterable, key):
    m = 0
    async for elem in aiterable:
        if key(elem) > m:
            m = key(elem)
    return m

async def main (tape) :

    candidates = permutations([5,6,7,8,9])

    tasks = [AmplifierArray(tape).run(candidate) for candidate in candidates]
    results = await gather(*tasks)

    return max(results)


if __name__ == "__main__":
    [line] = fileinput.input()
    tape = [int(x) for x in line.split(',')]
    print(run(main(tape)))
