"""A unit definition describes itself, and refuses a scale that is not positive."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import InvalidMeasurementError
from kuchka.quantities.base import AffineUnitDef
from kuchka.quantities.base import LogarithmicUnitDef
from kuchka.quantities.base import UnitDef
from kuchka.units import voltage

ZERO_SCALE_IDS = ["int", "float", "decimal", "fraction"]


def test_the_repr_shows_the_name_and_the_symbol() -> None:
    assert repr(voltage.Volt(1).unit) == "UnitDef('volt', 'V')"


DIMENSION = voltage.Volt(1).dimension
UNIT_DEFINITIONS = [
    pytest.param(lambda scale: UnitDef("test", "t", scale, DIMENSION), id="linear"),
    pytest.param(lambda scale: AffineUnitDef("test", "t", scale, 0), id="affine"),
    pytest.param(
        lambda scale: LogarithmicUnitDef("test", "t", scale), id="logarithmic"
    ),
]


@pytest.mark.parametrize("build", UNIT_DEFINITIONS)
@pytest.mark.parametrize("scale", [0, 0.0, Decimal(0), Fraction(0)], ids=ZERO_SCALE_IDS)
def test_a_zero_scale_is_rejected(build, scale: object) -> None:
    with pytest.raises(InvalidMeasurementError, match="positive scale"):
        build(scale)


@pytest.mark.parametrize("build", UNIT_DEFINITIONS)
@pytest.mark.parametrize("scale", [-1, Fraction(-1, 3)], ids=["int", "fraction"])
def test_a_negative_scale_is_rejected(build, scale: object) -> None:
    with pytest.raises(InvalidMeasurementError, match="positive scale"):
        build(scale)


@pytest.mark.parametrize("build", UNIT_DEFINITIONS)
def test_a_tiny_positive_scale_is_accepted(build) -> None:
    assert build(Fraction(1, 10**30)).scale == Fraction(1, 10**30)


@pytest.mark.parametrize("build", UNIT_DEFINITIONS)
def test_the_scale_error_names_the_unit(build) -> None:
    with pytest.raises(InvalidMeasurementError, match="'test'"):
        build(0)
