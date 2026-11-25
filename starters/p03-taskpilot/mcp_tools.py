"""Conversions between the MCP client and the Gemini Interactions API (task 9).

The shapes are in the kit's mcp/README.md ("Turning MCP tools into Gemini tools").
"""


def declarations(result) -> list[dict]:
    """Turn the result of `await client.list_tools()` into Gemini function declarations.

    Input: the list_tools result; its `.tools` each have `name`, `description`
    (may be None) and `input_schema` (a JSON Schema).
    Output: one dict per tool:
    `{"type": "function", "name": ..., "description": ..., "parameters": tool.input_schema}`,
    in the same order. A missing description becomes "".
    """
    raise NotImplementedError("TODO(task 9): one function declaration per MCP tool")


def result_text(result) -> tuple[str, bool]:
    """Read the result of `await client.call_tool(name, args)`.

    Input: the call_tool result: `content` (a list of blocks; the text ones have
    `type == "text"` and `text`) and `is_error`.
    Output: (the text of every text block joined with newlines, is_error).
    Blocks that are not text are skipped. The agent sends the text back as the
    function_result, and passes is_error on.
    The brief does not name this function; keep the name or use your own.
    """
    raise NotImplementedError("TODO(task 9): join the text blocks of result.content and return it with result.is_error")
