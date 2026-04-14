"""Proveedor Anthropic (Claude)."""
from __future__ import annotations
import os
from typing import Any
import anthropic
from .base import BaseProvider, ProviderResponse, ToolCall
class AnthropicProvider(BaseProvider):
    def __init__(self, model: str) -> None:
        super().__init__(model)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY no encontrada. "
                "Añádela en tu .env o como variable de entorno."
            )
        self._client = anthropic.Anthropic(api_key=api_key)
    def chat(
        self,
        messages: list[dict],
        system: str,
        tools: list[dict] | None = None,
    ) -> ProviderResponse:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": 8096,
            "system": system,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = [self._to_anthropic_tool(t) for t in tools]
        response = self._client.messages.create(**kwargs)
        text: str | None = None
        tool_calls: list[ToolCall] = []
        for block in response.content:
            if block.type == "text":
                text = block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(id=block.id, name=block.name, arguments=block.input)
                )
        return ProviderResponse(text=text, tool_calls=tool_calls, raw=response)
    @staticmethod
    def _to_anthropic_tool(tool: dict) -> dict:
        """Convierte el schema interno al formato de Anthropic."""
        return {
            "name": tool["name"],
            "description": tool["description"],
            "input_schema": tool["parameters"],
        }
    def build_tool_result_message(
        self, tool_call_id: str, result: str
    ) -> dict:
        """Construye el mensaje de resultado de herramienta para Anthropic."""
        return {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_call_id,
                    "content": result,
                }
            ],
        }
    def build_assistant_tool_call_message(self, response_raw: Any) -> dict:
        """Construye el mensaje del assistant con tool_use blocks para el historial."""
        return {"role": "assistant", "content": response_raw.content}
