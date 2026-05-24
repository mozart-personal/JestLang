from lexer import TokenType
import ast_nodes as ast

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset=0):
        if self.pos + offset >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos + offset]

    def advance(self):
        token = self.peek()
        self.pos += 1
        return token

    def check(self, type):
        return self.peek().type == type

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise Exception(f"Parser Error: {message} at line {self.peek().line}")

    def parse(self):
        statements = []
        while self.match(TokenType.NEWLINE): pass
        while not self.check(TokenType.EOF):
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
            while self.match(TokenType.NEWLINE):
                pass
        return ast.Program(statements)

    def declaration(self):
        if self.match(TokenType.KEYWORD):
            kw = self.tokens[self.pos - 1].value
            if kw == "fn": return self.function_decl()
            if kw == "use": return self.import_stmt()
            if kw == "if": return self.if_stmt()
            if kw == "while": return self.while_stmt()
            if kw == "for": return self.for_stmt()
            if kw == "return": return self.return_stmt()
            self.pos -= 1
        return self.statement()

    def function_decl(self):
        name = None
        if self.check(TokenType.IDENTIFIER):
            name = self.advance().value
        
        self.consume(TokenType.LPAREN, "Expect '(' after fn")
        params = []
        if not self.check(TokenType.RPAREN):
            while True:
                params.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name").value)
                if not self.match(TokenType.COMMA): break
        self.consume(TokenType.RPAREN, "Expect ')' after parameters")
        body = self.block()
        return ast.FunctionDecl(name, params, body)

    def import_stmt(self):
        module = self.consume(TokenType.IDENTIFIER, "Expect module name after use").value
        return ast.ImportStmt(module)

    def if_stmt(self):
        condition = self.expression()
        then_branch = self.block()
        else_branch = None
        if self.match(TokenType.KEYWORD) and self.tokens[self.pos-1].value == "else":
            else_branch = self.block()
        return ast.IfStmt(condition, then_branch, else_branch)

    def while_stmt(self):
        condition = self.expression()
        body = self.block()
        return ast.WhileStmt(condition, body)

    def for_stmt(self):
        iterator = self.consume(TokenType.IDENTIFIER, "Expect iterator name").value
        token = self.advance()
        if token.value != "in":
            raise Exception(f"Parser Error: Expect 'in' in for loop at line {token.line}")
        iterable = self.expression()
        body = self.block()
        return ast.ForStmt(iterator, iterable, body)

    def return_stmt(self):
        value = None
        if not self.check(TokenType.NEWLINE) and not self.check(TokenType.DEDENT) and not self.check(TokenType.EOF):
            value = self.expression()
        return ast.ReturnStmt(value)

    def block(self):
        self.match(TokenType.COLON)
        while self.match(TokenType.NEWLINE): pass
        self.consume(TokenType.INDENT, "Expect indentation for block")
        statements = []
        while not self.check(TokenType.DEDENT) and not self.check(TokenType.EOF):
            stmt = self.declaration()
            if stmt: statements.append(stmt)
            while self.match(TokenType.NEWLINE): pass
        self.consume(TokenType.DEDENT, "Expect dedent after block")
        return statements

    def statement(self):
        expr = self.expression()
        if isinstance(expr, ast.VarAccess) and self.match(TokenType.EQUALS):
            value = self.expression()
            return ast.VarAssign(expr.name, value)
        return expr

    def expression(self):
        return self.comparison()

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GT, TokenType.GTE, TokenType.LT, TokenType.LTE, TokenType.EE, TokenType.NE):
            op = self.tokens[self.pos-1]
            right = self.term()
            expr = ast.BinaryOp(expr, op.value, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.tokens[self.pos-1]
            right = self.factor()
            expr = ast.BinaryOp(expr, op.value, right)
        return expr

    def factor(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LPAREN):
                args = []
                if not self.check(TokenType.RPAREN):
                    while True:
                        args.append(self.expression())
                        if not self.match(TokenType.COMMA): break
                self.consume(TokenType.RPAREN, "Expect ')' after arguments")
                expr = ast.Call(expr, args)
            elif self.match(TokenType.DOT):
                member = self.consume(TokenType.IDENTIFIER, "Expect member name after '.'").value
                expr = ast.MemberAccess(expr, member)
            else:
                break
        return expr

    def primary(self):
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return ast.Literal(self.tokens[self.pos-1].value)
        if self.match(TokenType.KEYWORD):
            val = self.tokens[self.pos-1].value
            if val == "true": return ast.Literal(True)
            if val == "false": return ast.Literal(False)
            if val == "null": return ast.Literal(None)
            if val == "fn": return self.function_decl()
        if self.match(TokenType.IDENTIFIER):
            return ast.VarAccess(self.tokens[self.pos-1].value)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression")
            return expr
        if self.match(TokenType.LBRACKET):
            elements = []
            if not self.check(TokenType.RBRACKET):
                while True:
                    elements.append(self.expression())
                    if not self.match(TokenType.COMMA): break
            self.consume(TokenType.RBRACKET, "Expect ']' after array")
            return ast.ArrayLiteral(elements)
        if self.match(TokenType.LBRACE):
            pairs = {}
            while self.match(TokenType.NEWLINE, TokenType.INDENT): pass
            if not self.check(TokenType.RBRACE):
                while True:
                    while self.match(TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT): pass
                    if self.check(TokenType.RBRACE): break
                    key = self.consume(TokenType.IDENTIFIER, "Expect key").value
                    self.consume(TokenType.COLON, "Expect ':' after key")
                    value = self.expression()
                    pairs[key] = value
                    self.match(TokenType.COMMA)
                    while self.match(TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT): pass
                    if self.check(TokenType.RBRACE): break
            self.consume(TokenType.RBRACE, "Expect '}' after object")
            return ast.ObjectLiteral(pairs)
        
        raise Exception(f"Unexpected token {self.peek()} at line {self.peek().line}")
