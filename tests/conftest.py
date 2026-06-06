import pytest


@pytest.fixture
def sample_code():
    return """
def hello(name):
    return f"Hello, {name}!"
"""


@pytest.fixture
def sample_filepath(tmp_path):
    filepath = tmp_path / "sample.py"
    filepath.write_text("def foo():\n    pass\n")
    return str(filepath)
