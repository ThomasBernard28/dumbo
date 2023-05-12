import ply.yacc as yacc
from tokenizer import tokens

"""
Génération de la syntaxe fournie dans l'énoncé.
"""

def p_program_txt(p):
    '''program : TXT
               | TXT program'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]

def p_program_dumbo(p):
    '''program : dumbo_block
               | dumbo_block program'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]

def p_dumbo_block_expression_list(p):
    '''dumbo_block : DBLOCK_START expression_list DBLOCK_END
                    | DBLOCK_START DBLOCK_END''' #Just in case it's an empty block
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = []

def p_expression_list(p):
    '''expression_list : expression SEMICOLON
                       | expression SEMICOLON expression_list'''
    if len(p) == 3:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]

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
        p[0] = ("concat", p[1], p[3]) #Assemble the two strings thanks to ply syntax section 6.10

def p_expression_print(p):
    '''expression : PRINT string_expression'''
    p[0] = ("print", p[2])


def p_expression_for(p):
    '''expression : FOR VAR IN string_list DO expression_list ENDFOR
          | FOR VAR IN VAR DO expression_list ENDFOR'''

    if len(p) == 8:
        p[0] = ("for", p[2], p[4], p[6])

def p_expression_assign(p):
    '''expression : VAR ASSIGN string_expression
                | VAR ASSIGN string_list
                | VAR ASSIGN numerical_expression
                | VAR ASSIGN boolean_expression'''
    p[0] = ("assign", p[1], p[3])

def p_string_list(p):
    '''string_list : LPAREN string_list_interior RPAREN'''
    p[0] = p[2]

def p_string_list_interior(p):
    '''string_list_interior : STRING
                            | STRING COMMA string_list_interior'''

    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]

def p_numerical_expression(p):
    '''numerical_expression : numerical_expression PLUS numerical_term
                            | numerical_expression MINUS numerical_term
                            | numerical_term
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ("math_op", p[1], p[2], p[3])

def p_numerical_term(p):
    '''
    numerical_term : numerical_term TIMES numerical_base
                   | numerical_term DIVIDE numerical_base
                   | numerical_base
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ("math_op", p[1], p[2], p[3])

def p_numerical_base(p):
    '''
    numerical_base : NUMBER
                   | numerical_var
    '''
    p[0] = p[1]

def p_numerical_var(p):
    '''
    numerical_var : VAR
    '''
    p[0] = p[1]

def p_boolean_expression(p):
    '''
    boolean_expression : 
                       | boolean_expression OR boolean_expression
                       | boolean_and_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("bool_op", p[1], p[2], p[3])

def p_boolean_and_expression(p):
    '''
    boolean_and_expression : boolean_comparison
                           | TRUE
                           | FALSE
                           | boolean_and_expression AND boolean_and_expression
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("bool_op", p[1], p[2], p[3])

def p_boolean_comparison(p):
    '''
    boolean_comparison : numerical_expression BIGGER numerical_expression
                       | numerical_expression LOWER numerical_expression
                       | numerical_expression EQUALS numerical_expression
                       | numerical_expression DIFFERENT numerical_expression
    '''
    p[0] = ("bool_comp", p[1], p[2], p[3])

def p_if_expression(p):
    '''
    expression : IF boolean_expression DO expression_list ENDIF
    '''
    p[0] = ("if", p[2], p[4])

precedence = (
    ('left', 'PLUS'),
    ('left', 'MINUS'),
    ('left', 'TIMES'),
    ('left', 'DIVIDE'),
    ('left', 'AND'),
    ('left', 'OR'),
    ('right', 'DOT'),
)

def p_error(p):
    print("Syntax error in line {}".format(p.lineno))
    print("Illegal character '%s'" % p.value[0])

parser = yacc.yacc(outputdir='output')


def parse(input: str):
    return parser.parse(input, debug=False)

