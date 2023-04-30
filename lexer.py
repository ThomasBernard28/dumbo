from ply import lex

# Reserved keywords
reserved = {
    'print' : 'PRINT',
    'for'   : 'FOR',
    'in'    : 'IN',
    'do'    : 'DO',
    'endfor': 'ENDFOR',
    'if'    : 'IF',
    'endif' : 'ENDIF',
    'true'  : 'TRUE',
    'false' : 'FALSE',
    'or'    : 'OR',
    'and'   : 'AND'
}
#tokens
tokens = [
    'TXT',
    'DBLOCK_START',
    'DBLOCK_END',
    'VAR',
    'ASSIGN',
    'LPAREN',
    'STRING',
    'RPAREN',
    'SEMICOLON',
    'COMMA',
    'DOT',
    'QUOTE',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE'
] + list(reserved.values())


""" Voir section 4.19 de la doc de PLY 'Conditional lexing and start condtions' 
Grâce à cette section on peut définir des états pour le lexer.
http://www.dabeaz.com/ply/ply.html#ply_nn21
- L'état TEXT correspond à l'état par défaut. (i.e en dehors des blocs de code Dumbo)
- Pour cela on peut de par la documentation définir des conditions de début d'état.
"""

states = (
    ('TEXT', 'exclusive'),
    ('CODE', 'exclusive')
)

def t_TEXT_TXT(t):
    r'[^{]+'
    return t

""" 
Les conditions sont définies ci-dessous. On veut que lorsque l'on est dans l'état TEXT et que l'on rencontre le token DBLOCK_START on passe dans l'état CODE. 
De la même manière on veut que lorsque l'on est dans l'état CODE et que l'on rencontre le token DBLOCK_END on passe dans l'état TEXT.
"""
def t_TEXT_DBLOCK_START(t):
    r'{{'
    t.lexer.begin('CODE')
    return t

def t_CODE_DBLOCK_END(t):
    r'}}'
    t.lexer.begin('TEXT')
    return t

def t_CODE_VAR(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VAR')
    return t

def t_CODE_ASSIGN(t):
    r':='
    return t

def t_CODE_LPAREN(t):
    r'\('
    return t

def t_CODE_STRING(t):
    r"'[^']*'"
    t.value = t.value[1:-1] #Pour supprimer les guillemets autour de la chaîne.
    return t

def t_CODE_COMMA(t):
    r','
    return t

def t_CODE_DOT(t):
    r'\.'
    return t

def t_CODE_RPAREN(t):
    r'\)'
    return t

def t_CODE_SEMICOLON(t):
    r';'
    return t

def t_CODE_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CODE_PLUS(t):
    r'\+'
    return t

def t_CODE_MINUS(t):
    r'\-'
    return t

def t_CODE_TIMES(t):
    r'\*'
    return t

def t_CODE_DIVIDE(t):
    r'/'
    return t

t_CODE_ignore = ' \t\n'
t_TEXT_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineo += len(t.value)

def t_error(t):
    print("Illegal character '{}' at line {}".format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)

def t_TEXT_error(t):
    print("Illegal character '{}' at line {}".format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)

def t_CODE_error(t):
    print("Illegal character '{}' at line {}".format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)

lexer = lex.lex()
lexer.begin('TEXT')

def toToken(input: str):
    lexer = lex.lex()
    lexer.begin('TEXT')
    lexer.input(input)
    tokens = []
    for token in lexer:
        tokens.append((token.type, token.value))
    return tokens
