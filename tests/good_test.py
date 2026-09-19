import pytest
from decimal import Decimal
from src.toolkit.tokenizator import tokenize
from src.toolkit.calculator import pars_to_rpn, calculate
from src.toolkit.converter import convertation

# 1. Проверка калькулятора и приоритета операций
def test_calc_basic_math():
    rpn = pars_to_rpn(tokenize("2 + 3 * 4.5"))
    assert calculate(rpn) == Decimal('15.5')

# 2. Точность вычислений с помощью Decimal
def test_calc_decimal_precision():
    rpn = pars_to_rpn(tokenize("0.1 + 0.2"))
    assert calculate(rpn) == Decimal('0.3')

# 3. Унарный + и -
def test_calc_unary_operators():
    rpn = pars_to_rpn(tokenize("-5 + +3"))
    assert calculate(rpn) == Decimal('-2')

# 4. Игнорирование пробелов между токенами
def test_calc_spaces_ignored():
    rpn = pars_to_rpn(tokenize(" 10  /   2    - 1 "))
    assert calculate(rpn) == Decimal('4')

# 5. Регистр единиц измерения не учитывается
def test_convert_case_insensitivity():
    assert convertation('10', 'KG', 'g') == 10000.0

# 6. Конвертация единиц длины
def test_convert_length():
    assert convertation('150', 'cm', 'm') == 1.5

# 7. Конвертация температур + проверка на учет регистра
def test_convert_temperature():
    assert convertation('100', 'c', 'F') == 212.0