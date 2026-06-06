class SummaryGenerator:
    def __init__(self):
        self.summaries = {}

    def generate(self, parsed_code: dict) -> dict:
        return {
            "function_summaries": [
                self.generate_function_summary(f)
                for f in parsed_code.get("functions", [])
            ],
            "class_summaries": [
                self.generate_class_summary(c)
                for c in parsed_code.get("classes", [])
            ],
            "file_summary": self.generate_file_summary(parsed_code),
            "project_summary": self.generate_project_summary(parsed_code)
            if "files" in parsed_code
            else None,
        }

    def generate_function_summary(self, func_data: dict) -> str:
        name = func_data.get("name", "unknown")
        params = func_data.get("parameters", func_data.get("params", []))
        return_type = func_data.get("return_type", func_data.get("returns", "None"))
        docstring = func_data.get("docstring", "")

        param_str = ", ".join(str(p) for p in params) if params else "none"
        lines = [
            f"## Function: {name}",
            f"- Parameters: ({param_str})",
            f"- Returns: {return_type}",
        ]
        if docstring:
            summary = docstring.strip().split("\n")[0] if docstring else ""
            lines.append(f"- Summary: {summary}")

        return "\n".join(lines)

    def generate_class_summary(self, class_data: dict) -> str:
        name = class_data.get("name", "unknown")
        bases = class_data.get("bases", class_data.get("base_classes", []))
        methods = class_data.get("methods", [])
        attributes = class_data.get("attributes", class_data.get("attrs", []))
        docstring = class_data.get("docstring", "")

        lines = [
            f"## Class: {name}",
            f"- Bases: {', '.join(str(b) for b in bases) if bases else 'None'}",
            f"- Methods ({len(methods)}): {', '.join(m if isinstance(m, str) else m.get('name', str(m)) for m in methods)}",
            f"- Attributes ({len(attributes)}): {', '.join(str(a) for a in attributes) if attributes else 'None'}",
        ]
        if docstring:
            summary = docstring.strip().split("\n")[0] if docstring else ""
            lines.append(f"- Summary: {summary}")

        return "\n".join(lines)

    def generate_file_summary(self, file_data: dict) -> str:
        filename = file_data.get("filename", file_data.get("file", "unknown"))
        language = file_data.get("language", "unknown")
        total_lines = file_data.get("line_count", file_data.get("lines", 0))
        num_functions = len(file_data.get("functions", []))
        num_classes = len(file_data.get("classes", []))
        imports = file_data.get("imports", [])
        purpose = file_data.get("purpose", "")

        lines = [
            f"# File: {filename}",
            f"- Language: {language}",
            f"- Lines: {total_lines}",
            f"- Functions: {num_functions}",
            f"- Classes: {num_classes}",
            f"- Imports: {len(imports)}",
        ]
        if purpose:
            lines.append(f"- Purpose: {purpose}")

        return "\n".join(lines)

    def generate_project_summary(self, project_data: dict) -> str:
        files = project_data.get("files", {})
        if not files:
            return "# Project Summary\nNo files found."

        total_files = len(files)
        total_lines = 0
        total_functions = 0
        total_classes = 0
        languages = set()

        for fname, fdata in files.items():
            if isinstance(fdata, dict):
                total_lines += fdata.get("line_count", fdata.get("lines", 0))
                total_functions += len(fdata.get("functions", []))
                total_classes += len(fdata.get("classes", []))
                if "language" in fdata:
                    languages.add(fdata["language"])

        lines = [
            "# Project Summary",
            f"- Total Files: {total_files}",
            f"- Total Lines: {total_lines}",
            f"- Total Functions: {total_functions}",
            f"- Total Classes: {total_classes}",
            f"- Languages: {', '.join(sorted(languages)) if languages else 'N/A'}",
        ]
        return "\n".join(lines)
