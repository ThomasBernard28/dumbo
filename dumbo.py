import syntaxer

#We use a dictionnary to store variables and their values
# There are multiples "levels" of variables depending on the scope #Thx chat gpt for the idea
# e.g if we are assigning a global variable it's level will be 0
# but if we are assigning a variable in a for loop it's level will be 1
# and if we are assigning a variable in a for loop in a for loop it's level will be 2 etc.
level = 0

vars = {}

def run(rowData, rowTemplate):
    data = syntaxer.parse(rowData)
    template = syntaxer.parse(rowTemplate)

    # Assign variables
    global vars
    vars[level] = {}
    vars[level] = assignVar(data)

    #Insert variables in template and return the result
    return insertDataInTemplate(template)


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
                output += applyFor(item[1], item[2], item[3])
            #Even though we assigned the data files variables there might be local variables
            #e.g in a for loop, etc
            elif toApply == "assign":
                assignLocalVars(item[1], item[2])
    return output

def applyPrint(expr):
    #We need to check if the variable is a string or a list
    index = 0
    if type(expr) is str:
        if type(vars[level].get(expr)) is str:
            #We want to check every level of variables to see if the variable exists
            while index <= level:
                if expr in vars[index]:
                    return vars[index][expr]
                index += 1
        else:
            return expr


def assignLocalVars(var, value):
    if vars[level].get(var) == value:
        return #Do nothing if the variable is already assigned to the value
    else:
        vars[level][var] = value

def applyFor(var, array, expr):
    #Since we are in a for loop we need to increment the level
    output = ""
    global level
    level += 1
    #We need to check if the variable level exists before assigning it
    if vars.get(level) is None:
        vars[level] = {}
    for item in vars[level - 1].get(array):
        #Assign the variable
        assignLocalVars(var, item)
        #Apply the expression
        output += insertDataInTemplate(expr)

    return output

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
        #outputPath = sys.argv[3]

        #Run the program and write the output
        output = run(rowData, rowTemplate)
        print(output)
        #file = open(outputPath, "w")
        #file.write(output)
        #file.close()
