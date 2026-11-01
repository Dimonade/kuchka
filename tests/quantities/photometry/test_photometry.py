"""LuminousFlux and Illuminance: how the candela, the steradian, and the lux combine."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Area
from kuchka import Illuminance
from kuchka import IncompatibleDimensionError
from kuchka import LuminousFlux
from kuchka import LuminousIntensity
from kuchka import SolidAngle
from kuchka.units import length
from kuchka.units import luminous_intensity
from kuchka.units import solid_angle
from kuchka.units.geometry import area
from kuchka.units.photometry import illuminance
from kuchka.units.photometry import luminous_flux


def test_a_candela_steradian_is_a_lumen() -> None:
    flux = luminous_intensity.Candela(120) * solid_angle.Steradian(2)
    assert isinstance(flux, LuminousFlux)
    assert flux == luminous_flux.Lumen(240)


def test_the_solid_angle_commutes() -> None:
    assert solid_angle.Steradian(2) * luminous_intensity.Candela(3) == (
        luminous_flux.Lumen(6)
    )


def test_a_flux_over_a_solid_angle_is_an_intensity() -> None:
    intensity = luminous_flux.Lumen(240) / solid_angle.Steradian(2)
    assert isinstance(intensity, LuminousIntensity)
    assert intensity == luminous_intensity.Candela(120)


def test_a_flux_over_an_intensity_is_a_solid_angle() -> None:
    cone = luminous_flux.Lumen(240) / luminous_intensity.Candela(120)
    assert isinstance(cone, SolidAngle)
    assert cone == solid_angle.Steradian(2)


def test_a_lumen_per_square_metre_is_a_lux() -> None:
    lit = luminous_flux.Lumen(800) / area.SquareMetre(4)
    assert isinstance(lit, Illuminance)
    assert lit == illuminance.Lux(200)


def test_a_lux_over_a_square_metre_is_a_lumen() -> None:
    assert illuminance.Lux(200) * area.SquareMetre(4) == luminous_flux.Lumen(800)
    assert area.SquareMetre(4) * illuminance.Lux(200) == luminous_flux.Lumen(800)


def test_a_flux_over_an_illuminance_is_an_area() -> None:
    lit = luminous_flux.Lumen(800) / illuminance.Lux(200)
    assert isinstance(lit, Area)
    assert lit == area.SquareMetre(4)


def test_a_flux_is_not_an_intensity() -> None:
    with pytest.raises(IncompatibleDimensionError):
        luminous_flux.Lumen(1) + luminous_intensity.Candela(1)  # type: ignore[operator]


def test_a_flux_is_not_an_illuminance() -> None:
    with pytest.raises(IncompatibleDimensionError):
        luminous_flux.Lumen(1) + illuminance.Lux(1)  # type: ignore[operator]


def test_the_lumen_is_known_by_its_candela_steradian_spellings() -> None:
    from kuchka.units import LUMINOUS_FLUX_UNITS

    assert LUMINOUS_FLUX_UNITS["cd*sr"] is luminous_flux.Lumen
    assert LUMINOUS_FLUX_UNITS["candela steradian"] is luminous_flux.Lumen


def test_the_lux_is_known_by_its_lumen_per_square_metre_spellings() -> None:
    from kuchka.units import ILLUMINANCE_UNITS

    assert ILLUMINANCE_UNITS["lm/m²"] is illuminance.Lux
    assert ILLUMINANCE_UNITS["lm/m^2"] is illuminance.Lux
    assert ILLUMINANCE_UNITS["klx"] is illuminance.Kilolux


def test_a_phot_is_ten_thousand_lux() -> None:
    assert illuminance.Phot(1) == illuminance.Lux(10_000)


def test_a_phot_is_a_lumen_per_square_centimetre() -> None:
    assert luminous_flux.Lumen(1) / area.SquareCentimetre(1) == illuminance.Phot(1)


def test_a_foot_candle_is_a_lumen_per_square_foot() -> None:
    square_foot = length.Foot(1) * length.Foot(1)
    assert luminous_flux.Lumen(1) / square_foot == illuminance.FootCandle(1)


def test_a_foot_candle_is_exactly_one_over_a_square_foot_in_lux() -> None:
    lux = illuminance.FootCandle(1).value_in(illuminance.LUX)
    assert lux == Fraction(100_000_000, 9_290_304)
