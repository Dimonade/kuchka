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
from kuchka import Volt
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
        Volt(5) + Ampere(1)  # type: ignore


def test_incompatible_subtraction_raises():
    with pytest.raises(IncompatibleDimensionError):
        Volt(5) - Ampere(1)  # type: ignore


def test_naked_number_addition_is_rejected_with_a_helpful_message():
    with pytest.raises(InvalidMeasurementError, match="wrap it in a unit constructor"):
        Volt(5) + 4.2  # type: ignore


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
    # Equality follows ordinary Python convention: different types compare
    # unequal rather than raising. Only arithmetic and ordering raise.
    assert (Volt(5) == Ampere(5)) is False
