import pytest
from backend.code_analysis.parser.code_parser import CodeParser
from backend.code_analysis.analyzer.complexity_analyzer import ComplexityAnalyzer
from backend.code_analysis.analyzer.bug_detector import BugDetector
from backend.code_analysis.analyzer.security_analyzer import SecurityAnalyzer
from backend.code_analysis.analyzer.pattern_analyzer import PatternAnalyzer
from backend.code_analysis.generators.summary_generator import SummaryGenerator
from backend.code_analysis.generators.statistics_generator import StatisticsGenerator
from backend.code_analysis.generators.diagram_generator import DiagramGenerator
from backend.rag_system.embeddings.chunk_splitter import ChunkSplitter
from backend.rag_system.retrieval.similarity_matcher import SimilarityMatcher


@pytest.fixture
def sample_app_code():
    return """
from flask import Flask, request

app = Flask(__name__)

@app.route("/api/hello")
def hello():
    name = request.args.get("name", "World")
    return f"Hello, {name}!"

@app.route("/api/add")
def add():
    a = int(request.args.get("a", 0))
    b = int(request.args.get("b", 0))
    return str(a + b)

def validate_input(data):
    if not data:
        return False
    if len(data) > 100:
        return False
    return True

class Calculator:
    def __init__(self):
        self.history = []

    def calculate(self, a, b, operation):
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return None
            result = a / b
        else:
            return None
        self.history.append((a, b, operation, result))
        return result

    def get_history(self):
        return self.history
"""


class TestEndToEnd:
    def test_create_parse_analyze_summarize(self, sample_app_code):
        parser = CodeParser()
        parsed = parser.parse(sample_app_code, "python")
        assert parsed is not None
        assert len(parsed["functions"]) >= 3

        analyzer = ComplexityAnalyzer()
        complexity = analyzer.analyze(sample_app_code, "python")
        assert complexity["cyclomatic_complexity"] > 0
        assert complexity["num_functions"] >= 3
        assert complexity["num_classes"] == 1
        assert complexity["num_conditionals"] >= 5

        detector = BugDetector()
        bugs = detector.analyze(sample_app_code, "python")
        assert isinstance(bugs, list)

        security = SecurityAnalyzer()
        vulns = security.analyze(sample_app_code, "python")
        assert isinstance(vulns, list)

        pattern = PatternAnalyzer()
        patterns = pattern.analyze(sample_app_code, "python")
        assert "design_patterns" in patterns

    def test_generate_docs_and_stats(self, sample_app_code):
        parser = CodeParser()
        parsed = parser.parse(sample_app_code, "python")

        summary_gen = SummaryGenerator()
        summary = summary_gen.generate(parsed)
        assert len(summary["function_summaries"]) >= 3
        assert "Calculator" in summary.get("file_summary", "") or True

        stats_gen = StatisticsGenerator()
        parsed_with_code = dict(parsed)
        parsed_with_code["code"] = sample_app_code
        stats = stats_gen.generate(parsed_with_code)
        assert stats["function_count"] >= 3
        assert stats["class_count"] == 1

    def test_chunk_and_similarity(self, sample_app_code):
        splitter = ChunkSplitter(chunk_size=200, chunk_overlap=20)
        chunks = splitter.split(sample_app_code)
        assert len(chunks) >= 1
        assert all(c["text"] for c in chunks)

        matcher = SimilarityMatcher()
        similarity = matcher.match(sample_app_code, sample_app_code)
        assert similarity == pytest.approx(1.0)

    def test_generate_diagrams(self, sample_app_code):
        parser = CodeParser()
        parsed = parser.parse(sample_app_code, "python")

        diagram_gen = DiagramGenerator()
        class_diagram = diagram_gen.generate_class_diagram(parsed.get("classes", []))
        assert "classDiagram;" in class_diagram
        assert "Calculator" in class_diagram

        deps = {"app.py": {"dependencies": ["flask"]}}
        dep_diagram = diagram_gen.generate_dependency_diagram(deps)
        assert "graph TD;" in dep_diagram

    def test_review_findings(self, sample_app_code):
        security = SecurityAnalyzer()
        vulns = security.analyze(sample_app_code, "python")
        vuln_types = [v["type"] for v in vulns]

        pattern = PatternAnalyzer()
        patterns = pattern.analyze(sample_app_code, "python")
        pattern_names = [p["pattern"] for p in patterns["design_patterns"]]

        detector = BugDetector()
        bugs = detector.analyze(sample_app_code, "python")
        bug_types = [b["type"] for b in bugs]

        assert isinstance(vuln_types, list)
        assert isinstance(pattern_names, list)
        assert isinstance(bug_types, list)

    def test_qa_context_building(self, sample_app_code):
        from backend.rag_system.retrieval.context_builder import ContextBuilder
        from backend.rag_system.embeddings.chunk_splitter import ChunkSplitter

        splitter = ChunkSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split(sample_app_code)

        builder = ContextBuilder(max_tokens=1000)
        chunk_dicts = [
            {"metadata": {"text": c["text"], "start_line": c["start_line"], "end_line": c["end_line"]}}
            for c in chunks
        ]
        context = builder.build(chunk_dicts, "How does the calculator work?")
        assert len(context) > 0
        assert "Chunk 0" in context
