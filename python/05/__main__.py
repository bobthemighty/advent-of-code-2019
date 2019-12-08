import fileinput
from opcodes import Computer

if __name__ == "__main__":
     [data] = fileinput.input()
     tape = [int(x) for x in data.split(',')]
     prog = Computer(tape, [1])
     prog.run()
     print(prog.output)

