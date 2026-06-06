import re


class BugDetector:
    def __init__(self):
        self.patterns = []

    def analyze(self, code: str, language: str) -> list[dict]:
        bugs = []
        bugs.extend(self.detect_null_pointer(code, language))
        bugs.extend(self.detect_memory_leaks(code, language))
        bugs.extend(self.detect_concurrency_issues(code, language))
        bugs.extend(self.detect_type_errors(code, language))
        return bugs

    def detect_null_pointer(self, code: str, language: str) -> list[dict]:
        bugs = []
        lines = code.splitlines()
        lang = language.lower()

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//")):
                continue

            if re.search(r"(\w+)\s*\.\s*(\w+)\s*\(", stripped):
                deref_var = re.search(r"(\w+)\s*\.\s*(\w+)\s*\(", stripped)
                if deref_var:
                    var_name = deref_var.group(1)
                    if var_name != "self" and var_name != "this":
                        for j in range(max(0, i - 3), i):
                            if re.search(
                                rf"\b{var_name}\b.*=\s*(?:None|null|undefined|NULL)\s*$",
                                lines[j],
                            ):
                                bugs.append(
                                    {
                                        "type": "Null Pointer Dereference",
                                        "severity": "high",
                                        "line": i + 1,
                                        "message": f"Variable '{var_name}' assigned None/null and may be dereferenced",
                                        "suggestion": "Add a null check before dereferencing the variable",
                                    }
                                )

            if re.search(r"return\s+(?:None|null|undefined|NULL)\b", stripped):
                func_name = None
                for j in range(i - 1, -1, -1):
                    fm = re.search(
                        r"(?:def|function|func)\s+(\w+)\s*\(", lines[j]
                    )
                    if fm:
                        func_name = fm.group(1)
                        break
                if func_name:
                    bugs.append(
                        {
                            "type": "Null Pointer Risk",
                            "severity": "medium",
                            "line": i + 1,
                            "message": f"Function '{func_name}' may return None/null",
                            "suggestion": "Consider using Optional or adding a null check at call sites",
                        }
                    )

        return bugs

    def detect_memory_leaks(self, code: str, language: str) -> list[dict]:
        bugs = []
        lines = code.splitlines()
        lang = language.lower()

        open_calls = []
        for i, line in enumerate(lines):
            if re.search(r"\b(?:open|fopen|File)\s*\(", line):
                open_calls.append(i)

        for i in open_calls:
            has_close = False
            for j in range(i, min(i + 20, len(lines))):
                if re.search(r"\b(?:close|fclose|\.close)\s*\(", lines[j]):
                    has_close = True
                    break
            if not has_close:
                bugs.append(
                    {
                        "type": "Unclosed Resource",
                        "severity": "high",
                        "line": i + 1,
                        "message": "File handle or resource may not be closed",
                        "suggestion": "Use a context manager (with/as) or ensure close() is called",
                    }
                )

        for i, line in enumerate(lines):
            if re.search(r"\b(?:connect|Connect|Connection)\s*\(", line):
                has_disconnect = False
                for j in range(i, min(i + 20, len(lines))):
                    if re.search(
                        r"\b(?:disconnect|close|release|Disconnect)\s*\(", lines[j]
                    ):
                        has_disconnect = True
                        break
                if not has_disconnect:
                    bugs.append(
                        {
                            "type": "Unclosed Connection",
                            "severity": "high",
                            "line": i + 1,
                            "message": "Database/network connection may not be released",
                            "suggestion": "Use a context manager or ensure disconnect/close is called",
                        }
                    )

        return bugs

    def detect_concurrency_issues(self, code: str, language: str) -> list[dict]:
        bugs = []
        lines = code.splitlines()

        has_threading = bool(
            re.search(
                r"\b(?:thread|Thread|threading|multiprocessing|asyncio)\b", code
            )
        )

        if not has_threading:
            return bugs

        shared_vars = set()
        for i, line in enumerate(lines):
            if re.search(r"\b(?:global|nonlocal)\s+(\w+)", line):
                for g in re.finditer(r"\b(?:global|nonlocal)\s+(\w+)", line):
                    shared_vars.add(g.group(1))

        has_lock = bool(
            re.search(
                r"\b(?:Lock|lock|RLock|Semaphore|Mutex|mutex|atomic)\b", code
            )
        )

        if shared_vars and not has_lock:
            for var in shared_vars:
                bugs.append(
                    {
                        "type": "Shared Mutable State",
                        "severity": "high",
                        "line": 1,
                        "message": f"Shared variable '{var}' accessed without synchronization",
                        "suggestion": "Use a lock (threading.Lock) or atomic operations when accessing shared state",
                    }
                )

        for i, line in enumerate(lines):
            if re.search(r"\b(?:time\.sleep|sleep|thread\.sleep)\s*\(", line):
                bugs.append(
                    {
                        "type": "Timing via sleep",
                        "severity": "low",
                        "line": i + 1,
                        "message": "Using sleep for timing may cause race conditions",
                        "suggestion": "Use proper synchronization primitives (Event, Condition) instead of sleep",
                    }
                )

        return bugs

    def detect_type_errors(self, code: str, language: str) -> list[dict]:
        bugs = []
        lines = code.splitlines()

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//")):
                continue

            if re.search(r"(\w+)\s*\+\s*(\d+)", stripped):
                m = re.search(r"(\w+)\s*\+\s*(\d+)", stripped)
                var_name = m.group(1)
                for j in range(max(0, i - 5), i):
                    if re.search(
                        rf'\b{var_name}\b\s*=\s*["\']', lines[j]
                    ):
                        bugs.append(
                            {
                                "type": "Type Mismatch",
                                "severity": "medium",
                                "line": i + 1,
                                "message": f"String variable '{var_name}' used with numeric addition",
                                "suggestion": "Ensure consistent types or use explicit conversion",
                            }
                        )
                        break

            if re.search(r"\.(\w+)\s*(?!=)", stripped):
                attr = re.search(r"\.(\w+)\s*(?!=)", stripped)
                if attr:
                    attr_name = attr.group(1)
                    if attr_name.startswith("__"):
                        continue
                    if attr_name in (
                        "append",
                        "push",
                        "pop",
                        "sort",
                        "join",
                        "split",
                        "strip",
                    ):
                        continue

        return bugs
