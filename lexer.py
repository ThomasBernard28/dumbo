from ply import lex


def toToken(input: str):
    lexer = lex.lex()
    lexer.input(input)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens
