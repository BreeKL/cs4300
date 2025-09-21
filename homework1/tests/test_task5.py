import pytest
from task5 import *

def test_find_first_three_books():
    """Test that find_first_three_books returns the correctly formatted list."""
    reference_books = favorite_books[:3] 

    # Create expected formatting
    expected_output = [
        f"Book 1: {reference_books[0]['title']}, Author: {reference_books[0]['author']}",
        f"Book 2: {reference_books[1]['title']}, Author: {reference_books[1]['author']}",
        f"Book 3: {reference_books[2]['title']}, Author: {reference_books[2]['author']}"
    ]
    
    assert find_first_three_books() == expected_output

def test_student_database_access():
    """Test that students can be correctly accessed by their ID."""
    # Test known IDs
    assert get_student_name(100) == "Alice"
    assert get_student_name(101) == "Bob"
    assert get_student_name(102) == "Charlie"
    assert get_student_name(104) == "Ethan"

    # Test an invalid ID returns None
    assert get_student_name(999) is None