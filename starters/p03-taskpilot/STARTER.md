# TaskPilot: the Guided starter (P3)

This folder is the contents of your `taskpilot/` folder for P3. It gives you the set-up: the uv project, the file names the briefs use, the function signatures, the settings names and the test set-up. **It holds no solution.** Every function a task asks for raises `NotImplementedError("TODO(task NN): ...")`, and its docstring says what it must do. Tests for code you have not written yet are skipped with `@pytest.mark.skip(reason="TODO(task NN)")`.

## What is included

| File | What it is |
|---|---|
| `pyproject.toml`, `uv.lock`, `.python-version` | A flat uv project (Python 3.12) with `google-genai`, `chromadb` and `mcp[cli]`, and `pytest` for development. Versions as in the kit's `VERSIONS.md` |
| `.env.example`, `.gitignore` | The setting names (no values) and what Git ignores. `.env` is ignored |
| `tools.py` | The four tools (`search_docs`, `calculate`, `list_meetings`, `send_email`), the `TOOLS` declarations list and the DocAnswer import path |
| `agent.py` | `run_agent`, the system instruction and `PRICES` |
| `guards.py` | `ALLOWED_DOMAINS`, `check_email`, `confirm_email`, and two task 16 fixes |
| `mcp_server.py`, `mcp_tools.py` | The MCP server file and the MCP-to-Gemini conversions (`declarations`) |
| `main.py` | The command-line entry point and `SERVER_ENV` |
| `run_jobs.py`, `run_attacks.py`, `cache.py` | The job runner, the attack runner and the model-call cache |
| `tests/` | `test_starter.py` passes now; the others are skipped until their task |
| `docanswer/` | Empty, for **your own** DocAnswer copy (see the note inside) |

## Copy it in (task 6)

Do this **instead of step 1** of task 6 (`uv init` and `uv add`). In Git Bash, in task 6's folder:

```bash
mkdir -p taskpilot
cp -r ~/genai-ess-kit/starters/p03-taskpilot/. taskpilot/
cd taskpilot
cp <path to your 3.23 folder>/docanswer/.env .env
uv sync
uv run pytest -q
```

The `/.` copies the hidden files (`.gitignore`, `.env.example`, `.python-version`) too. Keep the starter's `.env.example`: it already lists the names TaskPilot uses. Every test passes or is skipped.

Then carry on with task 6 from step 2: copy your DocAnswer into `docanswer/` (the note there has the exact command) and make the `index.py` edit. Step 4's `sys.path` line is already in `tools.py`; you add the `from search import top_passages` line. The project already has `pytest` (task 6, step 11) and `mcp[cli]` (task 9, step 1), so those `uv add` commands change nothing.

Copy the starter **once**. In every later task, copy your own `taskpilot/` folder forward as the brief says. Never copy the starter on top of your work.

## How to run

```bash
uv run --env-file .env python main.py "What is 18% of 42,500?"   # from task 6
uv run --env-file .env mcp dev mcp_server.py                      # task 9, needs Node.js
uv run --env-file .env python run_jobs.py                         # task 15, Mailpit running
uv run --env-file .env python run_attacks.py                      # task 16
uv run python -m pytest -q                                         # any time
```

Before you start a stub, delete its skip in `tests/` when there is one, watch the test fail, then make it pass.

The tests never call a model, Mailpit or the network. If importing your DocAnswer needs a setting (for example it makes a client when it loads), run them as `uv run --env-file .env python -m pytest -q`.

## Every TODO

| Task | File | What you write |
|---|---|---|
| 6 | `tools.py` | The `top_passages` import, `search_docs`, `calculate` (with `ast`, never `eval`), the `TOOLS` declarations and `FUNCTIONS` |
| 6 | `main.py` | `main()`: one tool round trip with a `function_result` |
| 6 | `tests/test_calculate.py` | The two test bodies |
| 7 | `agent.py` | `SYSTEM_INSTRUCTION` and `run_agent`: the loop, the step limit, the JSONL trace |
| 7 | `main.py`, `.gitignore` | `main()` calls `run_agent`; add `traces/` |
| 8 | `tools.py` | `list_meetings`, `send_email`, and their two declarations |
| 8 | `guards.py` | `ALLOWED_DOMAINS`, `check_email`, `confirm_email` |
| 8 | `agent.py` | The `ask` parameter, the guards before `send_email`, the `guard` trace field, the calendar week in the instruction |
| 8 | `tests/test_guards.py` | The three task 8 test bodies |
| 9 | `mcp_server.py` | `MCPServer("taskpilot")`, four `@mcp.tool()` functions, `mcp.run()` |
| 9 | `mcp_tools.py` | `declarations` and `result_text` |
| 9 | `agent.py`, `main.py` | `run_agent` becomes async with `call_tool`; `main()` opens the MCP `Client`; `SERVER_ENV` |
| 15 | `agent.py` | `PRICES`, with the date you read them |
| 15 | `run_jobs.py` | `clear_mailpit`, `mailpit_recipients`, `cost_usd`, `judge`, `main` |
| 16 | `run_attacks.py` | `judge_attack`, `main` |
| 16 | `guards.py`, `agent.py`, `tools.py`, `main.py` | `as_data`, `tools_for_job`, using them in `run_agent`, `DOCS_COLLECTION` in `search_docs` and `SERVER_ENV` |
| 17 | `cache.py` | `cache_key`, `cached_create` |
| 17 | `agent.py`, `.gitignore` | `cached_create` in the loop, `cached` in the trace, `max_output_tokens`, `TASKPILOT_MODEL`; add `cache/` |

Find them all with `grep -rn "TODO(task" --include="*.py" --include=".gitignore" .`

Names the briefs do not give (`FUNCTIONS`, `result_text`, `as_data`, `tools_for_job`, `judge`, `judge_attack`, `cache_key`) are suggestions. Keep them so the tests fit, or rename them and change the tests.

## What you still write yourself

- All the logic above, and every file the briefs ask you to create: `calendar.json` (copied from the kit in task 8), `jobs.json` (task 15), `attacks/` (task 16), `evidence.md`, `AI_LOG.md`.
- **Task 18 has no TODO here**: you write `Dockerfile`, `.dockerignore` and `compose.yml` whole, from the brief. Check `.env.example` then still lists every setting you use.
- **Task 19 has no TODO here**: it is writing, not code (`README.md` and `EXPLAIN.md`). This file is `STARTER.md` so that the README stays yours.
- Your DocAnswer is your own code from P2. If its `search.py` needs a package this project lacks, `uv add` it here.
