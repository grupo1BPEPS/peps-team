"""
Herramienta de búsqueda web — usa DuckDuckGo (sin API key).
"""
from __future__ import annotations
from typing import Any
from ..ui import terminal as ui
def search(query: str, max_results: int = 5) -> str:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        return "Error: instala 'duckduckgo-search' para usar búsqueda web."
    ui.print_tool_call("web_search", {"query": query})
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            result_text = "No se encontraron resultados."
        else:
            lines = []
            for i, r in enumerate(results, 1):
                lines.append(f"**{i}. {r.get('title', 'Sin título')}**")
                lines.append(f"   {r.get('href', '')}")
                lines.append(f"   {r.get('body', '')}")
                lines.append("")
            result_text = "\n".join(lines)
        ui.print_tool_output(result_text)
        return result_text
    except Exception as exc:
        msg = f"Error en búsqueda web: {exc}"
        ui.print_error(msg)
        return msg
SCHEMA = {
    "name": "web_search",
    "description": (
        "Busca información actualizada en internet usando DuckDuckGo. "
        "Útil para CVEs, documentación, noticias técnicas, precios, etc."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Consulta de búsqueda.",
            },
            "max_results": {
                "type": "integer",
                "description": "Número máximo de resultados (por defecto 5).",
            },
        },
        "required": ["query"],
    },
}
def run_tool(arguments: dict[str, Any]) -> str:
    return search(
        query=arguments["query"],
        max_results=arguments.get("max_results", 5),
    )
