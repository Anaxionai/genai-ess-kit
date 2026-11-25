"""Score TicketSort's labels against the true labels in data/tickets.csv.

Run: uv run evaluate.py results/labels_v1.csv   (writes results/eval_v1.md)
"""

import sys  # noqa: F401
from pathlib import Path

import config  # noqa: F401
from labels import CATEGORIES, URGENCIES  # noqa: F401
from load import Ticket, load_tickets  # noqa: F401

# TODO(task 20): write the score's definition here, in your own words: label accuracy is the
# correct labels divided by 400, because each of the 200 tickets has two labels.

MISSING = "(missing)"  # the predicted value for a ticket that is missing or failed

Matrix = dict[tuple[str, str], int]  # (true label, predicted label) -> count


def load_predictions(path: str | Path) -> dict[str, dict[str, str]]:
    """Read a labels file (id, category, urgency, summary) into {ticket id: row}."""
    raise NotImplementedError("TODO(task 20): read the predictions, keyed by ticket id")


def score(tickets: list[Ticket], predictions: dict[str, dict[str, str]]) -> dict[str, float]:
    """Compare the predictions with the true labels.

    Inputs: every ticket (the truth) and the predictions from load_predictions.
    Output: {"category": ..., "urgency": ..., "label": ...}, each a percentage rounded to one
    decimal place. "label" counts category and urgency together, out of 2 * len(tickets).

    Edge cases the check looks at:
    - Join by ticket id, never by row order.
    - A ticket with no prediction (missing or failed) counts as wrong, so divide by the
      number of tickets, not the number of predictions.
    """
    raise NotImplementedError("TODO(task 20): join by id and compute the three accuracies")


def confusion(truth: list[str], pred: list[str]) -> Matrix:
    """Count every (true, predicted) pair. truth and pred are lists of the same length.

    Use MISSING as the predicted value for a missing ticket, so the counts add up to the number
    of tickets and the diagonal divided by that number equals the accuracy.
    """
    raise NotImplementedError("TODO(task 20): count the (true, predicted) pairs")


def to_markdown(matrix: Matrix, labels: list[str]) -> str:
    """Turn a confusion matrix into a Markdown table: one row per true label, one column per
    predicted label (add a MISSING column when there are missing tickets)."""
    raise NotImplementedError("TODO(task 20): write the matrix as a Markdown table")


def main() -> None:
    """Read the labels file named in sys.argv[1] and write its evaluation.

    results/labels_v1.csv gives results/eval_v1.md; results/labels_local.csv gives
    results/eval_local.md. The file holds the three accuracies, the category matrix, the
    urgency matrix and 10 wrong tickets with their true and predicted labels. You add the
    ## Findings section by hand.
    """
    raise NotImplementedError("TODO(task 20): score the file and write results/eval_<name>.md")


if __name__ == "__main__":
    main()
