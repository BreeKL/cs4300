# README for Homework 1 - CS4300

# CS4300 Homework 1
# Brianne Leatherman
# Sept 21, 2025

This project contains a series of Python exercises demonstrating basic Python 
concepts, file handling, metaprogramming, and package usage. Each task includes 
a Python script and corresponding pytest test cases.

-----------------------------------------------

## Python Virtual Environment Setup

It is recommended to use a virtual environment to isolate project dependencies.

# Create a virtual environment
    python -m venv hw1_venv

# Activate the virtual environment
    # Linux/macOS
        source hw1_venv/bin/activate
    # Windows (PowerShell)
        .\hw1_venv\Scripts\Activate.ps1

------------------------------------------------

## Install Dependencies

The project includes a requirements.txt file. Install all dependencies using:

    pip install -r requirements.txt

This ensures the correct version of Python and all necessary libraries are available.

------------------------------------------------

## Task Overview

### Task 1: Introduction to Python and Testing
- File: task1.py
- Prints "Hello, World!".
- Includes pytest tests that verify console output.

### Task 2: Variables and Data Types
- File: task2.py
- Demonstrates integers, floats, strings, and booleans.
- Includes pytest tests to verify correct behavior for each data type.

### Task 3: Control Structures
- File: task3.py
- Implements:
  - An if statement to check if a number is positive, negative, or zero.
  - A for loop to print the first 10 prime numbers.
  - A while loop to sum numbers from 1 to 100.
- Pytest tests verify correctness of all control structures.

### Task 4: Functions and Duck Typing
- File: task4.py
- Function: calculate_discount(price, discount)
- Demonstrates duck typing by accepting any numeric type (int, float).
- Pytest tests check correctness with different numeric types.

### Task 5: Lists and Dictionaries
- File: task5.py
- Demonstrates:
  - A list of favorite books (with title and author) and list slicing.
  - A dictionary representing a student database (name → student ID).
- Pytest tests verify list and dictionary operations.

### Task 6: File Handling and Metaprogramming
- Files: task6.py, task6_read_me.txt
  - task6_read_me.txt contains sample text.
  - task6.py reads the text file and counts the number of words.
- Input content types are dynamically handled at runtime
- Pytest tests verify the word count for file content and string inputs.

### Task 7: Package Management
- File: task7.py
- Demonstrates usage of the requests Python package.
- Includes pytest tests to verify correct functionality using mock head 
    calls and status codes.

-------------------------------------------

## Running Scripts

Activate your virtual environment from the homework1 directory 
and run the following scripts directly:

    python src/task1.py
    python src/task3.py
    python src/task5.py
    python src/task6.py

--------------------------------------------

## Running Tests

Run all pytest tests from the homework1 directory with:

    pytest

This will automatically discover and execute all 65 tests for tasks 1–7.

Or, run tests on specific tasks by indicating the test file as an argument.

Example:

    pytest tests/test_task1.py

--------------------------------------------

## Notes

- Always activate the virtual environment before running scripts or tests:

    source hw1_venv/bin/activate

- If test_task6 fails, ensure full file path for task6_read_me.txt is correct 
  in both task6.py and test_task6.py