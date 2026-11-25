"""A cache for model calls: the same arguments never pay twice (task 17).

One JSON file per key in cache/. TASKPILOT_CACHE=0 turns it off.
"""

import hashlib  # noqa: F401  (SHA-256 of the arguments)
import json  # noqa: F401  (the key text and the cache files)
import os  # noqa: F401  (TASKPILOT_CACHE)
from pathlib import Path

CACHE_DIR = Path("cache")


def cache_key(kwargs: dict) -> str:
    """The cache key for one call: the SHA-256 hex digest of json.dumps(kwargs, sort_keys=True).

    Every argument counts (model, input, previous_interaction_id, tools,
    system_instruction, generation_config), so changing any of them gives a new
    key and the same arguments always give the same key. Nothing that changes
    on every run (a run id, a time) may go into the call.
    """
    raise NotImplementedError("TODO(task 17): SHA-256 of the sorted JSON of every argument")


def cached_create(**kwargs) -> dict:
    """Takes the same arguments as interactions.create and returns a plain dict.

    On a hit, read cache/<key>.json. On a miss (or with TASKPILOT_CACHE=0),
    call the API and save, then return,
    `{"id": ..., "steps": [step.model_dump(mode="json") ...], "output_text": ..., "usage": {...}, "cached": False}`.
    run_agent reads this dict whether it came from the cache or the API, and a
    cached call costs 0.
    Your run_agent is async from task 9: you may make this `async def` and
    await `gemini.aio.interactions.create(**kwargs)`.
    """
    raise NotImplementedError("TODO(task 17): return the cached reply, or call the API and save it")
