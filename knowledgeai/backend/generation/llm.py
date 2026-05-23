"""
llm.py — Multi-provider LLM interface: OpenAI, Gemini, Anthropic.
Provider is determined by model name prefix:
  gpt-*      → OpenAI
  gemini-*   → Google Gemini
  claude-*   → Anthropic
"""
import logging
from typing import List, Dict, AsyncGenerator
from openai import AsyncOpenAI
from backend.config import OPENAI_API_KEY, GEMINI_API_KEY, ANTHROPIC_API_KEY, LLM_MODEL

logger = logging.getLogger(__name__)

_openai_client = None
_gemini_client = None
_anthropic_client = None


def _get_openai():
    global _openai_client
    if _openai_client is None:
        _openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    return _openai_client


def _get_gemini():
    global _gemini_client
    if _gemini_client is None:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        _gemini_client = genai
    return _gemini_client


def _get_anthropic():
    global _anthropic_client
    if _anthropic_client is None:
        import anthropic
        _anthropic_client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    return _anthropic_client


def _detect_provider(model: str) -> str:
    """Detect provider from model name prefix."""
    if model.startswith("gemini-"):
        return "gemini"
    elif model.startswith("claude-"):
        return "anthropic"
    else:
        return "openai"


def _messages_to_gemini(messages: List[Dict]) -> tuple:
    """Convert OpenAI-style messages to Gemini format."""
    system_prompt = ""
    contents = []
    for m in messages:
        if m["role"] == "system":
            system_prompt = m["content"]
        elif m["role"] == "user":
            contents.append({"role": "user", "parts": [m["content"]]})
        elif m["role"] == "assistant":
            contents.append({"role": "model", "parts": [m["content"]]})
    return system_prompt, contents


def _messages_to_anthropic(messages: List[Dict]) -> tuple:
    """Convert OpenAI-style messages to Anthropic format."""
    system_prompt = ""
    anthropic_messages = []
    for m in messages:
        if m["role"] == "system":
            system_prompt = m["content"]
        else:
            anthropic_messages.append({"role": m["role"], "content": m["content"]})
    return system_prompt, anthropic_messages


# ── Non-streaming generate ────────────────────────────────────────────────────

async def generate(messages: List[Dict], temperature: float = 0.2,
                   model: str = None) -> str:
    """Non-streaming: return full answer text."""
    model = model or LLM_MODEL
    provider = _detect_provider(model)

    try:
        if provider == "openai":
            client = _get_openai()
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=1024,
            )
            return response.choices[0].message.content or ""

        elif provider == "gemini":
            import asyncio
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            system_prompt, contents = _messages_to_gemini(messages)
            gemini_model = genai.GenerativeModel(
                model_name=model,
                system_instruction=system_prompt or None,
            )
            response = await asyncio.to_thread(
                gemini_model.generate_content,
                contents,
                generation_config={"temperature": temperature, "max_output_tokens": 1024},
            )
            return response.text or ""

        elif provider == "anthropic":
            client = _get_anthropic()
            system_prompt, anthropic_messages = _messages_to_anthropic(messages)
            response = await client.messages.create(
                model=model,
                max_tokens=1024,
                system=system_prompt,
                messages=anthropic_messages,
                temperature=temperature,
            )
            return response.content[0].text or ""

    except Exception as e:
        logger.error("LLM generate error (%s): %s", provider, e)
        raise


# ── Streaming generate ────────────────────────────────────────────────────────

async def stream_generate(messages: List[Dict], temperature: float = 0.2,
                          model: str = None) -> AsyncGenerator[str, None]:
    """Streaming: yields token chunks as they arrive."""
    model = model or LLM_MODEL
    provider = _detect_provider(model)

    try:
        if provider == "openai":
            client = _get_openai()
            stream = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=1024,
                stream=True,
            )
            async for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta

        elif provider == "gemini":
            import asyncio
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            system_prompt, contents = _messages_to_gemini(messages)
            gemini_model = genai.GenerativeModel(
                model_name=model,
                system_instruction=system_prompt or None,
            )
            # Gemini streaming runs in thread since SDK is sync
            response = await asyncio.to_thread(
                gemini_model.generate_content,
                contents,
                generation_config={"temperature": temperature, "max_output_tokens": 1024},
                stream=True,
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text

        elif provider == "anthropic":
            client = _get_anthropic()
            system_prompt, anthropic_messages = _messages_to_anthropic(messages)
            async with client.messages.stream(
                model=model,
                max_tokens=1024,
                system=system_prompt,
                messages=anthropic_messages,
                temperature=temperature,
            ) as stream:
                async for text in stream.text_stream:
                    yield text

    except Exception as e:
        logger.error("LLM stream error (%s): %s", provider, e)
        yield f"\n\n[Error generating response: {e}]"
