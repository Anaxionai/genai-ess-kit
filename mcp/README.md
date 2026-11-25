# MCP: serve your tools so any client can discover them

The **Model Context Protocol (MCP)** is an open standard for offering tools (and data) to AI applications. An **MCP server** lists its tools, with a name, a description and an input schema; an **MCP client** connects, discovers the tools and calls them. TaskPilot (P3) serves its tools from your own MCP server and calls them from your agent loop.

**Checked on 24 November 2026:**

- The current specification revision is **`2026-07-28`** (https://modelcontextprotocol.io/specification/latest).
- The official **MCP Python SDK is version 2**: PyPI `mcp` **2.3.0** (see [`../VERSIONS.md`](../VERSIONS.md)). Version 2 renamed the server class: `from mcp.server import MCPServer`. Tutorials that import `FastMCP` from `mcp.server.fastmcp` are written for version 1; do not mix them.
- The **MCP Inspector** is `@modelcontextprotocol/inspector` **2.16.0** on npm. It needs Node.js 22.23.4+, 24.22.1+ or 26.12.1+ ([`../setup/windows.md`](../setup/windows.md), "Later: Node.js").

Every example below was run on that date on Windows in Git Bash: the server, the client, `uv run mcp dev` and the Inspector's command-line mode.

## 1. Add the SDK to your project

In your project folder (for example `taskpilot/`):

```bash
uv add "mcp[cli]==2.3.0"
```

The `[cli]` extra adds the `mcp` command (`mcp dev`, `mcp run`).

## 2. A server with one tool

`server.py`:

```python
"""A tiny MCP server with one tool, over stdio."""
from mcp.server import MCPServer

mcp = MCPServer("calculator")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b


if __name__ == "__main__":
    mcp.run()  # stdio is the default transport
```

- The **docstring becomes the tool's description**, and the **type hints become its input schema** (`a` and `b` are numbers, both required). The model reads both, so write them for the model.
- The return value is sent back as text, and also as structured content (`{"result": 5.0}`) because the return type is declared.
- **Never `print()` in a stdio server.** Standard output *is* the connection: a stray print breaks the protocol. Log to standard error instead: `print("...", file=sys.stderr)` or the `logging` module.

## 3. Try it in the MCP Inspector

```bash
uv run mcp dev server.py
```

`mcp dev` starts the Inspector (it downloads it with `npx` the first time) and prints an address such as `http://127.0.0.1:6274?MCP_INSPECTOR_API_TOKEN=...`. Open that exact address, including the token. Then:

1. Select **Connect**.
2. Open the **Tools** tab and select **List tools**. You see `add`, its description and its input schema.
3. Select `add`, type 2 and 3, and run it. The result is `5.0`, with the JSON-RPC messages shown in the side panel.

Stop it with Ctrl+C. You can also start the Inspector yourself, with any command that starts your server:

```bash
npx @modelcontextprotocol/inspector@2.16.0 uv run server.py
npx @modelcontextprotocol/inspector@2.16.0 --cli uv run server.py --method tools/list
```

The second line is the Inspector's command-line mode: it prints the tool list as JSON and exits, which is handy for pasting into `evidence.md`.

## 4. A client that starts the server and calls a tool

`client.py`:

```python
"""Start server.py over stdio, list its tools and call one."""
import asyncio
import os
import sys

from mcp import Client, StdioServerParameters


async def main() -> None:
    server = StdioServerParameters(
        command=sys.executable,          # the same Python that runs this client
        args=["server.py"],
        env=dict(os.environ),            # pass your settings on (see below)
    )
    async with Client(server) as client:
        tools = await client.list_tools()
        for tool in tools.tools:
            print("tool:", tool.name, "-", tool.description)
        result = await client.call_tool("add", {"a": 2, "b": 3})
        print("structured:", result.structured_content)                     # {'result': 5.0}
        print("text:", [c.text for c in result.content if c.type == "text"])  # ['5.0']
        print("protocol:", client.protocol_version)                          # 2026-07-28


asyncio.run(main())
```

Run it with `uv run client.py`. The output, from our run:

```text
tool: add - Add two numbers and return the sum.
structured: {'result': 5.0}
text: ['5.0']
protocol: 2026-07-28
```

### The environment is not passed on by itself

A stdio server is a **child process**. The SDK starts it with only a few safe variables (such as `PATH`), **not** your `GEMINI_API_KEY`, `CHAT_MODEL` or `CALENDAR_FILE`. We checked: without `env=`, a variable set in the client was missing in the server. Pass the ones the server needs with `env=` (as above), or load `.env` inside the server itself. If a tool says it cannot find the API key or a file, a variable is missing from `env=`.

### Turning MCP tools into Gemini tools

`list_tools()` gives each tool's `name`, `description` and `input_schema` (a JSON Schema; version 1 called it `inputSchema`). That is almost exactly the function declaration the Gemini Interactions API wants:

```python
declarations = [
    {"type": "function", "name": t.name, "description": t.description or "",
     "parameters": t.input_schema}
    for t in tools.tools
]
```

When the model asks for a tool, call `await client.call_tool(step.name, step.arguments)` and send the text back as the `function_result`. [`../models.md`](../models.md) shows the shape of a function call and its result.

## 5. Transports

- **stdio** (the default, used above): the client starts the server as a child process on the same laptop. Use it for TaskPilot.
- **Streamable HTTP**: the server runs on its own and clients connect to a URL, such as `http://localhost:8000/mcp`. Start it with `uv run mcp run server.py --transport streamable-http`, and connect with `Client("http://localhost:8000/mcp")`. Useful when the server runs in another container.

## 6. Safety

MCP makes tools easy to discover, not safe to use. The specification says hosts must get the user's consent before invoking a tool, and that tool descriptions from a server you do not trust are themselves untrusted. Your guards (allow-lists, confirmation before email, step limits) stay in **your** code, around every `call_tool`.

## Sources (read on 24 November 2026)

- Specification, revision 2026-07-28: https://modelcontextprotocol.io/specification/latest
- MCP Inspector: https://modelcontextprotocol.io/docs/tools/inspector
- Python SDK: https://github.com/modelcontextprotocol/python-sdk and https://pypi.org/project/mcp/
- Inspector package: https://www.npmjs.com/package/@modelcontextprotocol/inspector
