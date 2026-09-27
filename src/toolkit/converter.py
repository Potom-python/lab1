import json
import os
from decimal import ROUND_HALF_UP, Decimal, getcontext

from .errors import AbsoluteZeroError

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_UP


def convertation(value: str, from_unit: str, to_unit: str) -> Decimal:
    """Конвертирует из одной величины в другую

    Сначала проверяются from_unit и to_unit на правильность, после чего начинается основная стадия.
    В случае масс и длин реализован с помощью словаря (берется из файла convert_coef.json),
    в котором есть какая-то базовая единица, в которую переводится
    переданная, после чего конвертируется в уже нужную умножая базовую на значение нужной в словаре.
    В случае с температурой реализовано с помощью if, elif, else и формул, по которым опять же переданная единица
    переводится в базовую и уже из нее с помощью другой формулы переводится в нужную.
    """
    value = Decimal(value)
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    ed_mass = ("kg", "g")
    ed_temp = ("c", "f", "k")
    ed_lens = ('mm', 'cm', 'm', 'km')

    os_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(os_directory, 'convert_coef.json')
    with open(file_path, 'r') as f:
        coefficients = json.load(f)

    result = None

    if (
            (from_unit == "k" and value < Decimal(0))
            or (from_unit == "c" and value < Decimal("-273.15"))
            or (from_unit == "f" and value < Decimal("-469.67"))
    ):
        raise AbsoluteZeroError(
            f"Физически невозможная температура:"
            f" {value}{from_unit.upper()} ниже абсолютного нуля"
        )
    if from_unit not in coefficients and from_unit not in ed_temp:
        raise ValueError(f"Неизвестная единица {from_unit}")
    if to_unit not in coefficients and to_unit not in ed_temp:
        raise ValueError(f"Неизвестная единица {to_unit}")

    if from_unit in ed_temp and to_unit not in ed_temp:
        raise ValueError(f"Невозможно перевести из {from_unit} в {to_unit}")
    elif from_unit in ed_mass and to_unit not in ed_mass:
        raise ValueError(f"Невозможно перевести из {from_unit} в {to_unit}")
    elif from_unit in ed_lens and to_unit not in ed_lens:
        raise ValueError(f"Невозможно перевести из {from_unit} в {to_unit}")

    if from_unit in coefficients:
        value = value * Decimal(coefficients[from_unit])
        result = value / Decimal(coefficients[to_unit])
        return result

    if from_unit == "c":
        pass
    elif from_unit == "f":
        value = (value - Decimal(32)) / Decimal("1.8")
    elif from_unit == "k":
        value = value - Decimal("273.15")

    if to_unit == "c":
        result = value
    elif to_unit == "f":
        result = (value * Decimal("1.8")) + Decimal(32)
    elif to_unit == "k":
        result = value + Decimal("273.15")
    else:
        raise ValueError(
            f"Невозможно перевести из {from_unit} в {to_unit} или {to_unit} нету в базе"
        )

    if result is None:
        raise ValueError("Введена неверная единица измерения")

    return result.normalize()
