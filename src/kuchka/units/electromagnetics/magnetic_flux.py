"""Magnetic flux constructors: the weber, from nanowebers to kilowebers.

The weber is the SI unit of magnetic flux: `1 Wb = 1 V·s`.

`MAGNETIC_FLUX_UNITS` maps each symbol to its constructor, for boundary code that reads
a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MAGNETIC_FLUX
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import MagneticFlux

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

    from kuchka.quantities import UnitDef
WEBER_NAME = "weber"
WEBER_SYMBOL = "Wb"

NANOWEBER = prefixed_unit(prefixes.NANO, WEBER_NAME, WEBER_SYMBOL, MAGNETIC_FLUX)
MICROWEBER = prefixed_unit(prefixes.MICRO, WEBER_NAME, WEBER_SYMBOL, MAGNETIC_FLUX)
MILLIWEBER = prefixed_unit(prefixes.MILLI, WEBER_NAME, WEBER_SYMBOL, MAGNETIC_FLUX)
WEBER = prefixed_unit(
    prefixes.UNIT,
    WEBER_NAME,
    WEBER_SYMBOL,
    MAGNETIC_FLUX,
    aliases=("V·s", "V*s"),
    words=("volt second", "volt-second"),
)
KILOWEBER = prefixed_unit(prefixes.KILO, WEBER_NAME, WEBER_SYMBOL, MAGNETIC_FLUX)

MagneticFlux._canonical_unit = WEBER  # noqa: SLF001 -- this module owns MagneticFlux's canonical unit


def Nanoweber(value: Numeric) -> MagneticFlux:
    """Construct a MagneticFlux from a magnitude expressed in nanowebers."""
    return MagneticFlux(to_exact(value) * NANOWEBER.scale, NANOWEBER)


def Microweber(value: Numeric) -> MagneticFlux:
    """Construct a MagneticFlux from a magnitude expressed in microwebers."""
    return MagneticFlux(to_exact(value) * MICROWEBER.scale, MICROWEBER)


def Milliweber(value: Numeric) -> MagneticFlux:
    """Construct a MagneticFlux from a magnitude expressed in milliwebers."""
    return MagneticFlux(to_exact(value) * MILLIWEBER.scale, MILLIWEBER)


def Weber(value: Numeric) -> MagneticFlux:
    """Construct a MagneticFlux from a magnitude expressed in webers."""
    return MagneticFlux(to_exact(value) * WEBER.scale, WEBER)


def Kiloweber(value: Numeric) -> MagneticFlux:
    """Construct a MagneticFlux from a magnitude expressed in kilowebers."""
    return MagneticFlux(to_exact(value) * KILOWEBER.scale, KILOWEBER)


MAGNETIC_FLUX_UNITS: Mapping[str, Callable[[Numeric], MagneticFlux]] = unit_table(
    "MAGNETIC_FLUX_UNITS",
    {
        NANOWEBER: Nanoweber,
        MICROWEBER: Microweber,
        MILLIWEBER: Milliweber,
        WEBER: Weber,
        KILOWEBER: Kiloweber,
    },
)

MAGNETIC_FLUX_LADDERS: tuple[tuple[UnitDef, ...], ...] = (
    (
        NANOWEBER,
        MICROWEBER,
        MILLIWEBER,
        WEBER,
        KILOWEBER,
    ),
)
"""The units `auto_scale` moves a magnetic flux along, smallest first."""

__all__ = [
    "KILOWEBER",
    "MAGNETIC_FLUX_LADDERS",
    "MAGNETIC_FLUX_UNITS",
    "MICROWEBER",
    "MILLIWEBER",
    "NANOWEBER",
    "WEBER",
    "Kiloweber",
    "Microweber",
    "Milliweber",
    "Nanoweber",
    "Weber",
]
