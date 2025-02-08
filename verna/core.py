import os
import argparse
from collections import Counter

def count_files_by_extension(directory):
    file_counts = Counter()

    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            file_counts[ext] += 1

    return file_counts

def main():
    parser = argparse.ArgumentParser(description="Count files by extension in a directory.")
    parser.add_argument("directory", type=str, help="Path to the directory to scan")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Error: Provided path is not a valid directory.")
        return

    file_counts = count_files_by_extension(args.directory)

    for ext, count in sorted(file_counts.items()):
        print(f"{ext if ext else '[no extension]'}\t{count}")

if __name__ == "__main__":
    main()
