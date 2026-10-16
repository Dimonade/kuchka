"""A small table of made-up units, and the helpers that build and read it."""

from __future__ import annotations

from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import LENGTH
from kuchka.internal.unit_table import unit_table
from kuchka.quantities.base import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable

    from kuchka.numeric import Numeric


def make_unit(name: str, symbol: str, **spellings: tuple[str, ...]) -> UnitDef:
    return UnitDef(name, symbol, Fraction(1), LENGTH, **spellings)


def make_ctor(label: str) -> Callable[[Numeric], tuple[str, Numeric]]:
    def construct(value: Numeric) -> tuple[str, Numeric]:
        return (label, value)

    return construct


MILLI = make_unit("millix", "mx")


MEGA = make_unit("megax", "Mx")


BASE = make_unit("basex", "x", aliases=("ex",), words=("base unit x", "the x"))


TABLE = unit_table(
    "TEST_UNITS",
    {
        MILLI: make_ctor("milli"),
        MEGA: make_ctor("mega"),
        BASE: make_ctor("base"),
    },
)


def resolves_to(text: str) -> str:
    return TABLE[text](1)[0]
