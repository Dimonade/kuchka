"""Proportion: a dimensionless quantity, and its arithmetic with the rest of the vocab.

Unlike `Frequency`/`SampleRate`/`BaudRate`, `Percent` and `Ratio` are not
different concepts sharing a dimension -- they are the same quantity at
different scale, the same relationship `Volt`/`Millivolt` has. The
interesting part of this module is proving that `Proportion` never
needed any new arithmetic: multiplying or dividing an existing quantity
by a `Proportion` already produces the correctly-typed result through
the same general dimension algebra every other quantity uses, and a
dimensionless result between two same-type quantities still collapses to
a bare `Decimal`, exactly as it did before `Proportion` existed.
"""

from decimal import Decimal

import pytest
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Ohm
from kuchka import Percent
from kuchka import Proportion
from kuchka import Ratio
from kuchka import Volt
from kuchka import Voltage


def test_percent_and_ratio_are_the_same_quantity_at_different_scale():
    assert Percent(5) == Ratio(Decimal("0.05"))
    assert Percent(100) == Ratio(1)


def test_addition_across_percent_and_ratio_is_exact():
    total = Percent(5) + Ratio(Decimal("0.05"))
    assert total == Percent(10)
    assert total == Ratio(Decimal("0.1"))


def test_isinstance_of_proportion():
    assert isinstance(Percent(5), Proportion)
    assert isinstance(Ratio(Decimal("0.5")), Proportion)


def test_scalar_multiplication_and_division():
    assert Percent(5) * 2 == Percent(10)
    assert Ratio(Decimal("0.5")) / 2 == Ratio(Decimal("0.25"))


def test_ordering_within_proportion():
    assert Percent(5) < Percent(10)
    assert Ratio(Decimal("0.5")) > Percent(10)


def test_naked_number_addition_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Percent(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_proportion_is_incompatible_with_a_dimensioned_quantity():
    with pytest.raises(IncompatibleDimensionError):
        Percent(5) + Volt(5)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types

    assert (Percent(5) == Volt(5)) is False


def test_multiplying_a_dimensioned_quantity_by_a_proportion_scales_it():
    """No new arithmetic needed: this falls out of the existing dimension algebra."""
    result = Volt(5) * Ratio(Decimal("0.1"))
    assert isinstance(result, Voltage)
    assert result == Volt(Decimal("0.5"))


def test_multiplying_is_commutative():
    assert Volt(5) * Ratio(Decimal("0.1")) == Ratio(Decimal("0.1")) * Volt(5)


def test_dividing_a_dimensioned_quantity_by_a_proportion_scales_it_up():
    result = Volt(5) / Ratio(Decimal("0.1"))
    assert isinstance(result, Voltage)
    assert result == Volt(50)


def test_same_type_division_is_still_dimensionless_not_a_proportion():
    """Ohm / Ohm collapsing to a bare Decimal is unchanged by Proportion existing."""
    ratio = Ohm(5) / Ohm(2)
    assert not hasattr(ratio, "magnitude")
    assert ratio == Decimal("2.5")


def test_percent_divided_by_percent_is_a_bare_decimal_not_a_proportion():
    """The same collapse applies here: Proportion / Proportion is still just a ratio."""
    ratio = Percent(50) / Percent(25)
    assert not hasattr(ratio, "magnitude")
    assert ratio == Decimal(2)


def test_repr_of_ratio_uses_the_coherent_unit_symbol():
    assert repr(Ratio(Decimal("0.05"))) == "0.05 1"


def test_repr_of_percent():
    assert repr(Percent(5)) == "5 %"
