"""Reactance and Impedance: roles of Resistance that read the ohm.

The generic role behaviour (refusals, scaling) is covered once for every role in
`test_role_kinds`; this module covers what is specific to the two electrical roles.
"""

from __future__ import annotations

import pytest

from kuchka import Impedance
from kuchka import IncompatibleDimensionError
from kuchka import Reactance
from kuchka import Resistance
from kuchka import parse
from kuchka.units.electromagnetics import impedance
from kuchka.units.electromagnetics import reactance
from kuchka.units.electromagnetics import resistance


def test_a_resistance_is_viewed_as_a_reactance_and_back() -> None:
    reading = resistance.Kiloohm(2).to_reactance()
    assert isinstance(reading, Reactance)
    assert reading.to_resistance() == resistance.Kiloohm(2)


def test_a_resistance_is_viewed_as_an_impedance_and_back() -> None:
    magnitude = resistance.Ohm(50).to_impedance()
    assert isinstance(magnitude, Impedance)
    assert magnitude.to_resistance() == resistance.Ohm(50)


def test_a_reactance_is_signed() -> None:
    capacitive = -resistance.Ohm(159).to_reactance()
    assert (
        capacitive + resistance.Ohm(159).to_reactance()
        == resistance.Ohm(0).to_reactance()
    )


def test_a_reactance_and_an_impedance_do_not_mix_directly() -> None:
    with pytest.raises(IncompatibleDimensionError):
        resistance.Ohm(1).to_reactance() + resistance.Ohm(1).to_impedance()  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_reactance_and_a_resistance_do_not_mix_directly() -> None:
    with pytest.raises(IncompatibleDimensionError):
        resistance.Ohm(1).to_reactance() + resistance.Ohm(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_tables_read_a_number_in_a_unit_as_the_role() -> None:
    assert reactance.REACTANCE_UNITS["kΩ"](3) == resistance.Kiloohm(3).to_reactance()
    assert isinstance(impedance.IMPEDANCE_UNITS["Ω"](50), Impedance)
    assert repr(impedance.IMPEDANCE_UNITS["mΩ"](5)) == "5 mΩ"


def test_the_tables_accept_the_text_of_the_resistance_table() -> None:
    for table in (reactance.REACTANCE_UNITS, impedance.IMPEDANCE_UNITS):
        assert list(table) == list(resistance.RESISTANCE_UNITS)


def test_a_role_is_read_from_text_through_its_own_table() -> None:
    assert parse("-3 kΩ", Reactance) == -resistance.Kiloohm(3).to_reactance()
    assert parse("50 ohm", Impedance) == resistance.Ohm(50).to_impedance()


def test_a_resistance_is_not_either_role() -> None:
    assert not isinstance(resistance.Ohm(1), (Reactance, Impedance))
    assert isinstance(resistance.Ohm(1), Resistance)
