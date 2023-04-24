import ply.yacc as yacc
from tokenizer import tokens

"""
Génération de la syntaxe Dumbo sur bae de la grammaire fournie dans l'énoncé.
"""
def p_programme(p):
    '''programme : txt
               | txt programme'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


parser = yacc.yacc(outputdir='generated')


def parse(input: str):
    return parser.parse(input, debug=False)
