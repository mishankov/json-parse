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
