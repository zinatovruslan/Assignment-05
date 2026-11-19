import json
import os
from decimal import Decimal

DEFAULT_PATH = "expenses.json"


def load(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        raw = json.load(f)
    # Amounts are stored as strings (older files may hold floats).
    return [{**e, "amount": Decimal(str(e["amount"]))} for e in raw]


def save(expenses, path=DEFAULT_PATH):
    serializable = [{**e, "amount": str(e["amount"])} for e in expenses]
    with open(path, "w") as f:
        json.dump(serializable, f, indent=2)
