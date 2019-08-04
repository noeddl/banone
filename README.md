# banone

A generator for joke riddles that combine two words into a pun

## Requirements

1. Python 3.6+
2. [Poetry](https://github.com/sdispater/poetry) for dependency management and packaging. Install with `pip install poetry`.

## Build and run

```
poetry install
poetry build
```

Now you can generate all currently possible riddles.

```
banone-run
```

## Development and tests

`banone` comes with some [pre-commit](https://pre-commit.com/) hooks for easy validation and formatting. After cloning the repo and building the project, run

```
pre-commit install
```

From now on, the pre-commit hooks will be run on every commit.

Run the test suite:

```
pytest
```
