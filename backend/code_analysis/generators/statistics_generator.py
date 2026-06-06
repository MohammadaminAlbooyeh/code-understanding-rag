import re


class StatisticsGenerator:
    def __init__(self):
        self.stats = {}

    def generate(self, parsed_code: dict) -> dict:
        return {
            "line_stats": self.generate_line_stats(parsed_code),
            "complexity_stats": self.generate_complexity_stats(
                parsed_code.get("analyses", [])
            ),
            "function_count": len(parsed_code.get("functions", [])),
            "class_count": len(parsed_code.get("classes", [])),
            "import_count": len(parsed_code.get("imports", [])),
        }

    def generate_line_stats(self, parsed_code: dict) -> dict:
        code = parsed_code.get("code", "")
        if not code:
            code = parsed_code.get("content", "")

        lines = code.splitlines()
        total = len(lines)
        blank = sum(1 for line in lines if not line.strip())
        comment = 0
        in_multiline = False

        lang = parsed_code.get("language", "").lower()

        for line in lines:
            stripped = line.strip()

            if in_multiline:
                comment += 1
                if "*/" in stripped or '"""' in stripped or "'''" in stripped:
                    if stripped.count('"""') == 1 and not stripped.startswith('"""'):
                        pass
                    elif stripped.count("'''") == 1 and not stripped.startswith("'''"):
                        pass
                    else:
                        in_multiline = False
                continue

            if stripped.startswith("#") or stripped.startswith("//"):
                comment += 1
            elif stripped.startswith("/*"):
                comment += 1
                if "*/" not in stripped:
                    in_multiline = True
            elif stripped.startswith('"""') or stripped.startswith("'''"):
                comment += 1
                if not (stripped.endswith('"""') and len(stripped) > 3) and not (
                    stripped.endswith("'''") and len(stripped) > 3
                ):
                    in_multiline = True
            elif stripped.startswith("--") and "sql" in lang:
                comment += 1
            elif stripped.startswith("%") and ("r" in lang or "matlab" in lang):
                comment += 1
            elif stripped.startswith("<!--"):
                comment += 1
                if "-->" not in stripped:
                    in_multiline = True

        code_lines = total - blank - comment
        return {
            "total": total,
            "code": code_lines,
            "blank": blank,
            "comment": comment,
        }

    def generate_language_stats(self, files: list[dict]) -> dict:
        stats = {}
        for f in files:
            lang = f.get("language", "unknown")
            lines = f.get("lines", f.get("line_count", 0))
            if lang not in stats:
                stats[lang] = {"files": 0, "lines": 0}
            stats[lang]["files"] += 1
            stats[lang]["lines"] += lines
        return stats

    def generate_complexity_stats(self, analyses: list[dict]) -> dict:
        if not analyses:
            return {
                "average": 0,
                "max": 0,
                "min": 0,
                "median": 0,
                "distribution": {},
            }

        complexities = []
        for a in analyses:
            if isinstance(a, dict):
                cc = a.get("cyclomatic_complexity", a.get("complexity", 0))
                if isinstance(cc, (int, float)):
                    complexities.append(cc)

        if not complexities:
            return {
                "average": 0,
                "max": 0,
                "min": 0,
                "median": 0,
                "distribution": {},
            }

        complexities.sort()
        avg = sum(complexities) / len(complexities)
        max_c = max(complexities)
        min_c = min(complexities)

        n = len(complexities)
        if n % 2 == 1:
            median = complexities[n // 2]
        else:
            median = (complexities[n // 2 - 1] + complexities[n // 2]) / 2

        distribution = {}
        for c in complexities:
            if c <= 5:
                bucket = "low (1-5)"
            elif c <= 10:
                bucket = "moderate (6-10)"
            elif c <= 20:
                bucket = "complex (11-20)"
            else:
                bucket = "high (>20)"
            distribution[bucket] = distribution.get(bucket, 0) + 1

        return {
            "average": round(avg, 2),
            "max": max_c,
            "min": min_c,
            "median": round(median, 2),
            "distribution": distribution,
        }
