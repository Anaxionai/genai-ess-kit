"""Cut the documents into chunks that keep their source (task 8).

Run it from inside docanswer/:
    uv run --env-file .env python chunk.py

You write all four functions. split_text() is pure: no model and no files.
"""

from pathlib import Path

CHUNKS_FILE = Path("data/chunks.json")


def split_text(text: str, max_words: int = 120, overlap: int = 1) -> list[str]:
    """Pack whole sentences into chunks of at most max_words words.

    Input: the text of one section.
    Output: a list of chunk strings.

    Must:
        - split into sentences with re.split(r"(?<=[.!?])\\s+|\\n+", text),
          so each bullet line is a sentence too, and drop empty pieces;
        - never cut a sentence;
        - start each new chunk with the last `overlap` sentences of the one before.
    Edge cases the tests check:
        - a short text gives exactly one chunk;
        - no chunk passes max_words (a single sentence longer than max_words
          becomes a chunk on its own);
        - neighbouring chunks share `overlap` sentences;
        - no sentence is lost.
    """
    raise NotImplementedError("TODO(task 8): pack whole sentences into chunks with an overlap")


def split_sections(text: str) -> list[tuple[str, str]]:
    """Cut a document at its "## " headings.

    Output: (heading, body) pairs in document order. Text before the first
    heading gets the heading "intro".
    Edge case: no chunk may cross a heading, so every chunk comes from one body.
    """
    raise NotImplementedError("TODO(task 8): cut the document at its ## headings")


def chunk_documents(docs: list[dict], max_words: int, overlap: int) -> list[dict]:
    """Chunk every document, section by section, with split_text().

    Input: the records from load.load_documents().
    Output: one dict per chunk with
        chunk_id  "<doc_id>#<n>", such as "travel-booking#2"
        doc_id, title, section
        chunk_no  counts from 0 across the whole document (not per section)
        text, words
    """
    raise NotImplementedError("TODO(task 8): chunk each section and keep the source fields")


def main() -> None:
    """Load the documents, chunk them and write CHUNKS_FILE.

    Read CHUNK_MAX_WORDS and CHUNK_OVERLAP from the environment (defaults 120
    and 1). Print, for example, "40 documents, 260 chunks".
    """
    raise NotImplementedError("TODO(task 8): write data/chunks.json and print the counts")


if __name__ == "__main__":
    main()
