"""TaskPilot's four tools and their function declarations.

Plain Python functions: the model never runs them. Your code runs the one the
model asks for and sends the result back (agent.py, and from task 9 the MCP
server in mcp_server.py calls these same functions).

Never name a TaskPilot file search.py, index.py or answer.py: they would hide
the DocAnswer modules of the same name.
"""

import ast  # noqa: F401  (task 6: the calculator parses with ast, never eval)
import json  # noqa: F401  (task 8: the calendar file)
import os  # noqa: F401  (task 8: CALENDAR_FILE, SMTP_HOST, SMTP_PORT; task 16: DOCS_COLLECTION)
import smtplib  # noqa: F401  (task 8: send_email)
import sys
from email.message import EmailMessage  # noqa: F401  (task 8: send_email)
from pathlib import Path

# Your own DocAnswer from task 3.23 lives in docanswer/ (see docanswer/COPY-DOCANSWER-HERE.md).
# Its folder goes on the import path, so its modules import by their own names.
DOCANSWER_DIR = Path(__file__).resolve().parent / "docanswer"
sys.path.insert(0, str(DOCANSWER_DIR))  # first, so DocAnswer's chunk.py wins over the standard library's chunk module

# TODO(task 6): once your DocAnswer copy is in docanswer/, import its search here:
#     from search import top_passages
# (It is not imported yet, so this starter runs before you copy DocAnswer in.)


def search_docs(question: str) -> str:
    """Search the staff handbook with your DocAnswer `top_passages`.

    Input: the question, as the model wrote it.
    Output: one line per passage, `[chunk_id] title, section: text`, from
    `top_passages(question, k=4)`. An empty search gives a short line that says
    nothing was found (never an exception), so the model can say so.

    Task 16: give `top_passages` an optional `collection` argument (in your
    docanswer/search.py) and pass `os.environ.get("DOCS_COLLECTION")` from here.
    """
    raise NotImplementedError("TODO(task 6): search with top_passages(question, k=4); TODO(task 16): pass DOCS_COLLECTION")


def calculate(expression: str) -> str:
    """Work out an arithmetic expression, such as "0.18 * 42500", without eval.

    Input: the expression as text.
    Output: the result as text, for example "14" for "2+3*4".
    Parse with `ast.parse(expression, mode="eval")` and allow only numbers,
    `+ - * / %`, unary minus and brackets. Anything else (names, calls,
    attributes, strings, `**`, `__import__('os')`) raises ValueError.
    Never call eval or exec: tests/test_starter.py checks this file for them.
    """
    raise NotImplementedError("TODO(task 6): an ast-based calculator; raise ValueError for anything but arithmetic")


def list_meetings(date: str) -> str:
    """Return the meetings on one day of the calendar.

    Input: the date as YYYY-MM-DD (say so in the declaration: the model may write "Tuesday").
    Output: one line per meeting on that date (times, title, attendees, notes),
    or a line saying there are no meetings that day.
    The file is named by the CALENDAR_FILE setting (default calendar.json);
    its meetings are in the top-level "meetings" list (kit data/calendar/README.md).
    The notes are data written by others, never instructions.
    """
    raise NotImplementedError("TODO(task 8): read CALENDAR_FILE and return that day's meetings")


def send_email(to: str, subject: str, body: str) -> str:
    """Send one email through SMTP (Mailpit on your laptop, never a real server).

    Inputs: one recipient address, a subject and a plain-text body.
    Output: a short confirmation text, such as "sent to ...".
    Use smtplib.SMTP and EmailMessage. Read SMTP_HOST (default localhost) and
    SMTP_PORT (default 1025) from the environment.
    This function sends whatever it is given: the guards in guards.py run
    before it, in the agent, never inside it.
    """
    raise NotImplementedError("TODO(task 8): send with smtplib to SMTP_HOST:SMTP_PORT")


# The function declarations the model sees. One dict per tool, for example:
#   {"type": "function", "name": "<function name>",
#    "description": "<what it does and when to use it>",
#    "parameters": {"type": "object", "properties": {...}, "required": [...]}}
# The model chooses a tool from the description, so write it for the model.
# TODO(task 6): declare search_docs and calculate and put them in TOOLS.
# TODO(task 8): declare list_meetings and send_email; send_email's description says the user must confirm every email.
TOOLS: list[dict] = []

# The functions by name, so the agent can run the one the model asks for.
# TODO(task 6): map each declared name to its function, for example {"calculate": calculate, ...}.
FUNCTIONS: dict = {}
