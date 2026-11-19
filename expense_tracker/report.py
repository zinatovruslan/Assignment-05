import csv
import io
import json

FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def safe_cell(text):
    """Neutralize spreadsheet formula injection by prefixing an apostrophe."""
    return "'" + text if text.startswith(FORMULA_PREFIXES) else text


class ReportFormat:
    """Strategy: one subclass per output format."""

    name = ""
    extension = ""
    mime_type = ""

    def render(self, tracker):
        raise NotImplementedError


class TextFormat(ReportFormat):
    name = "text"
    extension = ".txt"
    mime_type = "text/plain"

    def render(self, tracker):
        lines = [
            f"{e['category']:<12} {e['description']:<20} {e['amount']:.2f}"
            for e in tracker.expenses
        ]
        lines.append(f"TOTAL {tracker.total():.2f}")
        return "\n".join(lines)


class CsvFormat(ReportFormat):
    name = "csv"
    extension = ".csv"
    mime_type = "text/csv"

    def render(self, tracker):
        buf = io.StringIO()
        writer = csv.writer(buf, lineterminator="\n")
        writer.writerow(["description", "amount", "category"])
        for e in tracker.expenses:
            writer.writerow(
                [safe_cell(e["description"]), e["amount"], safe_cell(e["category"])]
            )
        return buf.getvalue().rstrip("\n")


class JsonFormat(ReportFormat):
    name = "json"
    extension = ".json"
    mime_type = "application/json"

    def render(self, tracker):
        expenses = [{**e, "amount": float(e["amount"])} for e in tracker.expenses]
        return json.dumps(
            {"expenses": expenses, "total": float(tracker.total())}, indent=2
        )


FORMATS = {f.name: f for f in (TextFormat(), CsvFormat(), JsonFormat())}


def get_format(fmt):
    try:
        return FORMATS[fmt]
    except KeyError:
        raise ValueError(f"unknown format: {fmt}") from None


def render_report(tracker, fmt):
    return get_format(fmt).render(tracker)


def file_extension(fmt):
    return get_format(fmt).extension


def mime_type(fmt):
    return get_format(fmt).mime_type
