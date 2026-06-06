from backend.code_analysis.parser.ast_extractor import ASTExtractor
from backend.code_analysis.parser.function_extractor import FunctionExtractor
from backend.code_analysis.parser.class_extractor import ClassExtractor
from backend.code_analysis.parser.import_extractor import ImportExtractor
from backend.code_analysis.parser.docstring_extractor import DocstringExtractor
from backend.code_analysis.utils.language_detector import LanguageDetector
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class CodeParser:
    def __init__(self):
        self.ast_extractor = ASTExtractor()
        self.function_extractor = FunctionExtractor()
        self.class_extractor = ClassExtractor()
        self.import_extractor = ImportExtractor()
        self.docstring_extractor = DocstringExtractor()
        self.language_detector = LanguageDetector()

    def parse(self, code: str, language: str) -> dict:
        return {
            "language": language,
            "ast": self.ast_extractor.extract(code, language),
            "functions": self.function_extractor.extract(code, language),
            "classes": self.class_extractor.extract(code, language),
            "imports": self.import_extractor.extract(code, language),
            "docstrings": self.docstring_extractor.extract(code, language),
            "line_count": len(code.split("\n")),
            "char_count": len(code),
        }

    def parse_file(self, filepath: str) -> dict:
        with open(filepath, "r") as f:
            code = f.read()
        import os
        _, ext = os.path.splitext(filepath)
        language = self.language_detector.detect_from_extension(filepath)
        if language == "unknown":
            language = self.language_detector.detect(code, filepath)
        return self.parse(code, language)

    def parse_directory(self, directory: str) -> list[dict]:
        import os
        results = []
        for root, _, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in (".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".cpp", ".c", ".rs"):
                    filepath = os.path.join(root, file)
                    try:
                        result = self.parse_file(filepath)
                        result["filepath"] = filepath
                        results.append(result)
                    except Exception as e:
                        logger.error(f"Error parsing {filepath}: {e}")
        return results
