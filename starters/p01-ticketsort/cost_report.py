"""Turn results/cost_log.csv into a cost report.

Run: uv run cost_report.py
"""

import csv  # noqa: F401

from label import COST_LOG_PATH  # noqa: F401


def main() -> None:
    """Read the cost log and print the number of calls, the total input, output and total
    tokens, the total rupees, the rupees per ticket (count distinct ticket ids: retries are
    extra calls for the same ticket) and the five most expensive calls."""
    raise NotImplementedError("TODO(task 13): read the log and print the report")


if __name__ == "__main__":
    main()
