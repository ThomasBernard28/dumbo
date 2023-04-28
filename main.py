from ply import lex
import lexer

def readFile(file):
    lines = ""
    with open(file, 'r') as f:
        lines = f.read()

    return lines

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        while True:
            user_input = input(">>> Please enter a code line: ")
            print(lexer.toToken(user_input))

    elif len(sys.argv) == 3:
        dataFile = sys.argv[1]
        templateFile = sys.argv[2]

        print(lexer.toToken(readFile(dataFile)))
        print(lexer.toToken(readFile(templateFile)))
