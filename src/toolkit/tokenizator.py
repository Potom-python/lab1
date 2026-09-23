from re import finditer

from .errors import ConsecutiveOperatorsError


def tokenize(expression: str | list) -> list:
    """Разбивает числа и операции на токены для дальнейшей обработки

    Проверяет корректность введенного выражения, после начинает его обработку.
    Работает на основе регулярных выражений, которые ищут числа, операции и некорректные символы.
    Пробегается по всем найденным объектам по правилам, описанным в регулярках, если идет вторая подряд операция или
    до этой операции уже была другая => операуия унарная. Ведет подсчет + и -, * и / для вызова исключения.
    """
    if type(expression) is list:
        expression = "".join(expression)
    if not expression:
        raise SyntaxError("Выражение не должно быть пустым")
    if expression[0] == ".":
        raise ValueError("Выражение не может начинаться с точки")
    rules = [("NUMBER", r"\d+(\.\d+)?"), ("OP", r"[+-/*]"), ("RANDSYM", r".")]

    tokens = []
    pattern = "|".join(f"(?P<{name}>{rule})" for name, rule in rules)
    last_name = None
    count_plus_and_minus = 0
    count_multip_division = 0
    for foldable in finditer(pattern, expression):
        name = foldable.lastgroup
        value = foldable.group()

        if value.isspace():
            continue
        if name == "RANDSYM":
            raise ValueError(f"Недопустимый символ: {value}")

        if name == "OP":
            if last_name is None or last_name == "OP":
                name = "UNAROP"
            if value in "+-":
                count_plus_and_minus += 1
            else:
                count_multip_division += 1

        else:
            count_plus_and_minus = 0
            count_multip_division = 0
        if count_plus_and_minus >= 3 or count_multip_division >= 2:
            raise ConsecutiveOperatorsError(
                "Недопустимое кол-во подряд идущих операторов"
            )
        last_name = name
        tokens.append((name, value))

    return tokens
