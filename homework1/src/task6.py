"""
This module provides utilities for counting words in text or files.

Features:
- `count_words(content)`: Count words in a string or a text file, ignoring punctuation.
- `print_info(content)`: Print the number of words and indicate whether the input
  was treated as a file or a raw string.
"""

import string
import os
from pathlib import Path

def count_words(content):
    """
    Count the number of words in a file or string, ignoring punctuation.

    This function accepts either a path to a text file (as a string or Path object)
    or a raw string of text. If the input is a file path and the file exists, the file
    will be read and processed. Otherwise, the input is treated as raw text.

    Punctuation characters (.,!?;: etc.) are removed before counting, so potential
    words such as "," are not counted.

    Parameters
    ----------
    content : str | Path
        The input to process. Can be:
        - A file path (string or Path object) to a text file.
        - A string of text to analyze directly.

    Returns
    -------
    int
        The total number of words in the input text.
    """
    if not isinstance(content, (str, Path)):
        raise ValueError("Input must be a string or Path object")

    path = Path(content)

    # Check path existence, and copies text from path or string
    if path.is_file():
        text = path.read_text(encoding="utf-8")
    else:
        text = str(content)

    # Remove punctuation
    translator = str.maketrans("", "", string.punctuation)
    cleaned_text = text.translate(translator)

    return len(cleaned_text.split())    

# Prints count info to the console when running as a script
def print_info(content):
    total_words = count_words(content)
    path = Path(content)
    if path.is_file():
        print(f"The file '{content}' contains {total_words} words.")
    else:
        print(f"The string '{content}' contains {total_words} words.")

if __name__ == "__main__":
    file_to_read = "/home/student/cs4300/homework1/src/task6_read_me.txt"
    string_to_read = "hello"

    print_info(file_to_read)
    print_info(string_to_read)