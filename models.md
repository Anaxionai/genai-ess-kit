# Models: which model to use for each job

Task briefs never name a model. They name a setting in your `.env` file, such as `CHAT_MODEL`, and link here for its value. Keep each model name in **one place**: your `.env` file, read with `os.environ["CHAT_MODEL"]`. Never type a model name into your code.

**Checked on 24 November 2026** on Google's and Ollama's own pages (links at the bottom).
Google moved the Gemini API documentation from `ai.google.dev/gemini-api/docs` to `aistudio.google.com/docs`; the old links still redirect.
Model names change every few months. If a name below stops working (`404` or "model not found"), open the [models page](https://aistudio.google.com/docs/models), pick the model that replaced it, and tell your mentor so the kit can be updated.

## Your `.env` settings

| Setting | Value on 24 Nov 2026 | What it is for |
|---|---|---|
| `GEMINI_API_KEY` | your own key | Every Gemini call. [`setup/api-key.md`](setup/api-key.md) shows how to get it. Never committed |
| `CHAT_MODEL` | `gemini-3.5-flash-lite` | **The chat model.** Every chat call: `ask.py`, TicketSort, DocAnswer, TaskPilot |
| `EMBED_MODEL` | `gemini-embedding-2` | **The embedding model.** DocAnswer's chunks and questions |
| `JUDGE_MODEL` | `gemini-4-hydrogen` | **The judge model.** A stronger model that grades answers: TicketSort's summary judge, DeepEval in DocAnswer |
| `LOCAL_MODEL` | `qwen3.5:4b`, or `qwen3.5:2b` on 8 GB | **The local model** in Ollama, on your own laptop. See [Ollama models](#ollama-models-local-free-offline) |

A copy-ready `.env` (put your key after the first `=`):

```bash
GEMINI_API_KEY=
CHAT_MODEL=gemini-3.5-flash-lite
EMBED_MODEL=gemini-embedding-2
JUDGE_MODEL=gemini-4-hydrogen
LOCAL_MODEL=qwen3.5:4b
```

Commit a `.env.example` with the same names and **no key**. A task may add its own setting, such as `TASKPILOT_MODEL`; its value is one of the names on this page.

## Gemini API models (cloud, with your free key)

| Job | Model name | Status on 24 Nov 2026 | Free tier | Paid price per 1M tokens (input / output) | Notes |
|---|---|---|---|---|---|
| **Chat model** (`CHAT_MODEL`) | `gemini-3.5-flash-lite` | Stable (last updated July 2026) | Yes | $0.30 / $2.50 | Fast and cheap. Supports JSON output (structured output), function calling and thinking |
| **Judge model** (`JUDGE_MODEL`), also the stronger chat model | `gemini-4-hydrogen` | Stable (November 2026) | Yes | $1.50 / $7.50 | Google's own quickstart uses it. Use it as a judge, or as the chat model only when your evaluation numbers show the chat model is not good enough |
| **Small chat model** | `gemini-3.1-flash-lite` | Stable | Yes | $0.25 / $1.50 | The "smaller model where it is enough" comparison: cost-cutting in TaskPilot, model choice in the capstone |
| **Embedding model** (`EMBED_MODEL`) | `gemini-embedding-2` | Listed, no status label | Yes | $0.20 (text input) | Up to 8,192 tokens per text. **Vector size: 768** (see below) |

- Prices are Google's **Standard** paid prices in US dollars, for when you compare costs. On the free tier you pay nothing, but your prompts may be used by Google ([`setup/api-key.md`](setup/api-key.md)). Thinking tokens are billed as output tokens.
- Google has announced price rises for some other models on 1 December 2026 and 1 January 2027. The four models above had no announced change on 24 November 2026.
- To log the cost of a call, keep the prices in one place in your code (for example `config.py`), with a comment that says the date you read them.

### Models not to use

- `gemini-2.5-flash` and `gemini-2.5-pro` are **deprecated**. From 1 December 2026 Google sends their requests to `gemini-3.5-flash-lite` and `gemini-3.8-flash`. Older tutorials still use them.
- `gemini-2.0-flash`, `gemini-2.0-flash-lite` and `gemini-3-pro-preview` are shut down.
- Names with `preview` or `exp` in them can change or disappear without notice.
- `gemini-4-carbon`, `gemini-4-argon` and `gemini-4-neon` have **no free tier**. You never need them in this course.

## How the course calls Gemini

The course uses the `google-genai` library, at the version in [`VERSIONS.md`](VERSIONS.md), and Google's **Interactions API**, which Google calls the recommended interface for new projects. Older tutorials use `client.models.generate_content(...)`: Google calls it legacy, and it still works, but the course does not use it for text.

### A chat call with a system instruction and token counts

```python
# chat_example.py: one call, a system instruction, the answer and the token counts.
import os

from dotenv import load_dotenv  # uv add python-dotenv
from google import genai

load_dotenv()  # reads GEMINI_API_KEY and CHAT_MODEL from .env
client = genai.Client()  # finds GEMINI_API_KEY in the environment

interaction = client.interactions.create(
    model=os.environ["CHAT_MODEL"],
    system_instruction="You are a support agent for an online shop. Answer in one sentence.",
    input="My parcel is three days late. What can I do?",
    store=False,  # a single call: Google does not keep it
)
print(interaction.output_text)
usage = interaction.usage
print("input tokens:", usage.total_input_tokens)
print("output tokens:", usage.total_output_tokens)
print("total tokens:", usage.total_tokens)
```

- `store=False` on every single call (labelling a ticket, answering a question). An agent loop that uses `previous_interaction_id` cannot use `store=False` (see function calling below).
- Use `total_input_tokens`, `total_output_tokens` and `total_tokens` for counts and cost. Other usage fields exist but the course does not rely on them.
- To limit the answer's length, pass `generation_config={"max_output_tokens": 300}`.

### Never set temperature

The newest Gemini models **ignore `temperature`, `top_p` and `top_k`**, Google has deprecated them, and future models will answer `400` if you send them. **Never set them in a Gemini call.** The same prompt can give different answers; your pipeline copes with that by validating every answer, retrying bad ones and measuring on a whole evaluation set. You can still try temperature on a local Ollama model, where it works.

### JSON output (structured output)

```python
from typing import Literal
from pydantic import BaseModel, Field

class TicketLabel(BaseModel):
    category: Literal["delivery", "refund"] = Field(description="the ticket's category")
    summary: str = Field(description="one sentence")

interaction = client.interactions.create(
    model=os.environ["CHAT_MODEL"],
    system_instruction=open("prompts/v1.txt", encoding="utf-8").read(),
    input=ticket_text,
    response_format={"type": "text", "mime_type": "application/json",
                     "schema": TicketLabel.model_json_schema()},
    store=False,
)
label = TicketLabel.model_validate_json(interaction.output_text)  # may raise ValidationError
```

Pass the JSON Schema (`model_json_schema()`), not the class itself. A `Literal[...]` field becomes a list of allowed values. Always validate: a schema makes bad JSON rare, not impossible, and the API does not check lengths such as `max_length`.

### Function calling (TaskPilot)

- A tool is a dictionary: `{"type": "function", "name": ..., "description": ..., "parameters": <JSON Schema>}`. Pass the list as `tools=[...]` on **every** call: the API does not remember it.
- The model's requests come back in `interaction.steps`: the steps with `step.type == "function_call"` have `step.id`, `step.name` and `step.arguments` (a dictionary).
- Your code runs the function, then sends the result back:
  `client.interactions.create(model=..., tools=tools, previous_interaction_id=interaction.id, input=[{"type": "function_result", "call_id": step.id, "name": step.name, "result": [{"type": "text", "text": result}]}])`
- `previous_interaction_id` needs the earlier interaction to be stored, so the agent loop leaves `store` at its default: Google keeps those interactions. The course data is synthetic, so that is acceptable; never put real personal data in an agent run.
- The course does not use automatic function calling: you write the loop.

## Embeddings (DocAnswer)

### The settings

- **Model:** `EMBED_MODEL` (`gemini-embedding-2`), for the documents **and** the questions. Vectors from two models cannot be compared, so never mix them in one Chroma collection.
- **Vector size: 768.** Pass `output_dimensionality=768`. The default is 3,072 numbers; 768 is one of Google's recommended smaller sizes and keeps Chroma small. `gemini-embedding-2` returns its vectors normalised (length 1) at every size, so cosine distance works directly.
- **No `task_type`.** `gemini-embedding-2` does not accept it. Write the task into the text instead.

### The two text formats

| What you embed | Text you send |
|---|---|
| A document chunk | `title: {document title} \| text: {chunk text}` (use `title: none` when there is no title) |
| A question | `task: search result \| query: {question}` |

For example, a chunk of the annual leave policy is sent as `title: Annual leave | text: You may carry up to 5 unused days...`, and the question as `task: search result | query: Can I carry leave over?`.

### The plain-list trap

**A plain list of strings gives one vector, not one per string.** `embed_content(contents=["text 1", "text 2"])` sends both texts as parts of a single input and returns **one combined vector**. (Checked in the library on 24 November 2026: the request holds one item with two parts.) Wrap each text in its own `types.Content` to get one vector each:

```python
# embed_example.py: one vector of 768 numbers for each text.
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

texts = [
    "title: Annual leave | text: You may carry up to 5 unused days into the next year.",
    "title: Booking work travel | text: Flights under six hours are booked in economy class.",
]
result = client.models.embed_content(
    model=os.environ["EMBED_MODEL"],
    contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],  # one Content per text
    config=types.EmbedContentConfig(output_dimensionality=768),
)
vectors = [e.values for e in result.embeddings]
print(len(vectors), "vectors of", len(vectors[0]), "numbers")  # 2 vectors of 768 numbers
```

Check it every time: the number of vectors must equal the number of texts. Send at most about 50 texts per call.

## DeepEval's judge and temperature (checked 24 November 2026)

DocAnswer's faithfulness judge is DeepEval's `GeminiModel` (DeepEval at the version in [`VERSIONS.md`](VERSIONS.md)). It calls the legacy `generate_content`, which is fine inside a library. But DeepEval 4.3.5 keeps a list of Gemini models, and for a model **not** on that list it sends `temperature=0` with every call. The judge model above, `gemini-4-hydrogen`, is not on the list (checked in the library's source and with a local test server). Switch it off with one line after you create the judge:

```python
from deepeval.models import GeminiModel

judge = GeminiModel(model=os.environ["JUDGE_MODEL"], api_key=os.environ["GEMINI_API_KEY"])
judge._temperature_configured = False  # DeepEval 4.3.5: send no temperature
```

The name starts with `_`, so a later DeepEval version may change it. If the line stops working, check the version in `VERSIONS.md` and tell your mentor.

## Limits, pauses and 429

- **See your limits** on the [rate limit page in AI Studio](https://aistudio.google.com/rate-limit): requests per minute (RPM), input tokens per minute (TPM) and requests per day (RPD), for each model. Google no longer prints the free-tier numbers in its documentation. Limits are per project, not per key, and the daily count resets at midnight Pacific time.
- **Pause after each call** in a batch: `time.sleep(60 / RPM)`, with `RPM` set from your own limit. At 10 requests a minute, 200 tickets take 20 minutes. An embedding call with many texts counts as one request, but its tokens count toward TPM.
- **On a `429`** (`RESOURCE_EXHAUSTED`): wait, then try again with a growing pause (2 s, 4 s, 8 s, 16 s...), at most about five times, then stop and save what you have. If it is the daily limit (RPD), stop for the day or use your `LOCAL_MODEL`. [`setup/api-key.md`](setup/api-key.md) has the details.

### The library's own retries (checked 24 November 2026)

We checked `google-genai` 3.6.1 by reading its source and by running it against a local test server that always answers `429`:

- **`client.interactions.create` retries by itself.** By default it tries **5 times in total** (the first call plus 4 retries) on `408`, `429`, `500`, `502`, `503` and `504`, waiting about 1, 2, 4 and 8 seconds with some randomness. In our test it gave up after 5 requests and about 7 seconds, then raised `RateLimitError`.
- **`client.models.embed_content` and `generate_content` do not retry by default.** They make one request and raise `google.genai.errors.ClientError` with `code == 429`.
- **To switch the retries off** (so your own backoff code sees every error), or to change them, create the client with `HttpRetryOptions`:

  ```python
  from google import genai
  from google.genai import types

  client = genai.Client(http_options=types.HttpOptions(
      retry_options=types.HttpRetryOptions(attempts=1)))  # 1 = no retries
  ```

  `attempts` counts the first call. `HttpRetryOptions` also takes `initial_delay`, `max_delay`, `exp_base`, `jitter` and `http_status_codes`. Setting `retry_options` also turns on retries for `embed_content`.
- **The error classes** for the Interactions API are in `google.genai._interactions`: `APIStatusError` (has `.status_code`), its subclass `RateLimitError` (429), and `APIConnectionError` (no connection; our test raised it when nothing was listening). The module name starts with `_`, so it may move in a later version: if the import fails, check the version in [`VERSIONS.md`](VERSIONS.md).

## Ollama models (local, free, offline)

Ollama runs small open models on your own laptop. Use them for TicketSort's cloud-versus-local comparison, and when you have no internet or have hit your daily limit. Nothing leaves your laptop, so there is no free-tier data question. Install Ollama with [`setup/windows.md`](setup/windows.md).

Checked on 24 November 2026 on [ollama.com/library](https://ollama.com/library). Sizes are the download sizes; a model needs roughly that much free memory to run.

| Use | Model name | Download | Fits |
|---|---|---|---|
| **Small local model** (`LOCAL_MODEL`) | `qwen3.5:4b` | 3.3 to 4.0 GB | 16 GB laptops; slow but possible on 8 GB |
| **Smallest local model for 8 GB laptops** (`LOCAL_MODEL` on 8 GB) | `qwen3.5:2b` | 2.7 to 3.1 GB | 8 GB laptops |
| Second choice on 8 GB, if `qwen3.5:2b` is too slow | `llama3.2:3b` | 2.0 GB | 8 GB laptops |
| A second model to compare, 16 GB only | `gemma4:e4b` | 6.6 GB | 16 GB laptops |
| Local embeddings (optional) | `embeddinggemma` | 622 MB | any |

- All four chat models are tagged **tools** on Ollama (they can call functions). `qwen3.5` and `gemma4` are also tagged **thinking**: they may reason before answering, which is slower.
- `embeddinggemma` needs Ollama 0.11.10 or newer and takes up to 2,000 tokens of text. Its vectors are not comparable with Gemini's: one Chroma collection uses one or the other.
- On 8 GB, close browser tabs you do not need and quit Docker Desktop while a local model runs.
- Ollama listens on `http://localhost:11434`. The Python library is `ollama` (version in [`VERSIONS.md`](VERSIONS.md)):

  ```python
  import os
  import ollama

  reply = ollama.chat(model=os.environ["LOCAL_MODEL"],
                      messages=[{"role": "user", "content": "Where is my parcel?"}],
                      options={"temperature": 0})  # temperature works on Ollama
  print(reply.message.content)
  ```

Pull a model once; then it works offline:

```bash
ollama pull qwen3.5:2b
ollama run qwen3.5:2b "Say hello in five words."
```

## Sources (read on 24 November 2026)

- Models: https://aistudio.google.com/docs/models (redirected from https://ai.google.dev/gemini-api/docs/models)
- Model pages: https://aistudio.google.com/docs/models/gemini-3.5-flash-lite and https://aistudio.google.com/docs/models/gemini-4-hydrogen
- Prices and the free tier: https://aistudio.google.com/docs/pricing
- Rate limits: https://aistudio.google.com/docs/rate-limits
- Quickstart (Interactions API): https://aistudio.google.com/docs/quickstart
- Tokens: https://aistudio.google.com/docs/tokens
- Structured output: https://aistudio.google.com/docs/structured-output
- Function calling: https://aistudio.google.com/docs/function-calling
- Embeddings: https://aistudio.google.com/docs/embeddings
- The library: https://pypi.org/project/google-genai/ (3.6.1) and https://github.com/googleapis/python-genai (retry code in `google/genai/_api_client.py`)
- Ollama: https://ollama.com/library/qwen3.5, https://ollama.com/library/llama3.2, https://ollama.com/library/gemma4/tags, https://ollama.com/library/embeddinggemma
