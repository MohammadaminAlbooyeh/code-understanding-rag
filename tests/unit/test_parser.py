import pytest
from backend.code_analysis.parser.code_parser import CodeParser


def test_parse_python():
    parser = CodeParser()
    code = "def foo():\n    pass\n"
    result = parser.parse(code, "python")
    assert result is not None


def test_parse_file(sample_filepath):
    parser = CodeParser()
    result = parser.parse_file(sample_filepath)
    assert result is not None
