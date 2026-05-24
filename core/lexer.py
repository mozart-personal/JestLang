from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()

    EQUALS = auto()

    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()

    LPAREN = auto()
    RPAREN = auto()

    LBRACE = auto()
    RBRACE = auto()

    LBRACKET = auto()
    RBRACKET = auto()

    COLON = auto()
    COMMA = auto()
    DOT = auto()

    GT = auto()
    LT = auto()
    GTE = auto()
    LTE = auto()
    EE = auto()
    NE = auto()

    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()

    EOF = auto()

KEYWORDS = {
    "fn",
    "if",
    "else",
    "for",
    "while",
    "return",
    "use",
    "break",
    "continue",
    "true",
    "false",
    "null",
    "in",
    "and",
    "or",
    "not"
}

class Token:
    def __init__(self, type, value=None, line=1, column=1):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]

    def peek(self, offset=0):
        if self.pos + offset >= len(self.source):
            return None
        return self.source[self.pos + offset]

    def advance(self):
        char = self.source[self.pos]
        self.pos += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char

    def tokenize(self):
        while self.pos < len(self.source):
            char = self.peek()

            if char in [" ", "\t"]:
                self.advance()
                continue

            if char == "#":
                while self.peek() and self.peek() != "\n":
                    self.advance()
                continue

            if char == "\n":
                self.tokens.append(Token(TokenType.NEWLINE, line=self.line, column=self.column))
                self.advance()
                self.handle_indentation()
                continue

            if char.isdigit():
                self.tokens.append(self.make_number())
                continue

            if char.isalpha() or char == "_":
                self.tokens.append(self.make_identifier())
                continue

            if char == "\"":
                self.tokens.append(self.make_string())
                continue

            if char == "=":
                if self.peek(1) == "=":
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.EE, "==", self.line, self.column))
                else:
                    self.advance()
                    self.tokens.append(Token(TokenType.EQUALS, "="))
                continue

            if char == "!":
                if self.peek(1) == "=":
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.NE, "!="))
                continue

            if char == ">":
                if self.peek(1) == "=":
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.GTE, ">="))
                else:
                    self.advance()
                    self.tokens.append(Token(TokenType.GT, ">"))
                continue

            if char == "<":
                if self.peek(1) == "=":
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(TokenType.LTE, "<="))
                else:
                    self.advance()
                    self.tokens.append(Token(TokenType.LT, "<"))
                continue

            simple = {
                "+": TokenType.PLUS,
                "-": TokenType.MINUS,
                "*": TokenType.MUL,
                "/": TokenType.DIV,
                "%": TokenType.MOD,

                "(": TokenType.LPAREN,
                ")": TokenType.RPAREN,

                "{": TokenType.LBRACE,
                "}": TokenType.RBRACE,

                "[": TokenType.LBRACKET,
                "]": TokenType.RBRACKET,

                ":": TokenType.COLON,
                ",": TokenType.COMMA,
                ".": TokenType.DOT
            }

            if char in simple:
                self.tokens.append(Token(simple[char], char))
                self.advance()
                continue

            self.advance()

        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT))

        self.tokens.append(Token(TokenType.EOF))
        return self.tokens

    def handle_indentation(self):
        count = 0

        while self.peek() == " ":
            count += 1
            self.advance()

        if self.peek() == "\n" or self.peek() is None:
            return

        if count > self.indent_stack[-1]:
            self.indent_stack.append(count)
            self.tokens.append(Token(TokenType.INDENT))

        elif count < self.indent_stack[-1]:
            while count < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.tokens.append(Token(TokenType.DEDENT))

    def make_number(self):
        value = ""
        dot = 0

        while self.peek() and (self.peek().isdigit() or self.peek() == "."):
            if self.peek() == ".":
                dot += 1
            value += self.advance()

        value = float(value) if dot else int(value)

        return Token(TokenType.NUMBER, value)

    def make_string(self):
        self.advance()

        value = ""

        while self.peek() and self.peek() != "\"":
            value += self.advance()

        self.advance()

        return Token(TokenType.STRING, value)

    def make_identifier(self):
        value = ""

        while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
            value += self.advance()

        token_type = TokenType.KEYWORD if value in KEYWORDS else TokenType.IDENTIFIER

        return Token(token_type, value)