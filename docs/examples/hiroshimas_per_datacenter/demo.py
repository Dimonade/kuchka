"""Run this file directly: `python demo.py` from this directory.

Counts the heat of the site in Hiroshimas, sets it beside sunlight and a nuclear
plant, and shows how much the efficiency of the gas plant matters.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from heat_budget import HIROSHIMA
from heat_budget import Plant
from heat_budget import blast_power
from heat_budget import heat_per_area
from heat_budget import hiroshimas_per_day
from heat_budget import hiroshimas_per_supercenter
from heat_budget import insolation
from heat_budget import load_scenario
from heat_budget import time_per_hiroshima

from kuchka import Day
from kuchka import Millisecond
from kuchka import Percent
from kuchka import Proportion
from kuchka.units import ACRE
from kuchka.units import GIGAWATT
from kuchka.units import KILOWATT_HOUR_PER_SQUARE_METRE
from kuchka.units import MEGAJOULE_PER_SQUARE_METRE
from kuchka.units import MINUTE
from kuchka.units import PETAWATT
from kuchka.units import TERAJOULE

HERE = Path(__file__).parent


def _count(count: Proportion, places: int = 1) -> str:
    return f"{float(count.magnitude):,.{places}f}"


def main() -> None:
    """Report on the shipped site, then vary the efficiency of its plant."""
    scenario = load_scenario(HERE / "site_spec.toml")
    site = scenario.site
    plant = site.plant
    heat = site.total_heat

    print(f"A Hiroshima is {HIROSHIMA} = {HIROSHIMA.to(TERAJOULE):.2f}\n")

    print("The site, as the post describes it:\n")
    print(
        f"  servers draw                   {plant.electrical_output.to(GIGAWATT):.0f}"
    )
    print(f"  gas plant efficiency           {plant.efficiency}")
    print(f"  waste heat of the plant        {plant.waste_heat.to(GIGAWATT):.2f}")
    print(f"  all heat the site releases     {heat.to(GIGAWATT):.2f}")
    print(f"  per day                        {(heat * Day(1)).to(TERAJOULE):.0f}")
    print(f"  in Hiroshimas per day          {_count(hiroshimas_per_day(heat))}")
    print(f"  one Hiroshima of heat every    {time_per_hiroshima(heat).to(MINUTE):.1f}")
    per_store = _count(hiroshimas_per_supercenter(heat, site), 4)
    print(
        f"  per Walmart Supercenter        {per_store} Hiroshimas per day"
        f" ({site.supercenter.to(ACRE):.0f} each)"
    )

    print("\nAgainst what else the ground and the sky deliver:\n")
    sun = insolation(site)
    site_heat = heat_per_area(heat, site)
    for label, fluence in (("sunlight", sun), ("site heat", site_heat)):
        print(
            f"  {label + ' per m2 and day':<30} "
            f"{fluence.to(MEGAJOULE_PER_SQUARE_METRE):.1f}, "
            f"{fluence.to(KILOWATT_HOUR_PER_SQUARE_METRE):.1f}"
        )
    nuclear = scenario.nuclear_reference
    vented = _count(hiroshimas_per_day(nuclear.waste_heat))
    label = f"nuclear plant, {nuclear.electrical_output.to(GIGAWATT):.1f}"
    print(f"  {label:<30} {vented} Hiroshimas a day vented")

    print("\nWhy the comparison misleads:\n")
    blast = blast_power(Millisecond(1))
    print(f"  one Hiroshima in 1 ms          {blast.to(PETAWATT):.2f}")
    print(f"  against the site's heat        {_count(blast / heat, 0)} times as fast")

    print("\nWhat the efficiency of the gas plant changes:\n")
    for efficiency in (Percent(50), Percent(53), Percent(55)):
        varied = replace(site, plant=Plant(plant.electrical_output, efficiency))
        count = _count(hiroshimas_per_day(varied.total_heat))
        print(f"  efficiency {efficiency!s:<6} {count} Hiroshimas a day")


if __name__ == "__main__":
    main()
