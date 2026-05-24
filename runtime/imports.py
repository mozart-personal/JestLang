import os
import importlib.util

class ImportSystem:
    def __init__(self, interpreter):
        self.interpreter = interpreter

        self.loaded_modules = {}

    def load(self, module_name):
        if module_name in self.loaded_modules:
            return self.loaded_modules[module_name]

        builtin = self.load_builtin(module_name)

        if builtin:
            self.loaded_modules[module_name] = builtin
            return builtin

        local = self.load_local(module_name)

        if local:
            self.loaded_modules[module_name] = local
            return local

        raise Exception(
            f"Module '{module_name}' not found"
        )

    def load_builtin(self, module_name):
        if module_name == "web":
            from runtime.web import WebModule

            return WebModule(
                self.interpreter
            )

        return None

    def load_local(self, module_name):
        filename = f"{module_name}.jest"

        if not os.path.exists(filename):
            return None

        with open(filename, "r") as file:
            source = file.read()

        from lexer import Lexer
        from jest_parser import Parser

        lexer = Lexer(source)

        tokens = lexer.tokenize()

        parser = Parser(tokens)

        program = parser.parse()

        self.interpreter.interpret(program)

        return self.interpreter.current_env

    def clear_cache(self):
        self.loaded_modules.clear()