def validate_code(code: str) -> bool:
    return bool(code and len(code.strip()) > 0)


def validate_language(language: str) -> bool:
    supported = ["python", "javascript", "typescript", "java", "go", "cpp", "rust"]
    return language.lower() in supported


def validate_filename(filename: str) -> bool:
    return bool(filename and "." in filename)
