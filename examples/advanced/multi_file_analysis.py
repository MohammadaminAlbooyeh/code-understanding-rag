from backend.code_analysis.analyzer.dependency_analyzer import DependencyAnalyzer


def main():
    analyzer = DependencyAnalyzer()
    deps = analyzer.analyze_directory("./src")
    graph = analyzer.build_dependency_graph(deps)
    print("Dependency graph:", graph)


if __name__ == "__main__":
    main()
