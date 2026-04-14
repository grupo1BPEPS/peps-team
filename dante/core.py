"""
Núcleo del agente — bucle ReAct: Razona → Actúa → Observa.
Flujo por turno:
  1. Construye messages = historial + nuevo mensaje del usuario
  2. Llama al proveedor con tools activos
  3. Si la respuesta contiene tool_calls → ejecuta → añade resultados → repite
  4. Cuando la respuesta es solo texto → devuelve al session.py para mostrar al usuario
"""
from __future__ import annotations
from typing import Any
from .providers.base import BaseProvider, ProviderResponse
from .tools.registry import ToolRegistry
from .ui import terminal as ui
# Límite de iteraciones del bucle ReAct por turno (evita bucles infinitos)
_MAX_REACT_ITERATIONS = 10
class AgentCore:
    def __init__(
        self,
        provider: BaseProvider,
        registry: ToolRegistry,
        system_prompt: str,
    ) -> None:
        self._provider = provider
        self._registry = registry
        self._system = system_prompt
        self._history: list[dict] = []
    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------
    def send(self, user_message: str) -> str:
        """
        Procesa un mensaje del usuario y devuelve la respuesta final de texto.
        Ejecuta internamente el bucle ReAct completo.
        """
        self._history.append({"role": "user", "content": user_message})
        response_text = self._react_loop()
        return response_text
    def clear_history(self) -> None:
        self._history.clear()
    @property
    def history(self) -> list[dict]:
        return list(self._history)
    def switch_provider(self, provider: BaseProvider) -> None:
        self._provider = provider
    def switch_system(self, system_prompt: str) -> None:
        self._system = system_prompt
    # ------------------------------------------------------------------
    # Bucle ReAct interno
    # ------------------------------------------------------------------
    def _react_loop(self) -> str:
        tools = self._registry.schemas if self._registry.has_tools() else None
        for iteration in range(_MAX_REACT_ITERATIONS):
            response: ProviderResponse = self._provider.chat(
                messages=self._history,
                system=self._system,
                tools=tools,
            )
            if not response.has_tool_calls:
                # Respuesta final de texto
                text = response.text or ""
                self._history.append({"role": "assistant", "content": text})
                return text
            # El modelo quiere ejecutar herramientas
            # 1. Añadir el mensaje del assistant con los tool_calls al historial
            assistant_msg = self._build_assistant_msg(response)
            self._history.append(assistant_msg)
            # 2. Ejecutar cada herramienta y recopilar resultados
            for tc in response.tool_calls:
                result = self._registry.execute(tc.name, tc.arguments)
                tool_result_msg = self._build_tool_result_msg(tc.id, result)
                self._history.append(tool_result_msg)
        # Si se agotaron las iteraciones, pide al modelo un resumen
        ui.print_warning(
            f"Se alcanzó el límite de {_MAX_REACT_ITERATIONS} iteraciones ReAct. "
            "Solicitando respuesta final..."
        )
        final = self._provider.chat(
            messages=self._history + [
                {"role": "user", "content": "Resume lo que has hecho hasta ahora."}
            ],
            system=self._system,
            tools=None,  # sin tools para forzar respuesta de texto
        )
        text = final.text or "(sin respuesta)"
        self._history.append({"role": "assistant", "content": text})
        return text
    # ------------------------------------------------------------------
    # Construcción de mensajes según proveedor
    # ------------------------------------------------------------------
    def _build_assistant_msg(self, response: ProviderResponse) -> dict:
        """Delega al proveedor la construcción del mensaje assistant con tool_calls."""
        p = self._provider
        if hasattr(p, "build_assistant_tool_call_message"):
            return p.build_assistant_tool_call_message(response.raw)
        # Fallback genérico
        return {"role": "assistant", "content": response.text or ""}
    def _build_tool_result_msg(self, tool_call_id: str, result: str) -> dict:
        """Delega al proveedor la construcción del mensaje de resultado de herramienta."""
        p = self._provider
        if hasattr(p, "build_tool_result_message"):
            return p.build_tool_result_message(tool_call_id, result)
        # Fallback genérico
        return {
            "role": "user",
            "content": f"[Tool result for {tool_call_id}]: {result}",
        }
