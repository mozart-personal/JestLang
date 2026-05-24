import ast_nodes as ast
from runtime.values import JestFunction, NativeFunction, JestObject, JestArray
from runtime.imports import ImportSystem

class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise Exception(f"Undefined variable '{name}'")

    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise Exception(f"Undefined variable '{name}'")

class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.globals.define("print", NativeFunction("print", lambda *args: print(*args)))
        self.import_system = ImportSystem(self)
        self.current_env = self.globals

    def interpret(self, program):
        try:
            results = []
            for stmt in program.body:
                results.append(self.execute(stmt))
            return results[-1] if results else None
        except Exception as e:
            print(f"Runtime Error: {e}")
            raise e

    def execute(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_VarAssign(self, node):
        value = self.execute(node.value)
        try:
            self.current_env.assign(node.name, value)
        except:
            self.current_env.define(node.name, value)
        return value

    def visit_VarAccess(self, node):
        return self.current_env.get(node.name)

    def visit_Literal(self, node):
        return node.value

    def visit_BinaryOp(self, node):
        left = self.execute(node.left)
        right = self.execute(node.right)
        
        ops = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            ">": lambda a, b: a > b,
            ">=": lambda a, b: a >= b,
            "<": lambda a, b: a < b,
            "<=": lambda a, b: a <= b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
        }
        return ops[node.op](left, right)

    def visit_FunctionDecl(self, node):
        func = JestFunction(node.name, node.params, node.body, self.current_env)
        if node.name:
            self.current_env.define(node.name, func)
        return func

    def visit_Call(self, node):
        callee = self.execute(node.callee)
        args = [self.execute(arg) for arg in node.args]
        return self.call_function(callee, args)

    def call_function(self, callee, args):
        if isinstance(callee, NativeFunction):
            return callee.func(*args)
        
        if isinstance(callee, JestFunction):
            env = Environment(callee.closure)
            for i in range(len(callee.params)):
                env.define(callee.params[i], args[i] if i < len(args) else None)
            
            old_env = self.current_env
            self.current_env = env
            try:
                for stmt in callee.body:
                    result = self.execute(stmt)
                    if isinstance(stmt, ast.ReturnStmt):
                        return result
            finally:
                self.current_env = old_env
            return None
        
        raise Exception(f"{callee} is not callable")

    def visit_ReturnStmt(self, node):
        return self.execute(node.value) if node.value else None

    def visit_IfStmt(self, node):
        if self.execute(node.condition):
            for stmt in node.then_branch:
                self.execute(stmt)
        elif node.else_branch:
            for stmt in node.else_branch:
                self.execute(stmt)

    def visit_WhileStmt(self, node):
        while self.execute(node.condition):
            for stmt in node.body:
                self.execute(stmt)

    def visit_ForStmt(self, node):
        iterable = self.execute(node.iterable)
        if isinstance(iterable, (int, float)):
            iterable = range(int(iterable))
        
        for val in iterable:
            self.current_env.define(node.iterator, val)
            for stmt in node.body:
                self.execute(stmt)

    def visit_ImportStmt(self, node):
        module = self.import_system.load(node.module)
        self.current_env.define(node.module, module)

    def visit_ArrayLiteral(self, node):
        return [self.execute(el) for el in node.elements]

    def visit_ObjectLiteral(self, node):
        obj = {}
        for k, v in node.pairs.items():
            obj[k] = self.execute(v)
        return JestObject(obj)

    def visit_MemberAccess(self, node):
        obj = self.execute(node.object)
        if hasattr(obj, "fields"):
            return obj.fields.get(node.member)
        if isinstance(obj, dict):
            return obj.get(node.member)
        raise Exception(f"Cannot access member '{node.member}' of {obj}")
