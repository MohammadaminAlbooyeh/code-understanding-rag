import ast
import re


class FunctionExtractor:
    def __init__(self):
        self.functions = []

    def extract(self, code: str, language: str) -> list[dict]:
        if language == "python":
            return self._extract_python_functions(code)
        return self._extract_regex_functions(code, language)

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

    def get_function_details(self, func_name: str, code: str, language: str) -> dict:
        functions = self.extract(code, language)
        for func in functions:
            if func.get("name") == func_name:
                return func
        return {"error": f"Function {func_name} not found"}

    def _extract_python_functions(self, code: str) -> list[dict]:
        functions = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func = {
                        "name": node.name,
                        "type": "async" if isinstance(node, ast.AsyncFunctionDef) else "function",
                        "lineno": node.lineno,
                        "end_lineno": node.end_lineno,
                        "args": [a.arg for a in node.args.args],
                        "defaults": len(node.args.defaults),
                        "decorators": [self._decorator_name(d) for d in node.decorator_list],
                        "returns": self._get_return_annotation(node),
                        "docstring": ast.get_docstring(node) or "",
                        "body_lines": len(node.body),
                        "source": ast.get_source_segment(code, node) or "",
                    }
                    functions.append(func)
        except SyntaxError:
            functions = self._extract_regex_functions(code, "python")
        return functions

    def _decorator_name(self, decorator) -> str:
        if isinstance(decorator, ast.Name):
            return decorator.id
        if isinstance(decorator, ast.Call):
            return self._decorator_name(decorator.func)
        if isinstance(decorator, ast.Attribute):
            return f"{self._decorator_name(decorator.value)}.{decorator.attr}"
        return str(decorator)

    def _get_return_annotation(self, node) -> str:
        if node.returns:
            if isinstance(node.returns, ast.Name):
                return node.returns.id
            if isinstance(node.returns, ast.Subscript):
                return f"{self._decorator_name(node.returns.value)}[{self._decorator_name(node.returns.slice)}]"
            if isinstance(node.returns, ast.Constant):
                return str(node.returns.value)
            return ast.dump(node.returns)
        return ""

    def _extract_regex_functions(self, code: str, language: str) -> list[dict]:
        functions = []
        patterns = {
            "python": r"(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^:]+))?\s*:",
            "javascript": r"(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)",
            "typescript": r"(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)\s*(?::\s*([^{]+))?",
            "java": r"(?:public|private|protected|static|\s)*\s+(\w+(?:\[\])?)\s+(\w+)\s*\(([^)]*)\)\s*(?:throws\s+\w+)?\s*\{",
            "go": r"func\s+(\w+)\s*\(([^)]*)\)\s*(?:\s*(\w+(?:\[\])?))?\s*\{",
        }
        pattern = patterns.get(language, r"(\w+)\s*=\s*(?:function|def)\s*\(([^)]*)\)")
        for match in re.finditer(pattern, code, re.MULTILINE):
            func = {
                "name": match.group(1),
                "lineno": code[:match.start()].count("\n") + 1,
                "args": [a.strip() for a in match.group(2).split(",") if a.strip()],
                "signature": match.group(0).strip(),
            }
            if language in ("typescript", "java") and match.lastindex >= 3:
                func["return_type"] = match.group(3).strip() if match.group(3) else ""
            functions.append(func)
        return functions
