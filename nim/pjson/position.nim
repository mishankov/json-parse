type
    Position* = object
        line*: int
        column*: int

proc copy*(p: Position): Position =
    return Position(line: p.line, column: p.column)
