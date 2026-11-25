# Versions

The tools, images and libraries the course uses, and the version of each.
Briefs never name versions: when a version matters, a task points here. The model names are in [`models.md`](models.md).
**Checked on 24 November 2026** against each project's release page or package registry (PyPI, npm, Docker Hub, GitHub releases).

How to read the tables:

- **Pinned** means: use exactly this version. The kit's own files use it, such as `mailpit/compose.yml` and `hello/ask.py`.
- **Course version** means: install this version. A newer patch release (the last number) is fine.
- **Tested** means: the version the course was checked with. Your project's `uv.lock` pins the exact version you get.

## On your laptop (Windows)

[`setup/windows.md`](setup/windows.md) installs these.

| Tool | Version | Kind | Notes |
|---|---|---|---|
| Windows | 11, version 23H2 or newer | minimum | Docker Desktop needs 23H2 (build 22631) or newer |
| Git for Windows (Git Bash) | 2.56.1 | course version | Any 2.45 or newer works |
| VS Code | the newest | — | It updates itself |
| uv | 0.13.9 | course version | 0.12 or newer. From uv 0.12, `uv init` makes a packaged `src/` project; for a flat project with `main.py`, use `uv init --no-package --python 3.12 NAME` |
| Python | 3.12.16 | course version | Any 3.12 release. Install it with `uv python install 3.12`; uv's Python is the only Python you need |
| Docker Desktop | 4.100.1 | course version | Released 23 November 2026, with the WSL 2 engine. Free under the Personal plan for individual learning |
| Docker Compose | v5 (comes with Docker Desktop) | tested | Use `docker compose` (with a space) |
| Ollama for Windows | 0.40.18 | course version | `embeddinggemma` needs 0.11.10 or newer |
| Node.js | 26.13.1 LTS ("Lithium") | course version | Only for the MCP Inspector (`npx`) and promptfoo. `winget install OpenJS.NodeJS.LTS` installs it. Version 24.22.1 or newer also works: the Inspector needs 22.23.4+, 24.22.1+ or 26.12.1+; promptfoo needs 22.22.0 or newer |

## Python libraries

Add them with `uv add`, for example `uv add "google-genai==3.6.1"` to pin one. Every one of them supports Python 3.12.

| Package | Tested | Notes |
|---|---|---|
| `google-genai` | 3.6.1 | The Gemini API library (`from google import genai`). Needs Python 3.11 or newer. Has both `client.interactions.create` and `client.models.generate_content` (see [`models.md`](models.md)) |
| `pydantic` | 2.14.4 | Models for structured output and request bodies |
| `chromadb` | 1.5.9 | The vector store for DocAnswer. `chromadb.PersistentClient(path="chroma")` keeps it in a folder; `chroma/` is in `.gitignore` |
| `fastapi` | 0.165.0 | Install as `fastapi[standard]` to get `uvicorn` and the `fastapi dev` command |
| `uvicorn` | 0.54.0 | Comes with `fastapi[standard]` |
| `httpx` | 0.28.1 | HTTP client; FastAPI's `TestClient` needs it |
| `pytest` | 9.2.0 | |
| `deepeval` | 4.3.5 | One of the two evaluation tools (P2). Needs Python 3.10 to 3.13 |
| `mcp` | 2.3.0 | The official MCP Python SDK. Install as `mcp[cli]` to get the `mcp` command. Version 2 renamed `FastMCP` to `MCPServer` (`from mcp.server import MCPServer`); older tutorials use the old name. See [`mcp/README.md`](mcp/README.md) |
| `ollama` | 0.6.3 | The Python library for a local Ollama |
| `python-dotenv` | 1.2.4 | Optional: reads `.env` into the environment. `uv run --env-file .env ...` does the same without a library |
| `numpy` | 2.5.5 | Optional: cosine similarity by hand in the embeddings lesson |

## npm packages (run with `npx`, nothing to install)

| Package | Tested | Notes |
|---|---|---|
| `promptfoo` | 0.126.0 | The other evaluation tool (P2): `npx promptfoo@0.126.0 eval`. Needs Node.js 22.22.0 or newer |
| `@modelcontextprotocol/inspector` | 2.16.0 | The MCP Inspector: `npx @modelcontextprotocol/inspector@2.16.0 uv run server.py` |

## Protocols and images

| Thing | Version | Kind | Notes |
|---|---|---|---|
| MCP specification | revision `2026-07-28` | course version | The current revision on modelcontextprotocol.io. The SDK above and the Inspector both speak it |
| Mailpit | `axllent/mailpit:v1.34.0` | pinned | In [`mailpit/compose.yml`](mailpit/compose.yml). Released 17 November 2026 |
| Python services in your own Dockerfiles | `python:3.12-slim` | course version | TaskPilot's Compose file (P3) and the capstone |
| uv inside your Dockerfiles | `ghcr.io/astral-sh/uv:0.13.9` | pinned | The **uv Docker tag**. In a Dockerfile: `COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /uvx /bin/` (uv's Docker guide). The tag `0.13` also exists and follows the newest 0.13 release |
| MCP Python SDK | `mcp` **2.3.0** (SDK version 2) | pinned | `uv add "mcp[cli]==2.3.0"`. Version 2: `from mcp.server import MCPServer`, client `from mcp import Client, StdioServerParameters`, tool schema in `input_schema`. Version 1 tutorials (`FastMCP`, `inputSchema`) do not match |

## Sources

- PyPI: `https://pypi.org/project/<name>/` for every Python package above.
- npm: https://www.npmjs.com/package/promptfoo and https://www.npmjs.com/package/@modelcontextprotocol/inspector
- uv: https://github.com/astral-sh/uv/releases · Git for Windows: https://github.com/git-for-windows/git/releases
- Docker Desktop: https://docs.docker.com/desktop/release-notes/ · Mailpit: https://hub.docker.com/r/axllent/mailpit/tags
- Ollama: https://github.com/ollama/ollama/releases · Node.js: https://nodejs.org/en/download
- MCP: https://modelcontextprotocol.io/specification/latest · Python: https://www.python.org/downloads/
