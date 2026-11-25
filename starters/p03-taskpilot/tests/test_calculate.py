"""Tests for calculate. You write the bodies in task 6, then remove the skips.

Run them with: uv run python -m pytest -q
"""

import pytest

from tools import calculate  # noqa: F401


@pytest.mark.skip(reason="TODO(task 6)")
def test_precedence():
    """2+3*4 gives 14."""
    raise NotImplementedError("TODO(task 6): assert calculate gives 14 for 2+3*4")


@pytest.mark.skip(reason="TODO(task 6)")
def test_refuses_code():
    """__import__('os') is refused with ValueError (use pytest.raises)."""
    raise NotImplementedError("TODO(task 6): assert __import__('os') is refused")
