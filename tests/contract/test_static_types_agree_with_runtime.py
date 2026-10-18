"""The static types accept what the runtime accepts, and refuse what it refuses.

A parameter typed `object` lets mypy accept `Degree(30) * Volt(1)`, which the runtime
refuses, and types it as an `Angle`.
Every pair of a representative operand set and every operator is revealed by mypy and
evaluated at runtime, and the two must agree:

- when the runtime refuses, mypy refuses too, or falls back to the weak
  `LinearQuantity | Fraction` that a linear operand and a linear operand or a plain
  number share, because only the dimension decides those results;
- when the runtime answers, mypy does not refuse, and a specific type is the runtime's.
"""

from __future__ import annotations

import importlib.util
import operator
import os
import re
import subprocess
import sys
from typing import TYPE_CHECKING

import pytest

from kuchka import Celsius
from kuchka import Decibel
from kuchka import Degree
from kuchka import Second
from kuchka.quantities.base import LinearQuantity
from tests.support.families import FAMILIES

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


def _static(
    path: Path, index: dict[int, tuple[str, str, str]]
) -> dict[tuple[str, str, str], str | None]:
    """Return mypy's verdict per expression: a type's name, or `None` for a refusal."""
    result = subprocess.run(
        [sys.executable, "-m", "mypy", "--strict", "--no-error-summary", str(path)],
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ},
    )
    verdicts: dict[tuple[str, str, str], str | None] = {}
    for line in result.stdout.splitlines():
        match = re.match(r".*?:(\d+): (error|note): (.*)", line)
        if match is None or int(match.group(1)) not in index:
            continue
        key = index[int(match.group(1))]
        if match.group(2) == "error" and "[operator]" in match.group(3):
            verdicts[key] = None
        elif key not in verdicts and "Revealed type is" in match.group(3):
            revealed = match.group(3).split('"')[1]
            names = {
                part.strip().split(".")[-1]
                for part in re.split(
                    r"\||,", revealed.replace("Union[", "").replace("]", "")
                )
            }
            verdicts[key] = "|".join(sorted(names))
    return verdicts


@pytest.mark.skipif(
    "TOX_ENV_NAME" not in os.environ and importlib.util.find_spec("mypy") is None,
    reason="mypy is not installed",
)
def test_mypy_and_the_runtime_agree_on_every_operand_pair(tmp_path: Path) -> None:
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
    path.write_text("\n".join(lines) + "\n")
    verdicts = _static(path, index)

    mismatches = []
    for (left, symbol, right), static in verdicts.items():
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
                f"{left} {symbol} {right}: mypy {static}, runtime {runtime}"
            )
    assert len(verdicts) == len(index)
    assert not mismatches, "\n".join(mismatches[:20])
