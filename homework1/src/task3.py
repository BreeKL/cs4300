import math

# Use if statements
def check_sign(num):
    if num > 0:
        return "positive"
    elif num < 0:
        return "negative"
    else: return "zero"

# Use for loop
def ten_primes():
    primes = []

    for num in range(100):
        if len(primes) < 10:
            if is_prime(num):
                primes.append(num)
        else: break

    return primes

# Use while loop
def sum_100():
    total = (100 + 1) * (100 / 2)
    return total

# Logic for this function based on code from https://pynative.com/python-check-prime-number/
def is_prime(n):
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
    print(ten_primes())

if __name__ == "__main__":
    main()