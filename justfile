default:
    just --list

alias fa := format-all
# format all relevant files.
format-all:
    ruff format
    taplo fmt
    prettier --write '**/*.md'

# Type-check with mypy --strict and ty.
typecheck:
    uv run mypy --strict src/kuchka
    uv run ty check src/kuchka tests


alias dfp := develop-fetch-pull
# Switch to develop, fetch, and pull changes.
develop-fetch-pull:
    git switch develop
    git fetch -p
    git pull -r

alias ct := covtest
# Run coverage on tests and present results.
covtest: typecheck
    cd tests
    clear
    coverage erase
    rm -rf htmlcov/
    coverage run --branch -m pytest -s -vv
    coverage report --show-missing
    coverage html
    firefox htmlcov/ &
