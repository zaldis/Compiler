class ExecutorError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class StackMachine:
    def __init__(self, poliz):
        self.poliz = poliz
        self.stack = []
        self.variables = {}
        self.pos = 0

    def process(self):
        while self.pos < len(self.poliz):
            self.stack.append(self.poliz[self.pos])
            self.pos += 1
            stack_head = self.stack.pop()

            if stack_head == "!":
                self.pos = self.stack.pop()
            elif stack_head == "!F":
                adr = self.stack.pop()
                if not self.stack.pop():
                    self.pos = adr
            elif stack_head == "print":
                self.printing(self.stack.pop())
            elif stack_head == "input":
                self.inputting(self.stack.pop())
            elif stack_head is not None:
                if (stack_head in ["+=", "+", "//=", "//", "/=", "/", "**", "*=", "*", "-=", "-", "not", "and", "or",
                                   "xor", ">=", ">", "<=", "<", "==", "=", "!=", "add", "inSet", "getValue", "getSize",
                                   "getFirst", "getLast", "getNext", "getPrev", "."]):
                    self.calculate(stack_head)
                else:
                    self.stack.append(stack_head)
            else:
                raise ExecutorError("Error: unexpected " + stack_head)

    def printing(self, value):
        if self.variables.get(value) is not None:
            print(f">  {str(self.variables.get(value))}")
        else:
            print(f">  {str(value)}")

    def inputting(self, var):
        if self.variables.get(var) is not None:
            v = str(input("<< "))
            self.variables[var] = self.convert_type(v)
        else:
            print(f"Error: variable '{var}' is not defined")
            exit(0)

    def convert_type(self, value):
        try:
            if value.find('"') != -1:
                return str(value)
            elif value == "True":
                return True
            elif value == "False":
                return False
            elif value.find('.') != -1:
                return float(value)
            else:
                return int(value)
        except Exception:
            print(f"Error: unknown type of value '{value}'")
            exit(0)

    def calculate(self, op):
        if op not in {"not", "getFirst", "getLast", "getNext", "getPrev", "getValue", "getSize"}:
            b = self.stack.pop()
            a = self.stack.pop()
        else:
            a = self.stack.pop()
            obj_ref = self.variables.get(a) if self.variables.get(a) is not None else a
            if op == "getFirst":
                self.stack.append(self.get_first(obj_ref))
            elif op == "getLast":
                self.stack.append(self.get_last(obj_ref))
            elif op == "getSize":
                self.stack.append(self.get_size(obj_ref))
            elif op == "getNext":
                self.stack.append(self.get_next(obj_ref))
            elif op == "getPrev":
                self.stack.append(self.get_prev(obj_ref))
            elif op == "getValue":
                self.stack.append(self.get_value(obj_ref))
            return

        if op == "=":
            b = self.variables.get(b) if type(b) == str else b
            self.assign(a, b)
        else:
            b = self.variables.get(b) if self.variables.get(b) is not None else b
            if op == "inSet":
                self.stack.append(self.in_set(a, b))
            elif op == "add":
                self.add(a, b)
            elif op == "-=":
                self.minusAssign(a, b)
            elif op == "+=":
                self.plusAssign(a, b)
            elif op == "*=":
                self.multAssign(a, b)
            elif op == "/=":
                self.divAssign(a, b)
            elif op == "//=":
                self.modAssign(a, b)
            else:
                a = self.variables.get(a) if self.variables.get(a) is not None else a
                if op == ".":
                    self.stack.append(self.concat(a, b))
                elif op == "+":
                    self.stack.append(self.plus(a, b))
                elif op == "-":
                    self.stack.append(self.minus(a, b))
                elif op == "*":
                    self.stack.append(self.mult(a, b))
                elif op == "**":
                    self.stack.append(self.pow(a, b))
                elif op == "/":
                    self.stack.append(self.div(a, b))
                elif op == "//":
                    self.stack.append(self.mod(a, b))
                elif op == "and":
                    self.stack.append(self.l_and(a, b))
                elif op == "or":
                    self.stack.append(self.l_or(a, b))
                elif op == "xor":
                    self.stack.append(self.l_xor(a, b))
                elif op == ">":
                    self.stack.append(self.l_greater(a, b))
                elif op == ">=":
                    self.stack.append(self.l_greaterEq(a, b))
                elif op == "<":
                    self.stack.append(self.l_less(a, b))
                elif op == "<=":
                    self.stack.append(self.l_lessEq(a, b))
                elif op == "!=":
                    self.stack.append(self.l_notEq(a, b))
                elif op == "==":
                    self.stack.append(self.l_equal(a, b))
                elif op == "not":
                    self.stack.append(self.l_not(a))

    def concat(self, val1, val2):
        return f"{val1}{val2}"

    def assign(self, num1, num2):
        try:
            self.variables[num1] = self.variables[num2] if self.variables.get(num2) is not None else num2
        except:
            raise ExecutorError(f"Error: {str(num1)} are not defined")

    def plus(self, num1, num2):
        try:
            return num1 + num2
        except:
            raise ExecutorError(f"Error: impossible operation: {str(num1)} + {str(num2)}")

    def minus(self, num1, num2):
        try:
            return num1 - num2
        except:
            raise ExecutorError(f"Error: impossible operation: {str(num1)} - {str(num2)}")

    def mult(self, num1, num2):
        try:
            return num1 * num2
        except:
            raise ExecutorError(f"Error: impossible operation: {str(num1)} * {str(num2)}")

    def pow(self, num1, num2):
        try:
            return num1 ** num2
        except:
            raise ExecutorError(f"Error: impossible operation: {str(num1)} ** {str(num2)}")

    def div(self, num1, num2):
        if num2 == 0:
            raise ExecutorError("Error: division by zero")
        try:
            return float(num1) / float(num2)
        except:
            raise ExecutorError("Error: impossible operation: " + str(num1) + " / " + str(num2))

    def mod(self, num1, num2):
        if type(num1) == float or type(num2) == float:
            raise ExecutorError("Error: modulus from float")
        elif num2 == 0:
            raise ExecutorError("Error: modulus by zero")
        try:
            return num1 % num2
        except:
            raise ExecutorError("Error: impossible operation: " + str(num1) + " // " + str(num2))

    def minusAssign(self, var, num):
        self.variables[var] = self.minus(self.variables.get(var), num)

    def plusAssign(self, var, num):
        self.variables[var] = self.plus(self.variables.get(var), num)

    def multAssign(self, var, num):
        self.variables[var] = self.mult(self.variables.get(var), num)

    def divAssign(self, var, num):
        self.variables[var] = self.div(self.variables.get(var), num)

    def modAssign(self, var, num):
        self.variables[var] = self.mod(self.variables.get(var), num)

    def l_greater(self, num1, num2):
        try:
            return num1 > num2,
        except:
            self.compare_exception(num1, num2)

    def l_greaterEq(self, num1, num2):
        try:
            return num1 >= num2
        except:
            self.compare_exception(num1, num2)

    def l_less(self, num1, num2):
        try:
            return num1 < num2
        except:
            self.compare_exception(num1, num2)

    def l_lessEq(self, num1, num2):
        try:
            return num1 <= num2
        except:
            self.compare_exception(num1, num2)

    def l_notEq(self, num1, num2):
        try:
            return num1 != num2
        except:
            self.compare_exception(num1, num2)

    def l_equal(self, num1, num2):
        try:
            return num1 == num2
        except:
            self.compare_exception(num1, num2)

    def l_not(self, num):
        if type(num) == bool:
            return not num
        else:
            raise ExecutorError("Error: using LOGICAL NOT for non-logical expression")

    def l_or(self, num1, num2):
        if type(num1) == bool and type(num2) == bool:
            return num1 or num2
        else:
            raise ExecutorError("Error: using LOGICAL OR for non-logical expression")

    def l_and(self, num1, num2):
        if type(num1) == bool and type(num2) == bool:
            return num1 and num2
        else:
            raise ExecutorError("Error: using LOGICAL AND for non-logical expression")

    def l_xor(self, num1, num2):
        if type(num1) == bool and type(num2) == bool:
            return ((not num1) and num2) or (num1 and (not num2))
        else:
            raise ExecutorError("Error: using LOGICAL XOR for non-logical expression")

    def add(self, obj, val):
        try:
            self.variables[obj].add(val)
        except:
            raise ExecutorError(f"Error: {str(obj)} has no add method")

    def in_set(self, obj, val):
        try:
            return self.variables[obj].in_set(val)
        except:
            raise ExecutorError(f"Error: {str(obj)} has no inSet method")

    def get_size(self, obj):
        try:
            return obj.get_size()
        except:
            raise ExecutorError(f"Error: {str(obj)} has no getSize method")

    def get_first(self, obj):
        try:
            return obj.get_first()
        except:
            raise ExecutorError(f"Error: {str(obj)} has no getFirst method")

    def get_last(self, obj):
        try:
            return obj.get_last()
        except:
            raise ExecutorError(f"Error: {str(obj)} has no getLast method")

    def get_next(self, obj):
        try:
            return obj.get_next()
        except:
            raise ExecutorError(f"Error: {str(obj)} has no getNext method")

    def get_prev(self, obj):
        try:
            return obj.get_prev()
        except:
            raise ExecutorError(f"Error: {str(obj)} has no getPrev method")

    def get_value(self, obj):
        try:
            return obj.get_value()
        except:
            raise ExecutorError(f"Error: {str(obj)} has no getValue method")

    def compare_exception(self, n1, n2):
        raise ExecutorError(f"Error: impossible to compare '{str(n1)}' and '{str(n2)}' values")


def do_calculate(poliz):
    machine = StackMachine(poliz)
    machine.process()
