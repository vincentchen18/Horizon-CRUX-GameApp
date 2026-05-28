from fractions import Fraction
from itertools import permutations, product
import ast, random

ops = ["+", "-", "*", "/"]

def apply_op(a,b,op):
    if op == "+":
        return a+b
    elif op == "-":
        return a-b
    elif op == "*":
        return a*b
    elif op == "/":
        return a/b
    return None

def solve(nums):
    target = Fraction(24)
    for a, b, c, d in permutations(nums):
        fa, fb, fc, fd = map(Fraction, (a, b, c, d))
        for op1, op2, op3 in product(ops, repeat=3):
            tries = [
                lambda: apply_op(apply_op(apply_op(fa, fb, op1), fc, op2), fd, op3),
                lambda: apply_op(apply_op(fa, apply_op(fb, fc, op2), op1), fd, op3),
                lambda: apply_op(apply_op(fa, fb, op1), apply_op(fc, fd, op3), op2),
                lambda: apply_op(fa, apply_op(apply_op(fb, fc, op2), fd, op3), op1),
                lambda: apply_op(fa, apply_op(fb, apply_op(fc, fd, op3), op2), op1),
            ]
            shapes = [
                f"(({a}{op1}{b}){op2}{c}){op3}{d}",
                f"({a}{op1}({b}{op2}{c})){op3}{d}",
                f"({a}{op1}{b}){op2}({c}{op3}{d})",
                f"{a}{op1}(({b}{op2}{c}){op3}{d})",
                f"{a}{op1}({b}{op2}({c}{op3}{d}))",
            ]
            for try_eval, shape in zip(tries, shapes):
                try:
                    if try_eval() == target:
                        return shape
                except ZeroDivisionError:
                    continue
    return None
legal_ops = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub, ast.UAdd)
def puzzle_generate():
    while True:
        nums = tuple(random.randint(1, 15) for _ in range(4))
        if solve(nums) is not None:
            return nums

def ast_applyop(a,b,op):
    if isinstance(op, ast.Add):
        return a + b
    elif isinstance(op, ast.Sub):
        return a - b
    elif isinstance(op, ast.Mult):
        return a * b
    elif isinstance(op, ast.Div):
        return a / b
    raise ValueError("Unsupported operator")

def eval_ast(node):
    if isinstance(node, ast.Expression):
        return eval_ast(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return Fraction(node.value)
    if isinstance(node, ast.BinOp) and isinstance(node.op, legal_ops):
        return ast_applyop(eval_ast(node.left), eval_ast(node.right), node.op)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, legal_ops):
        val = eval_ast(node.operand)
        if isinstance(node.op, ast.USub):
            return -val
        return val
    raise ValueError("SyntaxError")

def ints(node, out):
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        out.append(node.value)
    for child in ast.iter_child_nodes(node):
        ints(child, out)

def parse_check(expression, nums):
    try:
        tree = ast.parse(expression, mode='eval')
    except SyntaxError: # not a valid expression, or contains illegal ops
        return ('parse-error', 'Could not parse expression.')
    used = []
    ints(tree, used)
    if sorted(used) != sorted(nums): # used wrong numbers
        return ('wrong-numbers', f"You must exactly use {sorted(nums)}, each once, instead of {sorted(used)}.")
    try:
        val = eval_ast(tree)
    except ZeroDivisionError:
        return ('parse-error', 'Division by zero.')
    except ValueError as error:
        return ('parse-error', f"Illegal syntax: {error}.")

    if val == 24:
        return ('correct', f'{expression} = 24 ✓') #correct
    return ('wrong-value', f'{expression} = {val}, not 24.') #wrong

def puzzle24_play():
    print("=== 24 Puzzle ===")
    while True:
        c = input("1) Play 24 Puzzle    2) Exit    Please enter 1 or 2: ").strip()
        if c == "1":
            break
        elif c == "2":
            return
        else:
            print("That's not a valid choice, please enter 1 or 2.")
    solves = 0
    while True:
        nums = puzzle_generate()
        print()
        print(f"Make 24 using {' '.join(list(map(str, nums)))}, using each number exactly once with operations +, -, * and / and parentheses.")
        while True:
            inp = input("Your math expression (or Q to give up, or N to get a new puzzle): ").strip()
            if inp.upper() == "Q":
                print(f"One possible solution is {solve(nums)}.")
                break
            elif inp.upper() == "N":
                break
            status, detail = parse_check(inp, nums)
            print(detail)
            if status == "correct":
                solves += 1
                print(f"Solved! Total solves: {solves}")
                break
        while True:
            again = input("Would you like to play again? (y/n): ").strip().upper()
            if again in ("Y", "YES"):
                break
            elif again in ("N", "NO"):
                print(f"You solved a total of {solves} puzzles.")
                return
            else:
                print("That's not a valid choice, please enter Y or N.")

if __name__ == "__main__":
    puzzle24_play()


