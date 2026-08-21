from decimal import Decimal
from fractions import Fraction

import pytest
from kuchka import Ampere
from kuchka import InvalidMeasurementError
from kuchka import Volt
from kuchka import Voltage


def test_accepts_int_float_decimal_fraction():
    assert Volt(5) == Volt(Decimal(5))
    assert Volt(5.0) == Volt(Decimal(5))
    assert Volt(Fraction(1, 2)) == Volt(Decimal("0.5"))


def test_rejects_strings():
    with pytest.raises(InvalidMeasurementError):
        Volt("5")  # type: ignore


def test_rejects_bool():
    """Test that a `bool` cannot be used to create objects.

    `bool` is a subclass of `int`, and `False` means 0, `True` is 1.
    This is must not be accepted or converted silently.
    """
    with pytest.raises(InvalidMeasurementError):
        Volt(True)  # type: ignore


def test_rejects_incompatible_measurement_with_a_helpful_hint():
    with pytest.raises(InvalidMeasurementError, match="dimension mismatch"):
        Volt(Ampere(5))  # type: ignore


def test_measurements_are_immutable():
    voltage = Volt(5)
    with pytest.raises(AttributeError):
        voltage._magnitude = Decimal(10)  # noqa: SLF001


def test_isinstance_of_the_semantic_type_not_the_constructor():
    assert isinstance(Volt(4.2), Voltage)
    assert not isinstance(Volt, type)
