"""Requests a code review from a large language model."""

from argparse import ArgumentParser, Namespace
import glob
import os
import sys

LETTER_GRADES = ["A", "B", "C", "D", "F"]


def get_source_filenames(
    source_directory: str, filter_files_by_suffix: str | None = None
) -> set[str]:
    """Returns the filenames in a recursive listing of the source directory.

    :param source_directory: The directory in which to find files.
    :param filter_files_by_suffix: If specified, return only files whose names
        end with the given string. If None, return all files.
    :return: The filenames in a recursive listing of the source directory.
        The filenames are in arbitrary order, so the return type is set.
    """
    if filter_files_by_suffix is None:
        filter_files_by_suffix = ""
    paths_with_directories = glob.glob(
        os.path.join(source_directory, "**", f"*{filter_files_by_suffix}"),
        recursive=True,
    )
    paths_without_directories = [
        path for path in paths_with_directories if not os.path.isdir(path)
    ]
    return set(paths_without_directories)


def get_source_contents(source_filenames: list[str]) -> list[str]:
    """Return the contents of all given files in the same order as the input.

    :param source_filenames: The files to read.
    """
    contents = []
    for filename in source_filenames:
        with open(filename, "r", encoding="utf-8") as infile:
            contents.append(infile.read())
    return contents


def get_args(args: list[str]) -> Namespace:
    """Returns a Namespace containing the command line arguments.

    :param args: The raw command line arguments. As in argparse, this function
        expects the value to be sys.argv[1:].
    :return: The argparse.Namespace containing the processed command line
        arguments.
    """
    parser = ArgumentParser(
        description="Requests a code review from a large language model "
        "(LLM). The model will grade the code based on "
        "readability, expressiveness, and organization. The "
        f"output will include a letter grade in {LETTER_GRADES}, "
        "as well as the model's reasoning."
    )
    parser.add_argument(
        "--source_directory",
        default=".",
        help="The directory to search for source files. This search is "
        "recursive. The LLM will perform its code review on these files.",
    )
    parser.add_argument(
        "--filter_files_by_suffix",
        default=None,
        help="If specified, select only the files that end with the given "
        'string for code review. For instance, a value of ".py" '
        "selects only the Python files.",
    )
    parser.add_argument(
        "--fail_under",
        default=None,
        choices=LETTER_GRADES[:-1],
        help="If specified, exit with non-zero status if the LLM's grade "
        "falls below the given value. This value is not inclusive: if "
        'this value is "B" and the LLM gives a final grade of "B," '
        "then the program will exit with a zero status. If not "
        "specified, then the program will exit with a zero status no "
        "matter the LLM's grade.",
    )
    parser.add_argument(
        "--openai_api_key",
        required=True,
        help="The user's OpenAI API key. Each code review will make a request "
        "on an OpenAI model, which will incur a marginal cost. GPT3.5, "
        "for instance, currently costs $0.002 per 1K tokens.",
    )
    return parser.parse_args(args=args)


def main() -> None:
    """Runs a code review on the user-specified directory."""
    args = get_args(sys.argv[1:])
    source_filenames = list(get_source_filenames(args.source_directory))
    _ = get_source_contents(source_filenames)


if __name__ == "__main__":
    main()
