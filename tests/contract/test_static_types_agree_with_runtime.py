"""The static types accept what the runtime accepts, and refuse what it refuses.

A parameter typed `object` lets mypy accept `Degree(30) * Volt(1)`, which the runtime
refuses, and types it as an `Angle`.
Every pair of a representative operand set and every operator is revealed by each
checker (mypy and pyright) and evaluated at runtime, and they must agree:

- when the runtime refuses, the checker refuses too, or falls back to the weak
  `LinearQuantity | Fraction` that a linear operand and a linear operand or a plain
  number share, because only the dimension decides those results;
- when the runtime answers, the checker does not refuse, and a specific type is the
  runtime's.
"""

from __future__ import annotations

import operator
from typing import TYPE_CHECKING

import pytest

from kuchka import Celsius
from kuchka import Decibel
from kuchka import Degree
from kuchka import Second
from kuchka.quantities.base import LinearQuantity
from tests.support.families import FAMILIES
from tests.support.static_checkers import CHECKERS
from tests.support.static_checkers import require_or_skip
from tests.support.static_checkers import reveal

if TYPE_CHECKING:
    from pathlib import Path

LINEAR = ("Voltage", "Current", "Time", "Frequency", "SampleRate", "Proportion")
OTHER = {
    "Temperature": Celsius(20),
    "Instant": Second(5).to_instant(),
    "Angle": Degree(30),
    "LogarithmicRatio": Decibel(3),
    "int": 2,
}
OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "<": operator.lt,
    ">=": operator.ge,
}
WEAK = {"LinearQuantity", "Fraction"}


def _annotation(name: str) -> str:
    return name if name == "int" else f"kuchka.{name}"


def _operands() -> dict[str, object]:
    by_name = {family.quantity.__name__: family.canonical(12) for family in FAMILIES}
    return {**{name: by_name[name] for name in LINEAR}, **OTHER}


def _runtime(left: object, symbol: str, right: object) -> str | None:
    """Return the result type's name, or `None` when the runtime refuses."""
    try:
        return type(OPERATORS[symbol](left, right)).__name__
    except Exception:  # noqa: BLE001 -- any refusal counts as a refusal
        return None


@pytest.mark.parametrize("checker", CHECKERS)
def test_the_checker_and_the_runtime_agree_on_every_operand_pair(
    checker: str, tmp_path: Path
) -> None:
    require_or_skip(checker)
    operands = _operands()
    lines = ["from __future__ import annotations", "import kuchka"]
    index: dict[int, tuple[str, str, str]] = {}
    for left in operands:
        for right in operands:
            if left == right == "int":
                continue
            lines.append(
                f"def f_{left}_{right}(l: {_annotation(left)}, r: {_annotation(right)})"
                " -> None:"
            )
            for symbol in OPERATORS:
                lines.append(f"    reveal_type(l {symbol} r)")
                index[len(lines)] = (left, symbol, right)
    path = tmp_path / "pairs.py"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    revealed = reveal(checker, path)

    mismatches = []
    for number, (left, symbol, right) in index.items():
        assert number in revealed, (
            f"{checker} said nothing about {left} {symbol} {right}"
        )
        static = revealed[number]
        runtime = _runtime(operands[left], symbol, operands[right])
        sized = (LinearQuantity, int)
        both_sized = isinstance(operands[left], sized) and isinstance(
            operands[right], sized
        )
        weak = static is not None and set(static.split("|")) == WEAK
        if runtime is None:
            ok = static is None or (weak and both_sized)
        else:
            ok = static is not None and (weak or static == runtime)
        if not ok:
            mismatches.append(
                f"{left} {symbol} {right}: {checker} {static}, runtime {runtime}"
            )
    assert not mismatches, "\n".join(mismatches[:20])
