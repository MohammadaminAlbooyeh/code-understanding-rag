import pytest
from backend.rag_system.llm.prompt_manager import PromptManager
from backend.rag_system.llm.llm_factory import LLMFactory
import tempfile
import json


class TestPromptManager:
    @pytest.fixture
    def pm(self):
        return PromptManager()

    def test_register_and_get_prompt(self, pm):
        pm.register_prompt("greeting", "Hello, {name}!")
        result = pm.get_prompt("greeting", name="World")
        assert result == "Hello, World!"

    def test_get_prompt_no_args(self, pm):
        pm.register_prompt("simple", "Just a template")
        result = pm.get_prompt("simple")
        assert result == "Just a template"

    def test_get_prompt_not_found(self, pm):
        with pytest.raises(KeyError):
            pm.get_prompt("nonexistent")

    def test_format_prompt(self, pm):
        result = pm.format_prompt("Answer: {answer}", answer="42")
        assert result == "Answer: 42"

    def test_format_prompt_no_kwargs(self, pm):
        result = pm.format_prompt("static text")
        assert result == "static text"

    def test_register_multiple(self, pm):
        pm.register_prompt("a", "template a")
        pm.register_prompt("b", "template b")
        assert pm.get_prompt("a") == "template a"
        assert pm.get_prompt("b") == "template b"

    def test_load_prompts_from_file(self, pm):
        data = {"q1": "Question 1: {topic}", "q2": "Question 2"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            fpath = f.name
        try:
            pm.load_prompts_from_file(fpath)
            assert pm.get_prompt("q1", topic="math") == "Question 1: math"
            assert pm.get_prompt("q2") == "Question 2"
        finally:
            import os
            os.unlink(fpath)


class TestLLMFactory:
    @pytest.fixture
    def factory(self):
        return LLMFactory()

    def test_get_available_providers(self, factory):
        providers = factory.get_available_providers()
        assert "openai" in providers
        assert "anthropic" in providers
        assert "groq" in providers

    def test_create_unknown_provider(self, factory):
        with pytest.raises(ValueError, match="Unknown provider"):
            factory.create(provider="nonexistent")

    def test_create_openai_with_api_key(self, factory):
        llm = factory.create(provider="openai", api_key="sk-test")
        assert llm is not None

    def test_set_default_provider(self, factory):
        factory.set_default_provider("groq")
        assert factory.default_provider == "groq"

    def test_set_default_provider_invalid(self, factory):
        with pytest.raises(ValueError):
            factory.set_default_provider("invalid")

    def test_create_default_provider(self, factory):
        orig_default = factory.default_provider
        factory.set_default_provider("openai")
        result = factory.create(api_key="sk-test")
        assert result is not None
        factory.set_default_provider(orig_default)
