"""Levels add and subtract exactly in the log domain; other operations are refused."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING
from typing import ClassVar

import pytest

from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Proportion
from kuchka.dimensions import DIMENSIONLESS
from kuchka.quantities.base import PureLogarithmicQuantity
from kuchka.units import logarithmic
from kuchka.units import proportion
from kuchka.units import voltage
from tests.support.values import BINARY_IMPRECISE_TRIPLES

if TYPE_CHECKING:
    from kuchka.dimensions import Dimension


class _OtherLogarithmicQuantity(PureLogarithmicQuantity):
    """A second concrete level type, for exercising the exact-type guards."""

    dimension: ClassVar[Dimension] = DIMENSIONLESS
    __slots__ = ()


def test_cascaded_stages_add_their_levels():
    chain = (
        logarithmic.Decibel(20) + logarithmic.Decibel(-3.5) + logarithmic.Decibel(-1.5)
    )
    assert chain == logarithmic.Decibel(15)


def test_addition_is_exact_where_binary_floats_are_not():
    for a, b, total in BINARY_IMPRECISE_TRIPLES:
        assert logarithmic.Decibel(a) + logarithmic.Decibel(b) == logarithmic.Decibel(
            total
        )


def test_subtraction_divides_the_ratios():
    assert logarithmic.Decibel(20) - logarithmic.Decibel(3) == logarithmic.Decibel(17)


def test_units_mix_freely_and_the_left_operand_sets_the_display_unit():
    assert logarithmic.Decibel(10) + logarithmic.Bel(1) == logarithmic.Decibel(20)
    total = logarithmic.Bel(1) + logarithmic.Decibel(10)
    assert total == logarithmic.Bel(2)
    assert total.unit is logarithmic.BEL
    assert (logarithmic.Decibel(20) - logarithmic.Bel(1)).unit is logarithmic.DECIBEL


def test_negation_is_the_reciprocal_ratio():
    assert -logarithmic.Decibel(3) == logarithmic.Decibel(-3)
    assert logarithmic.Decibel(3) + (-logarithmic.Decibel(3)) == logarithmic.Decibel(0)
    assert (-logarithmic.Decibel(3)).unit is logarithmic.DECIBEL


def test_absolute_value_is_the_size_of_a_deviation():
    assert abs(logarithmic.Decibel(-0.4)) == logarithmic.Decibel(0.4)
    assert abs(logarithmic.Decibel(0.4)) == logarithmic.Decibel(0.4)
    measured, expected = logarithmic.Decibel(20.3), logarithmic.Decibel(20)
    assert abs(measured - expected) <= logarithmic.Decibel(0.5)
    assert abs(logarithmic.Decibel(19.4) - expected) > logarithmic.Decibel(0.5)


def test_scaling_by_a_plain_number():
    assert logarithmic.Decibel(-0.2) * 30 == logarithmic.Decibel(-6)
    assert 30 * logarithmic.Decibel(-0.2) == logarithmic.Decibel(-6)
    assert logarithmic.Decibel(-6) / 30 == logarithmic.Decibel(-0.2)
    assert logarithmic.Decibel(3) * Decimal("0.5") == logarithmic.Decibel(1.5)
    assert logarithmic.Decibel(3) * Fraction(1, 3) == logarithmic.Decibel(1)


def test_scaling_keeps_the_display_unit():
    assert (logarithmic.Bel(2) * 3).unit is logarithmic.BEL


def test_level_divided_by_level_is_a_proportion():
    assert logarithmic.Decibel(6) / logarithmic.Decibel(3) == proportion.Ratio(2)
    assert logarithmic.Bel(1) / logarithmic.Decibel(5) == proportion.Ratio(2)
    assert isinstance(logarithmic.Decibel(6) / logarithmic.Decibel(3), Proportion)


def test_sum_needs_a_level_as_its_start_value():
    assert sum(
        [logarithmic.Decibel(1), logarithmic.Decibel(2)], start=logarithmic.Decibel(0)
    ) == logarithmic.Decibel(3)
    with pytest.raises(InvalidMeasurementError):
        sum([logarithmic.Decibel(1), logarithmic.Decibel(2)])  # type: ignore[list-item]  # ty: ignore[no-matching-overload]


def test_naked_number_addition_and_subtraction_are_rejected():
    with pytest.raises(InvalidMeasurementError, match=r"e\.g\. Decibel\(3\)"):
        logarithmic.Decibel(3) + 3  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        3 + logarithmic.Decibel(3)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(InvalidMeasurementError, match="subtract"):
        logarithmic.Decibel(3) - 3  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_level_times_level_is_a_type_error():
    with pytest.raises(TypeError):
        logarithmic.Decibel(3) * logarithmic.Decibel(3)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_number_divided_by_a_level_is_a_type_error():
    with pytest.raises(TypeError):
        2 / logarithmic.Decibel(3)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_level_is_not_a_linear_quantity_and_does_not_mix_with_one():
    with pytest.raises(TypeError):
        logarithmic.Decibel(3) + proportion.Ratio(2)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(TypeError):
        proportion.Ratio(2) + logarithmic.Decibel(3)  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(TypeError):
        logarithmic.Decibel(3) * voltage.Volt(1)


def test_bool_scalar_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="bool"):
        logarithmic.Decibel(3) * True


def test_unsupported_scalar_types_are_type_errors():
    with pytest.raises(TypeError):
        logarithmic.Decibel(3) * "2"  # type: ignore[operator]  # ty: ignore[unsupported-operator]
    with pytest.raises(TypeError):
        logarithmic.Decibel(3) / "2"  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_division_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        logarithmic.Decibel(3) / 0
    with pytest.raises(ZeroDivisionError):
        logarithmic.Decibel(3) / logarithmic.Decibel(0)


def test_two_distinct_level_types_do_not_combine():
    other = _OtherLogarithmicQuantity(Fraction(3), logarithmic.DECIBEL)
    for operation in (
        lambda: logarithmic.Decibel(3) + other,  # type: ignore[operator]
        lambda: other + logarithmic.Decibel(3),  # type: ignore[operator]
        lambda: logarithmic.Decibel(3) - other,  # type: ignore[operator]
        lambda: logarithmic.Decibel(3) / other,  # type: ignore[operator]
    ):
        with pytest.raises(IncompatibleDimensionError, match="distinct concepts"):
            operation()
