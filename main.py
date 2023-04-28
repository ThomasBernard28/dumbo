from ply import lex
import lexer

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        while True:
            user_input = input(">>> Please enter a code line: ")
            print(lexer.toToken(user_input))

    elif len(sys.argv) == 3:
        dataFile = sys.argv[1]
        templateFile = sys.argv[2]

        data = ""
        with open(dataFile, 'r') as f:
            data = f.read()

        template = ""
        with open(templateFile, 'r') as f:
            template = f.read()

        print(lexer.toToken(dataFile))
