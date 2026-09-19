from decimal import Decimal, getcontext, ROUND_HALF_UP

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_UP

def pars_to_rpn(tokens):
    prioritets = {
        '+': 1, '-': 1, '*': 2, '/': 2, 'UN+': 3, 'UN-': 3
    }
    stack = []
    output = []
    for name, value in tokens:
        if name == 'NUMBER':
            output.append((name, value))
        elif 'OP' in name:
            op_key = f'UN{value}' if name == 'UNAROP' else value
            while stack:
                top_name, top_value = stack[-1]
                top_key = f'UN{top_value}' if top_name == 'UNAROP' else top_value
                if prioritets[top_key] >= prioritets[op_key]:
                    output.append(stack.pop())
                else:
                    break
            stack.append((name, value))
    while stack:
        output.append(stack.pop())
    return output


def calculate(rpn_tokens):
    calc_stack = []
    for name, value in rpn_tokens:
        if name == 'NUMBER':
            calc_stack.append(Decimal(value))
        elif name == 'UNAROP':
            if value == '+':
                pass
            elif value == '-':
                number = calc_stack.pop()
                calc_stack.append(-number)
        else:
            if len(calc_stack) < 2:
                raise ValueError("Пропущен операнд в выражении")
            a = calc_stack.pop()
            b = calc_stack.pop()
            if value == '+':
                calc_stack.append(a + b)
            elif value == '-':
                calc_stack.append(b - a)
            elif value == '*':
                calc_stack.append(a * b)
            elif value == '/':
                if a == Decimal(0):
                    raise ValueError('Деление на 0 недопустимо')
                calc_stack.append(b / a)

    return calc_stack[0].normalize()
