import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.code_analysis.parser.code_parser import CodeParser
from backend.code_analysis.generators.statistics_generator import StatisticsGenerator
from backend.code_analysis.generators.summary_generator import SummaryGenerator


def main():
    parser = CodeParser()
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
    results = parser.parse_directory(data_dir)

    stats_gen = StatisticsGenerator()
    summary_gen = SummaryGenerator()

    print("=" * 60)
    print("           CODE UNDERSTANDING RAG - ANALYSIS REPORT")
    print("=" * 60)

    total_files = len(results)
    total_functions = sum(len(r.get("functions", [])) for r in results)
    total_classes = sum(len(r.get("classes", [])) for r in results)
    total_lines = sum(r.get("line_count", 0) for r in results)

    print()
    print("--- Overview ---")
    print(f"  Total files:      {total_files}")
    print(f"  Total functions:  {total_functions}")
    print(f"  Total classes:    {total_classes}")
    print(f"  Total lines:      {total_lines}")

    print()
    print("--- Per-File Statistics ---")
    for r in results:
        fname = os.path.basename(r.get("filepath", "unknown"))
        lang = r.get("language", "unknown")

        line_stats = stats_gen.generate_line_stats(r)
        func_count = len(r.get("functions", []))
        class_count = len(r.get("classes", []))
        import_count = len(r.get("imports", []))

        print()
        print(f"  File: {fname}")
        print(f"    Language:     {lang}")
        print(f"    Lines:        {line_stats['total']} total, {line_stats['code']} code, {line_stats['blank']} blank, {line_stats['comment']} comment")
        print(f"    Functions:    {func_count}")
        print(f"    Classes:      {class_count}")
        print(f"    Imports:      {import_count}")

    print()
    print("--- Language Breakdown ---")
    lang_stats = stats_gen.generate_language_stats(results)
    for lang, data in lang_stats.items():
        print(f"  {lang}: {data['files']} files, {data['lines']} lines")

    print()
    print("--- File Summaries ---")
    for r in results:
        summary = summary_gen.generate_file_summary(r)
        print()
        print(summary)

    print()
    print("=" * 60)
    print("Report generation complete.")


if __name__ == "__main__":
    main()
