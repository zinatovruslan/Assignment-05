from expense_tracker import storage
from expense_tracker.cli import main
from expense_tracker.report import render_report
from expense_tracker.tracker import ExpenseTracker


def make():
    t = ExpenseTracker()
    t.add("coffee", 3.5, "food")
    t.add("bus", 2.0, "transport")
    t.add("lunch", 10.0, "food")
    return t


def test_total():  # AC2
    assert make().total() == 15.5


def test_by_category():  # AC3
    assert make().by_category() == {"food": 13.5, "transport": 2.0}


def test_storage_roundtrip(tmp_path):  # AC1
    p = tmp_path / "e.json"
    t = make()
    storage.save(t.expenses, str(p))
    assert storage.load(str(p)) == t.expenses


def test_reports_contain_total():  # AC4
    t = make()
    assert "TOTAL 15.50" in render_report(t, "text")
    assert "description,amount,category" in render_report(t, "csv")
    assert '"total": 15.5' in render_report(t, "json")


def test_cli_total(tmp_path, capsys):  # AC5
    f = str(tmp_path / "e.json")
    main(["--file", f, "add", "coffee", "3.5", "food"])
    main(["--file", f, "total"])
    assert capsys.readouterr().out.strip().endswith("3.50")
