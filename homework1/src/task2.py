"""
Task2 Module: Functions for working with different data types.

This module provides basic arithmetic, string, and logical operations
for specific data types including integers, floating-point numbers, 
strings, and booleans.

Sections and functionalities:
- Integers:
    - int_add, int_subtract, int_multiply, int_divide
- Floating-point numbers:
    - float_add, float_subtract, float_multiply, float_divide
- Strings:
    - string_add (concatenation)
    - string_subtract (remove occurrences)
    - string_multiply (repeat string)
- Booleans:
    - AND, OR, XOR, NAND, NOR, XNOR

Notes
-----
- Division functions return None if attempting to divide by zero.
- String functions automatically convert integers to strings when needed.
- Boolean functions perform standard logical operations.
"""


# ******** integers **************
def int_add(x, y):
    return x + y


def int_subtract(x, y):
    return x - y


def int_multiply(x, y):
    return x * y


def int_divide(x, y):
    """
    Divide one integer by another, returning an integer result.

    Parameters
    ----------
    x : int
        Dividend.
    y : int
        Divisor.

    Returns
    -------
    int or None
        The integer division result of x / y, or None if y is zero.
    """
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
    """
    Divide one floating-point number by another.

    Parameters
    ----------
    x : float
        Dividend.
    y : float
        Divisor.

    Returns
    -------
    float or None
        The result of x / y, or None if y is zero.
    """
    if y == 0:
        return None
    return x / y


# ********** Strings ****************
def string_add(x, y):
    """
    Concatenate two strings. Integers are converted to strings if necessary.

    Parameters
    ----------
    x : str or int
        First string or integer.
    y : str or int
        Second string or integer.

    Returns
    -------
    str
        Concatenated result of x and y.
    """
    if isinstance(x, int):
        x = str(x)
    if isinstance(y, int):
        y = str(y)
    return x + y


def string_subtract(x, y):
    """
    Remove all occurrences of y from x. Integers are converted to strings if necessary.

    Parameters
    ----------
    x : str or int
        Original string or integer.
    y : str or int
        String or integer to remove from x.

    Returns
    -------
    str
        Resulting string after removal.
    """
    if isinstance(x, int):
        x = str(x)
    if isinstance(y, int):
        y = str(y)
    return x.replace(y, '')


def string_multiply(x, y):
    """
    Repeat string x, y times if y is a positive integer.

    Parameters
    ----------
    x : str or int
        String or integer to repeat.
    y : int
        Number of times to repeat x.

    Returns
    -------
    str or None
        Repeated string if y > 0, otherwise None.
    """
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
