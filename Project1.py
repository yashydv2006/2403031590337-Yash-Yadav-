#Expression Calculator

import re
import sys

# ---------------- Exceptions ----------------
class CalculatorError(Exception):
    """Base class for calculator errors."""

class TokenizeError(CalculatorError):
    pass

class ParseError(CalculatorError):
    pass

class EvaluationError(CalculatorError):
    pass

# ---------------- Tokenizer ----------------
TOKEN_REGEX = re.compile(
    r"\s*(?:"                     # allow whitespace
    r"(?P<NUMBER>(?:\d+(?:\.\d*)?|\.\d+))"  # number (int or float)
    r"|(?P<OP>[\+\-\*/\^])"       # operators
    r"|(?P<LPAREN>\()"            # left paren
    r"|(?P<RPAREN>\))"            # right paren
    r")"
)

PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "^": 3,
    "u-": 4,  # unary minus
}

ASSOC = {
    "+": "L",
    "-": "L",
    "*": "L",
    "/": "L",
    "^": "R",
    "u-": "R",
}

def tokenize(expr: str):
    pos = 0
    tokens = []
    while pos < len(expr):
        m = TOKEN_REGEX.match(expr, pos)
        if not m:
            raise TokenizeError(f"Unexpected character at position {pos}: {expr[pos:pos+10]!r}")
        pos = m.end()
        if m.lastgroup == "NUMBER":
            tokens.append(("NUMBER", m.group("NUMBER")))
        elif m.lastgroup == "OP":
            tokens.append(("OP", m.group("OP")))
        elif m.lastgroup == "LPAREN":
            tokens.append(("LPAREN", "("))
        elif m.lastgroup == "RPAREN":
            tokens.append(("RPAREN", ")"))
    return tokens

def annotate_unary(tokens):
    """Turn unary minus into u- operator"""
    annotated = []
    prev_type = None
    for tok_type, tok_val in tokens:
        if tok_type == "OP" and tok_val == "-":
            if prev_type in (None, "OP", "LPAREN"):
                annotated.append(("OP", "u-"))
            else:
                annotated.append((tok_type, tok_val))
        else:
            annotated.append((tok_type, tok_val))
        prev_type = tok_type
    return annotated

# ---------------- Infix → Postfix ----------------
def infix_to_postfix(expr: str):
    tokens = tokenize(expr)
    tokens = annotate_unary(tokens)

    out = []
    stack = []

    for tok_type, tok_val in tokens:
        if tok_type == "NUMBER":
            out.append(tok_val)
        elif tok_type == "OP":
            while stack:
                top = stack[-1]
                if top == "(":
                    break
                if (ASSOC[tok_val] == "L" and PRECEDENCE[tok_val] <= PRECEDENCE[top]) or \
                   (ASSOC[tok_val] == "R" and PRECEDENCE[tok_val] < PRECEDENCE[top]):
                    out.append(stack.pop())
                else:
                    break
            stack.append(tok_val)
        elif tok_type == "LPAREN":
            stack.append("(")
        elif tok_type == "RPAREN":
            while stack and stack[-1] != "(":
                out.append(stack.pop())
            if not stack:
                raise ParseError("Mismatched parentheses")
            stack.pop()

    while stack:
        op = stack.pop()
        if op in ("(", ")"):
            raise ParseError("Mismatched parentheses")
        out.append(op)

    return out

# ---------------- Postfix Evaluation ----------------
def apply_op(op, stack):
    try:
        if op == "u-":
            a = float(stack.pop())
            stack.append(-a)
        elif op in {"+", "-", "*", "/", "^"}:
            b = float(stack.pop())
            a = float(stack.pop())
            if op == "+":
                stack.append(a + b)
            elif op == "-":
                stack.append(a - b)
            elif op == "*":
                stack.append(a * b)
            elif op == "/":
                if b == 0:
                    raise EvaluationError("Division by zero")
                stack.append(a / b)
            elif op == "^":
                stack.append(a ** b)
        else:
            raise EvaluationError(f"Unknown operator: {op}")
    except IndexError:
        raise ParseError("Insufficient operands")

def evaluate_postfix(postfix_tokens):
    stack = []
    for tok in postfix_tokens:
        if tok.replace('.', '', 1).isdigit() or (tok.startswith('.') and tok[1:].isdigit()):
            stack.append(tok)
        elif tok == "u-" or tok in {"+", "-", "*", "/", "^"}:
            apply_op(tok, stack)
        else:
            raise EvaluationError(f"Invalid token: {tok!r}")
    if len(stack) != 1:
        raise ParseError("Too many operands")
    return stack[0]

def evaluate(expr: str):
    postfix = infix_to_postfix(expr)
    result = evaluate_postfix(postfix)
    if abs(result - int(result)) < 1e-12:
        return int(result)
    return result

# ---------------- CLI / REPL ----------------
BANNER = "Expression Calculator (infix → postfix → evaluation). Type 'exit' to quit."

def repl():
    print(BANNER)
    while True:
        try:
            line = input("expr> ").strip()
        except EOFError:
            print()
            break
        if not line:
            continue
        if line.lower() in {"exit", "quit"}:
            break
        try:
            print(evaluate(line))
        except CalculatorError as e:
            print(f"Error: {e}")

def main():
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
        try:
            print(evaluate(expr))
        except CalculatorError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        repl()

if __name__ == "__main__":
    main()
