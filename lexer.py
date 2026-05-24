import re
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
    
    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()
    EOF = auto()

KEYWORDS = {
    "fn", "if", "else", "for", "while", "return", 
    "use", "break", "continue", "true", "false", "null"
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

    def advance(self):
        char = self.source[self.pos]
        self.pos += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def peek(self, offset=0):
        if self.pos + offset >= len(self.source):
            return None
        return self.source[self.pos + offset]

    def tokenize(self):
        while self.pos < len(self.source):
            char = self.peek()

            if char == " ":
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
                    self.advance(); self.advance()
                    self.tokens.append(Token(TokenType.EE, "==", self.line, self.column-2))
                else:
                    self.advance()
                    self.tokens.append(Token(TokenType.EQUALS, "=", self.line, self.column-1))
                continue

            if char == ">":
                if self.peek(1) == "=":
                    self.advance(); self.advance()
                    self.tokens.append(Token(TokenType.GTE, ">=", self.line, self.column-2))
                else:
                    self.advance()
                    self.tokens.append(Token(TokenType.GT, ">", self.line, self.column-1))
                continue

            if char == "<":
                if self.peek(1) == "=":
                    self.advance(); self.advance()
                    self.tokens.append(Token(TokenType.LTE, "<=", self.line, self.column-2))
                else:
                    self.advance()
                    self.tokens.append(Token(TokenType.LT, "<", self.line, self.column-1))
                continue

            if char == "!":
                if self.peek(1) == "=":
                    self.advance(); self.advance()
                    self.tokens.append(Token(TokenType.NE, "!=", self.line, self.column-2))
                else:
                    self.advance()
                continue

            simple_tokens = {
                "+": TokenType.PLUS, "-": TokenType.MINUS, "*": TokenType.MUL, "/": TokenType.DIV,
                "(": TokenType.LPAREN, ")": TokenType.RPAREN, "{": TokenType.LBRACE, "}": TokenType.RBRACE,
                "[": TokenType.LBRACKET, "]": TokenType.RBRACKET, ":": TokenType.COLON, ",": TokenType.COMMA,
                ".": TokenType.DOT
            }

            if char in simple_tokens:
                self.tokens.append(Token(simple_tokens[char], char, self.line, self.column))
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
        num_str = ""
        dot_count = 0
        while self.peek() and (self.peek().isdigit() or self.peek() == "."):
            if self.peek() == ".":
                dot_count += 1
            num_str += self.advance()
        
        val = float(num_str) if dot_count > 0 else int(num_str)
        return Token(TokenType.NUMBER, val, self.line, self.column - len(num_str))

    def make_string(self):
        self.advance()
        string = ""
        while self.peek() and self.peek() != "\"":
            string += self.advance()
        self.advance()
        return Token(TokenType.STRING, string, self.line, self.column - len(string) - 2)

    def make_identifier(self):
        id_str = ""
        while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
            id_str += self.advance()
        
        type = TokenType.KEYWORD if id_str in KEYWORDS else TokenType.IDENTIFIER
        return Token(type, id_str, self.line, self.column - len(id_str))
