"""Energy density constructors: joules per cubic metre and watt-hours per litre.

    from kuchka import MegajoulePerCubicMetre, WattHourPerLitre

    diesel = MegajoulePerCubicMetre(36_000)
    battery_cell = WattHourPerLitre(650)

`WattHourPerLitre` is the unit volumetric battery capacity is quoted in.
Its scale is computed from kuchka's own exact `WATT_HOUR` and `LITRE` scales, so it
cannot drift from either: one watt-hour per litre is `3 600 000` J/m³.

`ENERGY_DENSITY_UNITS` maps each symbol to its constructor, for boundary code that
reads a unit as a string from outside the application.
These units belong to `EnergyDensity` and are refused by `Pressure`, which shares
their dimension.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import ENERGY_DENSITY
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import EnergyDensity
from kuchka.quantities import UnitDef
from kuchka.units.geometry.volume import LITRE
from kuchka.units.mechanics.energy import WATT_HOUR

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

_PER_CUBIC_METRE = f"J/m{symbols.SUPERSCRIPT_THREE}"

JOULE_PER_CUBIC_METRE = UnitDef(
    "joule_per_cubic_metre", _PER_CUBIC_METRE, Decimal(1), ENERGY_DENSITY
)
KILOJOULE_PER_CUBIC_METRE = UnitDef(
    "kilojoule_per_cubic_metre", f"k{_PER_CUBIC_METRE}", Decimal(1000), ENERGY_DENSITY
)
MEGAJOULE_PER_CUBIC_METRE = UnitDef(
    "megajoule_per_cubic_metre",
    f"M{_PER_CUBIC_METRE}",
    Decimal(1_000_000),
    ENERGY_DENSITY,
)
WATT_HOUR_PER_LITRE = UnitDef(
    "watt_hour_per_litre", "Wh/L", WATT_HOUR.scale / LITRE.scale, ENERGY_DENSITY
)

JOULE_PER_CUBIC_METER = JOULE_PER_CUBIC_METRE
KILOJOULE_PER_CUBIC_METER = KILOJOULE_PER_CUBIC_METRE
MEGAJOULE_PER_CUBIC_METER = MEGAJOULE_PER_CUBIC_METRE
WATT_HOUR_PER_LITER = WATT_HOUR_PER_LITRE

EnergyDensity._canonical_unit = JOULE_PER_CUBIC_METRE  # noqa: SLF001 -- this module owns EnergyDensity's canonical unit


def JoulePerCubicMetre(value: Numeric) -> EnergyDensity:
    """Construct an EnergyDensity from a magnitude in joules per cubic metre."""
    return EnergyDensity(
        to_exact(value) * JOULE_PER_CUBIC_METRE.scale, JOULE_PER_CUBIC_METRE
    )


def KilojoulePerCubicMetre(value: Numeric) -> EnergyDensity:
    """Construct an EnergyDensity from a magnitude in kilojoules per cubic metre."""
    return EnergyDensity(
        to_exact(value) * KILOJOULE_PER_CUBIC_METRE.scale, KILOJOULE_PER_CUBIC_METRE
    )


def MegajoulePerCubicMetre(value: Numeric) -> EnergyDensity:
    """Construct an EnergyDensity from a magnitude in megajoules per cubic metre."""
    return EnergyDensity(
        to_exact(value) * MEGAJOULE_PER_CUBIC_METRE.scale, MEGAJOULE_PER_CUBIC_METRE
    )


def WattHourPerLitre(value: Numeric) -> EnergyDensity:
    """Construct an EnergyDensity from a magnitude expressed in watt-hours per litre."""
    return EnergyDensity(
        to_exact(value) * WATT_HOUR_PER_LITRE.scale, WATT_HOUR_PER_LITRE
    )


JoulePerCubicMeter = JoulePerCubicMetre
KilojoulePerCubicMeter = KilojoulePerCubicMetre
MegajoulePerCubicMeter = MegajoulePerCubicMetre
WattHourPerLiter = WattHourPerLitre


ENERGY_DENSITY_UNITS: Mapping[str, Callable[[Numeric], EnergyDensity]] = unit_table(
    "ENERGY_DENSITY_UNITS",
    {
        JOULE_PER_CUBIC_METRE: JoulePerCubicMetre,
        KILOJOULE_PER_CUBIC_METRE: KilojoulePerCubicMetre,
        MEGAJOULE_PER_CUBIC_METRE: MegajoulePerCubicMetre,
        WATT_HOUR_PER_LITRE: WattHourPerLitre,
    },
)

__all__ = [
    "ENERGY_DENSITY_UNITS",
    "JOULE_PER_CUBIC_METER",
    "JOULE_PER_CUBIC_METRE",
    "KILOJOULE_PER_CUBIC_METER",
    "KILOJOULE_PER_CUBIC_METRE",
    "MEGAJOULE_PER_CUBIC_METER",
    "MEGAJOULE_PER_CUBIC_METRE",
    "WATT_HOUR_PER_LITER",
    "WATT_HOUR_PER_LITRE",
    "JoulePerCubicMeter",
    "JoulePerCubicMetre",
    "KilojoulePerCubicMeter",
    "KilojoulePerCubicMetre",
    "MegajoulePerCubicMeter",
    "MegajoulePerCubicMetre",
    "WattHourPerLiter",
    "WattHourPerLitre",
]
