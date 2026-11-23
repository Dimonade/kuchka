"""The code excerpts in the README are lines of the modules, so they cannot drift."""

from __future__ import annotations

import ast
import re
from pathlib import Path

HERE = Path(__file__).parent
NINE = 9
MINIMUM_BLOCKS = 6
README = (HERE / "README.md").read_text(encoding="utf-8")
SOURCES = {
    line.strip()
    for path in HERE.glob("*.py")
    if not path.name.startswith("test_")
    for line in path.read_text(encoding="utf-8").splitlines()
}
BLOCKS = re.findall(r"^```python\n(.*?)^```", README, re.DOTALL | re.MULTILINE)


def test_the_readme_shows_excerpts_of_the_modules() -> None:
    assert len(BLOCKS) >= MINIMUM_BLOCKS


def test_every_line_of_every_python_excerpt_is_a_line_of_a_module() -> None:
    missing = [
        line.strip()
        for block in BLOCKS
        for line in block.splitlines()
        if line.strip() and line.strip() not in SOURCES
    ]
    assert not missing, missing


def test_the_readme_states_the_number_of_mistakes_the_ladder_test_holds() -> None:
    tree = ast.parse((HERE / "test_ladder.py").read_text(encoding="utf-8"))
    mistakes = next(
        node.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "MISTAKES" for t in node.targets)
    )
    assert isinstance(mistakes, ast.Dict)
    assert len(mistakes.keys) == NINE
    assert "a list of nine" in README
