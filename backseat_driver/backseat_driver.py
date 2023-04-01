"""Requests a code review from a large language model."""

from argparse import ArgumentParser, Namespace
import sys

LETTER_GRADES = ["A", "B", "C", "D", "F"]


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
        help="The directory to search for source files. The LLM will perform "
        "its code review on these files.",
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
        "--openai_key",
        required=True,
        help="The user's OpenAI API key. Each code review will make a request "
        "on an OpenAI model, which will incur a marginal cost. GPT3.5, "
        "for instance, currently costs $0.002 per 1K tokens.",
    )
    return parser.parse_args(args=args)


def main() -> None:
    """Runs a code review on the user-specified directory."""
    _ = get_args(sys.argv[1:])


if __name__ == "__main__":
    main()
