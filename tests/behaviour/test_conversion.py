"""Conversion: `.to(...)`, `repr()`, and `value_in(...)`."""

from decimal import Decimal

import pytest

from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka.units import current
from kuchka.units import resistance
from kuchka.units import voltage as voltage_units


def test_to_changes_display_unit_not_value():
    voltage = voltage_units.Volt(1)
    in_millivolts = voltage.to(voltage_units.MILLIVOLT)
    assert in_millivolts == voltage
    assert in_millivolts.value_in(voltage_units.MILLIVOLT) == Decimal(1000)


def test_repr_reflects_display_unit():
    assert repr(voltage_units.Volt(4.2)) == "4.2 V"
    assert repr(voltage_units.Volt(4.2).to(voltage_units.MILLIVOLT)) == "4200 mV"


def test_repr_avoids_scientific_notation_after_conversion():
    text = repr(voltage_units.Kilovolt(1).to(voltage_units.MILLIVOLT))
    assert "E" not in text
    assert text == "1000000 mV"


def test_to_rejects_a_unit_from_a_different_quantity():
    voltage = voltage_units.Volt(1)
    with pytest.raises(InvalidConversionError, match="incompatible dimensions"):
        voltage.to(resistance.OHM)


def test_to_rejects_non_unit_arguments():
    with pytest.raises(InvalidConversionError):
        voltage_units.Volt(1).to("mV")  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_construction_from_incompatible_measurement_is_rejected():

    with pytest.raises(InvalidMeasurementError):
        voltage_units.Volt(current.Ampere(5))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_to_is_idempotent_for_the_same_unit():
    voltage = voltage_units.Volt(5)
    assert voltage.to(voltage_units.VOLT) == voltage
    assert voltage.to(voltage_units.VOLT).unit is voltage_units.VOLT


def test_to_round_trips_through_multiple_units():
    original = voltage_units.Volt(1)
    round_tripped = (
        original.to(voltage_units.MILLIVOLT)
        .to(voltage_units.MICROVOLT)
        .to(voltage_units.VOLT)
    )
    assert round_tripped == original


def test_value_in_matches_the_constructor_it_mirrors():
    voltage = voltage_units.Kilovolt(2)
    assert voltage.value_in(voltage_units.MILLIVOLT) == Decimal(2_000_000)


def test_repr_of_a_negative_value():
    assert repr(voltage_units.Volt(-4.2)) == "-4.2 V"


def test_repr_of_zero():
    assert repr(voltage_units.Volt(0)) == "0 V"
