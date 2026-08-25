default:
    just --list

alias fa := format-all
# format all relevant files.
format-all:
    ruff format
    taplo fmt
    prettier --write '**/*.md'

alias dfp := develop-fetch-pull
# Switch to develop, fetch, and pull changes.
develop-fetch-pull:
    git switch develop
    git fetch -p
    git pull -r

alias ct := covtest
# Run coverage on tests and present results.
covtest:
    cd tests
    clear
    coverage erase
    rm -rf htmlcov/
    coverage run --branch -m pytest -s -vv
    coverage report --show-missing
    coverage html
    firefox htmlcov/ &
