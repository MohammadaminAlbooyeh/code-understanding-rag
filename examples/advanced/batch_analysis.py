import os
from backend.code_analysis.parser.code_parser import CodeParser


def batch_analyze(directory: str):
    parser = CodeParser()
    results = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                parsed = parser.parse_file(filepath)
                results.append(parsed)

    return results


if __name__ == "__main__":
    results = batch_analyze("./src")
    print(f"Analyzed {len(results)} files")
