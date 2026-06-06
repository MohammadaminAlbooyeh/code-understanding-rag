import time
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.code_analysis.analyzer.complexity_analyzer import ComplexityAnalyzer
from backend.code_analysis.analyzer.bug_detector import BugDetector
from backend.code_analysis.analyzer.security_analyzer import SecurityAnalyzer
from backend.code_analysis.analyzer.pattern_analyzer import PatternAnalyzer


def benchmark():
    sample_code = """
import os
import sys

def process_data(items, config=None):
    results = []
    for i, item in enumerate(items):
        if item is not None:
            for j in range(len(item)):
                if j % 2 == 0:
                    try:
                        value = item[j] * 2
                        if value > 100:
                            results.append(value)
                        elif value > 50:
                            results.append(value // 2)
                        else:
                            results.append(0)
                    except Exception as e:
                        print(f"Error: {e}")
                        continue
                else:
                    results.append(item[j])
    return results


class DataProcessor:
    def __init__(self, name):
        self.name = name
        self.data = []

    def load(self, filename):
        f = open(filename, "r")
        self.data = f.read()
        return self.data

    def save(self, filename):
        f = open(filename, "w")
        f.write(str(self.data))
        f.close()

    def execute_query(self, query):
        cursor = execute("SELECT " + query + " FROM users")
        return cursor.fetchall()

    def render_html(self, user_input):
        return "<div>" + user_input + "</div>"

    def run_command(self, cmd):
        os.system(cmd)
"""

    results = {}

    print("=== Benchmark Report ===")
    print(f"{'Analyzer':<25} {'Time (s)':>10} {'Results':>10}")
    print("-" * 47)

    start = time.perf_counter()
    ca = ComplexityAnalyzer()
    complexity = ca.analyze(sample_code, "python")
    elapsed = time.perf_counter() - start
    results["ComplexityAnalyzer"] = elapsed
    print(f"{'ComplexityAnalyzer':<25} {elapsed:>10.4f} {1:>10}")

    start = time.perf_counter()
    bd = BugDetector()
    bugs = bd.analyze(sample_code, "python")
    elapsed = time.perf_counter() - start
    results["BugDetector"] = elapsed
    print(f"{'BugDetector':<25} {elapsed:>10.4f} {len(bugs):>10}")

    start = time.perf_counter()
    sa = SecurityAnalyzer()
    vulns = sa.analyze(sample_code, "python")
    elapsed = time.perf_counter() - start
    results["SecurityAnalyzer"] = elapsed
    print(f"{'SecurityAnalyzer':<25} {elapsed:>10.4f} {len(vulns):>10}")

    start = time.perf_counter()
    pa = PatternAnalyzer()
    patterns = pa.analyze(sample_code, "python")
    elapsed = time.perf_counter() - start
    results["PatternAnalyzer"] = elapsed
    print(f"{'PatternAnalyzer':<25} {elapsed:>10.4f} {sum(len(v) for v in patterns.values()):>10}")

    print("-" * 47)
    total = sum(results.values())
    print(f"{'Total':<25} {total:>10.4f}")

    print()
    print("Complexity metrics:", complexity)
    print(f"Bugs found: {len(bugs)}")
    print(f"Vulnerabilities found: {len(vulns)}")
    print(f"Patterns found: design={len(patterns['design_patterns'])}, anti={len(patterns['anti_patterns'])}, smells={len(patterns['code_smells'])}")


if __name__ == "__main__":
    benchmark()
