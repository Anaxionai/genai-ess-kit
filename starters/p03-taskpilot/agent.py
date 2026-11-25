"""TaskPilot's agent loop: the model asks for a tool, your code runs it, until an answer or the step limit.

You write the loop yourself (no framework, no automatic function calling).
The Interactions API shapes are in the kit's models.md, "Function calling".
"""

import json  # noqa: F401  (task 7: one JSON line per step)
import os  # noqa: F401  (CHAT_MODEL; task 17: TASKPILOT_MODEL)
import uuid  # noqa: F401  (task 7: the run id, uuid.uuid4().hex[:8])
from pathlib import Path

from google import genai  # noqa: F401  (genai.Client() finds GEMINI_API_KEY in the environment)

TRACES_DIR = Path("traces")

# TODO(task 7): the system instruction: an office assistant that uses tools.
# TODO(task 8): add the calendar's week (11 to 15 January 2027) so the model can turn "Tuesday" into a date.
SYSTEM_INSTRUCTION = ""

# TODO(task 15): the paid-tier price per 1M tokens of each model you run, from the pricing page,
# and the date you read it, for example {"<model name>": {"input": 0.0, "output": 0.0}}  # read on <date>
PRICES: dict[str, dict[str, float]] = {}


def run_agent(job: str, max_steps: int = 6) -> dict:
    """Run one job: call the model, run the tools it asks for, until it answers or max_steps is reached.

    Task 7 (the loop):
    - Step 1 sends `job` as `input`, with `tools=TOOLS` and `system_instruction`.
    - `for step in range(1, max_steps + 1):`. From step 2 on, `input` is the list
      of `function_result` items and `previous_interaction_id` is the last reply's id.
      Leave `store` at its default (the chain needs it). Never set temperature.
    - No step with `type == "function_call"`: return
      `{"answer": interaction.output_text, "steps": step, "stop": "answer"}`.
    - Otherwise run every call and send one `function_result` per call, with its
      own `call_id`, all in one `input` list. A tool that raises sends its error
      text as the result: one bad call never crashes the run.
    - After the loop: answer "I stopped after N steps without finishing.", stop "step_limit".
    - Trace: `traces/<run id>.jsonl`, one JSON line per step with `step`, `tool`,
      `args`, `result` (first 200 characters), `input_tokens`, `output_tokens`
      (from `interaction.usage.total_input_tokens` / `total_output_tokens`) and
      the step's interaction id. The last line has `tool: null`, `stop` and `answer`.
      Return the trace path too, so main.py can print it.

    Task 8 (guards): add an `ask=input` parameter. Before `send_email` runs, call
    `check_email`, then `confirm_email(args, ask)`; on a refusal send an error
    result and do not send. That step's trace line gets `guard`: `allowed`,
    `refused: <reason>` or `declined by user`.

    Task 9 (MCP): becomes `async def run_agent(job, tools, call_tool, ask=input, max_steps=6)`,
    calls `await gemini.aio.interactions.create(...)` and runs every tool with
    `await call_tool(name, args)`. The guards stay here, before send_email.
    The first trace line records the client's protocol version.

    Task 16 (fixes): offer send_email only when the job asks for an email, and
    wrap every tool result as data (see guards.py).

    Task 17 (cost): call `cached_create` (cache.py) instead of the API, add
    `"cached": true/false` to each trace line, set
    `generation_config={"max_output_tokens": N}` and choose the model with
    `os.environ.get("TASKPILOT_MODEL") or os.environ["CHAT_MODEL"]`.

    Returns a dict with at least `answer`, `steps`, `stop` ("answer" or "step_limit").
    """
    raise NotImplementedError(
        "TODO(task 7): the agent loop with a step limit and a JSONL trace; "
        "TODO(task 8): ask=input and the email guards; TODO(task 9): async with call_tool; "
        "TODO(task 16): tools per job and results as data; TODO(task 17): cached_create, max_output_tokens, TASKPILOT_MODEL"
    )
