import pytest
from backend.code_analysis.generators.summary_generator import SummaryGenerator
from backend.code_analysis.generators.statistics_generator import StatisticsGenerator
from backend.code_analysis.generators.diagram_generator import DiagramGenerator


class TestSummaryGenerator:
    @pytest.fixture
    def gen(self):
        return SummaryGenerator()

    def test_function_summary(self, gen):
        func = {"name": "add", "parameters": ["a", "b"], "return_type": "int", "docstring": "Add two numbers."}
        summary = gen.generate_function_summary(func)
        assert "Function: add" in summary
        assert "Parameters: (a, b)" in summary
        assert "Returns: int" in summary
        assert "Add two numbers" in summary

    def test_function_summary_no_docstring(self, gen):
        func = {"name": "foo", "params": [], "returns": "None"}
        summary = gen.generate_function_summary(func)
        assert "Function: foo" in summary
        assert "Summary:" not in summary

    def test_class_summary(self, gen):
        cls = {
            "name": "Calculator",
            "bases": ["object"],
            "methods": ["add", "subtract"],
            "attributes": ["result"],
            "docstring": "A simple calculator.",
        }
        summary = gen.generate_class_summary(cls)
        assert "Class: Calculator" in summary
        assert "object" in summary
        assert "add" in summary

    def test_class_summary_no_bases(self, gen):
        cls = {"name": "Foo", "methods": [], "attributes": []}
        summary = gen.generate_class_summary(cls)
        assert "Bases: None" in summary

    def test_file_summary(self, gen):
        file_data = {
            "filename": "main.py",
            "language": "python",
            "line_count": 42,
            "functions": [{"name": "main"}],
            "classes": [],
            "imports": ["os", "sys"],
        }
        summary = gen.generate_file_summary(file_data)
        assert "File: main.py" in summary
        assert "python" in summary
        assert "Functions: 1" in summary
        assert "Imports: 2" in summary

    def test_project_summary(self, gen):
        project = {
            "files": {
                "main.py": {"line_count": 10, "functions": [{"name": "main"}], "classes": [], "language": "python"},
                "utils.py": {"line_count": 20, "functions": [{"name": "helper"}], "classes": [{"name": "Util"}], "language": "python"},
            }
        }
        summary = gen.generate_project_summary(project)
        assert "Total Files: 2" in summary
        assert "Total Lines: 30" in summary
        assert "Total Functions: 2" in summary
        assert "Total Classes: 1" in summary

    def test_project_summary_no_files(self, gen):
        summary = gen.generate_project_summary({"files": {}})
        assert "No files found" in summary

    def test_generate_top_level(self, gen):
        parsed = {
            "functions": [{"name": "foo", "parameters": [], "return_type": "None"}],
            "classes": [],
            "language": "python",
            "line_count": 5,
            "filename": "test.py",
        }
        result = gen.generate(parsed)
        assert "function_summaries" in result
        assert "file_summary" in result
        assert len(result["function_summaries"]) == 1


class TestStatisticsGenerator:
    @pytest.fixture
    def gen(self):
        return StatisticsGenerator()

    def test_line_stats_code_only(self, gen):
        parsed = {"code": "def foo():\n    return 1\n", "language": "python"}
        stats = gen.generate_line_stats(parsed)
        assert stats["total"] == 2
        assert stats["code"] == 2
        assert stats["blank"] == 0
        assert stats["comment"] == 0

    def test_line_stats_with_blanks(self, gen):
        parsed = {"code": "def foo():\n\n    return 1\n", "language": "python"}
        stats = gen.generate_line_stats(parsed)
        assert stats["blank"] == 1

    def test_line_stats_with_comments(self, gen):
        parsed = {"code": "# comment\ndef foo():\n    return 1\n", "language": "python"}
        stats = gen.generate_line_stats(parsed)
        assert stats["comment"] == 1

    def test_line_stats_empty_code(self, gen):
        parsed = {"code": "", "language": "python"}
        stats = gen.generate_line_stats(parsed)
        assert stats["total"] == 0

    def test_language_stats(self, gen):
        files = [
            {"language": "python", "lines": 10},
            {"language": "python", "lines": 20},
            {"language": "javascript", "lines": 15},
        ]
        stats = gen.generate_language_stats(files)
        assert stats["python"]["files"] == 2
        assert stats["python"]["lines"] == 30
        assert stats["javascript"]["files"] == 1
        assert stats["javascript"]["lines"] == 15

    def test_generate_top_level(self, gen):
        parsed = {"code": "x = 1", "language": "python", "functions": [], "classes": [], "imports": []}
        result = gen.generate(parsed)
        assert "line_stats" in result
        assert "function_count" in result
        assert "class_count" in result
        assert "import_count" in result

    def test_complexity_stats_empty(self, gen):
        stats = gen.generate_complexity_stats([])
        assert stats["average"] == 0
        assert stats["max"] == 0

    def test_complexity_stats_with_data(self, gen):
        analyses = [{"cyclomatic_complexity": 5}, {"cyclomatic_complexity": 10}, {"cyclomatic_complexity": 15}]
        stats = gen.generate_complexity_stats(analyses)
        assert stats["average"] == 10.0
        assert stats["max"] == 15
        assert stats["min"] == 5


class TestDiagramGenerator:
    @pytest.fixture
    def gen(self):
        return DiagramGenerator()

    def test_class_diagram_basic(self, gen):
        classes = [
            {
                "name": "Car",
                "attributes": [{"name": "color", "type": "str", "visibility": "private"}],
                "methods": [{"name": "drive", "parameters": [], "return_type": "None", "visibility": "public"}],
                "bases": [],
            }
        ]
        output = gen.generate_class_diagram(classes)
        assert "classDiagram;" in output
        assert "class Car" in output
        assert "-color str" in output
        assert "+drive() None" in output

    def test_class_diagram_with_inheritance(self, gen):
        classes = [
            {"name": "SUV", "attributes": [], "methods": [], "bases": ["Car"]},
        ]
        output = gen.generate_class_diagram(classes)
        assert "SUV --|> Car : extends" in output

    def test_class_diagram_simple_attrs(self, gen):
        classes = [
            {"name": "Simple", "attributes": ["x", "y"], "methods": [], "bases": []},
        ]
        output = gen.generate_class_diagram(classes)
        assert "+x" in output
        assert "+y" in output

    def test_flow_diagram_call_graph(self, gen):
        flow = {"call_graph": {"main": ["helper1", "helper2"]}}
        output = gen.generate_flow_diagram(flow)
        assert "flowchart TD;" in output
        assert "main" in output
        assert "helper1" in output
        assert "helper2" in output

    def test_flow_diagram_control_flow(self, gen):
        flow = {
            "control_flow": {
                "nodes": [{"id": 0, "type": "start"}, {"id": 1, "type": "condition", "keyword": "if"}],
                "edges": [{"from": 0, "to": 1, "label": "true"}],
            }
        }
        output = gen.generate_flow_diagram(flow)
        assert "flowchart TD;" in output
        assert "N0" in output
        assert "N1" in output

    def test_dependency_diagram(self, gen):
        deps = {
            "main.py": {"dependencies": ["utils.py"]},
            "utils.py": {"dependencies": []},
        }
        output = gen.generate_dependency_diagram(deps)
        assert "graph TD;" in output
        assert "main" in output or "main_py" in output

    def test_architecture_diagram(self, gen):
        project = {"files": {"src/main.py": {}, "src/utils.py": {}}}
        output = gen.generate_architecture_diagram(project)
        assert "graph TB;" in output
        assert "Project Root" in output

    def test_architecture_diagram_no_data(self, gen):
        output = gen.generate_architecture_diagram({"files": {}})
        assert "No Data" in output
