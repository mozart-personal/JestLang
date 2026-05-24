from lexer import Lexer

with open("api.jest", "r") as f:
    source = f.read()

lexer = Lexer(source)

tokens = lexer.tokenize()

for token in tokens:
    print(token.type, token.value)