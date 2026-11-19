from decimal import Decimal

import pytest

from expense_tracker import storage
from expense_tracker.cli import main
from expense_tracker.tracker import ExpenseTracker


def test_no_float_drift():  # AC2, regression for risk R1
    t = ExpenseTracker()
    t.add("a", 0.1, "x")
    t.add("b", 0.2, "x")
    assert t.total() == Decimal("0.30")


@pytest.mark.parametrize("bad", ["nan", "inf", "-inf", "-50", "0", "abc"])
def test_invalid_amounts_rejected(bad):
    with pytest.raises(ValueError):
        ExpenseTracker().add("x", bad, "food")


@pytest.mark.parametrize("desc,cat", [("", "food"), ("x", "  ")])
def test_blank_text_rejected(desc, cat):
    with pytest.raises(ValueError):
        ExpenseTracker().add(desc, "1", cat)


def test_storage_keeps_exact_decimals(tmp_path):  # AC1
    p = str(tmp_path / "e.json")
    t = ExpenseTracker()
    t.add("a", "0.10", "x")
    storage.save(t.expenses, p)
    assert storage.load(p)[0]["amount"] == Decimal("0.10")


def test_loads_legacy_float_file(tmp_path):
    p = tmp_path / "old.json"
    p.write_text('[{"description": "a", "amount": 3.5, "category": "x"}]')
    assert storage.load(str(p))[0]["amount"] == Decimal("3.5")


def test_cli_rejects_nan(tmp_path, capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--file", str(tmp_path / "e.json"), "add", "x", "nan", "food"])
    assert exc.value.code == 2
