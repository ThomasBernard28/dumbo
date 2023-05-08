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
functions = ["print", "for", "if", "assign", "concat", "math_op", "bool_comp"]


def run(rowData, rowTemplate):
    """
    This method aims to run the program. It will parse the data and template files,
    assign the variables and apply the template functions.

    Keyword arguments:
    rowData -- The data file.
    rowTemplate -- The template file.

    Return:
    The result of the program.
    """

    data = syntaxer.parse(rowData)
    template = syntaxer.parse(rowTemplate)

    # Assign variables
    global variables
    variables[indent_level] = {}
    variables[indent_level] = assignDataVars(data)

    return applyTemplateFunctions(template)


def assignDataVars(data):
    """
    This method aims to store in the variables' dictionary the variables that are in the data file.

    Keyword arguments:
    data -- The data set previously parsed.

    Return:
    The variables dictionary.
    """

    for item in data:
        # We need to ensure that the item is a tuple
        if type(item) is tuple:
            if item[0] == "assign":
                variables[item[1]] = item[2]
            else:
                raise Exception("Unknown expression type: " + item[0])
    return variables


def assignLocalVars(varName, varValue):
    """
    This method aims to assign the variables from a template file.
    There are 2 cases:
        - The variable is already in the variables dictionary :
            - We update the value of the variable :
                - If the value is a string or an int : we update the value
                - If the value is a tuple : we apply the template functions to the value
        - The variable is not in the variables dictionary :
            - We add the variable to the dictionary :
                - If the value is a string or an int : we add the variable
                - If the value is a tuple : we apply the template functions to the value

    Keyword arguments:
    varName -- The name of the variable.
    varValue -- The value to assign to the variable.
    """

    searchResult = checkIfVarExists(varName)

    # If the variable already exists
    if type(searchResult) is tuple:

        if type(varValue) is str or type(varValue) is int:
            variables[searchResult[1]][searchResult[0]] = varValue

        elif type(varValue) is tuple:
            variables[searchResult[1]][searchResult[0]] = applyTemplateFunctions(varValue)

    else:

        if type(varValue) is str or type(varValue) is int:
            variables[indent_level][varName] = varValue

        elif type(varValue) is tuple:
            variables[indent_level][varName] = applyTemplateFunctions(varValue)


def applyTemplateFunctions(template):
    """
    This method aims to apply the different function encountered during the evaluation of the template file.
    This method can be call recursively. The objective is to reduce the template file to basic expressions that
    will be evaluated by sub methods dedicated to each type of expression.

    Keyword arguments:
    template -- The current set of expression to be evaluated.

    Return:
    returns the evaluation of the expressions recursively.
    """

    output = ""
    # Thanks to template3 we know that it might me empty
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
                    case "assign":
                        assignLocalVars(item[1], item[2])
                    case "print":
                        output += applyPrint(item[1])
                    case "for":
                        global indent_level
                        indent_level += 1
                        output += applyFor(item[1], item[2], item[3])
                        indent_level -= 1
                    case "if":
                        indent_level += 1
                        output += applyIf(item[1], item[2])
                        indent_level -= 1
                    case "bool_comp":
                        applyBoolComp(item[1], item[2], item[3])
                    case "concat":
                        output += applyConcat(item[1], item[2])
                    case "math_op":
                        output += applyMathOp(item[1], item[2], item[3])
                    case _:
                        raise Exception("Unknown expression type: " + functionToApply)
        return output


def checkIfVarExists(varName):
    """
    This method aims to check if a variable exists in the variables' dictionary.
    If it exists, it returns the variable name and its level.
    If it doesn't exist, it returns the variable name.
    With these information the other methods will be able to know
    if they need to create a new variable or not.

    Keyword arguments:
    varName -- The name of the variable to check.

    Return:
    The variable name and its level if it exists. The variable name if it doesn't exist.
    """

    global indent_level
    currentLevel = indent_level
    if variables.get(currentLevel) is None:
        variables[currentLevel] = {}
    # We want to check first at the deepest level
    while currentLevel >= 0:
        if varName in variables[currentLevel]:
            return varName, currentLevel
        currentLevel -= 1
    return varName


def applyPrint(expr):
    """
    This method aims to print an expression.
    If the expression is a string it will first check if it's a variable name.
    If it's a variable name it will return its value.
    If it's not a variable name it will return the string.
    If the expression is a tuple it will call the master function recursively.

    Keyword arguments:
    expr -- The expression to print.

    Return:
    The value of the expression if it's a variable name. The string if it's not a variable name.
    """
    # First we want to check if the expression is a variable
    if type(expr) is str:
        # Then we want to check if it's a variable name
        searchResult = checkIfVarExists(expr)
        # This means that the variable exists
        if type(searchResult) is tuple:
            return str(variables[searchResult[1]][searchResult[0]])
        else:
            # This means that the variable doesn't exist so we return the string
            return expr
    # We can't print a tuple, so we will call the master function recursively
    elif type(expr) is tuple:
        return applyTemplateFunctions(expr)


def applyFor(varName, array, expr):
    """
    This method aims to apply the for loop.
    If the varName is a global variable, we will store the previous value of the variable.
    Then we will iterate over the array and apply the template functions to the expression.
    Finally, we will restore the previous value of the variable if it's a global variable.

    Keyword arguments:
    varName -- The name of the variable.
    array -- The array to iterate over.
    expr -- The expression(s) to apply to each item of the array.

    Return:
    The result of the for loop.
    """

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

    # Before returning the output we need to set the var back to its previous value
    if previousValue is not None:
        variables[searchVarName[1]][searchVarName[0]] = previousValue

    return output


def applyConcat(expr1, expr2):
    """
    This method aims to concatenate two expressions.
    By the syntax we defined we know that expr1 is a string.
    First we check if expr1 is a variable name or a string, and we add it to the output.
    Then we check for expr2. If it's a string we add it to the output.
    If it's a variable name we get its value and we add it to the output.
    If it's a tuple we call the master function recursively.

    Keyword arguments:
    expr1 -- The first expression to concatenate.
    expr2 -- The second expression to concatenate.

    Return:
    The concatenation of the two expressions.
    """

    output = ""
    # By the way we defined the syntax we know that expr1 is a string
    # We need to check if expr1 is a variable name
    searchResult1 = checkIfVarExists(expr1)

    # If it's a variable name we need to get its value
    if type(searchResult1) is tuple:
        output += variables[searchResult1[1]][searchResult1[0]]

    # If it's not a variable name we need to add the string
    else:
        output += expr1

    # We need to check if expr2 is a variable name
    if type(expr2) is str:
        searchResult2 = checkIfVarExists(expr2)
        if type(searchResult2) is tuple:
            output += variables[searchResult2[1]][searchResult2[0]]
        else:
            output += expr2
    # We can't concatenate a tuple, so we need to call the master function recursively
    elif type(expr2) is tuple:
        output += applyTemplateFunctions(expr2)

    return output


def applyMathOp(expr1, op, expr2):
    """
    This method aims to apply a mathematical operation to two expressions.
    First we check if expr1 is a variable name or a string, and if we can convert it to an int.
    If we can convert it to an int we store it in expr1.
    Then we check for expr2. If it's a string we add it to the output.
    If it's a variable name we get its value, and we add it to the output.
    If it's a tuple we call the master function recursively.
    If one of the expressions can't be converted to an int we raise an exception.

    Keyword arguments:
    expr1 -- The first expression to apply the operation to.
    op -- The operation to apply.
    expr2 -- The second expression to apply the operation to.

    Return:
    The result of the operation.
    """

    output = ""
    # We need to check if expr1 is a variable name
    if type(expr1) is str:
        searchResult1 = checkIfVarExists(expr1)
        try:
            expr1 = int(variables[searchResult1[1]][searchResult1[0]])
        except ValueError:
            raise Exception("Can't convert " + expr1 + " to int")
    # We need to check if expr2 is a variable name
    if type(expr2) is str:
        searchResult2 = checkIfVarExists(expr2)
        try:
            expr2 = int(variables[searchResult2[1]][searchResult2[0]])
        except ValueError:
            raise Exception("Can't convert " + expr2 + " to int")

    # Then we use a switch case to apply the operation
    match op:
        case "+":
            output += str(expr1 + expr2)
        case "-":
            output += str(expr1 - expr2)
        case "*":
            output += str(expr1 * expr2)
        case "/":
            # As we only use integers we need to use the integer division
            output += str(expr1 // expr2)
        case _:
            raise Exception("Unknown operation: " + op)

    return output


def applyIf(condition, expr):
    output = ""
    boolean = False
    if type(condition) is tuple:
        booleanCondition = applyTemplateFunctions(condition)
        try:
            boolean = bool(booleanCondition)
        except ValueError:
            raise Exception("Can't convert " + condition + " to bool")
    if boolean:
        output += applyTemplateFunctions(expr)

    elif type(condition) is str:
        try:
            condition = bool(condition)
        except ValueError:
            raise Exception("Can't convert " + condition + " to bool")
    if condition:
        output += applyTemplateFunctions(expr)

    return output


def applyBoolComp(expr1, op, expr2):
    output = ""
    if type(expr1) is tuple:
        expr1 = applyTemplateFunctions(expr1)

    if type(expr2) is tuple:
        expr2 = applyTemplateFunctions(expr2)

    if type(expr1) is str:
        searchResult1 = checkIfVarExists(expr1)
        if type(searchResult1) is tuple:
            try:
                expr1 = int(variables[searchResult1[1]][searchResult1[0]])
            except ValueError:
                raise Exception("Can't convert " + expr1 + " to int")
        else:
            try:
                expr1 = int(expr1)
            except ValueError:
                raise Exception("Can't convert " + expr1 + " to int")

    if type(expr2) is str:
        searchResult2 = checkIfVarExists(expr2)
        if type(searchResult2) is tuple:
            try:
                expr2 = int(variables[searchResult2[1]][searchResult2[0]])
            except ValueError:
                raise Exception("Can't convert " + expr2 + " to int")
        else:
            try:
                expr2 = int(expr2)
            except ValueError:
                raise Exception("Can't convert " + expr2 + " to int")

    if type(expr1) is int:
        if type(expr2) is int:
            match op:
                case "==":
                    output += str(expr1 == expr2)
                case "!=":
                    output += str(expr1 != expr2)
                case "<":
                    output += str(expr1 < expr2)
                case ">":
                    output += str(expr1 > expr2)
                case _:
                    raise Exception("Unknown operation: " + op)

    return output


def readFile(filename):
    # Read file
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
