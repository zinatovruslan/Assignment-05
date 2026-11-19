# Expense Tracker

Small command-line expense tracker (Python).

## Setup

    pip install -r requirements.txt

## Usage

    python -m expense_tracker.cli add coffee 3.50 food
    python -m expense_tracker.cli list
    python -m expense_tracker.cli total
    python -m expense_tracker.cli export --format csv

## Tests

    pytest
