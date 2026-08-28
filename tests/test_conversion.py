"""Conversion: `.to(...)`, `repr()`, and `value_in(...)`."""

from decimal import Decimal

import pytest
from kuchka import Ampere
from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import Kilovolt
from kuchka import Volt
from kuchka.units import MICROVOLT
from kuchka.units import MILLIVOLT
from kuchka.units import OHM
from kuchka.units import VOLT


def test_to_changes_display_unit_not_value():
    voltage = Volt(1)
    in_millivolts = voltage.to(MILLIVOLT)
    assert in_millivolts == voltage
    assert in_millivolts.value_in(MILLIVOLT) == Decimal(1000)


def test_repr_reflects_display_unit():
    assert repr(Volt(4.2)) == "4.2 V"
    assert repr(Volt(4.2).to(MILLIVOLT)) == "4200 mV"


def test_repr_avoids_scientific_notation_after_conversion():
    text = repr(Kilovolt(1).to(MILLIVOLT))
    assert "E" not in text
    assert text == "1000000 mV"


def test_to_rejects_a_unit_from_a_different_quantity():
    voltage = Volt(1)
    with pytest.raises(InvalidConversionError, match="incompatible dimensions"):
        voltage.to(OHM)


def test_to_rejects_non_unit_arguments():
    with pytest.raises(InvalidConversionError):
        Volt(1).to("mV")  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_construction_from_incompatible_measurement_is_rejected():

    with pytest.raises(InvalidMeasurementError):
        Volt(Ampere(5))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def test_to_is_idempotent_for_the_same_unit():
    voltage = Volt(5)
    assert voltage.to(VOLT) == voltage
    assert voltage.to(VOLT).unit is VOLT


def test_to_round_trips_through_multiple_units():
    original = Volt(1)
    round_tripped = original.to(MILLIVOLT).to(MICROVOLT).to(VOLT)
    assert round_tripped == original


def test_value_in_matches_the_constructor_it_mirrors():
    voltage = Kilovolt(2)
    assert voltage.value_in(MILLIVOLT) == Decimal(2_000_000)


def test_repr_of_a_negative_value():
    assert repr(Volt(-4.2)) == "-4.2 V"


def test_repr_of_zero():
    assert repr(Volt(0)) == "0 V"
