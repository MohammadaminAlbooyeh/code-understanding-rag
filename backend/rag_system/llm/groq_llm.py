from groq import Groq
from backend.utils.config import settings


class GroqLLM:
    def __init__(self, model: str = "mixtral-8x7b-32768", api_key: str = None):
        self.model = model
        self.api_key = api_key or settings.GROQ_API_KEY
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.client:
            return f"[GroqLLM Mock] Response for: {prompt[:50]}..."
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception:
            return f"[GroqLLM Mock] Response for: {prompt[:50]}..."

    def generate_stream(self, prompt: str, **kwargs):
        if not self.client:
            yield f"[GroqLLM Mock] Stream response for: {prompt[:50]}..."
            return
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                **kwargs
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception:
            yield f"[GroqLLM Mock] Stream response for: {prompt[:50]}..."

    def generate_with_context(self, context: str, prompt: str, **kwargs) -> str:
        if not self.client:
            return f"[GroqLLM Mock] Context: {context[:50]}... Prompt: {prompt[:50]}..."
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception:
            return f"[GroqLLM Mock] Context: {context[:50]}... Prompt: {prompt[:50]}..."
