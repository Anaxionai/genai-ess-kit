"""Label tickets with the chat model: one call per ticket, validated, retried, logged.

Run: uv run label.py

Rules from the course:
- The client is always passed in, never created inside label_ticket or label_all, so the tests
  in tests/ can pass a fake client instead (task 23).
- Every Gemini call uses client.interactions.create with store=False, and never sets
  temperature, top_p or top_k (the kit's models.md).
- Send the model only the ticket's "text", never its true labels.
"""

import csv  # noqa: F401
import random  # noqa: F401
import time  # noqa: F401
from collections.abc import Callable
from pathlib import Path
from typing import Any

from google import genai  # noqa: F401
from pydantic import ValidationError  # noqa: F401

import config
from labels import TicketLabel
from load import Ticket, load_tickets  # noqa: F401

# CSV files in results/ and their columns. They are committed as evidence.
LABEL_FIELDS = ["id", "category", "urgency", "summary"]  # results/labels_vN.csv
FAILED_PATH = config.RESULTS_DIR / "failed.csv"
FAILED_FIELDS = ["id", "raw_answer", "error"]
COST_LOG_PATH = config.RESULTS_DIR / "cost_log.csv"
COST_LOG_FIELDS = [
    "time",
    "ticket_id",
    "attempt",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "rupees",
]

MAX_RETRIES = 2  # after the first try: at most three calls per ticket (task 11)


def label_ticket(client, text: str, ticket_id: str = "") -> TicketLabel | None:
    """Ask the model for one ticket's label and return it validated.

    Inputs: a client with client.interactions.create (a genai.Client, or a fake in the tests),
    the ticket's text, and its id (used for failed.csv and the cost log).
    Output: a TicketLabel, or None when every attempt failed (from task 11).

    Task 10: one call with model=config.MODEL, the ticket text as input, your prompt file
    (config.PROMPTS_DIR / f"{config.PROMPT_VERSION}.txt") as system_instruction, store=False and
    response_format={"type": "text", "mime_type": "application/json",
    "schema": TicketLabel.model_json_schema()}. Return
    TicketLabel.model_validate_json(interaction.output_text).

    Task 11: catch ValidationError. Retry at most MAX_RETRIES more times, each with the ticket
    plus "Your last answer was invalid:" and the field and message of e.errors()[0] (loc, msg).
    (The first line of str(e) only says "1 validation error for TicketLabel".) If every attempt fails,
    append id, the last raw answer and the error to FAILED_PATH and return None. A failed
    ticket never goes to the labels file.

    Task 12: make each call through call_with_backoff.

    Task 13: after every call, retries included, append a row to COST_LOG_PATH with
    COST_LOG_FIELDS, reading interaction.usage (total_input_tokens, total_output_tokens,
    total_tokens) and cost_rupees(usage).
    """
    raise NotImplementedError("TODO(task 10): call the model with the schema and validate the answer")
    # TODO(task 11): retry a ValidationError at most twice, then record the ticket in failed.csv.
    # TODO(task 12): make each call through call_with_backoff.
    # TODO(task 13): append a cost_log.csv row after every call, retries included.


def label_all(client, tickets: list[Ticket], out_path: str | Path) -> dict[str, int]:
    """Label every ticket and write the labels to out_path (such as results/labels_v1.csv).

    Inputs: the client, the tickets from load_tickets, and the CSV file to write.
    Output: the counts {"first_try": ..., "after_retry": ..., "failed": ...}, also printed at
    the end of the run (task 11).

    Task 10: for each ticket, call label_ticket and write id, category, urgency and summary
    (LABEL_FIELDS) with csv.DictWriter. Pause time.sleep(60 / config.RPM) between calls.
    Create the results folder if it is missing.

    Task 12 (resume file): first read the ids already in out_path and skip those tickets.
    Append each new row as soon as its ticket is labelled, so a stopped run continues and
    no ticket is labelled twice. Write the header only when the file is new.
    """
    raise NotImplementedError("TODO(task 10): label each ticket, write the CSV, pause between calls")
    # TODO(task 11): count first-try, after-retry and failed labels and print them.
    # TODO(task 12): skip ids already in out_path; append each row as soon as it is labelled.


def is_retryable(error: Exception) -> bool:
    """Say whether an error is worth another try.

    True for a status_code of 429, 500 or 503 (read it with getattr(error, "status_code", None))
    and for a connection error (APIConnectionError in google.genai._interactions; see the kit's
    models.md). False for everything else: a 400-type error is never retried.
    """
    raise NotImplementedError("TODO(task 12): write this check yourself")


def call_with_backoff(fn: Callable[[], Any], max_tries: int = 5) -> Any:
    """Call fn() and retry it with growing waits while is_retryable(error) is true.

    Wait 2 ** attempt + random.uniform(0, 1) seconds, at most 60, and print the attempt, the
    error and the wait. Raise a non-retryable error at once. After max_tries, raise the last
    error. Chat AI may write this (the AI move); you test every claim and log it in AI_LOG.md.
    """
    raise NotImplementedError("TODO(task 12): exponential backoff with jitter, a cap and max_tries")


def cost_rupees(usage) -> float:
    """Return the rupee cost of one call from interaction.usage.

    (total_input_tokens * config.PRICE_IN + total_output_tokens * config.PRICE_OUT)
    / 1,000,000 * config.USD_TO_INR.
    """
    raise NotImplementedError("TODO(task 13): turn the usage into rupees with the prices in config.py")


def label_ticket_local(text: str) -> TicketLabel | None:
    """Label one ticket with the local model in Ollama (run `uv add ollama` first).

    Call ollama.chat with model=config.LOCAL_MODEL, your best prompt as the "system" message,
    the ticket as the "user" message, format=TicketLabel.model_json_schema() and
    options={"temperature": 0}. Validate response.message.content with TicketLabel, reuse your
    retry and failure handling, and log prompt_eval_count and eval_count as tokens and the
    seconds from time.perf_counter().
    """
    raise NotImplementedError("TODO(task 24): label with Ollama, the same schema and temperature 0")


def main() -> None:
    """Label the tickets in data/tickets.csv.

    Create the client here (genai.Client() reads GEMINI_API_KEY from the environment) and
    pass it in. First label one ticket and print its label beside its true labels; then
    label all tickets into config.RESULTS_DIR / f"labels_{config.PROMPT_VERSION}.csv".
    """
    raise NotImplementedError("TODO(task 10): create the client, label one ticket, then all")


if __name__ == "__main__":
    main()
