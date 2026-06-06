import re


class SecurityAnalyzer:
    def __init__(self):
        self.vulnerabilities = []

    def analyze(self, code: str, language: str) -> list[dict]:
        vulns = []
        vulns.extend(self.detect_injection(code, language))
        vulns.extend(self.detect_xss(code, language))
        vulns.extend(self.detect_auth_issues(code, language))
        vulns.extend(self.check_owasp_top10(code, language))
        return vulns

    def detect_injection(self, code: str, language: str) -> list[dict]:
        vulns = []
        lines = code.splitlines()
        lang = language.lower()

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//")):
                continue

            if re.search(
                r'(?:execute|exec|executemany)\s*\(\s*["\'].*["\']\s*[%+].*["\']',
                line,
            ) or re.search(r'cursor\.execute\s*\(\s*["\'].*[%+]', line):
                vulns.append(
                    {
                        "type": "SQL Injection",
                        "severity": "critical",
                        "line": i + 1,
                        "message": "Raw SQL query constructed with string concatenation/interpolation",
                        "remediation": "Use parameterized queries (?, %s placeholders) instead of string formatting",
                    }
                )

            if re.search(r"\b(?:eval|exec)\s*\(", stripped):
                vulns.append(
                    {
                        "type": "Code Injection",
                        "severity": "critical",
                        "line": i + 1,
                        "message": "Dynamic code execution via eval/exec",
                        "remediation": "Avoid eval/exec. Use safer alternatives like ast.literal_eval",
                    }
                )

            if re.search(r"\b(?:os\.system|subprocess\.[a-z]+|Popen|shell=True)\b", stripped):
                vulns.append(
                    {
                        "type": "OS Command Injection",
                        "severity": "critical",
                        "line": i + 1,
                        "message": "OS command execution detected",
                        "remediation": "Use subprocess with shell=False and pass arguments as a list",
                    }
                )

        return vulns

    def detect_xss(self, code: str, language: str) -> list[dict]:
        vulns = []
        lines = code.splitlines()
        lang = language.lower()

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//")):
                continue

            if re.search(r"\.innerHTML\s*=", stripped):
                vulns.append(
                    {
                        "type": "XSS (Stored/Reflected)",
                        "severity": "high",
                        "line": i + 1,
                        "message": "innerHTML assignment detected - vulnerable to XSS",
                        "remediation": "Use textContent or innerText instead of innerHTML, or sanitize input",
                    }
                )

            if re.search(r"(?:document\.write|eval)\s*\(", stripped):
                vulns.append(
                    {
                        "type": "XSS via DOM manipulation",
                        "severity": "high",
                        "line": i + 1,
                        "message": "DOM manipulation that may introduce XSS",
                        "remediation": "Avoid document.write and eval. Use safe DOM APIs instead",
                    }
                )

            if re.search(r"\{\{.*[^{].*\}\}", stripped) and re.search(r"\|\s*safe", stripped):
                vulns.append(
                    {
                        "type": "XSS (Unescaped Output)",
                        "severity": "high",
                        "line": i + 1,
                        "message": "Unescaped template variable with safe filter",
                        "remediation": "Remove the 'safe' filter or explicitly sanitize the output",
                    }
                )

        return vulns

    def detect_auth_issues(self, code: str, language: str) -> list[dict]:
        vulns = []
        lines = code.splitlines()

        sensitive_patterns = [
            (r"(?:password|passwd|pwd)\s*[:=]\s*['\"][^'\"]+['\"]", "Hardcoded Password"),
            (r"(?:api_key|apikey|api\.key)\s*[:=]\s*['\"][^'\"]+['\"]", "Hardcoded API Key"),
            (r"(?:secret|token|auth_token|access_token)\s*[:=]\s*['\"][^'\"]+['\"]", "Hardcoded Secret/Token"),
            (r"(?:private_key|private\s+key)\s*[:=]\s*['\"][^'\"]+['\"]", "Hardcoded Private Key"),
            (r"(?:connection_string|connstr)\s*[:=]\s*['\"][^'\"]+['\"]", "Hardcoded Connection String"),
        ]

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//")):
                continue

            for pattern, vuln_type in sensitive_patterns:
                if re.search(pattern, stripped, re.IGNORECASE):
                    vulns.append(
                        {
                            "type": vuln_type,
                            "severity": "critical",
                            "line": i + 1,
                            "message": f"Potential {vuln_type.lower()} detected in source code",
                            "remediation": "Use environment variables or a secrets manager instead of hardcoding",
                        }
                    )

        return vulns

    def check_owasp_top10(self, code: str, language: str) -> list[dict]:
        vulns = []
        lines = code.splitlines()

        vulns.extend(self.detect_injection(code, language))
        vulns.extend(self.detect_xss(code, language))
        vulns.extend(self.detect_auth_issues(code, language))

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//")):
                continue

            if re.search(
                r"\b(?:pickle\.loads?|yaml\.load(?!.*SafeLoader)|marshal\.loads?|xml\.parsers|ElementTree\.parse)\b",
                stripped,
            ):
                vulns.append(
                    {
                        "type": "Insecure Deserialization (A08:2021)",
                        "severity": "high",
                        "line": i + 1,
                        "message": "Insecure deserialization detected",
                        "remediation": "Use safe deserialization (e.g., yaml.safe_load) or validate input before deserializing",
                    }
                )

            if re.search(
                r"\b(?:requests\.get|requests\.post|urllib|httpx)\s*\(", stripped
            ):
                if not re.search(r"(?:verify|timeout)", stripped):
                    vulns.append(
                        {
                            "type": "SSRF / Missing Validation (A10:2021)",
                            "severity": "medium",
                            "line": i + 1,
                            "message": "Outbound HTTP request without URL validation",
                            "remediation": "Validate and restrict URLs to a whitelist to prevent SSRF attacks",
                        }
                    )

            if re.search(
                r"\b(?:AES|DES|ARC4|RC4|MD5|SHA-?1)\b", stripped, re.IGNORECASE
            ):
                vulns.append(
                    {
                        "type": "Cryptographic Failure (A02:2021)",
                        "severity": "high",
                        "line": i + 1,
                        "message": "Weak cryptographic algorithm detected",
                        "remediation": "Use strong modern algorithms (AES-256-GCM, SHA-256/SHA-3) instead",
                    }
                )

            if re.search(
                r"\b(?:pickle\.loads?|yaml\.load(?!.*SafeLoader)|eval|exec)\(", stripped
            ):
                vulns.append(
                    {
                        "type": "Insecure Deserialization (A08:2021)",
                        "severity": "high",
                        "line": i + 1,
                        "message": "Unsafe deserialization of untrusted data",
                        "remediation": "Use safe serialization formats (JSON) or validate input before deserialization",
                    }
                )

        seen = set()
        unique_vulns = []
        for v in vulns:
            key = (v["type"], v["line"])
            if key not in seen:
                seen.add(key)
                unique_vulns.append(v)

        return unique_vulns
