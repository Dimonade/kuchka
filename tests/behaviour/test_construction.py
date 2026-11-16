"""Construction: which raw values become measurements, and which are rejected."""

from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import InvalidMeasurementError
from kuchka import Voltage
from kuchka.units import current
from kuchka.units.electromagnetics import voltage as voltage_units


def test_accepts_int_float_decimal_fraction():
    assert voltage_units.Volt(5) == voltage_units.Volt(Decimal(5))
    assert voltage_units.Volt(5.0) == voltage_units.Volt(Decimal(5))
    assert voltage_units.Volt(Fraction(1, 2)) == voltage_units.Volt(Decimal("0.5"))


def test_rejects_strings():
    with pytest.raises(InvalidMeasurementError):
        voltage_units.Volt("5")  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_rejects_bool():
    """Test that a `bool` cannot be used to create objects.

    `bool` is a subclass of `int`, and `False` means 0, `True` is 1.
    This is must not be accepted or converted silently.
    """
    with pytest.raises(InvalidMeasurementError):
        voltage_units.Volt(True)


def test_rejects_incompatible_measurement_with_a_helpful_hint():
    with pytest.raises(InvalidMeasurementError, match="dimension mismatch"):
        voltage_units.Volt(current.Ampere(5))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_rejects_same_dimension_measurement_too():
    """A Voltage is not a valid input to Volt(), even though the dimension matches.

    Construction always starts from a plain number; converting between
    prefixes of the same quantity goes through `.to(...)`, not through
    re-wrapping an existing measurement in another constructor.
    """
    with pytest.raises(InvalidMeasurementError, match="dimension mismatch"):
        voltage_units.Volt(voltage_units.Volt(5))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_rejects_none():
    with pytest.raises(InvalidMeasurementError):
        voltage_units.Volt(None)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


@pytest.mark.parametrize(
    "bad_value",
    ["5", None, [5], {5}, 5j],
    ids=["string", "none", "list", "set", "complex"],
)
def test_rejects_a_variety_of_non_numeric_inputs(bad_value):
    # `bad_value` is untyped (parametrized), so mypy sees it as `Any` and
    # raises no static error here to suppress; only the runtime check in
    # `to_decimal` rejects it.
    with pytest.raises(InvalidMeasurementError):
        voltage_units.Volt(bad_value)


def test_measurements_are_immutable():
    voltage = voltage_units.Volt(5)
    with pytest.raises(AttributeError):
        voltage._magnitude = Decimal(10)  # ty: ignore[invalid-assignment]  # noqa: SLF001


def test_isinstance_of_the_semantic_type_not_the_constructor():
    assert isinstance(voltage_units.Volt(4.2), Voltage)
    assert not isinstance(voltage_units.Volt, type)


@pytest.mark.parametrize(
    "magnitude",
    [0, -5, Decimal("0.0000001"), 10**9],
    ids=["zero", "negative", "tiny_decimal", "extreme_positive"],
)
def test_accepts_zero_negative_and_extreme_magnitudes(magnitude):
    """Construction places no domain restriction on the magnitude itself.

    Whether a given voltage is physically sensible is an application-level
    concern (e.g. a safety check against a datasheet limit); the type
    system's job is only to guarantee that whatever the number is, it is
    unambiguously a Voltage.
    """
    voltage = voltage_units.Volt(magnitude)
    assert voltage.magnitude == Decimal(magnitude)
