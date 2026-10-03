default:
    just --list

alias fa := format-all
# format all relevant files.
format-all:
    ruff format
    taplo fmt
    prettier --write '**/*.md'

# Check the repository against the current code standards.
check:
    uv run python tools/generate_api.py --check
    uv run ruff check
    uv run mypy --strict --python-version 3.11 src/kuchka
    uv run ty check src/kuchka


alias ga := generate-api
# Regenerate `src/kuchka/_api.py`, the names promoted to the top level, after changing a leaf `__all__`.
generate-api:
    uv run python tools/generate_api.py
    uv run ruff format src/kuchka/_api.py

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
    firefox htmlcov/ &
