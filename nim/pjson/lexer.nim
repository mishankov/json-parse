import std/strutils

import position
import token

const DIGITS = "0123456789.-+Ee"

type Lexer* = object
    lines*: seq[string]
    position*: Position
    currentChar*: string
    previousChar*: string
    isDone*: bool

proc advance*(lexer: var Lexer) =
    if lexer.position.line == -1 and lexer.position.column == -1:
        lexer.position = Position(line: 0, column: 0)
    elif lexer.position.column + 1 < lexer.lines[lexer.position.line].len():
        lexer.position.column += 1
    elif lexer.position.line + 1 < lexer.lines.len() and lexer.lines[
            lexer.position.line + 1].len() > 0:
        lexer.position.line += 1
        lexer.position.column = 0
    else:
        lexer.isDone = true
        return

    lexer.previousChar = lexer.currentChar
    lexer.currentChar = $lexer.lines[lexer.position.line][lexer.position.column]

proc newLexer*(text: string): Lexer =
    result = Lexer(lines: text.splitLines(), position: Position(line: -1,
            column: -1), isDone: false)
    result.advance()

proc tokens*(lexer: var Lexer): seq[Token] =
    result = @[]

    while not lexer.isDone:
        if ["\n", "\t", " "].contains(lexer.currentChar):
            lexer.advance()
        elif lexer.currentChar == "{":
            result.add(newToken(TokenType.LEFT_CURLY_BRACE, lexer.position))
            lexer.advance()
        else:
            lexer.advance()


