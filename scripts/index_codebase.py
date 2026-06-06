import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.code_analysis.parser.code_parser import CodeParser


def main():
    parser = CodeParser()

    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        sys.exit(1)

    print(f"Indexing directory: {directory}")
    results = parser.parse_directory(directory)

    total_files = len(results)
    total_functions = sum(len(r.get("functions", [])) for r in results)
    total_classes = sum(len(r.get("classes", [])) for r in results)
    total_lines = sum(r.get("line_count", 0) for r in results)

    print()
    print("=== Indexing Summary ===")
    print(f"Files indexed:     {total_files}")
    print(f"Functions found:   {total_functions}")
    print(f"Classes found:     {total_classes}")
    print(f"Total lines:       {total_lines}")
    print()

    for r in results:
        fname = r.get("filepath", "unknown")
        lang = r.get("language", "unknown")
        funcs = len(r.get("functions", []))
        classes = len(r.get("classes", []))
        print(f"  {fname}  [{lang}]  {funcs} funcs, {classes} classes")

    print()
    print(f"Indexing complete. {total_files} files processed.")


if __name__ == "__main__":
    main()
