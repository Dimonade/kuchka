"""Power as an energy per minute or hour: the exact scales and the arithmetic."""

from __future__ import annotations

from fractions import Fraction

import pytest

from kuchka import Energy
from kuchka import Power
from kuchka.units import temporal
from kuchka.units.mechanics import energy
from kuchka.units.mechanics import power


@pytest.mark.parametrize(
    ("unit", "watts"),
    [
        (power.JoulePerMinute, Fraction(1, 60)),
        (power.JoulePerHour, Fraction(1, 3600)),
        (power.KilojoulePerMinute, Fraction(50, 3)),
        (power.KilojoulePerHour, Fraction(5, 18)),
        (power.MegajoulePerHour, Fraction(2500, 9)),
        (power.GigajoulePerHour, Fraction(2_500_000, 9)),
    ],
    ids=["J/min", "J/h", "kJ/min", "kJ/h", "MJ/h", "GJ/h"],
)
def test_the_energy_per_time_units_have_exact_scales(unit, watts) -> None:
    assert unit(1) == power.Watt(watts)
    assert unit(1).to(power.WATT).magnitude == watts


def test_a_measured_energy_over_a_time_reads_in_joules_per_hour() -> None:
    consumption = energy.Joule(7200) / temporal.Hour(2)
    assert type(consumption) is Power
    assert consumption.to(power.JOULE_PER_HOUR) == power.JoulePerHour(3600)
    assert consumption.to(power.JOULE_PER_MINUTE) == power.JoulePerMinute(60)


def test_a_power_in_joules_per_hour_times_a_time_is_an_energy() -> None:
    spent = power.MegajoulePerHour(36) * temporal.Hour(2)
    assert type(spent) is Energy
    assert spent == energy.Megajoule(72)


def test_a_consumption_adds_to_a_power_of_another_unit() -> None:
    total = power.JoulePerHour(1800) + power.Milliwatt(500)
    assert total == power.Watt(1)
