"""Tests for load.py (task 7). Remove each skip when you write the test."""

import pytest

# Given: a small document in the handbook's header format, for tmp_path.
SAMPLE = """# Booking work travel
Department: Finance
Updated: 2026-01-12

## Flights

Flights under six hours are booked in economy class.
"""


@pytest.mark.skip(reason="TODO(task 7)")
def test_read_document_fields(tmp_path):
    """Write SAMPLE to tmp_path and check title, department and word count."""
    raise NotImplementedError("TODO(task 7): write this test")


@pytest.mark.skip(reason="TODO(task 7)")
def test_document_with_no_title_raises(tmp_path):
    """A file with no "# " title line raises ValueError naming the file."""
    raise NotImplementedError("TODO(task 7): write this test")
