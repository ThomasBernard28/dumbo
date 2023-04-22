import ply.yacc as yacc
from tokenizer import tokens


def p_expression_dumboblock(p):
    '''expression : LBRACE LBRACE expression_list RBRACE RBRACE'''
    p[0] = p[3]


def p_expression_list(p):
    '''expression_list : expression SEMICOLON expression_list
                       | expression'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_expression_id(p):
    '''expression : ID'''
    p[0] = p[1]


parser = yacc.yacc(outputdir='generated')


def parse(input: str):
    return parser.parse(input, debug=False)
