import ply.yacc as yacc
from tokenizer import tokens
from main import *

"""
Génération de la syntaxe fournie dans l'énoncé.
"""
def p_program(p):
    '''program : TXT
               | TXT program'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_program(p):
    '''program : dblock
                | dblock program'''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_dblock(p):
    '''dblock : DBLOCK_START expression_list DBLOCK_END
                | DBLOCK_START DBLOCK_END''' # In data3 we have a dblock with no expression_list

    if len(p) == 3:
        p[0] = []
    elif len(p) == 4:
        p[0] = p[2]

def p_expression_list(p):
    ''' expression_list : expression SEMICOLON expression_list
                        | expression SEMICOLON'''

def p_expression_print_string_expression(p):
    '''expression : PRINT string_expression'''

    if len(p) == 3:
        p[0] = ("print", p[2])

def p_expression_for_loops(p):
    '''expression : FOR VAR IN string_list DO expression_list ENDFOR
                    | FOR VAR IN VAR DO expression_list ENDFOR'''

    if len(p) == 8:
        p[0] = ("for", p[2], p[4], p[6])

def p_expression_assign(p):
    '''expression : VAR ASSIGN string_expression
                    | VAR ASSIGN string_list
                    | VAR ASSIGN num_expression'''

    if len(p) == 4:
        p[0] = ("assign", p[1], p[3])

def p_string_expression(p):
    '''string_expression : STRING
                         | VAR
                         | string_expression DOT string_expression'''

    if len(p) == 2:
        if p[1][0] == '\'':
            p[0] = p[1]
        else:
            p[0] = p[1]
    elif len(p) == 4:
        p[0] = ("concat", p[1], p[3])

def p_string_list(p):
    '''string_list : LPAREN string_list_interior RPAREN'''

    if len(p) == 4:
        p[0] = p[2]

def p_string_list_interior(p):
    '''string_list_interior : string_expression COMMA string_list_interior
                            | STRING'''

def p_num_expression(p):
    '''num_expression : NUMBER
                      | VAR
                      | num_expression PLUS num_expression
                      | num_expression MINUS num_expression
                      | num_expression TIMES num_expression
                      | num_expression DIVIDE num_expression'''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[2], p[1], p[3])


precedence = (
    ('left', 'PLUS'),
    ('left', 'MINUS'),
    ('left', 'TIMES'),
    ('left', 'DIVIDE'),
    ('left', 'DOT')
)

def p_error(p):
    print("Syntax error in line {}".format(p.lineno))
    print("Illegal character '%s'" % p.value[0])


parser = yacc.yacc(outputdir='output')


def parse(input: str):
    return parser.parse(input, debug=False)

