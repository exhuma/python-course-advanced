import math

import ply.yacc as yacc

from lexer import Lilex


class LispParser(object):

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.tokens = tokenizer.tokens  # needed by PLY
        self.env = self.default_env()

    def default_env(self):
        return {
            'pi': math.pi
        }

    def p_expression(self, p):
        '''
        expression : LPAREN reserved atom atom RPAREN
                   | LPAREN operator atom atom RPAREN
        '''
        p[0] = ('expression', p[2], p[3], p[4])

    def p_atom(self, p):
        '''
        atom : ID
             | INTEGER
             | expression
        '''
        p[0] = ('atom', p[1])

    def p_reserved(self, p):
        '''
        reserved : DEFINE
                 | BEGIN
        '''
        p[0] = ('reserved', p[1])

    def p_operator(self, p):
        '''
        operator : '+'
                 | '-'
                 | '*'
                 | '/'
        '''
        p[0] = ('op', p[1])

    def build(self, *args, **kwargs):
        self.parser = yacc.yacc(module=self, *args, **kwargs)

    def parse(self, data):
        return self.parser.parse(data, lexer=self.tokenizer.lexer)


if __name__ == '__main__':
    from pprint import pprint
    tokenizer = Lilex()
    tokenizer.build()
    parser = LispParser(tokenizer)
    parser.build()
    result = parser.parse('(begin (define r 10) (* pi (* r r)))')
    pprint(result)
