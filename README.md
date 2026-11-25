# GENAI-ESS course kit

This is the course kit for **GENAI-ESS, Gen AI Essentials: LLM apps in Python** (9 weeks).
It holds what your tasks need beyond your own code: the laptop and API-key guides, the model list, a ready-made first script, synthetic practice data, Mailpit, the MCP guide, the Guided starters and the capstone briefs.
Your task briefs link to files in this kit.

## Get the kit

Run this once, in Git Bash, in the Launchpad (week 1):

```bash
cd ~ && git clone https://github.com/Anaxionai/genai-ess-kit.git
```

This makes the folder `~/genai-ess-kit`, which is `C:\Users\<your name>\genai-ess-kit` on Windows.
Keep it next to your course repository, never inside it.

Check it: `ls ~/genai-ess-kit` lists `README.md`, `VERSIONS.md`, `models.md`, `setup` and the other folders below.

On day 1, before you have Git, you only need [`hello/`](hello/README.md): its README shows how to download the one script you run.

## Update the kit

When a task says "Run `git pull` in your copy of the course kit", run:

```bash
cd ~/genai-ess-kit
git pull
```

Do not change the kit's files. Copy a file into your own repository first, then change your copy.
If `git pull` says your local changes would be overwritten, run `git restore .` in the kit folder. It undoes your changes to the kit's files. Then run `git pull` again.

Every command in the kit's READMEs is written for **Git Bash**, unless it says PowerShell. [`setup/windows.md`](setup/windows.md) sets it up.

## What is in the kit

| Path | What it is | Used in |
|---|---|---|
| `README.md` | This file | the whole course |
| `VERSIONS.md` | The version of every tool, library and image the course uses | the whole course |
| `models.md` | The model names for chat, small chat and embeddings, with prices, and the Ollama models that fit 8 GB and 16 GB. **Briefs never name a model: they link here** | the whole course |
| `LICENSE` | The MIT licence for the kit's code | — |
| `setup/windows.md` | Windows laptop setup: Git Bash in VS Code, uv and Python 3.12, Docker Desktop, Ollama, Node.js | Launchpad, P1 |
| `setup/api-key.md` | Your free Gemini API key: getting it, keeping it in `.env`, what the free tier does with your prompts, rate limits and `429` | Launchpad |
| `try-it.md` | Free sites where you practise each new idea in the browser | learn cards |
| `hello/` | `ask.py`: the day 1 script that sends one prompt and prints the answer and the token counts | Launchpad, day 1 |
| `data/tickets/` | `make_tickets.py`: 200 synthetic support tickets for an online shop, with true labels; a sample | P1 TicketSort |
| `data/handbook/` | A synthetic company staff handbook: about 40 short policy documents and example questions | P2 DocAnswer, P3 TaskPilot |
| `data/calendar/` | A week of meetings for TaskPilot's calendar tool | P3 TaskPilot |
| `mailpit/` | Mailpit in Docker Compose: a pretend mail server, so emails never leave your laptop | P3 TaskPilot |
| `mcp/` | Running an MCP server in Python, and connecting the MCP Inspector and a client to it | P3 TaskPilot |
| `starters/` | The Guided starters: a starting point for each project, for students on the Guided level | P1 to P3 |
| `capstone/` | How the capstone works, the plan template, three briefs and their data generators | Capstone |

## Running the kit's Python scripts

Every script in the kit starts with a `# /// script` block that lists the Python version and libraries it needs, so `uv run` sets everything up by itself. For example:

```bash
cd ~/genai-ess-kit/data/tickets
uv run make_tickets.py --student <your student id> --out <path to your project>/data/tickets.csv
```

The data generators use only Python's standard library, and the same `--student` id always gives the same data.

## Your API key and your data

- Your Gemini API key lives in a `.env` file and **never** in Git. The kit's `.gitignore` already ignores `.env`; your own repository's `.gitignore` must too. See [`setup/api-key.md`](setup/api-key.md).
- On the free tier, Google may read and use what you send. Every dataset in this kit is made up for that reason. **Never send personal data** to a model in this course: not your own resume, not anyone's real messages.

## Line endings

The kit's `.gitattributes` file makes Git check out every text file with LF line endings, on Windows too.
Data files and Compose files then work the same in Git Bash and inside Linux containers. Do not convert them to CRLF.

## Licence and attribution

- **The kit's code** is under the MIT licence: see [`LICENSE`](LICENSE). That covers the scripts, data generators and configuration files written for the kit.
- **Made-up data.** The tickets, the online shop, the company "Fernhill Software" and its handbook, the calendar, the meeting transcripts, the resumes, the job posts and the shop help data are invented by the kit. Any likeness to a real company or person is chance. You may use the data freely.
- **Tools and images.** The tools, libraries and Docker images the course uses keep their own licences. Docker Desktop is free under the Personal plan for individual learning, and for small businesses with fewer than 250 employees and less than $10 million in yearly revenue. Gemini and Google AI Studio are Google products, used under Google's terms. Ollama models each have their own licence, shown on their ollama.com page.
- Company and product names belong to their owners.
