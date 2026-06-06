import pytest
from backend.code_analysis.analyzer.complexity_analyzer import ComplexityAnalyzer
from backend.code_analysis.analyzer.bug_detector import BugDetector
from backend.code_analysis.analyzer.security_analyzer import SecurityAnalyzer
from backend.code_analysis.analyzer.pattern_analyzer import PatternAnalyzer


@pytest.fixture
def complexity():
    return ComplexityAnalyzer()


@pytest.fixture
def bug_detector():
    return BugDetector()


@pytest.fixture
def security():
    return SecurityAnalyzer()


@pytest.fixture
def pattern():
    return PatternAnalyzer()


class TestComplexityAnalyzer:
    def test_cyclomatic_complexity_simple(self, complexity):
        code = "def foo():\n    return 1\n"
        result = complexity.analyze(code, "python")
        assert result["cyclomatic_complexity"] == 1

    def test_cyclomatic_complexity_with_conditionals(self, complexity):
        code = "def foo(x):\n    if x > 0:\n        return 1\n    elif x < 0:\n        return -1\n    else:\n        return 0\n"
        result = complexity.analyze(code, "python")
        assert result["cyclomatic_complexity"] >= 3

    def test_cyclomatic_complexity_with_loops(self, complexity):
        code = "def foo(items):\n    for item in items:\n        if item:\n            print(item)\n"
        result = complexity.analyze(code, "python")
        assert result["cyclomatic_complexity"] >= 3

    def test_cognitive_complexity(self, complexity):
        code = "def foo(x):\n    if x:\n        if x > 5:\n            return 1\n    return 0\n"
        result = complexity.analyze(code, "python")
        assert result["cognitive_complexity"] > 0

    def test_time_complexity_constant(self, complexity):
        code = "def foo():\n    return 42\n"
        result = complexity.analyze(code, "python")
        assert result["time_complexity"] == "O(1)"

    def test_time_complexity_linear(self, complexity):
        code = "def foo(items):\n    for i in items:\n        print(i)\n"
        result = complexity.analyze(code, "python")
        assert result["time_complexity"] in ("O(n)", "O(1)")

    def test_time_complexity_quadratic(self, complexity):
        code = "def foo(items):\n    for i in items:\n        for j in items:\n            print(i, j)\n"
        result = complexity.analyze(code, "python")
        assert result["time_complexity"] == "O(n²)"

    def test_space_complexity_constant(self, complexity):
        code = "def foo():\n    x = 1\n    return x\n"
        result = complexity.analyze(code, "python")
        assert result["space_complexity"] == "O(1)"

    def test_line_count(self, complexity):
        code = "def foo():\n    pass\n"
        result = complexity.analyze(code, "python")
        assert result["lines_of_code"] == 2

    def test_count_functions(self, complexity):
        code = "def a(): pass\ndef b(): pass\n"
        result = complexity.analyze(code, "python")
        assert result["num_functions"] == 2

    def test_count_classes(self, complexity):
        code = "class A: pass\nclass B: pass\n"
        result = complexity.analyze(code, "python")
        assert result["num_classes"] == 2

    def test_count_conditionals(self, complexity):
        code = "if x:\n    pass\nelif y:\n    pass\nelse:\n    pass\n"
        result = complexity.analyze(code, "python")
        assert result["num_conditionals"] >= 3

    def test_count_loops(self, complexity):
        code = "for i in range(10):\n    while True:\n        break\n"
        result = complexity.analyze(code, "python")
        assert result["num_loops"] == 2

    def test_javascript_complexity(self, complexity):
        code = "function foo(x) {\n  if (x) { return 1; }\n  return 0;\n}\n"
        result = complexity.analyze(code, "javascript")
        assert result["num_functions"] >= 1


class TestBugDetector:
    def test_null_pointer_detection(self, bug_detector):
        code = "def foo():\n    x = None\n    x.strip()\n"
        bugs = bug_detector.analyze(code, "python")
        types = [b["type"] for b in bugs]
        assert "Null Pointer Dereference" in types

    def test_null_return_detection(self, bug_detector):
        code = "def find_item(items):\n    return None\n"
        bugs = bug_detector.analyze(code, "python")
        types = [b["type"] for b in bugs]
        assert "Null Pointer Risk" in types

    def test_memory_leak_detection(self, bug_detector):
        code = "def read_file():\n    f = open('test.txt')\n    data = f.read()\n"
        bugs = bug_detector.analyze(code, "python")
        types = [b["type"] for b in bugs]
        assert "Unclosed Resource" in types

    def test_memory_leak_with_close(self, bug_detector):
        code = "def read_file():\n    f = open('test.txt')\n    data = f.read()\n    f.close()\n"
        bugs = bug_detector.analyze(code, "python")
        types = [b["type"] for b in bugs]
        assert "Unclosed Resource" not in types

    def test_concurrency_sleep_detection(self, bug_detector):
        code = "import threading\nimport time\nwhile True:\n    time.sleep(1)\n    print('working')\n"
        bugs = bug_detector.analyze(code, "python")
        types = [b["type"] for b in bugs]
        assert "Timing via sleep" in types

    def test_no_bugs_on_clean_code(self, bug_detector):
        code = "def add(a, b):\n    return a + b\n"
        bugs = bug_detector.analyze(code, "python")
        assert len(bugs) == 0


class TestSecurityAnalyzer:
    def test_sql_injection_detection(self, security):
        code = 'cursor.execute("SELECT * FROM users WHERE id = " + user_id)\n'
        vulns = security.analyze(code, "python")
        types = [v["type"] for v in vulns]
        assert "SQL Injection" in types

    def test_code_injection_detection(self, security):
        code = 'eval(user_input)\n'
        vulns = security.analyze(code, "python")
        types = [v["type"] for v in vulns]
        assert "Code Injection" in types

    def test_os_command_injection_detection(self, security):
        code = 'os.system("rm -rf /")\n'
        vulns = security.analyze(code, "python")
        types = [v["type"] for v in vulns]
        assert "OS Command Injection" in types

    def test_hardcoded_password_detection(self, security):
        code = 'password = "supersecret123"\n'
        vulns = security.analyze(code, "python")
        types = [v["type"] for v in vulns]
        assert "Hardcoded Password" in types

    def test_hardcoded_api_key_detection(self, security):
        code = 'api_key = "sk-1234567890abcdef"\n'
        vulns = security.analyze(code, "python")
        types = [v["type"] for v in vulns]
        assert "Hardcoded API Key" in types

    def test_xss_innerhtml_detection(self, security):
        code = 'element.innerHTML = userInput\n'
        vulns = security.analyze(code, "javascript")
        types = [v["type"] for v in vulns]
        assert any("XSS" in t for t in types)

    def test_insecure_deserialization_detection(self, security):
        code = 'data = pickle.loads(raw_data)\n'
        vulns = security.analyze(code, "python")
        types = [v["type"] for v in vulns]
        assert "Insecure Deserialization (A08:2021)" in types

    def test_weak_crypto_detection(self, security):
        code = 'hash = MD5.new()\n'
        vulns = security.analyze(code, "python")
        types = [v["type"] for v in vulns]
        assert "Cryptographic Failure (A02:2021)" in types

    def test_no_vulns_on_clean_code(self, security):
        code = "def add(a, b):\n    return a + b\n"
        vulns = security.analyze(code, "python")
        assert len(vulns) == 0


class TestPatternAnalyzer:
    def test_singleton_detection(self, pattern):
        code = "class Config:\n    _instance = None\n    @classmethod\n    def getInstance(cls):\n        return cls._instance\n"
        result = pattern.analyze(code, "python")
        patterns = [p["pattern"] for p in result["design_patterns"]]
        assert "Singleton" in patterns

    def test_factory_detection(self, pattern):
        code = "def create_instance(name):\n    return User(name)\n"
        result = pattern.analyze(code, "python")
        patterns = [p["pattern"] for p in result["design_patterns"]]
        assert "Factory" in patterns

    def test_observer_detection(self, pattern):
        code = "def on_click():\n    print('clicked')\nbutton.addEventListener('click', on_click)\n"
        result = pattern.analyze(code, "javascript")
        patterns = [p["pattern"] for p in result["design_patterns"]]
        assert "Observer" in patterns

    def test_decorator_detection(self, pattern):
        code = "@timer\ndef slow_function():\n    pass\n"
        result = pattern.analyze(code, "python")
        patterns = [p["pattern"] for p in result["design_patterns"]]
        assert "Decorator" in patterns

    def test_god_class_detection(self, pattern):
        code = "class GodObject:\n"
        for i in range(15):
            code += f"    def method{i}(self): pass\n"
        result = pattern.analyze(code, "python")
        anti_patterns = [a["pattern"] for a in result["anti_patterns"]]
        assert "God Class" in anti_patterns

    def test_long_method_detection(self, pattern):
        code = "def long_function():\n"
        for i in range(55):
            code += f"    x = {i}\n"
        result = pattern.analyze(code, "python")
        smells = [s["smell"] for s in result["code_smells"]]
        assert "Long Method" in smells

    def test_too_many_params_detection(self, pattern):
        code = "def process(a, b, c, d, e, f, g):\n    pass\n"
        result = pattern.analyze(code, "python")
        smells = [s["smell"] for s in result["code_smells"]]
        assert "Too Many Parameters" in smells

    def test_no_patterns_on_simple_code(self, pattern):
        code = "x = 1\n"
        result = pattern.analyze(code, "python")
        assert len(result["design_patterns"]) == 0
