"""
Herramienta de ficheros — leer, escribir y listar ficheros del sistema.
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any
from ..ui import terminal as ui
# Extensiones binarias que no tiene sentido leer como texto
_BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
    ".pdf", ".zip", ".tar", ".gz", ".bz2", ".xz", ".rar",
    ".exe", ".bin", ".so", ".dylib", ".dll", ".whl", ".pyc",
    ".mp3", ".mp4", ".avi", ".mkv", ".mov",
}
def read_file(path: str, max_bytes: int = 100_000) -> str:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return f"Error: el fichero '{path}' no existe."
    if p.suffix.lower() in _BINARY_EXTENSIONS:
        return f"Error: '{path}' es un fichero binario y no se puede leer como texto."
    try:
        content = p.read_text(encoding="utf-8", errors="replace")
        if len(content) > max_bytes:
            content = content[:max_bytes] + f"\n... [truncado a {max_bytes} bytes]"
        return content
    except Exception as exc:
        return f"Error leyendo '{path}': {exc}"
def write_file(path: str, content: str) -> str:
    p = Path(path).expanduser().resolve()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Fichero escrito correctamente: {p}"
    except Exception as exc:
        return f"Error escribiendo '{path}': {exc}"
def list_directory(path: str = ".") -> str:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return f"Error: '{path}' no existe."
    if not p.is_dir():
        return f"Error: '{path}' no es un directorio."
    try:
        entries = sorted(p.iterdir(), key=lambda e: (e.is_file(), e.name))
        lines = []
        for entry in entries:
            if entry.is_dir():
                lines.append(f"[DIR]  {entry.name}/")
            else:
                size = entry.stat().st_size
                lines.append(f"[FILE] {entry.name}  ({size} bytes)")
        return "\n".join(lines) if lines else "(directorio vacío)"
    except Exception as exc:
        return f"Error listando '{path}': {exc}"
READ_SCHEMA = {
    "name": "read_file",
    "description": "Lee el contenido de un fichero de texto. Soporta código, logs, configs, etc.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Ruta al fichero a leer."},
        },
        "required": ["path"],
    },
}
WRITE_SCHEMA = {
    "name": "write_file",
    "description": (
        "Escribe o sobreescribe un fichero con el contenido indicado. "
        "Crea los directorios necesarios automáticamente."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Ruta del fichero a escribir."},
            "content": {"type": "string", "description": "Contenido a escribir en el fichero."},
        },
        "required": ["path", "content"],
    },
}
LIST_SCHEMA = {
    "name": "list_directory",
    "description": "Lista el contenido de un directorio.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Ruta del directorio. Por defecto: directorio actual.",
            },
        },
        "required": [],
    },
}
_TOOL_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "list_directory": list_directory,
}
SCHEMAS = [READ_SCHEMA, WRITE_SCHEMA, LIST_SCHEMA]
def run_tool(name: str, arguments: dict[str, Any]) -> str:
    fn = _TOOL_MAP.get(name)
    if fn is None:
        return f"Herramienta de ficheros desconocida: {name}"
    ui.print_tool_call(name, arguments)
    result = fn(**arguments)
    ui.print_tool_output(result)
    return result
