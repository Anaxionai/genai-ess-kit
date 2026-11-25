"""Tests for the cache key. Remove the skips when you write cache.py in task 17."""

import pytest

from cache import cache_key

CALL = {
    "model": "chat-model",
    "input": "What is 2+3*4?",
    "tools": [{"type": "function", "name": "calculate"}],
    "generation_config": {"max_output_tokens": 400},
}


@pytest.mark.skip(reason="TODO(task 17)")
def test_same_arguments_same_key():
    assert cache_key(dict(CALL)) == cache_key(dict(reversed(list(CALL.items()))))


@pytest.mark.skip(reason="TODO(task 17)")
def test_every_argument_changes_the_key():
    base = cache_key(CALL)
    assert cache_key({**CALL, "model": "small-model"}) != base
    assert cache_key({**CALL, "previous_interaction_id": "abc"}) != base
    assert cache_key({**CALL, "generation_config": {"max_output_tokens": 500}}) != base
