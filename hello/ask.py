# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "google-genai==3.6.1",
# ]
# ///
"""ask.py: send one prompt to a Gemini model and print the answer and the token counts.

Run it with uv, from the folder that holds your .env file:

    uv run ask.py "Explain a token in one sentence."
    uv run ask.py --file prompt.txt
    uv run ask.py

The script reads GEMINI_API_KEY and CHAT_MODEL from a .env file in the current
folder (or next to this script). The key never appears in the code, and .env is
never committed. The model names are in the kit's models.md.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

# Used only when .env has no CHAT_MODEL line: the kit's chat model on 24 Nov 2026 (see models.md).
DEFAULT_MODEL = "gemini-3.5-flash-lite"
DEFAULT_PROMPT = "In two short sentences, explain what a token is in a language model."


def read_env_file(path: Path) -> dict[str, str]:
    """Read KEY=value lines from a .env file. Blank lines and # comments are skipped."""
    values: dict[str, str] = {}
    # utf-8-sig also removes the invisible mark that some editors put at the start of a file.
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip().removeprefix("export ").strip()
        value = value.strip().strip('"').strip("'")
        values[name] = value
    return values


def find_setting(name: str) -> tuple[str | None, str]:
    """Return (value, where it came from) for a setting such as GEMINI_API_KEY.

    A .env file in the current folder wins, then one next to this script,
    then the environment.
    """
    for folder in (Path.cwd(), Path(__file__).resolve().parent):
        env_path = folder / ".env"
        if env_path.is_file():
            value = read_env_file(env_path).get(name, "")
            if value:
                return value, str(env_path)
    value = os.environ.get(name, "")
    if value:
        return value, f"the {name} environment variable"
    return None, ""


def explain_error(error: Exception) -> str:
    """Turn the common API errors into a sentence that says what to do."""
    status = getattr(error, "status_code", None)
    name = type(error).__name__
    if status == 429:
        return ("429: you went over a rate limit (requests per minute, tokens per minute or "
                "requests per day). The library already tried 5 times. Wait a minute and run "
                "it again. See setup/api-key.md.")
    if status in (400, 401, 403) and "key" in str(error).lower():
        return ("The API rejected your key. Check that .env has one line, "
                "GEMINI_API_KEY=<your key>, with no spaces or quotes, and that the key "
                "still exists in Google AI Studio.")
    if status == 404:
        return "404: the model name was not found. Check the current names in models.md."
    if status is not None and status >= 500:
        return f"{status}: a problem on Google's side. Wait a minute and try again."
    if "Connect" in name or "Timeout" in name:
        return "Could not reach the API. Check your internet connection and try again."
    return f"{name}: {error}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Send one prompt to a Gemini model.")
    parser.add_argument("prompt", nargs="*", help="the prompt, in quotes (default: a question about tokens)")
    parser.add_argument("--file", help="read the prompt from this text file instead")
    parser.add_argument("--model", help="a model name from models.md (default: CHAT_MODEL in .env)")
    args = parser.parse_args()
    if args.file:
        prompt = Path(args.file).read_text(encoding="utf-8-sig").strip()
    else:
        prompt = " ".join(args.prompt) or DEFAULT_PROMPT
    if not prompt:
        print("The prompt is empty.", file=sys.stderr)
        return 1
    model = args.model or find_setting("CHAT_MODEL")[0] or DEFAULT_MODEL

    key, source = find_setting("GEMINI_API_KEY")
    if not key:
        print("No API key found. Create a file named .env in this folder with one line:\n"
              "    GEMINI_API_KEY=<your key>\n"
              "setup/api-key.md shows how to get a free key.", file=sys.stderr)
        return 1

    from google import genai  # imported here so the key check above runs first

    client = genai.Client(api_key=key)
    shown = prompt if len(prompt) <= 300 else prompt[:300] + " ..."
    print(f"Model:  {model}   (key from {source})")
    print(f"Prompt: {shown}\n", flush=True)

    started = time.perf_counter()
    try:
        # store=False: Google does not keep this interaction after answering.
        interaction = client.interactions.create(model=model, input=prompt, store=False)
    except Exception as error:  # noqa: BLE001 - every API error gets a plain-English line
        print(explain_error(error), file=sys.stderr)
        return 2
    seconds = time.perf_counter() - started

    print(interaction.output_text or "(the model returned no text)")
    print()

    usage = interaction.usage
    if usage is None:
        print("The API returned no token counts for this call.")
        return 0
    print("Tokens")
    print(f"  input (your prompt):  {usage.total_input_tokens or 0}")
    print(f"  output (the answer):  {usage.total_output_tokens or 0}")
    print(f"  total:                {usage.total_tokens or 0}")
    print(f"Time: {seconds:.1f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
