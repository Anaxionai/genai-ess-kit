"""Tests for answer.py (tasks 10, 11 and 22). They use a fake search and a
fake model, so they make no API calls. Remove each skip when you write the test."""

import pytest


@pytest.mark.skip(reason="TODO(task 10)")
def test_parse_citations():
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 10)")
def test_citation_never_sent_is_a_bad_citation():
    """Call answer() with a fake search and a fake model."""
    raise NotImplementedError("TODO(task 10): write this test")


@pytest.mark.skip(reason="TODO(task 11)")
def test_far_best_distance_makes_no_model_call():
    """Give the fake model a list to append to; assert it stays empty."""
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 11)")
def test_answer_with_no_citation_becomes_refusal():
    raise NotImplementedError("TODO(task 11): write this test")


@pytest.mark.skip(reason="TODO(task 22)")
def test_check_output_blocks_the_marker():
    raise NotImplementedError("TODO(task 22): write this test")


@pytest.mark.skip(reason="TODO(task 22)")
def test_passage_cannot_close_its_tag():
    raise NotImplementedError("TODO(task 22): write this test")
