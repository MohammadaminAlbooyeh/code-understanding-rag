import os
from backend.services.indexing_service import IndexingService


def main():
    service = IndexingService()
    directory = input("Enter directory to index: ")
    if os.path.isdir(directory):
        ids = service.index_directory(directory)
        print(f"Indexed {len(ids)} files")
    else:
        print("Invalid directory")


if __name__ == "__main__":
    main()
