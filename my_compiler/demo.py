from utils.tokenizer.main import Tokenizer
from utils.parser import do_parse
from utils.executer import do_calculate


program = ""

# with open("tests/test_programs/factorial.zaldis") as f:
# with open("tests/test_programs/fibonacci.zaldis") as f:
with open("tests/test_programs/pow.zaldis") as f:
    program = f.read()
    print(f"Source program:\n{'=' * 20}\n{program}\n\n{'=' * 20}")

tokenizer = Tokenizer(program)
tokens = tokenizer.get_tokens()
for token in tokens:
    print(token)

print('=' * 20)

print("\n Postfix notation:\n")
print('=' * 20)
postfix_notation = do_parse(tokens)
print(postfix_notation)
print('=' * 20)

do_calculate(postfix_notation)