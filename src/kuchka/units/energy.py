"""Energy unit constructors: Picojoule through Megajoule.

Each function here does the same thing: take a plain number, multiply it by a fixed
scale factor, and wrap it in :class:`~kuchka.quantities.Energy`.

    from kuchka import Joule, Millijoule

    pulse_energy = Millijoule(2) + Microjoule(500)

`ENERGY_UNITS` maps each symbol to its constructor, for boundary code that reads a unit
as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import ENERGY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Energy
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


JOULE_NAME = "joule"
JOULE_SYMBOL = "J"

PICOJOULE = prefixed_unit(prefixes.PICO, JOULE_NAME, JOULE_SYMBOL, ENERGY)
NANOJOULE = prefixed_unit(prefixes.NANO, JOULE_NAME, JOULE_SYMBOL, ENERGY)
MICROJOULE = prefixed_unit(prefixes.MICRO, JOULE_NAME, JOULE_SYMBOL, ENERGY)
MILLIJOULE = prefixed_unit(prefixes.MILLI, JOULE_NAME, JOULE_SYMBOL, ENERGY)
JOULE = prefixed_unit(prefixes.UNIT, JOULE_NAME, JOULE_SYMBOL, ENERGY)
KILOJOULE = prefixed_unit(prefixes.KILO, JOULE_NAME, JOULE_SYMBOL, ENERGY)
MEGAJOULE = prefixed_unit(prefixes.MEGA, JOULE_NAME, JOULE_SYMBOL, ENERGY)


Energy._canonical_unit = JOULE  # noqa: SLF001 -- this module owns Energy's canonical unit


def Picojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in picojoules."""
    return Energy(to_exact(value) * PICOJOULE.scale, PICOJOULE)


def Nanojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in nanojoules."""
    return Energy(to_exact(value) * NANOJOULE.scale, NANOJOULE)


def Microjoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in microjoules."""
    return Energy(to_exact(value) * MICROJOULE.scale, MICROJOULE)


def Millijoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in millijoules."""
    return Energy(to_exact(value) * MILLIJOULE.scale, MILLIJOULE)


def Joule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in joules."""
    return Energy(to_exact(value) * JOULE.scale, JOULE)


def Kilojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in kilojoules."""
    return Energy(to_exact(value) * KILOJOULE.scale, KILOJOULE)


def Megajoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in megajoules."""
    return Energy(to_exact(value) * MEGAJOULE.scale, MEGAJOULE)


# Electronvolt

ELECTRONVOLT = UnitDef("electronvolt", "eV", Decimal("1.602176634e-19"), ENERGY)


def Electronvolt(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in electronvolts."""
    return Energy(to_exact(value) * ELECTRONVOLT.scale, ELECTRONVOLT)


# Watt times Time.

MILLIWATT_HOUR = UnitDef("milliwatt_hour", "mWh", Decimal("3.6"), ENERGY)
WATT_HOUR = UnitDef("watt_hour", "Wh", Decimal(3600), ENERGY)


def MilliwattHour(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in milliwatt-hours."""
    return Energy(to_exact(value) * MILLIWATT_HOUR.scale, MILLIWATT_HOUR)


def WattHour(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in watt-hours."""
    return Energy(to_exact(value) * WATT_HOUR.scale, WATT_HOUR)


ENERGY_UNITS: Mapping[str, Callable[[Numeric], Energy]] = MappingProxyType(
    {
        PICOJOULE.symbol: Picojoule,
        NANOJOULE.symbol: Nanojoule,
        MICROJOULE.symbol: Microjoule,
        MILLIJOULE.symbol: Millijoule,
        JOULE.symbol: Joule,
        KILOJOULE.symbol: Kilojoule,
        MEGAJOULE.symbol: Megajoule,
        ELECTRONVOLT.symbol: Electronvolt,
        MILLIWATT_HOUR.symbol: MilliwattHour,
        WATT_HOUR.symbol: WattHour,
    }
)

__all__ = [
    "ELECTRONVOLT",
    "ENERGY_UNITS",
    "JOULE",
    "KILOJOULE",
    "MEGAJOULE",
    "MICROJOULE",
    "MILLIJOULE",
    "MILLIWATT_HOUR",
    "NANOJOULE",
    "PICOJOULE",
    "WATT_HOUR",
    "Electronvolt",
    "Joule",
    "Kilojoule",
    "Megajoule",
    "Microjoule",
    "Millijoule",
    "MilliwattHour",
    "Nanojoule",
    "Picojoule",
    "WattHour",
]
