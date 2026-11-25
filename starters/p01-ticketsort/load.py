"""Load the support tickets and print a summary of what is in them.

Run: uv run load.py
"""

import csv  # noqa: F401
from pathlib import Path

import config

Ticket = dict[str, str]  # one CSV row: id, text, category, urgency, summary, channel, ...


def load_tickets(path: str | Path) -> list[Ticket]:
    """Return every row of the tickets CSV file as a dictionary.

    Input: the path of a CSV file made by the kit's make_tickets.py, with the columns
    id, text, category, urgency, summary, channel, created_at, order_id and alt_category.
    Output: a list with one dictionary per ticket, keyed by those column names, in file order.

    Edge cases the check looks at:
    - Use csv.DictReader.
    - Open the file with newline="" and encoding="utf-8", so a text with a comma, a quote or
      a line break stays one ticket, and 200 tickets give 200 dictionaries.
    """
    raise NotImplementedError("TODO(task 9): read the rows with csv.DictReader")


def summary(tickets: list[Ticket]) -> dict:
    """Summarise the tickets.

    Input: the list from load_tickets.
    Output: a dictionary with these keys:
    - "count": the number of tickets (int);
    - "by_category": the number of tickets per category, such as {"delivery": 31, ...};
    - "by_urgency": the number of tickets per urgency, such as {"low": 80, ...};
    - "average_length": the average length of "text" in characters (float).

    Edge cases: the category counts add up to "count", and so do the urgency counts.
    """
    raise NotImplementedError("TODO(task 9): count the tickets, per category and per urgency")


def main() -> None:
    """Print the summary of data/tickets.csv.

    Print the count, the categories sorted by count (largest first), the urgencies and the
    average length. Then print the three shortest ticket texts and the longest one.
    """
    raise NotImplementedError("TODO(task 9): load config.DATA_PATH and print the summary")


if __name__ == "__main__":
    main()
