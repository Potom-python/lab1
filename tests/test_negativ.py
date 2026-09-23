import pytest

from src.toolkit.calculator import calculate, pars_to_rpn
from src.toolkit.converter import convertation
from src.toolkit.errors import AbsoluteZeroError, ConsecutiveOperatorsError
from src.toolkit.tokenizator import tokenize


# 1. Пустое выражение
def test_empty_expression():
    with pytest.raises(SyntaxError, match="Выражение не должно быть пустым"):
        tokenize("")


# 2. Недопустимый символ в выражении
def test_invalid_character():
    with pytest.raises(ValueError, match="Недопустимый символ"):
        tokenize("2 + a")


# 3. Два оператора подряд
def test_neg_consecutive_operators():
    with pytest.raises(ConsecutiveOperatorsError):
        tokenize("5 * * 3")


# 4. Деление на 0
def test_division_by_zero():
    with pytest.raises(ValueError, match="Деление на 0 недопустимо"):
        calculate(pars_to_rpn(tokenize("5 / 0")))


# 5. Температура ниже абсолютного нуля
def test_absolute_zero():
    with pytest.raises(AbsoluteZeroError):
        convertation("-300", "c", "k")


# 6. Несовместимые группы перевода
def test_incompatible_units():
    with pytest.raises(ValueError, match="Невозможно перевести"):
        convertation("10", "kg", "m")
