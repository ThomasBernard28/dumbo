import syntaxer

#We use a dictionnary to store variables and their values
# There are multiples "levels" of variables depending on the scope #Thx chat gpt for the idea
# e.g if we are assigning a global variable it's level will be 0
# but if we are assigning a variable in a for loop it's level will be 1
# and if we are assigning a variable in a for loop in a for loop it's level will be 2 etc.

indent_level = 0
variables = {}

def run(rowData, rowTemplate):
    data = syntaxer.parse(rowData)
    template = syntaxer.parse(rowTemplate)
    print(data)

    # Assign variables
    global variables
    variables[indent_level] = {}
    variables[indent_level] = assignVar(data)


def assignVar(data):
    for item in data:
        #We need to ensure that the item is a tuple
        if type(item) is tuple:
            if item[0] == "assign":
                variables[item[1]] = item[2]
            else:
                raise Exception("Unknown expression type: " + item[0])
    return variables

def applyIf(condition, expr):
    if type(condition) is str:
        if condition == "true":
            return insertDataInTemplate(expr)
        else:
            return
    elif type(condition) is tuple:
        return insertDataInTemplate(condition)

def applyComparison(part1, op, part2):
    if type(part1) is str:
        part1 = checkIfAlreadyDefined(part1)
        try :
            part1 = int(part1)
        except ValueError:
            raise Exception("Cannot convert " + part1 + " to int")


def p_expression_if(p):
    '''expression : IF boolean_expression DO expression_list ENDIF'''

    p[0] = ("if", p[2], p[4])

def p_boolean_expression(p):
    '''boolean_expression :  boolean_expression AND boolean_expression
                            | boolean_expression OR boolean_expression
                            | boolean
                            | comparison'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ("bool_op", p[1], p[2], p[3])

def p_comparison(p):
    '''comparison :  numerical_expression EQUALS numerical_expression
                    | numerical_expression DIFFERENT numerical_expression
                    | numerical_expression GREATER numerical_expression
                    | numerical_expression LESS numerical_expression'''
    p[0] = ("comparison", p[1], p[2], p[3])

def p_boolean(p):
    '''boolean : TRUE
                | FALSE'''
    p[0] = p[1]



def readFile(filename):
    # Read file
    lines = ""
    with open(filename, 'r') as f:
        lines = f.read()
    return lines

if __name__ == 'main':

    import sys
    if len(sys.argv) == 3:
        # Init files and data
        dataFile = sys.argv[1]
        templateFile = sys.argv[2]
        rowData = readFile(dataFile)
        rowTemplate = readFile(templateFile)

        # Run the program and write the output
        output = run(rowData, rowTemplate)
        # file = open(outputPath, "w")
        # file.write(output)
        # file.close()