
# integers
def integer_math(x,y):
    return x+y, x-y, x*y, x/y

# floating-point numbers
def float_math(x,y):
    if y == 0: 
        div = None
    else: div = x/y

    return x+y, x-y, x*y, div

# strings
# Performs basic "string math": addition (concatenation), subtraction (removing occurrences of y from x),
# and multiplication (repeating x y times if y is a positive integer; otherwise None)
def string_math(x,y):
    # Ensure x is string for string multiplication
    if isinstance(x, int):
        x = str(x)

    # Multiply only if y is a positive int
    if isinstance(y, int) and y > 0:
        mult = x * y
        y = str(y)
    else:
        y = str(y)
        mult = None

    add = x+y
    sub = x.replace(y, '')

    return add, sub, mult

# booleans
def AND(x, y):
    return x and y

def OR(x, y):
    return x or y

def XOR(x, y):
    return x != y

def NAND(x, y):
    return not (x and y)

def NOR(x, y):
    return not (x or y)

def XNOR(x, y):
    return x == y

