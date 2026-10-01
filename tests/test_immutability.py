"""A quantity is born with its state and keeps it.

State is written exactly once, and only through a validated path: construction, or
restoring a pickled/copied value.
After that the magnitude and display unit cannot be rebound, deleted, or replaced by
calling `__init__` or `__setstate__` again.
A value restored from pickle data is held to the same contract as one built through
its constructor, so a forged or corrupt payload cannot produce a value that
construction would have refused.
"""

from __future__ import annotations

import copy
import pickle
from decimal import Decimal
from fractions import Fraction

import pytest

from kuchka import Celsius
from kuchka import InvalidMeasurementError
from kuchka import Temperature
from kuchka import Volt
from kuchka import Voltage
from kuchka.units import AMPERE
from kuchka.units import KELVIN
from kuchka.units import VOLT
from tests.quantity_families import CONCRETE_QUANTITY_TYPES
from tests.quantity_families import sample_of

STATE_ATTRIBUTES = ["_magnitude", "_display_unit"]

BAD_MAGNITUDES = [0.5, 5, Decimal("0.5"), "5", None]
BAD_MAGNITUDE_IDS = ["float", "int", "decimal", "str", "none"]

MALFORMED_STATES = [
    None,
    5,
    (),
    (Fraction(1),),
    (Fraction(1), VOLT, VOLT),
    [Fraction(1), VOLT],
]
MALFORMED_STATE_IDS = ["none", "int", "empty", "short", "long", "list"]


def _type_id(cls: type) -> str:
    return cls.__name__


def _state_of(value) -> tuple[Fraction, object]:
    """Magnitude in the display unit, plus that unit: readable on every type."""
    return (value.value_in(value.unit), value.unit)


# A live value cannot be changed


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
@pytest.mark.parametrize("attribute", [*STATE_ATTRIBUTES, "anything_else"])
def test_attributes_cannot_be_rebound(cls, attribute) -> None:
    value = sample_of(cls)
    before = _state_of(value)
    with pytest.raises(AttributeError, match="immutable"):
        setattr(value, attribute, 1)
    assert _state_of(value) == before


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
@pytest.mark.parametrize("attribute", [*STATE_ATTRIBUTES, "anything_else"])
def test_attributes_cannot_be_deleted(cls, attribute) -> None:
    value = sample_of(cls)
    before = _state_of(value)
    with pytest.raises(AttributeError, match="immutable"):
        delattr(value, attribute)
    assert _state_of(value) == before


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
def test_init_cannot_be_called_again_to_replace_the_state(cls) -> None:
    value = sample_of(cls)
    before = _state_of(value)
    with pytest.raises(AttributeError, match="immutable"):
        value.__init__(Fraction(9), value.unit)
    assert _state_of(value) == before


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
def test_setstate_cannot_replace_the_state_of_a_live_value(cls) -> None:
    value = sample_of(cls)
    before = _state_of(value)
    with pytest.raises(AttributeError, match="immutable"):
        value.__setstate__((Fraction(9), value.unit))
    assert _state_of(value) == before


def test_reinitialising_a_voltage_leaves_it_unchanged() -> None:
    voltage = Volt(1)
    with pytest.raises(AttributeError, match="immutable"):
        voltage.__init__(Fraction(9), VOLT)
    assert voltage == Volt(1)


# Restoring state is validated like construction


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
def test_a_valid_state_restores_an_equal_value(cls) -> None:
    original = sample_of(cls)
    blank = cls.__new__(cls)
    blank.__setstate__(original.__getstate__())
    assert blank == original
    assert blank.unit is original.unit


@pytest.mark.parametrize("cls", CONCRETE_QUANTITY_TYPES, ids=_type_id)
def test_copy_and_pickle_round_trip_every_type(cls) -> None:
    original = sample_of(cls)
    assert copy.copy(original) == original
    assert copy.deepcopy(original) == original
    assert pickle.loads(pickle.dumps(original)) == original


@pytest.mark.parametrize("bad", BAD_MAGNITUDES, ids=BAD_MAGNITUDE_IDS)
def test_restoring_rejects_a_magnitude_that_is_not_a_fraction(bad) -> None:
    blank = Voltage.__new__(Voltage)
    with pytest.raises(InvalidMeasurementError, match="unit constructors"):
        blank.__setstate__((bad, VOLT))


@pytest.mark.parametrize(
    "bad", [None, "V", 1, KELVIN], ids=["none", "str", "int", "affine"]
)
def test_restoring_rejects_a_display_unit_of_the_wrong_kind(bad) -> None:
    blank = Voltage.__new__(Voltage)
    with pytest.raises(InvalidMeasurementError, match="display unit"):
        blank.__setstate__((Fraction(1), bad))


def test_restoring_rejects_a_display_unit_of_another_dimension() -> None:
    blank = Voltage.__new__(Voltage)
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        blank.__setstate__((Fraction(1), AMPERE))


@pytest.mark.parametrize("state", MALFORMED_STATES, ids=MALFORMED_STATE_IDS)
def test_restoring_rejects_a_state_that_is_not_a_magnitude_and_unit_pair(state) -> None:
    blank = Voltage.__new__(Voltage)
    with pytest.raises(InvalidMeasurementError, match="magnitude, display unit"):
        blank.__setstate__(state)


def test_restoring_below_absolute_zero_is_rejected() -> None:
    blank = Temperature.__new__(Temperature)
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        blank.__setstate__((Fraction(-1), KELVIN))


def test_a_rejected_restore_leaves_the_value_without_state() -> None:
    blank = Voltage.__new__(Voltage)
    with pytest.raises(InvalidMeasurementError):
        blank.__setstate__((0.5, VOLT))
    with pytest.raises(AttributeError):
        _ = blank.unit


def test_a_value_can_be_restored_after_a_rejected_attempt() -> None:
    blank = Voltage.__new__(Voltage)
    with pytest.raises(InvalidMeasurementError):
        blank.__setstate__((0.5, VOLT))
    blank.__setstate__((Fraction(3), VOLT))
    assert blank == Volt(3)


# Forged pickle payloads


class _ForgedPayload:
    """Pickles to a payload that rebuilds `cls` around an arbitrary state."""

    def __init__(self, cls: type, state: object) -> None:
        self._cls = cls
        self._state = state

    def __reduce__(self) -> tuple[object, ...]:
        return (object.__new__, (self._cls,), self._state)


def test_a_forged_payload_with_a_float_magnitude_is_rejected_on_load() -> None:
    payload = pickle.dumps(_ForgedPayload(Voltage, (0.5, VOLT)))
    with pytest.raises(InvalidMeasurementError, match="unit constructors"):
        pickle.loads(payload)


def test_a_forged_payload_with_a_foreign_unit_is_rejected_on_load() -> None:
    payload = pickle.dumps(_ForgedPayload(Voltage, (Fraction(1), AMPERE)))
    with pytest.raises(InvalidMeasurementError, match="incompatible dimensions"):
        pickle.loads(payload)


def test_a_forged_temperature_below_absolute_zero_is_rejected_on_load() -> None:
    payload = pickle.dumps(_ForgedPayload(Temperature, (Fraction(-5), KELVIN)))
    with pytest.raises(InvalidMeasurementError, match="absolute zero"):
        pickle.loads(payload)


def test_an_honest_payload_loads_equal() -> None:
    assert pickle.loads(pickle.dumps(Celsius(20))) == Celsius(20)
