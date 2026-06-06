import re
import math


class ComplexityAnalyzer:
    def __init__(self):
        self.metrics = {}

    def analyze(self, code: str, language: str) -> dict:
        return {
            "cyclomatic_complexity": self.cyclomatic_complexity(code, language),
            "cognitive_complexity": self.cognitive_complexity(code, language),
            "time_complexity": self.time_complexity(code, language),
            "space_complexity": self.space_complexity(code, language),
            "lines_of_code": len(code.splitlines()),
            "num_functions": self._count_functions(code, language),
            "num_classes": self._count_classes(code, language),
            "num_conditionals": self._count_conditionals(code, language),
            "num_loops": self._count_loops(code, language),
        }

    def _count_functions(self, code: str, language: str) -> int:
        patterns = {
            "python": r"\bdef\s+\w+",
            "javascript": r"(?:function\s+\w+|=>\s*\{)",
            "typescript": r"(?:function\s+\w+|=>\s*\{)",
            "java": r"(?:public|private|protected|static)?\s*\w+\s+\w+\s*\(",
            "go": r"\bfunc\s+\w+",
            "cpp": r"\b\w+\s+\w+\s*\(",
        }
        for key, pat in patterns.items():
            if key in language.lower():
                return len(re.findall(pat, code))
        return len(re.findall(r"\bdef\s+\w+|\bfunction\s+\w+|\bfunc\s+\w+", code))

    def _count_classes(self, code: str, language: str) -> int:
        patterns = {
            "python": r"\bclass\s+\w+",
            "javascript": r"\bclass\s+\w+",
            "typescript": r"\bclass\s+\w+",
            "java": r"\bclass\s+\w+",
            "cpp": r"\bclass\s+\w+",
        }
        for key, pat in patterns.items():
            if key in language.lower():
                return len(re.findall(pat, code))
        return len(re.findall(r"\bclass\s+\w+", code))

    def _count_conditionals(self, code: str, language: str) -> int:
        pattern = r"\b(?:if|elif|else|case|switch|when)\b"
        return len(re.findall(pattern, code))

    def _count_loops(self, code: str, language: str) -> int:
        pattern = r"\b(?:for|while|do)\b"
        return len(re.findall(pattern, code))

    def cyclomatic_complexity(self, code: str, language: str) -> int:
        decision_points = re.findall(
            r"\b(?:if|elif|else|for|while|and|or|case|catch|except)\b", code
        )
        ternary = re.findall(r"\?\s*\:", code)
        logical_ops = re.findall(r"(?:&&|\|\|)", code)
        return len(decision_points) + len(ternary) + len(logical_ops) + 1

    def cognitive_complexity(self, code: str, language: str) -> int:
        lines = code.splitlines()
        complexity = 0
        nesting = 0
        keywords = re.compile(
            r"\b(?:if|elif|else|for|while|case|catch|except|switch)\b"
        )
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//", "/*", "*")):
                continue
            indent = len(line) - len(line.lstrip())
            if keywords.search(stripped):
                current_nesting = indent // 4
                complexity += 1 + current_nesting
            nesting = indent // 4
        return complexity

    def time_complexity(self, code: str, language: str) -> str:
        lines = code.splitlines()
        loop_pattern = re.compile(r"\b(?:for|while|do)\b")

        total_loops = len(loop_pattern.findall(code))
        if total_loops == 0:
            if re.search(r"\bdef\s+\w+.*\w+\(", code):
                func_calls = re.findall(r"\b(\w+)\s*\(", code)
                for call in func_calls:
                    if call in ["recurse"] or call[:3] == "rec":
                        return "O(2^n)"
            return "O(1)"

        loop_lines = [i for i, line in enumerate(lines) if loop_pattern.search(line)]

        nesting_levels = []
        for line_num in loop_lines:
            indent = len(lines[line_num]) - len(lines[line_num].lstrip())
            count = len(loop_pattern.findall(lines[line_num]))
            for other in loop_lines:
                if other == line_num:
                    continue
                other_indent = len(lines[other]) - len(lines[other].lstrip())
                if other_indent > indent:
                    count += 1
            nesting_levels.append(count)

        max_nesting = max(nesting_levels) if nesting_levels else 1
        if max_nesting == 1:
            return "O(n)"
        elif max_nesting == 2:
            return "O(n²)"
        elif max_nesting == 3:
            return "O(n³)"
        else:
            return f"O(n^{max_nesting})"

    def space_complexity(self, code: str, language: str) -> str:
        allocation_patterns = re.findall(
            r"\b(?:new\s+\w+\s*(?:\(|\[)|\[\]|list\s*\(|dict\s*\(|set\s*\(|array|malloc|calloc|vector|ArrayList|HashMap|Map\s*<|List\s*<|Set\s*<)",
            code,
        )
        lines = code.splitlines()
        loop_lines = [i for i, line in enumerate(lines) if re.search(r"\b(?:for|while)\b", line)]
        nested_alloc = False
        for i in loop_lines:
            for j in loop_lines:
                if j > i:
                    nested_alloc = True
                    break
            if nested_alloc:
                break
        if nested_alloc:
            return "O(n²)"
        if len(allocation_patterns) > 3:
            return "O(n)"
        if allocation_patterns:
            return "O(n)"
        return "O(1)"
