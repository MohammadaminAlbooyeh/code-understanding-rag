from backend.code_analysis.analyzer.dependency_analyzer import DependencyAnalyzer


def main():
    analyzer = DependencyAnalyzer()
    deps = analyzer.analyze_directory("./src")
    circular = analyzer.find_circular_dependencies(deps)
    print("Circular dependencies:", circular)


if __name__ == "__main__":
    main()
