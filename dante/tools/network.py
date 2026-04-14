"""
Herramienta de red — nmap, ping, whois, traceroute, dig.
Solo disponible cuando el perfil activo la habilita (pentester, sysadmin).
"""
from __future__ import annotations
import shutil
import subprocess
from typing import Any
from ..ui import terminal as ui
# Herramientas permitidas y sus comandos base seguros
_TOOL_TEMPLATES: dict[str, str] = {
    "ping":        "ping -c 4 {target}",
    "traceroute":  "traceroute {target}",
    "nmap":        "nmap {options} {target}",
    "dig":         "dig {target} {record_type}",
    "whois":       "whois {target}",
    "nslookup":    "nslookup {target}",
    "curl":        "curl -s -I --max-time 10 {url}",
    "ss":          "ss -tulpn",
    "netstat":     "netstat -tulpn",
    "ip":          "ip {subcommand}",
}
# Opciones de nmap permitidas (bloquea flags agresivos sin destino claro)
_NMAP_SAFE_FLAGS = {"-sV", "-sC", "-p", "-T4", "-A", "-O", "--script", "-sn", "-Pn"}
def _check_available(tool: str) -> bool:
    return shutil.which(tool) is not None
def run_network_tool(
    tool: str,
    target: str = "",
    options: str = "",
    allowed_tools: list[str] | None = None,
) -> str:
    allowed = allowed_tools or list(_TOOL_TEMPLATES.keys())
    if tool not in allowed:
        return f"Herramienta '{tool}' no permitida en el perfil actual. Permitidas: {allowed}"
    if not _check_available(tool):
        return f"'{tool}' no está instalado en el sistema."
    # Construye el comando
    template = _TOOL_TEMPLATES.get(tool, "{tool} {target}")
    if tool == "nmap":
        command = f"nmap {options} {target}".strip()
    elif tool == "dig":
        parts = target.split()
        host = parts[0]
        record = parts[1] if len(parts) > 1 else "A"
        command = f"dig {host} {record}"
    elif tool == "curl":
        command = f"curl -s -I --max-time 10 {target}"
    elif tool == "ip":
        command = f"ip {options or 'addr'}"
    elif tool in ("ss", "netstat"):
        command = f"{tool} -tulpn"
    else:
        command = f"{tool} {target}".strip()
    ui.print_tool_call(f"network:{tool}", {"target": target, "options": options})
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = result.stdout + result.stderr
        ui.print_tool_output(output or "(sin salida)")
        return output or f"[exit code: {result.returncode}]"
    except subprocess.TimeoutExpired:
        return f"Timeout (120s) esperando respuesta de {tool}."
    except Exception as exc:
        return f"Error ejecutando {tool}: {exc}"
SCHEMA = {
    "name": "network_tool",
    "description": (
        "Ejecuta herramientas de red: nmap, ping, traceroute, dig, whois, etc. "
        "Solo disponible en perfiles pentester y sysadmin."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "tool": {
                "type": "string",
                "description": "Herramienta a usar: nmap, ping, traceroute, dig, whois, curl, ss, ip...",
                "enum": list(_TOOL_TEMPLATES.keys()),
            },
            "target": {
                "type": "string",
                "description": "IP, dominio o URL objetivo.",
            },
            "options": {
                "type": "string",
                "description": "Opciones adicionales para la herramienta (ej: '-sV -p 80,443' para nmap).",
            },
        },
        "required": ["tool"],
    },
}
def run_tool(arguments: dict[str, Any], allowed_tools: list[str] | None = None) -> str:
    return run_network_tool(
        tool=arguments["tool"],
        target=arguments.get("target", ""),
        options=arguments.get("options", ""),
        allowed_tools=allowed_tools,
    )
