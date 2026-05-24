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

    def check(self, token_type):
        return self.peek().type == token_type

    def match(self, *types):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        raise Exception(
            f"{message} at line {self.peek().line}"
        )

    def parse(self):
        statements = []

        while self.match(TokenType.NEWLINE):
            pass

        while not self.check(TokenType.EOF):
            stmt = self.declaration()

            if stmt:
                statements.append(stmt)

            while self.match(TokenType.NEWLINE):
                pass

        return ast.Program(statements)

    def declaration(self):
        if self.check(TokenType.KEYWORD):

            keyword = self.peek().value

            if keyword == "fn":
                self.advance()
                return self.function_decl()

            if keyword == "if":
                self.advance()
                return self.if_stmt()

            if keyword == "while":
                self.advance()
                return self.while_stmt()

            if keyword == "for":
                self.advance()
                return self.for_stmt()

            if keyword == "return":
                self.advance()
                return self.return_stmt()

            if keyword == "use":
                self.advance()
                return self.import_stmt()

        return self.statement()

    def function_decl(self):
        name = self.consume(
            TokenType.IDENTIFIER,
            "Expected function name"
        ).value

        self.consume(
            TokenType.LPAREN,
            "Expected '('"
        )

        params = []

        if not self.check(TokenType.RPAREN):
            while True:
                params.append(
                    self.consume(
                        TokenType.IDENTIFIER,
                        "Expected parameter name"
                    ).value
                )

                if not self.match(TokenType.COMMA):
                    break

        self.consume(
            TokenType.RPAREN,
            "Expected ')'"
        )

        body = self.block()

        return ast.FunctionDecl(
            name,
            params,
            body
        )

    def if_stmt(self):
        condition = self.expression()

        then_branch = self.block()

        else_branch = None

        if (
            self.check(TokenType.KEYWORD)
            and self.peek().value == "else"
        ):
            self.advance()
            else_branch = self.block()

        return ast.IfStmt(
            condition,
            then_branch,
            else_branch
        )

    def while_stmt(self):
        condition = self.expression()

        body = self.block()

        return ast.WhileStmt(
            condition,
            body
        )

    def for_stmt(self):
        iterator = self.consume(
            TokenType.IDENTIFIER,
            "Expected iterator"
        ).value

        keyword = self.consume(
            TokenType.KEYWORD,
            "Expected 'in'"
        )

        if keyword.value != "in":
            raise Exception(
                f"Expected 'in' at line {keyword.line}"
            )

        iterable = self.expression()

        body = self.block()

        return ast.ForStmt(
            iterator,
            iterable,
            body
        )

    def return_stmt(self):
        value = None

        if (
            not self.check(TokenType.NEWLINE)
            and not self.check(TokenType.DEDENT)
            and not self.check(TokenType.EOF)
        ):
            value = self.expression()

        return ast.ReturnStmt(value)

    def import_stmt(self):
        module = self.consume(
            TokenType.IDENTIFIER,
            "Expected module name"
        ).value

        return ast.ImportStmt(module)

    def block(self):
        self.match(TokenType.COLON)

        while self.match(TokenType.NEWLINE):
            pass

        self.consume(
            TokenType.INDENT,
            "Expected indentation"
        )

        statements = []

        while (
            not self.check(TokenType.DEDENT)
            and not self.check(TokenType.EOF)
        ):
            stmt = self.declaration()

            if stmt:
                statements.append(stmt)

            while self.match(TokenType.NEWLINE):
                pass

        self.consume(
            TokenType.DEDENT,
            "Expected dedent"
        )

        return statements

    def statement(self):
        expr = self.expression()

        if (
            isinstance(expr, ast.VarAccess)
            and self.match(TokenType.EQUALS)
        ):
            value = self.expression()

            return ast.VarAssign(
                expr.name,
                value
            )

        return expr

    def expression(self):
        return self.comparison()

    def comparison(self):
        expr = self.term()

        while self.match(
            TokenType.GT,
            TokenType.GTE,
            TokenType.LT,
            TokenType.LTE,
            TokenType.EE,
            TokenType.NE
        ):
            operator = self.tokens[self.pos - 1]

            right = self.term()

            expr = ast.BinaryOp(
                expr,
                operator.value,
                right
            )

        return expr

    def term(self):
        expr = self.factor()

        while self.match(
            TokenType.PLUS,
            TokenType.MINUS
        ):
            operator = self.tokens[self.pos - 1]

            right = self.factor()

            expr = ast.BinaryOp(
                expr,
                operator.value,
                right
            )

        return expr

    def factor(self):
        expr = self.call()

        while self.match(
            TokenType.MUL,
            TokenType.DIV,
            TokenType.MOD
        ):
            operator = self.tokens[self.pos - 1]

            right = self.call()

            expr = ast.BinaryOp(
                expr,
                operator.value,
                right
            )

        return expr

    def call(self):
        expr = self.primary()

        while True:

            if self.match(TokenType.LPAREN):

                args = []

                if not self.check(TokenType.RPAREN):
                    while True:
                        args.append(
                            self.expression()
                        )

                        if not self.match(TokenType.COMMA):
                            break

                self.consume(
                    TokenType.RPAREN,
                    "Expected ')'"
                )

                expr = ast.Call(
                    expr,
                    args
                )

            elif self.match(TokenType.DOT):

                member = self.consume(
                    TokenType.IDENTIFIER,
                    "Expected property name"
                ).value

                expr = ast.MemberAccess(
                    expr,
                    member
                )

            else:
                break

        return expr

    def primary(self):

        if self.match(TokenType.NUMBER):
            return ast.Literal(
                self.tokens[self.pos - 1].value
            )

        if self.match(TokenType.STRING):
            return ast.Literal(
                self.tokens[self.pos - 1].value
            )

        if self.match(TokenType.IDENTIFIER):
            return ast.VarAccess(
                self.tokens[self.pos - 1].value
            )

        if self.match(TokenType.KEYWORD):

            keyword = self.tokens[self.pos - 1].value

            if keyword == "true":
                return ast.Literal(True)

            if keyword == "false":
                return ast.Literal(False)

            if keyword == "null":
                return ast.Literal(None)

        if self.match(TokenType.LPAREN):

            expr = self.expression()

            self.consume(
                TokenType.RPAREN,
                "Expected ')'"
            )

            return expr

        if self.match(TokenType.LBRACKET):

            elements = []

            if not self.check(TokenType.RBRACKET):

                while True:

                    elements.append(
                        self.expression()
                    )

                    if not self.match(TokenType.COMMA):
                        break

            self.consume(
                TokenType.RBRACKET,
                "Expected ']'"
            )

            return ast.ArrayLiteral(elements)

        if self.match(TokenType.LBRACE):

            pairs = {}

            while self.match(
                TokenType.NEWLINE,
                TokenType.INDENT,
                TokenType.DEDENT
            ):
                pass

            while not self.check(TokenType.RBRACE):

                key_token = self.advance()

                if key_token.type not in [
                    TokenType.IDENTIFIER,
                    TokenType.STRING
                ]:
                    raise Exception(
                        f"Expected object key at line {key_token.line}"
                    )

                key = key_token.value

                self.consume(
                    TokenType.COLON,
                    "Expected ':' after object key"
                )

                value = self.expression()

                pairs[key] = value

                if self.match(TokenType.COMMA):
                    pass

                while self.match(
                    TokenType.NEWLINE,
                    TokenType.INDENT,
                    TokenType.DEDENT
                ):
                    pass

            self.consume(
                TokenType.RBRACE,
                "Expected '}' after object"
            )

            return ast.ObjectLiteral(pairs)
        
        raise Exception(
            f"Unexpected token {self.peek()} at line {self.peek().line}"
        )