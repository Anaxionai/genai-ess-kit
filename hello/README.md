# Hello: a model answers you on day 1

`ask.py` is a ready-made script. It reads your API key and the model name from `.env`, sends one prompt to a Gemini model, and prints the answer and the **token counts**: how many tokens your prompt used, how many the answer used, and the total.
You do not write code today. You run it, read it, and change the prompt.

## What you need

- Your free API key in a `.env` file: [`../setup/api-key.md`](../setup/api-key.md).
- **uv**, the tool that runs Python for you. If you have not installed it yet, run this once in **PowerShell**, then close and reopen the terminal:

  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

  Check it: `uv --version` prints a version number. (Day 2's two laptop tasks set up the rest.)

You do not need to install Python or any library. The first lines of `ask.py` list what it needs, and `uv run` downloads Python 3.12 and the `google-genai` library the first time. That takes a minute; later runs start at once.

## Run it

1. Make a folder for your experiments and go into it. In PowerShell or Git Bash:

   ```bash
   mkdir hello
   cd hello
   ```

2. Get `ask.py` into the folder. On day 1, open `hello/ask.py` in the kit on GitHub, select **Download raw file** (the download arrow above the code), and save it into the folder. If you have cloned the kit, copy it instead: `cp ~/genai-ess-kit/hello/ask.py .` (Git Bash). Or download it from the terminal:

   ```bash
   curl -O https://raw.githubusercontent.com/Anaxionai/genai-ess-kit/main/hello/ask.py
   ```

   In PowerShell, type `curl.exe` instead of `curl` (PowerShell's own `curl` is a different command).

3. Make `.env` in the same folder, in VS Code, with these two lines ([`../setup/api-key.md`](../setup/api-key.md), section 2). Take the chat model's name from [`../models.md`](../models.md):

   ```bash
   GEMINI_API_KEY=<your key>
   CHAT_MODEL=<the chat model from models.md>
   ```

   If `CHAT_MODEL` is missing, `ask.py` uses the kit's chat model of 24 November 2026.
4. Run it in one of two ways:

   ```bash
   uv run ask.py "Explain what an API key is in two sentences."
   uv run ask.py --file prompt.txt
   ```

   The first form takes the prompt in quotes. The second reads the prompt from a text file, which is easier for long prompts with several lines: make `prompt.txt` in the same folder first. With no prompt at all, `uv run ask.py` asks a question about tokens.

You see something like this (the words and numbers will differ):

```text
Model:  gemini-3.5-flash-lite   (key from C:\Users\you\hello\.env)
Prompt: Explain what an API key is in two sentences.

An API key is a secret code that identifies your program when it calls a service. The service uses it to check that you are allowed in and to count how much you use.

Tokens
  input (your prompt):  11
  output (the answer):  38
  total:                49
Time: 1.2 s
```

## Change it

- Your own prompt, in quotes: `uv run ask.py "Rewrite this in plain English: Kindly do the needful."`
- Another model, by name from [`../models.md`](../models.md), for one run: `uv run ask.py --model <model name> "Say hello in five words."`
- Run the same prompt three times. Do you get the same answer? Do the token counts change?
- Make the prompt twice as long. What happens to the input tokens? To the time?

## Read it

Open `ask.py` in VS Code. Find:

- `find_setting`: where the key and the model name come from (`.env`). The key is never in the code.
- `client.interactions.create(model=..., input=..., store=False)`: the one line that calls the model. `store=False` asks Google not to keep the conversation after it answers.
- `interaction.output_text`: the answer.
- `interaction.usage`: the token counts. Some models also "think" before they answer; those tokens are billed as output, so the total can be more than input plus output.
- `explain_error`: what each error means, such as `429` (too many requests).

## If something goes wrong

| What you see | What to do |
|---|---|
| `No API key found` | `.env` is not in the folder you ran from, or its name is `.env.txt`. Run `ls -a` and check. |
| `The API rejected your key` | Copy the key again. The line must be `GEMINI_API_KEY=...` with no spaces or quotes. |
| `429: you went over a rate limit` | Wait a minute and run it again. [`../setup/api-key.md`](../setup/api-key.md), section 5. |
| `404: the model name was not found` | The model was renamed. Check [`../models.md`](../models.md). |
| `uv` is not recognised | Close every terminal and VS Code, then open them again. |
| `UnicodeEncodeError` or `charmap` | Run `setx PYTHONUTF8 1` in PowerShell once, then reopen the terminal. |

Never commit `.env`. If you put this folder in Git, check `git check-ignore -v .env` first.
