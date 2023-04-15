# Backseat Driver

Requests a code review from a large language model.

Software developers want reviews so that they can improve their code.
But developers are busy.
Peers may be unavailable or lack the context to provide comments.
Backseat Driver prompts a large language model to give code a letter grade for
readability, expressiveness, and organization.
It also instructs the model to explain its reasoning.
Developers gain the benefits of code review without needing another engineer.

## Installation

```shell
pip install backseat-driver
```

## Usage

Users need to [create an OpenAI account](https://platform.openai.com/signup)
and API key.
Backseat Driver needs the API key to be able to request code review from a
language model.
Set the `OPENAI_API_KEY` environment variable to your API key.

Note that OpenAI will charge your account for Backseat Driver's requests.
Each Backseat Driver invocation will make a request of at most 4096 tokens on a
language model.
[ChatGPT's current pricing model](https://openai.com/pricing) is $0.002 per 1K
tokens.
At this price, users can expect each call to Backseat Driver to cost
$0.002 * 4.096 = $0.008192, or just under 1 cent.

### Local

Run Backseat Driver on the command line with the following.

```shell
backseat-driver my_script.py
```

Provide multiple scripts for simultaneous code review of all given files.

```shell
backseat-driver script1.py script2.py script3.py
```

Wildcard operators also work as expected.

```shell
backseat-driver *.py
```

Set the `fail_under` flag to cause Backseat Driver to exit with an error if the
model gives the code a lower grade than what you have specified.

```shell
backseat-driver --fail_under B *.py
```

### GitHub Actions

TODO

```yaml
# TODO not sure what source-directory should be in GitHub Actions
backseat-driver:
  openai_api_key: ${{ secrets.OPENAI_API_KEY }}
  fail_under: B
  source_directory: /
  filter_files_by_suffix: ".py"
```

## Help

```console
foo@bar:~$ backseat-driver -h
usage: backseat-driver [-h] [--fail_under {A,B,C,D}] filenames [filenames ...]

Requests a code review from a large language model (LLM). The model will grade the code based on readability, expressiveness, and organization. The output will include a letter grade in ['A', 'B', 'C', 'D', 'F'], as well as the model's reasoning.

positional arguments:
  filenames             The files to pass to the LLM for code review.

options:
  -h, --help            show this help message and exit
  --fail_under {A,B,C,D}
                        If specified, exit with non-zero status if the LLM's grade falls below the given value. This value is not inclusive: if this value is "B" and the LLM gives a final grade of "B," then the program will exit with a zero status. If not specified, then the program will exit with a zero status no matter the LLM's grade.
```

## Example output

You can try Backseat Driver on the input program below to see how it works.
Copy the code into `test.py`.

```python
"""A file for testing prompt creation."""


def fib(n):
    """Returns the nth fibonacci number."""
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


def fact(n):
    """Returns n factorial."""
    if n <= 1:
        return 1
    return n * fact(n - 1)


def hailstone(n):
    """Returns the hailstone sequence starting with positive integer n."""
    if n <= 0:
        raise ValueError(f"Cannot compute hailstone of negative number {n}")
    if n == 1:
        return [n]
    if n % 2 == 0:
        return [n] + hailstone(n // 2)
    return [n] + hailstone(3 * n + 1)

```

Run Backseat Driver with the following.

```shell
backseat-driver test.py
```

What Backseat Driver says:

> Grade: A
> 
> This code is well-written, easy to read, and well-organized. The function names are clear and descriptive, and the docstrings provide useful information about the functions' purpose and behavior. The code also follows the recommended Python style guidelines (PEP 8), including appropriate indentation, whitespace, and naming conventions. Overall, there are no major issues with the code, and it is highly readable and maintainable.
> 
> One possible improvement could be to add some error handling to the `fib()` and `fact()` functions, for cases where the input is not a positive integer. Another potential improvement could be to add some more comments to explain the logic behind the `hailstone()` function. However, these are minor suggestions and are not necessary for the code to function correctly.
