import json


def render_report(tracker, fmt):
    if fmt == "text":
        lines = [
            f"{e['category']:<12} {e['description']:<20} {e['amount']:.2f}"
            for e in tracker.expenses
        ]
        lines.append(f"TOTAL {tracker.total():.2f}")
        return "\n".join(lines)
    elif fmt == "csv":
        lines = ["description,amount,category"]
        for e in tracker.expenses:
            lines.append(f"{e['description']},{e['amount']},{e['category']}")
        return "\n".join(lines)
    elif fmt == "json":
        return json.dumps(
            {"expenses": tracker.expenses, "total": tracker.total()}, indent=2
        )
    else:
        raise ValueError(f"unknown format: {fmt}")


def file_extension(fmt):
    if fmt == "text":
        return ".txt"
    elif fmt == "csv":
        return ".csv"
    elif fmt == "json":
        return ".json"
    else:
        raise ValueError(f"unknown format: {fmt}")


def mime_type(fmt):
    if fmt == "text":
        return "text/plain"
    elif fmt == "csv":
        return "text/csv"
    elif fmt == "json":
        return "application/json"
    else:
        raise ValueError(f"unknown format: {fmt}")
