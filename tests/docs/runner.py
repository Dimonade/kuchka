"""Run the Python code blocks of a Markdown document the way a reader would.

A document's blocks run in order in one namespace, so a later block can use what an
earlier one imported or defined.
Each top-level statement is expected to succeed, and the outcome is checked:

- a bare comparison must come out as its comment says, ``# False`` or ``# True``, and
  true when there is none, so a documented equality cannot go stale;
- a statement whose trailing comment names an error in backticks, such as
  ``# rejected: `TypeError`.``, must raise that error, and one that says only
  ``# rejected`` or ``# raises`` must raise something;
- a block preceded by ``<!-- doc-test: skip <reason> -->`` is not run.
"""

from __future__ import annotations

import ast
import builtins
import io
import re
import sys
import tokenize
import types
from dataclasses import dataclass
from typing import TYPE_CHECKING

import kuchka
import kuchka.errors

if TYPE_CHECKING:
    from pathlib import Path

FENCE = re.compile(r"^```python\n(.*?)^```", re.DOTALL | re.MULTILINE)
SKIP = re.compile(r"<!--\s*doc-test:\s*skip\b[^>]*-->\s*$")
ERROR_NAME = re.compile(r"`(\w*(?:Error|Exception))`")
REJECTED = re.compile(r"#\s*(?:rejected|raises)\b")
OUTCOME = re.compile(r"#\s*(True|False)\b")


@dataclass(frozen=True)
class Block:
    """One fenced Python block of a document."""

    source: str
    line: int
    skipped: bool


def blocks_of(text: str) -> list[Block]:
    """Return the Python blocks of a Markdown text, with their first line number."""
    found = []
    for match in FENCE.finditer(text):
        before = text[: match.start()].rstrip().split("\n")[-1]
        line = text[: match.start()].count("\n") + 2
        found.append(Block(match.group(1), line, bool(SKIP.search(before))))
    return found


def comments_after(source: str, statement: ast.stmt) -> list[str]:
    """Return the comment on the last line of `statement`, then one on a line below."""
    row = statement.end_lineno
    found = {}
    alone = set()
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT:
            found[token.start[0]] = token.string
            if token.line.strip().startswith("#"):
                alone.add(token.start[0])
    own = [found[row]] if row in found else []
    following = [found[row + 1]] if row + 1 in alone else []
    return own + following


def expected_error(source: str, statement: ast.stmt) -> type[BaseException] | None:
    """Return the error the trailing comment of `statement` says it raises."""
    for comment in comments_after(source, statement)[:1]:
        named = ERROR_NAME.search(comment)
        if named:
            name = named.group(1)
            return getattr(kuchka.errors, name, None) or getattr(builtins, name)
        if REJECTED.match(comment):
            return Exception
    return None


def expected_truth(source: str, statement: ast.stmt) -> bool:
    """Return the outcome the comments of a comparison give, true when they say none."""
    for comment in comments_after(source, statement):
        outcome = OUTCOME.match(comment)
        if outcome:
            return outcome.group(1) == "True"
    return True


def run(path: Path) -> list[str]:
    """Run every block of `path`; return a description of each statement that failed."""
    failures = []
    module = types.ModuleType("documentation_example")
    sys.modules[module.__name__] = module
    namespace = module.__dict__
    for block in blocks_of(path.read_text(encoding="utf-8")):
        if block.skipped:
            continue
        tree = ast.parse(block.source)
        for statement in tree.body:
            where = f"{path}:{block.line + statement.lineno - 1}"
            unit = ast.Module([statement], [])
            expect = expected_error(block.source, statement)
            try:
                if isinstance(statement, ast.Expr) and isinstance(
                    statement.value, ast.Compare
                ):
                    value = eval(  # noqa: S307 -- documentation code is the input
                        compile(ast.Expression(statement.value), where, "eval"),
                        namespace,
                    )
                    wanted = expected_truth(block.source, statement)
                    if expect is None and value is not wanted:
                        failures.append(
                            f"{where}: documented as {wanted}, evaluates to {value!r}"
                        )
                        continue
                else:
                    exec(compile(unit, where, "exec"), namespace)  # noqa: S102
            except Exception as error:  # noqa: BLE001 -- reported, not hidden
                if expect is not None and isinstance(error, expect):
                    continue
                failures.append(f"{where}: {type(error).__name__}: {str(error)[:100]}")
                continue
            if expect is not None and not (
                isinstance(statement, ast.Expr)
                and isinstance(statement.value, ast.Compare)
            ):
                failures.append(f"{where}: should raise {expect.__name__}, did not")
    del sys.modules[module.__name__]
    return failures
