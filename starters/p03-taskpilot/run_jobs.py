"""Run TaskPilot on the 10 scripted jobs in jobs.json and record each run (task 15).

    uv run --env-file .env python run_jobs.py

jobs.json is a JSON list that you write, one object per job:
    {"id": "j01", "job": "<the job text>",
     "check": {"tools": ["<tool name>"], "answer_has": ["<key number or word>"], "email_to": "<address, email job only>"}}

Success is judged in code, from the trace, the answer and the Mailpit API.
Never ask a model whether a job succeeded.
"""

import csv  # noqa: F401  (results/jobs.csv)
import json  # noqa: F401  (jobs.json, the trace lines, the Mailpit API)
import time  # noqa: F401  (seconds per job)
import urllib.request  # noqa: F401  (the Mailpit API, with no new package)
from pathlib import Path

JOBS_FILE = Path("jobs.json")
RESULTS_FILE = Path("results/jobs.csv")
MAILPIT_MESSAGES = "http://localhost:8025/api/v1/messages"
COLUMNS = ["id", "success", "steps", "input_tokens", "output_tokens", "cost_usd", "seconds", "stop"]


def clear_mailpit() -> None:
    """Delete every message in Mailpit before a job: a DELETE request to MAILPIT_MESSAGES.

    Use urllib.request.Request(url, method="DELETE"). See the kit's mailpit/README.md.
    """
    raise NotImplementedError("TODO(task 15): DELETE every Mailpit message")


def mailpit_recipients() -> list[str]:
    """Return the addresses of every message now in Mailpit (one entry per message).

    Read GET MAILPIT_MESSAGES; each message's "To" is a list of {"Name", "Address"}.
    """
    raise NotImplementedError("TODO(task 15): read the recipients from the Mailpit API")


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    """The cost of a run in US dollars, from PRICES (agent.py), which are per 1M tokens.

    Task 17: a cached call costs 0, so count only the tokens of calls that reached the API.
    """
    raise NotImplementedError("TODO(task 15): tokens times the price per 1M tokens")


def judge(job: dict, answer: str, trace: list[dict], recipients: list[str]) -> bool:
    """Decide in code whether one job succeeded.

    Success means all three:
    - every tool in job["check"]["tools"] appears in the trace;
    - the answer contains every string in job["check"]["answer_has"];
    - for an email job (it has "email_to"), Mailpit holds exactly one message, to that address.
    """
    raise NotImplementedError("TODO(task 15): judge the job from the trace, the answer and Mailpit")


def main() -> None:
    """For each job: clear Mailpit, run the agent with ask=lambda _: "y", time it, read its trace, judge it.

    Write results/jobs.csv with COLUMNS, one row per job, and print the totals:
    successes out of 10, total cost, average steps and the slowest job.
    From task 9 the agent is async and needs the MCP client: reuse what main.py does.
    """
    raise NotImplementedError("TODO(task 15): run the 10 jobs and write results/jobs.csv")


if __name__ == "__main__":
    main()
