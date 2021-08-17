import sys


INPUT_FILEPATH = sys.argv[1]

with open(INPUT_FILEPATH) as f:
    input_lines = f.readlines()

scope = {}
for idx, input_line in enumerate(input_lines):
    print(f"Line #{idx}")
    
    lexems = [lexem.strip() for lexem in input_line.split() if lexem.strip()]

    stack = []
    for idx, lexem in enumerate(lexems):
        if lexem == ':=':
            if idx != len(lexems) - 1:
                raise ValueError("Incorrect use of :=")
            right, left = stack.pop(), stack.pop()
            scope[left] = float(right)
            break
        
        if lexem in "+-*/":
            right, left = stack.pop(), stack.pop()
            
            try:
                right = scope[right]
            except:
                right = float(right)
            try:
                left = scope[left]
            except:
                left = float(left)
            
            if lexem == "+":
                res = left + right
            elif lexem == "-":
                res = left - right
            elif lexem == "*":
                res = left * right
            else:
                res = left / right
            
            stack.append(res)
            continue

        stack.append(lexem)
    
    if stack:
        raise ValueError("Incorrect input", stack)
    
    print(scope)
