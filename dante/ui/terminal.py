"""
UI de terminal para Dante usando Rich.
Maneja el renderizado de respuestas, tool calls, errores y estado del agente.
"""
from __future__ import annotations
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.style import Style
from rich.text import Text
from rich import box
console = Console()
# Paleta de colores
COLORS = {
    "prompt":    "bold cyan",
    "response":  "white",
    "tool_call": "bold yellow",
    "tool_out":  "dim white",
    "error":     "bold red",
    "warning":   "yellow",
    "success":   "bold green",
    "info":      "dim cyan",
    "profile":   "bold magenta",
    "separator": "dim blue",
}
def print_welcome(profile_name: str, provider: str, model: str, soul_path: str) -> None:
    banner = Text()
    banner.append("  DANTE  ", style="bold white on dark_red")
    banner.append(f"  {profile_name}", style=COLORS["profile"])
    banner.append(f"  {provider}/{model}", style=COLORS["info"])
    console.print()
    console.print(banner)
    console.print(f"  soul: [dim]{soul_path}[/dim]")
    console.print(f"  [dim]Escribe tu mensaje. /help para comandos. /exit para salir.[/dim]")
    console.print()
def print_separator() -> None:
    console.print(Rule(style=COLORS["separator"]))
def print_response(text: str) -> None:
    """Renderiza la respuesta del agente como Markdown."""
    console.print()
    try:
        console.print(Markdown(text))
    except Exception:
        console.print(text, style=COLORS["response"])
    console.print()
def print_tool_call(tool_name: str, args: dict) -> None:
    """Muestra qué herramienta va a ejecutar Dante."""
    args_str = "  ".join(f"[dim]{k}[/dim]=[yellow]{v}[/yellow]" for k, v in args.items())
    console.print(f"  [bold yellow]⚙[/bold yellow]  [yellow]{tool_name}[/yellow]  {args_str}")
def print_tool_output(output: str, truncate: int = 2000) -> None:
    """Muestra el resultado de una herramienta (truncado si es muy largo)."""
    if len(output) > truncate:
        output = output[:truncate] + f"\n... [dim](truncado a {truncate} chars)[/dim]"
    console.print(
        Panel(output, style=COLORS["tool_out"], box=box.SIMPLE, padding=(0, 1))
    )
def print_confirmation_prompt(action: str) -> str:
    """
    Muestra un aviso de acción peligrosa y pide confirmación.
    Devuelve 's' o 'n'.
    """
    console.print()
    console.print(
        Panel(
            f"[bold red]ACCION CRITICA[/bold red]\n{action}",
            border_style="red",
            box=box.HEAVY,
        )
    )
    response = console.input("[bold red]¿Confirmas? [s/N]: [/bold red]").strip().lower()
    return response
def print_error(message: str) -> None:
    console.print(f"  [bold red]✗[/bold red]  {message}", style=COLORS["error"])
def print_warning(message: str) -> None:
    console.print(f"  [yellow]⚠[/yellow]  {message}", style=COLORS["warning"])
def print_info(message: str) -> None:
    console.print(f"  [dim cyan]ℹ[/dim cyan]  [dim]{message}[/dim]")
def print_success(message: str) -> None:
    console.print(f"  [bold green]✓[/bold green]  {message}")
def print_profile_switch(profile_name: str, provider: str, model: str) -> None:
    console.print(
        f"  [bold magenta]»[/bold magenta]  Perfil: [magenta]{profile_name}[/magenta]  "
        f"[dim]{provider}/{model}[/dim]"
    )
def print_help() -> None:
    help_text = """\
## Comandos disponibles
| Comando | Descripción |
|---|---|
| `/profile <nombre>` | Cambia el perfil activo (default, programmer, pentester, sysadmin) |
| `/model <id>` | Cambia el modelo (ej: gpt-4o, claude-opus-4-6, gemini-2.0-flash) |
| `/provider <nombre>` | Cambia el proveedor (anthropic, openai, gemini) |
| `/tools` | Muestra herramientas activas en el perfil actual |
| `/soul` | Muestra el contenido del archivo soul activo |
| `/clear` | Limpia el historial de la sesión actual |
| `/help` | Muestra esta ayuda |
| `/exit` | Guarda hitos en soul y cierra la sesión |
"""
    console.print(Markdown(help_text))
def print_tools_status(tools_config: dict) -> None:
    lines = []
    for name, cfg in tools_config.items():
        enabled = cfg.get("enabled", False)
        status = "[green]activa[/green]" if enabled else "[dim]desactivada[/dim]"
        lines.append(f"  [bold]{name}[/bold]: {status}")
    console.print("\n".join(lines))
    console.print()
