"""Requests a code review from a large language model."""

from argparse import ArgumentParser, Namespace
import sys


def get_args(args: list[str]) -> Namespace:
    """Returns a Namespace containing the command line arguments.

    :param args: The raw command line arguments. As in argparse, this function
        expects the value to be sys.argv[1:].
    :return: The argparse.Namespace containing the processed command line
        arguments.
    """
    parser = ArgumentParser(
        description="Requests a code review from a large language model."
    )
    # TODO add args, add arg tests, then add CI
    # TODO see README for expected args
    return parser.parse_args(args=args)


def main() -> None:
    """Runs a code review on the user-specified directory."""
    _ = get_args(sys.argv[1:])


if __name__ == "__main__":
    main()
