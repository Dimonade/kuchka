"""The documentation of a unit module has the structure that the how-to describes.

A module has a title, an `Examples` section, and `Notes`.
A public constructor has `Parameters`, `Returns`, and `Examples` with at least two
examples, each of which opens with a sentence, and the first of which shows the
constructor itself with its result.
Imports in the examples name one thing per line and come from the public paths, and an
error is written in the traceback form with an ellipsis.

Modules that predate the structure are listed in the baseline.
A module in the baseline must still fall short, so the list only shrinks.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

import kuchka

UNITS = Path(kuchka.__file__).resolve().parent / "units"
BASELINE = Path(__file__).with_name("unit_docstring_baseline.txt")

TITLE = re.compile(r"^[A-Z].* (constructors|units): .+\.$")
HEADING = re.compile(r"^(\w[\w ]*)\n-{3,}$", re.MULTILINE)
IMPORT = re.compile(r"^\s*>>> (?:from (\S+) import (.+)|import (\S+))$", re.MULTILINE)
PUBLIC_IMPORTS = ("kuchka.constants", "kuchka.errors", "kuchka.units.archaic")
MINIMUM_EXAMPLES = 2
MODULE_SECTIONS = ("Examples", "Notes", "References", "See Also")
CONSTRUCTOR_SECTIONS = ("Parameters", "Returns", "Notes", "Examples")


def modules() -> list[Path]:
    """Return the leaf unit modules that follow the structure."""
    return sorted(
        path
        for path in UNITS.rglob("*.py")
        if path.name != "__init__.py" and "archaic" not in path.parts
    )


def dotted(path: Path) -> str:
    """Return the dotted name of the module at `path`."""
    return ".".join(("kuchka", "units", *path.relative_to(UNITS).with_suffix("").parts))


def baseline() -> set[str]:
    """Return the modules that are not yet held to the structure."""
    lines = (line.strip() for line in BASELINE.read_text().splitlines())
    return {line for line in lines if line and not line.startswith("#")}


def sections(docstring: str) -> dict[str, str]:
    """Return the body of each section of `docstring`, by heading."""
    found = list(HEADING.finditer(docstring))
    return {
        heading.group(1): docstring[
            heading.end() : found[index + 1].start()
            if index + 1 < len(found)
            else len(docstring)
        ]
        for index, heading in enumerate(found)
    }


def in_order(found: list[str], expected: tuple[str, ...]) -> bool:
    """Return whether `found` lists the `expected` headings in their order."""
    known = [heading for heading in found if heading in expected]
    return known == sorted(known, key=expected.index)


def examples(body: str) -> list[tuple[bool, list[str]]]:
    """Split an `Examples` body into blocks of a scenario and its code.

    Each block is a flag for whether prose opens it, and its code lines.
    """
    blocks: list[tuple[bool, list[str]]] = []
    for chunk in re.split(r"\n\s*\n", body.strip()):
        if chunk.lstrip().startswith(">>>"):
            if not blocks:
                blocks.append((False, []))
            blocks[-1][1].extend(chunk.splitlines())
        elif not blocks or blocks[-1][1]:
            blocks.append((True, []))
    return blocks


def style_problems(label: str, docstring: str) -> list[str]:
    """Return the problems with the imports and the tracebacks of `docstring`."""
    problems = []
    for match in IMPORT.finditer(docstring):
        source, names, plain = match.groups()
        if plain or source is None:
            continue
        public = source in ("kuchka", "kuchka.units") or source.startswith(
            PUBLIC_IMPORTS
        )
        if source.startswith("kuchka") and not public:
            problems.append(f"{label}: imports from `{source}`, which is not public")
        if "," in names:
            problems.append(f"{label}: imports several names on one line")
    lines = docstring.splitlines()
    for number, line in enumerate(lines):
        opens = line.startswith("Traceback (most recent call last):")
        if opens and "+ELLIPSIS" not in lines[number - 1]:
            problems.append(f"{label}: a traceback needs `# doctest: +ELLIPSIS`")
    return problems


def constructor_problems(function: ast.FunctionDef) -> list[str]:
    """Return the problems with the docstring of a constructor."""
    name = function.name
    docstring = ast.get_docstring(function)
    if docstring is None:
        return [f"{name}: no docstring"]
    found = sections(docstring)
    problems = style_problems(name, docstring)
    for heading in ("Parameters", "Returns", "Examples"):
        if heading not in found:
            problems.append(f"{name}: no `{heading}` section")
    if not in_order(list(found), CONSTRUCTOR_SECTIONS):
        problems.append(f"{name}: sections are out of order")
    blocks = examples(found.get("Examples", ""))
    if len(blocks) < MINIMUM_EXAMPLES:
        problems.append(f"{name}: needs at least two examples")
    problems += [
        f"{name}: an example has no sentence that sets the scene"
        for scene, _ in blocks
        if not scene
    ]
    if blocks:
        first = blocks[0][1]
        calls = any(re.search(rf"\b{name}\(", line) for line in first)
        shows = any(line and not line.startswith((">>>", "...")) for line in first)
        if not (calls and shows):
            problems.append(f"{name}: the first example shows `{name}` and its result")
    return problems


def module_problems(path: Path) -> list[str]:
    """Return the problems with the documentation of the module at `path`."""
    tree = ast.parse(path.read_text())
    docstring = ast.get_docstring(tree)
    if docstring is None:
        return ["no module docstring"]
    found = sections(docstring)
    problems = style_problems("module", docstring)
    if not TITLE.match(docstring.splitlines()[0]):
        problems.append("the title is `<Quantity> constructors: ...` or `units: ...`")
    for heading in ("Examples", "Notes"):
        if heading not in found:
            problems.append(f"module: no `{heading}` section")
    if not in_order(list(found), MODULE_SECTIONS):
        problems.append("module: sections are out of order")
    problems += [
        "module: an example has no sentence that sets the scene"
        for scene, _ in examples(found.get("Examples", ""))
        if not scene
    ]
    for function in tree.body:
        if isinstance(function, ast.FunctionDef) and function.name[0].isupper():
            problems += constructor_problems(function)
    return problems


HELD = [path for path in modules() if dotted(path) not in baseline()]
LISTED = [path for path in modules() if dotted(path) in baseline()]


@pytest.mark.parametrize("path", HELD, ids=[dotted(path) for path in HELD])
def test_a_unit_module_has_the_documented_structure(path: Path) -> None:
    problems = module_problems(path)
    assert not problems, "\n".join(problems)


@pytest.mark.parametrize("path", LISTED, ids=[dotted(path) for path in LISTED])
def test_a_module_in_the_baseline_still_falls_short(path: Path) -> None:
    problems = module_problems(path)
    assert problems, f"{dotted(path)} conforms: remove it from the baseline"


def test_the_baseline_lists_only_modules_that_exist() -> None:
    assert baseline() <= {dotted(path) for path in modules()}


def function(source: str) -> ast.FunctionDef:
    """Return the function that `source` defines."""
    definition = ast.parse(source).body[0]
    assert isinstance(definition, ast.FunctionDef)
    return definition


def test_a_constructor_without_examples_is_reported() -> None:
    bare = function(
        'def Metre(value):\n    """Construct a Length.\n\n    Parameters\n'
        "    ----------\n    value : Numeric\n        The magnitude.\n\n    Returns\n"
        '    -------\n    Length\n        The length.\n    """\n'
    )
    problems = constructor_problems(bare)
    assert "Metre: no `Examples` section" in problems
    assert "Metre: needs at least two examples" in problems


def test_an_example_that_opens_with_code_is_reported() -> None:
    body = ">>> Metre(1)\n1 m\n\nA sentence.\n\n>>> Metre(2)\n2 m"
    blocks = examples(body)
    assert blocks == [(False, [">>> Metre(1)", "1 m"]), (True, [">>> Metre(2)", "2 m"])]
