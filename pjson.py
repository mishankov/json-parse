"""
[x] Token should have information about its position
[ ] Lexer errors with positions
[ ] Parsing validation
    [ ] Do not ignore commas and colons
"""


from enum import Enum


class TokenType(Enum):
    LEFT_CURLY_BRACE = "LEFT_CURLY_BRACE"
    RIGHT_CURLY_BRACE = "RIGHT_CURLY_BRACE"
    LEFT_SQUARE_BRACE = "LEFT_SQUARE_BRACE"
    RIGHT_SQUARE_BRACE = "RIGHT_SQUARE_BRACE"
    COLON = "COLON"
    COMMA = "COMMA"
    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"


class Position:
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

    def copy(self):
        return Position(self.line, self.column)

    def __eq__(self, other: object) -> bool:
        return self.line == other.line and self.column == other.column

    def __repr__(self) -> str:
        return f"{self.line}:{self.column}"


class Token:
    def __init__(self, type_: TokenType, start_position: Position, end_position: Position = None, value=None) -> None:
        self.type = type_
        self.value = value
        self.start_position = start_position.copy()
        self.end_position = end_position.copy() if end_position else start_position.copy()

    def __repr__(self) -> str:
        match (self.value, self.start_position == self.end_position):
            case (None, True):
                return f"{self.type.name}@{self.start_position}"
            case (None, False):
                return f"{self.type.name}@{self.start_position}->{self.end_position}"
            case (_, False):
                return f"{self.type.name}@{self.start_position}->{self.end_position}={self.value}"
            case _:
                raise TypeError(
                    f"Token __repr__ not implemented for {(self.value, self.start_position == self.end_position)}")


class Lexer:
    def __init__(self, text: str) -> None:
        self.lines = text.split("\n")
        self.position = Position(-1, -1)
        self.current_char = None

        self.advance()

    def advance(self):
        if self.position.line == -1 and self.position.column == -1:
            self.position = Position(0, 0)
        elif self.position.column + 1 < len(self.lines[self.position.line]):
            self.position.column += 1
        elif self.position.line + 1 < len(self.lines):
            self.position.line += 1
            self.position.column = 0
        else:
            self.position = None

        self.current_char = self.lines[self.position.line][self.position.column] if self.position else None

    def retreat(self):
        if self.position.column > 0:
            self.position.column -= 1
        else:
            self.position.line -= 1
            self.position.column = len(self.lines[self.position.line]) - 1

        self.current_char = self.lines[self.position.line][self.position.column]

    def tokens(self):
        tokens: list[Token] = []

        while self.current_char != None:
            if self.current_char in ("\n", "\t", " "):
                pass

            elif self.current_char == "{":
                tokens.append(Token(TokenType.LEFT_CURLY_BRACE, self.position))
            elif self.current_char == "}":
                tokens.append(
                    Token(TokenType.RIGHT_CURLY_BRACE, self.position))

            elif self.current_char == "[":
                tokens.append(
                    Token(TokenType.LEFT_SQUARE_BRACE, self.position))
            elif self.current_char == "]":
                tokens.append(
                    Token(TokenType.RIGHT_SQUARE_BRACE, self.position))

            elif self.current_char == ":":
                tokens.append(
                    Token(TokenType.COLON, self.position))
            elif self.current_char == ",":
                tokens.append(
                    Token(TokenType.COMMA, self.position))

            elif self.current_char == "\"":
                tokens.append(self.make_string())

            elif self.current_char in "0123456789.":
                tokens.append(self.make_number())

            elif self.current_char in "ft":
                tokens.append(self.make_boolean())

            else:
                raise NotImplementedError(
                    f"Not implemented for {self.current_char}")

            self.advance()

        return tokens

    def make_string(self) -> Token:
        value = ""
        start_position = self.position.copy()
        self.advance()

        while self.current_char is not None:
            if self.current_char == "\"":
                return Token(TokenType.STRING, start_position, self.position, value)
            else:
                value += self.current_char

            self.advance()

        return Token(TokenType.STRING, start_position, self.position, value)

    def make_number(self) -> Token:
        value = ""
        start_position = self.position.copy()

        while self.current_char is not None:
            if self.current_char not in "0123456789.":
                self.retreat()
                return Token(TokenType.NUMBER, start_position, self.position, value)
            else:
                value += self.current_char

            self.advance()

        return Token(TokenType.NUMBER, start_position, self.position, value)

    def make_boolean(self) -> Token:
        value = ""
        start_position = self.position.copy()

        while self.current_char is not None:
            value += self.current_char
            if value in ("true", "false"):
                return Token(TokenType.BOOLEAN, start_position, self.position, value)

            self.advance()


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.position = -1
        self.current_token: Token = None

        self.advance()

    def advance(self):
        self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(
            self.tokens) else None

    def parse_simple(self) -> str | bool | float | int:
        if self.current_token.type == TokenType.STRING:
            return self.current_token.value
        elif self.current_token.type == TokenType.BOOLEAN:
            return True if self.current_token.value == "true" else False
        elif self.current_token.type == TokenType.NUMBER:
            return float(
                self.current_token.value) if "." in self.current_token.value else int(self.current_token.value)

        self.advance()

    def parse_object(self) -> dict:
        result = {}
        current_key = None

        self.advance()

        while self.current_token is not None:
            if self.current_token.type in (TokenType.COMMA, TokenType.COLON):
                pass
            elif self.current_token.type == TokenType.LEFT_CURLY_BRACE:
                result[current_key] = self.parse_object()
                current_key = None
            elif self.current_token.type == TokenType.RIGHT_CURLY_BRACE:
                self.advance()
                return result

            elif self.current_token.type == TokenType.LEFT_SQUARE_BRACE:
                result[current_key] = self.parse_list()
                current_key = None

            elif current_key is not None and self.current_token.type in (TokenType.BOOLEAN, TokenType.NUMBER, TokenType.STRING):
                result[current_key] = self.parse_simple()
                current_key = None
            elif self.current_token.type == TokenType.STRING:
                current_key = self.current_token.value
            else:
                print(result)
                raise NotImplementedError(
                    f"Not implemented for {self.current_token}")

            self.advance()

    def parse_list(self) -> list:
        result = []
        while self.current_token is not None:
            self.advance()

            if self.current_token.type in (TokenType.BOOLEAN, TokenType.NUMBER, TokenType.STRING):
                result.append(self.parse_simple())

            elif self.current_token.type == TokenType.LEFT_CURLY_BRACE:
                result.append(self.parse_object())

            elif self.current_token.type == TokenType.LEFT_SQUARE_BRACE:
                result.append(self.parse_list())

            elif self.current_token.type == TokenType.RIGHT_SQUARE_BRACE:
                self.advance()
                return result

    def parse(self) -> dict | list | str | bool | float | int:
        result = None

        if self.current_token.type == TokenType.LEFT_CURLY_BRACE:
            result = self.parse_object()
        elif self.current_token.type == TokenType.LEFT_SQUARE_BRACE:
            result = self.parse_list()
        elif self.current_token.type in (TokenType.BOOLEAN, TokenType.NUMBER, TokenType.STRING):
            result = self.parse_simple()
        else:
            raise TypeError(f"Invalid token {self.current_token}")

        return result


def parse(text: str) -> dict:
    tokens = Lexer(text).tokens()
    print(tokens)
    return Parser(tokens).parse()
