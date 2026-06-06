class PromptManager:
    def __init__(self):
        self.templates = {}

    def register_prompt(self, name: str, template: str):
        pass

    def get_prompt(self, name: str, **kwargs) -> str:
        pass

    def format_prompt(self, template: str, **kwargs) -> str:
        pass

    def load_prompts_from_file(self, filepath: str):
        pass
