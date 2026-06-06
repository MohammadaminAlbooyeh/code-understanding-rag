import pytest
from backend.code_analysis.parser.code_parser import CodeParser
from backend.code_analysis.utils.language_detector import LanguageDetector


@pytest.fixture
def parser():
    return CodeParser()


def test_parse_python_functions(parser):
    code = "def foo():\n    pass\n"
    result = parser.parse(code, "python")
    assert result["language"] == "python"
    assert len(result["functions"]) == 1
    assert result["functions"][0]["name"] == "foo"
    assert result["line_count"] == 3


def test_parse_python_class(parser):
    code = """
class MyClass:
    def method(self):
        pass
"""
    result = parser.parse(code, "python")
    assert len(result["classes"]) == 1
    assert result["classes"][0]["name"] == "MyClass"
    assert len(result["classes"][0]["methods"]) == 1


def test_parse_python_imports(parser):
    code = "import os\nfrom sys import path\n"
    result = parser.parse(code, "python")
    assert len(result["imports"]) >= 2


def test_parse_javascript(parser):
    code = "function greet(name) {\n    return `Hello ${name}`;\n}\n"
    result = parser.parse(code, "javascript")
    assert result["language"] == "javascript"
    assert len(result["functions"]) >= 1


def test_parse_empty_string(parser):
    result = parser.parse("", "python")
    assert result["language"] == "python"
    assert result["line_count"] == 1
    assert result["char_count"] == 0


def test_parse_single_line(parser):
    result = parser.parse("x = 1", "python")
    assert result["line_count"] == 1


def test_parse_syntax_error(parser):
    code = "def broken(\n"
    result = parser.parse(code, "python")
    assert result["language"] == "python"
    assert "line_count" in result


def test_parse_file(sample_filepath, parser):
    result = parser.parse_file(sample_filepath)
    assert result is not None
    assert "language" in result
    assert "functions" in result


def test_parse_file_with_imports(parser, tmp_path):
    filepath = tmp_path / "utils.py"
    filepath.write_text("import json\n\ndef load(path):\n    return json.load(open(path))\n")
    result = parser.parse_file(str(filepath))
    assert len(result["functions"]) == 1
    assert len(result["imports"]) > 0


def test_language_detection_from_extension():
    detector = LanguageDetector()
    assert detector.detect_from_extension("main.py") == "python"
    assert detector.detect_from_extension("app.js") == "javascript"
    assert detector.detect_from_extension("component.tsx") == "typescript"
    assert detector.detect_from_extension("Main.java") == "java"
    assert detector.detect_from_extension("main.go") == "go"
    assert detector.detect_from_extension("unknown.txt") == "unknown"


def test_language_detection_from_content():
    detector = LanguageDetector()
    py_code = "def hello():\n    print('hi')\n"
    js_code = "function hello() {\n  console.log('hi');\n}\n"
    assert detector.detect_from_content(py_code) == "python"
    assert detector.detect_from_content(js_code) == "javascript"


def test_language_detection_with_filename(detector=LanguageDetector()):
    code = "def hello():\n    pass\n"
    assert detector.detect(code, "test.py") == "python"
    assert detector.detect(code, "test.js") == "javascript"


def test_language_detection_unknown():
    detector = LanguageDetector()
    assert detector.detect_from_extension("readme.md") == "unknown"


def test_parse_directory(parser, tmp_path):
    sub = tmp_path / "subdir"
    sub.mkdir()
    (sub / "a.py").write_text("def a(): pass\n")
    (sub / "b.js").write_text("function b() {}\n")
    results = parser.parse_directory(str(sub))
    assert len(results) == 2
    langs = {r["language"] for r in results}
    assert "python" in langs
    assert "javascript" in langs
