"""The label a model gives one ticket, as a Pydantic model.

TicketSort sends TicketLabel.model_json_schema() as the response schema and checks every
answer with TicketLabel.model_validate_json(...).
"""

from typing import Literal  # noqa: F401  (you use it in TicketLabel)

from pydantic import BaseModel, Field  # noqa: F401  (you use Field in TicketLabel)

# The eight categories and three urgencies from the kit's data/tickets/README.md.
# evaluate.py uses them as the rows and columns of the confusion matrices.
CATEGORIES = (
    "delivery",
    "damaged_or_wrong",
    "return",
    "refund",
    "payment",
    "account",
    "order_change",
    "product_question",
)
URGENCIES = ("low", "medium", "high")


class TicketLabel(BaseModel):
    """One ticket's label: a category, an urgency and a one-line summary.

    TODO(task 10): add three fields, each with Field(description=...):
    - category: a Literal of the eight categories above. The description says what each means.
    - urgency: Literal["low", "medium", "high"]. The description says how to judge urgency.
    - summary: str. The description says "one line, at most 15 words".
    The descriptions go to the model inside the schema, so they are part of your prompt.

    TODO(task 11): give summary a maximum length with Field(..., max_length=120).
    The API does not check lengths; Pydantic does.

    Checks: an unknown category, a missing urgency or a 300-character summary must each raise
    pydantic.ValidationError that names the field.
    """
