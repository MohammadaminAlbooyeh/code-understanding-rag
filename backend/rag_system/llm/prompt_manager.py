import json


class PromptManager:
    def __init__(self):
        self.templates = {}

    def register_prompt(self, prompt_name: str, template: str):
        self.templates[prompt_name] = template

    def get_prompt(self, prompt_name: str, **kwargs) -> str:
        if prompt_name not in self.templates:
            raise KeyError(f"Prompt template '{prompt_name}' not found")
        template = self.templates[prompt_name]
        if kwargs:
            return template.format(**kwargs)
        return template

    def format_prompt(self, template: str, **kwargs) -> str:
        return template.format(**kwargs)

    def load_prompts_from_file(self, filepath: str):
        with open(filepath, "r") as f:
            data = json.load(f)
        for name, template in data.items():
            self.register_prompt(name, template)
