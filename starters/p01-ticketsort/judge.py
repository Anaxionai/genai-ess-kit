"""Check the one-line summaries with your rubric (RUBRIC.md) and a model judge.

Run: uv run judge.py
"""

import csv  # noqa: F401
import random  # noqa: F401
from pathlib import Path

from google import genai  # noqa: F401
from pydantic import BaseModel

import config
from load import Ticket

HAND_SCORES_PATH = config.RESULTS_DIR / "summary_scores.csv"  # your hand scores, one column per criterion
JUDGE_SCORES_PATH = config.RESULTS_DIR / "judge_scores.csv"  # the judge's scores, the same columns


class JudgeScores(BaseModel):
    """The judge's answer: one bool per criterion in your RUBRIC.md.

    TODO(task 22): add four bool fields, named after your own four criteria.
    """


def pick_sample(tickets: list[Ticket], n: int = 30, seed: int = 7) -> list[Ticket]:
    """Return the same n tickets every time: random.seed(seed), then random.sample(tickets, n)."""
    raise NotImplementedError("TODO(task 22): choose the 30 tickets with a fixed seed")


def judge_summary(client, rubric: str, ticket_text: str, summary: str) -> JudgeScores:
    """Send the rubric, the ticket and its summary to config.JUDGE_MODEL with store=False and
    JudgeScores.model_json_schema() as the response schema; return the validated scores."""
    raise NotImplementedError("TODO(task 22): ask the judge model and validate its answer")


def agreement(hand_path: str | Path, judge_path: str | Path) -> dict[str, float]:
    """Return the share of scores where you and the judge agree, per criterion and overall
    (30 tickets x 4 criteria = 120 scores), joining the two files by ticket id."""
    raise NotImplementedError("TODO(task 22): compare the two score files")


def main() -> None:
    """Score the 30 sampled summaries with the judge into JUDGE_SCORES_PATH, then print the
    agreement per criterion and the criterion with the lowest agreement."""
    raise NotImplementedError("TODO(task 22): run the judge and print the agreement")


if __name__ == "__main__":
    main()
