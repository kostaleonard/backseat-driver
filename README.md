# Backseat Driver

Software developers want reviews from colleagues so that they can improve the
code they write.
But often, a developer's peers are too busy or lack the context to provide
comments.
Backseat Driver prompts a large language model to give a code base a letter
grade for readability, expressiveness, and organization.
It also instructs the model to explain its reasoning.
Developers gain the benefits of a code review without needing another engineer.

Backseat Driver is not a linting tool.
Linters check code compliance with a language-specific style guide.
While linters are extremely valuable for promoting readability and
standardizing practices within a team, they don't examine a code base for key
elements that make code relatable to another human being.
For example, linters don't comment on whether function or variable names
express the intent of the author.
They only ensure that names use the correct combination of lower case, upper
case, and other characters.
Linters also do not discuss whether functions or classes have intuitive
interfaces.
Backseat Driver goes beyond linting, looking for deeper ways to improve code.

## Installation

TODO pip install

## Usage

TODO users need to specify an OpenAI API key

### Local

TODO

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

## Example output

You can try Backseat Driver on the input program below to see how it works.
Copy the code below into a file and run Backseat Driver with the following.

TODO show python command to reproduce this output

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

What Backseat Driver says:

> Grade: A
> 
> This code is well-written, easy to read, and well-organized. The function names are clear and descriptive, and the docstrings provide useful information about the functions' purpose and behavior. The code also follows the recommended Python style guidelines (PEP 8), including appropriate indentation, whitespace, and naming conventions. Overall, there are no major issues with the code, and it is highly readable and maintainable.
> 
> One possible improvement could be to add some error handling to the `fib()` and `fact()` functions, for cases where the input is not a positive integer. Another potential improvement could be to add some more comments to explain the logic behind the `hailstone()` function. However, these are minor suggestions and are not necessary for the code to function correctly.
