from . import AbsoluteZeroError


def convertation(value, from_unit, to_unit):
    value = float(value)

    mass_coefficients = {
        'g': 1.0,
        'kg': 1000.0
    }
    lens_coefficients = {
        'mm': 1.0,
        'cm': 10.0,
        'm': 1000.0,
        'km': 1000000.0
    }

    result = None

    if (from_unit == 'k' and value < 0) or (from_unit == 'c' and value < -273.15) or (
            from_unit == 'f' and value < -459.67):
        raise AbsoluteZeroError(f'Физически невозможная температура: {value} {from_unit} ниже абсолютного нуля')

    if from_unit in mass_coefficients.keys():
        value = value * mass_coefficients[from_unit]
        if to_unit not in mass_coefficients.keys():
            raise ValueError(f'Невозможно перевести из {from_unit} в {to_unit}')
        result = value / mass_coefficients[to_unit]
        return result
    elif from_unit in lens_coefficients.keys():
        value = value * lens_coefficients[from_unit]
        if to_unit not in lens_coefficients.keys():
            raise ValueError(f'Невозможно перевести из {from_unit} в {to_unit}')
        result = value / lens_coefficients[to_unit]
        return result
    elif from_unit == 'c':
        pass
    elif from_unit == 'f':
        value = (value - 32) / 1.8
    elif from_unit == 'k':
        value = value - 273.15

    if to_unit == 'c':
        result = value
    elif to_unit == 'f':
        result = (value * 1.8) + 32
    elif to_unit == 'k':
        result = value + 273.15
    else:
        raise ValueError(f'Невозможно перевести из {from_unit} в {to_unit} или {to_unit} нету в базе')

    if result is None:
        raise ValueError('Введена неверная единица измерения')

    return result
