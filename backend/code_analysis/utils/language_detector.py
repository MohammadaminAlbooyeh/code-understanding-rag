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
        }

    def detect(self, code: str, filename: str = None) -> str:
        pass

    def detect_from_extension(self, filename: str) -> str:
        ext = filename[filename.rfind("."):]
        return self.extensions.get(ext, "unknown")

    def detect_from_content(self, code: str) -> str:
        pass
