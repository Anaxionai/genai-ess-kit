"""Tests for TicketLabel. Remove each skip when you have written the code it names."""

import json

import pytest
from pydantic import ValidationError

from labels import CATEGORIES, TicketLabel

GOOD = {"category": "refund", "urgency": "medium", "summary": "Customer asks where the refund is."}


def answer(**changes) -> str:
    data = {**GOOD, **changes}
    return json.dumps({k: v for k, v in data.items() if v is not None})


@pytest.mark.skip(reason="TODO(task 10)")
def test_a_good_answer_is_accepted():
    label = TicketLabel.model_validate_json(answer())
    assert (label.category, label.urgency) == ("refund", "medium")


@pytest.mark.skip(reason="TODO(task 10)")
def test_the_schema_lists_the_choices_and_describes_each_field():
    schema = TicketLabel.model_json_schema()
    assert set(schema["properties"]["category"]["enum"]) == set(CATEGORIES)
    assert set(schema["properties"]["urgency"]["enum"]) == {"low", "medium", "high"}
    for field in ("category", "urgency", "summary"):
        assert schema["properties"][field].get("description")


@pytest.mark.skip(reason="TODO(task 10)")
def test_an_unknown_category_is_rejected():
    with pytest.raises(ValidationError, match="category"):
        TicketLabel.model_validate_json(answer(category="shipping"))


@pytest.mark.skip(reason="TODO(task 10)")
def test_a_missing_urgency_is_rejected():
    with pytest.raises(ValidationError, match="urgency"):
        TicketLabel.model_validate_json(answer(urgency=None))


@pytest.mark.skip(reason="TODO(task 11)")
def test_a_long_summary_is_rejected():
    with pytest.raises(ValidationError, match="summary"):
        TicketLabel.model_validate_json(answer(summary="x" * 300))
