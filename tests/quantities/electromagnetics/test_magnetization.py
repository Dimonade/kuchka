"""Magnetization: a role of MagneticFieldStrength that reads the ampere per metre.

The generic role behaviour (refusals, scaling) is covered once for every role in
`test_role_kinds`; this module covers what is specific to magnetization.
"""

from __future__ import annotations

import pytest

from kuchka import IncompatibleDimensionError
from kuchka import MagneticFieldStrength
from kuchka import MagneticFluxDensity
from kuchka import Magnetization
from kuchka import parse
from kuchka.units.electromagnetics import magnetic_field_strength as field
from kuchka.units.electromagnetics import magnetic_flux_density
from kuchka.units.electromagnetics import magnetization
from kuchka.units.electromagnetics import permeability


def test_a_field_strength_is_viewed_as_a_magnetization_and_back() -> None:
    reading = field.KiloamperePerMetre(2).to_magnetization()
    assert isinstance(reading, Magnetization)
    assert reading.to_magnetic_field_strength() == field.KiloamperePerMetre(2)


def test_a_magnetization_and_a_field_strength_do_not_add_directly() -> None:
    with pytest.raises(IncompatibleDimensionError):
        field.AmperePerMetre(1).to_magnetization() + field.AmperePerMetre(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_total_field_adds_the_magnetization_to_the_applied_field() -> None:
    applied = field.AmperePerMetre(1000)
    response = magnetization.MAGNETIZATION_UNITS["A/m"](3000)
    total = applied + response.to_magnetic_field_strength()
    assert isinstance(total, MagneticFieldStrength)
    flux = permeability.MicrohenryPerMetre(2) * total
    assert isinstance(flux, MagneticFluxDensity)
    assert flux == magnetic_flux_density.Millitesla(8)


def test_a_magnetization_is_not_scaled_by_a_permeability_directly() -> None:
    with pytest.raises(IncompatibleDimensionError):
        permeability.HenryPerMetre(1) * field.AmperePerMetre(1).to_magnetization()  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_table_reads_a_number_in_a_unit_as_a_magnetization() -> None:
    reading = magnetization.MAGNETIZATION_UNITS["kA/m"](3)
    assert isinstance(reading, Magnetization)
    assert reading == field.KiloamperePerMetre(3).to_magnetization()
    assert repr(reading) == "3 kA/m"


def test_the_table_accepts_the_spellings_of_the_field_strength_table() -> None:
    assert list(magnetization.MAGNETIZATION_UNITS) == list(
        field.MAGNETIC_FIELD_STRENGTH_UNITS
    )


def test_a_magnetization_is_read_from_text_through_its_own_table() -> None:
    assert parse("1.71 MA/m", Magnetization) == (
        field.MegaamperePerMetre(1.71).to_magnetization()
    )
