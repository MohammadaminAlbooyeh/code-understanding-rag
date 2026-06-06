from backend.rag_system.chain.rag_chain import RAGChain
from backend.rag_system.llm.llm_factory import LLMFactory
from backend.rag_system.llm.prompt_manager import PromptManager


def main():
    factory = LLMFactory()
    llm = factory.create("openai")
    prompt_manager = PromptManager()
    rag_chain = RAGChain(None, llm, prompt_manager)

    answer = rag_chain.run("What does this code do?")
    print(answer)


if __name__ == "__main__":
    main()
