"""Integer expression calculator: tokenize -> to_rpn (shunting-yard) -> eval_rpn."""

BINARY = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 4}
NEG_PREC = 3
RIGHT_ASSOC = {"^"}


def tokenize(text):
    tokens = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit():
            num = 0
            while i < n and text[i].isdigit():
                num = num * 10 + int(text[i])
                i += 1
            tokens.append(num)
            continue
        if ch == "-":
            prev = tokens[-1] if tokens else None
            if prev is None or prev == "(" or prev == "neg" or prev in BINARY:
                tokens.append("neg")
            else:
                tokens.append("-")
            i += 1
            continue
        if ch in BINARY or ch in "()":
            tokens.append(ch)
            i += 1
            continue
        raise ValueError("unexpected character: %r" % ch)
    return tokens


def _prec(op):
    if op == "neg":
        return NEG_PREC
    return BINARY[op]


def to_rpn(tokens):
    output = []
    stack = []
    for tok in tokens:
        if isinstance(tok, int):
            output.append(tok)
        elif tok == "neg":
            stack.append(tok)
        elif tok in BINARY:
            while stack and stack[-1] != "(":
                top = stack[-1]
                if _prec(top) > _prec(tok) or (
                    _prec(top) == _prec(tok) and tok not in RIGHT_ASSOC
                ):
                    output.append(stack.pop())
                else:
                    break
            stack.append(tok)
        elif tok == "(":
            stack.append(tok)
        elif tok == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("unbalanced ')'")
            stack.pop()
        else:
            raise ValueError("bad token: %r" % (tok,))
    while stack:
        top = stack.pop()
        if top == "(":
            raise ValueError("unbalanced '('")
        output.append(top)
    return output


def _apply(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("division by zero")
        q = abs(a) // abs(b)
        return q if (a < 0) == (b < 0) else -q
    if op == "%":
        if b == 0:
            raise ZeroDivisionError("modulo by zero")
        r = abs(a) % abs(b)
        return r if a >= 0 else -r
    if op == "^":
        if b < 0:
            raise ValueError("negative exponent")
        return a ** b
    raise ValueError("bad operator: %r" % op)


def eval_rpn(rpn):
    stack = []
    for tok in rpn:
        if isinstance(tok, int):
            stack.append(tok)
        elif tok == "neg":
            if not stack:
                raise ValueError("missing operand")
            stack.append(-stack.pop())
        else:
            if len(stack) < 2:
                raise ValueError("missing operand")
            b = stack.pop()
            a = stack.pop()
            stack.append(_apply(tok, a, b))
    if len(stack) != 1:
        raise ValueError("malformed expression")
    return stack[0]


def evaluate(text):
    return eval_rpn(to_rpn(tokenize(text)))
