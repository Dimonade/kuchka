default:
    just --list

browser := env("BROWSER", "firefox")

alias fa := format-all
# Format all relevant files.
format-all:
    uv run ruff format
    taplo fmt
    prettier --write '**/*.md'

alias ck := check
# Check the repository against the current code standards.
check:
    uv run python tools/generate_api.py --check
    uv run python tools/generate_overloads.py --check
    uv run ruff check
    uv run ruff format --check
    uv run mypy --strict --python-version 3.11 src/kuchka
    uv run ty check src/kuchka

alias ts := test
# Run the doctests and the test suite.
test:
    uv run pytest -q --doctest-modules src/kuchka
    uv run pytest -q

alias tx := tox
# Run the doctests, the test suite, and the checks on every supported Python version.
tox:
    uv run tox

alias wt := watch-tools
# Run the checks on the newest tool versions the dependency floors allow, as a scheduled job would.
# `uv run` uses `uv.lock` while tox resolves fresh, so a failure here with `just check` green means a tool moved.
watch-tools:
    uv run tox -e lint,pyright,3.14

alias ga := generate-api
# Regenerate `src/kuchka/_api.py`, the names promoted to the top level, after changing a leaf `__all__`.
generate-api:
    uv run python tools/generate_api.py
    uv run ruff format src/kuchka/_api.py

alias go := generate-overloads
# Regenerate the `*` and `/` overloads of the linear quantity types, after adding or changing a type.
generate-overloads:
    uv run python tools/generate_overloads.py

alias dfp := develop-fetch-pull
# Switch to develop, fetch, and pull changes.
develop-fetch-pull:
    git switch develop
    git fetch -p
    git pull -r

alias ct := covtest
# Run coverage on tests and present results.
covtest: check
    clear
    coverage erase
    coverage run --branch -m pytest --doctest-modules src/kuchka
    coverage run --branch --append -m pytest -s -vv
    coverage report --show-missing
    coverage html
    {{ browser }} htmlcov/ &
