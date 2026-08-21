from decimal import Decimal

import pytest
from kuchka import Ampere
from kuchka import InvalidConversionError
from kuchka import InvalidMeasurementError
from kuchka import Kilovolt
from kuchka import Volt
from kuchka.units import MILLIVOLT
from kuchka.units import OHM


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
    with pytest.raises(InvalidConversionError, match="different physical dimension"):
        voltage.to(OHM)


def test_to_rejects_non_unit_arguments():
    with pytest.raises(InvalidConversionError):
        Volt(1).to("mV")  # type: ignore


def test_construction_from_incompatible_measurement_is_rejected():

    with pytest.raises(InvalidMeasurementError):
        Volt(Ampere(5))  # type: ignore
