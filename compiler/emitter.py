from compiler.bytecode import OpCode, BytecodeInstruction

class Emitter:
    def __init__(self):
        self.instructions = []

    def emit(self, opcode, operand=None):
        instr = BytecodeInstruction(opcode, operand)
        self.instructions.append(instr)
        return len(self.instructions) - 1

    def patch(self, index, operand):
        self.instructions[index].operand = operand

    def get_instructions(self):
        return self.instructions
