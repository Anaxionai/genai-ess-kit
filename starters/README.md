# Guided starters

Each project has three levels. Your mentor tells you yours.

- **Core**: you start from an empty folder.
- **Guided**: you start from a starter in this folder.
- **Stretch**: you do Core plus the project's Stretch goals.

A starter removes the set-up work that is not the point of the project: the uv project files, the folder layout, the settings, the test set-up, and the names and signatures of the functions the briefs ask for. Your time then goes on the ideas the tasks teach.

**A starter never contains a solution.** Every piece of logic a task asks you to write is left as a stub that raises `NotImplementedError("TODO(task NN): ...")`, where NN is the task's number in the project. Its docstring says what the function must do. Tests for code you have not written yet are marked `@pytest.mark.skip(reason="TODO(task NN)")`: remove the skip when you write that code.

| Starter | Project | Copy it in the task that says so |
|---|---|---|
| [`p01-ticketsort/`](p01-ticketsort/) | P1 TicketSort (weeks 2 and 3) | the first TicketSort build task |
| [`p02-docanswer/`](p02-docanswer/) | P2 DocAnswer (weeks 4 and 5) | the first DocAnswer build task |
| [`p03-taskpilot/`](p03-taskpilot/) | P3 TaskPilot (weeks 6 and 7) | the first TaskPilot build task |

## How to use a starter

1. Run `git pull` in `~/genai-ess-kit` to get the latest kit.
2. Copy the starter's **contents** into your project folder with the exact command in its `STARTER.md`, for example:

   ```bash
   mkdir -p ticketsort
   cp -r ~/genai-ess-kit/starters/p01-ticketsort/. ticketsort/
   ```

3. In the project folder, make your `.env` from `.env.example` and fill in your key and the model names from [`../models.md`](../models.md). Check `git check-ignore -v .env`.
4. Run `uv sync`, then `uv run pytest -q`. Everything passes or is skipped.
5. Work through the tasks in order. `STARTER.md` has a table of every TODO, its task number and its file.

Each starter's `STARTER.md` (not `README.md`: you write the project's README yourself in the wrap-up) says what is included and what you still write.

## Rules

- Never copy the starter on top of work you have already done: it would overwrite your files.
- The starter's names (files, functions, settings) match the briefs. Keep them, so that the briefs, the tests and AxReview all agree.
- You still write and own the code: the AI rules of the course apply as usual, and your `AI_LOG.md` covers starter projects too.
