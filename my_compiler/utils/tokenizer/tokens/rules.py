from .token import Token
from . import token
from . import tags


from typing import NamedTuple, List


class Rule(NamedTuple):
    pattern: str
    tag: str
    priority: int


RULES: List[Rule] = [
    Rule(r'[ \t\n]+', tags.SPACE, 0),
    Rule(r'!![^\n]*', tags.COMMENT, 0),

    Rule(r'\+=', tags.PLUS_ASSIGN, 1),
    Rule(r'\+', tags.PLUS, 6),
    Rule(r'//=', tags.MOD_ASSIGN, 1),
    Rule(r'//', tags.MOD, 7),
    Rule(r'/=', tags.DIVISION_ASSIGN, 1),
    Rule(r'/', tags.DIVISION, 7),
    Rule(r'\*\*', tags.POW, 8),
    Rule(r'\*=', tags.MULT_ASSIGN, 1),
    Rule(r'\*', tags.MULT, 7),

    Rule(r'not', tags.NOT, 4),
    Rule(r'and', tags.AND, 3),
    Rule(r'or', tags.OR, 2),
    Rule(r'xor', tags.XOR, 2),
    Rule(r'>=', tags.GREATER_EQUAL, 5),
    Rule(r'>', tags.GREATER, 5),
    Rule(r'<=', tags.LESS_EQUAL, 5),
    Rule(r'<', tags.LESS, 5),
    Rule(r'==', tags.EQUAL, 4),
    Rule(r'=', tags.ASSIGN, 1),
    Rule(r'!=', tags.NOT_EQUAL, 4),

    Rule(r'\(', tags.BRACKET_OPEN, 0),
    Rule(r'\)', tags.BRACKET_CLOSE, 0),
    Rule(r'\{', tags.CURLY_BRACKET_OPEN, 0),
    Rule(r'\}', tags.CURLY_BRACKET_CLOSE, 0),
    Rule(r';', tags.SEMICOLON, 0),
    Rule(r'\.', tags.CONCAT, 1),

    Rule(r'add', tags.ADD, 1),
    Rule(r'if', tags.IF, 1),
    Rule(r'else', tags.ELSE, 1),
    Rule(r'while', tags.WHILE, 1),
    Rule(r'print', tags.PRINT, 1),
    Rule(r'input', tags.INPUT, 1),
    Rule(r'True', tags.BOOL, 0),
    Rule(r'False', tags.BOOL, 0),
    Rule(r'"[^"]*"', tags.STRING, 0),
    Rule(r'-=', tags.MINUS_ASSIGN, 1),
    Rule(r'-?[0-9]+\.[0-9]+', tags.FLOAT, 0),
    Rule(r'-?[0-9]+', tags.INT, 0),
    Rule(r'-', tags.MINUS, 6),
    Rule(r'[A-Za-z_][A-Za-z0-9_]*', tags.VARIABLE, 0)
]
