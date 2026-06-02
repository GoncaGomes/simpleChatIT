# OpenAI Agents SDK Ollama Chatbot

A minimal Gradio chatbot using the OpenAI Agents SDK with an OpenAI-compatible Ollama server.

## Configuration

Edit `.env` and replace `PUT_YOUR_API_KEY_HERE` with the real API key.

The working OpenAI-compatible Chat Completions endpoint is:

```text
https://skynet.av.it.pt/openai
```

The `https://skynet.av.it.pt/ollama/v1` endpoint may list no models and return `Model 'llama70b' was not found`.

## Setup

```powershell
uv python install 3.12
uv python pin 3.12
uv sync
uv run python main.py
```
