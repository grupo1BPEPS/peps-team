"""
Registro central de herramientas.
Lee la configuración del perfil activo y expone solo las herramientas habilitadas.
"""
from __future__ import annotations
from typing import Any, Callable
from . import shell, files, web_search, network
class ToolRegistry:
    """
    Construye el conjunto de herramientas disponibles para una sesión
    a partir de la configuración del perfil activo.
    """
    def __init__(self, tools_config: dict, shell_timeout: int = 60) -> None:
        self._tools_config = tools_config
        self._shell_timeout = shell_timeout
        self._handlers: dict[str, Callable[[dict], str]] = {}
        self._schemas: list[dict] = []
        self._register_enabled_tools()
    def _register_enabled_tools(self) -> None:
        cfg = self._tools_config
        if cfg.get("shell", {}).get("enabled", False):
            self._schemas.append(shell.SCHEMA)
            timeout = self._shell_timeout
            self._handlers["execute_shell"] = lambda args: shell.run_tool(args, timeout=timeout)
        if cfg.get("files", {}).get("enabled", False):
            self._schemas.extend(files.SCHEMAS)
            for schema in files.SCHEMAS:
                name = schema["name"]
                self._handlers[name] = lambda args, n=name: files.run_tool(n, args)
        if cfg.get("web_search", {}).get("enabled", False):
            self._schemas.append(web_search.SCHEMA)
            self._handlers["web_search"] = web_search.run_tool
        network_cfg = cfg.get("network", {})
        if network_cfg.get("enabled", False):
            self._schemas.append(network.SCHEMA)
            allowed = network_cfg.get("allowed_tools")
            self._handlers["network_tool"] = lambda args, a=allowed: network.run_tool(args, allowed_tools=a)
    @property
    def schemas(self) -> list[dict]:
        """Schemas en formato interno que se pasan a los proveedores."""
        return self._schemas
    @property
    def tools_config(self) -> dict:
        return self._tools_config
    def execute(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """Ejecuta una herramienta por nombre y devuelve el resultado como string."""
        handler = self._handlers.get(tool_name)
        if handler is None:
            return f"Herramienta desconocida o desactivada en este perfil: '{tool_name}'"
        try:
            return handler(arguments)
        except Exception as exc:
            return f"Error ejecutando '{tool_name}': {exc}"
    def has_tools(self) -> bool:
        return len(self._schemas) > 0
