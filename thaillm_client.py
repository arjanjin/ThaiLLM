import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://thaillm.or.th/api/pathumma/v1/chat/completions"
API_KEY = os.getenv("THAILLM_API_KEY", "")


def chat(messages, model="/model", max_tokens=2048, temperature=0.3):
    """Send a chat completion request to the ThaiLLM Pathumma API."""
    headers = {
        "Content-Type": "application/json",
        "apikey": API_KEY,
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def chat_simple(user_message, **kwargs):
    """Send a single user message and return the assistant's reply text."""
    messages = [{"role": "user", "content": user_message}]
    data = chat(messages, **kwargs)
    return data["choices"][0]["message"]["content"]
