"""Checks that pass from the start: the project's set-up is in place."""

import importlib

import pytest

import config
from labels import CATEGORIES, URGENCIES


@pytest.mark.parametrize(
    "module", ["config", "load", "labels", "label", "evaluate", "cost_report", "check_validation", "judge"]
)
def test_every_module_imports(module):
    importlib.import_module(module)


def test_categories_match_the_kit():
    assert len(CATEGORIES) == 8
    assert set(URGENCIES) == {"low", "medium", "high"}


def test_prompt_file_exists():
    assert (config.PROMPTS_DIR / f"{config.PROMPT_VERSION}.txt").is_file()


def test_env_example_holds_no_secret():
    lines = (config.BASE_DIR / ".env.example").read_text(encoding="utf-8").splitlines()
    for line in lines:
        if line and not line.startswith("#"):
            name, _, value = line.partition("=")
            assert value == "", f"{name} must have nothing after = in .env.example"
