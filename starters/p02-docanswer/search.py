"""Find the passages nearest to a question (task 9).

Run it from inside docanswer/:
    uv run --env-file .env python search.py

TaskPilot (P3) imports top_passages() from this file, so keep its name and
signature.
"""

from index import collection_name, get_collection


def top_passages(question: str, k: int = 3) -> list[dict]:
    """Return the k chunks nearest to the question, nearest first.

    Use get_collection(collection_name()) and collection.query(...).
    Output: one dict per passage with
        chunk_id, doc_id, title, section, text and distance (cosine distance,
        smaller is nearer).
    """
    raise NotImplementedError("TODO(task 9): query the collection and return the passages")


def main() -> None:
    """Print your 10 questions, each with its top 3 chunk ids and distances.

    Write the 10 questions yourself, about 10 different documents, in your
    own words.
    """
    raise NotImplementedError("TODO(task 9): print ten questions with their top 3 chunks")


if __name__ == "__main__":
    main()
