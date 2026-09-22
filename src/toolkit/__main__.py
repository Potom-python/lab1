import sys

from .calculator import calculate, pars_to_rpn
from .converter import convertation
from .tokenizator import tokenize


def main():
    command = sys.argv[1]
    if command == "":
        raise ValueError("Строка не должна быть пустой")
    if command == "calc":
        arguments = sys.argv[1:]
        tokens = tokenize(arguments[1:])
        rpn_tokens = pars_to_rpn(tokens)
        print(calculate(rpn_tokens))
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

        print(convertation(value, from_unit, to_unit))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(2)
