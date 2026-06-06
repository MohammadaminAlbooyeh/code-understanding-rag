from backend.code_analysis.parser.code_parser import CodeParser
from backend.code_analysis.analyzer.complexity_analyzer import ComplexityAnalyzer


def main():
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    parser = CodeParser()
    parsed = parser.parse(code, "python")

    analyzer = ComplexityAnalyzer()
    complexity = analyzer.analyze(code, "python")

    print("Parsed:", parsed)
    print("Complexity:", complexity)


if __name__ == "__main__":
    main()
