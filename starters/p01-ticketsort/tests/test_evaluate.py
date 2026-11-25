"""Tests for evaluate.py. Remove each skip when you have written the code it names."""

import pytest

from evaluate import MISSING, confusion, score, to_markdown

TRUTH = [
    {"id": "T0001", "category": "delivery", "urgency": "medium"},
    {"id": "T0002", "category": "refund", "urgency": "low"},
    {"id": "T0003", "category": "payment", "urgency": "high"},
    {"id": "T0004", "category": "return", "urgency": "low"},
]
# Not in ticket order on purpose, and T0004 is missing (a failed ticket).
PREDICTIONS = {
    "T0003": {"id": "T0003", "category": "payment", "urgency": "high"},
    "T0001": {"id": "T0001", "category": "delivery", "urgency": "medium"},
    "T0002": {"id": "T0002", "category": "payment", "urgency": "low"},
}


@pytest.mark.skip(reason="TODO(task 20)")
def test_score_joins_by_id_and_counts_missing_as_wrong():
    result = score(TRUTH, PREDICTIONS)
    assert result["category"] == 50.0  # T0001 and T0003 right; T0004 is missing, so out of 4
    assert result["urgency"] == 75.0  # T0001, T0002 and T0003 right
    assert result["label"] == 62.5  # 5 of 8 labels


@pytest.mark.skip(reason="TODO(task 20)")
def test_confusion_counts_pairs_and_adds_up():
    truth = ["delivery", "refund", "payment", "return"]
    pred = ["delivery", "payment", "payment", MISSING]
    matrix = confusion(truth, pred)
    assert matrix[("refund", "payment")] == 1
    assert matrix[("return", MISSING)] == 1
    assert sum(matrix.values()) == 4
    diagonal = sum(n for (t, p), n in matrix.items() if t == p)
    assert diagonal / 4 * 100 == 50.0  # the same as the category accuracy


@pytest.mark.skip(reason="TODO(task 20)")
def test_to_markdown_has_a_row_per_true_label():
    labels = ["delivery", "refund"]
    table = to_markdown({("delivery", "delivery"): 2, ("refund", "delivery"): 1}, labels)
    lines = [line for line in table.strip().splitlines() if line.startswith("|")]
    assert len(lines) == 2 + len(labels)  # header, separator, one row per label
    assert all(label in lines[0] for label in labels)
