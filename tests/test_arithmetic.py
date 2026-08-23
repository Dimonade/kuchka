"""Arithmetic: the runtime dimension algebra behind +, -, *, /, and comparisons."""

from decimal import Decimal

import pytest
from kuchka import Ampere
from kuchka import Current
from kuchka import IncompatibleDimensionError
from kuchka import InvalidMeasurementError
from kuchka import Kiloohm
from kuchka import Milliampere
from kuchka import Millivolt
from kuchka import Ohm
from kuchka import Power
from kuchka import Resistance
from kuchka import UnrepresentableDimensionError
from kuchka import Volt
from kuchka import Voltage
from kuchka import Watt


def test_addition_within_same_unit():
    assert Volt(5) + Volt(1) == Volt(6)


def test_addition_across_prefixes_is_exact():
    one_point_five_volts = Volt(1) + Millivolt(500)
    assert one_point_five_volts == Volt(1.5)
    assert one_point_five_volts == Millivolt(1500)


def test_addition_across_many_prefixes_stays_exact():
    total = Millivolt(100) + Millivolt(200) + Millivolt(300)
    assert total == Volt(Decimal("0.6"))


def test_subtraction():
    assert Volt(5) - Volt(2) == Volt(3)


def test_incompatible_addition_raises():
    with pytest.raises(IncompatibleDimensionError):
        Volt(5) + Ampere(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types


def test_incompatible_subtraction_raises():
    with pytest.raises(IncompatibleDimensionError):
        Volt(5) - Ampere(1)  # type: ignore[operator]  # not (yet) flagged by ty across sibling quantity types


def test_naked_number_addition_is_rejected_with_a_helpful_message():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Volt(5) + 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_multiplication_derives_power():
    result = Volt(5) * Ampere(2)
    assert isinstance(result, Power)
    assert result == Watt(10)


def test_division_derives_resistance():
    result = Volt(10) / Ampere(2)
    assert isinstance(result, Resistance)
    assert result == Ohm(5)


def test_division_derives_current_from_power_and_voltage():
    result = Watt(20) / Volt(5)
    assert isinstance(result, Current)
    assert result == Ampere(4)


def test_ohms_law_round_trip_stays_exact_with_prefixed_units():
    voltage = Volt(5)
    current = Milliampere(2)
    resistance = voltage / current
    assert resistance == Kiloohm(Decimal("2.5"))


def test_scalar_multiplication():
    assert Volt(2) * 3 == Volt(6)
    assert 3 * Volt(2) == Volt(6)


def test_scalar_division():
    assert Volt(6) / 3 == Volt(2)


def test_same_dimension_division_is_dimensionless():
    ratio = Ohm(10) / Ohm(5)
    assert not hasattr(ratio, "magnitude")  # it's a plain Decimal, not a Resistance
    assert ratio == Decimal(2)


def test_negation_and_abs():
    assert -Volt(5) == Volt(-5)
    assert abs(Volt(-5)) == Volt(5)


def test_ordering_within_same_dimension():
    assert Volt(1) < Volt(2)
    assert Millivolt(1500) > Volt(1)


def test_ordering_across_dimensions_raises():
    with pytest.raises(IncompatibleDimensionError):
        Volt(1) < Ampere(1)  # noqa: B015


def test_equality_across_dimensions_is_false_not_an_error():
    assert (Volt(5) == Ampere(5)) is False


def test_resistance_times_current_derives_voltage():
    result = Ohm(5) * Ampere(2)
    assert isinstance(result, Voltage)
    assert result == Volt(10)


def test_current_times_resistance_derives_voltage_commutatively():
    assert Ampere(2) * Ohm(5) == Ohm(5) * Ampere(2)


def test_power_divided_by_current_derives_voltage():
    result = Watt(20) / Ampere(4)
    assert isinstance(result, Voltage)
    assert result == Volt(5)


def test_multiplication_by_unregistered_dimension_has_no_registered_type():
    """Resistance * Resistance is dimensionally valid but has no registered type.

    This is a scope boundary (see UnrepresentableDimensionError), not a
    dimensional-analysis bug: the exponent-vector algebra behind the scenes
    happily computes the result, but nothing in this version of the
    library has a name for it yet.
    """
    match = "no registered engineering type"
    with pytest.raises(UnrepresentableDimensionError, match=match):
        # Statically valid: Resistance * Resistance falls through to the
        # generic `object` overload (LinearQuantity | Decimal), so this is
        # a runtime-only scope-boundary error, not a static type error.
        Ohm(5) * Ohm(2)


def test_naked_number_subtraction_is_rejected_with_a_helpful_message():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Volt(5) - 4.2  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_zero_division_by_a_measurement_raises_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        Volt(5) / Ampere(0)


def test_zero_division_by_a_plain_number_raises_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        Volt(5) / 0


def test_arithmetic_results_are_new_immutable_objects():
    a = Volt(1)
    b = Volt(2)
    result = a + b
    assert result is not a
    assert result is not b
    assert a == Volt(1)  # `a` itself was not mutated


def test_equal_measurements_in_different_prefixes_hash_equal():
    """Equal measurements must hash equal to be usable as dict keys or set members."""
    assert hash(Volt(1)) == hash(Millivolt(1000))


@pytest.mark.parametrize(
    ("left", "right"),
    [
        (Volt(1), Volt(2)),
        (Millivolt(500), Volt(1)),
        (Volt(-5), Volt(-1)),
    ],
)
def test_ordering_operators_agree_with_each_other(left, right):
    assert (left < right) == (not (left >= right))
    assert (left <= right) == (not (left > right))
    assert (left < right) or (left == right) or (left > right)


def test_ordering_operators_all_raise_across_dimensions():
    with pytest.raises(IncompatibleDimensionError):
        Volt(1) <= Ampere(1)  # noqa: B015

    with pytest.raises(IncompatibleDimensionError):
        Volt(1) > Ampere(1)  # noqa: B015

    with pytest.raises(IncompatibleDimensionError):
        Volt(1) >= Ampere(1)  # noqa: B015


def test_reflected_addition():
    """`3 + Volt(2)`-style reflected addition falls back to `__radd__`."""
    assert Volt(1) + Volt(2) == Volt(2) + Volt(1)


def test_unsupported_operand_type_raises_type_error():
    """An operand kuchka has no opinion about is Python's problem, not ours."""
    with pytest.raises(TypeError):
        Volt(5) + object()  # type: ignore[operator]  # ty: ignore[unsupported-operator]

    with pytest.raises(TypeError):
        # Statically valid: falls through to the fallback `object` overload
        # (LinearQuantity | Decimal), so no ignore is needed here -- the
        # TypeError only shows up once `to_decimal` runs at call time.
        Volt(5) * object()

    with pytest.raises(TypeError):
        # Same reasoning as above, for the reflected form.
        object() * Volt(5)


def test_naked_number_addition_reflected_is_also_rejected():
    """`3 + Volt(2)` falls to `__radd__`, rejecting it the same as `__add__`."""
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        3 + Volt(2)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_division_by_an_unsupported_operand_type_raises_type_error():
    with pytest.raises(TypeError):
        # Statically valid: falls through to the fallback `object` overload
        # (LinearQuantity | Decimal), so no ignore is needed -- the
        # TypeError only shows up once `to_decimal` runs at call time.
        Volt(5) / object()
