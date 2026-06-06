import re


class PatternAnalyzer:
    def __init__(self):
        self.patterns = {}

    def analyze(self, code: str, language: str) -> dict:
        return {
            "design_patterns": self.detect_design_patterns(code, language),
            "anti_patterns": self.detect_anti_patterns(code, language),
            "code_smells": self.detect_code_smells(code, language),
        }

    def detect_design_patterns(self, code: str, language: str) -> list[dict]:
        patterns = []
        lang = language.lower()

        if re.search(r"__new__|_instance\s*=|getInstance\s*\(", code) or re.search(
            r"private\s+static\s+\w+\s+instance", code
        ):
            patterns.append(
                {
                    "pattern": "Singleton",
                    "confidence": "medium",
                    "evidence": "Private constructor or _instance/instance variable detected",
                }
            )

        if re.search(
            r"\b(?:create|build|factory|make)_?(?:instance|object|widget|element|node)?\s*\(",
            code,
        ):
            factory_matches = re.findall(
                r"\b(?:create|build|factory|make)_?(?:instance|object|widget|element|node)?\s*\(",
                code,
            )
            patterns.append(
                {
                    "pattern": "Factory",
                    "confidence": "medium",
                    "evidence": f"Factory method{'s' if len(factory_matches) > 1 else ''} detected: {', '.join(m.strip('(') for m in factory_matches)}",
                }
            )

        if re.search(
            r"\b(?:subscribe|notify|emit|on|addEventListener|dispatch|publish|listen)\s*\(",
            code,
        ):
            obs_matches = re.findall(
                r"\b(?:subscribe|notify|emit|on|addEventListener|dispatch|publish|listen)\s*\(",
                code,
            )
            patterns.append(
                {
                    "pattern": "Observer",
                    "confidence": "medium",
                    "evidence": f"Observer pattern detected: {', '.join(m.strip('(') for m in obs_matches[:3])}",
                }
            )

        if lang in ("python",) and re.search(r"^@\w+", code, re.MULTILINE):
            decorators = re.findall(r"^@(\w+)", code, re.MULTILINE)
            patterns.append(
                {
                    "pattern": "Decorator",
                    "confidence": "high" if len(decorators) > 1 else "medium",
                    "evidence": f"Decorator{'s' if len(decorators) > 1 else ''} detected: {', '.join(decorators)}",
                }
            )

        has_interface = bool(
            re.search(r"(?:interface|ABC|abstract\s+class|protocol)\s+\w+", code)
        )
        has_multiple_impl = len(
            re.findall(r"class\s+\w+.*\(.*\w+.*\):", code)
        ) > 1 or len(
            re.findall(
                r"class\s+\w+\s+(?:extends|implements)\s+\w+", code
            )
        ) > 1
        if has_interface and has_multiple_impl:
            patterns.append(
                {
                    "pattern": "Strategy",
                    "confidence": "medium",
                    "evidence": "Interface/abstract class with multiple implementations detected",
                }
            )

        return patterns

    def detect_anti_patterns(self, code: str, language: str) -> list[dict]:
        anti_patterns = []
        lines = code.splitlines()

        func_defs = list(re.finditer(r"^\s*(?:def|function|func)\s+\w+", code, re.MULTILINE))
        class_defs = list(re.finditer(r"^\s*class\s+\w+", code, re.MULTILINE))

        for cd in class_defs:
            class_start = cd.start()
            class_end = len(code)
            for nd in class_defs:
                if nd.start() > class_start:
                    class_end = nd.start()
                    break
            class_body = code[class_start:class_end]
            methods_in_class = len(
                re.findall(
                    r"^\s+(?:def|function|async\s+def)\s+\w+", class_body, re.MULTILINE
                )
            )
            if methods_in_class > 10:
                anti_patterns.append(
                    {
                        "pattern": "God Class",
                        "severity": "medium",
                        "evidence": f"Class has {methods_in_class} methods (> 10)",
                    }
                )

        max_nesting = 0
        for line in lines:
            stripped = line.rstrip()
            if not stripped:
                continue
            indent = len(line) - len(line.lstrip())
            indent_level = indent // 4
            if re.search(
                r"\b(?:if|for|while|with|try|except|def|class)\b", stripped
            ):
                max_nesting = max(max_nesting, indent_level)

        if max_nesting >= 5:
            anti_patterns.append(
                {
                    "pattern": "Spaghetti Code",
                    "severity": "high" if max_nesting >= 7 else "medium",
                    "evidence": f"Deep nesting detected (level {max_nesting})",
                }
            )

        normalized = re.sub(r"\s+", "", code)
        block_size = 50
        blocks_seen = {}
        for i in range(0, len(normalized) - block_size, 10):
            block = normalized[i : i + block_size]
            if block in blocks_seen:
                anti_patterns.append(
                    {
                        "pattern": "Copy-Paste Code",
                        "severity": "medium",
                        "evidence": "Duplicated code blocks detected",
                    }
                )
                break
            blocks_seen[block] = i

        return anti_patterns

    def detect_code_smells(self, code: str, language: str) -> list[dict]:
        smells = []
        lines = code.splitlines()

        func_bodies = []
        func_starts = [
            m.start()
            for m in re.finditer(
                r"^\s*(?:def|function|func|public|private|protected)\s+\w+\s*\(",
                code,
                re.MULTILINE,
            )
        ]
        for i, start in enumerate(func_starts):
            end = func_starts[i + 1] if i + 1 < len(func_starts) else len(code)
            func_bodies.append((start, end))

        for start, end in func_bodies:
            func_code = code[start:end]
            func_lines = func_code.splitlines()
            if len(func_lines) > 50:
                func_name_match = re.search(
                    r"(?:def|function|func)\s+(\w+)", func_code
                )
                name = func_name_match.group(1) if func_name_match else "unknown"
                smells.append(
                    {
                        "smell": "Long Method",
                        "severity": "medium",
                        "evidence": f"Function '{name}' has {len(func_lines)} lines (> 50)",
                        "line": lines.index(func_lines[0]) + 1 if func_lines else 0,
                    }
                )

        pattern = re.compile(r"(?:def|function|func)\s+\w+\s*\(([^)]*)\)")
        for pm in pattern.finditer(code):
            params = pm.group(1)
            param_count = 0
            if params.strip():
                param_count = len(re.split(r",\s*", params.strip()))
            if param_count > 5:
                smells.append(
                    {
                        "smell": "Too Many Parameters",
                        "severity": "low",
                        "evidence": f"Function has {param_count} parameters (> 5)",
                        "line": code[: pm.start()].count("\n") + 1,
                    }
                )

        for cd in re.finditer(r"^\s*class\s+(\w+)", code, re.MULTILINE):
            class_start = cd.start()
            class_end = len(code)
            for nd in re.finditer(r"^\s*class\s+\w+", code, re.MULTILINE):
                if nd.start() > class_start:
                    class_end = nd.start()
                    break
            class_code = code[class_start:class_end]
            class_lines = class_code.splitlines()
            if len(class_lines) > 300:
                smells.append(
                    {
                        "smell": "Large Class",
                        "severity": "medium",
                        "evidence": f"Class '{cd.group(1)}' has {len(class_lines)} lines (> 300)",
                        "line": code[: cd.start()].count("\n") + 1,
                    }
                )

        if re.search(r"except\s*:\s*pass|catch\s*\(.*\)\s*\{\s*\}", code):
            smells.append(
                {
                    "smell": "Empty Catch Block",
                    "severity": "high",
                    "evidence": "Empty exception handler detected",
                    "line": code[: re.search(r"except\s*:\s*pass", code).start()].count(
                        "\n"
                    )
                    + 1
                    if re.search(r"except\s*:\s*pass", code)
                    else 0,
                }
            )

        return smells
