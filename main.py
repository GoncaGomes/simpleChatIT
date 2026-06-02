import os
from pathlib import Path

import gradio as gr
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv(dotenv_path=Path(__file__).with_name(".env"))
set_tracing_disabled(True)

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

missing = [
    name
    for name, value in {
        "OPENAI_BASE_URL": OPENAI_BASE_URL,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "OLLAMA_MODEL": OLLAMA_MODEL,
    }.items()
    if not value
]

if missing:
    raise RuntimeError(f"Missing required environment variable(s): {', '.join(missing)}")

if OPENAI_API_KEY == "PUT_YOUR_API_KEY_HERE":
    raise RuntimeError("Set OPENAI_API_KEY in .env before running the chatbot.")

client = AsyncOpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY, timeout=120)

agent = Agent(
    name="Ollama Chatbot",
    instructions="You are a helpful assistant.",
    model=OpenAIChatCompletionsModel(
        model=OLLAMA_MODEL,
        openai_client=client,
    ),
)


async def chat(message: str, history: list) -> str:
    conversation = []
    for item in history:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content")
            if role in {"user", "assistant"} and content:
                conversation.append({"role": role, "content": content})
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user_message, assistant_message = item
            if user_message:
                conversation.append({"role": "user", "content": user_message})
            if assistant_message:
                conversation.append({"role": "assistant", "content": assistant_message})

    conversation.append({"role": "user", "content": message})

    try:
        result = await Runner.run(agent, conversation)
    except Exception as exc:
        return f"Model request failed: {exc}"

    return result.final_output


def main() -> None:
    demo = gr.ChatInterface(fn=chat, title="Ollama Agents SDK Chatbot")
    demo.launch()


if __name__ == "__main__":
    main()
