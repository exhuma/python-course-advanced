from lexer import lexer


# Test it out
data = '''
3 + 4 * 10
  + -20 *2
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
for token in lexer:
    print(token.type, token.value, token.lineno, token.lexpos)
