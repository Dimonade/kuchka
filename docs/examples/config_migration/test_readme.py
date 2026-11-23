"""The code excerpts in the README are code of the modules, so they cannot drift."""

from __future__ import annotations

import ast
import re
from pathlib import Path

HERE = Path(__file__).parent
NINE = 9
MINIMUM_BLOCKS = 6
README = (HERE / "README.md").read_text(encoding="utf-8")


def _normal(text: str) -> str:
    """Drop whitespace and trailing commas, which a formatter is free to change."""
    return re.sub(r",(?=[)\]}])", "", re.sub(r"\s+", "", text))


SOURCES = [
    _normal(path.read_text(encoding="utf-8"))
    for path in HERE.glob("*.py")
    if not path.name.startswith("test_")
]
BLOCKS = re.findall(r"^```python\n(.*?)^```", README, re.DOTALL | re.MULTILINE)


def test_the_readme_shows_excerpts_of_the_modules() -> None:
    assert len(BLOCKS) >= MINIMUM_BLOCKS


def test_every_python_excerpt_is_code_of_a_module() -> None:
    missing = [
        block
        for block in BLOCKS
        if not any(_normal(block) in source for source in SOURCES)
    ]
    assert not missing, missing


def test_the_readme_states_the_number_of_mistakes_the_ladder_test_holds() -> None:
    tree = ast.parse((HERE / "mistakes.py").read_text(encoding="utf-8"))
    mistakes = next(
        node.value
        for node in tree.body
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id == "MISTAKES"
        and node.value is not None
    )
    assert isinstance(mistakes, ast.Dict)
    assert len(mistakes.keys) == NINE
    assert "a list of nine" in README
