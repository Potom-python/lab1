from decimal import Decimal, getcontext, ROUND_HALF_UP
from . import AbsoluteZeroError

getcontext().prec = 10
getcontext().rounding = ROUND_HALF_UP


def convertation(value, from_unit, to_unit):
    value = Decimal(value)
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    mass_coefficients = {
        'g': Decimal(1),
        'kg': Decimal(1000)
    }
    lens_coefficients = {
        'mm': Decimal(1),
        'cm': Decimal(10),
        'm': Decimal(1000),
        'km': Decimal(1000000)
    }

    result = None

    if (from_unit == 'k' and value < Decimal(0)) \
            or (from_unit == 'c' and value < Decimal('-273.15')) \
            or (from_unit == 'f' and value < Decimal('-469.67')):
        raise AbsoluteZeroError(f'Физически невозможная температура:'
                                f' {value} {from_unit} ниже абсолютного нуля')

    if from_unit in mass_coefficients:
        value = value * mass_coefficients[from_unit]
        if to_unit not in mass_coefficients:
            raise ValueError(f'Невозможно перевести из {from_unit} в {to_unit}')
        result = value / mass_coefficients[to_unit]
        return result
    if from_unit in lens_coefficients:
        value = value * lens_coefficients[from_unit]
        if to_unit not in lens_coefficients:
            raise ValueError(f'Невозможно перевести из {from_unit} в {to_unit}')
        result = value / lens_coefficients[to_unit]
        return result
    if from_unit == 'c':
        pass
    elif from_unit == 'f':
        value = (value - Decimal(32)) / Decimal('1.8')
    elif from_unit == 'k':
        value = value - Decimal('273.15')

    if to_unit == 'c':
        result = value
    elif to_unit == 'f':
        result = (value * Decimal('1.8')) + Decimal(32)
    elif to_unit == 'k':
        result = value + Decimal('273.15')
    else:
        raise ValueError(f'Невозможно перевести из {from_unit}'
                         f' в {to_unit} или {to_unit} нету в базе')

    if result is None:
        raise ValueError('Введена неверная единица измерения')

    return result.normalize()
