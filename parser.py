class Token:
    def __init__(self, type_: str, value: str="") -> None:
        self.type = type_
        self.value = value


class Parser:
    def __init__(self) -> None:
        self.tokens = []
        self.pos = 0

    def tokenize(self, string: str) -> list[Token]:
        tokens = []
        for ch in string:
            if ch in {'(', ')', '|', '*', '+', '?'}:
                tokens.append(Token(ch))
            else:
                tokens.append(Token('CHAR', ch))
        return tokens

    def lookahead(self) -> str | None:
        return self.tokens[self.pos].type if self.pos < len(self.tokens) else None

    def consume(self, expected=None):
        if self.pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of input. Are you missing a bracket?")
        token = self.tokens[self.pos]
        if expected and token.type != expected:
            raise SyntaxError(f"Expected {expected}, got {token.type} instead.")
        self.pos += 1
        return token

    def parse(self, string):
        self.tokens = self.tokenize(string)
        ast = self.parse_expression()
        if self.pos != len(self.tokens):
            raise SyntaxError(f"Unexpected token {self.lookahead()}")
        return ast

    def parse_base(self):
        token = self.lookahead()
        if token == "CHAR":
            return self.consume().value
        elif token == '(':
            self.consume('(')
            expression = self.parse_expression()
            self.consume(')')
            return expression
        else:
            raise SyntaxError(f"Unexpected token {token}")

    def parse_factor(self):
        base = self.parse_base()
        while self.lookahead() in {'*', '+', '?'}:
            operation = self.consume().type
            base = {"type": {"*": "star", "+": "plus", "?": "optional"}[operation],
                    "left": base, "right": 0}
        return base

    def parse_term(self):
        left = self.parse_factor()
        while self.lookahead() in {"CHAR", '('}:
            right = self.parse_factor()
            left = {"type": "concat", "left": left, "right": right}
        return left

    def parse_expression(self):
        left = self.parse_term()
        while self.lookahead() == '|':
            self.consume('|')
            right = self.parse_term()
            left = {"type": "union", "left": left, "right": right}
        return left

