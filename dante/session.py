"""
REPL interactivo de Dante.
Gestiona el bucle de prompt, los comandos internos (/profile, /model, etc.)
y la escritura del session log al salir.
"""
from __future__ import annotations
import os
from pathlib import Path
import yaml
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from . import memory
from .core import AgentCore
from .providers import get_provider
from .tools.registry import ToolRegistry
from .ui import terminal as ui
# Estilo del prompt de prompt_toolkit
_PROMPT_STYLE = Style.from_dict({
    "prompt": "ansibrightcyan bold",
})
_PROMPT_TEXT = [("class:prompt", "dante ❯ ")]
def _load_profile(profiles_dir: Path, profile_name: str) -> dict:
    profile_file = profiles_dir / f"{profile_name}.yaml"
    if not profile_file.exists():
        ui.print_warning(f"Perfil '{profile_name}' no encontrado. Usando 'default'.")
        profile_file = profiles_dir / "default.yaml"
    if not profile_file.exists():
        return {
            "name": "Default",
            "provider": "anthropic",
            "model": "claude-sonnet-4-6",
            "system_prompt": "Eres Dante, un agente de IA personal en terminal.",
            "tools": {},
        }
    with open(profile_file, encoding="utf-8") as f:
        return yaml.safe_load(f)
def _load_settings(config_dir: Path) -> dict:
    settings_file = config_dir / "settings.yaml"
    if not settings_file.exists():
        return {"shell_timeout": 60}
    with open(settings_file, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
def _build_system_prompt(soul_content: str, profile_system: str) -> str:
    return f"""{soul_content}
---
## Perfil activo
{profile_system}
## Contexto de ejecución
- Directorio de trabajo: {os.getcwd()}
- Fecha: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
def _summarize_session(history_entries: list[str]) -> str:
    """Genera un resumen breve de la sesión para el soul."""
    if not history_entries:
        return "Sesión vacía."
    count = len(history_entries)
    preview = history_entries[-1][:120].replace("\n", " ")
    return f"{count} mensajes. Último: {preview}"
class DanteSession:
    """Encapsula todo el estado de una sesión interactiva de Dante."""
    def __init__(self, config_dir: Path, initial_profile: str = "default") -> None:
        self._config_dir = config_dir
        self._profiles_dir = config_dir / "profiles"
        self._settings = _load_settings(config_dir)
        # Carga soul
        self._soul_content, self._soul_path = memory.load()
        # Carga perfil inicial
        self._profile_name = initial_profile
        self._profile = _load_profile(self._profiles_dir, initial_profile)
        # Inicializa proveedor, tools y core
        self._provider = get_provider(
            self._profile["provider"],
            self._profile["model"],
        )
        self._registry = ToolRegistry(
            self._profile.get("tools", {}),
            shell_timeout=self._settings.get("shell_timeout", 60),
        )
        system = _build_system_prompt(self._soul_content, self._profile["system_prompt"])
        self._core = AgentCore(self._provider, self._registry, system)
        # Historial de mensajes del usuario (para el session log)
        self._user_inputs: list[str] = []
    # ------------------------------------------------------------------
    # REPL principal
    # ------------------------------------------------------------------
    def run(self) -> None:
        ui.print_welcome(
            profile_name=self._profile["name"],
            provider=self._profile["provider"],
            model=self._profile["model"],
            soul_path=str(self._soul_path),
        )
        history_file = Path.home() / ".dante" / "history"
        history_file.parent.mkdir(parents=True, exist_ok=True)
        prompt_session: PromptSession = PromptSession(
            history=FileHistory(str(history_file)),
            style=_PROMPT_STYLE,
            multiline=False,
        )
        while True:
            try:
                user_input = prompt_session.prompt(_PROMPT_TEXT).strip()
            except (KeyboardInterrupt, EOFError):
                self._exit_session()
                break
            if not user_input:
                continue
            if user_input.startswith("/"):
                should_exit = self._handle_command(user_input)
                if should_exit:
                    break
                continue
            self._user_inputs.append(user_input)
            self._process_message(user_input)
    # ------------------------------------------------------------------
    # Procesamiento de mensajes
    # ------------------------------------------------------------------
    def _process_message(self, message: str) -> None:
        with ui.console.status("[cyan]Pensando...[/cyan]", spinner="dots"):
            try:
                response = self._core.send(message)
            except Exception as exc:
                ui.print_error(f"Error del agente: {exc}")
                return
        ui.print_response(response)
    # ------------------------------------------------------------------
    # Comandos internos
    # ------------------------------------------------------------------
    def _handle_command(self, command: str) -> bool:
        """Procesa un comando /xxx. Devuelve True si hay que salir."""
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""
        if cmd == "/exit":
            self._exit_session()
            return True
        elif cmd == "/clear":
            self._core.clear_history()
            self._user_inputs.clear()
            ui.print_success("Historial de sesión limpiado.")
        elif cmd == "/help":
            ui.print_help()
        elif cmd == "/soul":
            content, path = memory.load()
            ui.print_info(f"Soul: {path}")
            ui.console.print(content)
        elif cmd == "/tools":
            ui.print_tools_status(self._registry.tools_config)
        elif cmd == "/profile":
            if not arg:
                ui.print_warning("Uso: /profile <nombre>")
            else:
                self._switch_profile(arg)
        elif cmd == "/provider":
            if not arg:
                ui.print_warning("Uso: /provider <anthropic|openai|gemini>")
            else:
                self._switch_provider(arg)
        elif cmd == "/model":
            if not arg:
                ui.print_warning("Uso: /model <id-del-modelo>")
            else:
                self._switch_model(arg)
        else:
            ui.print_warning(f"Comando desconocido: {cmd}. Escribe /help para ver los disponibles.")
        return False
    # ------------------------------------------------------------------
    # Cambios en caliente de perfil / proveedor / modelo
    # ------------------------------------------------------------------
    def _switch_profile(self, profile_name: str) -> None:
        try:
            profile = _load_profile(self._profiles_dir, profile_name)
            self._profile_name = profile_name
            self._profile = profile
            self._provider = get_provider(profile["provider"], profile["model"])
            self._registry = ToolRegistry(
                profile.get("tools", {}),
                shell_timeout=self._settings.get("shell_timeout", 60),
            )
            system = _build_system_prompt(self._soul_content, profile["system_prompt"])
            self._core = AgentCore(self._provider, self._registry, system)
            ui.print_profile_switch(profile["name"], profile["provider"], profile["model"])
        except Exception as exc:
            ui.print_error(f"No se pudo cambiar al perfil '{profile_name}': {exc}")
    def _switch_provider(self, provider_name: str) -> None:
        try:
            new_provider = get_provider(provider_name, self._profile["model"])
            self._provider = new_provider
            self._profile["provider"] = provider_name
            self._core.switch_provider(new_provider)
            ui.print_success(f"Proveedor cambiado a: {provider_name}")
        except Exception as exc:
            ui.print_error(f"No se pudo cambiar al proveedor '{provider_name}': {exc}")
    def _switch_model(self, model_id: str) -> None:
        try:
            new_provider = get_provider(self._profile["provider"], model_id)
            self._provider = new_provider
            self._profile["model"] = model_id
            self._core.switch_provider(new_provider)
            ui.print_success(f"Modelo cambiado a: {model_id}")
        except Exception as exc:
            ui.print_error(f"No se pudo cambiar al modelo '{model_id}': {exc}")
    # ------------------------------------------------------------------
    # Cierre de sesión
    # ------------------------------------------------------------------
    def _exit_session(self) -> None:
        ui.print_info("Cerrando sesión...")
        summary = _summarize_session(self._user_inputs)
        try:
            memory.append_session_log(self._soul_path, summary)
            ui.print_success(f"Sesión guardada en soul: {self._soul_path}")
        except Exception as exc:
            ui.print_error(f"No se pudo actualizar el soul: {exc}")
        ui.console.print()
