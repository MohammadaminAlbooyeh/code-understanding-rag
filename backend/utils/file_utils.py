import os


def read_file(filepath: str) -> str:
    with open(filepath, "r") as f:
        return f.read()


def write_file(filepath: str, content: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)


def get_file_size(filepath: str) -> int:
    return os.path.getsize(filepath)


def get_file_extension(filepath: str) -> str:
    _, ext = os.path.splitext(filepath)
    return ext.lower()


def list_files(directory: str, pattern: str = None) -> list[str]:
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if pattern is None or filename.endswith(pattern):
                files.append(os.path.join(root, filename))
    return files
