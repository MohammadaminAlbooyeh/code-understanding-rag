class CodeUnderstandingError(Exception):
    pass


class CodeNotFoundError(CodeUnderstandingError):
    pass


class AnalysisNotFoundError(CodeUnderstandingError):
    pass


class InvalidLanguageError(CodeUnderstandingError):
    pass


class FileTooLargeError(CodeUnderstandingError):
    pass


class LLMError(CodeUnderstandingError):
    pass


class EmbeddingError(CodeUnderstandingError):
    pass
