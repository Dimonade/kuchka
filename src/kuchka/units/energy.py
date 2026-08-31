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
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.quantities import Energy
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

PICOJOULE = UnitDef("picojoule", "pJ", Decimal("0.000000000001"), ENERGY)
NANOJOULE = UnitDef("nanojoule", "nJ", Decimal("0.000000001"), ENERGY)
MICROJOULE = UnitDef("microjoule", "\u00b5J", Decimal("0.000001"), ENERGY)
MILLIJOULE = UnitDef("millijoule", "mJ", Decimal("0.001"), ENERGY)
JOULE = UnitDef("joule", "J", Decimal(1), ENERGY)
KILOJOULE = UnitDef("kilojoule", "kJ", Decimal(1000), ENERGY)
MEGAJOULE = UnitDef("megajoule", "MJ", Decimal(1_000_000), ENERGY)

Energy._canonical_unit = JOULE  # noqa: SLF001 -- this module owns Energy's canonical unit


def Picojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in picojoules."""
    return Energy(to_decimal(value) * PICOJOULE.scale, PICOJOULE)


def Nanojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in nanojoules."""
    return Energy(to_decimal(value) * NANOJOULE.scale, NANOJOULE)


def Microjoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in microjoules."""
    return Energy(to_decimal(value) * MICROJOULE.scale, MICROJOULE)


def Millijoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in millijoules."""
    return Energy(to_decimal(value) * MILLIJOULE.scale, MILLIJOULE)


def Joule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in joules."""
    return Energy(to_decimal(value) * JOULE.scale, JOULE)


def Kilojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in kilojoules."""
    return Energy(to_decimal(value) * KILOJOULE.scale, KILOJOULE)


def Megajoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in megajoules."""
    return Energy(to_decimal(value) * MEGAJOULE.scale, MEGAJOULE)


ENERGY_UNITS: Mapping[str, Callable[[Numeric], Energy]] = MappingProxyType(
    {
        "pJ": Picojoule,
        "nJ": Nanojoule,
        "uJ": Microjoule,
        "mJ": Millijoule,
        "J": Joule,
        "kJ": Kilojoule,
        "MJ": Megajoule,
    }
)
