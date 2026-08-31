"""Energy unit constructors: Picojoule through Megajoule.

    from kuchka import Joule, Millijoule

    pulse_energy = Millijoule(2)

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

JOULE = UnitDef("joule", "J", Decimal(1), ENERGY)

Energy._canonical_unit = JOULE  # noqa: SLF001 -- this module owns Energy's canonical unit


def Joule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in joules."""
    return Energy(to_decimal(value) * JOULE.scale, JOULE)


PICOJOULE = UnitDef("picojoule", "pJ", Decimal(10) ** -12, ENERGY)
NANOJOULE = UnitDef("nanojoule", "nJ", Decimal(10) ** -9, ENERGY)
MICROJOULE = UnitDef("microjoule", "µJ", Decimal(10) ** -6, ENERGY)
MILLIJOULE = UnitDef("millijoule", "mJ", Decimal(10) ** -3, ENERGY)
KILOJOULE = UnitDef("kilojoule", "kJ", Decimal(10) ** 3, ENERGY)
MEGAJOULE = UnitDef("megajoule", "MJ", Decimal(10) ** 6, ENERGY)


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


def Kilojoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in kilojoules."""
    return Energy(to_decimal(value) * KILOJOULE.scale, KILOJOULE)


def Megajoule(value: Numeric) -> Energy:
    """Construct an Energy from a magnitude expressed in megajoules."""
    return Energy(to_decimal(value) * MEGAJOULE.scale, MEGAJOULE)


GENERATED_ENERGY_UNITS: Mapping[str, Callable[[Numeric], Energy]] = MappingProxyType(
    {
        "pJ": Picojoule,
        "nJ": Nanojoule,
        "µJ": Microjoule,
        "mJ": Millijoule,
        "kJ": Kilojoule,
        "MJ": Megajoule,
    }
)

ENERGY_UNITS: Mapping[str, Callable[[Numeric], Energy]] = MappingProxyType(
    {
        "J": Joule,
        **GENERATED_ENERGY_UNITS,
    }
)
