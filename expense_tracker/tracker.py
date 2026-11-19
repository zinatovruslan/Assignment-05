from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

CENT = Decimal("0.01")


def to_money(value):
    """Convert user input to a positive, finite Decimal rounded to cents."""
    try:
        amount = Decimal(str(value))
    except InvalidOperation:
        raise ValueError(f"invalid amount: {value!r}") from None
    if not amount.is_finite():
        raise ValueError(f"amount must be finite: {value!r}")
    if amount <= 0:
        raise ValueError(f"amount must be greater than zero: {value!r}")
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


class ExpenseTracker:
    def __init__(self, expenses=None):
        self.expenses = expenses if expenses is not None else []

    def add(self, description, amount, category):
        description = description.strip()
        category = category.strip()
        if not description or not category:
            raise ValueError("description and category must not be empty")
        self.expenses.append(
            {
                "description": description,
                "amount": to_money(amount),
                "category": category,
            }
        )

    def remove(self, index):
        return self.expenses.pop(index)

    def total(self):
        return sum((e["amount"] for e in self.expenses), Decimal(0))

    def by_category(self):
        result = {}
        for e in self.expenses:
            current = result.get(e["category"], Decimal(0))
            result[e["category"]] = current + e["amount"]
        return result
