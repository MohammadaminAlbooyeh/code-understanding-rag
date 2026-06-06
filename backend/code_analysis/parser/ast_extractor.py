import ast
import importlib
import re
import os

from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

try:
    import tree_sitter
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    tree_sitter = None

_LANGUAGE_QUERIES = {
    "python": """
        (function_definition) @function
        (class_definition) @class
        (call) @call
        (assignment) @assignment
        (if_statement) @if
        (for_statement) @for
        (while_statement) @while
    """,
}

_LANGUAGE_PARSERS = {}


def _get_parser(language: str):
    if not TREE_SITTER_AVAILABLE:
        return None
    if language in _LANGUAGE_PARSERS:
        return _LANGUAGE_PARSERS[language]
    try:
        lang_module = importlib.import_module(f"tree_sitter_{language}")
        parser = tree_sitter.Parser()
        parser.set_language(lang_module.language())
        _LANGUAGE_PARSERS[language] = parser
    except Exception:
        _LANGUAGE_PARSERS[language] = None
        logger.warning(f"Tree-sitter parser not available for {language}")
    return _LANGUAGE_PARSERS[language]


class ASTExtractor:
    def __init__(self):
        self.supported_languages = ["python", "javascript", "typescript", "java", "go", "cpp"]

    def extract(self, code: str, language: str) -> dict:
        if language == "python":
            return self._extract_python_ast(code)
        ts_parser = _get_parser(language)
        if ts_parser:
            try:
                return self._extract_tree_sitter_ast(code, language)
            except Exception as e:
                logger.warning(f"Tree-sitter extraction failed for {language}: {e}")
        return self._regex_fallback_ast(code, language)

    def extract_from_file(self, filepath: str) -> dict:
        with open(filepath, "r") as f:
            code = f.read()
        language = self._detect_language(filepath)
        return self.extract(code, language)

    def get_ast_tree(self, code: str, language: str) -> str:
        if language == "python":
            try:
                tree = ast.parse(code)
                return ast.dump(tree, indent=2)
            except SyntaxError as e:
                return f"Syntax error: {e}"
        return "AST tree output only supported for Python"

    def _detect_language(self, filepath: str) -> str:
        ext_map = {
            ".py": "python", ".js": "javascript", ".jsx": "javascript",
            ".ts": "typescript", ".tsx": "typescript", ".java": "java",
            ".go": "go", ".cpp": "cpp", ".c": "cpp", ".rs": "rust",
        }
        import os
        ext = os.path.splitext(filepath)[1]
        return ext_map.get(ext, "unknown")

    def _extract_python_ast(self, code: str) -> dict:
        try:
            tree = ast.parse(code)
            result = {
                "type": "Module",
                "language": "python",
                "body": [],
                "errors": [],
            }
            for node in ast.iter_child_nodes(tree):
                child = self._python_node_to_dict(node)
                if child:
                    result["body"].append(child)
            return result
        except SyntaxError as e:
            return {"type": "Module", "language": "python", "body": [], "errors": [str(e)]}

    def _python_node_to_dict(self, node) -> dict:
        node_type = type(node).__name__
        info = {"type": node_type, "lineno": getattr(node, "lineno", None)}

        if isinstance(node, ast.FunctionDef):
            info["name"] = node.name
            info["args"] = [a.arg for a in node.args.args]
            info["decorators"] = [self._python_node_to_dict(d) for d in node.decorator_list]
            info["body"] = [self._python_node_to_dict(n) for n in ast.iter_child_nodes(node)]
        elif isinstance(node, ast.AsyncFunctionDef):
            info["name"] = node.name
            info["args"] = [a.arg for a in node.args.args]
            info["decorators"] = [self._python_node_to_dict(d) for d in node.decorator_list]
            info["body"] = [self._python_node_to_dict(n) for n in ast.iter_child_nodes(node)]
        elif isinstance(node, ast.ClassDef):
            info["name"] = node.name
            info["bases"] = [self._python_node_to_dict(b) for b in node.bases]
            info["decorators"] = [self._python_node_to_dict(d) for d in node.decorator_list]
            info["body"] = [self._python_node_to_dict(n) for n in ast.iter_child_nodes(node)]
        elif isinstance(node, ast.Assign):
            info["targets"] = [self._python_node_to_dict(t) for t in node.targets]
            info["value"] = self._python_node_to_dict(node.value)
        elif isinstance(node, ast.Import):
            info["names"] = [{"name": alias.name, "asname": alias.asname} for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            info["module"] = node.module
            info["names"] = [{"name": alias.name, "asname": alias.asname} for alias in node.names]
        elif isinstance(node, (ast.Expr,)):
            if hasattr(node, "value"):
                info["value"] = self._python_node_to_dict(node.value)
        elif isinstance(node, (ast.Return,)):
            if hasattr(node, "value") and node.value:
                info["value"] = self._python_node_to_dict(node.value)
        elif isinstance(node, ast.If):
            info["test"] = self._python_node_to_dict(node.test)
            info["body"] = [self._python_node_to_dict(n) for n in node.body]
            info["orelse"] = [self._python_node_to_dict(n) for n in node.orelse]
        elif isinstance(node, ast.For):
            info["target"] = self._python_node_to_dict(node.target)
            info["iter"] = self._python_node_to_dict(node.iter)
            info["body"] = [self._python_node_to_dict(n) for n in node.body]
        elif isinstance(node, ast.While):
            info["test"] = self._python_node_to_dict(node.test)
            info["body"] = [self._python_node_to_dict(n) for n in node.body]
        elif isinstance(node, ast.Try):
            info["body"] = [self._python_node_to_dict(n) for n in node.body]
            info["handlers"] = [self._python_node_to_dict(h) for h in node.handlers]
            info["finalbody"] = [self._python_node_to_dict(n) for n in node.finalbody]
        elif isinstance(node, ast.Name):
            info["id"] = node.id
        elif isinstance(node, ast.Constant):
            info["value"] = repr(node.value)
        elif isinstance(node, ast.Call):
            info["func"] = self._python_node_to_dict(node.func)
            info["args"] = [self._python_node_to_dict(a) for a in node.args]
        elif isinstance(node, ast.Attribute):
            info["attr"] = node.attr
            info["value"] = self._python_node_to_dict(node.value)
        elif isinstance(node, ast.Subscript):
            info["value"] = self._python_node_to_dict(node.value)
            info["slice"] = self._python_node_to_dict(node.slice)
        elif isinstance(node, ast.List):
            info["elts"] = [self._python_node_to_dict(e) for e in node.elts]
        elif isinstance(node, ast.Dict):
            info["keys"] = [self._python_node_to_dict(k) for k in node.keys]
            info["values"] = [self._python_node_to_dict(v) for v in node.values]
        elif isinstance(node, ast.Lambda):
            info["args"] = [a.arg for a in node.args.args]
            info["body"] = self._python_node_to_dict(node.body)
        elif isinstance(node, ast.Starred):
            info["value"] = self._python_node_to_dict(node.value)
        else:
            info["_summary"] = ast.dump(node, annotate_fields=False)[:80]
        return info

    def _extract_tree_sitter_ast(self, code: str, language: str) -> dict:
        parser = _get_parser(language)
        if not parser:
            return self._regex_fallback_ast(code, language)
        tree = parser.parse(bytes(code, "utf8"))
        root = tree.root_node
        return self._ts_node_to_dict(root, code)

    def _ts_node_to_dict(self, node, code: str) -> dict:
        result = {
            "type": node.type,
            "start": (node.start_point[0], node.start_point[1]),
            "end": (node.end_point[0], node.end_point[1]),
        }
        if node.type in ("function_definition", "method_definition"):
            name_node = node.child_by_field_name("name")
            if name_node:
                result["name"] = code[name_node.start_byte:name_node.end_byte]
        elif node.type in ("class_definition",):
            name_node = node.child_by_field_name("name")
            if name_node:
                result["name"] = code[name_node.start_byte:name_node.end_byte]
        if node.children:
            result["children"] = []
            for child in node.children:
                child_dict = self._ts_node_to_dict(child, code)
                if child_dict:
                    result["children"].append(child_dict)
        else:
            result["text"] = code[node.start_byte:node.end_byte][:100]
        return result

    def _regex_fallback_ast(self, code: str, language: str) -> dict:
        result = {
            "type": "Module",
            "language": language,
            "body": [],
            "source": "regex_fallback",
        }
        func_pattern = r"(?:def|function|func|fn)\s+(\w+)\s*\("
        class_pattern = r"(?:class|struct|interface)\s+(\w+)"
        import_patterns = {
            "python": r"(?:import|from)\s+(\w+)",
            "javascript": r"(?:import|require)\s+\(?['\"]?(\w+)",
            "typescript": r"(?:import|require)\s+\(?['\"]?(\w+)",
            "java": r"import\s+([\w.]+)",
            "go": r"(?:import|package)\s+([\w./\"\"]+)",
        }
        for m in re.finditer(func_pattern, code, re.MULTILINE):
            result["body"].append({"type": "Function", "name": m.group(1), "line": code[:m.start()].count("\n") + 1})
        for m in re.finditer(class_pattern, code, re.MULTILINE):
            result["body"].append({"type": "Class", "name": m.group(1), "line": code[:m.start()].count("\n") + 1})
        impat = import_patterns.get(language, r"(?:import|from|include)\s+(\w+)")
        for m in re.finditer(impat, code, re.MULTILINE):
            result["body"].append({"type": "Import", "name": m.group(1), "line": code[:m.start()].count("\n") + 1})
        return result



