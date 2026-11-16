"""Check the built distributions before anything is published."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tarfile
import tomllib
import zipfile
from email.parser import Parser
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

# The version of twine that validates the long description as PyPI renders it.
TWINE = "twine==7.0.0"


def fail(message: str) -> None:
    """Report a failed check and stop."""
    print(f"FAILED: {message}", file=sys.stderr, flush=True)
    raise SystemExit(1)


def project_version() -> str:
    """Return the version declared in `pyproject.toml`."""
    with (REPOSITORY_ROOT / "pyproject.toml").open("rb") as handle:
        return str(tomllib.load(handle)["project"]["version"])


def check_wheel(wheel: Path, version: str, *, pinned: bool) -> None:
    """Check the contents and the metadata of the wheel."""
    if wheel.name != f"kuchka-{version}-py3-none-any.whl":
        fail(f"unexpected wheel name {wheel.name} for version {version}")

    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        metadata = Parser().parsestr(
            archive.read(f"kuchka-{version}.dist-info/METADATA").decode()
        )

    if "kuchka/py.typed" not in names:
        fail("the wheel does not contain kuchka/py.typed")
    stray = sorted(
        {n.split("/")[0] for n in names} - {"kuchka", f"kuchka-{version}.dist-info"}
    )
    if stray:
        fail(f"the wheel contains top-level entries besides the package: {stray}")
    if metadata["License-Expression"] != "Apache-2.0":
        fail(f"unexpected licence expression {metadata['License-Expression']!r}")
    if metadata["Requires-Python"] != ">=3.11":
        fail(f"unexpected Requires-Python {metadata['Requires-Python']!r}")
    if pinned and "/HEAD/" in metadata.as_string():
        fail("the metadata still links to /HEAD/ although the build is pinned to a tag")


def check_sdist(sdist: Path, version: str) -> None:
    """Check that the source distribution carries what a rebuild needs."""
    with tarfile.open(sdist) as archive:
        names = set(archive.getnames())
    root = f"kuchka-{version}"
    required = {
        f"{root}/pyproject.toml",
        f"{root}/README.md",
        f"{root}/LICENSE-APACHE",
        f"{root}/src/kuchka/py.typed",
    }
    missing = sorted(required - names)
    if missing:
        fail(f"the source distribution lacks {missing}")


def main() -> int:
    """Check the distributions in the directory named on the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="the directory `uv build` wrote")
    parser.add_argument(
        "--pinned",
        action="store_true",
        help="The links were pointed at a tag, so none may still name /HEAD/.",
    )
    arguments = parser.parse_args()

    wheels = sorted(arguments.directory.glob("*.whl"))
    sdists = sorted(arguments.directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        fail(f"expected one wheel and one sdist, found {len(wheels)} and {len(sdists)}")

    version = project_version()
    check_wheel(wheels[0], version, pinned=arguments.pinned)
    check_sdist(sdists[0], version)

    # The command is a fixed `uvx` invocation over the files found above.
    subprocess.run(  # noqa: S603
        [  # noqa: S607
            "uvx",
            "--from",
            TWINE,
            "twine",
            "check",
            "--strict",
            str(wheels[0]),
            str(sdists[0]),
        ],
        check=True,
    )
    print(f"Distributions for {version} passed every check.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
