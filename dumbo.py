import syntaxer

#We use a dictionnary to store variables and their values
# There are multiples "levels" of variables depending on the scope
# e.g if we are assigning a global variable it's level will be 0
# but if we are assigning a variable in a for loop it's level will be 1
# and if we are assigning a variable in a for loop in a for loop it's level will be 2 etc.
level = 0

vars = {}

def initialize(rowData, rowTemplate):
    data = syntaxer.parse(rowData)
    template = syntaxer.parse(rowTemplate)
    print(data)

    # Assign variables
    global vars
    vars[level] = {}
    vars[level] = assignVar(data)

    #Insert variables in template
    insertDataInTemplate(template)


def assignVar(data):
    for item in data:
        #We need to ensure that the item is a tuple
        if type(item) is tuple:
            if item[0] == "assign":
                vars[item[1]] = item[2]
            else:
                raise Exception("Unknown expression type: " + item[0])
    return vars

def insertDataInTemplate(template):
    output = ""
    #Thanks to template3 we know that it might me empty
    if template == "":
        return ""
    print(template)
    for item in template:
        if type(item) is str:
            #In case we are in the TEXT mode
            output += item
        else:
            # toApply is the function we need to apply to the item
            toApply = item[0]
            if toApply == "print":
                output += applyPrint(item[1])
            elif toApply == "for":
                #output += applyFor(item[1], item[2], item[3])
                pass
            #Even though we assigned the data files variables there might be local variables
            #e.g in a for loop, etc
            elif toApply == "assing":
                #assignLocalVars(item[1], item[2])
                pass
    print(output)


def applyPrint(expr):
    #We need to check if the variable is a string or a list
    if type(expr) is str:
        if type(vars[level].get(expr)) is str:
            return vars[level].get(expr)
        else:
            raise Exception("Variable " + expr + " is not a string")
    else:
        raise Exception("Unknown variable type: " + type(vars[level][expr]))





def readFile(filename):
    # Read file
    lines = ""
    with open(filename, 'r') as f:
        lines = f.read()
    return lines

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        while True:
            user_input = input(">>> Please enter a code line: ")
            print(syntaxer.parse(user_input))
    elif len(sys.argv) == 3:
        #Init files and data
        dataFile = sys.argv[1]
        templateFile = sys.argv[2]
        rowData = readFile(dataFile)
        rowTemplate = readFile(templateFile)

        #Initialize
        initialize(rowData, rowTemplate)
