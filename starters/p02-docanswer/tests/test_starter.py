"""Given: checks of the starter's own set-up. They make no API calls."""

import importlib

import pytest

MODULES = ["load", "chunk", "index", "search", "answer", "evaluate", "faithfulness", "api"]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name):
    importlib.import_module(name)


def test_read_questions(tmp_path):
    from evaluate import read_questions

    path = tmp_path / "questions.csv"
    path.write_text("id,question,expected_source\nq01,Can I carry leave over?,leave-annual\n", encoding="utf-8")
    assert read_questions(path) == [
        {"id": "q01", "question": "Can I carry leave over?", "expected_source": "leave-annual"}
    ]


def test_collection_name_follows_the_settings(monkeypatch):
    from index import collection_name

    monkeypatch.delenv("CHUNK_MAX_WORDS", raising=False)
    monkeypatch.delenv("CHUNK_OVERLAP", raising=False)
    assert collection_name() == "handbook-w120-o1"
    monkeypatch.setenv("CHUNK_MAX_WORDS", "200")
    monkeypatch.setenv("CHUNK_OVERLAP", "2")
    assert collection_name() == "handbook-w200-o2"


def test_get_collection_uses_cosine(tmp_path, monkeypatch):
    # Runs in a temporary folder, so it never touches your real chroma/ index.
    from index import GeminiEmbedding, get_collection

    monkeypatch.chdir(tmp_path)
    collection = get_collection("starter-check")
    assert collection.count() == 0
    assert collection.configuration["hnsw"]["space"] == "cosine"
    assert isinstance(collection.configuration["embedding_function"], GeminiEmbedding)
