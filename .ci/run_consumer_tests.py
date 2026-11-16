"""Build or install Kuchka in an isolated consumer project and test it."""

from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CONSUMER_ROOT = REPOSITORY_ROOT / ".ci" / "consumer"
CONSUMER_PROJECT = CONSUMER_ROOT / "pyproject.toml"
TYPING_CHECKS = CONSUMER_ROOT / "typing_checks"

# The checkers the consumer code is checked with, at the versions `uv.lock` holds.
MYPY = "mypy==2.4.0"
PYRIGHT = "pyright==1.1.414"


def run_step(
    description: str,
    command: Sequence[str],
    *,
    working_directory: Path,
) -> None:
    """Run a command and stream its output to the CI log."""
    print(f"\n=== {description} ===", flush=True)
    print(f"$ {shlex.join(command)}", flush=True)

    # Commands are constructed internally from trusted executables and arguments.
    # Dynamic arguments are generated filesystem paths.
    subprocess.run(  # noqa: S603
        command,
        cwd=working_directory,
        check=True,
        shell=False,
    )


def consumer_python(consumer_directory: Path) -> str:
    """Return the interpreter of the consumer project's environment."""
    # The command is a fixed `uv` invocation inside a generated directory.
    result = subprocess.run(
        [  # noqa: S607
            "uv",
            "run",
            "python",
            "-I",
            "-c",
            "import sys; print(sys.executable)",
        ],
        cwd=consumer_directory,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def run_typing_checks(consumer_directory: Path) -> None:
    """Type-check consumer code against the installed distribution.

    `good.py` must pass as written, and every line of `bad.py` carries a
    `# type: ignore` that the checkers report when the line stops being an error.
    """
    python = consumer_python(consumer_directory)

    run_step(
        "Type-check the consumer code with mypy",
        [
            "uvx",
            "--from",
            MYPY,
            "mypy",
            "--strict",
            "--python-executable",
            python,
            str(TYPING_CHECKS / "good.py"),
            str(TYPING_CHECKS / "bad.py"),
        ],
        working_directory=consumer_directory,
    )
    run_step(
        "Type-check the consumer code with pyright",
        [
            "uvx",
            "--from",
            PYRIGHT,
            "pyright",
            "--pythonpath",
            python,
            "--project",
            str(TYPING_CHECKS / "pyrightconfig.json"),
        ],
        working_directory=consumer_directory,
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
            f"Expected exactly one wheel, found {len(wheels)} in {wheel_directory}"
        )

    return wheels[0]


def run_consumer_tests(
    source: str,
    *,
    version: str | None = None,
    typing: bool = False,
) -> None:
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
            requirement = f"kuchka=={version}" if version else "kuchka"

            run_step(
                f"Resolve and install {requirement} from PyPI",
                [
                    "uv",
                    "add",
                    "--refresh-package",
                    "kuchka",
                    requirement,
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

        if typing:
            run_typing_checks(consumer_directory)


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

    parser.add_argument(
        "--version",
        help="With pypi, install this exact release instead of the latest.",
    )
    parser.add_argument(
        "--typing",
        action="store_true",
        help="Also type-check consumer code against the installed distribution.",
    )

    arguments = parser.parse_args()

    if arguments.version and arguments.source != "pypi":
        parser.error("--version applies to the pypi source only")

    try:
        run_consumer_tests(
            arguments.source,
            version=arguments.version,
            typing=arguments.typing,
        )
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
