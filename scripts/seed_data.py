import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.code_analysis.parser.code_parser import CodeParser


def main():
    parser = CodeParser()
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

    results = parser.parse_directory(data_dir)

    total_files = len(results)
    total_functions = sum(len(r.get("functions", [])) for r in results)
    total_classes = sum(len(r.get("classes", [])) for r in results)
    total_lines = sum(r.get("line_count", 0) for r in results)

    print("=== Seed Data Summary ===")
    print(f"Files parsed:     {total_files}")
    print(f"Functions found:  {total_functions}")
    print(f"Classes found:    {total_classes}")
    print(f"Total lines:      {total_lines}")
    print()

    for r in results:
        fname = r.get("filepath", "unknown")
        lang = r.get("language", "unknown")
        funcs = len(r.get("functions", []))
        classes = len(r.get("classes", []))
        lines = r.get("line_count", 0)
        print(f"  {fname}  [{lang}]  {lines} lines, {funcs} functions, {classes} classes")

    print()
    print("Seeding complete.")


if __name__ == "__main__":
    main()
