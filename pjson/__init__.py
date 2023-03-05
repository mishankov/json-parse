from pjson.lexer import Lexer
from pjson.parser import Parser


def parse(text: str):
    tokens = Lexer(text).tokens()
    print(tokens)
    return Parser(tokens).parse()
