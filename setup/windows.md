# Set up your Windows laptop

This guide sets up a Windows 11 laptop for the whole course. Everything runs on Windows.
Follow it section by section; after each step, run its check before you go on.

- **Day 1** (Launchpad task 3): VS Code and uv, in **PowerShell**. That is all you need for `hello/ask.py`.
- **Day 2, part 1** (Launchpad task 8): Git Bash in VS Code, line endings, Python 3.12, UTF-8 and the course kit. Steps 2 to 6, all in Git Bash.
- **Day 2, part 2** (Launchpad task 9): WSL 2, Docker Desktop, and Ollama if you have the disk space. Steps 7, 8 and 10.
- **Later**: Node.js, before TaskPilot (week 6); Ollama in week 3 if you skipped it.

From Launchpad task 8 on, **Git Bash is your terminal**, inside VS Code. Run every course command in Git Bash, unless a step says PowerShell.
The versions the course uses are in [`../VERSIONS.md`](../VERSIONS.md). The model names are in [`../models.md`](../models.md).

## Before you start

- **Windows 11, version 23H2 or newer.** Press Windows+R, type `winver` and press Enter to see your version. Docker Desktop needs 23H2 or newer.
- **At least 8 GB of memory** and **20 GB of free disk space** (Docker Desktop and a small local model take most of it).
- **Virtualisation turned on.** Open Task Manager, select Performance, then CPU. It must say `Virtualization: Enabled`. If it says Disabled, ask your mentor to turn on Intel VT-x or AMD SVM in the laptop's BIOS.
- **An administrator account** on the laptop, for WSL 2 and Docker Desktop.
- Keep the charger plugged in. If your laptop does not run Windows, ask your mentor for the matching steps.

## Day 1: VS Code and uv (PowerShell)

This is Launchpad task 3. You have no Git Bash yet, so every command here runs in PowerShell.

### VS Code

1. Install VS Code from https://code.visualstudio.com/download with the default options.
2. Open VS Code, select **Extensions** (Ctrl+Shift+X), search for **Python** and install the extension from Microsoft.

Check it: open **PowerShell** (press the Windows key, type `PowerShell`, press Enter) and run `code --version`. It prints a version number.

### uv

uv installs Python and runs your programs. In **PowerShell**, run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close every terminal window and VS Code, then open a new PowerShell window and check it:

```powershell
uv --version
```

It prints `uv` and a version number. You do not install Python yourself: the first `uv run` downloads it. You can now run [`../hello/ask.py`](../hello/README.md).

## Day 2: the rest of the laptop

Launchpad task 7 does Step 1. Task 8 (part 1) does Steps 2 to 6, all in Git Bash. Task 9 (part 2) does Steps 7, 8 and 10: only the `wsl` commands and the Ollama installer there run in PowerShell. Step 9 is a rule to read now; you need it from week 6.

### Step 1: Git for Windows

You installed Git in Launchpad task 7, from https://git-scm.com/downloads/win with the default options. Those options include Git Bash and Git Credential Manager (for signing in to GitHub).

Check it in Git Bash: `git --version` prints `git version 2.` and more numbers. Any version from 2.45 is fine.

### Step 2: Git Bash in VS Code

Part 1 (Launchpad task 8) starts here.

1. In VS Code, press Ctrl+Shift+P and type `Terminal: Select Default Profile`.
2. Choose **Git Bash**.

Check it: open a new terminal (**Terminal**, then **New Terminal** in the top menu). The prompt shows `MINGW64`, and `uname -s` prints a line that starts with `MINGW64`.

### Step 3: Line endings

Windows ends each line of a text file with two characters (CRLF), and Linux ends it with one (LF).
Containers need LF: a file saved with CRLF can fail inside a container with errors such as `$'\r': command not found`.

1. In VS Code, open **Settings** (Ctrl+,) and search for `eol`.
2. Set **Files: Eol** to `\n`.

Check it: open a new file. The status bar at the bottom right shows `LF`, not `CRLF`. In Git Bash, this prints the setting:

```bash
grep eol "$APPDATA/Code/User/settings.json"
```

If it prints nothing, set **Files: Eol** under the **User** tab of Settings, not Workspace.

### Step 4: Python 3.12 through uv

In Git Bash:

```bash
uv --version
uv python install 3.12
uv run --python 3.12 python --version
```

The last line prints `Python 3.12.` and more numbers. uv's Python is the only Python you need. When a course command says `uv run`, uv starts this Python for you.

Three ways you will use uv:

| Command | What it does |
|---|---|
| `uv run ask.py` | Runs a single script. If the script lists its libraries in a `# /// script` block at the top (like `hello/ask.py`), uv installs them first |
| `uv init --no-package --python 3.12 ticketsort` then `uv add google-genai pydantic` | Makes a project folder with `pyproject.toml` and `uv.lock`, and adds libraries to it |
| `uv run pytest` | Runs a command inside the project's environment |

### Step 5: Python and UTF-8

In Git Bash, Python cannot print some characters (such as `₹` or `é`) through a pipe or into a file unless UTF-8 mode is on. Model answers often contain such characters.
Turn it on once, in Git Bash (the same command works in PowerShell):

```bash
setx PYTHONUTF8 1
```

Then close and reopen VS Code. Check it in Git Bash:

```bash
uv run python -c "print('₹ ok')" | cat
```

You see `₹ ok`. An error that names `charmap` means the setting is not on yet: reopen VS Code.

### Step 6: Clone the course kit

In Git Bash:

```bash
cd ~ && git clone https://github.com/Anaxionai/genai-ess-kit.git
```

This makes the folder `~/genai-ess-kit`, which is `C:\Users\<your name>\genai-ess-kit`.
Keep it next to your course repository, never inside it. When a task says so, update it with `git pull` in that folder.

Check it: `ls ~/genai-ess-kit` lists `README.md`, `VERSIONS.md`, `models.md`, `setup` and `data`.

### Step 7: WSL 2

Part 2 (Launchpad task 9) starts here.

WSL 2 runs a small Linux system inside Windows. Docker Desktop runs on it; you will not use Linux directly.
Open **PowerShell as administrator** (right-click PowerShell and choose **Run as administrator**) and run:

```powershell
wsl --install
```

Restart the laptop when it asks. If a Linux window opens after the restart and asks for a user name and password, choose a short name and a password you will remember; the course does not use it, so you can close the window.

Check it in PowerShell:

```powershell
wsl --version
wsl -l -v
```

`wsl --version` shows `WSL version: 2.` and more numbers. If it is not recognised or the version is old, run `wsl --update`. `wsl -l -v` lists at least one line with `2` under `VERSION`; task 9 asks you to paste it.

### Step 8: Docker Desktop

Docker Desktop runs containers on Windows. The course uses it for Mailpit (a pretend mail server) and to package TaskPilot and your capstone.
**Licence:** Docker Desktop is free under the Personal plan for individual learning. It is also free for small businesses with fewer than 250 employees and less than $10 million in yearly revenue.

1. Download **Docker Desktop for Windows (x86_64)** from https://docs.docker.com/desktop/setup/install/windows-install/.
2. Run the installer. Keep **Use WSL 2 instead of Hyper-V** ticked, then finish. Restart the laptop if it asks.
3. Start **Docker Desktop** from the Start menu.
4. Accept the Docker Subscription Service Agreement. Signing in is optional: you may skip it.
5. Wait until the bottom left of the Docker Desktop window says **Engine running**.

Check it in Git Bash:

```bash
docker run hello-world
docker compose version
```

- `docker run hello-world` prints `Hello from Docker!` and a few lines that explain what happened.
- `docker compose version` prints `Docker Compose version` and a number.

Docker Desktop must be running whenever you use Docker. You do not need it while you use a local model on an 8 GB laptop: quit it from the tray icon to free memory.

**On an 8 GB laptop**, limit Docker's memory so Windows, VS Code and your browser keep enough. Create the file `~/.wslconfig` (that is `C:\Users\<your name>\.wslconfig`) with these lines:

```ini
[wsl2]
memory=3GB
swap=2GB
```

Then run `wsl --shutdown` in PowerShell, wait 8 seconds and start Docker Desktop again. On 16 GB you can skip this.

### Step 9: Git Bash and Docker: the path rule

Git Bash changes any word that looks like a Linux path, such as `/data`, into a Windows path before Docker sees it.
When a `docker` command names a path inside a container, put `MSYS_NO_PATHCONV=1` in front of it:

```bash
MSYS_NO_PATHCONV=1 docker run --rm alpine ls /etc
```

- Put it in front of one command at a time. Never `export` it for the whole terminal.
- You do not need it for `docker compose up`, or for paths written inside a Compose file.

### Step 10: Ollama, for small models on your laptop

Ollama runs small open models on your own laptop, with no key, no limit and no internet once a model is downloaded. It needs about 4 GB of disk for the program, plus the model.

First check your free disk space in Git Bash:

```bash
df -h ~
```

Read the `Avail` column. **With 8 GB or more free**, install Ollama now. With less, skip this step: TicketSort installs it in week 3, after you have made space.

1. Run this in **PowerShell** (it needs no administrator rights):

   ```powershell
   irm https://ollama.com/install.ps1 | iex
   ```

   Or download and run `OllamaSetup.exe` from https://ollama.com/download/windows.
2. Ollama starts in the background (a llama icon in the tray) and listens on `http://localhost:11434`.
3. Close and reopen VS Code.

Check it in Git Bash:

```bash
ollama --version
curl http://localhost:11434
```

You see a version number, then `Ollama is running`.

**Which model fits your laptop.** Open Task Manager, select Performance, then Memory: the total is at the top right.

| Memory | `LOCAL_MODEL` | Download |
|---|---|---|
| **8 GB** | `qwen3.5:2b` | about 3 GB |
| **16 GB or more** | `qwen3.5:4b` | about 4 GB |

These names were checked on 24 November 2026; [`../models.md`](../models.md) has the current list and a second choice for each size. Pull your model when a task asks for it:

```bash
ollama pull qwen3.5:2b
ollama run qwen3.5:2b "Say hello in five words."
```

The first answer can take 10 to 30 seconds while the model loads. Type `/bye` if a chat prompt stays open. Models are stored in your home folder; if your C: drive is short of space, set `OLLAMA_MODELS` to a folder on another drive in your user environment variables, then quit and restart Ollama.

## Later: Node.js, before TaskPilot

You need Node.js only for two tools that run with `npx`: the MCP Inspector (TaskPilot) and promptfoo (DocAnswer, if you choose it). You write no JavaScript with it.

In PowerShell:

```powershell
winget install OpenJS.NodeJS.LTS
```

On 24 November 2026 this installs Node.js 26 LTS, which both tools support. Close and reopen VS Code, then check it in Git Bash:

```bash
node --version
npx --version
```

`node --version` prints `v26.` (or `v24.22.1` or newer, if you installed version 24 another way). The MCP Inspector needs 24.22.1+ or 26.12.1+.

## Final check

Run these in Git Bash, in VS Code's terminal.

| Command | You see |
|---|---|
| `uname -s` | a line starting with `MINGW64` |
| `git --version` | `git version 2.` and more |
| `uv run --python 3.12 python --version` | `Python 3.12.` and more |
| `ls ~/genai-ess-kit` | `README.md`, `VERSIONS.md`, `models.md` and the kit folders |
| `docker run hello-world` | `Hello from Docker!` |
| `ollama --version` | a version number (or "Ollama in week 3") |
| `node --version` | `v26.` or `v24.22.` or newer (before TaskPilot) |

## If something goes wrong

| What you see | What to do |
|---|---|
| `uv`, `ollama`, `node` or `npx` is not recognised | The terminal was open before the install. Close every terminal and VS Code, then open them again. |
| `wsl --install` or Docker Desktop says virtualisation is off | Turn on Intel VT-x or AMD SVM in the BIOS. Ask your mentor if you are unsure. |
| Docker Desktop says WSL needs an update | Run `wsl --update` in PowerShell, then start Docker Desktop again. |
| `error during connect` or `Is the docker daemon running?` | Start Docker Desktop and wait for **Engine running**, then open a new terminal. |
| An error shows a path such as `C:/Program Files/Git/...` | Add `MSYS_NO_PATHCONV=1` in front of the `docker` command (Step 9). |
| `UnicodeEncodeError` and `charmap` | Do Step 5, then reopen VS Code. |
| `$'\r': command not found` | The file has CRLF line endings. In VS Code, select `CRLF` in the status bar, choose `LF` and save. Then do Step 3. |
| `port is already allocated` for 1025 or 8025 | Another Mailpit is running. Run `docker ps` and stop it with `docker stop <name>`. |
| A local model answers very slowly or the laptop freezes | Use the smaller model for your memory, quit Docker Desktop and close browser tabs. |
| `curl http://localhost:11434` fails | Start Ollama from the Start menu and wait for the tray icon. |
