from backend.utils.config import settings
from backend.rag_system.llm.openai_llm import OpenAILLM
from backend.rag_system.llm.claude_llm import ClaudeLLM
from backend.rag_system.llm.groq_llm import GroqLLM


class LLMFactory:
    def __init__(self):
        self.providers = {
            "openai": OpenAILLM,
            "anthropic": ClaudeLLM,
            "groq": GroqLLM,
        }
        self.default_provider = settings.DEFAULT_LLM

    def create(self, provider: str = None, **kwargs):
        provider = provider or self.default_provider
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(self.providers.keys())}")

        llm_class = self.providers[provider]
        if "api_key" not in kwargs:
            if provider == "openai":
                kwargs.setdefault("api_key", settings.OPENAI_API_KEY)
            elif provider == "anthropic":
                kwargs.setdefault("api_key", settings.ANTHROPIC_API_KEY)
            elif provider == "groq":
                kwargs.setdefault("api_key", settings.GROQ_API_KEY)

        if "model" not in kwargs:
            if provider == "openai":
                kwargs.setdefault("model", settings.OPENAI_MODEL)
            elif provider == "anthropic":
                kwargs.setdefault("model", settings.ANTHROPIC_MODEL)
            elif provider == "groq":
                kwargs.setdefault("model", settings.GROQ_MODEL)

        return llm_class(**kwargs)

    def get_available_providers(self) -> list[str]:
        return list(self.providers.keys())

    def set_default_provider(self, provider: str):
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(self.providers.keys())}")
        self.default_provider = provider
