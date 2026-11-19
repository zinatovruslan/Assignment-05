import pytest

from expense_tracker.report import file_extension, mime_type, render_report
from expense_tracker.tracker import ExpenseTracker


def sample():
    t = ExpenseTracker()
    t.add("coffee", 3.5, "food")
    return t


@pytest.mark.parametrize(
    "fmt,ext,mime",
    [
        ("text", ".txt", "text/plain"),
        ("csv", ".csv", "text/csv"),
        ("json", ".json", "application/json"),
    ],
)
def test_format_metadata(fmt, ext, mime):  # AC4
    assert file_extension(fmt) == ext
    assert mime_type(fmt) == mime
    assert "coffee" in render_report(sample(), fmt)


def test_unknown_format_rejected():
    with pytest.raises(ValueError):
        render_report(sample(), "xml")
