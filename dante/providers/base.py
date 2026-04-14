"""Clase base abstracta para todos los proveedores de IA."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
class BaseProvider(ABC):
    """
    Interfaz común para Claude, OpenAI y Gemini.
    Todos los proveedores reciben la misma estructura de mensajes y herramientas
    y devuelven un formato normalizado.
    """
    def __init__(self, model: str) -> None:
        self.model = model
    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        system: str,
        tools: list[dict] | None = None,
    ) -> "ProviderResponse":
        """
        Envía mensajes al modelo y devuelve una ProviderResponse.
        Args:
            messages: Historial de mensajes [{role, content}, ...]
            system:   System prompt (soul + perfil)
            tools:    Lista de tool schemas en formato interno
        """
        ...
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model!r})"
class ToolCall:
    """Representa una llamada a herramienta solicitada por el modelo."""
    def __init__(self, id: str, name: str, arguments: dict[str, Any]) -> None:
        self.id = id
        self.name = name
        self.arguments = arguments
    def __repr__(self) -> str:
        return f"ToolCall(name={self.name!r}, args={self.arguments})"
class ProviderResponse:
    """Respuesta normalizada de cualquier proveedor."""
    def __init__(
        self,
        text: str | None,
        tool_calls: list[ToolCall],
        raw: Any = None,
    ) -> None:
        self.text = text
        self.tool_calls = tool_calls
        self.raw = raw
    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0
    def __repr__(self) -> str:
        return (
            f"ProviderResponse(text={self.text[:40]!r}..., "
            f"tool_calls={len(self.tool_calls)})"
        )
