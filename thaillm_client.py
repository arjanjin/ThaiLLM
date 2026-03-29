import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://thaillm.or.th/api/pathumma/v1/chat/completions"
API_KEY = os.getenv("THAILLM_API_KEY", "")
CONSUMER_ID = os.getenv("THAILLM_CONSUMER_ID", "")


def _headers():
    return {
        "Content-Type": "application/json",
        "apikey": API_KEY,
        "consumerid": CONSUMER_ID,
    }


def chat(messages, model="/model", max_tokens=2048, temperature=0.3):
    """Send a chat completion request to the ThaiLLM Pathumma API."""
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    response = requests.post(API_URL, headers=_headers(), json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def chat_stream(messages, model="/model", max_tokens=2048, temperature=0.3):
    """Stream a chat completion request, yielding raw data strings from SSE."""
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": True,
    }
    response = requests.post(API_URL, headers=_headers(), json=payload, timeout=120, stream=True)
    response.raise_for_status()
    for line in response.iter_lines():
        if line:
            decoded = line.decode("utf-8")
            if decoded.startswith("data: "):
                yield decoded[6:]


def chat_simple(user_message, **kwargs):
    """Send a single user message and return the assistant's reply text."""
    messages = [{"role": "user", "content": user_message}]
    data = chat(messages, **kwargs)
    return data["choices"][0]["message"]["content"]
