import pytest
from backend.code_analysis.analyzer.complexity_analyzer import ComplexityAnalyzer


def test_complexity_analysis():
    analyzer = ComplexityAnalyzer()
    code = "def foo():\n    if x:\n        return 1\n    return 2\n"
    result = analyzer.analyze(code, "python")
    assert result is not None
