"""
Gestión del archivo soul — memoria a largo plazo de Dante.
Busca soul en el directorio actual primero, luego en ~/.dante/soul.
"""
from __future__ import annotations
import os
from datetime import datetime
from pathlib import Path
_GLOBAL_SOUL = Path.home() / ".dante" / "soul"
_SESSION_LOG_MARKER = "## Session Log"
def _find_soul_path() -> Path:
    """Devuelve la ruta al soul activo (local > global)."""
    local = Path.cwd() / "soul"
    if local.exists():
        return local
    _GLOBAL_SOUL.parent.mkdir(parents=True, exist_ok=True)
    if not _GLOBAL_SOUL.exists():
        _create_default_soul(_GLOBAL_SOUL)
    return _GLOBAL_SOUL
def _create_default_soul(path: Path) -> None:
    """Crea un soul mínimo por defecto."""
    default = """\
# DANTE — Long Term Memory (LTM)
## Identity
Name: Dante
Version: 0.1.0
## Personality
- Responde de forma directa, técnica y sin relleno.
- Razona en bloques completos antes de actuar.
- Pide confirmación solo para acciones irreversibles.
## User Profile
- (Edita con tu nombre y contexto)
## Rules
- Ejecuta comandos automáticamente salvo que sean destructivos.
- Al finalizar la sesión, actualiza Session Log.
## Session Log
"""
    path.write_text(default, encoding="utf-8")
def load() -> tuple[str, Path]:
    """
    Carga el contenido del soul activo.
    Devuelve (contenido, ruta).
    """
    path = _find_soul_path()
    content = path.read_text(encoding="utf-8")
    return content, path
def append_session_log(path: Path, summary: str) -> None:
    """
    Añade una entrada de sesión al soul.
    Se llama al cerrar con /exit.
    """
    content = path.read_text(encoding="utf-8")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"- [{timestamp}] — {summary}\n"
    if _SESSION_LOG_MARKER in content:
        updated = content + entry
    else:
        updated = content + f"\n{_SESSION_LOG_MARKER}\n" + entry
    path.write_text(updated, encoding="utf-8")
def soul_path() -> Path:
    """Devuelve la ruta al soul activo (sin cargarlo)."""
    return _find_soul_path()
