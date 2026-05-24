class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, body):
        self.body = body

class VarAssign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class VarAccess(ASTNode):
    def __init__(self, name):
        self.name = name

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op, right):
        self.op = op
        self.right = right

class FunctionDecl(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Call(ASTNode):
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

class IfStmt(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStmt(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForStmt(ASTNode):
    def __init__(self, iterator, iterable, body):
        self.iterator = iterator
        self.iterable = iterable
        self.body = body

class ReturnStmt(ASTNode):
    def __init__(self, value):
        self.value = value

class ImportStmt(ASTNode):
    def __init__(self, module):
        self.module = module

class ArrayLiteral(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class ObjectLiteral(ASTNode):
    def __init__(self, pairs):
        self.pairs = pairs

class MemberAccess(ASTNode):
    def __init__(self, object, member):
        self.object = object
        self.member = member
