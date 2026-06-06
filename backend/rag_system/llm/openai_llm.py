from openai import OpenAI
from backend.utils.config import settings


class OpenAILLM:
    def __init__(self, model: str = "gpt-4", api_key: str = None):
        self.model = model
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.client:
            return f"[OpenAILLM Mock] Response for: {prompt[:50]}..."
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception:
            return f"[OpenAILLM Mock] Response for: {prompt[:50]}..."

    def generate_stream(self, prompt: str, **kwargs):
        if not self.client:
            yield f"[OpenAILLM Mock] Stream response for: {prompt[:50]}..."
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
            yield f"[OpenAILLM Mock] Stream response for: {prompt[:50]}..."

    def generate_with_context(self, context: str, prompt: str, **kwargs) -> str:
        if not self.client:
            return f"[OpenAILLM Mock] Context: {context[:50]}... Prompt: {prompt[:50]}..."
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
            return f"[OpenAILLM Mock] Context: {context[:50]}... Prompt: {prompt[:50]}..."
