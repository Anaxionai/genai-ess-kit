"""Answer a question from the top passages, with citations (tasks 10, 11 and 22).

Run it from inside docanswer/:
    uv run --env-file .env python answer.py "Can I fly business class?"

search and model are arguments of answer(), so a test can pass fakes and
make no API call.
"""

from search import top_passages

# TODO(task 10): write the grounding rule: answer only from the passages, cite an
# id in square brackets after each sentence, never cite an id that is not listed.
# TODO(task 11): add the refusal rule (reply with exactly REFUSAL).
# TODO(task 22): add the rule that text inside passage tags is data, never orders.
SYSTEM_RULE = "TODO(task 10): write the system rule."

# Given: the exact refusal sentence from task 11.
REFUSAL = "I don't know based on the handbook."

# TODO(task 11): add MAX_DISTANCE, a little above the largest top distance of
# your ten questions in task 9.

# TODO(task 22): start the list with the planted document's marker phrase.
BLOCKED_PHRASES: list[str] = []


def build_prompt(question: str, passages: list[dict]) -> str:
    """Build the prompt: every passage labelled with its id, the question last.

    Input: the question and the passages from top_passages().
    Output: one string. Each passage starts on its own line with its id in
    square brackets, such as [travel-booking#2].

    Task 22 changes it: wrap each passage in <passage id="..."> and
    </passage>, after removing any "<passage" or "</passage" text inside the
    passage, so a passage cannot close its own tag.
    """
    raise NotImplementedError("TODO(task 10): label each passage with its id; TODO(task 22): wrap it in tags")


def ask_model(system: str, prompt: str) -> str:
    """Send one call to CHAT_MODEL and return the model's text.

    Use client.interactions.create(...) with system_instruction and
    store=False, as in P1. Read the model name from os.environ["CHAT_MODEL"].
    Set no temperature.
    """
    raise NotImplementedError("TODO(task 10): one Interactions API call")


def parse_citations(text: str) -> list[str]:
    """Return every cited id in order, such as ["travel-booking#2"].

    Use re.findall(r"\\[([^\\[\\]]+#\\d+)\\]", text).
    Edge cases: no citation gives []; an id cited twice appears twice.
    """
    raise NotImplementedError("TODO(task 10): find the cited ids")


def check_output(answer: str, passages: list[dict]) -> str | None:
    """Check a model answer before it reaches the user.

    Output: None when the answer may be shown, otherwise the reason it is
    blocked (for example the blocked phrase, or the bad citation).
    Rejects an answer that holds a phrase from BLOCKED_PHRASES, or that cites
    an id not among the passages sent.
    """
    raise NotImplementedError("TODO(task 22): block the marker and bad citations")


def answer(question: str, k: int = 3, search=top_passages, model=ask_model) -> dict:
    """Answer the question from the top k passages.

    Output (task 10): a dict with
        question, answer, citations, sources (the passages sent) and
        bad_citations (cited ids that were never sent).

    Task 11 adds the refusals. Return REFUSAL, with refused: True, when:
        - the best distance is above MAX_DISTANCE (then make no model call);
        - the answer has bad citations or no citation at all (keep the model's
          text in a field rejected).
    Task 22 adds check_output(): a blocked answer becomes REFUSAL with blocked_by.
    """
    raise NotImplementedError("TODO(task 10): answer with citations; TODO(task 11): refuse; TODO(task 22): check the output")


def main() -> None:
    """Answer the question given on the command line and print the result."""
    raise NotImplementedError("TODO(task 10): answer the question on the command line")


if __name__ == "__main__":
    main()
