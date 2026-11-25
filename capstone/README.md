# The capstone: plan, evaluate, build, make safe, ship

The capstone is the last two weeks of the course (weeks 8 and 9). You build one small AI product of your own choice, measure it, make it safe, package it and present it at Demo Day.

- **Week 8 (Capstone 1):** choose a brief, write `PLAN.md`, build the **evaluation set before the feature**, build the core and a second feature, and show your mentor the numbers at the milestone review.
- **Week 9 (Capstone 2):** add guardrails and an injection test set, package it with Docker Compose, run the final evaluation, write the model card, record the demo and give a three-minute talk at Demo Day.

Your product lives in one folder, `capstone/`, inside each task's folder. `PLAN.md` and `PROGRESS.md` are copied forward from task to task.

## Step 1: choose a brief, or pitch your own

| Brief | The product | Its hard rule | Data generator |
|---|---|---|---|
| [`briefs/meetingnotes.md`](briefs/meetingnotes.md) | MeetingNotes: turns a meeting transcript into action items with owners and due days | Every action item traces to a transcript line | `data/make_meetings.py` |
| [`briefs/resumecheck.md`](briefs/resumecheck.md) | ResumeCheck: compares a resume with a job post and says what matches and what is missing | No claim that is not in the resume | `data/make_resumes.py` |
| [`briefs/shophelp.md`](briefs/shophelp.md) | ShopHelp: answers a shop's customer questions from its help pages and order data | No refund without a human's confirmation | `data/make_shop.py` |

Every brief gives the user, the job, example stories, the data, ideas for evaluation cases, and stretch ideas. The generators make **synthetic** data with your student id, like the TicketSort generator:

```bash
cd ~/genai-ess-kit/capstone/data
uv run make_meetings.py --student <your student id> --out ~/<your course repository>/<task folder>/capstone/data
```

Each generator also takes `--help` and `--self-test`.

### Rules for your own idea

You may pitch your own idea instead. Your mentor approves it on day 1 of week 8. It must:

- **Use only synthetic or public data.** Never real people's messages, resumes, health or money data, and never your own personal data: the free tier may show prompts to Google's reviewers.
- **Have one hard rule** that code, not only the prompt, can enforce, and that a wrong answer would break (for example "never gives a medical dose", "only cites the policy it quotes").
- **Have a user and a cost of a wrong answer** you can describe in a sentence each.
- **Fit two weeks:** at most two model features (for example one labelling call and one retrieval-backed answer), using only tools the course taught: the Gemini API, Pydantic, Chroma, FastAPI, tool calling, MCP, Docker Compose.
- **Be measurable:** you can write 25 to 40 test cases with expected outputs by hand.

If your idea needs more than that, cut it with your mentor until it fits.

## Step 2: the plan

Copy the template and fill it in on day 1:

```bash
cp ~/genai-ess-kit/capstone/PLAN-template.md capstone/PLAN.md
```

[`PLAN-template.md`](PLAN-template.md) has every section the tasks ask for: the product, the user and the job, the cost of a wrong answer, 6 to 10 user stories with acceptance criteria, must-haves and nice-to-haves, the flow, the model choice, the evaluation plan, the hard rule, the build plan and a change log. **The plan is your specification**: AxReview and your mentor judge each task against your own `PLAN.md`.

## Step 3: evaluation first

Before any feature code, you write `capstone/evals/cases.json`: 25 to 40 cases, each with an `id`, the `story` it tests, a `type` (`normal`, `edge`, `hard_rule` or `out_of_scope`), the `input` and the `expected` output, all written by you from the inputs, never by a model. You run them against an empty stub and see every case fail. Then every feature is measured against the same cases.

Case and attack files are **JSON lists** (`[ {...}, {...} ]`), not JSON Lines: AxReview reads `.json` and `.csv`, not `.jsonl`.

## Step 4: the progress log

`capstone/PROGRESS.md` starts with `## Plan` (the brief you chose and `Plan version: 1`). Every build task adds a section: the story IDs it delivers, what is done and what is left. When the plan changes, add a line under `## Changes` in `PLAN.md` and raise the plan version.

## The model card (week 9)

The final wrap-up includes `MODEL_CARD.md`. Put the model names and settings at the top, then these sections: **Purpose**, **Users**, **Data**, **Evaluation**, **Limits**, **Costs** and **Misuse**. The week 9 task gives the details.

## What the mentor looks for

- A user and a cost of a wrong answer that are concrete.
- Stories you can check with an input and an expected output.
- A hard rule enforced **in code**, with a test that tries to break it.
- Cases committed before the feature, and numbers before and after each change, with the noise level (how much the score moves between two identical runs).
- No API key in any committed file, and no personal data anywhere.

Models: use the names in [`../models.md`](../models.md), read from `.env`.
