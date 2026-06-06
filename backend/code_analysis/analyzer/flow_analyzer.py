class FlowAnalyzer:
    def __init__(self):
        self.flow_graphs = {}

    def analyze(self, code: str, language: str) -> dict:
        pass

    def build_call_graph(self, code: str, language: str) -> dict:
        pass

    def build_control_flow_graph(self, code: str, language: str) -> dict:
        pass

    def find_execution_paths(self, code: str, language: str) -> list[list[str]]:
        pass
