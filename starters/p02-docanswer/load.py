"""Load the handbook and record where every document came from (task 7).

Run it from inside docanswer/:
    uv run python load.py

You write all three functions. The handbook's header format is in
~/genai-ess-kit/data/handbook/README.md.
"""

from pathlib import Path

HANDBOOK = Path("data/handbook")
MANIFEST = Path("sources.csv")


def read_document(path: Path) -> dict:
    """Read one handbook file and return its record.

    Input: the path of one Markdown file.
    Output: a dict with
        doc_id      the file name without .md, such as "travel-booking"
        file        the file name
        title       the text after the first "# " line
        department  from the "Department: " line
        updated     from the "Updated: " line (YYYY-MM-DD)
        text        the whole file as text
        words       the number of words in the text
        sha256      the SHA-256 hex digest of the file's bytes (hashlib.sha256)

    Edge cases the task checks:
        - a file with no "# " title line raises ValueError naming the file;
        - open the file with encoding="utf-8" (the rupee sign, ₹).
    """
    raise NotImplementedError("TODO(task 7): parse the header lines and hash the file")


def load_documents(folder: Path) -> list[dict]:
    """Read every *.md file in folder, in name order, with read_document().

    Output: one record per document (40 for the handbook).
    Edge case: a document with no title raises ValueError naming the file.
    """
    raise NotImplementedError("TODO(task 7): read every Markdown file in name order")


def main() -> None:
    """Load HANDBOOK, write MANIFEST and print a summary.

    MANIFEST (sources.csv) has one row per document and no text column.
    Print the document count, the total words, and the shortest and the
    longest document.
    """
    raise NotImplementedError("TODO(task 7): write sources.csv and print the summary")


if __name__ == "__main__":
    main()
