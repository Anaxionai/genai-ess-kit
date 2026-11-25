# Your free Gemini API key

Every program in this course calls a Gemini model with **your own free API key**: a secret code that lets your program use Google's models.
This page shows how to get one, how to keep it safe, what the free tier costs you in privacy, and how to read your limits.

**Checked on 24 November 2026** against Google's Gemini API documentation (links at the bottom).
The model names are in [`../models.md`](../models.md).

## 1. Get the key (5 minutes)

You need a personal Google account. Google's terms say you must be **18 or older** to use the API. If you are not, tell your mentor.

1. Open the API keys page in Google AI Studio: https://aistudio.google.com/apikey and sign in.
2. Accept the terms if AI Studio asks you to.
3. Select **Create API key**. AI Studio puts the key in a Google Cloud project for you.
4. Copy the key. Treat it like a password: anyone who has it can use your quota.

Notes:

- **Create the key in AI Studio**, not in the Google Cloud console. A project brought in from Google Cloud may need verification before it can use the free tier.
- If you already use Google Cloud, AI Studio may not make a project for you. Import an existing project when it asks, or ask your mentor.
- The API rejects keys that are not restricted. Keys made in AI Studio are set up correctly; do not change their restrictions.
- You do not need a payment card. Do not add billing: the course never needs it.

## 2. Keep it in `.env`, never in Git

Put the key in a file named `.env` in the folder where you run your program. The file has one line:

```bash
GEMINI_API_KEY=paste-your-key-here
```

No spaces around `=`, and no quotes. Make it in Git Bash (replace the text after `=`):

```bash
echo "GEMINI_API_KEY=paste-your-key-here" > .env
```

Or in VS Code: **File > New File**, save it as `.env`. (Windows Notepad may save it as `.env.txt`. In the Save dialog, choose **All files** for the type.)

Then protect it:

1. Your repository's `.gitignore` must list `.env`. Check it:

   ```bash
   git check-ignore -v .env
   ```

   It prints the `.gitignore` line that matches. **If it prints nothing, Git would commit your key.** Add a line `.env` to `.gitignore` first.
2. Commit a `.env.example` with the name only, so a reader knows the setting exists:

   ```bash
   GEMINI_API_KEY=
   ```

3. Never paste the key into code, a notebook, a screenshot, `evidence.md`, a chat with an AI, or a message to your mentor.

Every task that calls a model has the rule **"No API key, token or other secret in any committed file."** AxReview checks it.

**If a key reaches GitHub, or anyone else sees it:** open https://aistudio.google.com/apikey, create a new key, put it in `.env`, then delete the old key. Do this at once, even if the repository is private. Removing the line in a new commit is not enough: the old commit still holds it.

### How your program reads the key

- The library `google-genai` finds the key in the `GEMINI_API_KEY` environment variable. If `GOOGLE_API_KEY` is also set, that one wins, so do not set both.
- A `.env` file is not the environment by itself. Load it in one of these ways:
  - `uv run --env-file .env python main.py` (no library needed);
  - the `python-dotenv` library: `from dotenv import load_dotenv` then `load_dotenv()` at the top of your program;
  - read it yourself, as [`../hello/ask.py`](../hello/ask.py) does.

## 3. The free tier: what you get and what you give

- **It costs nothing.** The models in [`../models.md`](../models.md) are free of charge on the free tier, within your rate limits.
- **Google may use what you send.** On the free tier, Google uses your prompts and the answers to improve its products, and **human reviewers may read them**. Google's terms say: *"Do not submit sensitive, confidential, or personal information to the Unpaid Services."*
- So, in this course:
  - Use only the course's made-up data: the kit's tickets, handbook, calendar, transcripts and resumes are all synthetic.
  - **Never send personal data**: not your own resume, not a friend's messages, not real customer data, not phone numbers, addresses or ID numbers.
  - Never send your API key, passwords or your employer's documents.
- (In the European Economic Area, the UK and Switzerland, Google applies its paid-service data terms to the free tier too. The course's rule stays the same everywhere: synthetic data only.)

## 4. Read your rate limits

A **rate limit** is the most you may use in a time window. Google counts three things for each model:

| Limit | Means | Resets |
|---|---|---|
| **RPM**, requests per minute | how many calls you make in a minute | every minute |
| **TPM**, input tokens per minute | how much text you send in a minute | every minute |
| **RPD**, requests per day | how many calls you make in a day | at midnight Pacific time: 13:30 in India from November to early March, 12:30 from March to early November |

- Limits are **per project, not per key**. A second key in the same project gives you nothing more.
- Going over **any one** of them gives an error, even if the others are fine.
- Google no longer prints the free-tier numbers in its documentation, and they change. **See your own numbers** on https://aistudio.google.com/rate-limit: pick the model, and read RPM, TPM and RPD. Your use so far is at https://aistudio.google.com/usage.
- Write your limits for the main chat model into your notes on day 1. You will plan TicketSort's 200-ticket runs around them.

### Plan a batch around the limits

Before you run 200 calls, do the sums:

- 200 tickets at a limit of, say, 10 RPM takes at least 20 minutes. Put a pause between calls (`time.sleep(60 / rpm)`).
- If your RPD is lower than the number of calls you need in a day, split the run over two days, or use a local Ollama model for the practice runs (see [`../models.md`](../models.md)).
- Test on 5 tickets first. Run all 200 only when 5 work.

## 5. What to do on a `429`

`429 RESOURCE_EXHAUSTED` means you went over a limit. It is not a bug in your code.

1. **Stop and wait.** Wait at least a minute, then try again. Do not retry at once in a loop: that uses more of your quota.
2. **In code, back off.** Retry after a growing wait (2 s, 4 s, 8 s, 16 s, with a little randomness), at most about five times, then stop and save your progress. TicketSort teaches this.
3. **Keep a resume file.** Write each result to a file as soon as you get it, so a re-run skips the work already done.
4. **If it is the daily limit (RPD)**, waiting a minute does not help. Stop for the day, or switch to a local Ollama model, or to the small chat model in [`../models.md`](../models.md), which has its own limits.

Other errors you may see:

| Error | Means | What to do |
|---|---|---|
| `400` with "API key not valid" | The key is wrong, or `.env` has spaces or quotes | Copy the key again into `.env` |
| `403` | The key is blocked or the project is not allowed to use the API | Create a new key in AI Studio |
| `404` | The model name is wrong or the model was retired | Check [`../models.md`](../models.md) |
| `500` or `503` | A problem on Google's side | Wait a minute and try again |

## Sources (read on 24 November 2026)

- API keys: https://aistudio.google.com/docs/api-key
- Rate limits: https://aistudio.google.com/docs/rate-limits
- Prices and the free tier: https://aistudio.google.com/docs/pricing
- Terms of service: https://aistudio.google.com/docs/terms
