import argparse
import sys

from . import storage
from .report import file_extension, render_report
from .tracker import ExpenseTracker


def main(argv=None):
    parser = argparse.ArgumentParser(prog="expense-tracker")
    parser.add_argument("--file", default=storage.DEFAULT_PATH)
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("description")
    p_add.add_argument("amount")
    p_add.add_argument("category")

    sub.add_parser("list")
    sub.add_parser("total")

    p_export = sub.add_parser("export")
    p_export.add_argument("--format", default="text")
    p_export.add_argument("--out")

    args = parser.parse_args(argv)
    tracker = ExpenseTracker(storage.load(args.file))

    if args.command == "add":
        try:
            tracker.add(args.description, args.amount, args.category)
        except ValueError as exc:
            parser.error(str(exc))
        storage.save(tracker.expenses, args.file)
        print("added")
    elif args.command == "list":
        for i, e in enumerate(tracker.expenses):
            print(f"{i}: {e['category']} {e['description']} {e['amount']:.2f}")
    elif args.command == "total":
        print(f"{tracker.total():.2f}")
    elif args.command == "export":
        text = render_report(tracker, args.format)
        out = args.out or "report" + file_extension(args.format)
        with open(out, "w") as f:
            f.write(text)
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
