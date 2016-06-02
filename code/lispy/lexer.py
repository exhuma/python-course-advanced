import ply.lex as lex


class Lilex(object):

    literals = '+-*/'
    reserved = {
        'define': 'DEFINE',
        'begin': 'BEGIN',
    }

    # List of token names.   This is always required
    tokens = [
        'ID',
        'INTEGER',
        'FLOAT',
        'LPAREN',
        'RPAREN',
    ] + list(reserved.values())

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ignore = ' \t'

    def t_FLOAT(self, t):
        r'[0-9]+\.[0-9]+'
        return t

    def t_INTEGER(self, t):
        r'[0-9]+'
        return t

    def t_ID(self, t):
        r'[a-zA-Z0-9_]+'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        '''
        Error handling rule
        '''
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, *args, **kwargs):
        '''
        Builds the lexer
        '''
        self.lexer = lex.lex(module=self, *args, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        for token in self.lexer:
            print(token)

if __name__ == '__main__':
    lilex = Lilex()
    lilex.build()
    lilex.test('(begin (define r 10) (* pi (* r r)))')
