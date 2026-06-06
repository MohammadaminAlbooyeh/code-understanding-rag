class DependencyAnalyzer:
    def __init__(self):
        self.dependencies = {}

    def analyze(self, code: str, language: str) -> dict:
        pass

    def analyze_directory(self, directory: str) -> dict:
        pass

    def build_dependency_graph(self, dependencies: dict) -> dict:
        pass

    def find_circular_dependencies(self, dependencies: dict) -> list[list[str]]:
        pass
