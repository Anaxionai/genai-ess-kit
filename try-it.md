# Try it: free sites where you practise in the browser

Learn cards ask you to **try** each new idea for 15 to 20 minutes. These free sites let you do that with nothing to install, except the MCP Inspector, which runs from your laptop with one command.
Every address was checked on 24 November 2026 and opened with status 200.
A site that needs an account says so in its row.

**Privacy rule for every AI site below:** type only made-up text or the kit's synthetic data. Never paste personal data, real messages, your resume or an API key.

## Language models and prompts

| Site | Address | Use it for |
|---|---|---|
| Google AI Studio | https://aistudio.google.com/ | Chat with the Gemini models from [`models.md`](models.md), change the system instructions, the temperature and the output format, and see the token count of your prompt. Select **Get code** to see the same call in Python. Needs your Google account; free. |
| Tokenizer Playground (Hugging Face) | https://huggingface.co/spaces/Xenova/the-tokenizer-playground | Type a sentence and see how it splits into tokens, coloured one by one. Try a long word, a number, an emoji and a sentence in another language. |
| Tiktokenizer | https://tiktokenizer.vercel.app/ | The same idea with other models' tokenizers. Each model family splits text differently, so Gemini's counts (in AI Studio or `hello/ask.py`) will not match exactly. |
| Gandalf (Lakera) | https://gandalf.lakera.ai/ | A game: trick a chatbot into telling you a password, level by level. The best way to feel why prompt injection is hard to stop. |
| TensorFlow Embedding Projector | https://projector.tensorflow.org/ | Explore word embeddings in 3D: search a word and see its nearest neighbours by meaning. Use a laptop; it loads 10,000 points. |

## Python

| Site | Address | Use it for |
|---|---|---|
| Python Tutor | https://pythontutor.com/visualize.html | Run Python one line at a time and watch the variables, lists, dictionaries and function calls change. Paste code that confuses you. |
| futurecoder | https://futurecoder.io/ | A free Python course for beginners, with exercises and hints, in the browser. |

## JSON and schemas

| Site | Address | Use it for |
|---|---|---|
| JSONLint | https://jsonlint.com/ | Paste a model's answer and see at once whether it is valid JSON, and where it breaks. |
| JSON Schema Validator | https://www.jsonschemavalidator.net/ | Paste a JSON Schema (for example from `YourModel.model_json_schema()`) on the left and an answer on the right, and see every rule it breaks. |
| jq play | https://play.jqlang.org/ | Pick fields out of JSON with `jq` filters, such as `.[] \| .category`. |

## APIs and the web

| Site | Address | Use it for |
|---|---|---|
| httpbin | https://httpbin.org/ | Send requests and see exactly what a server received. `https://httpbin.org/status/429` always answers `429`, so you can test your retry code without using your quota. |
| Hoppscotch | https://hoppscotch.io/ | Send GET and POST requests from the browser and read the status code, headers and body. |
| MDN Playground | https://developer.mozilla.org/en-US/play | Try HTML, CSS and JavaScript together, with a live preview and a console: practice for DocAnswer's question page. |

## Diagrams, Git and security

| Site | Address | Use it for |
|---|---|---|
| Mermaid Live Editor | https://mermaid.live/ | Draw diagrams from text: `flowchart` for your pipeline or agent loop, `sequenceDiagram` for a tool call. If it renders here, it renders on GitHub too. |
| Learn Git Branching | https://learngitbranching.js.org/ | Type real Git commands and watch commits and branches move in a picture. Do the "Main" levels first. |
| OWASP Top 10 for LLM Applications | https://genai.owasp.org/llm-top-10/ | Not interactive: the list of the ten biggest risks in LLM apps, starting with prompt injection. Read the entry before you write attacks. |

## On your laptop: the MCP Inspector

| Tool | How to start it | Use it for |
|---|---|---|
| MCP Inspector | `npx @modelcontextprotocol/inspector@2.16.0 uv run server.py` in the folder of your MCP server | A web page that connects to your MCP server, lists its tools and lets you call them by hand, with the JSON messages on show. Needs Node.js ([`setup/windows.md`](setup/windows.md), "Later: Node.js"). Full steps in [`mcp/README.md`](mcp/README.md). |
