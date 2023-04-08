"""Requests a code review from a large language model."""

from argparse import ArgumentParser, Namespace
import glob
import os
import sys

LETTER_GRADES = ["A", "B", "C", "D", "F"]
GPT_3_5_MAX_TOKENS = 4096
APPROXIMATE_NUM_CHARACTERS_PER_TOKEN = 4
# Use a conservative estimate for the number of characters per prompt so that
# the model doesn't cut off something important.
MAX_PROMPT_LENGTH = GPT_3_5_MAX_TOKENS * (APPROXIMATE_NUM_CHARACTERS_PER_TOKEN - 1)


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


def get_prompt(source_contents: list[str], max_length: int | None = None) -> str:
    """Returns the prompt for the language model to perform code review.

    :param source_contents: The contents of all source files to be reviewed.
    :param max_length: The maximum length of the prompt, in characters.
        Language models take a maximum number of tokens (roughly 4 characters;
        somewhere between a syllable and a word) as context. Configuring this
        parameter helps ensure that the model doesn't incorrectly cut off
        important parts of the prompt. If not specified, the prompt will
        contain all source contents.
    """
    prompt = (
        "Give the following code a letter grade based on readability, style, "
        "and structure. Valid letter grades are A (exceptional), B (very "
        "good), C (mediocre), D (poor), and F (unsatisfactory). Explain your "
        "reasoning and give recommendations for improvements. Begin your "
        'response with "Grade: " and the letter grade.\n'
    )
    all_source_contents = "\n".join(source_contents)
    for line in all_source_contents.split("\n"):
        if max_length and len(prompt) + 1 + len(line) > max_length:
            break
        prompt += "\n" + line
    return prompt


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
    source_contents = get_source_contents(source_filenames)
    _ = get_prompt(source_contents, max_length=MAX_PROMPT_LENGTH)


if __name__ == "__main__":
    main()
