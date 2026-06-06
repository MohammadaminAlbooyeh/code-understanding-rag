import re


class FlowAnalyzer:
    def __init__(self):
        self.flow_graphs = {}

    def analyze(self, code: str, language: str) -> dict:
        return {
            "call_graph": self.build_call_graph(code, language),
            "control_flow": self.build_control_flow_graph(code, language),
            "execution_paths": self.find_execution_paths(code, language),
        }

    def build_call_graph(self, code: str, language: str) -> dict:
        call_graph = {}
        func_def_pattern = re.compile(
            r"(?:def|function|func)\s+(\w+)\s*\(", re.MULTILINE
        )
        call_pattern = re.compile(r"\b(\w+)\s*\(")

        func_matches = list(func_def_pattern.finditer(code))
        if not func_matches:
            return {}

        for i, fm in enumerate(func_matches):
            func_name = fm.group(1)
            start = fm.end()
            end = (
                func_matches[i + 1].start()
                if i + 1 < len(func_matches)
                else len(code)
            )
            body = code[start:end]

            called_funcs = set()
            for cm in call_pattern.finditer(body):
                called = cm.group(1)
                if called not in (
                    "if",
                    "for",
                    "while",
                    "switch",
                    "catch",
                    "return",
                    "def",
                    "function",
                    "class",
                    "elif",
                    "else",
                    "except",
                    "raise",
                    "yield",
                    "assert",
                    "del",
                    "import",
                    "from",
                    "pass",
                    "break",
                    "continue",
                    "try",
                    "with",
                    "and",
                    "or",
                    "not",
                    "in",
                    "is",
                    "lambda",
                    "print",
                    "len",
                    "range",
                    "type",
                    "int",
                    "str",
                    "float",
                    "list",
                    "dict",
                    "set",
                    "tuple",
                    "super",
                    "self",
                    "null",
                    "None",
                    "true",
                    "false",
                    "True",
                    "False",
                    "undefined",
                ) and called != func_name:
                    called_funcs.add(called)
            call_graph[func_name] = sorted(called_funcs)

        return call_graph

    def build_control_flow_graph(self, code: str, language: str) -> dict:
        lines = code.splitlines()
        nodes = []
        edges = []
        node_id = 0
        block_start = 0
        stack = []

        branch_keywords = re.compile(
            r"\b(?:if|elif|else|for|while|do|switch|case|try|catch|except|finally)\b"
        )

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            indent = len(line) - len(line.lstrip())

            if branch_keywords.search(stripped):
                if i > block_start:
                    nodes.append(
                        {
                            "id": node_id,
                            "type": "block",
                            "lines": f"{block_start + 1}-{i}",
                            "content": "\n".join(lines[block_start:i]),
                        }
                    )
                    if stack:
                        edges.append(
                            {"from": stack[-1]["node"], "to": node_id, "label": ""}
                        )
                    node_id += 1
                nodes.append(
                    {
                        "id": node_id,
                        "type": "branch",
                        "keyword": stripped.split()[0] if stripped else "",
                        "line": i + 1,
                    }
                )
                if stack:
                    edges.append(
                        {"from": stack[-1]["node"], "to": node_id, "label": ""}
                    )
                stack.append({"node": node_id, "indent": indent})
                node_id += 1
                block_start = i + 1

            elif stripped in ("}", ")"):
                while stack and stack[-1]["indent"] >= indent:
                    stack.pop()
                block_start = i + 1

        if block_start < len(lines):
            nodes.append(
                {
                    "id": node_id,
                    "type": "block",
                    "lines": f"{block_start + 1}-{len(lines)}",
                    "content": "\n".join(lines[block_start:]),
                }
            )
            if stack:
                edges.append({"from": stack[-1]["node"], "to": node_id, "label": ""})

        return {"nodes": nodes, "edges": edges}

    def find_execution_paths(self, code: str, language: str) -> list[list[str]]:
        lines = code.splitlines()
        paths = []
        current_path = []
        branch_points = []

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//")):
                continue
            current_path.append(stripped)

            if re.search(r"\b(?:if|elif)\b", stripped):
                branch_points.append(len(current_path) - 1)
            elif re.search(r"\belse\b", stripped):
                pass

        if branch_points:
            for bp in branch_points:
                alt_path = list(current_path)
                alt_path.insert(bp + 1, f"# BRANCH: alternate of line ~{bp + 1}")
                paths.append(alt_path)
            paths.append(current_path)
        else:
            paths.append(current_path)

        if not paths:
            paths = [["(no executable paths detected)"]]

        return [p[:10] for p in paths]
