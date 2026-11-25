"""Measure the search with your 25 test questions (task 18).

Run it from inside docanswer/:
    uv run --env-file .env python evaluate.py

Given: read_questions(). You write: hit_rate() and main().
"""

import csv
from pathlib import Path

QUESTIONS_FILE = Path("evalset/questions.csv")
RESULTS_DIR = Path("results")


def read_questions(path: Path = QUESTIONS_FILE) -> list[dict]:
    """Given: read the test set (id,question,expected_source) as a list of dicts."""
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def hit_rate(results: list[dict], k: int) -> float:
    """Return the share of questions whose expected source is in the first k passages.

    Input: one dict per question with expected_source and passages (the list
    from top_passages(), nearest first; each passage has a doc_id).
    Output: a number from 0.0 to 1.0.
    Pure: no search, no files. Decide what an empty list returns, and test it.
    """
    raise NotImplementedError("TODO(task 18): compute the hit rate at k")


def main() -> None:
    """Search every question with top_passages(question, k=3) and report.

    Print hits at 1 and at 3 as counts of 25, the ids of the misses and the
    mean words in the 3 passages. Save one row per question in
    results/retrieval-<collection>.csv: id, expected_source, the 3 doc_ids
    with their distances, and hit_at_3.
    """
    raise NotImplementedError("TODO(task 18): measure the search and save the results")


if __name__ == "__main__":
    main()
