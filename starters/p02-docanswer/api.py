"""Serve DocAnswer as a web API (task 20) and its question page (task 21).

Run it from inside docanswer/:
    uv run --env-file .env fastapi dev api.py

Tests import this module and replace answer with a fake:
    monkeypatch.setattr(api, "answer", fake_answer)
so keep the import below as it is.
"""

from fastapi import FastAPI, HTTPException  # noqa: F401
from pydantic import BaseModel, Field  # noqa: F401

from answer import answer  # noqa: F401

# TODO(task 20): create the app: app = FastAPI(title="DocAnswer"), and put
# @app.get("/health") on health() and @app.post("/ask") on ask().


class AskRequest(BaseModel):
    """The body of POST /ask.

    TODO(task 20): question (3 to 500 characters) and k (default 3, from 1 to 8),
    both with Field(...).
    """


class Source(BaseModel):
    """One cited passage. TODO(task 20): chunk_id, doc_id, title, section."""


class AskResponse(BaseModel):
    """The reply of POST /ask. TODO(task 20): answer, refused: bool, sources: list[Source]."""


def health() -> dict:
    """GET /health returns {"status": "ok"}."""
    raise NotImplementedError("TODO(task 20): the health route")


def ask(body: AskRequest) -> AskResponse:
    """POST /ask: call answer(body.question, body.k) and return an AskResponse.

    - sources holds only the cited passages;
    - the model's rate-limit error (as in P1) becomes
      HTTPException(503, "The model is busy. Try again in a minute.");
    - write it with def, not async def: the model call blocks.
    """
    raise NotImplementedError("TODO(task 20): the /ask route")


# TODO(task 21): after every route, serve the page:
# app.mount("/", StaticFiles(directory="static", html=True), name="static")
