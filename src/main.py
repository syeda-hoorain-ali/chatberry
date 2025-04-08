import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional, Dict
from chainlit.types import ThreadDict


load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
thread_id = None

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please provide a valid API key in the environment variables.")


genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")


def format_history(history: list[dict[str, str]]):
    formatted_history = []

    for msg in history:
        role = "user" if msg["role"] == "user" else "model"

        if msg["content"].strip():
            formatted_history.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

    return formatted_history


async def process_message(prompt: str, history: list[dict[str, str]]):
        
    actions = [
        cl.Action(name="regenerate", payload={"message": prompt}, icon="rotate-ccw", tooltip="Regenerate")
    ]

    history.append({
        "role": "user",
        "content": prompt
    })

    formatted_history = format_history(history)
    msg = cl.Message(content="", actions=actions)

    response = model.generate_content(formatted_history, stream=True)
    for chunk in response:
        token = chunk.text if hasattr(chunk, "text") else ''
        if token.strip():  # Check if token is not empty
            await msg.stream_token(token)

    history.append({"role": "assistant", "content": msg.content})
    cl.user_session.set("history", history)
    msg.actions = actions
    await msg.update()







# --------------------------- Chainlit app ---------------------------


@cl.action_callback("regenerate")
async def on_action(action: cl.Action):

    history = cl.user_session.get("history")
    if not history:
        return
    
    prompt = f"regenerate: \n {action.payload['message']}"
    await process_message(prompt, history)


@cl.oauth_callback
def handle_oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
        
    return default_user


@cl.on_chat_resume
async def handle_chat_resume(thread: ThreadDict):
    pass


@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! How can I help you today?").send()


@cl.on_message
async def handle_message(message: cl.Message):
        prompt = message.content
        history = cl.user_session.get("history")
        await process_message(prompt, history)
    