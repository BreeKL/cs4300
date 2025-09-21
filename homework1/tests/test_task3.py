from task3 import *
import pytest

@pytest.mark.parametrize("num, expected_result", [(10, "positive"), (-2, "negative"), (0, "zero"), ("Hi", "Not a Number"), (0.11, "positive")] )
def test_check_sign(num, expected_result):
    assert check_sign(num) == expected_result

def test_ten_primes():
    assert ten_primes() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_sum_100():
    assert sum_100() == 5050

