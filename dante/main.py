"""
Entry point de la CLI de Dante.
Instalado globalmente via pyproject.toml: dante = "dante.main:main"
Uso:
    dante                        # perfil default
    dante --profile pentester    # perfil pentester
    dante --profile sysadmin     # perfil sysadmin
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv
def _find_config_dir() -> Path:
    """
    Busca el directorio de config en orden:
    1. Junto al paquete instalado (para desarrollo: dante/config/)
    2. ~/.dante/config/ (instalación global)
    """
    # Directorio del paquete: dante/dante/ → dante/
    pkg_dir = Path(__file__).parent
    project_config = pkg_dir.parent / "config"
    if project_config.exists():
        return project_config
    global_config = Path.home() / ".dante" / "config"
    return global_config
def _load_env() -> None:
    """Carga .env del directorio actual y del home de Dante."""
    load_dotenv(Path.cwd() / ".env", override=False)
    load_dotenv(Path.home() / ".dante" / ".env", override=False)
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="dante",
        description="Dante — Agente de IA personal en terminal.",
    )
    parser.add_argument(
        "--profile", "-p",
        default="default",
        metavar="NOMBRE",
        help="Perfil a cargar al iniciar (default, programmer, pentester, sysadmin).",
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="dante 0.1.0",
    )
    args = parser.parse_args()
    _load_env()
    config_dir = _find_config_dir()
    if not config_dir.exists():
        print(
            f"[dante] Directorio de configuración no encontrado: {config_dir}\n"
            f"Asegúrate de instalar Dante correctamente con: pip install -e /ruta/a/dante",
            file=sys.stderr,
        )
        sys.exit(1)
    from .session import DanteSession
    session = DanteSession(
        config_dir=config_dir,
        initial_profile=args.profile,
    )
    try:
        session.run()
    except KeyboardInterrupt:
        pass
if __name__ == "__main__":
    main()
