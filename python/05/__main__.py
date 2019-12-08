import fileinput
from opcodes import Computer

if __name__ == "__main__":
     [data] = fileinput.input()
     tape = [int(x) for x in data.split(',')]
     prog = Computer(tape)
     prog.run([1])
     prog.run([5])
     print(prog.output)

