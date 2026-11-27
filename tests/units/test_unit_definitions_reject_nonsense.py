"""A unit definition is built from a name, a symbol, and a dimension, and says so.

A unit built from `None`, or from a dimension that is no `Dimension`, once came out as
a unit and failed far from the line that built it.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import InvalidMeasurementError
from kuchka.dimensions import DIMENSIONLESS
from kuchka.quantities.base.units import AffineUnitDef
from kuchka.quantities.base.units import LogarithmicUnitDef
from kuchka.quantities.base.units import UnitDef


class Dinosaur:
    """Nothing a unit is built from."""


TEXT = {
    "None": None,
    "an integer": 5,
    "a dinosaur": Dinosaur(),
    "a list": ["V"],
    "empty": "",
    "blank": "   ",
}
BUILDERS = {
    "UnitDef": lambda name, symbol: UnitDef(name, symbol, 1, DIMENSIONLESS),
    "AffineUnitDef": lambda name, symbol: AffineUnitDef(name, symbol, 1, 0),
    "LogarithmicUnitDef": lambda name, symbol: LogarithmicUnitDef(name, symbol, 1),
}


@pytest.mark.parametrize("kind", BUILDERS)
@pytest.mark.parametrize("what", TEXT)
def test_the_name_and_the_symbol_are_text_that_says_something(
    kind: str, what: str
) -> None:
    with pytest.raises(InvalidMeasurementError, match="non-empty string"):
        BUILDERS[kind](TEXT[what], "x")
    with pytest.raises(InvalidMeasurementError, match="non-empty string"):
        BUILDERS[kind]("x", TEXT[what])


@pytest.mark.parametrize("kind", BUILDERS)
def test_a_unit_with_a_name_and_a_symbol_is_built(kind: str) -> None:
    unit = BUILDERS[kind]("thing", "t")
    assert (unit.name, unit.symbol) == ("thing", "t")


@pytest.mark.parametrize(
    "dimension", [None, 5, "T", Fraction(1), Dinosaur(), [DIMENSIONLESS], object]
)
def test_the_dimension_of_a_unit_is_a_dimension(dimension: object) -> None:
    with pytest.raises(InvalidMeasurementError, match="needs a Dimension"):
        UnitDef("thing", "t", 1, dimension)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
