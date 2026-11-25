"""Embed the chunks into a Chroma collection (task 9).

Run it from inside docanswer/:
    uv run --env-file .env python index.py --limit 20
    uv run --env-file .env python index.py

Given: collection_name(), get_collection(), main() and the Chroma plumbing of
GeminiEmbedding (__init__, name, get_config, build_from_config, default_space).
You write: embed_texts(), GeminiEmbedding.__call__(), GeminiEmbedding.embed_query()
and build_index().
"""

import argparse
import json
import os
from pathlib import Path
from typing import Any

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings

CHUNKS_FILE = Path("data/chunks.json")
BATCH_SIZE = 20  # texts per embedding call; the brief allows up to 20
VECTOR_SIZE = 768  # from the kit's models.md: pass output_dimensionality=768


def embed_texts(texts: list[str], kind: str) -> list[list[float]]:
    """Embed up to BATCH_SIZE texts with one call to EMBED_MODEL.

    Inputs:
        texts: 1 to 20 strings.
        kind: "document" for chunks, "question" for questions.
    Output:
        One vector of VECTOR_SIZE floats per text, in the same order.

    Must:
        - send each text as its own types.Content (the plain-list trap in models.md);
        - put each text in the document or the question format from models.md
          (no task_type);
        - read the model name from os.environ["EMBED_MODEL"], never type it;
        - raise an error unless the number of vectors equals the number of texts
          and every vector has VECTOR_SIZE numbers;
        - pause after the call as models.md says.
    Edge cases: more than 20 texts or an unknown kind is an error.
    """
    raise NotImplementedError("TODO(task 9): embed the texts, one Content per text")


class GeminiEmbedding(EmbeddingFunction[Documents]):
    """Chroma's embedding function for DocAnswer, built on embed_texts()."""

    def __init__(self) -> None:
        # Given: nothing to set up. Chroma warns when __init__ is missing.
        pass

    def __call__(self, input: Documents) -> Embeddings:
        """Embed chunk texts for Chroma's add().

        Input: any number of texts. Output: one vector per text, in order.
        Send them to embed_texts(..., "document") in groups of BATCH_SIZE.
        Note: Chroma passes only the texts, not the metadata.
        """
        raise NotImplementedError("TODO(task 9): embed documents in groups of 20")

    def embed_query(self, input: Documents) -> Embeddings:
        """Embed questions for Chroma's query(query_texts=[...]).

        Input: a list of questions. Output: one vector per question, in order.
        Use embed_texts(..., "question"), so questions get the question format.
        """
        raise NotImplementedError("TODO(task 9): embed questions in the question format")

    # Given: the plumbing Chroma 1.x asks every embedding function for.
    @staticmethod
    def name() -> str:
        return "docanswer-gemini"

    def get_config(self) -> dict[str, Any]:
        return {}

    @staticmethod
    def build_from_config(config: dict[str, Any]) -> "GeminiEmbedding":
        return GeminiEmbedding()

    def default_space(self) -> str:
        return "cosine"


def collection_name() -> str:
    """Given: name the collection after the chunk settings, such as handbook-w120-o1."""
    max_words = os.environ.get("CHUNK_MAX_WORDS", "120")
    overlap = os.environ.get("CHUNK_OVERLAP", "1")
    return f"handbook-w{max_words}-o{overlap}"


def get_collection(name: str):
    """Given: open (or create) the persistent collection, with cosine distance."""
    client = chromadb.PersistentClient(path="chroma")
    return client.get_or_create_collection(
        name=name,
        embedding_function=GeminiEmbedding(),
        configuration={"hnsw": {"space": "cosine"}},
    )


def build_index(chunks: list[dict], collection) -> int:
    """Add the chunks that are not in the collection yet. Return how many were added.

    Input: the chunk dicts from data/chunks.json (chunk_id, doc_id, title,
    section, chunk_no, text, words).

    Must:
        - work in batches of BATCH_SIZE;
        - skip chunk ids stored already: collection.get(ids=batch_ids)["ids"];
          a second run makes no embedding calls;
        - add with ids = chunk_id, documents = text, and metadatas holding
          doc_id, title, section and chunk_no.
    Edge cases: an empty list adds nothing; a run stopped by HTTP 429 continues
    where it stopped when run again.
    """
    raise NotImplementedError("TODO(task 9): add only the new chunks, 20 at a time")


def main() -> None:
    """Given: index data/chunks.json (or its first --limit chunks)."""
    parser = argparse.ArgumentParser(description="Embed DocAnswer's chunks into Chroma.")
    parser.add_argument("--limit", type=int, default=None, help="index only the first N chunks")
    args = parser.parse_args()

    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    if args.limit is not None:
        chunks = chunks[: args.limit]
    name = collection_name()
    collection = get_collection(name)
    added = build_index(chunks, collection)
    print(f"{name}: added {added}, collection has {collection.count()}, chunks in this run {len(chunks)}")


if __name__ == "__main__":
    main()
