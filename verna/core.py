import os
import argparse
from collections import Counter
import datetime
from re import sub
from pathlib import Path, PosixPath
import logging
import shutil

logging.basicConfig(level=logging.DEBUG, format="%(lineno)d\t%(message)s")


def count_files_by_extension(directory):
    file_counts = Counter()

    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1]
            file_counts[ext] += 1

    return file_counts


def main():
    parser = argparse.ArgumentParser(
        description="Count files by extension in a directory."
    )
    parser.add_argument("directory", type=str, help="Path to the directory to scan")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Error: Provided path is not a valid directory.")
        return

    file_counts = count_files_by_extension(args.directory)

    for ext, count in sorted(file_counts.items()):
        print(f"{ext if ext else '[no extension]'}\t{count}")

    source_path = Path(args.directory)

    label = input("What is the label? ")
    target = input("What is the target dir? ")
    type_str = str(input("What are the file extensions? "))
    types = type_str.split(",")
    logging.debug(f"types: {types}")

    dt = datetime.datetime.now()
    filepath = mk_filepath(target, label, dt)
    filepath.mkdir()
    logging.debug(f"--> Ready to copy files of type {types} to {filepath}")

    for t in types:
        glob_path = "**/*" + t
        logging.debug(f"glob_path: {glob_path}")
        globs = sorted(source_path.glob(glob_path))

        logging.debug(f"found {len(globs)} files matching extension {t}:")
        for g in globs:
            logging.debug(f"copying {g} to {filepath}")
            shutil.copy(g, filepath)


def canonical_date(dt: datetime) -> str:
    try:
        return dt.strftime("%Y_%m_%d")
    except AttributeError as e:
        raise AttributeError(f"arg '{dt}' not a valid datetime")


def snake_case(s: str) -> str:
    # Replace hyphens with spaces, then apply regular expression substitutions for title case conversion
    # and add an underscore between words, finally convert the result to lowercase
    return "_".join(
        sub(
            "([A-Z][a-z]+)",
            r" \1",
            sub("([A-Z]+)", r" \1", s.replace("-", " ").replace("'", "")),
        ).split()
    ).lower()


def mk_filepath(base_dir, label, dt=datetime.datetime.now()) -> PosixPath:
    formatted_date = canonical_date(dt)
    formatted_label = snake_case(label)
    p = Path(base_dir)
    return p / f"{formatted_date}_{formatted_label}"


if __name__ == "__main__":
    main()
