"""Run TaskPilot on one job from the command line.

    uv run --env-file .env python main.py "What is 18% of 42,500?"

The job is the command-line text (`" ".join(sys.argv[1:])`), so the Compose
run in task 18 works the same way: docker compose run --rm taskpilot "<job>".
"""

import asyncio  # noqa: F401  (task 9: asyncio.run(main()))
import os  # noqa: F401  (CHAT_MODEL; task 9: the server's environment)
import sys  # noqa: F401  (the job from the command line)

# The names of the settings the MCP server needs. The server is a child process
# and does NOT inherit your environment, so main.py passes these on with
# env={k: os.environ[k] for k in SERVER_ENV if k in os.environ}. If a tool cannot find the key,
# the index or the calendar, its name is missing here.
# TODO(task 9): list them (key, models, chunk settings, SMTP, calendar). TODO(task 16): add DOCS_COLLECTION.
SERVER_ENV: list[str] = []


def main() -> None:
    """Answer one job and print the result. It grows over three tasks.

    Task 6 (one round trip): `client.interactions.create(model=os.environ["CHAT_MODEL"],
    input=question, tools=TOOLS)`; run each `function_call` step's function with
    `step.arguments`; send each result back with `previous_interaction_id=interaction.id`
    and a `function_result` (`name`, `call_id=step.id`, the result as text);
    print `output_text`. Print the tool calls too: you paste them into evidence.md.

    Task 7: call `run_agent(job)` instead, and print the answer and the trace path.

    Task 9 (MCP): make this `async def main()` and start it with `asyncio.run(main())`.
    Open `Client(StdioServerParameters(command="uv", args=["run", "mcp_server.py"],
    env={k: os.environ[k] for k in SERVER_ENV if k in os.environ}))`, print `client.protocol_version`,
    build the declarations from `await client.list_tools()` (mcp_tools.declarations)
    and pass them and `client.call_tool` to `run_agent`.
    """
    raise NotImplementedError(
        "TODO(task 6): one tool round trip; TODO(task 7): call run_agent; "
        "TODO(task 9): async main with an MCP Client over stdio"
    )


if __name__ == "__main__":
    main()
