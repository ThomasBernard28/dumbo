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
        if type(item) is str and item != "concat":
            #In case we are in the TEXT mode
            output += item
        else:
            # toApply is the function we need to apply to the item
            toApply = item[0]
            if toApply == "print":
                output += applyPrint(item[1])
            elif toApply == "for":
                output += applyFor(item[1], item[2], item[3])
                global level
                level -= 1
            elif toApply == "if":
                output += applyIf(item[1], item[2])
            #Even though we assigned the data files variables there might be local variables
            #e.g in a for loop, etc
            elif toApply == "assign":
                assignLocalVars(item[1], item[2])
            elif toApply == "concat":
                output += concat(item[1], item[2])
            elif toApply == "math_op":
                output += mathOp(item[1], item[2], item[3])
    return output

def applyPrint(expr):
    if type(expr) is str:
        return str(checkIfAlreadyDefined(expr))
    elif type(expr) is tuple:
        return insertDataInTemplate(expr)


def assignLocalVars(var, value):
    if type(value) is str:
        vars[level][var] = checkIfAlreadyDefined(value)
    elif type(value) is int or type(value) is float:
        vars[level][var] = value
    elif type(value) is tuple:
        if value[0] == "math_op":
            vars[level][var] = mathOp(value[1], value[2], value[3])


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

    #We need to decrement the level
    return output

def concat(part1, part2):
    output = ""

    if type(part2) is str:
        output += checkIfAlreadyDefined(part1) + checkIfAlreadyDefined(part2)
    elif type(part2) is tuple:
        output += checkIfAlreadyDefined(part1) + insertDataInTemplate(part2)

    return output

def mathOp(part1, op, part2):
    output = ""

    if type(part1) is str:
        part1 = checkIfAlreadyDefined(part1)
        try :
            part1 = int(part1)
        except ValueError:
            raise Exception("Cannot convert " + part1 + " to int")
    if type(part2) is str:
        part2 = checkIfAlreadyDefined(part2)
        try :
            part2 = int(part2)
        except ValueError:
            raise Exception("Cannot convert " + part2 + " to int")

    if op == "+":
        output += str(part1 + part2)
    elif op == "-":
        output += str(part1 - part2)
    elif op == "*":
        output += str(part1 * part2)
    elif op == "/":
        output += str(part1 // part2)

    return output

def applyIf(condition, expr):
    output = ""
    if evaluate_condition(condition):
        output += insertDataInTemplate(expr)
    return output
        
def evaluate_condition(expr):
    if type(expr) == bool:
        return expr
    part1 = expr[1]
    op = expr[2]
    part2 = expr[3]
    if type(part1) == tuple:
        part1 = evaluate_condition(part1)
    if type(part2) == tuple:
        part2 = evaluate_condition(part2)

    if expr[0] == "bool_comp":
        return boolComp(part1, op, part2)
    elif expr[0] == "bool_op":
        return boolOp(part1, op, part2)

def boolComp(part1, op, part2):
    part1 = int(part1)
    part2 = int(part2)
    if op == ">" and part1 > part2:
        return True
    elif op == "<" and part1 < part2:
        return True
    elif op == "=" and part1 == part2:
        return True
    elif op == "!=" and part1 != part2:
        return True
    return False

def boolOp(part1, op, part2):
    part1 = bool(part1)
    part2 = bool(part2)
    if op == "and" and (part1 and part2):
        return True
    if op == "or" and (part1 or part2):
        return True
    return False

def checkIfAlreadyDefined(varName):
    index = level
    while index >= 0:
        if varName in vars[index]:
            return vars[index][varName]
        index -= 1
    return varName

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
