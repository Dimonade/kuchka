#!/bin/sh
set -eu

usage() {
    echo "Usage: $0 pypi | wheel <wheel-path>" >&2
    exit 2
}

mode="${1:-}"

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)"
repo_root="$(CDPATH= cd -- "$script_dir/.." && pwd -P)"

case "$mode" in
    pypi)
        ;;
    wheel)
        [ "$#" -eq 2 ] || usage

        wheel="$2"

        case "$wheel" in
            /*) ;;
            *) wheel="$PWD/$wheel" ;;
        esac

        [ -f "$wheel" ] || {
            echo "Wheel not found: $wheel" >&2
            exit 1
        }
        ;;
    *)
        usage
        ;;
esac

consumer_dir="$(mktemp -d)"
trap 'rm -rf "$consumer_dir"' EXIT

# Create an independent consumer project.
cp "$repo_root/.ci/consumer/pyproject.toml" "$consumer_dir/pyproject.toml"

cd "$consumer_dir"

# Install the requested distribution.
case "$mode" in
    pypi)
        echo "Installing the latest Kuchka release from PyPI..."
        uv add --refresh kuchka
        ;;
    wheel)
        echo "Installing the locally built Kuchka wheel..."
        uv add "$wheel"
        ;;
esac

# Show exactly which distribution version is being tested.
uv run python -I -c \
    'from importlib.metadata import version; print("Installed Kuchka:", version("kuchka"))'

# Execute the same consumer contract suite in both cases.
uv run python -I -m unittest discover \
    --start-directory "$repo_root/.ci/consumer" \
    --pattern "test_*.py" \
    --verbose