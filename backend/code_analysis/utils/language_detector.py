import re


class LanguageDetector:
    def __init__(self):
        self.extensions = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".java": "java",
            ".go": "go",
            ".cpp": "cpp",
            ".c": "c",
            ".h": "c",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
        }
        self.shebangs = {
            "python": r"python[23]?",
            "node": "javascript",
            "bash": "bash",
        }

    def detect(self, code: str, filename: str = None) -> str:
        if filename:
            result = self.detect_from_extension(filename)
            if result != "unknown":
                return result
        return self.detect_from_content(code)

    def detect_from_extension(self, filename: str) -> str:
        idx = filename.rfind(".")
        if idx == -1:
            return "unknown"
        ext = filename[idx:].lower()
        return self.extensions.get(ext, "unknown")

    def detect_from_content(self, code: str) -> str:
        first_line = code.strip().split("\n")[0] if code.strip() else ""
        shebang_match = re.match(r"^#!\s*(?:\S+/)?(\w+)", first_line)
        if shebang_match:
            interpreter = shebang_match.group(1)
            for key, lang in self.shebangs.items():
                if re.match(key, interpreter):
                    return lang
        if re.search(r"^\s*import\s+\w+|^\s*from\s+\w+\s+import|^\s*def\s+\w+\s*\(|^\s*class\s+\w+[:\s]|^\s*print\s*\(", code, re.MULTILINE):
            return "python"
        if re.search(r"^\s*(?:import|export)\s+.*?\s+from\s+['\"]|^\s*(?:const|let|var)\s+\w+\s*=|(?:function\s+\w+\s*\()", code, re.MULTILINE):
            return "javascript"
        if re.search(r"^\s*(?:public|private|protected)\s+(?:class|interface|enum)\s+\w+", code, re.MULTILINE):
            return "java"
        if re.search(r"^\s*package\s+\w+|^\s*func\s+\w+\s*\(", code, re.MULTILINE):
            return "go"
        if re.search(r"^\s*#include\s+[<\"\w]", code, re.MULTILINE):
            return "cpp"
        if re.search(r"^\s*use\s+\w+|^\s*fn\s+\w+\s*\(", code, re.MULTILINE):
            return "rust"
        return "unknown"
