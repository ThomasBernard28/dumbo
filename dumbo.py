import sys
import tokenizer
import syntaxer

def read_file(file):
    lines = ""
    with open(file, 'r') as f:
        lines = f.read()
    return lines

def init_variables():
    pass

def inject_variables():
    pass

if __name__ == '__main__':
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    print(repr(read_file(arg2)))
    print(tokenizer.tokenize(read_file(arg2)))
    #print(syntaxer.parse(arg1))
    """
    for line in read_file(arg1):
        print(line)
        print(tokenizer.tokenize(line))
    """
