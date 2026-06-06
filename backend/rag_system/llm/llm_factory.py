class LLMFactory:
    def __init__(self):
        self.providers = {
            "openai": "OpenAILLM",
            "anthropic": "ClaudeLLM",
            "groq": "GroqLLM",
        }

    def create(self, provider: str, **kwargs):
        pass

    def get_available_providers(self) -> list[str]:
        return list(self.providers.keys())

    def set_default_provider(self, provider: str):
        pass
