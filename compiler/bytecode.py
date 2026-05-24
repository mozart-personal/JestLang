from enum import Enum, auto

class OpCode(Enum):
    PUSH_CONST = auto()
    LOAD_VAR = auto()
    STORE_VAR = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    CALL = auto()
    RETURN = auto()
    JUMP = auto()
    JUMP_IF_FALSE = auto()
    HALT = auto()

class BytecodeInstruction:
    def __init__(self, opcode, operand=None):
        self.opcode = opcode
        self.operand = operand

    def __repr__(self):
        return f"{self.opcode.name} {self.operand if self.operand is not None else ''}"
