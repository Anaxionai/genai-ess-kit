# TicketSort Guided starter (P1)

This folder is the start of your `ticketsort/` project for P1 (module m02). It gives you the
set-up: the uv project, the file layout, the settings file, the function names and the
test set-up. It holds **no answers**. Every function a task asks you to write stops with
`NotImplementedError("TODO(task NN): ...")`, and its docstring says what it must do.
The tasks, the checks and the 90% bar are the same as for everyone.

## What is included

| File | What it is |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | A uv project for Python 3.12 with `google-genai`, `pydantic`, `python-dotenv`, and `pytest` for tests |
| `.env.example` | `GEMINI_API_KEY=` and `CHAT_MODEL=`, with nothing after `=` |
| `.gitignore` | Keeps `.env`, `.venv/` and caches out of git. `results/` **is** committed: it is your evidence |
| `config.py` | Settings in one place: folders, `MODEL` from `.env`, `RPM`, `PROMPT_VERSION` |
| `load.py` | `load_tickets(path)`, `summary(tickets)` |
| `labels.py` | `CATEGORIES`, `URGENCIES` and an empty `TicketLabel` |
| `label.py` | `label_ticket`, `label_all`, `is_retryable`, `call_with_backoff`, `cost_rupees`, `label_ticket_local`; the CSV column names |
| `prompts/v1.txt` | A placeholder: you replace it with your own system instruction |
| `check_validation.py`, `cost_report.py`, `evaluate.py`, `judge.py` | The scripts tasks 11, 13, 20 and 22 ask for, as stubs |
| `tests/` | `conftest.py` (the fake client, as stubs) and tests. Tests for code you have not written yet are skipped |

No data is included. You make your own 200 tickets in task 9.

## Copy it in (task 9, instead of step 1)

In Git Bash, in task 9's folder:

```bash
cp -r ~/genai-ess-kit/starters/p01-ticketsort/. ticketsort/
cd ticketsort
uv sync
uv run pytest -q
```

`uv sync` installs what step 1's `uv add` would. The tests end with something like
`11 passed, 17 skipped`. Then carry on with task 9 from step 2: make `data/tickets.csv` with
the command in the kit's `data/tickets/README.md`, and copy your `.env` into `ticketsort/`.
`git status` must not list `.env`.

## How to run it

| Command | What it does | Works after |
|---|---|---|
| `uv run load.py` | Prints the summary of your tickets | Task 9 |
| `uv run label.py` | Labels the tickets into `results/labels_<version>.csv` | Task 10 |
| `uv run check_validation.py` | Shows bad answers rejected | Task 11 |
| `uv run cost_report.py` | Prints the cost report from `results/cost_log.csv` | Task 13 |
| `uv run evaluate.py results/labels_v1.csv` | Writes `results/eval_v1.md` | Task 20 |
| `uv run judge.py` | Scores 30 summaries with the judge model | Task 22 |
| `uv run pytest -q` | Runs the tests, never the real model | Always |

Before a TODO is done, its command stops with `NotImplementedError` and the task number.

## Every TODO

Search them with `grep -rn "TODO(task" .`

| Task | File | What you write |
|---|---|---|
| 9 | `load.py` | `load_tickets`, `summary`, `main` (print the summary, shortest and longest tickets) |
| 9 | `tests/test_load.py` | Remove the skips when your code is written |
| 10 | `labels.py` | The three fields of `TicketLabel`, with `Literal` choices and descriptions |
| 10 | `config.py` | `RPM`: your own limit |
| 10 | `prompts/v1.txt` | Your system instruction |
| 10 | `label.py` | `label_ticket` (the call with the schema), `label_all` (CSV and pause), `main` |
| 10, 11 | `tests/test_labels.py` | Remove the skips when your code is written |
| 11 | `labels.py` | `max_length` on `summary` |
| 11 | `label.py` | Retries after a `ValidationError`, `failed.csv`, the three counts |
| 11 | `check_validation.py` | Three bad answers and their errors |
| 12 | `label.py` | `is_retryable`, `call_with_backoff`, the resume file in `label_all` |
| 13 | `config.py` | `PRICE_IN`, `PRICE_OUT`, `USD_TO_INR`, with the date |
| 13 | `label.py` | `cost_rupees` and a cost log row after every call |
| 13 | `cost_report.py` | `main`: the report |
| 20 | `evaluate.py` | The score's definition, `load_predictions`, `score`, `confusion`, `to_markdown`, `main` |
| 20 | `tests/test_evaluate.py` | Remove the skips when your code is written |
| 21 | `config.py` | `PROMPT_VERSION`: your best version |
| 22 | `config.py` | `JUDGE_MODEL` |
| 22 | `judge.py` | `JudgeScores`, `pick_sample`, `judge_summary`, `agreement`, `main` |
| 23 | `tests/conftest.py` | `fake_answer`, `FakeClient`, `FakeRateLimit` and a 400 error, the `fake_client` fixture |
| 23 | `tests/test_label.py` | The six tests (their names and docstrings are there) |
| 24 | `config.py` | `LOCAL_MODEL` |
| 24 | `label.py` | `label_ticket_local` (run `uv add ollama` first) |

Task 21 and task 25 write no new functions, so they have no other TODO: task 21 is new prompt
files and `PROMPTS.md`; task 25 is `README.md` and `EXPLAIN.md`.

## What you still write yourself

- All the logic above, and every prompt in `prompts/`.
- `data/tickets.csv` (made by the kit's generator, never edited by hand) and `.env`.
- Everything in `results/`: labels, `failed.csv`, `cost_log.csv`, evaluations, scores.
- `AI_LOG.md`, `PROMPTS.md`, `RUBRIC.md`, `COMPARE.md`, `README.md`, `EXPLAIN.md` and
  each task's `evidence.md`.
- `JUDGE_MODEL=` (task 22) and `LOCAL_MODEL=` (task 24) in `.env.example`.

## Notes

- `config.py` reads `CHAT_MODEL` with `os.environ.get(...)`, so the tests run without a
  `.env`. The brief's `os.environ["CHAT_MODEL"]` is fine too once your `.env` is in place.
- `pyproject.toml` sets `pythonpath = ["."]` for pytest, so the tests can import `label.py`
  and the rest from this folder.
- You may change any name or signature if your code still does what the task asks. Keep the
  client as an argument of `label_ticket` and `label_all`: the tests in task 23 need that.
