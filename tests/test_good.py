from decimal import Decimal

from src.toolkit.calculator import calculate, pars_to_rpn
from src.toolkit.converter import convertation
from src.toolkit.tokenizator import tokenize


# 1. Проверка калькулятора и приоритета операций
def test_calc_basic_math():
    rpn = pars_to_rpn(tokenize("2 + 3 * 4.5"))
    assert calculate(rpn) == Decimal("15.5")


# 2. Точность вычислений с помощью Decimal
def test_calc_decimal_precision():
    rpn = pars_to_rpn(tokenize("0.1 + 0.2"))
    assert calculate(rpn) == Decimal("0.3")


# 3. Унарный + и -
def test_calc_unary_operators():
    rpn = pars_to_rpn(tokenize("-5 + +3"))
    assert calculate(rpn) == Decimal(-2)


# 4. Игнорирование пробелов между токенами
def test_calc_spaces_ignored():
    rpn = pars_to_rpn(tokenize(" 10  /   2    - 1 "))
    assert calculate(rpn) == Decimal(4)


# 5. Проверка деления с большим кол-вом нулей
def test_calc_format_float():
    rpn = pars_to_rpn(tokenize("1 / 1000000000 "))
    assert calculate(rpn) == Decimal("0.000000001")


# 6. Проверка вычислений больших чисел
def test_calc_large_expression():
    rpn = pars_to_rpn(tokenize('-12 * 12312 + 53242 - 742 + 432 * 5 - 8 + 7876 - 1234 / 2'))
    assert calculate(rpn) == Decimal(-85833)


# 7. Регистр единиц измерения не учитывается
def test_convert_case_insensitivity():
    assert convertation("10", "KG", "g") == Decimal('10000')


# 8. Конвертация единиц длины
def test_convert_length():
    assert convertation("150", "cm", "m") == Decimal('1.5')


# 9. Конвертация температур + проверка на учет регистра
def test_convert_temperature():
    assert convertation("100", "c", "F") == Decimal('212')
