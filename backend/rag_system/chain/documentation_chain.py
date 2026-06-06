class DocumentationChain:
    def __init__(self, llm, prompt_manager):
        self.llm = llm
        self.prompt_manager = prompt_manager

    def generate_function_docs(self, func_data: dict) -> str:
        pass

    def generate_class_docs(self, class_data: dict) -> str:
        pass

    def generate_module_docs(self, module_data: dict) -> str:
        pass

    def generate_api_docs(self, api_data: dict) -> str:
        pass

    def generate_readme(self, project_data: dict) -> str:
        pass
