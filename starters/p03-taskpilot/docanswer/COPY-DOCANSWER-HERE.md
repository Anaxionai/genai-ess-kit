# Your DocAnswer goes here

This folder is empty on purpose. TaskPilot's search tool reuses **your own** DocAnswer from task 3.23, not a new search.

In task 6 (step 2), copy the **contents** of your finished `docanswer/` folder here, with its `data/` and `chroma/` folders. From the task 6 folder, in Git Bash:

```bash
cp -r <path to your 3.23 folder>/docanswer/. taskpilot/docanswer/
rm -rf taskpilot/docanswer/.venv
```

The `/.` at the end of the source copies what is inside `docanswer/`, so you do not get `docanswer/docanswer/`.

Then make the one edit task 6 asks for: in `docanswer/index.py`, build the Chroma path from `__file__`, so the index is found from any folder. `tools.py` puts this folder on the import path, so `from search import top_passages` finds your `search.py`.

You may delete this note once your copy is in.
