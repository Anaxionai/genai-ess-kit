"""TaskPilot's MCP server: serves the four tools from tools.py over stdio (task 9).

Try it with `uv run --env-file .env mcp dev mcp_server.py` (needs Node.js; see the kit's mcp/README.md).

Never print() in this file or in anything it imports: standard output carries
the protocol. Log to standard error (print(..., file=sys.stderr)) if you must.

The server runs whatever it is asked. The email guards stay in the agent.
"""

from mcp.server import MCPServer  # noqa: F401  (MCP Python SDK v2, the version in the kit's VERSIONS.md)

import tools  # noqa: F401  (each MCP tool calls the function of the same name in tools.py)

# TODO(task 9): create the server: mcp = MCPServer("taskpilot")

# TODO(task 9): write four typed @mcp.tool() functions, one for each tool in tools.py
# (search_docs, calculate, list_meetings, send_email). Each calls its tools.py function.
# The docstring becomes the tool's description and the type hints its input schema,
# so write both for the model.


if __name__ == "__main__":
    # TODO(task 9): run the server over stdio with mcp.run().
    raise NotImplementedError("TODO(task 9): create the MCPServer, register four tools and call mcp.run()")
