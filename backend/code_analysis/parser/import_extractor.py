import ast
import re


class ImportExtractor:
    def __init__(self):
        self.imports = []

    def extract(self, code: str, language: str) -> list[dict]:
        if language == "python":
            return self._extract_python_imports(code)
        return self._extract_regex_imports(code, language)

    def get_dependency_tree(self, imports: list[dict]) -> dict:
        tree = {}
        for imp in imports:
            module = imp.get("module", "")
            parts = module.split(".")
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
            if imp.get("names"):
                for name in imp["names"]:
                    if isinstance(name, dict):
                        key = name.get("name", "")
                    else:
                        key = name
                    if key not in current:
                        current[key] = None
        return tree

    def _extract_python_imports(self, code: str) -> list[dict]:
        imports = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({
                            "type": "import",
                            "module": alias.name,
                            "alias": alias.asname,
                            "lineno": node.lineno,
                        })
                elif isinstance(node, ast.ImportFrom):
                    names = []
                    for alias in node.names:
                        names.append({
                            "name": alias.name,
                            "alias": alias.asname,
                        })
                    imports.append({
                        "type": "from",
                        "module": node.module or "",
                        "names": names,
                        "level": node.level,
                        "lineno": node.lineno,
                    })
        except SyntaxError:
            imports = self._extract_regex_imports(code, "python")
        return imports

    def _extract_regex_imports(self, code: str, language: str) -> list[dict]:
        imports = []
        patterns = {
            "python": [
                r"^import\s+(\S+(?:\s*,\s*\S+)*)",
                r"^from\s+(\S+)\s+import\s+(.+)",
            ],
            "javascript": [
                r"(?:import|export)\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
                r"(?:const|let|var)\s+.*?=\s*require\s*\(['\"]([^'\"]+)['\"]\)",
            ],
            "typescript": [
                r"(?:import|export)\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
                r"(?:import|export)\s+type\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
            ],
            "java": [
                r"^import\s+(?:static\s+)?([^;]+);",
            ],
            "go": [
                r"\"([^\"]+)\"",
            ],
            "cpp": [
                r"#include\s+[<\"]([^>\"]+)[>\"]",
            ],
        }
        lang_patterns = patterns.get(language, [])
        for pattern in lang_patterns:
            for match in re.finditer(pattern, code, re.MULTILINE):
                imports.append({
                    "type": "import",
                    "module": match.group(1).strip(),
                    "language": language,
                    "lineno": code[:match.start()].count("\n") + 1,
                })
        return imports
