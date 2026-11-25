"""Checks that hold from the first day: the modules import, and the tools never use eval.

These pass now and must keep passing. They need no key, no model and no network.
"""

import ast
import importlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MODULES = ["tools", "agent", "guards", "mcp_tools", "mcp_server", "cache", "main", "run_jobs", "run_attacks"]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports_without_running(name):
    """Importing a module must not call a model, send an email or start a server."""
    importlib.import_module(name)


def test_no_taskpilot_file_hides_docanswer():
    """search.py, index.py or answer.py here would hide DocAnswer's own modules."""
    for name in ("search.py", "index.py", "answer.py"):
        assert not (ROOT / name).exists(), f"rename {name}: DocAnswer has a module of that name"


def test_tools_never_call_eval_or_exec():
    """The calculator parses with ast; eval and exec never appear as calls in tools.py."""
    tree = ast.parse((ROOT / "tools.py").read_text(encoding="utf-8"))
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert not calls & {"eval", "exec"}
