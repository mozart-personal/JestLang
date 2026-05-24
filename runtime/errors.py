class JestError(Exception):
    def __init__(self, message, line=None):
        self.message = message
        self.line = line
        super().__init__(self.message)

    def __str__(self):
        prefix = f"Error at line {self.line}: " if self.line else "Error: "
        return f"{prefix}{self.message}"

class RuntimeError(JestError):
    pass

class SyntaxError(JestError):
    pass
