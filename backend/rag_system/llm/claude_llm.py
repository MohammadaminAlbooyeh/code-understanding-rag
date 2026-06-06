from anthropic import Anthropic
from backend.utils.config import settings


class ClaudeLLM:
    def __init__(self, model: str = "claude-3-opus-20240229", api_key: str = None):
        self.model = model
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.client = Anthropic(api_key=self.api_key) if self.api_key else None

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.client:
            return f"[ClaudeLLM Mock] Response for: {prompt[:50]}..."
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.pop("max_tokens", 4096),
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.content[0].text
        except Exception:
            return f"[ClaudeLLM Mock] Response for: {prompt[:50]}..."

    def generate_stream(self, prompt: str, **kwargs):
        if not self.client:
            yield f"[ClaudeLLM Mock] Stream response for: {prompt[:50]}..."
            return
        try:
            stream = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.pop("max_tokens", 4096),
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                **kwargs
            )
            for chunk in stream:
                if chunk.type == "content_block_delta" and chunk.delta.text:
                    yield chunk.delta.text
        except Exception:
            yield f"[ClaudeLLM Mock] Stream response for: {prompt[:50]}..."

    def generate_with_context(self, context: str, prompt: str, **kwargs) -> str:
        if not self.client:
            return f"[ClaudeLLM Mock] Context: {context[:50]}... Prompt: {prompt[:50]}..."
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.pop("max_tokens", 4096),
                system=context,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.content[0].text
        except Exception:
            return f"[ClaudeLLM Mock] Context: {context[:50]}... Prompt: {prompt[:50]}..."
