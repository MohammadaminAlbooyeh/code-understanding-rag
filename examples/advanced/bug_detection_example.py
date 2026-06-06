from backend.code_analysis.analyzer.bug_detector import BugDetector


def main():
    detector = BugDetector()
    code = """
def divide(a, b):
    return a / b
"""
    bugs = detector.analyze(code, "python")
    print("Potential bugs:", bugs)


if __name__ == "__main__":
    main()
