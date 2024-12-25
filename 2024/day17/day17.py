from itertools import groupby

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

registers, prog = [list(g) for k, g in groupby(lines, key=bool) if k]
registers = [int(x.split(" ")[2]) for x in registers]
prog = [int(x) for x in prog[0].split(" ")[1].split(",")]


class Computer:
    def __init__(self, registers, program):
        self.registers = registers
        self.program = program
        self.pointer = 0
        self.funcs = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def adv(self, operand):
        self.dv(operand, 0)

    def bdv(self, operand):
        self.dv(operand, 1)

    def cdv(self, operand):
        self.dv(operand, 2)

    def dv(self, operand, reg):
        num = self.registers[0]
        combo = self.combo(operand)
        den = pow(2, combo)
        self.registers[reg] = num // den
        self.ptr_next()

    def bxl(self, operand):
        b = self.registers[1]
        self.registers[1] = b ^ operand
        self.ptr_next()

    def bst(self, operand):
        combo = self.combo(operand)
        self.registers[1] = combo % 8
        self.ptr_next()

    def jnz(self, operand):
        if self.registers[0] == 0:
            self.ptr_next()
        else:
            self.pointer = operand

    def bxc(self, operand):
        b = self.registers[1]
        c = self.registers[2]
        self.registers[1] = b ^ c
        self.ptr_next()

    def out(self, operand):
        combo = self.combo(operand)
        self.ptr_next()
        return combo % 8

    def combo(self, operand):
        if 0 <= operand <= 3:
            return operand
        return self.registers[operand - 4]

    def ptr_next(self):
        self.pointer += 2

    def run(self):
        while self.pointer < len(self.program):
            ins = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            o = self.funcs[ins](operand)
            if o is not None:
                yield o


def str_output(output):
    return ",".join([str(x) for x in output])


comp = Computer(registers, prog)
output = comp.run()
print(str_output(output))


def search(prog, output, prev):
    if len(output) == 0:
        return prev
    for a in range(1 << 10):
        comp = Computer([a, 0, 0], prog)
        if next(comp.run()) == output[-1]:
            if a >> 3 == prev & 127:
                r = search(prog, output[:-1], (prev << 3) | (a % 8))
                if r is not None:
                    return r


print(search(prog, prog, 0))
