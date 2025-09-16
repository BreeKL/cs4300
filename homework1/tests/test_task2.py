from task2 import *
import pytest

@pytest.mark.parametrize("x,y,expected", [(1,2,[3,-1,2,0]), (0,2,[2,2,0,0]), (2,0,[2,2,0,None])])
def test_string_math(x,y,expected):
    assert string_math(x,y) == expected

@pytest.mark.parametrize("x,y,expected", [(1.5,2,(3.5,-0.5,3.0,0.75)), (0.0,2.0,(2.0,-2.0,0.0,0.)), (2.0,0.0,(2.0,2.0,0.0,None))])
def test_float_math(x,y,expected):
    assert float_math(x,y) == expected

@pytest.mark.parametrize(
    "x, y, expected",
    [
        ("", "", ("", "", None)),
        ("a", "", ("a", "a", None)),
        ("", "b", ("b", "", None)),
        ("abc", "a", ("abca", "bc", None)),
        ("abc", "abcd", ("abcabcd", "abc", None)),
        ("x"*1000, "y"*1000, ("x"*1000 + "y"*1000, "x"*1000, None)),
        ("abc", 0, ("abc0", "abc", None)),
        ("abc", -1, ("abc-1", "abc", None)),
        ("abc", 2, ("abc2", "abc", "abcabc")),
        ("a\nb\tc", "b", ("a\nb\tcb", "a\n\tc", None)),
        ("123", 3, ("1233", "12", "123123123")),
        ("!@#", "@", ("!@#@", "!#", None)),
        (2, "abc", ("2abc", "2", None))
    ]
)
def test_string_math(x, y, expected):
    assert string_math(x, y) == expected

@pytest.mark.parametrize(
    "x, y, expected_and, expected_or, expected_xor, expected_nand, expected_nor, expected_xnor",
    [
        (True, True, True, True, False, False, False, True),
        (True, False, False, True, True, True, False, False),
        (False, True, False, True, True, True, False, False),
        (False, False, False, False, False, True, True, True),
    ]
)
def test_boolean_functions(x, y, expected_and, expected_or, expected_xor, expected_nand, expected_nor, expected_xnor):
    assert AND(x, y) == expected_and
    assert OR(x, y) == expected_or
    assert XOR(x, y) == expected_xor
    assert NAND(x, y) == expected_nand
    assert NOR(x, y) == expected_nor
    assert XNOR(x, y) == expected_xnor

