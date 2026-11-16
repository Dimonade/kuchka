"""Luminous energy and exposure, luminance, and luminous efficacy: how they combine."""

from __future__ import annotations

import math

import pytest

from kuchka import Illuminance
from kuchka import IncompatibleDimensionError
from kuchka import Luminance
from kuchka import LuminousEfficacy
from kuchka import LuminousEnergy
from kuchka import LuminousExposure
from kuchka import LuminousFlux
from kuchka import LuminousIntensity
from kuchka import Power
from kuchka import Time
from kuchka.units import length
from kuchka.units import luminous_intensity
from kuchka.units import solid_angle
from kuchka.units.geometry import area
from kuchka.units.mechanics import power
from kuchka.units.photometry import illuminance
from kuchka.units.photometry import luminance
from kuchka.units.photometry import luminous_efficacy
from kuchka.units.photometry import luminous_energy
from kuchka.units.photometry import luminous_exposure
from kuchka.units.photometry import luminous_flux
from kuchka.units.temporal import time


def test_a_lumen_over_a_second_is_a_lumen_second() -> None:
    energy = luminous_flux.Lumen(5) * time.Second(3)
    assert isinstance(energy, LuminousEnergy)
    assert energy == luminous_energy.LumenSecond(15)


def test_an_energy_over_a_time_is_a_flux() -> None:
    flux = luminous_energy.LumenSecond(15) / time.Second(3)
    assert isinstance(flux, LuminousFlux)
    assert flux == luminous_flux.Lumen(5)


def test_a_lumen_hour_is_3600_lumen_seconds() -> None:
    assert luminous_energy.LumenHour(1) == luminous_energy.LumenSecond(3600)


def test_a_lux_over_a_second_is_a_lux_second() -> None:
    exposure = illuminance.Lux(5) * time.Second(3)
    assert isinstance(exposure, LuminousExposure)
    assert exposure == luminous_exposure.LuxSecond(15)


def test_an_exposure_over_an_illuminance_is_a_time() -> None:
    elapsed = luminous_exposure.LuxHour(400) / illuminance.Lux(50)
    assert isinstance(elapsed, Time)
    assert elapsed == time.Hour(8)


def test_an_energy_over_an_area_is_an_exposure() -> None:
    exposure = luminous_energy.LumenSecond(8) / area.SquareMetre(4)
    assert isinstance(exposure, LuminousExposure)
    assert exposure == luminous_exposure.LuxSecond(2)


def test_a_kilolux_hour_is_a_thousand_lux_hours() -> None:
    assert luminous_exposure.KiloluxHour(1) == luminous_exposure.LuxHour(1000)


def test_a_candela_over_a_square_metre_is_a_luminance() -> None:
    bright = luminous_intensity.Candela(100) / area.SquareMetre(0.5)
    assert isinstance(bright, Luminance)
    assert bright == luminance.CandelaPerSquareMetre(200)


def test_a_luminance_over_an_area_is_an_intensity_and_back() -> None:
    seen = luminance.CandelaPerSquareMetre(200) * area.SquareMetre(0.5)
    assert isinstance(seen, LuminousIntensity)
    assert seen == luminous_intensity.Candela(100)


def test_a_luminance_over_a_solid_angle_is_an_illuminance() -> None:
    lit = luminance.CandelaPerSquareMetre(10) * solid_angle.Steradian(2)
    assert isinstance(lit, Illuminance)
    assert lit == illuminance.Lux(20)


def test_a_luminance_is_not_an_illuminance() -> None:
    with pytest.raises(IncompatibleDimensionError):
        luminance.CandelaPerSquareMetre(1) + illuminance.Lux(1)  # type: ignore[operator]


def test_a_nit_is_a_candela_per_square_metre() -> None:
    from kuchka.units import LUMINANCE_UNITS

    assert LUMINANCE_UNITS["nit"] is luminance.CandelaPerSquareMetre
    assert LUMINANCE_UNITS["nits"] is luminance.CandelaPerSquareMetre
    assert LUMINANCE_UNITS["cd/m2"] is luminance.CandelaPerSquareMetre
    assert LUMINANCE_UNITS["kilonit"] is luminance.KilocandelaPerSquareMetre


def test_a_stilb_is_a_candela_per_square_centimetre() -> None:
    per_area = luminous_intensity.Candela(1) / area.SquareCentimetre(1)
    assert per_area == luminance.Stilb(1)
    assert luminance.Stilb(1) == luminance.CandelaPerSquareMetre(10_000)


def test_a_foot_lambert_is_a_candela_per_square_foot_over_pi() -> None:
    square_foot = length.Foot(1) * length.Foot(1)
    per_foot = luminous_intensity.Candela(1) / square_foot
    in_foot_lamberts = per_foot.value_in(luminance.FOOT_LAMBERT)
    assert float(in_foot_lamberts) == pytest.approx(math.pi, rel=1e-15)


def test_a_lumen_over_a_watt_is_an_efficacy() -> None:
    rating = luminous_flux.Lumen(1000) / power.Watt(10)
    assert isinstance(rating, LuminousEfficacy)
    assert rating == luminous_efficacy.LumenPerWatt(100)


def test_an_efficacy_times_a_power_is_a_flux() -> None:
    flux = luminous_efficacy.LumenPerWatt(100) * power.Watt(10)
    assert isinstance(flux, LuminousFlux)
    assert flux == luminous_flux.Lumen(1000)
    assert power.Watt(10) * luminous_efficacy.LumenPerWatt(100) == flux


def test_a_flux_over_an_efficacy_is_a_power() -> None:
    drawn = luminous_flux.Lumen(1000) / luminous_efficacy.LumenPerWatt(100)
    assert isinstance(drawn, Power)
    assert drawn == power.Watt(10)


def test_the_efficacy_is_known_by_its_candela_steradian_spelling() -> None:
    from kuchka.units import LUMINOUS_EFFICACY_UNITS

    assert LUMINOUS_EFFICACY_UNITS["cd*sr/W"] is luminous_efficacy.LumenPerWatt


def test_a_talbot_is_a_lumen_second() -> None:
    from kuchka.units import LUMINOUS_ENERGY_UNITS

    assert LUMINOUS_ENERGY_UNITS["talbot"] is luminous_energy.LumenSecond
    assert LUMINOUS_ENERGY_UNITS["lm*h"] is luminous_energy.LumenHour
