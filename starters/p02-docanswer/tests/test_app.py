"""Tests for api.py (task 20). Run `import api`, replace api.answer with a fake
(monkeypatch.setattr(api, "answer", fake_answer)) and use
fastapi.testclient.TestClient(api.app), so no test calls a model.
Remove each skip when you write the test."""

import pytest


@pytest.mark.skip(reason="TODO(task 20)")
def test_health():
    raise NotImplementedError("TODO(task 20): write this test")


@pytest.mark.skip(reason="TODO(task 20)")
def test_good_question_returns_sources():
    raise NotImplementedError("TODO(task 20): write this test")


@pytest.mark.skip(reason="TODO(task 20)")
def test_too_short_question_is_422():
    raise NotImplementedError("TODO(task 20): write this test")


@pytest.mark.skip(reason="TODO(task 20)")
def test_model_failure_is_503():
    raise NotImplementedError("TODO(task 20): write this test")
