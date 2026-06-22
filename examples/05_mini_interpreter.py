"""
Мини-интерпретатор арифметических выражений.
Поддерживает: +, -, *, /, ** (степень), унарный минус, скобки, переменные.

Грамматика (рекурсивный спуск):
  expr   = term (('+' | '-') term)*
  term   = factor (('*' | '/') factor)*
  factor = base ('**' factor)?          # правоассоциативное
  base   = NUMBER | IDENT | '(' expr ')' | '-' base
"""


class Token:
    NUM = "NUM"
    OP = "OP"
    IDENT = "IDENT"
    LPAREN = "("
    RPAREN = ")"
    EOF = "EOF"

    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f"Token({self.kind}, {self.value!r})"


class Lexer:
    def __init__(self, text):
        self._tokens = self._tokenize(text)
        self._pos = 0

    def _tokenize(self, text):
        tokens = []
        i = 0
        while i < len(text):
            if text[i] == " ":
                i += 1
                continue
            if text[i:i+2] == "**":
                tokens.append(Token(Token.OP, "**"))
                i += 2
                continue
            ch = text[i]
            if ch.isdigit() or ch == ".":
                j = i
                while j < len(text) and (text[j].isdigit() or text[j] == "."):
                    j += 1
                tokens.append(Token(Token.NUM, float(text[i:j])))
                i = j
                continue
            if ch.isalpha() or ch == "_":
                j = i
                while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                    j += 1
                tokens.append(Token(Token.IDENT, text[i:j]))
                i = j
                continue
            if ch in "+-*/()":
                tokens.append(Token(Token.OP, ch))
                i += 1
                continue
            raise SyntaxError(f"Unknown character: {ch!r}")
        tokens.append(Token(Token.EOF, None))
        return tokens

    def peek(self):
        return self._tokens[self._pos]

    def consume(self):
        tok = self._tokens[self._pos]
        if tok.kind != Token.EOF:
            self._pos += 1
        return tok


class Parser:
    def __init__(self, text, env=None):
        self.lexer = Lexer(text)
        self.env = env or {}

    def parse(self):
        value = self.expr()
        if self.lexer.peek().kind != Token.EOF:
            raise SyntaxError("Unexpected token")
        return value

    def expr(self):
        left = self.term()
        while self.lexer.peek().kind == Token.OP and self.lexer.peek().value in ("+", "-"):
            op = self.lexer.consume().value
            right = self.term()
            left = left + right if op == "+" else left - right
        return left

    def term(self):
        left = self.factor()
        while self.lexer.peek().kind == Token.OP and self.lexer.peek().value in ("*", "/"):
            op = self.lexer.consume().value
            right = self.factor()
            if op == "*":
                left = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                left = left / right
        return left

    def factor(self):
        base = self.base()
        if self.lexer.peek().kind == Token.OP and self.lexer.peek().value == "**":
            self.lexer.consume()
            exp = self.factor()
            return base ** exp
        return base

    def base(self):
        tok = self.lexer.peek()
        if tok.kind == Token.NUM:
            self.lexer.consume()
            return tok.value
        if tok.kind == Token.IDENT:
            self.lexer.consume()
            if tok.value not in self.env:
                raise NameError(f"Undefined variable: {tok.value!r}")
            return self.env[tok.value]
        if tok.kind == Token.OP and tok.value == "(":
            self.lexer.consume()
            value = self.expr()
            if self.lexer.peek().value != ")":
                raise SyntaxError("Expected ')'")
            self.lexer.consume()
            return value
        if tok.kind == Token.OP and tok.value == "-":
            self.lexer.consume()
            return -self.base()
        raise SyntaxError(f"Unexpected token: {tok!r}")


def evaluate(expression, env=None):
    return Parser(expression, env).parse()


def main():
    env = {"x": 5, "y": 3, "pi": 3.141592653589793}

    expressions = [
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "2 ** 10",
        "x * y + 2",
        "pi * x ** 2",
        "-(x + y) * 2",
        "100 / (x - y) ** 2",
    ]

    print("Variables:", env)
    print()
    for expr in expressions:
        result = evaluate(expr, env)
        print(f"  {expr:<25} = {result}")


if __name__ == "__main__":
    main()
