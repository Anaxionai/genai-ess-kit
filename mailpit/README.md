# Mailpit: email that never leaves your laptop

TaskPilot drafts and sends emails. In this course they go to **Mailpit**, a pretend mail server that runs in Docker on your laptop. It accepts every email, keeps it, and shows it on a web page. **Nothing is ever delivered to a real inbox**, so a mistake or an attack costs nothing.

Checked on 24 November 2026 with Mailpit `v1.34.0` (the image in [`compose.yml`](compose.yml)), Docker Desktop and the Mailpit docs at https://mailpit.axllent.org/docs/install/docker/.

## Start it

Docker Desktop must be running ([`../setup/windows.md`](../setup/windows.md), Step 8). In Git Bash:

```bash
cd ~/genai-ess-kit/mailpit
docker compose up -d
```

Then open http://localhost:8025. You see Mailpit's inbox, empty.

| Port | What it is for |
|---|---|
| **1025** | SMTP: your code sends email to `localhost:1025` |
| **8025** | The web page, and the API that your tests read |

Both ports listen only on your own laptop (`127.0.0.1`), not on your network.

Check it: `docker compose ps` shows `mailpit` with the status `Up`.

## Send an email from Python

```python
import os
import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["From"] = "taskpilot@fernhill.example"
msg["To"] = "alex.chen@fernhill.example"
msg["Subject"] = "Meeting notes"
msg.set_content("Here are the notes from today.")

host = os.environ.get("SMTP_HOST", "localhost")
port = int(os.environ.get("SMTP_PORT", "1025"))
with smtplib.SMTP(host, port) as smtp:
    smtp.send_message(msg)
```

No user name, password or TLS is needed. The email appears at http://localhost:8025 at once.

## Read and clear emails from code (the API)

Your job runner and attack tests check Mailpit through its API, not by eye:

```bash
curl -s "http://localhost:8025/api/v1/messages?limit=1"      # the newest message, as JSON
curl -s -X DELETE "http://localhost:8025/api/v1/messages"     # delete every message
```

In Python, with no extra library:

```python
import json
import urllib.request

with urllib.request.urlopen("http://localhost:8025/api/v1/messages?limit=10") as r:
    data = json.load(r)
print(data["total"], "messages")
for m in data["messages"]:
    print(m["Subject"], [t["Address"] for t in m["To"]])

urllib.request.urlopen(urllib.request.Request("http://localhost:8025/api/v1/messages", method="DELETE"))
```

Each message has `ID`, `From`, `To` (a list of `{"Name", "Address"}`), `Subject`, `Snippet` and `Created`. The full API is at https://mailpit.axllent.org/docs/api-v1/.

## Stop it

```bash
docker compose down
```

Mailpit keeps messages **in memory inside the container**, so `docker compose down` deletes them; `docker compose stop` and `start` keep them. It keeps at most the newest 500 (`MP_MAX_MESSAGES`).

## Mailpit inside your own Compose file

When you package TaskPilot with Docker Compose (P3), your `compose.yml` gets its own `mailpit` service, with the same image. Then:

- Inside Compose, TaskPilot reaches Mailpit by its **service name**: `SMTP_HOST=mailpit`, `SMTP_PORT=1025`. `localhost` inside a container means that container itself.
- **Stop the kit's Mailpit first** (`docker compose down` in this folder), or the ports 1025 and 8025 are already taken.

## If something goes wrong

| What you see | What to do |
|---|---|
| `ConnectionRefusedError` when sending | Mailpit is not running. Run `docker compose ps` here, then `docker compose up -d` |
| `port is already allocated` | Another Mailpit (or your TaskPilot Compose file) uses 1025 or 8025. Run `docker ps` and stop it with `docker stop <name>` |
| `error during connect` | Start Docker Desktop and wait for **Engine running** |
| The page at http://localhost:8025 is empty after a restart | Expected after `docker compose down`: messages live in memory |
