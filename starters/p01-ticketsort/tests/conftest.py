"""Shared test set-up: a fake model client, so no test calls the real API.

pytest loads this file before the tests in this folder. Everything here is yours to write in
task 23; until then no test uses it, because those tests are skipped.
"""

import types  # noqa: F401  (types.SimpleNamespace builds the fake answers)

import pytest


def fake_answer(output_text: str, input_tokens: int = 100, output_tokens: int = 20):
    """Return an object shaped like an interaction: a types.SimpleNamespace with output_text
    and a usage holding total_input_tokens, total_output_tokens and total_tokens."""
    raise NotImplementedError("TODO(task 23): build a fake answer with types.SimpleNamespace")


class FakeClient:
    """A stand-in for genai.Client with scripted answers.

    FakeClient(items) takes a list. Each call to client.interactions.create(**kwargs) returns
    the next item; if the item is an exception, it raises it instead. Keep every kwargs it was
    called with, so a test can check what was sent and how many calls were made.
    """

    def __init__(self, items: list) -> None:
        raise NotImplementedError("TODO(task 23): give the fake an interactions.create that "
                                  "returns or raises the next scripted item")


# TODO(task 23): write FakeRateLimit(Exception) with status_code = 429, and a second error class
# with status_code = 400, for the backoff tests.


@pytest.fixture
def fake_client():
    """Return a function that makes a FakeClient from a list of scripted items."""
    raise NotImplementedError("TODO(task 23): return a FakeClient maker")
