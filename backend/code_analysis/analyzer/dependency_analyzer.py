import re
import os


class DependencyAnalyzer:
    def __init__(self):
        self.dependencies = {}

    def analyze(self, code: str, language: str) -> dict:
        imports = self._extract_imports(code, language)
        exports = self._extract_exports(code, language)
        return {
            "imports": imports,
            "exports": exports,
            "dependencies": [imp["module"] for imp in imports],
            "dependents_count": len(exports),
        }

    def _extract_imports(self, code: str, language: str) -> list[dict]:
        imports = []
        lang = language.lower()

        if "python" in lang:
            for m in re.finditer(r"^import\s+(\S+)", code, re.MULTILINE):
                imports.append({"module": m.group(1), "type": "import"})
            for m in re.finditer(r"^from\s+(\S+)\s+import\s+(.+)", code, re.MULTILINE):
                for name in m.group(2).split(","):
                    imports.append(
                        {
                            "module": m.group(1),
                            "name": name.strip().split()[0] if name.strip() else "",
                            "type": "from_import",
                        }
                    )

        elif "javascript" in lang or "typescript" in lang or "js" in lang or "ts" in lang:
            for m in re.finditer(
                r"(?:import\s+(?:\w+\s*,?\s*)?(?:\{[^}]*\})?\s*from\s+['\"]([^'\"]+)['\"]|const\s+\w+\s*=\s*require\s*\(\s*['\"]([^'\"]+)['\"]\s*\))",
                code,
            ):
                module = m.group(1) or m.group(2)
                imports.append({"module": module, "type": "import"})

        elif "java" in lang:
            for m in re.finditer(r"^import\s+([\w.]+)", code, re.MULTILINE):
                imports.append({"module": m.group(1), "type": "import"})

        elif "go" in lang:
            for m in re.finditer(r'import\s+["\'](\S+)["\']', code):
                imports.append({"module": m.group(1), "type": "import"})

        elif "cpp" in lang or "c++" in lang or "c" in lang:
            for m in re.finditer(r'#include\s+[<"]([^>"]+)[>"]', code):
                imports.append({"module": m.group(1), "type": "include"})

        else:
            for m in re.finditer(
                r"\b(?:import|require|include)\s+[\"']?([\w./-]+)", code
            ):
                imports.append({"module": m.group(1), "type": "import"})

        return imports

    def _extract_exports(self, code: str, language: str) -> list[dict]:
        exports = []
        lang = language.lower()

        if "python" in lang:
            for m in re.finditer(r"^(?:def|class)\s+(\w+)", code, re.MULTILINE):
                exports.append({"name": m.group(1), "type": "definition"})

        elif "javascript" in lang or "typescript" in lang or "js" in lang or "ts" in lang:
            for m in re.finditer(
                r"\b(?:export\s+(?:default\s+)?(?:function|class|const|let|var)\s+(\w+)|module\.exports\s*=|exports\.(\w+))",
                code,
            ):
                name = m.group(1) or m.group(2)
                if name:
                    exports.append({"name": name, "type": "export"})

        elif "java" in lang:
            for m in re.finditer(
                r"(?:public|private|protected)?\s*(?:static\s+)?(?:class|interface|enum)\s+(\w+)",
                code,
            ):
                exports.append({"name": m.group(1), "type": "class"})

        elif "go" in lang:
            for m in re.finditer(
                r"^func\s+(\w+)|^type\s+(\w+)\s", code, re.MULTILINE
            ):
                name = m.group(1) or m.group(2)
                if name and name[0].isupper():
                    exports.append({"name": name, "type": "export"})

        return exports

    def analyze_directory(self, directory: str) -> dict:
        combined = {}
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                lang_map = {
                    ".py": "python",
                    ".js": "javascript",
                    ".jsx": "javascript",
                    ".ts": "typescript",
                    ".tsx": "typescript",
                    ".java": "java",
                    ".go": "go",
                    ".cpp": "cpp",
                    ".c": "c",
                    ".h": "cpp",
                    ".hpp": "cpp",
                    ".rb": "ruby",
                    ".rs": "rust",
                    ".php": "php",
                    ".swift": "swift",
                }
                if ext not in lang_map:
                    continue
                filepath = os.path.join(root, fname)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()
                except Exception:
                    continue
                relpath = os.path.relpath(filepath, directory)
                combined[relpath] = self.analyze(code, lang_map[ext])
        return combined

    def build_dependency_graph(self, dependencies: dict) -> dict:
        nodes = set()
        edges = []
        for module, info in dependencies.items():
            nodes.add(module)
            for dep in info.get("dependencies", []):
                dep_name = dep
                if dep_name.startswith("."):
                    base = os.path.dirname(module)
                    dep_name = os.path.normpath(os.path.join(base, dep_name))
                edges.append({"source": module, "target": dep_name})
                nodes.add(dep_name)
        return {
            "nodes": [{"id": n} for n in sorted(nodes)],
            "edges": edges,
        }

    def find_circular_dependencies(self, dependencies: dict) -> list[list[str]]:
        graph = {}
        for module, info in dependencies.items():
            graph[module] = info.get("dependencies", [])
        cycles = []
        visited = set()
        path = []

        def dfs(node):
            if node in path:
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(list(cycle))
                return
            if node in visited:
                return
            visited.add(node)
            path.append(node)
            for neighbor in graph.get(node, []):
                dfs(neighbor)
            path.pop()

        for module in list(graph.keys()):
            dfs(module)
        return cycles
