"""TicketSort's settings, kept in one place.

Every other file imports this one. Model names come from .env, never from code
(see the kit's models.md).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # reads .env from this folder into the environment

# Folders and files. Paths are relative to this file, so the scripts work from any folder.
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "tickets.csv"  # made by the kit's make_tickets.py in task 9
PROMPTS_DIR = BASE_DIR / "prompts"  # prompts/v1.txt, v2.txt, ...
RESULTS_DIR = BASE_DIR / "results"  # labels, failures, cost log, evaluations (all committed)

# The chat model's name, from .env. It is empty until you copy your .env into this folder.
# .get() lets the tests import config.py without a .env. The brief's os.environ["CHAT_MODEL"]
# is fine too once your .env is in place.
MODEL = os.environ.get("CHAT_MODEL", "")

# TODO(task 10): set RPM to the requests-per-minute limit of your CHAT_MODEL, read in AI Studio.
# 0 is a placeholder: label_all's pause of 60 / RPM fails until you set it.
RPM = 0

# The prompt file in prompts/ that label.py sends as the system instruction.
# TODO(task 21): set this to your best version when you finish the prompt log.
PROMPT_VERSION = "v1"

# TODO(task 13): add PRICE_IN and PRICE_OUT (US dollars per million tokens, paid tier, from the
# pricing page) and USD_TO_INR, with a comment giving the date you read them.

# TODO(task 22): add JUDGE_MODEL, read from .env with os.environ["JUDGE_MODEL"].

# TODO(task 24): add LOCAL_MODEL, read from .env with os.environ["LOCAL_MODEL"].
