"""Tests for heat_budget.py.

This directory is documentation, not part of the installed `kuchka` package, so
`heat_budget` is imported by adding this directory to `sys.path`, not through a
package import.

Run with `pytest docs/examples/hiroshimas_per_datacenter` from the repository root,
or `pytest` from inside this directory.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
from heat_budget import HIROSHIMA
from heat_budget import Plant
from heat_budget import blast_power
from heat_budget import heat_per_area
from heat_budget import hiroshimas
from heat_budget import hiroshimas_per_day
from heat_budget import hiroshimas_per_supercenter
from heat_budget import insolation
from heat_budget import load_scenario
from heat_budget import one_hiroshima_per_supercenter
from heat_budget import time_per_hiroshima

from kuchka import Acre
from kuchka import Day
from kuchka import Fluence
from kuchka import Gigawatt
from kuchka import KilowattHourPerSquareMetre
from kuchka import Millisecond
from kuchka import Percent
from kuchka import Petawatt
from kuchka import Power
from kuchka import Proportion
from kuchka import Terajoule
from kuchka.errors import UnknownUnitError

SPEC = Path(__file__).parent / "site_spec.toml"
SCENARIO = load_scenario(SPEC)
SITE = SCENARIO.site
SUPERCENTERS = 2000


def count(proportion: Proportion) -> float:
    return float(proportion.magnitude)


def test_a_hiroshima_is_fifteen_kilotonnes_of_tnt() -> None:
    assert Terajoule(Fraction(6276, 100)) == HIROSHIMA


def test_the_spec_reads_into_typed_quantities() -> None:
    assert SITE.plant.electrical_output == Gigawatt(9)
    assert SITE.plant.efficiency == Percent(53)
    assert SITE.area == Acre(40_000)
    assert SITE.supercenters == SUPERCENTERS
    assert SITE.sunlight_per_day == Terajoule(3200)


def test_the_plant_wastes_about_eight_gigawatts() -> None:
    assert abs(SITE.plant.waste_heat - Gigawatt(8)) < Gigawatt(0.1)


def test_the_servers_and_the_waste_make_all_the_heat_of_the_fuel() -> None:
    assert SITE.total_heat == SITE.plant.thermal_input
    assert SITE.total_heat == Gigawatt(Fraction(900, 53))


def test_the_site_releases_about_23_hiroshimas_a_day() -> None:
    assert count(hiroshimas_per_day(SITE.total_heat)) == pytest.approx(23.4, abs=0.05)


def test_the_site_releases_a_hiroshima_of_heat_about_every_hour() -> None:
    hours = time_per_hiroshima(SITE.total_heat) / Day(1) * 24
    assert count(hours) == pytest.approx(1.03, abs=0.01)


def test_a_supercenter_is_twenty_acres() -> None:
    assert SITE.supercenter == Acre(20)


def test_the_unit_of_the_thread_is_one_hiroshima_on_a_supercenter() -> None:
    reference = one_hiroshima_per_supercenter(SITE)
    assert type(reference) is Fluence
    assert reference == HIROSHIMA / Acre(20)


def test_the_heat_per_supercenter_is_the_number_of_the_thread() -> None:
    per_supercenter = hiroshimas_per_supercenter(SITE.total_heat, SITE)
    assert count(per_supercenter) == pytest.approx(0.0117, abs=0.0001)


def test_per_supercenter_is_the_daily_count_over_the_number_of_supercenters() -> None:
    per_day = hiroshimas_per_day(SITE.total_heat)
    assert hiroshimas_per_supercenter(SITE.total_heat, SITE) == per_day / SUPERCENTERS


def test_sunlight_on_the_plot_is_about_fifty_hiroshimas_a_day() -> None:
    assert count(hiroshimas(SITE.sunlight_per_day)) == pytest.approx(51, abs=0.5)


def test_sunlight_on_the_plot_is_about_five_and_a_half_kilowatt_hours() -> None:
    sun = insolation(SITE)
    assert type(sun) is Fluence
    assert abs(sun - KilowattHourPerSquareMetre(5.5)) < KilowattHourPerSquareMetre(0.05)


def test_the_site_heats_the_ground_less_than_the_sun_does() -> None:
    assert heat_per_area(SITE.total_heat, SITE) < insolation(SITE)


def test_a_nuclear_plant_vents_about_nine_hiroshimas_a_day() -> None:
    vented = hiroshimas_per_day(SCENARIO.nuclear_reference.waste_heat)
    assert count(vented) == pytest.approx(9.2, abs=0.05)


def test_one_hiroshima_in_a_millisecond_is_tens_of_petawatts() -> None:
    blast = blast_power(Millisecond(1))
    assert blast == Petawatt(Fraction(6276, 100))
    assert blast > SITE.total_heat * 3_000_000


@pytest.mark.parametrize(
    ("efficiency", "hiroshimas_a_day"),
    [(50, 24.8), (53, 23.4), (55, 22.5)],
)
def test_a_less_efficient_plant_releases_more_heat(
    efficiency: int, hiroshimas_a_day: float
) -> None:
    plant = Plant(Gigawatt(9), Percent(efficiency))
    assert count(hiroshimas_per_day(plant.thermal_input)) == pytest.approx(
        hiroshimas_a_day, abs=0.05
    )


def test_the_total_heat_is_a_power() -> None:
    assert isinstance(SITE.total_heat, Power)


def test_a_figure_in_the_wrong_unit_is_refused_at_the_boundary(tmp_path: Path) -> None:
    broken = tmp_path / "site_spec.toml"
    broken.write_text(SPEC.read_text(encoding="utf-8").replace('"9 GW"', '"9 A"'))
    with pytest.raises(UnknownUnitError):
        load_scenario(broken)


def test_a_figure_with_no_unit_is_refused_at_the_boundary(tmp_path: Path) -> None:
    broken = tmp_path / "site_spec.toml"
    broken.write_text(SPEC.read_text(encoding="utf-8").replace('"9 GW"', "9"))
    with pytest.raises(TypeError):
        load_scenario(broken)
