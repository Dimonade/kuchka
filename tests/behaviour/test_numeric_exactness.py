"""Numeric exactness: `to_exact`, `to_decimal`, and exact storage end to end.

Magnitude storage is `Fraction`, `Decimal` is a materialization.
"""

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import InvalidMeasurementError
from kuchka import Proportion
from kuchka.numeric import to_decimal
from kuchka.numeric import to_exact
from kuchka.units import proportion
from kuchka.units import thermal
from kuchka.units.electromagnetics import resistance
from kuchka.units.electromagnetics import voltage
from kuchka.units.geometry import volume
from kuchka.units.temporal import frequency


def test_int_is_exact():
    assert to_exact(5) == Fraction(5)


def test_decimal_is_exact():
    assert to_exact(Decimal("0.1")) == Fraction(1, 10)


def test_fraction_passes_through_unchanged():
    value = Fraction(5, 18)
    assert to_exact(value) is value


def test_float_preserves_typed_digits_not_binary_value():
    """`Fraction(4.2)` reproduces IEEE-754 rounding error; `to_exact` must not."""
    assert to_exact(4.2) == Fraction("4.2")
    assert to_exact(4.2) != Fraction(4.2)


def test_bool_is_rejected():
    with pytest.raises(InvalidMeasurementError, match="bool"):
        to_exact(True)


def test_string_is_rejected():
    with pytest.raises(InvalidMeasurementError):
        to_exact("5")


@pytest.mark.parametrize(
    "bad_value",
    [float("nan"), float("inf"), float("-inf")],
    ids=["nan", "inf", "-inf"],
)
def test_non_finite_float_is_rejected(bad_value):
    with pytest.raises(InvalidMeasurementError, match="not finite"):
        to_exact(bad_value)


@pytest.mark.parametrize(
    "bad_value",
    [Decimal("NaN"), Decimal("Infinity"), Decimal("-Infinity")],
    ids=["nan", "inf", "-inf"],
)
def test_non_finite_decimal_is_rejected(bad_value):
    with pytest.raises(InvalidMeasurementError, match="not finite"):
        to_exact(bad_value)


def test_rejects_incompatible_measurement_with_a_helpful_hint():
    with pytest.raises(InvalidMeasurementError, match="dimension mismatch"):
        to_exact(voltage.Volt(5))


def test_to_decimal_of_a_terminating_fraction_is_exact():
    assert to_decimal(Fraction(1, 4)) == Decimal("0.25")


def test_to_decimal_of_a_non_terminating_fraction_rounds_at_context_precision():
    result = to_decimal(Fraction(1, 3))
    assert result != Fraction(1, 3)  # Decimal cannot hold this exactly
    assert str(result).startswith("0.333333333333333333333333333")


def test_litre_from_a_non_terminating_fraction_stays_exact():
    from kuchka.units import LITRE

    quantity = volume.Litre(Fraction(5, 18))
    assert quantity.value_in(LITRE) == Fraction(5, 18)
    assert isinstance(quantity.magnitude, Fraction)


def test_millilitre_from_a_non_terminating_fraction_stays_exact():
    quantity = volume.Millilitre(Fraction(5, 18))
    assert quantity.magnitude == Fraction(5, 18) * volume.Millilitre(1).magnitude


def test_exactness_survives_addition():
    from kuchka.units import LITRE

    total = volume.Litre(Fraction(1, 3)) + volume.Litre(Fraction(1, 6))
    assert total.value_in(LITRE) == Fraction(1, 2)


def test_exactness_survives_scalar_multiplication():
    from kuchka.units import LITRE

    result = volume.Litre(Fraction(1, 3)) * 3
    assert result.value_in(LITRE) == Fraction(1, 1)


def test_exactness_survives_round_trip_through_to():
    from kuchka.units import LITRE
    from kuchka.units import MILLILITRE

    original = volume.Litre(Fraction(5, 18))
    round_tripped = original.to(MILLILITRE).to(LITRE)
    assert round_tripped.value_in(LITRE) == Fraction(5, 18)


def test_int_construction_still_gives_the_expected_magnitude():
    assert voltage.Volt(5).magnitude == Decimal(5)


def test_decimal_construction_still_gives_the_expected_magnitude():
    assert voltage.Volt(Decimal("4.2")).magnitude == Decimal("4.2")


def test_repr_of_a_simple_value_is_unaffected():
    assert repr(voltage.Volt(4.2)) == "4.2 V"


def test_repr_of_a_prefix_sum_is_unaffected():
    from kuchka import Millivolt

    assert repr(voltage.Volt(1) + Millivolt(500)) == "1.5 V"


def test_like_quantity_division_result_is_an_exact_proportion():
    ratio = resistance.Ohm(5) / resistance.Ohm(2)
    assert isinstance(ratio, Proportion)
    assert isinstance(ratio.magnitude, Fraction)


def test_like_quantity_division_result_compares_equal_to_a_decimal_ratio():
    ratio = resistance.Ohm(5) / resistance.Ohm(2)
    assert ratio == proportion.Ratio(Decimal("2.5"))


def test_time_times_frequency_result_is_a_fraction():
    from kuchka import Second

    ratio = Second(2) * frequency.Hertz(Decimal("0.5"))
    assert isinstance(ratio, Fraction)
    assert ratio == Decimal(1)


def test_celsius_to_kelvin_offset_stays_exact():
    assert thermal.Celsius(0).kelvin == Fraction(27315, 100)
    assert thermal.Celsius(0).kelvin == Decimal("273.15")


def test_celsius_from_a_fraction_stays_exact():
    reading = thermal.Celsius(Fraction(1, 3))
    assert reading.kelvin == Fraction(1, 3) + Fraction(27315, 100)


def test_fahrenheit_to_kelvin_offset_stays_exact():
    assert thermal.Fahrenheit(0).kelvin == Fraction(45967, 180)
    assert thermal.Fahrenheit(Decimal("-459.67")).kelvin == 0


def test_fahrenheit_from_a_fraction_stays_exact():
    reading = thermal.Fahrenheit(Fraction(1, 3))
    assert reading.kelvin == (Fraction(1, 3) + Fraction(45967, 100)) * Fraction(5, 9)


def test_fahrenheit_equals_celsius_across_representations():
    assert thermal.Fahrenheit(Decimal("33.8")) == thermal.Celsius(Decimal(1))
    assert thermal.Fahrenheit(33.8) == thermal.Celsius(1)


def test_kelvin_equals_celsius_across_representations():
    assert thermal.Celsius(0) == thermal.Kelvin(Decimal("273.15"))


def test_wraparound_subtraction_does_not_reproduce_the_decimal_mod_bug():
    """`Decimal(-10) % Decimal(360) == -10`, not `350`.

    `Fraction` gets this right natively. Pins the correct wraparound
    behavior as a regression test.
    """
    from typing import ClassVar

    from kuchka.dimensions import Dimension
    from kuchka.quantities.base import ModularQuantity
    from kuchka.quantities.base.units import UnitDef

    dim = Dimension(mass=97)  # unused slot, safe for a scratch type
    degree = UnitDef("degree", "deg", 1, dim)

    class ScratchAngle(ModularQuantity):
        dimension: ClassVar[Dimension] = dim
        _period: ClassVar[Fraction] = Fraction(360)
        _canonical_unit: ClassVar[UnitDef] = degree
        __slots__ = ()

    ten = ScratchAngle(Fraction(10), degree)
    twenty = ScratchAngle(Fraction(20), degree)
    assert (ten - twenty)._magnitude == Fraction(350)  # noqa: SLF001
