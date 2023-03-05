from enum import Enum

from pjson.position import Position


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


VALID_NEXT_TOKENS = {
    TokenType.LEFT_CURLY_BRACE: [TokenType.RIGHT_CURLY_BRACE, TokenType.STRING],
    TokenType.RIGHT_CURLY_BRACE: [TokenType.COMMA, TokenType.RIGHT_SQUARE_BRACE],
    TokenType.LEFT_SQUARE_BRACE: [TokenType.STRING, TokenType.BOOLEAN, TokenType.NUMBER, TokenType.LEFT_CURLY_BRACE],
    TokenType.RIGHT_SQUARE_BRACE: [TokenType.COMMA, TokenType.RIGHT_SQUARE_BRACE, TokenType.RIGHT_CURLY_BRACE],
    TokenType.COLON: [TokenType.STRING, TokenType.BOOLEAN, TokenType.NUMBER, TokenType.LEFT_SQUARE_BRACE, TokenType.LEFT_CURLY_BRACE],
    TokenType.COMMA: [TokenType.STRING, TokenType.BOOLEAN, TokenType.NUMBER, TokenType.LEFT_SQUARE_BRACE, TokenType.LEFT_CURLY_BRACE],
    TokenType.STRING: [TokenType.COLON, TokenType.COMMA, TokenType.RIGHT_SQUARE_BRACE, TokenType.RIGHT_CURLY_BRACE],
    TokenType.NUMBER: [TokenType.COMMA, TokenType.RIGHT_CURLY_BRACE, TokenType.RIGHT_SQUARE_BRACE],
    TokenType.BOOLEAN: [TokenType.COMMA, TokenType.RIGHT_CURLY_BRACE, TokenType.RIGHT_SQUARE_BRACE],

}


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
