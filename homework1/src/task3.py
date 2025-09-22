"""
Module for demonstrating basic Python control structures and functions.

This script includes:
- `check_sign`: Determines whether a number is positive, negative, or zero.
- `ten_primes`: Uses a for loop to generate the first ten prime numbers.
- `sum_100`: Uses a formula to calculate the sum of numbers from 1 to 100.
- `is_prime`: Determines if a number is prime using trial division up to √n.
- `main`: Entry point that prints the first ten primes.
"""

import math

# Use if statements
def check_sign(num):
    """
    Determine the sign of a given number.

    Parameters
    ----------
    num : int or float
        The number to evaluate.

    Returns
    -------
    str
        - "positive" if the number is greater than zero.
        - "negative" if the number is less than zero.
        - "zero" if the number equals zero.
        - "Not a Number" if the input is not an int or float.
    """
    if not isinstance(num, (int, float)):
        return "Not a Number"
    if num > 0:
        return "positive"
    elif num < 0:
        return "negative"
    else: return "zero"

# Use for loop
def ten_primes():
    """
    Generate the first ten prime numbers.

    Returns
    -------
    list of int
        A list containing the first ten prime numbers, in ascending order.
    """
    primes = []

    for num in range(100):
        if len(primes) < 10:
            if is_prime(num):
                primes.append(num)
        else: break

    return primes

# Use while loop
def sum_100():
    """
    Calculate the sum of integers from 1 to 100.

    Uses a while loop to iterate though all the integers

    Returns
    -------
    float
        The sum of integers from 1 through 100.
    """
    next = 100
    total = 0
    while next >= 1:
        total += next
        next -= 1
        
    return total

# Logic for this function based on code from https://pynative.com/python-check-prime-number/
def is_prime(n):
    """
    Check whether a number is prime.

    Parameters
    ----------
    n : int
        The number to check for primality.

    Returns
    -------
    bool
        True if the number is prime, False otherwise.

    Notes
    -----
    - 2 is treated as the only even prime.
    - Negative numbers, 0, and 1 are not considered prime.
    """
    # Handle special cases for 1 and 2
    if n <= 1:
        return False
    elif n == 2:
        return True  # 2 is the only even prime number
    elif n % 2 == 0:
        return False

    # Loop through odd numbers from 3 to √n
    sqrt_number = int(math.sqrt(n)) + 1  # Add 1 to ensure we check the square root itself
    for i in range(3, sqrt_number, 2): # Skip even numbers
        if n % i == 0:
            return False
    return True

def main():
    print("The first ten primes are: ", ten_primes())

if __name__ == "__main__":
    main()