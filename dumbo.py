import sys
import ply.lex as lex

def read_file(file):
    lines = ""
    with open(file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    return lines

def init_variables():
    pass

def inject_variables():
    pass

if __name__ == '__main__':
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    print(read_file(arg1))
