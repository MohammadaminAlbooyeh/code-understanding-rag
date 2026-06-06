# Parser Guide

The code parser extracts structural information from source code including:

- Abstract Syntax Trees (AST)
- Functions and their signatures
- Classes and their methods
- Import statements
- Docstrings and comments

## Usage

```python
from backend.code_analysis.parser.code_parser import CodeParser

parser = CodeParser()
result = parser.parse(code, "python")
```
