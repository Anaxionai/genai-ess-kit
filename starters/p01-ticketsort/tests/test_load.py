"""Tests for load.py. Remove each skip when you have written the code it names."""

import pytest

from load import load_tickets, summary

HEADER = "id,text,category,urgency,summary,channel,created_at,order_id,alt_category\n"
ROWS = (
    'T0001,"Subject: Late | Where is order 123456, please?",delivery,medium,s,email,2026-11-02 10:00,123456,\n'
    "T0002,the blender sparked,damaged_or_wrong,high,s,chat,2026-11-02 11:00,,\n"
    "T0003,Does the kettle come in red?,product_question,low,s,web_form,2026-11-02 12:00,,\n"
)


@pytest.fixture
def tickets_csv(tmp_path):
    path = tmp_path / "tickets.csv"
    path.write_text(HEADER + ROWS, encoding="utf-8", newline="")
    return path


@pytest.mark.skip(reason="TODO(task 9)")
def test_load_tickets_reads_every_row(tickets_csv):
    tickets = load_tickets(tickets_csv)
    assert len(tickets) == 3
    assert tickets[0]["id"] == "T0001"
    assert tickets[0]["text"] == "Subject: Late | Where is order 123456, please?"  # comma inside quotes
    assert tickets[1]["category"] == "damaged_or_wrong"


@pytest.mark.skip(reason="TODO(task 9)")
def test_summary_counts_add_up(tickets_csv):
    result = summary(load_tickets(tickets_csv))
    assert result["count"] == 3
    assert sum(result["by_category"].values()) == 3
    assert sum(result["by_urgency"].values()) == 3
    assert result["by_urgency"]["high"] == 1


@pytest.mark.skip(reason="TODO(task 9)")
def test_summary_average_length():
    tickets = [{"text": "ab", "category": "return", "urgency": "low"},
               {"text": "abcd", "category": "return", "urgency": "low"}]
    assert summary(tickets)["average_length"] == 3
