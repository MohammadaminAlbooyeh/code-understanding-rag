import re


class CodeCleaner:
    def __init__(self):
        pass

    def remove_comments(self, code: str, language: str) -> str:
        if language == "python":
            cleaned = re.sub(r"#.*$", "", code, flags=re.MULTILINE)
            cleaned = re.sub(r"'''(?:.|\n)*?'''", "", cleaned)
            cleaned = re.sub(r'"""(?:.|\n)*?"""', "", cleaned)
            return cleaned
        elif language in ("javascript", "typescript", "java", "cpp", "go"):
            cleaned = re.sub(r"//.*$", "", code, flags=re.MULTILINE)
            cleaned = re.sub(r"/\*[\s\S]*?\*/", "", cleaned)
            return cleaned
        return code

    def remove_empty_lines(self, code: str) -> str:
        lines = [line for line in code.split("\n") if line.strip()]
        return "\n".join(lines)

    def normalize_whitespace(self, code: str) -> str:
        lines = []
        for line in code.split("\n"):
            stripped = line.rstrip()
            lines.append(stripped)
        result = "\n".join(lines)
        result = re.sub(r"\n{3,}", "\n\n", result)
        return result

    def strip_code(self, code: str) -> str:
        code = self.remove_comments(code, "python")
        code = self.remove_empty_lines(code)
        code = self.normalize_whitespace(code)
        return code.strip()
