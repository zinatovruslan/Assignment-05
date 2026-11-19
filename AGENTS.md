# AGENTS.md

## Purpose
Command-line expense tracker (Python 3.13, standard library only at runtime).
Stores expenses in a local JSON file; reports as text, CSV or JSON.

## Architecture
- `expense_tracker/tracker.py`: business logic (`ExpenseTracker`: add, remove, total, by_category). No I/O.
- `expense_tracker/storage.py`: JSON load/save. Only module that reads/writes the data file.
- `expense_tracker/report.py`: report rendering per output format.
- `expense_tracker/cli.py`: argparse CLI; parses arguments, calls the modules above, prints.
- `tests/`: pytest suite. Acceptance criteria are tagged `# ACn` in test comments.

## Setup
    pip install -r requirements.txt
    pip install ruff

## Safe commands (run without asking)
    python3 -m pytest -q
    python3 -m ruff check .
    git status / git diff / git log
    python3 -m expense_tracker.cli --file /tmp/demo.json <command>

## Acceptance criteria (must stay true after every change)
- AC1: an added expense is persisted to the JSON file and can be loaded back unchanged.
- AC2: `total` equals the sum of all expense amounts (printed with 2 decimals).
- AC3: `by_category` groups amounts by category.
- AC4: text, CSV and JSON reports can be generated and contain all expenses and the total.
- AC5: CLI `add` followed by `total` prints the added amount.

## Coding conventions
- Keep business logic out of `cli.py`. Keep I/O out of `tracker.py`.
- Small functions, type-obvious names, no new runtime dependencies without approval.
- Money is a currency amount; do not introduce new float arithmetic on money.
- One focused change per commit; commit message states the why.

## Test expectations
- Every behavior change needs a test in `tests/`. Bug fixes need a regression test.
- `pytest` and `ruff check .` must pass before a change is proposed.
- Never edit or delete existing tests to make them pass; report conflicts instead.

## Forbidden actions
- No real secrets, credentials, tokens or personal data in code, tests, fixtures or logs.
- No production deployment, publishing, or pushing to protected branches.
- No destructive commands (`rm -rf`, `git reset --hard`, `git push --force`, overwriting user data files).
- No adding, upgrading or removing dependencies without human review.
- No network access beyond the package index for approved installs.
- No changes outside the repository directory.

## Review gates
- A human reviews every diff before merge. The agent proposes; it does not merge.
- The agent reports: change summary, diff, test output, ruff output, remaining risks.
- If a check cannot be run, the agent states that explicitly. It never fabricates results.
