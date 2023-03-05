"""
[x] Token should have information about its position
[x] Lexer errors with positions
[ ] Parsing validation
    [ ] Do not ignore commas and colons
"""

from pjson.lexer import Lexer
from pjson.parser import Parser


def parse(text: str):
    tokens = Lexer(text).tokens()
    print(tokens)
    return Parser(tokens).parse()
