from backend.rag_system.prompts.documentation_prompts import (
    FUNCTION_DOC_PROMPT,
    CLASS_DOC_PROMPT,
    MODULE_DOC_PROMPT,
    API_DOC_PROMPT,
)


class DocumentationChain:
    def __init__(self, llm, prompt_manager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    def generate_function_docs(self, func_data: dict) -> str:
        prompt = f"{FUNCTION_DOC_PROMPT}\n\nFunction Data:\n{func_data}"
        return self.llm.generate(prompt)

    def generate_class_docs(self, class_data: dict) -> str:
        prompt = f"{CLASS_DOC_PROMPT}\n\nClass Data:\n{class_data}"
        return self.llm.generate(prompt)

    def generate_module_docs(self, module_data: dict) -> str:
        prompt = f"{MODULE_DOC_PROMPT}\n\nModule Data:\n{module_data}"
        return self.llm.generate(prompt)

    def generate_api_docs(self, api_data: dict) -> str:
        prompt = f"{API_DOC_PROMPT}\n\nAPI Data:\n{api_data}"
        return self.llm.generate(prompt)

    def generate_readme(self, project_data: dict) -> str:
        prompt = f"{MODULE_DOC_PROMPT}\n\nGenerate a README for the following project:\n\nProject Data:\n{project_data}"
        return self.llm.generate(prompt)
