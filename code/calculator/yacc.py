from lexer import tokens  # NOQA
import ply.yacc as yacc


def p_expression_plus(p):
    '''
    expression : expression '+' term
    '''
    p[0] = p[1] + p[3]


def p_expression_minus(p):
    '''
    expression : expression '-' term
    '''
    p[0] = p[1] - p[3]


def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]


def p_term_times(p):
    '''
    term : term '*' factor
    '''
    p[0] = p[1] * p[3]


def p_term_div(p):
    '''
    term : term '/' factor
    '''
    return p[1] / p[3]


def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]


def p_factor_num(p):
    '''
    factor : NUMBER
    '''
    p[0] = p[1]


parser = yacc.yacc()
