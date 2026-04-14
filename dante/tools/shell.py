"""
Herramienta shell — ejecución de comandos del sistema.
Auto-ejecución salvo patrones marcados como peligrosos en settings.yaml.
"""
from __future__ import annotations
import re
import subprocess
from typing import Any
from ..ui import terminal as ui
# Patrones que siempre requieren confirmación humana
_DEFAULT_DANGER_PATTERNS = [
    r"rm\s+-rf",
    r"rm\s+-r\s+/",
    r"\bdd\b.*of=",
    r"\bmkfs\b",
    r">\s*/dev/sd",
    r"DROP\s+DATABASE",
    r"DROP\s+TABLE",
    r"TRUNCATE\s+TABLE",
    r":\(\)\s*\{.*\}.*:",
    r"sudo\s+rm\s+-rf\s+/",
    r"chmod\s+-R\s+777\s+/",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bhalt\b",
]
_compiled: list[re.Pattern] | None = None
def _get_patterns(extra: list[str] | None = None) -> list[re.Pattern]:
    global _compiled
    if _compiled is None:
        _compiled = [re.compile(p, re.IGNORECASE) for p in _DEFAULT_DANGER_PATTERNS]
    if extra:
        return _compiled + [re.compile(p, re.IGNORECASE) for p in extra]
    return _compiled
def is_dangerous(command: str, extra_patterns: list[str] | None = None) -> bool:
    """Devuelve True si el comando coincide con algún patrón peligroso."""
    for pattern in _get_patterns(extra_patterns):
        if pattern.search(command):
            return True
    return False
def execute(command: str, timeout: int = 60, cwd: str | None = None) -> dict[str, Any]:
    """
    Ejecuta un comando shell y devuelve stdout, stderr y código de retorno.
    Si el comando es peligroso, pide confirmación antes de ejecutar.
    """
    if is_dangerous(command):
        answer = ui.print_confirmation_prompt(command)
        if answer not in ("s", "si", "sí", "y", "yes"):
            return {
                "stdout": "",
                "stderr": "Comando cancelado por el usuario.",
                "returncode": -1,
                "cancelled": True,
            }
    ui.print_tool_call("shell", {"cmd": command})
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
        )
        output = result.stdout + result.stderr
        ui.print_tool_output(output or "(sin salida)")
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "cancelled": False,
        }
    except subprocess.TimeoutExpired:
        msg = f"Timeout ({timeout}s) alcanzado para el comando."
        ui.print_error(msg)
        return {"stdout": "", "stderr": msg, "returncode": -1, "cancelled": False}
    except Exception as exc:
        msg = str(exc)
        ui.print_error(msg)
        return {"stdout": "", "stderr": msg, "returncode": -1, "cancelled": False}
# Schema de herramienta para los proveedores de IA
SCHEMA = {
    "name": "execute_shell",
    "description": (
        "Ejecuta un comando en la terminal del sistema operativo. "
        "Úsalo para operaciones de sistema, git, docker, compilar código, "
        "instalar paquetes, leer procesos, etc."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "El comando shell a ejecutar.",
            },
            "cwd": {
                "type": "string",
                "description": "Directorio de trabajo opcional. Por defecto: directorio actual.",
            },
        },
        "required": ["command"],
    },
}
def run_tool(arguments: dict[str, Any], timeout: int = 60) -> str:
    """Entry point llamado por el core cuando el modelo invoca esta herramienta."""
    command = arguments["command"]
    cwd = arguments.get("cwd")
    result = execute(command, timeout=timeout, cwd=cwd)
    if result["cancelled"]:
        return "El usuario canceló la ejecución del comando."
    parts = []
    if result["stdout"]:
        parts.append(result["stdout"])
    if result["stderr"]:
        parts.append(f"[stderr]\n{result['stderr']}")
    parts.append(f"[exit code: {result['returncode']}]")
    return "\n".join(parts)
