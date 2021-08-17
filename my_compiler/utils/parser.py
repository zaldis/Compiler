from typing import List

from .tokenizer.tokens.token import Token
from .tokenizer.tokens import tags


class ParseError(Exception):
    def __init__(self, expected, detected, message="Parse error"):
        self.expected = expected
        self.detected = detected
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: expected {self.expected}, detected {self.detected}"


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_position = 0
        self.postfix_notation = []
        self.buffer: List[Token] = []
        self.filling_addresses = []
        self.jump_addresses = []
        self.calls = []

    def end_script(self):
        return self.current_position == len(self.tokens)

    def parse(self):
        return self.lang()

    def lang(self):
        while not self.end_script():
            if not self.expr():
                raise ParseError("expression", self.tokens[self.current_position].value)
        return True

    def expr(self):
        return self.assign() or self.while_stmt() or self.if_stmt() or self.io()

    def io(self):
        return self.printing() or self.inputting()

    def assign(self):
        if not self.var():
            return False
        elif self.assign_op():
            if not (self.obj_mulref() or self.arif_stmt()):
                raise ParseError("arifmetical expression or object initialization", self.tokens[self.current_position].value)
        elif not self.add_val():
            raise ParseError("var or object initialization", self.tokens[self.current_position].value)
        if not self.semicolon():
            raise ParseError(";", self.tokens[self.current_position].value)
        return True

    def add_val(self):
        return self.obj_ref() and self.obj_add()

    def obj_mulref(self):
        if not self.var():
            return False
        # elif self.obj_ref() and self.obj_simp_method():
        #     while True:
        #         if not self.obj_ref() and self.obj_simp_method():
        #             return True
        else:
            self.postfix_notation.pop()
            self.current_position -= 1
            return False

    def obj_add(self):
        if not self.tokens[self.current_position].tag == tags.ADD:
            return False
        self.pushInStack(self.tokens[self.current_position])
        self.current_position += 1
        if not self.bkt_open():
            raise ParseError("(", self.tokens[self.current_position].value)
        elif not self.arif_stmt():
            raise ParseError("arithmetic expression", self.tokens[self.current_position].value)
        elif not self.bkt_close():
            raise ParseError(")", self.tokens[self.current_position].value)
        return True

    # def obj_simp_method(self):
    #     if (self.tokens[self.current_position][1] == "GSIZE" or self.tokens[self.current_position][1] == "GNEXT" or
    #         self.tokens[self.current_position][1] == "GPREV" or self.tokens[self.current_position][1] == "GVALUE" or
    #         self.tokens[self.current_position][1] == "GFIRST" or self.tokens[self.current_position][1] == "GLAST"):
    #         self.pushInStack(self.tokens[self.current_position])
    #         self.current_position += 1
    #         return True
    #     return self.obj_inset()

    # def obj_inset(self):
    #     if not self.tokens[self.current_position][1] == "INSET":
    #         return False
    #     self.pushInStack(self.tokens[self.current_position])
    #     self.current_position += 1
    #     if not self.bkt_open():
    #         raise ParseError("(", self.tokens[self.current_position][0])
    #     elif not self.arif_stmt():
    #         raise ParseError("arithmetic expression", self.tokens[self.current_position][0])
    #     elif not self.bkt_close():
    #         raise ParseError(")", self.tokens[self.current_position][0])
    #     return True

    # def obj_ref(self):
    #     if self.tokens[self.current_position][1] == "OBJ_REF":
    #         self.current_position += 1
    #         return True
    #     return False

    def var(self):
        if self.tokens[self.current_position].tag == tags.VARIABLE:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def assign_op(self):
        if self.tokens[self.current_position].tag in [
            tags.ASSIGN,
            tags.PLUS_ASSIGN,
            tags.MINUS_ASSIGN,
            tags.MULT_ASSIGN,
            tags.DIVISION_ASSIGN,
            tags.MOD_ASSIGN
        ]:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def arif_stmt(self):
        if not self.value():
            return False
        while True:
            if not self.arif_op() and not self.value():
                break
        return True

    def value(self):
        return self.var() or self.number() or self.bkt_expr()

    def number(self):
        if self.tokens[self.current_position].tag in [
            tags.INT,
            tags.FLOAT,
            tags.BOOL
        ]:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def bkt_expr(self):
        if not self.bkt_open():
            return False
        elif not self.arif_stmt():
            raise ParseError("arithmetic expression", self.tokens[self.current_position].value)
        elif not self.bkt_close():
            raise ParseError(")", self.tokens[self.current_position].value)
        return True

    def log_stmt(self):
        if not self.comp_expr():
            return False
        while True:
            if self.log_op():
                if not self.comp_expr():
                    raise ParseError("compare expression", self.tokens[self.current_position].value)
            else:
                break
        return True

    def comp_expr(self):
        if self.log_not():
            return False
        if self.arif_stmt():
            if not self.comp_op():
                raise ParseError("compare expression", self.tokens[self.current_position].value)
            elif not self.arif_stmt():
                raise ParseError("arithmetic expression", self.tokens[self.current_position].value)
            return True
        return False

    def if_stmt(self):
        if not self.KW_IF():
            return False
        elif not self.bkt_open():
            raise ParseError("(", self.tokens[self.current_position].value)
        elif not self.log_stmt():
            raise ParseError("logical expression", self.tokens[self.current_position].value)
        elif not self.bkt_close():
            raise ParseError(")", self.tokens[self.current_position].value)
        elif not self.brace_open():
            raise ParseError("{", self.tokens[self.current_position].value)
        while True:
            if not self.expr():
                break
        if not self.brace_close():
            raise ParseError("}", self.tokens[self.current_position].value)

        return not (self.tokens[self.current_position].tag == tags.ELSE and not self.else_stmt())

    def else_stmt(self):
        if not self.KW_ELSE():
            return False
        elif not self.brace_open():
            raise Exception("{", self.tokens[self.current_position].value)
        while True:
            if not self.expr():
                break
        if not self.brace_close():
            raise Exception("}", self.tokens[self.current_position].value)
        return True

    def KW_IF(self):
        if self.tokens[self.current_position].tag == tags.IF:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def KW_ELSE(self):
        if self.tokens[self.current_position].tag == tags.ELSE:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def printing(self):
        if not self.KW_PRINT():
            return False
        elif not self.bkt_open():
            raise ParseError("(", self.tokens[self.current_position].tag)
        elif not self.str_stmt():
            raise ParseError("string or arithmetic expression", self.tokens[self.current_position].tag)
        elif (not self.bkt_close()):
            raise ParseError(")", self.tokens[self.current_position].tag)
        elif (not self.semicolon()):
            raise ParseError(";", self.tokens[self.current_position].tag)
        return True

    def KW_PRINT(self):
        if self.tokens[self.current_position].tag == tags.PRINT:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def str_stmt(self):
        if not self.substr():
            return False
        while True:
            if not self.concat() and not self.substr():
                break
        return True

    def substr(self):
        return self.string() or self.arif_stmt()

    def string(self):
        if self.tokens[self.current_position].tag == tags.STRING:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def concat(self):
        if self.tokens[self.current_position].tag == tags.CONCAT:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def inputting(self):
        if not self.KW_INPUT():
            return False
        elif not self.bkt_open():
            raise ParseError("(", self.tokens[self.current_position].value)
        elif not self.var():
            raise ParseError("variable", self.tokens[self.current_position].value)
        elif not self.bkt_close():
            raise ParseError(")", self.tokens[self.current_position].value)
        elif not self.semicolon():
            raise ParseError(";", self.tokens[self.current_position].value)
        return True

    def KW_INPUT(self):
        if (self.tokens[self.current_position].tag == tags.INPUT):
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def while_stmt(self):
        if not self.KW_WHILE():
            return False
        elif not self.bkt_open():
            raise ParseError("(", self.tokens[self.current_position].value)
        elif not self.log_stmt():
            raise ParseError("logical expression", self.tokens[self.current_position].value)
        elif not self.bkt_close():
            raise ParseError(")", self.tokens[self.current_position].value)
        elif not self.brace_open():
            raise ParseError("{", self.tokens[self.current_position].value)
        while True:
            if not self.expr():
                break
        if not self.brace_close():
            raise ParseError("}", self.tokens[self.current_position].value)
        return True

    def KW_WHILE(self):
        if self.tokens[self.current_position].tag == tags.WHILE:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def brace_open(self):
        if self.tokens[self.current_position].tag == tags.CURLY_BRACKET_OPEN:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def brace_close(self):
        if self.tokens[self.current_position].tag == tags.CURLY_BRACKET_CLOSE:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def bkt_open(self):
        if self.tokens[self.current_position].tag == tags.BRACKET_OPEN:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def bkt_close(self):
        if self.tokens[self.current_position].tag == tags.BRACKET_CLOSE:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    # def inc_dec(self):
    #     if self.tokens[self.current_position][1] == "INC" or self.tokens[self.current_position][1] == "DEC":
    #         self.pushInStack(self.tokens[self.current_position])
    #         self.current_position += 1
    #         return True
    #     return False

    def arif_op(self):
        if self.tokens[self.current_position].tag in [
            tags.MULT,
            tags.PLUS,
            tags.MINUS,
            tags.DIVISION,
            tags.MOD,
            tags.POW
        ]:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def log_op(self):
        if self.tokens[self.current_position].tag in [
            tags.AND,
            tags.OR,
            tags.XOR
        ]:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def comp_op(self):
        if self.tokens[self.current_position].tag in [
            tags.GREATER_EQUAL,
            tags.GREATER,
            tags.LESS_EQUAL,
            tags.LESS,
            tags.EQUAL,
            tags.NOT_EQUAL,
        ]:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def log_not(self):
        if self.tokens[self.current_position].tag == tags.NOT:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def semicolon(self):
        if self.tokens[self.current_position].tag == tags.SEMICOLON:
            self.pushInStack(self.tokens[self.current_position])
            self.current_position += 1
            return True
        return False

    def valInTruthType(self, token: Token):
        if token.tag == tags.INT:
            return int(token.value)
        elif token.tag == tags.FLOAT:
            return float(token.value)
        elif token.tag == tags.BOOL:
            return token.value == "True"
        else:
            return token.value

    def pushInStack(self, token: Token):
        if token.tag in {
            tags.INT, tags.FLOAT, tags.BOOL,
            tags.VARIABLE,
            tags.STRING,
        }:
            self.postfix_notation.append(self.valInTruthType(token))
        elif token.tag in {
            tags.WHILE, tags.IF, tags.ELSE
        }:
            self.calls.append(token.tag)
            self.buffer.append(token)
            if token.tag == tags.ELSE:
                self.buffer.pop()
                self.filling_addresses.append(len(self.postfix_notation))
                self.postfix_notation.append(0)
                self.postfix_notation.append("!")
            elif token.tag == tags.WHILE:
                self.jump_addresses.append(len(self.postfix_notation))
        else:
            if token.value == ")":
                while self.buffer[-1].value != "(":
                    head_token = self.buffer.pop()
                    self.postfix_notation.append(head_token.value)
                self.buffer.pop()

                if self.buffer[-1].tag in {tags.IF, tags.WHILE}:
                    self.buffer.pop()
                    self.filling_addresses.append(len(self.postfix_notation))
                    self.postfix_notation.append(0)
                    self.postfix_notation.append("!F")
            elif token.value == "}":
                while self.buffer[-1].value != "{":
                    body_token = self.buffer.pop()
                    self.postfix_notation.append(body_token.value)
                self.buffer.pop()
                lastCall = self.calls.pop()
                if lastCall == tags.WHILE:
                    self.postfix_notation.append(self.jump_addresses.pop())
                    self.postfix_notation.append("!")
                    self.postfix_notation[self.filling_addresses.pop()] = len(self.postfix_notation)
                elif lastCall == tags.IF:
                    self.postfix_notation[self.filling_addresses.pop()] = len(self.postfix_notation)
                elif lastCall == tags.ELSE:
                    self.postfix_notation[self.filling_addresses.pop()] = len(self.postfix_notation)
                else:
                    self.postfix_notation.append(None)
            elif token.value != "(" and token.value != "{" and len(self.buffer) != 0:
                if token.priority < self.buffer[-1].priority:
                    if token.tag == tags.SEMICOLON:
                        while not self.buffer[-1].value in {"=", "-=", "+=", "*=", "/=", "//=", "print", ".",
                                                                 "input", "add"}:
                            body_token = self.buffer.pop()
                            self.postfix_notation.append(body_token.value)
                    body_token = self.buffer.pop()
                    self.postfix_notation.append(body_token.value)

            if not token.value in {";", ")", "}"}:
                self.buffer.append(token)

    def endEl(self, n):
        return 0 if (len(n) == 0) else n[-1]


def do_parse(tokens):
    p = Parser(tokens)
    if p.parse():
        return p.postfix_notation
