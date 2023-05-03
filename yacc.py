import ply.yacc as yacc
from lexer import tokens

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
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]

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
        p[0] = ("assemble", p[1], p[3]) #Assemble the two strings thanks to ply syntax section 6.10

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
                | VAR ASSIGN string_list'''
    p[0] = ("assign", p[1], p[3])

def p_expression_number(p):
    '''number : NUMBER
              | NUMBER PLUS NUMBER
              | NUMBER MINUS NUMBER
              | NUMBER TIMES NUMBER
              | NUMBER DIVIDE NUMBER'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == 'PLUS':
            p[0] = p[1] + p[3]
        if p[2] == 'MINUS':
            p[0] = p[1] - p[3]
        if p[2] == 'TIMES':
            p[0] = p[1] * p[3]
        if p[2] == 'DEVIDE':
            p[0] = int(p[1] / p[3])

def p_expression_boolean(p):
    '''boolean : boolean OR boolean
               | boolean AND boolean
               | number BIGGER number
               | number LOWER number
               | number EQUALS number
               | number DIFFERENT number
               | TRUE
               | FALSE'''
    if len(p) == 2:
        p[0] = p[1] == 'TRUE'
    else:
        p[0] = ("boolean", p[1], p[2], p[3])

def p_expression_if(p):
    '''expression_list : IF boolean DO expression_list ENDIF'''
    p[0] = ("if", p[2], p[4])

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

def p_error(p):
    print("Syntax error in line {}".format(p.lineno))
    print("Illegal character '%s'" % p.value[0])

parser = yacc.yacc(outputdir='output')

precedence = (
    ('left', 'DOT')
)

def parse(input: str):
    return parser.parse(input, debug=False)

