import sys

from .calculator import calculate, pars_to_rpn
from .converter import convertation
from .tokenizator import tokenize
import argparse


def format_float(a: float) -> str:
    """Форматирование вывода типа float"""
    return f"{a:.12f}".rstrip('0').rstrip('.')


def main():
    """Обработка CLI для дальнейшей загрузки значений в вычислительное ядро

    Работает с помощью argparse.
    calc: заносит в функцию calculate все аргументы
    введенные в консоль после calc, что делает необязательным ввод через командную строку вида:
    python -m toolkit calc "1+2". Теперь можно: python -m toolkit calc 1 + 2 +3+4 +1 - 7, далее выводит
    отформатированный результат выполнения функции
    --help: выводит справку по использованию калькулятора
    convert: выводит отформатированный результат выполнения функции
    """

    parser = argparse.ArgumentParser(description="Калькулятор и конвертер",
                                     epilog="Допустимые единицы\n"
                                            "mass: g, kg\n"
                                            "lens: mm cm m km\n"
                                            "t: K, F, C\n"
                                            "Использование:\n"
                                            "python -m toolkit calc <выражение>\n"
                                            "python -m toolkit convert <значение> "
                                            "--from <ед из которой переводишь> --to <ед, в которую перевести>",
                                     formatter_class=argparse.RawDescriptionHelpFormatter
                                     )
    subparsers = parser.add_subparsers(dest="command")
    calc_parser = subparsers.add_parser("calc")
    convert_parser = subparsers.add_parser("convert")
    calc_parser.add_argument("expression", nargs="+")
    convert_parser.add_argument("value")
    convert_parser.add_argument("--from", dest="from_unit", required=True)
    convert_parser.add_argument("--to", dest="to_unit", required=True)
    arguments = parser.parse_args()

    if arguments.command == "calc":
        tokens = tokenize(arguments.expression)
        rpn_tokens = pars_to_rpn(tokens)
        print(format_float(float(calculate(rpn_tokens))))
    elif arguments.command == "convert":
        print(format_float(float(convertation(arguments.value, arguments.from_unit, arguments.to_unit))))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{e.__class__} Ошибка: {e}", file=sys.stderr)
        sys.exit(2)
