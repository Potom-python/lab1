import sys
from . import tokenize, pars_to_rpn, calculate, convertation

if __name__ == '__main__':
    command = sys.argv[1]
    if command == '':
        raise ValueError('Строка не должна быть пустой')
    if command == 'calc':
        arguments = sys.argv[1:]
        tokens = tokenize(arguments[1:])
        rpn_tokens = pars_to_rpn(tokens)
        print(calculate(rpn_tokens))
    if command == 'convert':
        arguments = sys.argv[1:]
        if len(arguments) != 6:
            raise ValueError('Неверное количество команд или значений')
        args_pars = {
            arguments[2]: arguments[3],
            arguments[4]: arguments[5]
        }
        print(convertation(arguments[1], args_pars['--from'], args_pars['--to']))