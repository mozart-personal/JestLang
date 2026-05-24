import sys
import os
from lexer import Lexer
from jest_parser import Parser
from interpreter import Interpreter

class CLI:
    def __init__(self):
        self.interpreter = Interpreter()

    def run_file(self, path):
        if not os.path.exists(path):
            print(f"Error: File '{path}' not found.")
            return

        with open(path, "r") as f:
            source = f.read()

        try:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            parser = Parser(tokens)
            ast = parser.parse()
            
            self.interpreter.interpret(ast)
        except Exception as e:
            print(f"Jestlang Error: {e}")

    def main(self):
        if len(sys.argv) < 2:
            print("Usage: jest <file.jest>")
            return

        command = sys.argv[1]
        
        if command.endswith(".jest"):

            self.run_file(command)

        else:

            print(f"Unknown command or file type: {command}")

if __name__ == "__main__":
    cli = CLI()
    cli.main()
