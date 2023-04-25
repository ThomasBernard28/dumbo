import ply.yacc as yacc
from tokenizer import tokens

"""
Génération de la syntaxe Dumbo sur bae de la grammaire fournie dans l'énoncé.
"""
def p_programme_txt(p):
    '''programme : TXT
               | TXT programme'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


def p_programme_dumbo(p):
    '''programme : dumbo_block
               | dumbo_block programme'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_dumbo_block(p):
    '''dumbo_block : DBLOCK_START expression_list DBLOCK_END
                   | DBLOCK_START DBLOCK_END'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_expression_list(p):
    '''expression_list : expression
                       | expression expression_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_expression_assign_stringexpr_or_stringlst(p):
    '''expression : ID ASSIGN stringexpr SEMICOLON
                  | ID ASSIGN stringlst SEMICOLON'''
    p[0] = (p[1], p[3])

def p_stringexpr(p):
    '''stringexpr : STRING
                  | ID
                  | stringexpr DOT stringexpr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[3])

def p_stringlst(p):
    '''stringlst : LPAREN stringlst_interior RPAREN'''
    if len(p) == 4:
        p[0] = p[2]

def p_stringlst_interior(p):
    '''stringlst_interior : stringexpr
                          | stringexpr COMMA stringlst_interior'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


parser = yacc.yacc(outputdir='generated')


def parse(input: str):
    return parser.parse(input, debug=False)
