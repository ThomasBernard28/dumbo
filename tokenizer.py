import ply.lex as lex

# tokens
tokens = (
    'ID',
    'LBRACE',
    'RBRACE',
    'QUOTE',
    'SEMICOLON',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'ASSIGN',
    'STRING',
)

# regex
t_QUOTE = '\''
t_SEMICOLON = r';'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_ASSIGN = r':='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t 

def t_STRING(t):
    #r'\'[^\']*\''
    r'\'([^"\n]|(\\"))*\'$'
    return t.value[1:-1]

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
