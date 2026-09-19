from re import *

from toolkit.errors import ConsecutiveOperatorsError


def tokenize(expression):
    if type(expression) is list:
        expression = ''.join(expression)
    if expression[0] == '.':
        raise ValueError('Выражение не может начинаться с точки')
    rules = [
        ('NUMBER', '\d+(\.\d+)?'),
        ('OP', '[+-/*]'),
        ('RANDSYM', '.')
    ]

    tokens = []
    pattern = '|'.join(f'(?P<{name}>{rule})' for name, rule in rules)
    last_name = None
    count_near_op = 0
    for foldable in finditer(pattern, expression):
        name = foldable.lastgroup
        value = foldable.group()

        if value.isspace():
            continue
        if name == 'RANDSYM':
            raise ValueError(f'Недопустимый символ: {value}')

        if name == 'OP':
            if (last_name is None or last_name == 'OP'):
                name = 'UNAROP'
            count_near_op += 1
        else:
            count_near_op = 0
        if count_near_op >= 3:
            raise ConsecutiveOperatorsError('Недопустимое кол-во подряд идущих операторов')
        last_name = name
        tokens.append((name, value))

    return tokens
