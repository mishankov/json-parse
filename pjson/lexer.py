from pjson.position import Position
from pjson.token import Token, TokenType


class UnexpectedToken(Exception):
    pass


DIGITS = "0123456789.-+Ee"


class Lexer:
    def __init__(self, text: str) -> None:
        self.lines = text.split("\n")
        self.position = Position(-1, -1)
        self.current_char = None
        self.previous_char = None

        self.advance()

    def advance(self):
        if self.position.line == -1 and self.position.column == -1:
            self.position = Position(0, 0)
        elif self.position.column + 1 < len(self.lines[self.position.line]):
            self.position.column += 1
        elif self.position.line + 1 < len(self.lines) and len(self.lines[self.position.line + 1]) > 0:
            self.position.line += 1
            self.position.column = 0
        else:
            self.position, self.current_char, self.previous_char = None, None, None
            return

        self.previous_char = self.current_char
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
                self.advance()

            elif self.current_char == "{":
                tokens.append(Token(TokenType.LEFT_CURLY_BRACE, self.position))
                self.advance()
            elif self.current_char == "}":
                tokens.append(
                    Token(TokenType.RIGHT_CURLY_BRACE, self.position))
                self.advance()

            elif self.current_char == "[":
                tokens.append(
                    Token(TokenType.LEFT_SQUARE_BRACE, self.position))
                self.advance()
            elif self.current_char == "]":
                tokens.append(
                    Token(TokenType.RIGHT_SQUARE_BRACE, self.position))
                self.advance()

            elif self.current_char == ":":
                tokens.append(
                    Token(TokenType.COLON, self.position))
                self.advance()
            elif self.current_char == ",":
                tokens.append(
                    Token(TokenType.COMMA, self.position))
                self.advance()

            elif self.current_char == "\"":
                tokens.append(self.make_string())

            elif self.current_char in DIGITS:
                tokens.append(self.make_number())

            elif self.current_char in "ft":
                tokens.append(self.make_boolean())

            elif self.current_char == "n":
                tokens.append(self.make_null())

            else:
                raise UnexpectedToken(
                    f"Unexpected token '{self.current_char}' at {self.position}")

            # self.advance()

        return tokens

    def make_string(self) -> Token:
        value = ""
        consecutive_backslash_amount = 0
        start_position = self.position.copy()
        self.advance()

        while self.current_char is not None:
            if self.current_char == "\"" and consecutive_backslash_amount % 2 == 0:
                end_position = self.position.copy()
                self.advance()
                return Token(TokenType.STRING, start_position, end_position, value)
            else:
                value += self.current_char

            if self.current_char == "\\":
                consecutive_backslash_amount += 1
            else:
                consecutive_backslash_amount = 0

            self.advance()

        return Token(TokenType.STRING, start_position, self.position, value)

    def make_number(self) -> Token:
        value = ""
        start_position = self.position.copy()
        end_position = self.position.copy()

        while self.current_char is not None:
            if self.current_char not in DIGITS:
                return Token(TokenType.NUMBER, start_position, end_position, value)
            else:
                value += self.current_char
                end_position = self.position.copy()
                self.advance()

        return Token(TokenType.NUMBER, start_position, self.position, value)

    def make_boolean(self) -> Token:
        value = ""
        start_position = self.position.copy()

        while self.current_char is not None:
            value += self.current_char
            self.advance()
            if value in ("true", "false"):
                return Token(TokenType.BOOLEAN, start_position, self.position, value)

    def make_null(self) -> Token:
        value = ""
        start_position = self.position.copy()

        while self.current_char is not None:
            value += self.current_char
            end_position = self.position.copy()
            self.advance()
            if value == "null":
                return Token(TokenType.NULL, start_position, end_position, value)
