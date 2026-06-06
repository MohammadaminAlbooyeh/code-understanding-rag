import os
import datetime


class MetadataGenerator:
    def __init__(self):
        self.metadata = {}

    def generate(self, parsed_code: dict) -> dict:
        return {
            "file_info": {
                "filename": parsed_code.get("filename", "unknown"),
                "extension": os.path.splitext(parsed_code.get("filename", ""))[1],
            },
            "language": self._detect_language(parsed_code.get("filename", ""), parsed_code.get("language", "")),
            "size": {
                "bytes": parsed_code.get("char_count", 0),
                "lines": parsed_code.get("line_count", 0),
            },
            "encoding": "utf-8",
        }

    def _detect_language(self, filename: str, language_hint: str = "") -> str:
        if language_hint:
            return language_hint

        ext_map = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".java": "java",
            ".go": "go",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
            ".rb": "ruby",
            ".rs": "rust",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
            ".r": "r",
            ".m": "objective-c",
            ".mm": "objective-c",
            ".sql": "sql",
            ".html": "html",
            ".css": "css",
            ".json": "json",
            ".xml": "xml",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".md": "markdown",
            ".sh": "shell",
            ".bash": "shell",
            ".zsh": "shell",
            ".dockerfile": "dockerfile",
            ".cs": "csharp",
            ".fs": "fsharp",
        }
        ext = os.path.splitext(filename)[1].lower()
        return ext_map.get(ext, "unknown")

    def generate_file_metadata(self, filepath: str) -> dict:
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filename)[1].lower()

        try:
            stat = os.stat(filepath)
            return {
                "filename": filename,
                "filepath": os.path.abspath(filepath),
                "extension": ext,
                "language": self._detect_language(filename),
                "size_bytes": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "lines": 0,
                "last_modified": datetime.datetime.fromtimestamp(
                    stat.st_mtime
                ).isoformat(),
                "created": datetime.datetime.fromtimestamp(
                    stat.st_ctime
                ).isoformat(),
                "permissions": oct(stat.st_mode)[-3:],
            }
        except Exception as e:
            return {
                "filename": filename,
                "filepath": filepath,
                "error": str(e),
            }

    def generate_project_metadata(self, directory: str) -> dict:
        total_files = 0
        total_lines = 0
        languages = {}
        dir_structure = []

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
            rel_dir = os.path.relpath(root, directory)
            if rel_dir == ".":
                rel_dir = "/"

            dir_files = []
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                fpath = os.path.join(root, fname)
                lang = self._detect_language(fname)
                if lang != "unknown":
                    languages[lang] = languages.get(lang, 0) + 1
                total_files += 1
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        line_count = len(f.readlines())
                    total_lines += line_count
                except Exception:
                    line_count = 0
                dir_files.append(
                    {"name": fname, "language": lang, "lines": line_count}
                )

            dir_structure.append({"directory": rel_dir, "files": dir_files})

        return {
            "directory": os.path.abspath(directory),
            "total_files": total_files,
            "total_lines": total_lines,
            "languages": languages,
            "language_count": len(languages),
            "directory_structure": dir_structure,
        }
