import sys
from toolkit.tokenizator import tokenize
from toolkit.calculator import pars_to_rpn, calculate

if __name__ == '__main__':
    arguments = sys.argv[1:]
    if arguments[0] == 'calc':
        tokens = tokenize(arguments[1:])
        rpn_tokens = pars_to_rpn(tokens)
        print(calculate(rpn_tokens))
