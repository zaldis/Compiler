import re
from typing import List

from .errors.syntax import InvalidSyntaxError
from .tokens.rules import RULES, Rule
from .tokens.token import Token
from .tokens import tags


class Tokenizer:

    def __init__(self, program: str):
        self.program = program

    def get_tokens(self, rules: List[Rule] = RULES) -> List[Token]:
        tokens: List[Token] = []
        position = 0
        while position < len(self.program):
            match = None
            for rule in rules:
                pattern, tag, priority = rule

                regex = re.compile(pattern)
                match = regex.match(self.program, position)
                if match:
                    lexem = match.group(0)
                    if tag not in [tags.SPACE, tags.COMMENT]:
                        token = Token(lexem.replace('"', ''), tag, priority)
                        tokens.append(token)
                    break

            if not match:
                raise InvalidSyntaxError(self.program[position])
            else:
                position = match.end(0)
        return tokens
