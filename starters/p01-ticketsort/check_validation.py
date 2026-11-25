"""Prove the validator: bad answers must be rejected, each naming the right field.

Run: uv run check_validation.py
"""

from pydantic import ValidationError  # noqa: F401

from labels import TicketLabel  # noqa: F401


def main() -> None:
    """Pass at least three bad JSON answers to TicketLabel.model_validate_json: an unknown
    category, no urgency, and a 300-character summary. Print each ValidationError and check
    that it names the right field."""
    raise NotImplementedError("TODO(task 11): write three bad answers and print each error")


if __name__ == "__main__":
    main()
