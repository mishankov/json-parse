from pjson.token import Token, TokenType, VALID_NEXT_TOKENS


class InvalidFirstToken(Exception):
    pass


class UnexpectedNextToken(Exception):
    pass


def escape_chars_hack(value: str):
    SYMBOLS = {
        "\\n": "\n",
        "\\r": "\r",
        "\\t": "\t",
        "\\b": "\b",
        "\\f": "\f",
    }

    for _from, to in SYMBOLS.items():
        value = value.replace(_from, to)

    return value


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.position = -1
        self.current_token: Token = None
        self.previous_token: Token = None

        self.advance()

    def advance(self):
        self.previous_token = self.current_token

        self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(
            self.tokens) else None

        if not self.previous_token or not self.current_token:
            return

        if self.current_token.type not in VALID_NEXT_TOKENS[self.previous_token.type]:
            raise UnexpectedNextToken(
                f"{self.current_token} is not expeted after {self.previous_token}")

    def parse_simple(self) -> str | bool | float | int:
        current_token = self.current_token
        self.advance()

        if current_token.type == TokenType.STRING:
            return escape_chars_hack(current_token.value)
        elif current_token.type == TokenType.BOOLEAN:
            return True if current_token.value == "true" else False
        elif current_token.type == TokenType.NUMBER:
            return float(
                current_token.value) if "." in current_token.value or "e" in current_token.value.lower() else int(current_token.value)
        elif current_token.type == TokenType.NULL:
            return None

    def parse_object(self) -> dict:
        result = {}
        current_key = None

        self.advance()

        while self.current_token is not None:
            if self.current_token.type in (TokenType.COMMA, TokenType.COLON):
                self.advance()
            elif self.current_token.type == TokenType.LEFT_CURLY_BRACE:
                result[current_key] = self.parse_object()
                current_key = None
            elif self.current_token.type == TokenType.RIGHT_CURLY_BRACE:
                self.advance()
                return result

            elif self.current_token.type == TokenType.LEFT_SQUARE_BRACE:
                result[current_key] = self.parse_list()
                current_key = None

            elif current_key is not None and self.current_token.type in (TokenType.BOOLEAN, TokenType.NUMBER, TokenType.STRING, TokenType.NULL):
                result[current_key] = self.parse_simple()
                current_key = None
            elif self.current_token.type == TokenType.STRING:
                current_key = self.current_token.value
                self.advance()
            else:
                raise NotImplementedError(
                    f"Not implemented for {self.current_token}")

    def parse_list(self) -> list:
        result = []
        self.advance()
        while self.current_token is not None:

            if self.current_token.type in (TokenType.BOOLEAN, TokenType.NUMBER, TokenType.STRING, TokenType.NULL):
                result.append(self.parse_simple())

            elif self.current_token.type == TokenType.LEFT_CURLY_BRACE:
                result.append(self.parse_object())

            elif self.current_token.type == TokenType.LEFT_SQUARE_BRACE:
                result.append(self.parse_list())

            elif self.current_token.type == TokenType.COMMA:
                self.advance()

            elif self.current_token.type == TokenType.RIGHT_SQUARE_BRACE:
                self.advance()
                return result

    def parse(self) -> dict | list | str | bool | float | int:
        result = None

        if self.current_token.type == TokenType.LEFT_CURLY_BRACE:
            result = self.parse_object()
        elif self.current_token.type == TokenType.LEFT_SQUARE_BRACE:
            result = self.parse_list()
        elif self.current_token.type in (TokenType.BOOLEAN, TokenType.NUMBER, TokenType.STRING, TokenType.NULL):
            result = self.parse_simple()
        else:
            raise InvalidFirstToken(
                f"Invalid fist token {self.current_token}")

        return result
