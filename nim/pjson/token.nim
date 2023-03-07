from position import Position

type
    TokenType* = enum
        LEFT_CURLY_BRACE,
        RIGHT_CURLY_BRACE,
        LEFT_SQUARE_BRACE,
        RIGHT_SQUARE_BRACE,
        COLON,
        COMMA,
        STRING,
        NUMBER,
        BOOLEAN,
        NULL

const VALID_NEXT_TOKENS* = {
    TokenType.LEFT_CURLY_BRACE: @[TokenType.RIGHT_CURLY_BRACE,
            TokenType.STRING],
    TokenType.RIGHT_CURLY_BRACE: @[TokenType.COMMA,
            TokenType.RIGHT_SQUARE_BRACE],
    TokenType.LEFT_SQUARE_BRACE: @[TokenType.STRING, TokenType.BOOLEAN,
            TokenType.NUMBER, TokenType.NULL, TokenType.LEFT_CURLY_BRACE,
            TokenType.RIGHT_SQUARE_BRACE, TokenType.LEFT_SQUARE_BRACE],
    TokenType.RIGHT_SQUARE_BRACE: @[TokenType.COMMA,
            TokenType.RIGHT_SQUARE_BRACE, TokenType.RIGHT_CURLY_BRACE],
    TokenType.COLON: @[TokenType.STRING, TokenType.BOOLEAN, TokenType.NUMBER,
            TokenType.NULL, TokenType.LEFT_SQUARE_BRACE,
            TokenType.LEFT_CURLY_BRACE],
    TokenType.COMMA: @[TokenType.STRING, TokenType.BOOLEAN, TokenType.NUMBER,
            TokenType.NULL, TokenType.LEFT_SQUARE_BRACE,
            TokenType.LEFT_CURLY_BRACE],
    TokenType.STRING: @[TokenType.COLON, TokenType.COMMA,
            TokenType.RIGHT_SQUARE_BRACE, TokenType.RIGHT_CURLY_BRACE],
    TokenType.NUMBER: @[TokenType.COMMA, TokenType.RIGHT_CURLY_BRACE,
            TokenType.RIGHT_SQUARE_BRACE],
    TokenType.BOOLEAN: @[TokenType.COMMA, TokenType.RIGHT_CURLY_BRACE,
            TokenType.RIGHT_SQUARE_BRACE],
    TokenType.NULL: @[TokenType.COMMA, TokenType.RIGHT_CURLY_BRACE,
            TokenType.RIGHT_SQUARE_BRACE],

}

type
    Token* = object
        tokenType*: TokenType
        startPosition*: Position
        endPosition*: Position
        value*: string

proc newToken*(tokenType: TokenType, startPosition: Position): Token =
    return Token(tokenType: tokenType, startPosition: startPosition,
            endPosition: startPosition)

proc newToken*(tokenType: TokenType, startPosition: Position,
        endPosition: Position = startPosition, value: string): Token =
    return Token(tokenType: tokenType, startPosition: startPosition,
            endPosition: endPosition, value: value)
