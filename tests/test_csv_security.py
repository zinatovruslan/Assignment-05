import csv
import io

import pytest

from expense_tracker.report import render_report
from expense_tracker.tracker import ExpenseTracker


def rows_of(tracker):
    return list(csv.reader(io.StringIO(render_report(tracker, "csv"))))


@pytest.mark.parametrize("lead", ["=", "+", "-", "@"])
def test_formula_prefix_neutralized(lead):  # regression for risk R2
    t = ExpenseTracker()
    t.add(lead + 'HYPERLINK("http://evil.example","x")', "5", "food")
    description = rows_of(t)[1][0]
    assert description.startswith("'")
    assert not description.startswith(("=", "+", "-", "@"))


def test_comma_and_quote_keep_three_columns():  # AC4
    t = ExpenseTracker()
    t.add('lunch, "big"', "9", "food")
    rows = rows_of(t)
    assert all(len(r) == 3 for r in rows)
    assert rows[1] == ['lunch, "big"', "9.00", "food"]


def test_normal_text_unchanged():
    t = ExpenseTracker()
    t.add("coffee", "3.5", "food")
    assert rows_of(t)[1] == ["coffee", "3.50", "food"]
