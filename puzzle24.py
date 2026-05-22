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