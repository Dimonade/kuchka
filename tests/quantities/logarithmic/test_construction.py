"""Constructing a `LogarithmicRatio` and showing it in its units."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import LogarithmicRatio
from kuchka.dimensions import DIMENSIONLESS
from kuchka.quantities.base import LogarithmicUnitDef
from kuchka.quantities.base import PureLogarithmicQuantity
from kuchka.units import logarithmic
from kuchka.units import proportion


def test_decibel_is_canonical_and_stored_exactly():
    assert logarithmic.Decibel(3).magnitude == Fraction(3)
    assert logarithmic.Decibel(0.1).magnitude == Fraction(1, 10)


def test_bel_is_ten_decibels():
    assert logarithmic.Bel(1) == logarithmic.Decibel(10)
    assert logarithmic.Bel(1).magnitude == Fraction(10)
    assert logarithmic.Bel(0.35) == logarithmic.Decibel(3.5)


def test_constructors_return_logarithmic_ratio():
    assert isinstance(logarithmic.Decibel(3), LogarithmicRatio)
    assert isinstance(logarithmic.Bel(3), LogarithmicRatio)
    assert isinstance(logarithmic.Decibel(3), PureLogarithmicQuantity)


def test_dimension_is_dimensionless():
    assert LogarithmicRatio.dimension == DIMENSIONLESS


@pytest.mark.parametrize("constructor", [logarithmic.Decibel, logarithmic.Bel])
@pytest.mark.parametrize(
    "bad",
    [True, "3", None, float("nan"), float("inf"), Decimal("NaN")],
    ids=["bool", "str", "none", "nan", "inf", "decimal-nan"],
)
def test_constructors_reject_non_numeric_input(constructor, bad):
    with pytest.raises(InvalidMeasurementError):
        constructor(bad)


def test_logarithmic_unit_def_is_its_own_type():
    assert isinstance(logarithmic.DECIBEL, LogarithmicUnitDef)
    assert isinstance(logarithmic.BEL, LogarithmicUnitDef)
    assert logarithmic.DECIBEL.scale == Fraction(1)
    assert logarithmic.BEL.scale == Fraction(10)
    assert repr(logarithmic.DECIBEL) == "LogarithmicUnitDef('decibel', 'dB')"


def test_units_table_resolves_every_symbol():
    assert logarithmic.LOGARITHMIC_RATIO_UNITS["dB"](3) == logarithmic.Decibel(3)
    assert logarithmic.LOGARITHMIC_RATIO_UNITS["B"](1) == logarithmic.Bel(1)
    assert set(logarithmic.LOGARITHMIC_RATIO_UNITS) == {"dB", "B"}


def test_repr_shows_value_and_display_unit():
    assert repr(logarithmic.Decibel(3)) == "3 dB"
    assert repr(logarithmic.Decibel(-3.5)) == "-3.5 dB"
    assert repr(logarithmic.Bel(2)) == "2 B"


def test_format_spec_applies_to_the_display_value():
    assert f"{logarithmic.Decibel(3.14159):.2f}" == "3.14 dB"
    assert f"{logarithmic.Decibel(3)}" == "3 dB"


def test_to_changes_only_the_display_unit():
    level = logarithmic.Decibel(35).to(logarithmic.BEL)
    assert level == logarithmic.Decibel(35)
    assert level.unit is logarithmic.BEL
    assert repr(level) == "3.5 B"
    assert level.value_in(logarithmic.DECIBEL) == Fraction(35)
    assert level.value_in(logarithmic.BEL) == Fraction(7, 2)


def test_to_rejects_a_dimensionless_unit_of_another_kind():
    """`PERCENT` and `RATIO` are dimensionless too, but they are not levels."""
    with pytest.raises(InvalidConversionError, match="logarithmic unit"):
        logarithmic.Decibel(3).to(proportion.PERCENT)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    with pytest.raises(InvalidConversionError):
        logarithmic.Decibel(3).to(proportion.RATIO)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_to_rejects_a_string():
    with pytest.raises(InvalidConversionError):
        logarithmic.Decibel(3).to("dB")  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
