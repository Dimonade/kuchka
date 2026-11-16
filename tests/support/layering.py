"""The import order of the themed packages, checked from the source of each leaf."""

from __future__ import annotations

import ast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def leaves(root: Path, *, skip: frozenset[str] = frozenset()) -> list[Path]:
    """Return every leaf module under `root`, except the packages named in `skip`."""
    return sorted(
        path
        for path in root.rglob("*.py")
        if path.name != "__init__.py" and skip.isdisjoint(path.relative_to(root).parts)
    )


def package_of(root: Path, leaf: Path) -> str:
    """Return the package a leaf sits in, the empty string for the top level."""
    parts = leaf.relative_to(root).parts
    return parts[0] if len(parts) > 1 else ""


def imported_packages(leaf: Path, package: str, rank: dict[str, int]) -> set[str]:
    """Return the packages a leaf imports from when it is imported.

    Only statements that run at import time count: an import under `TYPE_CHECKING`
    or inside a function does not.
    The empty string stands for the top level.
    """
    prefix = package.split(".")
    found: set[str] = set()
    for node in ast.parse(leaf.read_text(encoding="utf-8")).body:
        if not isinstance(node, ast.ImportFrom) or node.module is None:
            continue
        parts = node.module.split(".")
        if parts[: len(prefix)] != prefix:
            continue
        tail = parts[len(prefix) :]
        names = [alias.name for alias in node.names] if not tail else tail[:1]
        found.update(name if name in rank else "" for name in names)
    return found


def violations(root: Path, package: str, rank: dict[str, int], leaf: Path) -> list[str]:
    """Return a message for each import of `leaf` that runs against the order."""
    own = package_of(root, leaf)
    return [
        f"{leaf.relative_to(root)} imports from {imported or 'the top level'}, "
        f"which does not come before {own or 'the top level'}"
        for imported in sorted(imported_packages(leaf, package, rank))
        if imported != own and rank[imported] >= rank[own]
    ]
