import pytest
from task4 import calculate_discount

@pytest.mark.parametrize(
    "price, discount, expected",
    [
        (100, 10, 90),          # integers
        (200, 50, 100),         # 50% off
        (100.0, 25.0, 75.0),    # floats
        (99.99, 10, 89.991),    # mixed float and int
        (150, 0, 150),          # no discount
        (150, 100, 0),          # full discount
    ]
)
def test_calculate_discount(price, discount, expected):
    result = calculate_discount(price, discount)
    assert result == pytest.approx(expected)


def test_invalid_discount_negative():
    with pytest.raises(ValueError):
        calculate_discount(100, -5)


def test_invalid_discount_above_100():
    with pytest.raises(ValueError):
        calculate_discount(100, 150)


@pytest.mark.parametrize("bad_price", ["100", None, [100], {"price": 100}])
def test_invalid_price_type(bad_price):
    with pytest.raises(ValueError):
        calculate_discount(bad_price, 10)


@pytest.mark.parametrize("bad_discount", ["10", None, [10], {"discount": 10}])
def test_invalid_discount_type(bad_discount):
    with pytest.raises(ValueError):
        calculate_discount(100, bad_discount)
