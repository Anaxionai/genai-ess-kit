# DocAnswer: the Guided starter

This folder is the start of your `docanswer/` project for P2. It gives you the
set-up: the uv project, the file layout, the function names and signatures, and
empty tests. **It holds no solutions.** Every function a task asks you to write
stops with `raise NotImplementedError("TODO(task NN): ...")`, and its docstring
says what it takes, what it returns and which edge cases the task checks.

## What is included

| File | What it is |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | A uv project for Python 3.12 with `google-genai`, `chromadb`, `fastapi[standard]`, `pydantic` and, for development, `pytest`, at the versions in the kit's `VERSIONS.md` |
| `.env.example` | The setting names, with no values and no key |
| `.gitignore` | Ignores `.env`, `.venv/`, `__pycache__/`, `.pytest_cache/`, `chroma/` and `data/` |
| `load.py`, `chunk.py`, `index.py`, `search.py`, `answer.py` | The pipeline: load, chunk, embed, search, answer |
| `evaluate.py`, `faithfulness.py` | Measuring search and answers |
| `api.py`, `static/index.html` | The web API and the question page |
| `tests/` | One test file per module, every test skipped until you write it, plus `test_starter.py` |

Given, so you do not write them: `get_collection()` and `collection_name()` in
`index.py`, the Chroma plumbing of `GeminiEmbedding` (`__init__`, `name`,
`get_config`, `build_from_config`, `default_space`), `index.py`'s `main()` with
`--limit`, `read_questions()` in `evaluate.py`, the exact `REFUSAL` sentence in
`answer.py`, and `tests/test_starter.py`, which checks the set-up and makes no
API call.

## Copy it in (task 7, step 1)

In Git Bash, in task 7's folder, before a `docanswer/` folder exists:

```bash
cp -r ~/genai-ess-kit/starters/p02-docanswer docanswer
```

Then go on with task 7's step 2 (copy the handbook into `docanswer/data/handbook`).
`git check-ignore -v docanswer/data` prints a line, because the starter's
`.gitignore` already ignores `data/` and `chroma/`.

## Run it

```bash
cd docanswer
uv sync
uv run python -m pytest -q
```

You should see `11 passed, 18 skipped`. The skipped tests are yours to write.

For the steps that call Gemini, copy `.env.example` to `.env` and fill in your
key and the model names from the kit's `models.md`. Run those steps with
`uv run --env-file .env python <file>.py`, as the briefs say. Never commit `.env`.

Some brief steps are already done here, and running them again is harmless:
`uv add --dev pytest` (task 7), `uv add google-genai chromadb` (task 9) and
`uv add "fastapi[standard]"` (task 20). `deepeval` is **not** included: add it
yourself in task 19, step 1.

## Your TODOs

`grep -rn "TODO(task" .` lists them all.

| Task | File | What you write |
|---|---|---|
| 7 | `load.py` | `read_document()`, `load_documents()`, `main()` |
| 7 | `tests/test_load.py` | the field test and the no-title test |
| 8 | `chunk.py` | `split_text()`, `split_sections()`, `chunk_documents()`, `main()` |
| 8 | `tests/test_chunk.py` | the five chunking tests |
| 8 | `.env.example` | `CHUNK_MAX_WORDS` and `CHUNK_OVERLAP` |
| 9 | `index.py` | `embed_texts()`, `GeminiEmbedding.__call__()`, `GeminiEmbedding.embed_query()`, `build_index()` |
| 9 | `search.py` | `top_passages()`, `main()` with your ten questions |
| 10 | `answer.py` | `SYSTEM_RULE`, `build_prompt()`, `ask_model()`, `parse_citations()`, `answer()`, `main()` |
| 10 | `tests/test_answer.py` | `parse_citations()` and a bad citation, with fakes |
| 11 | `answer.py` | `MAX_DISTANCE`, the refusal rule and the refusals in `answer()` |
| 11 | `tests/test_answer.py` | the two refusal tests |
| 18 | `evaluate.py` | `hit_rate()`, `main()` |
| 18 | `tests/test_evaluate.py` | the `hit_rate()` test |
| 19 | `faithfulness.py` | `answer_all()`, `score_all()`, `summarise()`, `main()` |
| 20 | `api.py` | the `app`, `AskRequest`, `Source`, `AskResponse`, `health()`, `ask()` |
| 20 | `tests/test_app.py` | the four route tests |
| 21 | `static/index.html` | the whole page: form, `fetch`, states, `textContent` |
| 21 | `api.py` | the `app.mount(...)` line after the routes |
| 22 | `answer.py` | `BLOCKED_PHRASES`, `check_output()`, the passage tags in `build_prompt()`, the data rule in `SYSTEM_RULE`, `blocked_by` in `answer()` |
| 22 | `tests/test_answer.py` | the marker test and the tag-escape test |

## What you still write yourself

- Every body and test above. Remove a test's `@pytest.mark.skip` line when you
  write it.
- Files the starter leaves out on purpose, because the task is to write them:
  `check_refusals.py` and `evalset/refusals.csv` (task 11),
  `evalset/questions.csv` (task 18), `check_injection.py` (task 22).
- Files your runs make: `sources.csv`, `data/chunks.json`, `chroma/` and
  `results/`.
- `README.md`, `evidence.md`, `AI_LOG.md` and `EXPLAIN.md`. Task 23 writes no
  code, so it has no TODO: the starter has no `README.md` because you write it
  in task 23.

## Two things to keep

- `get_collection()` uses `PersistentClient(path="chroma")`, so run every
  command from inside `docanswer/`. TaskPilot (P3) changes this line to a path
  built from `__file__`; leave it as it is until then.
- TaskPilot imports `top_passages` from `search.py`. Keep its name and
  signature, `top_passages(question, k=3)`.
