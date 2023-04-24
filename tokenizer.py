import ply.lex as lex

# tokens
tokens = (
    ### Tokens de base ###
    'ID',
    'QUOTE',
    'SEMICOLON',
    'COMMA',
    'DOT',
    'LPAREN',
    'RPAREN',
    'ASSIGN',
    'STRING',
    'DBLOCK_START',
    'DBLOCK_END',
    'TXT'
    #####################
)

""" Voir section 4.19 de la doc de PLY 'Conditional lexing and start condtions' 

http://www.dabeaz.com/ply/ply.html#ply_nn21

- L'état TEXT dans ce cas sert à éviter de prendre en compte les blocs de code dans les blocs de texte.
- Pour cela on peut de par la documentation définir des conditions de début d'état.
- On choisit inclusive pour garder les token déjà définis par défaut.
"""

states = (('CODE', 'inclusive'),('TEXT', 'inclusive'))

""" 
Les conditions sont définies ci dessus. On veut que lorsque l'on est dans l'état state et que l'on rencontre le token t_DBLOCK_START on passe dans l'état CODE. 
De la même manière on veut que lorsque l'on est dans l'état CODE et que l'on rencontre le token t_DBLOCK_END on passe dans l'état TEXT.
"""
def t_TEXT_DBLOCK_START(t):
    r'{{'
    t.lexer.begin('CODE')
    return t

def t_CODE_DBLOCK_END(t):
    r'}}'
    t.lexer.begin('TEXT')
    return t


### Regex tokens de base ###
t_TEXT_TXT = r"[^'{{}}]+"
t_CODE_SEMICOLON = r';'
t_CODE_COMMA = r','
t_CODE_DOT = r'\.'
t_CODE_ASSIGN = r':='
t_CODE_LPAREN = r'\('
t_CODE_RPAREN = r'\)'
############################


def t_CODE_ID(t):
    r'[a-zA-Z0-9_]+'
    return t

def t_CODE_STRING(t):
    r"'[^']*'"
    t.value = t.value[1:-1] #Sert à supprimer les guillemets autour de la chaîne
    return t

t_CODE_ignore = ' \t'
t_TEXT_ignore = ' \t\n'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '{}' at line {}".format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)


def tokenize(input: str):
    lexer = lex.lex()
    # On commence dans l'état TEXT car c'est le plus général.
    # Si on rencontre un bloc de code on passera dans l'état CODE.
    lexer.begin('TEXT')
    lexer.input(input)
    tokens = []
    for token in lexer:
        tokens.append((token.type, token.value))

    return tokens
