import ast
import re


class ClassExtractor:
    def __init__(self):
        self.classes = []

    def extract(self, code: str, language: str) -> list[dict]:
        if language == "python":
            return self._extract_python_classes(code)
        return self._extract_regex_classes(code, language)

    def extract_from_file(self, filepath: str) -> list[dict]:
        with open(filepath, "r") as f:
            code = f.read()
        import os
        ext = os.path.splitext(filepath)[1]
        lang_map = {".py": "python", ".js": "javascript", ".ts": "typescript",
                     ".jsx": "javascript", ".tsx": "typescript", ".java": "java",
                     ".go": "go", ".cpp": "cpp", ".rs": "rust"}
        language = lang_map.get(ext, "unknown")
        return self.extract(code, language)

    def get_class_details(self, class_name: str, code: str, language: str) -> dict:
        classes = self.extract(code, language)
        for cls in classes:
            if cls.get("name") == class_name:
                return cls
        return {"error": f"Class {class_name} not found"}

    def _extract_python_classes(self, code: str) -> list[dict]:
        classes = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = []
                    attributes = []
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            methods.append({
                                "name": item.name,
                                "type": "async" if isinstance(item, ast.AsyncFunctionDef) else "method",
                                "lineno": item.lineno,
                                "args": [a.arg for a in item.args.args],
                                "decorators": [self._decorator_name(d) for d in item.decorator_list],
                                "docstring": ast.get_docstring(item) or "",
                            })
                        elif isinstance(item, (ast.Assign, ast.AnnAssign)):
                            target = item.target if isinstance(item, ast.Assign) else item.target
                            if isinstance(target, ast.Name):
                                attributes.append({
                                    "name": target.id,
                                    "lineno": item.lineno,
                                })

                    cls_info = {
                        "name": node.name,
                        "lineno": node.lineno,
                        "end_lineno": node.end_lineno,
                        "bases": [self._base_name(b) for b in node.bases],
                        "decorators": [self._decorator_name(d) for d in node.decorator_list],
                        "docstring": ast.get_docstring(node) or "",
                        "methods": methods,
                        "attributes": attributes,
                        "method_count": len(methods),
                        "source": ast.get_source_segment(code, node) or "",
                    }
                    classes.append(cls_info)
        except SyntaxError:
            pass
        return classes

    def _base_name(self, base) -> str:
        if isinstance(base, ast.Name):
            return base.id
        if isinstance(base, ast.Attribute):
            return f"{self._base_name(base.value)}.{base.attr}"
        if isinstance(base, ast.Call):
            return self._base_name(base.func)
        return str(base)

    def _decorator_name(self, decorator) -> str:
        if isinstance(decorator, ast.Name):
            return decorator.id
        if isinstance(decorator, ast.Call):
            return self._decorator_name(decorator.func)
        if isinstance(decorator, ast.Attribute):
            return f"{self._decorator_name(decorator.value)}.{decorator.attr}"
        return str(decorator)

    def _extract_regex_classes(self, code: str, language: str) -> list[dict]:
        classes = []
        patterns = {
            "python": r"class\s+(\w+)\s*(?:\(([^)]*)\))?\s*:",
            "java": r"(?:public|private|protected|static|abstract|final|\s)*\s*class\s+(\w+)(?:\s*extends\s+(\w+))?(?:\s*implements\s+([^{]+))?\s*\{",
            "typescript": r"(?:export\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s*extends\s+(\w+))?(?:\s*implements\s+([^{]+))?\s*\{",
            "javascript": r"class\s+(\w+)(?:\s*extends\s+(\w+))?\s*\{",
            "cpp": r"class\s+(\w+)(?:\s*:\s*(?:public|private|protected)\s+(\w+))?\s*\{",
        }
        pattern = patterns.get(language)
        if not pattern:
            return classes
        for match in re.finditer(pattern, code, re.MULTILINE):
            cls_info = {
                "name": match.group(1),
                "lineno": code[:match.start()].count("\n") + 1,
                "bases": [],
            }
            if match.lastindex and match.lastindex >= 2 and match.group(2):
                cls_info["bases"].append(match.group(2).strip())
            classes.append(cls_info)
        return classes
