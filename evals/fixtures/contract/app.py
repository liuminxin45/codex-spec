from pricing import total_cents


def checkout(prices, discount_cents=0):
    total = total_cents(prices) - discount_cents
    return f"¥{total:.2f}"
