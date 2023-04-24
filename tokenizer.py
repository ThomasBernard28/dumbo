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
    #####################
)



### Regex tokens de base ###
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_ASSIGN = r':='
t_LPAREN = r'\('
t_RPAREN = r'\)'
############################


def t_ID(t):
    r'[a-zA-Z0-9_]+'
    return t

def t_STRING(t):
    r"'[^']*'"
    t.value = t.value[1:-1] #Sert à supprimer les guillemets autour de la chaîne
    return t
def t_DBLOCK_START(t):
    r'{{'
    return t

def t_DBLOCK_END(t):
    r'\}\}'
    return t

t_ignore = ' \t\r\n'

def t_error(t):
    print(f"error : {t.value[0]}")
    t.lexer.skip(1)


def tokenize(input: str):
    lexer = lex.lex()
    lexer.input(input)
    tokens = []
    for token in lexer:
        tokens.append((token.type, token.value))

    return tokens
