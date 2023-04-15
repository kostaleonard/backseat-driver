"""Requests a code review from a large language model."""

from argparse import ArgumentParser, Namespace
import sys
import openai

LETTER_GRADES = ["A", "B", "C", "D", "F"]
MODEL = "gpt-3.5-turbo"
GPT_3_5_MAX_TOKENS = 4096
APPROXIMATE_NUM_CHARACTERS_PER_TOKEN = 4
# Use a conservative estimate for the number of characters per prompt so that
# the model doesn't cut off something important.
MAX_PROMPT_LENGTH = GPT_3_5_MAX_TOKENS * (APPROXIMATE_NUM_CHARACTERS_PER_TOKEN - 1)


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
        "reasoning and give recommendations for improvements. Don't suggest "
        'adding comments to the code. Begin your response with "Grade: " and '
        "the letter grade.\n"
    )
    all_source_contents = "\n".join(source_contents)
    for line in all_source_contents.split("\n"):
        if max_length and len(prompt) + 1 + len(line) > max_length:
            break
        prompt += "\n" + line
    return prompt


def get_model_prediction(prompt: str) -> dict:
    """Returns the language model's response to the prompt.

    :param prompt: The body of a prompt for the language model.
    """
    return openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a code review assistant."},
            {"role": "user", "content": prompt},
        ],
    )


def get_grade_from_prediction(prediction: dict) -> str:
    """Return the letter grade from the prediction.

    Raises a ValueError if the prediction does not start with "Grade: " and
    then a valid letter grade.
    """
    code_review_message = prediction["choices"][0]["message"]["content"]
    grade_prefix = "grade: "
    if not code_review_message.lower().startswith(grade_prefix):
        raise ValueError("Code review message in prediction does not start with grade.")
    grade = code_review_message[len(grade_prefix)].upper()
    if grade not in LETTER_GRADES:
        raise ValueError(
            f"Model prediction does not contain a letter grade:\n{prediction}"
        )
    return grade


def is_grade_under(grade, fail_under) -> bool:
    """Returns True if the grade is under (worse than) than the benchmark.

    :param grade: The model's predicted grade.
    :param fail_under: The benchmark grade.
    """
    return LETTER_GRADES.index(grade) > LETTER_GRADES.index(fail_under)


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
        "filenames", nargs="+", help="The files to pass to the LLM for code review."
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
    return parser.parse_args(args=args)


def main() -> None:
    """Runs a code review on the user-specified directory."""
    args = get_args(sys.argv[1:])
    source_contents = get_source_contents(args.filenames)
    prompt = get_prompt(source_contents, max_length=MAX_PROMPT_LENGTH)
    print(f"Prompt:\n{prompt}")
    print("=" * 79)
    prediction = get_model_prediction(prompt)
    code_review_message = prediction["choices"][0]["message"]["content"]
    print(f"Response:\n{code_review_message}")
    if args.fail_under:
        grade = get_grade_from_prediction(prediction)
        if is_grade_under(grade, args.fail_under):
            raise ValueError(
                f"Returned grade did not meet fail_under criteria: {grade} < {args.fail_under}"
            )


if __name__ == "__main__":
    main()
