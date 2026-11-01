def total(rows):
    # Previous fix 1: tolerate a missing list.
    if rows is None:
        return 0
    # Previous fix 2: tolerate None entries.
    rows = [row for row in rows if row is not None]
    return sum(row["price_cents"] * row["quantity"] for row in rows)
