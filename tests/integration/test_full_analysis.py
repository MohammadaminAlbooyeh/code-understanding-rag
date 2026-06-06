import pytest
from backend.code_analysis.parser.code_parser import CodeParser
from backend.code_analysis.analyzer.complexity_analyzer import ComplexityAnalyzer
from backend.code_analysis.analyzer.bug_detector import BugDetector
from backend.code_analysis.analyzer.security_analyzer import SecurityAnalyzer
from backend.code_analysis.generators.summary_generator import SummaryGenerator


@pytest.fixture
def sample_python_code():
    return """
import os
import sys

class UserManager:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}"

def process_data(items):
    result = []
    for item in items:
        if item > 0:
            result.append(item)
        elif item == 0:
            print("zero")
        else:
            print("negative")
    return result

def main():
    manager = UserManager("Alice")
    print(manager.greet())
    data = [1, -2, 0, 3]
    output = process_data(data)
    return len(output)
"""


class TestFullAnalysisPipeline:
    def test_parse_to_complexity_analysis(self, sample_python_code):
        parser = CodeParser()
        parsed = parser.parse(sample_python_code, "python")

        assert parsed["language"] == "python"
        assert len(parsed["functions"]) >= 3
        assert len(parsed["classes"]) == 1
        assert parsed["classes"][0]["name"] == "UserManager"

        analyzer = ComplexityAnalyzer()
        complexity = analyzer.analyze(sample_python_code, "python")

        assert complexity["cyclomatic_complexity"] > 1
        assert complexity["num_functions"] >= 3
        assert complexity["num_classes"] == 1
        assert complexity["num_conditionals"] >= 3
        assert complexity["num_loops"] >= 1
        assert complexity["lines_of_code"] > 0

    def test_parse_to_bug_detection(self, sample_python_code):
        parser = CodeParser()
        parsed = parser.parse(sample_python_code, "python")
        assert parsed is not None

        detector = BugDetector()
        bugs = detector.analyze(sample_python_code, "python")
        assert isinstance(bugs, list)

    def test_parse_to_security_analysis(self, sample_python_code):
        parser = CodeParser()
        parsed = parser.parse(sample_python_code, "python")
        assert parsed is not None

        security = SecurityAnalyzer()
        vulns = security.analyze(sample_python_code, "python")
        assert isinstance(vulns, list)

    def test_parse_to_summary(self, sample_python_code):
        parser = CodeParser()
        parsed = parser.parse(sample_python_code, "python")

        generator = SummaryGenerator()
        summary = generator.generate(parsed)

        assert "function_summaries" in summary
        assert "file_summary" in summary
        assert len(summary["function_summaries"]) >= 3

        file_summary = summary["file_summary"]
        assert "Functions: 3" in file_summary or "Functions: 4" in file_summary
        assert "Classes: 1" in file_summary

    def test_full_pipeline(self, sample_python_code):
        parser = CodeParser()
        parsed = parser.parse(sample_python_code, "python")

        analyzer = ComplexityAnalyzer()
        complexity = analyzer.analyze(sample_python_code, "python")

        detector = BugDetector()
        bugs = detector.analyze(sample_python_code, "python")

        security = SecurityAnalyzer()
        vulns = security.analyze(sample_python_code, "python")

        generator = SummaryGenerator()
        summary = generator.generate(parsed)

        assert parsed["language"] == "python"
        assert complexity["cyclomatic_complexity"] > 0
        assert isinstance(bugs, list)
        assert isinstance(vulns, list)
        assert len(summary["function_summaries"]) > 0

    def test_analyze_multiple_files(self, tmp_path):
        parser = CodeParser()

        (tmp_path / "mod1.py").write_text("def func1():\n    return 1\n")
        (tmp_path / "mod2.py").write_text("def func2():\n    return 2\n")

        results = parser.parse_directory(str(tmp_path))
        assert len(results) == 2

        all_code = "\n".join(r["code"] for r in results) if False else ""

        for r in results:
            assert "language" in r
            assert "functions" in r
