"""Heat budget of a power-hungry site, counted in Hiroshimas.

A Hiroshima is a reference `Energy`, the yield of the bomb at fifteen kilotonnes of
TNT, and counting in Hiroshimas is dividing by it, so a count is a `Proportion`.
The same trick makes the unit of the Reddit thread this example comes from,
Hiroshimas per Walmart Supercenter: a reference quantity and a division.

A TOML file holds the figures of the site, and every figure is a number with its
unit.
`load_scenario` reads each of them once with `parse`, and from there on every value is
a typed quantity.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import Final

from kuchka import Area
from kuchka import Day
from kuchka import Energy
from kuchka import HeatFlux
from kuchka import KilotonneOfTNT
from kuchka import Power
from kuchka import Proportion
from kuchka import Time
from kuchka import parse

if TYPE_CHECKING:
    from pathlib import Path

HIROSHIMA: Final[Energy] = KilotonneOfTNT(15)
"""The yield of the Hiroshima bomb, 15 kilotonnes of TNT or 62.76 TJ."""


@dataclass(frozen=True)
class Plant:
    """A plant that turns the heat of a fuel into electricity and waste heat."""

    electrical_output: Power
    efficiency: Proportion

    @property
    def thermal_input(self) -> Power:
        """Return the heat of the fuel, the electricity divided by the efficiency."""
        return self.electrical_output / self.efficiency

    @property
    def waste_heat(self) -> Power:
        """Return the part of the fuel's heat that leaves as waste."""
        return self.thermal_input - self.electrical_output


@dataclass(frozen=True)
class Site:
    """A site whose servers run on the electricity of its own plant."""

    plant: Plant
    area: Area
    supercenters: int
    sunlight_per_day: Energy

    @property
    def total_heat(self) -> Power:
        """Return all the heat the site releases.

        The servers turn their electricity into heat, and the plant releases its
        waste heat beside it.
        """
        return self.plant.electrical_output + self.plant.waste_heat

    @property
    def supercenter(self) -> Area:
        """Return the area of one Walmart Supercenter, as the post counts them."""
        return self.area / self.supercenters


@dataclass(frozen=True)
class Scenario:
    """The site and the plant it is compared with."""

    site: Site
    nuclear_reference: Plant


def hiroshimas(energy: Energy) -> Proportion:
    """Return how many Hiroshimas `energy` is."""
    return energy / HIROSHIMA


def hiroshimas_per_day(power: Power) -> Proportion:
    """Return how many Hiroshimas `power` releases in a day."""
    return hiroshimas(power * Day(1))


def one_hiroshima_per_day_per_supercenter(site: Site) -> HeatFlux:
    """Return the unit of the thread, as a heat flux: a Hiroshima a day on a store.

    Energy per area has no registered type, so the day is part of the unit.
    """
    return HIROSHIMA / Day(1) / site.supercenter


def hiroshimas_per_supercenter(power: Power, site: Site) -> Proportion:
    """Return `power` spread over the site, in Hiroshimas per day per supercenter."""
    return (power / site.area) / one_hiroshima_per_day_per_supercenter(site)


def time_per_hiroshima(power: Power) -> Time:
    """Return the time in which `power` releases the energy of one Hiroshima."""
    return HIROSHIMA / power


def blast_power(duration: Time) -> Power:
    """Return the power of one Hiroshima released within `duration`."""
    return HIROSHIMA / duration


def _plant(table: dict[str, Any], output: str, efficiency: str) -> Plant:
    return Plant(parse(table[output], Power), parse(table[efficiency], Proportion))


def load_scenario(path: Path) -> Scenario:
    """Read the site and the reference plant from the TOML file at `path`."""
    with path.open("rb") as file:
        data = tomllib.load(file)
    site = data["site"]
    plant = _plant(site, "electrical_load", "plant_efficiency")
    return Scenario(
        Site(
            plant,
            parse(site["area"], Area),
            site["supercenters"],
            parse(site["sunlight_per_day"], Energy),
        ),
        _plant(data["nuclear_reference"], "electrical_output", "efficiency"),
    )
