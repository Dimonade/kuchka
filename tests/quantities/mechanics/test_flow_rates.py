"""VolumetricFlowRate and MassFlowRate: the relations that make a flow a flow."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import IncompatibleDimensionError
from kuchka import Mass
from kuchka import MassFlowRate
from kuchka import Power
from kuchka import Volume
from kuchka import VolumetricFlowRate
from kuchka.units import length
from kuchka.units import mass
from kuchka.units.geometry import area
from kuchka.units.geometry import volume
from kuchka.units.kinematics import velocity
from kuchka.units.mechanics import density
from kuchka.units.mechanics import mass_flow_rate
from kuchka.units.mechanics import power
from kuchka.units.mechanics import pressure
from kuchka.units.mechanics import specific_energy
from kuchka.units.mechanics import volumetric_flow_rate as vfr
from kuchka.units.temporal import time


def test_a_volume_over_a_time_is_a_volumetric_flow_rate() -> None:
    flow = volume.Litre(10) / time.Second(40)
    assert isinstance(flow, VolumetricFlowRate)
    assert flow == vfr.LitrePerMinute(15)


def test_an_area_times_a_velocity_is_a_volumetric_flow_rate() -> None:
    flow = area.SquareMetre(0.05) * velocity.MetrePerSecond(2)
    assert isinstance(flow, VolumetricFlowRate)
    assert flow == vfr.CubicMetrePerSecond(0.1)
    assert velocity.MetrePerSecond(2) * area.SquareMetre(0.05) == flow


def test_a_flow_rate_times_a_time_is_a_volume() -> None:
    carried = vfr.LitrePerMinute(60) * time.Minute(2)
    assert isinstance(carried, Volume)
    assert carried == volume.Litre(120)


def test_a_flow_rate_over_an_area_is_a_velocity() -> None:
    speed = vfr.CubicMetrePerSecond(0.1) / area.SquareMetre(0.05)
    assert speed == velocity.MetrePerSecond(2)


def test_a_mass_over_a_time_is_a_mass_flow_rate() -> None:
    flow = mass.Kilogram(36) / time.Hour(1)
    assert isinstance(flow, MassFlowRate)
    assert flow == mass_flow_rate.KilogramPerHour(36)


def test_a_mass_flow_rate_times_a_time_is_a_mass() -> None:
    carried = mass_flow_rate.TonnePerHour(3.6) * time.Hour(1)
    assert isinstance(carried, Mass)
    assert carried == mass.Tonne(3.6)


def test_a_density_times_a_volumetric_flow_rate_is_a_mass_flow_rate() -> None:
    flow = density.KilogramPerCubicMetre(800) * vfr.LitrePerSecond(36)
    assert isinstance(flow, MassFlowRate)
    assert flow == mass_flow_rate.KilogramPerSecond(Fraction(144, 5))


def test_a_mass_flow_rate_over_a_density_is_a_volumetric_flow_rate() -> None:
    flow = mass_flow_rate.KilogramPerSecond(1) / density.KilogramPerCubicMetre(1000)
    assert isinstance(flow, VolumetricFlowRate)
    assert flow == vfr.LitrePerSecond(1)


def test_a_pressure_times_a_volumetric_flow_rate_is_a_power() -> None:
    hydraulic = pressure.Bar(2) * vfr.LitrePerSecond(5)
    assert isinstance(hydraulic, Power)
    assert hydraulic == power.Watt(1000)


def test_a_mass_flow_rate_times_a_specific_energy_is_a_power() -> None:
    heat = mass_flow_rate.KilogramPerSecond(2) * specific_energy.JoulePerKilogram(500)
    assert heat == power.Watt(1000)


def test_a_volumetric_flow_rate_is_not_a_mass_flow_rate() -> None:
    with pytest.raises(IncompatibleDimensionError):
        vfr.LitrePerSecond(1) + mass_flow_rate.KilogramPerSecond(1)  # type: ignore[operator]  # ty: ignore[unsupported-operator]


def test_a_cubic_foot_is_exactly_the_foot_cubed() -> None:
    assert volume.CubicFoot(1) == length.Foot(1) * length.Foot(1) * length.Foot(1)


def test_a_us_gallon_is_exactly_231_cubic_inches() -> None:
    litres = volume.UsGallon(1).value_in(volume.LITRE)
    assert litres == Fraction(3_785_411_784, 1_000_000_000)


def test_a_cubic_foot_per_minute_is_a_cubic_foot_each_minute() -> None:
    assert vfr.CubicFootPerMinute(1) * time.Minute(1) == volume.CubicFoot(1)


def test_a_us_gallon_per_minute_is_a_us_gallon_each_minute() -> None:
    assert vfr.UsGallonPerMinute(1) * time.Minute(1) == volume.UsGallon(1)


def test_a_cubic_metre_per_hour_is_a_cubic_metre_each_hour() -> None:
    assert vfr.CubicMetrePerHour(1) * time.Hour(1) == volume.CubicMetre(1)


def test_a_pound_per_hour_is_a_pound_each_hour() -> None:
    assert mass_flow_rate.PoundPerHour(1) * time.Hour(1) == mass.Pound(1)
