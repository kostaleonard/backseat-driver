# Backseat Driver

Software developers want code reviews from colleagues so that they can improve
their code.
But often, a developer's peers are too busy or lack the context to provide
comments.
Backseat Driver prompts a large language model to give a code base a letter
grade for readability, expressiveness, style, and organization.
It also instructs the model to explain its reasoning.
Developers gain the benefits of a code review without needing another engineer.

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
backseat-driver:
  openai-key: ${{ secrets.OPENAI_KEY }}
  fail-under: B
```

## Example output

TODO input program

```python
# TODO input program
```

TODO backseat driver output
