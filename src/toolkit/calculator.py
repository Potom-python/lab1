from decimal import ROUND_HALF_UP, Decimal, getcontext

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_UP


def pars_to_rpn(tokens: list) -> list:
    """ С помощью алгоритма ОПН возвращает список токенов для дальнейшего вычисления выражения

    Проходит по списку токенов, если это число, то сразу добавляет в output, если это операция, то создает ключ
    для сверки приоритетов из словаря. Начинается цикл while,
    если приоритет последней операции в стеке >= приоритета обрабатываемой операции, то добавляет последнюю
    из операций в output, в ином случае завершает работу цикла.
    После цикла операция добавляется в стек.
    """
    prioritets = {"+": 1, "-": 1, "*": 2, "/": 2, "UN+": 3, "UN-": 3}
    stack = []
    output = []
    for name, value in tokens:
        if name == "NUMBER":
            output.append((name, value))
        elif "OP" in name:
            op_key = f"UN{value}" if name == "UNAROP" else value
            while stack:
                top_name, top_value = stack[-1]
                top_key = f"UN{top_value}" if top_name == "UNAROP" else top_value
                if prioritets[top_key] >= prioritets[op_key]:
                    output.append(stack.pop())
                else:
                    break
            stack.append((name, value))
    while stack:
        output.append(stack.pop())
    return output


def calculate(rpn_tokens: list) -> Decimal:
    """Вычисляет значение выражение переданного в консоли на основе токенов ОПН

    Обрабатывает рпн токены, добавляет в стек числа, как только встречает операцию, то производит с последними 2
    числами из стека определенную операцию. Результат добавляет обратно в стек. В конце в стеке останется только 1
    элемент, являющийся значением, полученным из выражения, и возвращает его.
    """
    calc_stack = []
    for name, value in rpn_tokens:
        if name == "NUMBER":
            calc_stack.append(Decimal(value))
        elif name == "UNAROP":
            if value == "+":
                pass
            elif value == "-":
                number = calc_stack.pop()
                calc_stack.append(-number)
        else:
            if len(calc_stack) < 2:
                raise ValueError("Пропущен операнд в выражении")
            a = calc_stack.pop()
            b = calc_stack.pop()
            if value == "+":
                calc_stack.append(a + b)
            elif value == "-":
                calc_stack.append(b - a)
            elif value == "*":
                calc_stack.append(a * b)
            elif value == "/":
                if a == Decimal(0):
                    raise ValueError("Деление на 0 недопустимо")
                calc_stack.append(b / a)

    return calc_stack[0].normalize()
