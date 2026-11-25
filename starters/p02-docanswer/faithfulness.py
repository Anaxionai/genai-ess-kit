"""Score the faithfulness of DocAnswer's answers with DeepEval (task 19).

Run `uv add deepeval` first (task 19, step 1). Then, from inside docanswer/:
    uv run --env-file .env python faithfulness.py

The judge is DeepEval's GeminiModel with the model name from JUDGE_MODEL. Then set
judge._temperature_configured = False: DeepEval 4.3.5 sends temperature=0 for a model
it does not know, and a Gemini call must not set it (the kit's models.md). Import deepeval inside the functions that use it, or at the
top once you have added it.
"""

from pathlib import Path

RESULTS_DIR = Path("results")


def answer_all(questions: list[dict], path: Path) -> list[dict]:
    """Answer every question with answer(question, k=3) and save to path.

    path is results/answers-<collection>.json. Reuse the answers saved there,
    so a judge rerun never asks the chat model again. Pause between calls as
    models.md says.
    """
    raise NotImplementedError("TODO(task 19): answer the questions once and save them")


def score_all(answers: list[dict], path: Path) -> list[dict]:
    """Score each saved answer with FaithfulnessMetric and save to path.

    path is results/faithfulness-<collection>.csv with id, score, refused.
    - Use FaithfulnessMetric(model=judge, async_mode=False, include_reason=False)
      with the sent passages as retrieval_context.
    - Skip ids scored already; pause between calls.
    - A refusal has no claims: mark it refused, never score it 1 or 0.
    - When the judge fails (for example invalid JSON), leave the score empty.
    """
    raise NotImplementedError("TODO(task 19): score each answer, skipping finished ids")


def summarise(scores: list[dict]) -> dict:
    """Return the mean score and the 3 lowest ids, leaving out refusals and empty scores."""
    raise NotImplementedError("TODO(task 19): the mean and the 3 lowest ids")


def main() -> None:
    """Answer, score and print the mean and the 3 lowest ids for the current collection."""
    raise NotImplementedError("TODO(task 19): run answer_all, score_all and summarise")


if __name__ == "__main__":
    main()
