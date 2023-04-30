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
    print(data)

    # Assign variables
    var = assignVar(data)
    print(var)
    if var == {}:
        print("No variable found in data file")
        return
    else:
        insertVar(template, var)

def insertVar(template, var):
    output = ""
    for expr in template:
        if type(expr) is str:
            output += expr
        elif type(expr[0]) is tuple:
            if expr[0][0] == 'print':
                output += applyPrint(expr[0], var)
            elif expr[0][0] == 'for':
                output += applyFor(expr[0], var)

    return output

def applyPrint(expr, var):
    inserted = ""
    toAdd = var.get(expr[1])
    if type(toAdd) is str:
        inserted += toAdd
    else:
        for item in toAdd:
            inserted += item
    return inserted

def applyFor(expr, var):
    print(expr)
    toAdd = var.get(expr[2])
    return ""

def assignVar(data):
    var = {}
    for item in data[0]:
        if item != None:
            var[item[1]] = item[2]
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
