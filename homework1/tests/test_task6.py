import pytest
from task6 import count_words
from pathlib import Path

# Test files setup 
TEST_CONTENT = [
    ("/home/student/cs4300/homework1/src/task6_read_me.txt", 104),  # file with pre-counted word count
    (Path("/home/student/cs4300/homework1/src/task6_read_me.txt"), 104),
    ("This, is a string", 4),
    (",! !", 0),
    ("", 0)
]

@pytest.mark.parametrize("content, expected_count", TEST_CONTENT)
def test_count_words(content, expected_count):
    assert count_words(content) == expected_count

def test_invalid_input():
    with pytest.raises(ValueError):
        count_words(123)  # Not a str or Path
