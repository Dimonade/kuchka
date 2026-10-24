"""Restoring a state is validated like construction.

A value restored from pickle data is held to the contract of one built through its
constructor, so a forged or corrupt payload cannot produce a value that construction
would have refused.
"""

from __future__ import annotations

import pickle
from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import InvalidMeasurementError
from kuchka import Temperature
from kuchka import Voltage
from kuchka.units import current
from kuchka.units import thermal
from kuchka.units.electromagnetics import voltage

BAD_MAGNITUDES = (0.5, 5, Decimal("0.5"), "5", None)
WRONG_KIND_OF_UNIT = (None, "V", 1, thermal.KELVIN)
NOT_A_PAIR = (
    None,
    5,
    (),
    (Fraction(1),),
    (Fraction(1), voltage.VOLT, voltage.VOLT),
    [Fraction(1), voltage.VOLT],
)


def blank_voltage() -> Voltage:
    """Return an instance that has not been given its state yet."""
    return Voltage.__new__(Voltage)


def test_a_magnitude_that_is_not_a_fraction_is_rejected() -> None:
    for bad in BAD_MAGNITUDES:
        with pytest.raises(InvalidMeasurementError, match="unit constructors"):
            blank_voltage().__setstate__((bad, voltage.VOLT))


def test_a_display_unit_of_the_wrong_kind_is_rejected() -> None:
    for bad in WRONG_KIND_OF_UNIT:
        with pytest.raises(InvalidMeasurementError, match="display unit"):
            blank_voltage().__setstate__((Fraction(1), bad))


def test_a_display_unit_of_another_dimension_is_rejected() -> None:
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        blank_voltage().__setstate__((Fraction(1), current.AMPERE))


def test_a_state_that_is_not_a_magnitude_and_unit_pair_is_rejected() -> None:
    for state in NOT_A_PAIR:
        with pytest.raises(InvalidMeasurementError, match="magnitude, display unit"):
            blank_voltage().__setstate__(state)


def test_a_temperature_below_absolute_zero_is_rejected() -> None:
    blank = Temperature.__new__(Temperature)
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        blank.__setstate__((Fraction(-1), thermal.KELVIN))


def test_a_rejected_restore_leaves_the_value_without_state() -> None:
    blank = blank_voltage()
    with pytest.raises(InvalidMeasurementError):
        blank.__setstate__((0.5, voltage.VOLT))
    with pytest.raises(AttributeError):
        _ = blank.unit


def test_a_value_can_be_restored_after_a_rejected_attempt() -> None:
    blank = blank_voltage()
    with pytest.raises(InvalidMeasurementError):
        blank.__setstate__((0.5, voltage.VOLT))
    blank.__setstate__((Fraction(3), voltage.VOLT))
    assert blank == voltage.Volt(3)


class ForgedPayload:
    """Pickles to a payload that rebuilds `cls` around an arbitrary state."""

    def __init__(self, cls: type, state: object) -> None:
        """Hold the class to rebuild and the state to give it."""
        self._cls = cls
        self._state = state

    def __reduce__(self) -> tuple[object, ...]:
        return (object.__new__, (self._cls,), self._state)


def test_a_forged_payload_is_rejected_on_load() -> None:
    float_magnitude = pickle.dumps(ForgedPayload(Voltage, (0.5, voltage.VOLT)))
    with pytest.raises(InvalidMeasurementError, match="unit constructors"):
        pickle.loads(float_magnitude)
    foreign_unit = pickle.dumps(ForgedPayload(Voltage, (Fraction(1), current.AMPERE)))
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        pickle.loads(foreign_unit)
    below_zero = pickle.dumps(
        ForgedPayload(Temperature, (Fraction(-5), thermal.KELVIN))
    )
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        pickle.loads(below_zero)


def test_an_honest_payload_loads_equal() -> None:
    celsius = thermal.Celsius(20)
    assert pickle.loads(pickle.dumps(celsius)) == celsius
