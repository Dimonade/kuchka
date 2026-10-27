"""Generate the `@overload` declarations of `*` and `/` on every linear quantity type.

A type checker cannot infer "Voltage times Current is Power" from dimension algebra, so
each linear quantity type declares the result of `*` and `/` for every operand type as
an overload.
The runtime already knows each of those results: it is the registry (the dimension of
every kind, which kinds are principal or contested, and the declared rules).
This tool reads the results back by running the operators on one value of each pair of
types, so the declarations are never typed by hand and cannot disagree with the
runtime.

Each declaration list sits between `# BEGIN GENERATED <method>` and `# END GENERATED`
in its class, and the `TYPE_CHECKING` imports of the quantity types a module names are
recomputed from the names the module uses.
Everything else in a module, including the implementation each list is followed by, is
hand-written.

    uv run python tools/generate_overloads.py          # rewrite the modules
    uv run python tools/generate_overloads.py --check  # exit 1 if one is out of date
"""

from __future__ import annotations

import argparse
import ast
import inspect
import operator
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from kuchka import quantities
from kuchka.errors import MeasurementError
from kuchka.quantities.base import LinearQuantity

BEGIN = "# BEGIN GENERATED"
END = "# END GENERATED"
INDENT = "    "
FALLBACK = "other: LinearQuantity | Numeric) -> LinearQuantity | Fraction"
OPERATIONS: dict[str, Callable[[LinearQuantity, LinearQuantity], object]] = {
    "__mul__": operator.mul,
    "__truediv__": operator.truediv,
}
RECIPROCAL = "__rtruediv__"


def linear_types() -> list[type[LinearQuantity]]:
    """Return every concrete linear quantity type `kuchka.quantities` publishes."""
    found = []
    for name in quantities.__all__:
        cls = getattr(quantities, name)
        if (
            isinstance(cls, type)
            and issubclass(cls, LinearQuantity)
            and cls is not LinearQuantity
            and "dimension" in vars(cls)
        ):
            found.append(cls)
    return sorted(found, key=lambda cls: cls.__name__)


def sample(cls: type[LinearQuantity], magnitude: int) -> LinearQuantity:
    """Return `magnitude` of the canonical unit of `cls`."""
    return cls(Fraction(magnitude), cls._canonical_unit)


def combined(
    operation: Callable[[LinearQuantity, LinearQuantity], object],
    left: type[LinearQuantity],
    right: type[LinearQuantity],
) -> str | None:
    """Return the type `left <operation> right` is, or `None` if the runtime refuses."""
    try:
        result = operation(sample(left, 12), sample(right, 3))
    except (MeasurementError, TypeError):
        return None
    return type(result).__name__


def reciprocal_of(cls: type[LinearQuantity]) -> str | None:
    """Return the type a plain number divided by `cls` is, or `None` if it refuses."""
    try:
        result = Fraction(12) / sample(cls, 3)
    except (MeasurementError, TypeError):
        return None
    return type(result).__name__


def declarations(types: list[type[LinearQuantity]]) -> dict[str, dict[str, list[str]]]:
    """Return, per type name and method, the lines of its overloads in canonical order.

    A quantity operand comes before the plain number, which comes before the fallback,
    and quantity operands are sorted by name.
    No operand type is a subclass of another, so the order never changes what a type
    checker infers.
    """
    for first in types:
        for second in types:
            if first is not second and issubclass(first, second):
                msg = f"{first.__name__} is a subclass of {second.__name__}"
                raise SystemExit(f"overload order would matter: {msg}")
    out: dict[str, dict[str, list[str]]] = {}
    for left in types:
        methods: dict[str, list[str]] = {}
        for method, operation in OPERATIONS.items():
            pairs = []
            for right in types:
                name = combined(operation, left, right)
                if name is not None:
                    pairs.append((right.__name__, name))
            pairs.append(("Numeric", left.__name__))
            methods[method] = _overloads(method, pairs)
        reciprocal = reciprocal_of(left)
        if reciprocal is not None:
            methods[RECIPROCAL] = _overloads(RECIPROCAL, [("Numeric", reciprocal)])
        out[left.__name__] = methods
    return out


def _overloads(method: str, pairs: list[tuple[str, str]]) -> list[str]:
    lines = []
    for operand, result in pairs:
        lines += [
            f"{INDENT}@overload",
            f"{INDENT}def {method}(self, other: {operand}) -> {result}: ...",
        ]
    lines += [f"{INDENT}@overload", f"{INDENT}def {method}(self, {FALLBACK}: ..."]
    return lines


def _is_overload(node: ast.stmt, method: str) -> bool:
    return (
        isinstance(node, ast.FunctionDef)
        and node.name == method
        and any(
            isinstance(d, ast.Name) and d.id == "overload" for d in node.decorator_list
        )
    )


def _standard_implementation(method: str) -> list[str]:
    return [
        f"{INDENT}@override",
        f"{INDENT}def {method}(self, {FALLBACK}:",
        f"{INDENT * 2}return super().{method}(other)",
    ]


def _region(method: str, overloads: list[str]) -> list[str]:
    return [f"{INDENT}{BEGIN} {method}", *overloads, f"{INDENT}{END}"]


def place(
    lines: list[str], cls_name: str, method: str, overloads: list[str]
) -> list[str]:
    """Return `lines` with the overloads of `method` in `cls_name` written out."""
    tree = ast.parse("\n".join(lines))
    node = next(
        n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls_name
    )
    region = _region(method, overloads)
    start_marker = f"{INDENT}{BEGIN} {method}"
    inside = range(node.lineno - 1, node.end_lineno)
    begin = next((i for i in inside if lines[i].rstrip() == start_marker), None)
    if begin is not None:
        end = next(i for i in range(begin, node.end_lineno) if lines[i].strip() == END)
        return [*lines[:begin], *region, *lines[end + 1 :]]
    positions = [i for i, n in enumerate(node.body) if _is_overload(n, method)]
    if positions:
        if positions != list(range(positions[0], positions[-1] + 1)):
            raise SystemExit(f"{cls_name}.{method}: the overloads are not contiguous")
        first = node.body[positions[0]]
        first_line = min([first.lineno, *(d.lineno for d in first.decorator_list)])
        last = node.body[positions[-1]]
        return [*lines[: first_line - 1], *region, *lines[last.end_lineno :]]
    addition = ["", *region, "", *_standard_implementation(method)]
    return [*lines[: node.end_lineno], *addition, *lines[node.end_lineno :]]


def _quantity_imports(tree: ast.Module) -> list[ast.ImportFrom]:
    """Return the `TYPE_CHECKING` imports of quantity types, which this tool owns."""
    found = []
    for node in tree.body:
        if isinstance(node, ast.If) and "TYPE_CHECKING" in ast.unparse(node.test):
            found += [
                n
                for n in node.body
                if isinstance(n, ast.ImportFrom)
                and n.module is not None
                and n.module.startswith("kuchka.quantities.")
                and not n.module.startswith("kuchka.quantities.base")
            ]
    return found


def _needed_type_imports(tree: ast.Module, homes: dict[str, str]) -> dict[str, str]:
    """Return the quantity types a module names without defining or importing them."""
    bound = {n.name for n in tree.body if isinstance(n, ast.ClassDef)}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            bound.update(alias.asname or alias.name for alias in node.names)
    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    return {name: homes[name] for name in sorted(used & homes.keys() - bound)}


def fix_imports(text: str, homes: dict[str, str]) -> str:
    """Return `text` with the quantity imports under `TYPE_CHECKING` recomputed."""
    tree = ast.parse(text)
    lines = text.splitlines()
    owned = _quantity_imports(tree)
    block = next(
        n
        for n in tree.body
        if isinstance(n, ast.If) and "TYPE_CHECKING" in ast.unparse(n.test)
    )
    wanted = _needed_type_imports(tree, homes)
    drop = {i for n in owned for i in range(n.lineno - 1, n.end_lineno or n.lineno)}
    anchor = block.body[0].lineno - 1
    new = [f"{INDENT}from {module} import {name}" for name, module in wanted.items()]
    out = []
    for index, line in enumerate(lines):
        if index == anchor:
            out += new
        if index not in drop:
            out.append(line)
    return "\n".join(out) + "\n"


def tidy(text: str, path: Path) -> str:
    """Return `text` with its imports sorted and pruned, formatted like the project."""
    for command in (
        ["check", "--fix-only", "--exit-zero", "--select", "I001,F401"],
        ["format"],
    ):
        text = subprocess.run(  # noqa: S603
            [
                sys.executable,
                "-m",
                "ruff",
                *command,
                "--stdin-filename",
                str(path),
                "-",
            ],
            input=text,
            capture_output=True,
            text=True,
            check=True,
            cwd=ROOT,
        ).stdout
    return text


def generate() -> dict[Path, str]:
    """Return the new text of every module whose text the tool changes."""
    types = linear_types()
    wanted = declarations(types)
    homes = {
        name: published.__module__
        for name in quantities.__all__
        if isinstance(published := getattr(quantities, name), type)
        and published.__module__.startswith("kuchka.quantities.")
        and not published.__module__.startswith("kuchka.quantities.base")
    }
    changed: dict[Path, str] = {}
    for cls in types:
        path = Path(inspect.getsourcefile(cls) or "")
        text = changed.get(path, path.read_text(encoding="utf-8"))
        lines = text.splitlines()
        for method, overloads in wanted[cls.__name__].items():
            lines = place(lines, cls.__name__, method, overloads)
        changed[path] = "\n".join(lines) + "\n"
    result = {}
    for path, text in changed.items():
        tidied = tidy(fix_imports(text, homes), path)
        if tidied != path.read_text(encoding="utf-8"):
            result[path] = tidied
    return result


def main() -> int:
    """Rewrite the modules, or with `--check` report the ones that are out of date."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="exit 1 if out of date")
    arguments = parser.parse_args()
    stale = generate()
    if arguments.check:
        for path in sorted(stale):
            sys.stderr.write(f"{path.relative_to(ROOT)} is out of date.\n")
        if stale:
            sys.stderr.write("Run `just generate-overloads`.\n")
        return 1 if stale else 0
    for path, text in stale.items():
        path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
