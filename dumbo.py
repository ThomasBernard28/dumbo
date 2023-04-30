from ply import lex
import lexer
import yacc

def loadFiles(dataFile, templateFile):
    # Read files
    rowData = readFile(dataFile)
    rowTemplate = readFile(templateFile)

    # Parse files
    data = yacc.parse(rowData)
    template = yacc.parse(rowTemplate)

    # Assign variables
    var = assignVar(data)
    if var == {}:
        print("No variable found in data file")
        return
    else:
        insertVar(template, var)

def insertVar(template, var):
    # TODO: Insert variables in template
    return

def assignVar(data):
    var = {}
    for i in range(len(data) -1):
        for j in range(len(data[i])):
            var[data[i][j][1]] = data[i][j][2]
    return var


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
            print(yacc.parse(user_input))

    elif len(sys.argv) == 3:
        dataFile = sys.argv[1]
        templateFile = sys.argv[2]
        loadFiles(dataFile, templateFile)
    else:
        print("Usage: python3 dumbo.py [data file] [template file]\nOR python3 dumbo.py (for infinite prompt)\n")
