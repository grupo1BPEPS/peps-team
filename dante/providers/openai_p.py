"""Proveedor OpenAI (GPT)."""
from __future__ import annotations
import json
import os
from typing import Any
from openai import OpenAI
from .base import BaseProvider, ProviderResponse, ToolCall
class OpenAIProvider(BaseProvider):
    def __init__(self, model: str) -> None:
        super().__init__(model)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "OPENAI_API_KEY no encontrada. "
                "Añádela en tu .env o como variable de entorno."
            )
        self._client = OpenAI(api_key=api_key)
    def chat(
        self,
        messages: list[dict],
        system: str,
        tools: list[dict] | None = None,
    ) -> ProviderResponse:
        full_messages = [{"role": "system", "content": system}] + messages
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": full_messages,
        }
        if tools:
            kwargs["tools"] = [self._to_openai_tool(t) for t in tools]
            kwargs["tool_choice"] = "auto"
        response = self._client.chat.completions.create(**kwargs)
        message = response.choices[0].message
        text = message.content
        tool_calls: list[ToolCall] = []
        if message.tool_calls:
            for tc in message.tool_calls:
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    args = {"raw": tc.function.arguments}
                tool_calls.append(
                    ToolCall(id=tc.id, name=tc.function.name, arguments=args)
                )
        return ProviderResponse(text=text, tool_calls=tool_calls, raw=response)
    @staticmethod
    def _to_openai_tool(tool: dict) -> dict:
        return {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"],
            },
        }
    def build_tool_result_message(self, tool_call_id: str, result: str) -> dict:
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result,
        }
    def build_assistant_tool_call_message(self, response_raw: Any) -> dict:
        message = response_raw.choices[0].message
        return {
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in (message.tool_calls or [])
            ],
        }
