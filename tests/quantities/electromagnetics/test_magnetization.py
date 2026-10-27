"""Magnetization: the ampere per metre, as a current per length.

The generic behaviour of a quantity type is covered once for every type;
this module covers what is specific to the magnetization.
"""

from __future__ import annotations

import pytest

from kuchka import Current
from kuchka import IncompatibleDimensionError
from kuchka import Length
from kuchka import Magnetization
from kuchka import MagneticFluxDensity
from kuchka import Permeability
from kuchka.units import current
from kuchka.units import length
from kuchka.units.electromagnetics import magnetization as field
from kuchka.units.electromagnetics import magnetic_flux_density
from kuchka.units.electromagnetics import permeability


def test_a_current_per_length_is_a_magnetization() -> None:
    strength = current.Ampere(6) / length.Metre(3)
    assert isinstance(strength, Magnetization)
    assert strength == field.AmperePerMetre(2)


def test_a_magnetization_over_a_length_is_a_current() -> None:
    carried = field.KiloamperePerMetre(2) * length.Metre(3)
    assert isinstance(carried, Current)
    assert carried == current.Kiloampere(6)


def test_a_current_over_a_magnetization_is_a_length() -> None:
    reach = current.Ampere(6) / field.AmperePerMetre(3)
    assert isinstance(reach, Length)
    assert reach == length.Metre(2)


def test_a_permeability_and_a_magnetization_make_a_flux_density() -> None:
    density = permeability.HenryPerMetre(2) * field.AmperePerMetre(3)
    assert isinstance(density, MagneticFluxDensity)
    assert density == magnetic_flux_density.Tesla(6)


def test_a_flux_density_over_a_magnetization_is_a_permeability() -> None:
    material = magnetic_flux_density.Millitesla(2) / field.AmperePerMetre(1000)
    assert isinstance(material, Permeability)
    assert material == permeability.MicrohenryPerMetre(2)


def test_a_flux_density_over_a_permeability_is_a_magnetization() -> None:
    applied = magnetic_flux_density.Tesla(6) / permeability.HenryPerMetre(2)
    assert isinstance(applied, Magnetization)
    assert applied == field.AmperePerMetre(3)


def test_a_magnetization_is_not_a_current() -> None:
    with pytest.raises(IncompatibleDimensionError):
        field.AmperePerMetre(1) + current.Ampere(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_boundary_reads_the_spoken_forms() -> None:
    assert field.MAGNETIZATION_UNITS["kA/m"] is field.KiloamperePerMetre
    assert field.MAGNETIZATION_UNITS["ampere per meter"] is field.AmperePerMetre
