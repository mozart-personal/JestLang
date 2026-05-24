import ast_nodes as ast
from compiler.bytecode import OpCode
from compiler.emitter import Emitter

class Compiler:
    def __init__(self):
        self.emitter = Emitter()
        self.constants = []

    def compile(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)
        return self.emitter.get_instructions(), self.constants

    def generic_visit(self, node):
        if hasattr(node, "body") and isinstance(node.body, list):
            for stmt in node.body:
                self.compile(stmt)
        elif isinstance(node, list):
            for stmt in node:
                self.compile(stmt)

    def visit_Program(self, node):
        for stmt in node.body:
            self.compile(stmt)
        self.emitter.emit(OpCode.HALT)

    def visit_Literal(self, node):
        idx = len(self.constants)
        self.constants.append(node.value)
        self.emitter.emit(OpCode.PUSH_CONST, idx)

    def visit_VarAccess(self, node):
        self.emitter.emit(OpCode.LOAD_VAR, node.name)

    def visit_VarAssign(self, node):
        self.compile(node.value)
        self.emitter.emit(OpCode.STORE_VAR, node.name)

    def visit_BinaryOp(self, node):
        self.compile(node.left)
        self.compile(node.right)
        ops = {
            "+": OpCode.ADD, "-": OpCode.SUB, "*": OpCode.MUL, "/": OpCode.DIV
        }
        if node.op in ops:
            self.emitter.emit(ops[node.op])

    def visit_Call(self, node):
        for arg in node.args:
            self.compile(arg)
        self.compile(node.callee)
        self.emitter.emit(OpCode.CALL, len(node.args))

    def visit_ReturnStmt(self, node):
        if node.value:
            self.compile(node.value)
        else:
            idx = len(self.constants)
            self.constants.append(None)
            self.emitter.emit(OpCode.PUSH_CONST, idx)
        self.emitter.emit(OpCode.RETURN)
