from __future__ import annotations

import json
from typing import Any

from openai import OpenAI


def get_client(api_key: str, base_url: str | None = None) -> OpenAI:
    if not api_key:
        raise ValueError("API key is required.")
    kwargs = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def call_llm_json(
    *,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    base_url: str | None = None,
    temperature: float = 0.1,
) -> dict[str, Any]:
    """
    Calls an OpenAI-compatible chat completion endpoint and returns parsed JSON.

    Works with OpenAI and many OpenAI-compatible providers if the provider supports:
    - /v1/chat/completions
    - JSON-mode response_format
    """
    client = get_client(api_key=api_key, base_url=base_url)

    try:
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content or "{}"
    except Exception as exc:
        raise RuntimeError(f"LLM request failed: {exc}") from exc

    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM did not return valid JSON. Raw output:\n{content}") from exc
