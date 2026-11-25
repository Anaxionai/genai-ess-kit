"""Tests for the MCP conversions, with stand-in objects: no server, no network.

Remove the skips when you write mcp_tools.py in task 9.
"""

from types import SimpleNamespace

import pytest

from mcp_tools import declarations, result_text

SCHEMA = {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}


@pytest.mark.skip(reason="TODO(task 9)")
def test_declarations_from_list_tools():
    listed = SimpleNamespace(tools=[
        SimpleNamespace(name="calculate", description="Work out a sum.", input_schema=SCHEMA),
        SimpleNamespace(name="list_meetings", description=None, input_schema={"type": "object"}),
    ])
    assert declarations(listed) == [
        {"type": "function", "name": "calculate", "description": "Work out a sum.", "parameters": SCHEMA},
        {"type": "function", "name": "list_meetings", "description": "", "parameters": {"type": "object"}},
    ]


@pytest.mark.skip(reason="TODO(task 9)")
def test_result_text_joins_text_blocks():
    result = SimpleNamespace(
        content=[
            SimpleNamespace(type="text", text="first"),
            SimpleNamespace(type="image", data="..."),
            SimpleNamespace(type="text", text="second"),
        ],
        is_error=False,
    )
    assert result_text(result) == ("first\nsecond", False)


@pytest.mark.skip(reason="TODO(task 9)")
def test_result_text_passes_on_errors():
    result = SimpleNamespace(content=[SimpleNamespace(type="text", text="no such date")], is_error=True)
    assert result_text(result) == ("no such date", True)
