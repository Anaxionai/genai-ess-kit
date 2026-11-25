"""Tests for label.py with the fake client from conftest.py. You write these in task 23.

Rules: no test calls the real API, and no test sleeps for real. Replace the sleep with
monkeypatch.setattr (record the waits in a list instead), and use tmp_path for every file
a test writes (failed.csv, the cost log, the labels file).
Remove each skip when you have written the test.
"""

import pytest

import label  # noqa: F401


@pytest.mark.skip(reason="TODO(task 23)")
def test_valid_answer_returns_a_label(fake_client):
    """1. A valid JSON answer returns a TicketLabel with the right fields."""
    raise NotImplementedError("TODO(task 23)")


@pytest.mark.skip(reason="TODO(task 23)")
def test_invalid_then_valid_answer_retries_once(fake_client):
    """2. An answer with a category not in the list, then a valid one, returns the valid label
    after one retry."""
    raise NotImplementedError("TODO(task 23)")


@pytest.mark.skip(reason="TODO(task 23)")
def test_three_invalid_answers_go_to_failed_csv(fake_client, tmp_path, monkeypatch):
    """3. Three invalid answers return None and write the ticket to failed.csv in tmp_path,
    not to the labels file."""
    raise NotImplementedError("TODO(task 23)")


@pytest.mark.skip(reason="TODO(task 23)")
def test_rate_limit_is_retried_with_growing_waits(fake_client, monkeypatch):
    """4. FakeRateLimit (429) twice, then a valid answer, succeeds, and the recorded waits grow."""
    raise NotImplementedError("TODO(task 23)")


@pytest.mark.skip(reason="TODO(task 23)")
def test_a_400_error_is_raised_at_once(fake_client, monkeypatch):
    """5. A 400 error is raised at once, with no retry and no wait."""
    raise NotImplementedError("TODO(task 23)")


@pytest.mark.skip(reason="TODO(task 23)")
def test_label_all_skips_ids_already_labelled(fake_client, tmp_path, monkeypatch):
    """6. With a results file that already holds two ids, label_all labels only the others."""
    raise NotImplementedError("TODO(task 23)")
