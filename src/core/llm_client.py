"""Simple LLM client supporting OpenAI, Gemini, and Ollama."""

import os
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

from openai import OpenAI
from google import genai
from ollama import Client as OllamaClient
import time
from .cost_tracker import calculate_cost

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama

# Load .env from project root (works regardless of cwd)
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# Read configuration from .env file
PROVIDER = os.getenv("PROVIDER", "openai").lower()
MODEL = os.getenv("MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
TIMEOUT = 60

Message = Dict[str, str]

def chat(messages: List[Message]) -> Dict:
    """Send messages to LLM and return response with metadata."""
    if not messages:
        raise ValueError("Messages list cannot be empty")

    start_time = time.time()

    if PROVIDER == "openai":
        response = _call_openai(messages)
    elif PROVIDER == "google":
        response = _call_gemini(messages)
    elif PROVIDER == "ollama":
        response = _call_ollama(messages)
    else:
        raise NotImplementedError(f"Provider {PROVIDER} not implemented")

    duration_ms = int((time.time() - start_time) * 1000)

    # Estimate tokens (rough: 1 token ≈ 4 characters)
    prompt_text = " ".join([m["content"] for m in messages])
    prompt_tokens = len(prompt_text) // 4
    response_tokens = len(response) // 4
    cost = calculate_cost(PROVIDER, MODEL, prompt_tokens, response_tokens)

    return {
        "response": response,
        "metadata": {
            "provider": PROVIDER,
            "model": MODEL,
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens,
            "total_tokens": prompt_tokens + response_tokens,
            "duration_ms": duration_ms,
            "cost_usd": cost
        }
    }

def _call_openai(messages: List[Message]) -> str:
    """Call OpenAI API."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set in .env")

    client = OpenAI(api_key=OPENAI_API_KEY, timeout=TIMEOUT)
    response = client.chat.completions.create(
        model=MODEL, messages=messages, temperature=0
    )
    return response.choices[0].message.content

def _call_gemini(messages: List[Message]) -> str:
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set in the .env file")

    client = genai.Client(api_key=GOOGLE_API_KEY)

    system_text = ""
    contents = []
    for msg in messages:
        if msg["role"] == "system":
            system_text = msg["content"]
        elif msg["role"] == "user":
            contents.append({"role": "user", "parts": [{"text": msg["content"]}]})
        elif msg["role"] == "assistant":
            contents.append({"role": "model", "parts": [{"text": msg["content"]}]})

    config = genai.types.GenerateContentConfig(
        temperature=0,
        system_instruction=system_text if system_text else None,
    )
    response = client.models.generate_content(
        model=MODEL, contents=contents, config=config
    )
    return response.text

def _call_ollama(messages: List[Message]) -> str:
    """Call local Ollama API."""
    client = OllamaClient(host=OLLAMA_HOST)
    response = client.chat(model=MODEL, messages=messages)
    if not response.message or not response.message.content:
        raise RuntimeError("Ollama returned empty response. Is Ollama running?")
    return response.message.content

# ========== LANGCHAIN SUPPORT (ADVANCED COURSE) ==========

def get_langchain_llm():
    """
    Returns Langchain LLM wrapper based on .env PROVIDER.
    Used by agents_langchain/ (Langchain-based agents).
    """
    if PROVIDER == "openai":
        return ChatOpenAI(
            model=MODEL,
            api_key=OPENAI_API_KEY
        )

    elif PROVIDER == "google":
        return ChatGoogleGenerativeAI(
            model=MODEL,
            google_api_key=GOOGLE_API_KEY
        )

    elif PROVIDER == "ollama":
        return Ollama(
            model=MODEL,
            base_url=OLLAMA_HOST
        )

    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")