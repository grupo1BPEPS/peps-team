from .anthropic_p import AnthropicProvider
from .openai_p import OpenAIProvider
from .gemini_p import GeminiProvider
from .base import BaseProvider
_REGISTRY: dict[str, type[BaseProvider]] = {
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
}
def get_provider(name: str, model: str) -> BaseProvider:
    name = name.lower()
    if name not in _REGISTRY:
        raise ValueError(f"Proveedor desconocido: '{name}'. Opciones: {list(_REGISTRY)}")
    return _REGISTRY[name](model=model)
