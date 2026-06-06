# LLM Guide

## Supported Providers

- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3)
- Groq (Mixtral, Llama)

## Configuration

Configure via environment variables or `config/llm_config.py`.

```python
from backend.rag_system.llm.llm_factory import LLMFactory

factory = LLMFactory()
llm = factory.create("openai", model="gpt-4")
```
