# Project Explanation

## Purpose

This project is a minimal Gradio chatbot that uses the OpenAI Agents SDK with an OpenAI-compatible server hosted at `https://skynet.av.it.pt/`.

The app is intended as a simple local test client. It launches a Gradio web UI, sends chat messages to the configured model, and keeps the conversation context across turns.

## Project Management

The project is fully managed with `uv`.

Python is pinned to 3.12 through:

- `.python-version`
- `pyproject.toml`
- `uv.lock`

The Python version range in `pyproject.toml` is:

```toml
requires-python = ">=3.12,<3.13"
```

Dependencies are declared directly in `pyproject.toml`:

```toml
dependencies = [
    "gradio",
    "openai",
    "openai-agents",
    "python-dotenv",
]
```

No `requirements.txt`, `pip`, `conda`, `poetry`, or `pipenv` setup is used.

## Configuration

Runtime configuration is loaded from `.env` using `python-dotenv`.

The relevant environment variables are:

```text
OPENAI_BASE_URL=https://skynet.av.it.pt/openai
OPENAI_API_KEY=your_api_key_here
OLLAMA_MODEL=llama70b
```

The API key is not hard-coded in `main.py` and is not shown in the Gradio UI.

The original Ollama-compatible endpoint was:

```text
https://skynet.av.it.pt/ollama/v1
```

During testing, that endpoint accepted requests but did not expose `llama70b` through Chat Completions. The working OpenAI-compatible Chat Completions endpoint was:

```text
https://skynet.av.it.pt/openai
```

## Implementation

The application entry point is `main.py`.

It performs these steps:

1. Loads `.env` from the same folder as `main.py`.
2. Disables OpenAI Agents SDK tracing with `set_tracing_disabled(True)`.
3. Reads and validates:
   - `OPENAI_BASE_URL`
   - `OPENAI_API_KEY`
   - `OLLAMA_MODEL`
4. Creates an `AsyncOpenAI` client using the configured base URL and API key.
5. Creates an `Agent` using `OpenAIChatCompletionsModel`.
6. Uses `Runner.run` inside an async Gradio callback.
7. Reconstructs conversation history from Gradio and sends it with the latest user message.
8. Returns the model response to the chat UI.

The model setup is:

```python
client = AsyncOpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY,
    timeout=120,
)

agent = Agent(
    name="Ollama Chatbot",
    instructions="You are a helpful assistant.",
    model=OpenAIChatCompletionsModel(
        model=OLLAMA_MODEL,
        openai_client=client,
    ),
)
```

The app uses Chat Completions instead of the Responses API because the organization server is OpenAI-compatible but may not fully support the newer Responses API.

## Running The Project

From the project root:

```powershell
uv sync
uv run python main.py
```

If Python 3.12 is not installed yet:

```powershell
uv python install 3.12
uv python pin 3.12
uv sync
uv run python main.py
```

Gradio will print a local URL in the terminal, usually:

```text
http://127.0.0.1:7860
```

Open that URL in a browser to use the chatbot.

## Expected Structure

```text
.
├── .env
├── .env.example
├── .gitignore
├── .python-version
├── README.md
├── documents
│   └── project_explanation.md
├── main.py
├── pyproject.toml
└── uv.lock
```
