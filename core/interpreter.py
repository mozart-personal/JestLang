import ast_nodes as ast

from runtime.values import (
    JestFunction,
    NativeFunction,
    JestObject,
    JestArray
)

from runtime.imports import ImportSystem

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class BreakSignal(Exception):
    pass

class ContinueSignal(Exception):
    pass

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
            return value

        if self.parent:
            return self.parent.assign(name, value)

        raise Exception(f"Undefined variable '{name}'")

class Interpreter:
    def __init__(self):
        self.globals = Environment()

        self.import_system = ImportSystem(self)

        self.current_env = self.globals

        self.setup_builtins()

    def setup_builtins(self):
        self.globals.define(
            "print",
            NativeFunction(
                "print",
                lambda *args: print(*args)
            )
        )

        self.globals.define(
            "len",
            NativeFunction(
                "len",
                lambda value: len(value)
            )
        )

        self.globals.define(
            "type",
            NativeFunction(
                "type",
                lambda value: type(value).__name__
            )
        )

    def interpret(self, program):
        result = None

        for stmt in program.body:
            result = self.execute(stmt)

        return result

    def execute(self, node):
        method_name = f"visit_{type(node).__name__}"

        visitor = getattr(
            self,
            method_name,
            self.generic_visit
        )

        return visitor(node)

    def generic_visit(self, node):
        raise Exception(
            f"No visit method for {type(node).__name__}"
        )

    def is_truthy(self, value):
        return bool(value)

    def execute_block(self, statements, env):
        previous = self.current_env

        self.current_env = env

        try:
            result = None

            for stmt in statements:
                result = self.execute(stmt)

            return result

        finally:
            self.current_env = previous

    def visit_Literal(self, node):
        return node.value

    def visit_VarAccess(self, node):
        return self.current_env.get(node.name)

    def visit_VarAssign(self, node):
        value = self.execute(node.value)

        try:
            self.current_env.assign(
                node.name,
                value
            )

        except:
            self.current_env.define(
                node.name,
                value
            )

        return value

    def visit_BinaryOp(self, node):
        left = self.execute(node.left)
        right = self.execute(node.right)

        operations = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "%": lambda a, b: a % b,

            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,

            "and": lambda a, b: a and b,
            "or": lambda a, b: a or b
        }

        if node.op not in operations:
            raise Exception(
                f"Unknown operator '{node.op}'"
            )

        return operations[node.op](left, right)

    def visit_UnaryOp(self, node):
        right = self.execute(node.right)

        operations = {
            "-": lambda value: -value,
            "not": lambda value: not value
        }

        if node.op not in operations:
            raise Exception(
                f"Unknown unary operator '{node.op}'"
            )

        return operations[node.op](right)

    def visit_FunctionDecl(self, node):
        function = JestFunction(
            node.name,
            node.params,
            node.body,
            self.current_env
        )

        if node.name:
            self.current_env.define(
                node.name,
                function
            )

        return function

    def visit_Call(self, node):
        callee = self.execute(node.callee)

        args = []

        for arg in node.args:
            args.append(
                self.execute(arg)
            )

        return self.call_function(
            callee,
            args
        )

    def call_function(self, callee, args):
        if isinstance(callee, NativeFunction):
            return callee.func(*args)

        if isinstance(callee, JestFunction):
            env = Environment(
                callee.closure
            )

            for index, param in enumerate(callee.params):
                value = args[index] if index < len(args) else None

                env.define(
                    param,
                    value
                )

            try:
                self.execute_block(
                    callee.body,
                    env
                )

            except ReturnSignal as signal:
                return signal.value

            return None

        raise Exception(
            f"{callee} is not callable"
        )

    def visit_ReturnStmt(self, node):
        value = None

        if node.value:
            value = self.execute(node.value)

        raise ReturnSignal(value)

    def visit_IfStmt(self, node):
        condition = self.execute(
            node.condition
        )

        if self.is_truthy(condition):
            return self.execute_block(
                node.then_branch,
                Environment(self.current_env)
            )

        if node.else_branch:
            return self.execute_block(
                node.else_branch,
                Environment(self.current_env)
            )

    def visit_WhileStmt(self, node):
        while self.is_truthy(
            self.execute(node.condition)
        ):
            try:
                self.execute_block(
                    node.body,
                    Environment(self.current_env)
                )

            except BreakSignal:
                break

            except ContinueSignal:
                continue

    def visit_ForStmt(self, node):
        iterable = self.execute(
            node.iterable
        )

        if isinstance(iterable, int):
            iterable = range(iterable)

        for value in iterable:
            env = Environment(
                self.current_env
            )

            env.define(
                node.iterator,
                value
            )

            try:
                self.execute_block(
                    node.body,
                    env
                )

            except BreakSignal:
                break

            except ContinueSignal:
                continue

    def visit_ImportStmt(self, node):
        module = self.import_system.load(
            node.module
        )

        self.current_env.define(
            node.module,
            module
        )

        return module

    def visit_ArrayLiteral(self, node):
        values = []

        for element in node.elements:
            values.append(
                self.execute(element)
            )

        return JestArray(values)

    def visit_ObjectLiteral(self, node):
        values = {}

        for key, value in node.pairs.items():
            values[key] = self.execute(value)

        return JestObject(values)

    def visit_MemberAccess(self, node):
        obj = self.execute(node.object)

        if hasattr(obj, "fields"):
            return obj.fields.get(node.member)

        if isinstance(obj, dict):
            return obj.get(node.member)

        raise Exception(
            f"Cannot access member '{node.member}'"
        )

    def visit_IndexAccess(self, node):
        obj = self.execute(node.object)

        index = self.execute(node.index)

        try:
            return obj[index]

        except:
            raise Exception(
                f"Invalid index access"
            )

    def visit_BreakStmt(self, node):
        raise BreakSignal()

    def visit_ContinueStmt(self, node):
        raise ContinueSignal()