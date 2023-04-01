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
For example, linters don't comment on function or variable names except to
ensure that they use the correct combination of lower case, upper case, and
other characters.
Linters also do not discuss whether a function or class has a sensible
interface with which to interact.
Backseat Driver fills this gap.

TODO revise above

## Installation

TODO pip install

## Usage

TODO users need to specify an OpenAI API key

### Local

TODO

### GitHub Actions

TODO

```yaml
# TODO this config should have a fail-under entry for the letter grade. Here, code must score at least a B
# TODO not sure what source-directory should be in GitHub Actions
backseat-driver:
  openai-key: ${{ secrets.OPENAI_KEY }}
  fail-under: B
  source-directory: /
```

## Example output

TODO input program

```python
# TODO input program
```

TODO backseat driver output
