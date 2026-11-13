# Contributing

Thank you for looking at `kuchka`.
Bug reports, quantity requests, documentation fixes, and code are all welcome.

## Before you start

- A bug or a small fix can go straight to a pull request.
- A new quantity, a new unit family, or a change to how quantities combine starts as
  an issue, because the vocabulary is curated: a name earns a quantity type only
  when it changes an operation or a result. The reasoning is in
  [Dimensional algebra](docs/concepts/dimensional_algebra.md), and the
  [quantity request form](https://github.com/Dimonade/kuchka/issues/new?template=quantity_request.yml)
  asks for what that decision needs.

## Setting up

`kuchka` uses [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/).

```bash
git clone git@github.com:Dimonade/kuchka.git
cd kuchka
uv sync
just --list
```

The recipes you need most:

| Recipe    | What it does                                                      |
| --------- | ----------------------------------------------------------------- |
| `just ck` | Check the code standards: ruff, mypy, ty, and the generated files |
| `just ts` | Run the doctests and the test suite                               |
| `just tx` | Run the checks and the tests on every supported Python version    |
| `just fa` | Format the code, the TOML, and the Markdown                       |
| `just ga` | Regenerate `src/kuchka/_api.py` after changing a leaf `__all__`   |
| `just go` | Regenerate the `*` and `/` overloads after adding a quantity      |
| `just gt` | Regenerate the README table of contents after changing headings   |

## A pull request

- It targets `develop`, which is where work lands. `master` holds the last release.
- It has tests for what it changes, and `just ck` and `just ts` pass.
- It updates the docstrings and the documentation it touches, in the NumPy style.
  [Writing documentation](docs/how-to/writing_documentation.md) says how.
- It adds a short entry to the `develop` section of `CHANGELOG.md`.

The pages under [docs/how-to](docs/how-to/README.md) walk through adding a unit, a
quantity, a dimension, and the tests and documentation each needs.
