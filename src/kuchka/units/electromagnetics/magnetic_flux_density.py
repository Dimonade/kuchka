"""Magnetic flux density unit constructors: Microtesla, Millitesla, Tesla, ...

The tesla is the SI unit of magnetic flux density: `1 T = 1 Wb/m²`.

`MAGNETIC_FLUX_DENSITY_UNITS` maps each symbol to its constructor, for boundary code
that reads a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MAGNETIC_FLUX_DENSITY
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import MagneticFluxDensity

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

TESLA_NAME = "tesla"
TESLA_SYMBOL = "T"

FEMTOTESLA = prefixed_unit(
    prefixes.FEMTO, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)
PICOTESLA = prefixed_unit(
    prefixes.PICO, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)
NANOTESLA = prefixed_unit(
    prefixes.NANO, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)
MICROTESLA = prefixed_unit(
    prefixes.MICRO, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)
MILLITESLA = prefixed_unit(
    prefixes.MILLI, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)
TESLA = prefixed_unit(
    prefixes.UNIT,
    TESLA_NAME,
    TESLA_SYMBOL,
    MAGNETIC_FLUX_DENSITY,
    aliases=(f"Wb/m{symbols.SUPERSCRIPT_TWO}", *powered("Wb/m", 2)),
    words=("weber per square metre", "weber per square meter"),
)
KILOTESLA = prefixed_unit(
    prefixes.KILO, TESLA_NAME, TESLA_SYMBOL, MAGNETIC_FLUX_DENSITY
)

MagneticFluxDensity._canonical_unit = TESLA  # noqa: SLF001 -- this module owns MagneticFluxDensity's canonical unit


def Femtotesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a MagneticFluxDensity from a magnitude expressed in femtoteslas."""
    return MagneticFluxDensity(to_exact(value) * FEMTOTESLA.scale, FEMTOTESLA)


def Picotesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a MagneticFluxDensity from a magnitude expressed in picoteslas."""
    return MagneticFluxDensity(to_exact(value) * PICOTESLA.scale, PICOTESLA)


def Nanotesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a MagneticFluxDensity from a magnitude expressed in nanoteslas."""
    return MagneticFluxDensity(to_exact(value) * NANOTESLA.scale, NANOTESLA)


def Microtesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a MagneticFluxDensity from a magnitude expressed in microteslas."""
    return MagneticFluxDensity(to_exact(value) * MICROTESLA.scale, MICROTESLA)


def Millitesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a MagneticFluxDensity from a magnitude expressed in milliteslas."""
    return MagneticFluxDensity(to_exact(value) * MILLITESLA.scale, MILLITESLA)


def Tesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a MagneticFluxDensity from a magnitude expressed in teslas."""
    return MagneticFluxDensity(to_exact(value) * TESLA.scale, TESLA)


def Kilotesla(value: Numeric) -> MagneticFluxDensity:
    """Construct a MagneticFluxDensity from a magnitude expressed in kiloteslas."""
    return MagneticFluxDensity(to_exact(value) * KILOTESLA.scale, KILOTESLA)


MAGNETIC_FLUX_DENSITY_UNITS: Mapping[str, Callable[[Numeric], MagneticFluxDensity]] = (
    unit_table(
        "MAGNETIC_FLUX_DENSITY_UNITS",
        {
            FEMTOTESLA: Femtotesla,
            PICOTESLA: Picotesla,
            NANOTESLA: Nanotesla,
            MICROTESLA: Microtesla,
            MILLITESLA: Millitesla,
            TESLA: Tesla,
            KILOTESLA: Kilotesla,
        },
    )
)

__all__ = [
    "FEMTOTESLA",
    "KILOTESLA",
    "MAGNETIC_FLUX_DENSITY_UNITS",
    "MICROTESLA",
    "MILLITESLA",
    "NANOTESLA",
    "PICOTESLA",
    "TESLA",
    "Femtotesla",
    "Kilotesla",
    "Microtesla",
    "Millitesla",
    "Nanotesla",
    "Picotesla",
    "Tesla",
]
