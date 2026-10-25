"""Stress: the force per area a material carries, a role of Pressure.

The generic role behaviour (refusals, scaling) is covered once for every role in
`test_role_kinds`; this module covers what is specific to stress and its units.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import IncompatibleDimensionError
from kuchka import Pressure
from kuchka import Proportion
from kuchka import Stress
from kuchka.units import proportion
from kuchka.units.geometry import area
from kuchka.units.mechanics import force
from kuchka.units.mechanics import pressure
from kuchka.units.mechanics import stress


def test_a_pressure_is_read_as_a_stress_in_the_unit_it_carries() -> None:
    reading = pressure.Megapascal(250).to_stress()
    assert isinstance(reading, Stress)
    assert repr(reading) == "250 MPa"


def test_a_stress_is_read_back_as_a_pressure() -> None:
    back = pressure.Megapascal(250).to_stress().to_pressure()
    assert isinstance(back, Pressure)
    assert back == pressure.Megapascal(250)
    assert repr(back) == "250 MPa"


def test_a_stress_and_a_pressure_of_one_value_do_not_mix() -> None:
    with pytest.raises(IncompatibleDimensionError):
        pressure.Pascal(1).to_stress() + pressure.Pascal(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_load_a_section_carries_goes_through_the_pressure() -> None:
    strength = pressure.Megapascal(250).to_stress()
    section = area.SquareMillimetre(100)
    assert strength.to_pressure() * section == force.Kilonewton(25)
    with pytest.raises(IncompatibleDimensionError, match="to_pressure"):
        strength * section


def test_the_stiffness_of_steel_is_stated_in_gigapascals() -> None:
    modulus = pressure.Gigapascal(200).to_stress()
    assert modulus == pressure.Megapascal(200_000).to_stress()
    assert repr(modulus) == "200 GPa"


def test_a_kilopound_per_square_inch_is_a_thousand_pounds_per_square_inch() -> None:
    assert pressure.KilopoundPerSquareInch(1) == pressure.PoundPerSquareInch(1000)


def test_a_ksi_is_exact_from_the_definitions_of_the_pound_force_and_the_inch() -> None:
    pound_force = Fraction(44482216152605, 10**13)
    inch = Fraction(254, 10**4)
    expected = 1000 * pound_force / (inch * inch)
    assert pressure.KilopoundPerSquareInch(1).to(pressure.PASCAL) == pressure.Pascal(
        expected
    )
    assert repr(pressure.KilopoundPerSquareInch(36).to(pressure.MEGAPASCAL)).startswith(
        "248.2112625540610081"
    )


def test_a_proportion_of_a_stress_is_a_stress() -> None:
    utilisation = proportion.Percent(80) * pressure.Megapascal(250).to_stress()
    assert isinstance(utilisation, Stress)
    assert utilisation == pressure.Megapascal(200).to_stress()


def test_the_ratio_of_two_stresses_is_a_proportion() -> None:
    ratio = pressure.Megapascal(100).to_stress() / pressure.Megapascal(250).to_stress()
    assert isinstance(ratio, Proportion)
    assert ratio == proportion.Ratio(Fraction(2, 5))


def test_the_stress_table_reads_a_number_in_a_unit_as_a_stress() -> None:
    assert stress.STRESS_UNITS["GPa"](200) == pressure.Gigapascal(200).to_stress()
    assert isinstance(stress.STRESS_UNITS["ksi"](36), Stress)
    assert repr(stress.STRESS_UNITS["MPa"](250)) == "250 MPa"


def test_the_stress_table_accepts_the_text_of_the_pressure_table() -> None:
    reference = pressure.PRESSURE_UNITS
    assert list(stress.STRESS_UNITS) == list(reference)
    for unit in reference.units:
        for spelling in (unit.symbol, *unit.aliases, *unit.words, unit.name):
            assert spelling in stress.STRESS_UNITS, spelling
