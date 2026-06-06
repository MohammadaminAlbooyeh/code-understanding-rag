from backend.rag_system.chain.documentation_chain import DocumentationChain
from backend.rag_system.llm.llm_factory import LLMFactory
from backend.rag_system.llm.prompt_manager import PromptManager


def main():
    factory = LLMFactory()
    llm = factory.create("openai")
    prompt_manager = PromptManager()
    doc_chain = DocumentationChain(llm, prompt_manager)

    func_data = {
        "name": "calculate_total",
        "params": [{"name": "items", "type": "list"}],
        "returns": "float",
    }

    docs = doc_chain.generate_function_docs(func_data)
    print(docs)


if __name__ == "__main__":
    main()
