"""Requests a code review from a large language model."""

from argparse import ArgumentParser, Namespace
import sys


def get_args(args: list[str]) -> Namespace:
    """Returns a Namespace containing the command line arguments.

    :param args: The raw command line arguments; sys.argv.
    """
    # TODO


def main() -> None:
    """Runs a code review on the user-specified directory."""
    args = get_args(sys.argv)
    # TODO


if __name__ == "__main__":
    main()
