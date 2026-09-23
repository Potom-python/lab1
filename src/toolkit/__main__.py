import sys

from .calculator import calculate, pars_to_rpn
from .converter import convertation
from .tokenizator import tokenize


def format_float(a: float) -> str:
    """Форматирование вывода типа float"""
    return f"{a:.10f}".rstrip('0').rstrip('.')


def main():
    """Обработка CLI для дальнейшей загрузки значенйи в вычислительное ядро

    Обрабатывает sys.argv 1 эл. всегда явл командой.
    calc: заносит в функцию calculate все аргументы
    введенные в консоль после calc, что делает необязательным ввод через командную строку вида:
    python -m toolkit calc "1+2". Теперь можно: python -m toolkit calc 1 + 2 +3+4 +1 - 7, далее выводит
    отформатированный результат выполнения функции
    --help: выводит справку по использованию калькулятора, заканчивается с кодом возврата 0
    convert: обрабатывает все аргументы после convert, проверяет длину, чтобы удостоверится
    в корректном использовании команды. Далее создает словарь флаг: значение и вносит значения в функцию.
    Далее выводит отформатированный результат выполнения функции
    """
    command = sys.argv[1]
    if command == "":
        raise ValueError("Строка не должна быть пустой")
    if command == "calc":
        arguments = sys.argv[1:]
        tokens = tokenize(arguments[1:])
        rpn_tokens = pars_to_rpn(tokens)
        print(format_float(float(calculate(rpn_tokens))))
    elif command == "--help":
        print("Калькулятор и конвертер")
        print("Допустимые единицы")
        print("mass: g, kg")
        print("lens: mm cm m km")
        print("t: K, F, C")
        print("Использование:")
        print("python -m toolkit calc выражение")
        print(
            "python -m toolkit convert <значение> "
            "--from <ед из которой переводишь> --to <ед, в которую перевести>"
        )
        sys.exit(0)
    elif command == "convert":
        arguments = sys.argv[1:]
        if len(arguments) != 6:
            raise ValueError("Неверное количество команд или значений")
        try:
            value = arguments[1]
            args_pars = {arguments[2]: arguments[3], arguments[4]: arguments[5]}
            from_unit = args_pars["--from"]
            to_unit = args_pars["--to"]
        except Exception:
            raise ValueError("Неверно указаны параметры --from или --to")

        print(format_float(float(convertation(value, from_unit, to_unit))))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{e.__class__} Ошибка: {e}", file=sys.stderr)
        sys.exit(2)
