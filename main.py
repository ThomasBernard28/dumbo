import syntaxer

'''
We use a dictionnary to store variables and their values
There are multiples "levels" of variables depending on the scope #Thx chat gpt for the idea
e.g if we are assigning a global variable it's level will be 0
but if we are assigning a variable in a for loop it's level will be 1
and if we are assigning a variable in a for loop in a for loop it's level will be 2 etc.
'''
indent_level = 0
variables = {}
functions = ["print", "for", "if", "assign", "concat", "math_op"]

def run(rowData, rowTemplate):
    data = syntaxer.parse(rowData)
    template = syntaxer.parse(rowTemplate)

    # Assign variables
    global variables
    variables[indent_level] = {}
    variables[indent_level] = assignDataVars(data)

    return applyTemplateFunctions(template)

'''
This method aims to store in the variables dictionary the variables that are in the data file.
'''
def assignDataVars(data):
    for item in data:
        #We need to ensure that the item is a tuple
        if type(item) is tuple:
            if item[0] == "assign":
                variables[item[1]] = item[2]
            else:
                raise Exception("Unknown expression type: " + item[0])
    return variables

'''
This method aims to assign the variables from a template file.
There are multiple cases:
- The variable is a string or an integer : 
    1. we check if it exists in the variables dictionary
    2. if it exists we update its value
    3. if it doesn't exist we create it
- The variable is a tuple :
    1. we apply the applyTemplateFunctions method to the tuple
'''
def assignLocalVars(varName, varValue):
    if type(varValue) is str or type(varValue) is int:
        searchResult = checkIfVarExists(varName)
        if type(searchResult) is tuple:
            variables[searchResult[1]][searchResult[0]] = varValue
        else:
            variables[indent_level][varName] = varValue
    elif type(varValue) is tuple:
        variables[indent_level][varName] = applyTemplateFunctions(varValue)


'''
This method aims to apply the different function encountered during the evaluation of the template file.
This method can be call recursively. The objective is to reduce the template file to basic expressions that
will be evaluated by sub methods dedicated to each type of expression.
'''
def applyTemplateFunctions(template):
    output = ""
    #Thanks to template3 we know that it might me empty
    if template == "":
        return ""
    else:
        # If the template is a simple tuple
        # that contains a function
        if template[0] in functions:
            newTemplate = [template]
            return applyTemplateFunctions(newTemplate)
        for item in template:
            # Had a problem with the concat function.
            # The word concat was added to the template
            if type(item) is str and item not in functions:
                output += item
            else:
                # functionToApply is the function we need to apply to the item
                functionToApply = item[0]
                match functionToApply:
                    case "print":
                        output += applyPrint(item[1])
                    case "for":
                        global indent_level
                        indent_level += 1
                        output += applyFor(item[1], item[2], item[3])
                        indent_level -= 1
                    case _:
                        raise Exception("Unknown expression type: " + functionToApply)
        return output
'''
This method aims to check if a variable exists in the variables dictionary.
If it exists, it returns the variable name and its level.
If it doesn't exist, it returns the variable name.
With these information the other methods will be able to know 
if they need to create a new variable or not.
'''
def checkIfVarExists(varName):
    global indent_level
    currentLevel = indent_level
    # We want to check first at the deepest level
    while currentLevel >= 0:
        if varName in variables[currentLevel]:
            return varName, currentLevel
        currentLevel -= 1
    return varName

'''
This method aims to print an expression.
If the expression is a string it will first check if it's a variable name.
If it's a variable name it will return its value.
If it's not a variable name it will return the string.
If the expression is a tuple it will call the master function recursively.
'''
def applyPrint(expr):
    # First we want to check if the expression is a variable
    if type(expr) is str:
        # Then we want to check if it's a variable name
        searchResult = checkIfVarExists(expr)
        # This means that the variable exists
        if type(searchResult) is tuple:
            return variables[searchResult[1]][searchResult[0]]
        else:
            #This means that the variable doesn't exist so we return the string
            return expr
    # We can't print a tuple, so we will call the master function recursively
    elif type(expr) is tuple:
        return applyTemplateFunctions(expr)

def applyFor(varName, array, expr):
    output = ""
    # We first need to check if the variables level exists
    if variables.get(indent_level) is None:
        variables[indent_level] = {}

    # We need to check if varName is a variable name
    searchVarName = checkIfVarExists(varName)
    # If it's a variable name we need to get its value
    previousValue = None
    if type(searchVarName) is tuple:
        previousValue = variables[searchVarName[1]][searchVarName[0]]

    lst = []
    # Then we need to check if the array is a variable or a list
    if type(array) is str:
        searchResult = checkIfVarExists(array)
        lst = variables[searchResult[1]][searchResult[0]]
    elif type(array) is list:
        lst = array

    for item in lst:
        # Assign the value to the variable
        assignLocalVars(varName, item)
        # Apply the template functions
        output += applyTemplateFunctions(expr)

    #Before returning the output we need to set the var back to its previous value
    if previousValue is not None:
        variables[searchVarName[1]][searchVarName[0]] = previousValue

    return output


def readFile(filename):
    # Read file
    lines = ""
    with open(filename, 'r') as f:
        lines = f.read()
    return lines

if __name__ == '__main__':

    import sys
    if len(sys.argv) == 3:
        # Init files and data
        dataFile = sys.argv[1]
        templateFile = sys.argv[2]
        rowData = readFile(dataFile)
        rowTemplate = readFile(templateFile)

        # Run the program and write the output
        output = run(rowData, rowTemplate)
        print(output)
