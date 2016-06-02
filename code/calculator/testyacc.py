from yacc import parser

while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        print ''
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
