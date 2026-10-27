"""MagneticFluxDensity: the weber per square metre, and the quantities it relates to.

The generic behaviour of a quantity type is covered once for every type;
this module covers what is specific to the tesla and the gauss.
"""

from __future__ import annotations

import pytest

from kuchka import Area
from kuchka import IncompatibleDimensionError
from kuchka import MagneticFlux
from kuchka import MagneticFluxDensity
from kuchka.units.electromagnetics import magnetic_flux
from kuchka.units.electromagnetics import magnetic_flux_density
from kuchka.units.geometry import area


def test_a_tesla_over_a_square_metre_is_a_weber() -> None:
    flux = magnetic_flux_density.Tesla(2) * area.SquareMetre(3)
    assert isinstance(flux, MagneticFlux)
    assert flux == magnetic_flux.Weber(6)


def test_the_area_commutes() -> None:
    assert area.SquareMetre(3) * magnetic_flux_density.Millitesla(2) == (
        magnetic_flux.Milliweber(6)
    )


def test_a_flux_over_a_flux_density_is_an_area() -> None:
    swept = magnetic_flux.Weber(6) / magnetic_flux_density.Tesla(2)
    assert isinstance(swept, Area)
    assert swept == area.SquareMetre(3)


def test_a_tesla_through_a_square_centimetre_is_a_hundred_microweber() -> None:
    flux = magnetic_flux_density.Tesla(1) * area.SquareCentimetre(1)
    assert flux == magnetic_flux.Microweber(100)


def test_a_flux_density_is_not_a_flux() -> None:
    with pytest.raises(IncompatibleDimensionError):
        magnetic_flux_density.Tesla(1) + magnetic_flux.Weber(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_the_tesla_is_known_by_its_weber_per_square_metre_spellings() -> None:
    from kuchka.units import MAGNETIC_FLUX_DENSITY_UNITS

    assert MAGNETIC_FLUX_DENSITY_UNITS["Wb/m²"] is magnetic_flux_density.Tesla
    assert isinstance(MAGNETIC_FLUX_DENSITY_UNITS["mT"](3), MagneticFluxDensity)


def test_a_gauss_is_a_ten_thousandth_of_a_tesla() -> None:
    assert magnetic_flux_density.Gauss(10_000) == magnetic_flux_density.Tesla(1)


def test_a_gauss_through_a_square_centimetre_is_ten_nanoweber() -> None:
    flux = magnetic_flux_density.Gauss(1) * area.SquareCentimetre(1)
    assert flux == magnetic_flux.Nanoweber(10)


def test_the_gauss_is_known_by_its_plural_and_by_gs() -> None:
    from kuchka.units import MAGNETIC_FLUX_DENSITY_UNITS

    assert MAGNETIC_FLUX_DENSITY_UNITS["Gs"] is magnetic_flux_density.Gauss
    assert MAGNETIC_FLUX_DENSITY_UNITS["gausses"] is magnetic_flux_density.Gauss
