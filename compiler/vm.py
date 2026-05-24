from compiler.bytecode import OpCode

class VM:
    def __init__(self, instructions, constants):
        self.instructions = instructions
        self.constants = constants
        self.stack = []
        self.ip = 0
        self.globals = {}

    def run(self):
        while self.ip < len(self.instructions):
            instr = self.instructions[self.ip]
            self.ip += 1
            
            if instr.opcode == OpCode.PUSH_CONST:
                self.stack.append(self.constants[instr.operand])
            elif instr.opcode == OpCode.LOAD_VAR:
                self.stack.append(self.globals.get(instr.operand))
            elif instr.opcode == OpCode.STORE_VAR:
                self.globals[instr.operand] = self.stack.pop()
            elif instr.opcode == OpCode.ADD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            elif instr.opcode == OpCode.HALT:
                break
        
        return self.stack[-1] if self.stack else None
