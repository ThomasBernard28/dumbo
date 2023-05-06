import syntaxer

# We use a dictionnary to store variables and their values
# There are multiples "levels" of variables depending on the scope #Thx chat gpt for the idea
# e.g if we are assigning a global variable it's level will be 0
# but if we are assigning a variable in a for loop it's level will be 1
# and if we are assigning a variable in a for loop in a for loop it's level will be 2 etc.
indent_level = 0
variables = {}

def main(rowData, rowTemplate):
    #data = syntaxer.parse(rowData)
    template = syntaxer.parse(rowTemplate)

    print(template)
def readFile(filename):
    # Read file
    lines = ""
    with open(filename, 'r') as f:
        lines = f.read()
    return lines

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 3:
        #Load Files
        dataFile = readFile(sys.argv[1])
        templateFile = readFile(sys.argv[2])

        #Parse Files
        output = main(dataFile, templateFile)
        print(output)