"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # the commands
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, file):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [None] * 256

        try:
            with open(file) as f:
                for i, line in enumerate(f):
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == '':
                        continue

                    val = int(num, 2)

                    program[i] = val

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

        for instruction in program:
            if instruction is not None:
                self.ram[address] = instruction
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010  # 130
        PRN = 0b01000111  # 71
        HLT = 0b00000001  # 1
        MUL = 0b10100010  # 162

        running = True

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == MUL:
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
                self.pc += 3
            elif IR == HLT:
                running = False
            else:
                print(f"Invalid command: {IR}")
                quit()
