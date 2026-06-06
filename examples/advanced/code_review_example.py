from backend.rag_system.chain.review_chain import ReviewChain
from backend.rag_system.llm.llm_factory import LLMFactory
from backend.rag_system.llm.prompt_manager import PromptManager


def main():
    factory = LLMFactory()
    llm = factory.create("openai")
    prompt_manager = PromptManager()
    review_chain = ReviewChain(llm, prompt_manager)

    code = """
def process(data):
    result = []
    for i in range(len(data)):
        result.append(data[i] * 2)
    return result
"""
    review = review_chain.review_code(code, "python")
    print("Review:", review)


if __name__ == "__main__":
    main()
