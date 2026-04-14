"""Proveedor Google Gemini."""
from __future__ import annotations
import os
from typing import Any
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool as GeminiTool
from .base import BaseProvider, ProviderResponse, ToolCall
class GeminiProvider(BaseProvider):
    def __init__(self, model: str) -> None:
        super().__init__(model)
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GOOGLE_API_KEY no encontrada. "
                "Añádela en tu .env o como variable de entorno."
            )
        genai.configure(api_key=api_key)
    def chat(
        self,
        messages: list[dict],
        system: str,
        tools: list[dict] | None = None,
    ) -> ProviderResponse:
        model_kwargs: dict[str, Any] = {
            "model_name": self.model,
            "system_instruction": system,
        }
        if tools:
            model_kwargs["tools"] = [self._to_gemini_tools(tools)]
        model = genai.GenerativeModel(**model_kwargs)
        # Convierte historial al formato de Gemini
        history = self._convert_messages(messages[:-1])
        last_message = messages[-1]["content"] if messages else ""
        chat = model.start_chat(history=history)
        response = chat.send_message(last_message)
        text: str | None = None
        tool_calls: list[ToolCall] = []
        candidate = response.candidates[0]
        for part in candidate.content.parts:
            if hasattr(part, "text") and part.text:
                text = part.text
            elif hasattr(part, "function_call") and part.function_call:
                fc = part.function_call
                tool_calls.append(
                    ToolCall(
                        id=fc.name,
                        name=fc.name,
                        arguments=dict(fc.args),
                    )
                )
        return ProviderResponse(text=text, tool_calls=tool_calls, raw=response)
    @staticmethod
    def _to_gemini_tools(tools: list[dict]) -> GeminiTool:
        declarations = []
        for tool in tools:
            declarations.append(
                FunctionDeclaration(
                    name=tool["name"],
                    description=tool["description"],
                    parameters=tool["parameters"],
                )
            )
        return GeminiTool(function_declarations=declarations)
    @staticmethod
    def _convert_messages(messages: list[dict]) -> list[dict]:
        """Convierte mensajes internos al formato history de Gemini."""
        history = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            content = msg.get("content", "")
            if isinstance(content, str) and content:
                history.append({"role": role, "parts": [content]})
        return history
    def build_tool_result_message(self, tool_call_id: str, result: str) -> dict:
        # Gemini usa function_response como parte de un mensaje user
        return {
            "role": "user",
            "content": f"[Tool result for {tool_call_id}]: {result}",
        }
    def build_assistant_tool_call_message(self, response_raw: Any) -> dict:
        text = ""
        try:
            text = response_raw.text
        except Exception:
            pass
        return {"role": "assistant", "content": text or ""}
