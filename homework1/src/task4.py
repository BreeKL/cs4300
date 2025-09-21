def calculate_discount(price, discount):
    """
    Calculate the final price after applying a percentage discount.

    :param price: original price (any type that supports numeric operations)
    :param discount: discount percentage (any type that supports numeric operations)
    :return: final price after discount
    """
    # Use try block to allow duck-typing
    try:
        final_price = price * (1 - discount / 100)
    except Exception as e:
        raise ValueError("Price and discount must support numeric operations") from e

    if discount < 0 or discount > 100:
        raise ValueError("Discount must be between 0 and 100")

    return final_price