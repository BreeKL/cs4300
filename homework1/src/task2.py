# Task2 defines functions to work with specific data types


# ******** integers **************
def int_add(x, y):
    return x + y

def int_subtract(x, y):
    return x - y

def int_multiply(x, y):
    return x * y

def int_divide(x, y):
    if y == 0:
        return None
    return int(x / y)

# ********** floating-point numbers *****************
def float_add(x, y):
    return x + y

def float_subtract(x, y):
    return x - y

def float_multiply(x, y):
    return x * y

def float_divide(x, y):
    if y == 0:
        return None
    return x / y

# ********** Strings ****************
# String addition (concatenation)
def string_add(x, y):
    if isinstance(x, int):
        x = str(x)
    if isinstance(y, int):
        y = str(y)
    return x + y

# String subtraction (remove occurrences of y from x)
def string_subtract(x, y):
    if isinstance(x, int):
        x = str(x)
    if isinstance(y, int):
        y = str(y)
    return x.replace(y, '')

# String multiplication (repeat x y times if y is positive integer)
def string_multiply(x, y):
    if isinstance(x, int):
        x = str(x)
    if isinstance(y, int) and y > 0:
        return x * y
    return None

# ************ booleans *******************
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

