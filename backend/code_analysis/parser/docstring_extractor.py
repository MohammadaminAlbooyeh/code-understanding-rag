import ast
import re


class DocstringExtractor:
    def __init__(self):
        self.docstrings = []

    def extract(self, code: str, language: str) -> list[dict]:
        if language == "python":
            return self._extract_python_docstrings(code)
        return self._extract_comment_docstrings(code, language)

    def extract_from_file(self, filepath: str) -> list[dict]:
        with open(filepath, "r") as f:
            code = f.read()
        import os
        ext = os.path.splitext(filepath)[1]
        lang_map = {".py": "python", ".js": "javascript", ".ts": "typescript",
                     ".java": "java", ".go": "go", ".cpp": "cpp", ".rs": "rust"}
        language = lang_map.get(ext, "unknown")
        return self.extract(code, language)

    def format_docstring(self, docstring: str, format_type: str = "markdown") -> str:
        if format_type == "markdown":
            return self._to_markdown(docstring)
        elif format_type == "html":
            return self._to_html(docstring)
        elif format_type == "rst":
            return self._to_rst(docstring)
        return docstring

    def _extract_python_docstrings(self, code: str) -> list[dict]:
        docstrings = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if not isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    continue
                doc = ast.get_docstring(node)
                if doc:
                    info = {
                        "type": type(node).__name__,
                        "lineno": node.lineno,
                        "docstring": doc,
                        "length": len(doc),
                    }
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        info["name"] = node.name
                        info["parent"] = "function"
                    elif isinstance(node, ast.ClassDef):
                        info["name"] = node.name
                        info["parent"] = "class"
                    elif isinstance(node, ast.Module):
                        info["name"] = "module"
                        info["parent"] = "module"
                    docstrings.append(info)
        except SyntaxError:
            pass
        return docstrings

    def _extract_comment_docstrings(self, code: str, language: str) -> list[dict]:
        docstrings = []
        if language in ("javascript", "typescript", "java", "cpp"):
            jsdoc_pattern = r"/\*\*([^*]|\*(?!/))*\*/"
            for match in re.finditer(jsdoc_pattern, code, re.DOTALL):
                text = match.group(0)
                lines_before = code[:match.start()].strip().split("\n")
                context = lines_before[-1] if lines_before else ""

                cleaned = re.sub(r'^\s*\*\s?', '', text.strip("/**/"), flags=re.MULTILINE)
                docstrings.append({
                    "type": "comment",
                    "lineno": code[:match.start()].count("\n") + 1,
                    "docstring": cleaned.strip(),
                    "language": language,
                    "context": context,
                })
        elif language == "go":
            for match in re.finditer(r"//\s*(.+)", code):
                docstrings.append({
                    "type": "comment",
                    "lineno": code[:match.start()].count("\n") + 1,
                    "docstring": match.group(1).strip(),
                    "language": language,
                })
        return docstrings

    def _to_markdown(self, docstring: str) -> str:
        lines = docstring.split("\n")
        md_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith(":param"):
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    param_info = parts[2].strip()
                    param_name = parts[1].replace("param ", "").strip()
                    md_lines.append(f"- `{param_name}`: {param_info}")
            elif line.startswith(":return"):
                md_lines.append(f"**Returns:** {line.split(':', 1)[1].strip()}")
            elif line.startswith(":raises") or line.startswith(":raise"):
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    md_lines.append(f"- ⚠️ `{parts[1].strip()}`: {parts[2].strip()}")
            else:
                md_lines.append(line)
        return "\n".join(md_lines)

    def _to_html(self, docstring: str) -> str:
        md = self._to_markdown(docstring)
        import re
        html = md.replace("**", "<strong>", 1)
        # basic conversion
        html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
        html = html.replace("\n", "<br>")
        return f"<div class=\"docstring\">{html}</div>"

    def _to_rst(self, docstring: str) -> str:
        return docstring
