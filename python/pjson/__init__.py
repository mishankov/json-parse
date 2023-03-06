from pjson.lexer import Lexer
from pjson.parser import Parser, UnexpectedNextToken


def parse(text: str, print_tokens=False):
    tokens = Lexer(text).tokens()
    if print_tokens:
        print(tokens)
    try:
        return Parser(Lexer(text).tokens()).parse()
    except UnexpectedNextToken as e:
        print(tokens)
        raise e
