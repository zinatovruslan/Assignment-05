class ExpenseTracker:
    def __init__(self, expenses=None):
        self.expenses = expenses if expenses is not None else []

    def add(self, description, amount, category):
        self.expenses.append(
            {"description": description, "amount": amount, "category": category}
        )

    def remove(self, index):
        return self.expenses.pop(index)

    def total(self):
        return sum(e["amount"] for e in self.expenses)

    def by_category(self):
        result = {}
        for e in self.expenses:
            result[e["category"]] = result.get(e["category"], 0) + e["amount"]
        return result
