
"""Build or install Kuchka in an isolated consumer project and test it."""

from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CONSUMER_ROOT = REPOSITORY_ROOT / ".ci" / "consumer"
CONSUMER_PROJECT = CONSUMER_ROOT / "pyproject.toml"


def run_step(
    description: str,
    command: Sequence[str],
    *,
    working_directory: Path,
) -> None:
    """Run a command and stream its output to the CI log."""
    print(f"\n=== {description} ===", flush=True)
    print(f"$ {shlex.join(command)}", flush=True)

    subprocess.run(
        command,
        cwd=working_directory,
        check=True,
    )


def build_wheel(wheel_directory: Path) -> Path:
    """Build the current checkout and return its wheel."""
    wheel_directory.mkdir(parents=True, exist_ok=True)

    run_step(
        "Build wheel from current checkout",
        [
            "uv",
            "build",
            "--wheel",
            "--out-dir",
            str(wheel_directory),
        ],
        working_directory=REPOSITORY_ROOT,
    )

    wheels = sorted(wheel_directory.glob("*.whl"))

    if len(wheels) != 1:
        raise RuntimeError(
            f"Expected exactly one wheel, found {len(wheels)} "
            f"in {wheel_directory}"
        )

    return wheels[0]


def run_consumer_tests(source: str) -> None:
    """Install Kuchka from the selected source and run consumer tests."""
    with tempfile.TemporaryDirectory(prefix="kuchka-consumer-") as temporary:
        temporary_directory = Path(temporary)

        # Create an independent consumer project.
        consumer_directory = temporary_directory / "project"
        consumer_directory.mkdir()

        shutil.copy2(
            CONSUMER_PROJECT,
            consumer_directory / "pyproject.toml",
        )

        if source == "pypi":
            run_step(
                "Resolve and install latest Kuchka release from PyPI",
                [
                    "uv",
                    "add",
                    "--refresh-package",
                    "kuchka",
                    "kuchka",
                ],
                working_directory=consumer_directory,
            )

        elif source == "wheel":
            wheel_directory = temporary_directory / "dist"
            wheel = build_wheel(wheel_directory)

            print(f"\nBuilt distribution: {wheel.name}", flush=True)

            run_step(
                "Install wheel into independent consumer project",
                [
                    "uv",
                    "add",
                    str(wheel),
                ],
                working_directory=consumer_directory,
            )

        # Display the exact installed version.
        run_step(
            "Verify installed distribution",
            [
                "uv",
                "run",
                "python",
                "-I",
                "-c",
                (
                    "from importlib.metadata import version; "
                    "print('Installed Kuchka:', version('kuchka'))"
                ),
            ],
            working_directory=consumer_directory,
        )

        # Execute the consumer contract tests.
        run_step(
            "Run consumer contract tests",
            [
                "uv",
                "run",
                "python",
                "-I",
                "-m",
                "unittest",
                "discover",
                "--start-directory",
                str(CONSUMER_ROOT),
                "--pattern",
                "test_*.py",
                "--verbose",
            ],
            working_directory=consumer_directory,
        )


def main() -> int:
    """Run the selected consumer test workflow."""
    parser = argparse.ArgumentParser(
        description="Test Kuchka as an independently installed dependency."
    )

    parser.add_argument(
        "source",
        choices=("pypi", "wheel"),
        help="Install the latest PyPI release or build and install the current wheel.",
    )

    arguments = parser.parse_args()

    try:
        run_consumer_tests(arguments.source)
    except subprocess.CalledProcessError as error:
        print(
            f"\nFAILED: command exited with status {error.returncode}",
            file=sys.stderr,
            flush=True,
        )
        return error.returncode or 1
    except (OSError, RuntimeError) as error:
        print(f"\nFAILED: {error}", file=sys.stderr, flush=True)
        return 1

    print("\nConsumer validation completed successfully.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
