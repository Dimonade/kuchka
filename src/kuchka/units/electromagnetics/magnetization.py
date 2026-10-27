"""Magnetization unit constructors: MilliamperePerMetre, AmperePerMetre, ...

Magnetization is current per unit length: `1 A/m = 1 A / 1 m`.

`MAGNETIZATION_UNITS` maps each symbol to its constructor, for boundary code
that reads a unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import MAGNETIZATION
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Magnetization

if TYPE_CHECKING:
    from kuchka.internal.unit_table import UnitTable

AMPERE_PER_METRE_NAME = "ampere_per_metre"
AMPERE_PER_METRE_SYMBOL = "A/m"
AMPERE_PER_METRE_WORDS = ("ampere per metre", "ampere per meter")
"""Spoken forms, which prefixed names follow: `milliampere per metre`."""

MICROAMPERE_PER_METRE = prefixed_unit(
    prefixes.MICRO,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIZATION,
    base_words=AMPERE_PER_METRE_WORDS,
)
MILLIAMPERE_PER_METRE = prefixed_unit(
    prefixes.MILLI,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIZATION,
    base_words=AMPERE_PER_METRE_WORDS,
)
AMPERE_PER_METRE = prefixed_unit(
    prefixes.UNIT,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIZATION,
    base_words=AMPERE_PER_METRE_WORDS,
)
KILOAMPERE_PER_METRE = prefixed_unit(
    prefixes.KILO,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIZATION,
    base_words=AMPERE_PER_METRE_WORDS,
)
MEGAAMPERE_PER_METRE = prefixed_unit(
    prefixes.MEGA,
    AMPERE_PER_METRE_NAME,
    AMPERE_PER_METRE_SYMBOL,
    MAGNETIZATION,
    base_words=AMPERE_PER_METRE_WORDS,
)

Magnetization._canonical_unit = AMPERE_PER_METRE  # noqa: SLF001 -- this module owns Magnetization's canonical unit


def MicroamperePerMetre(value: Numeric) -> Magnetization:
    """Construct magnetization from a magnitude in microamperes per metre."""
    return Magnetization(
        to_exact(value) * MICROAMPERE_PER_METRE.scale, MICROAMPERE_PER_METRE
    )


def MilliamperePerMetre(value: Numeric) -> Magnetization:
    """Construct magnetization from a magnitude in milliamperes per metre."""
    return Magnetization(
        to_exact(value) * MILLIAMPERE_PER_METRE.scale, MILLIAMPERE_PER_METRE
    )


def AmperePerMetre(value: Numeric) -> Magnetization:
    """Construct magnetization from a magnitude in amperes per metre."""
    return Magnetization(to_exact(value) * AMPERE_PER_METRE.scale, AMPERE_PER_METRE)


def KiloamperePerMetre(value: Numeric) -> Magnetization:
    """Construct magnetization from a magnitude in kiloamperes per metre."""
    return Magnetization(
        to_exact(value) * KILOAMPERE_PER_METRE.scale, KILOAMPERE_PER_METRE
    )


def MegaamperePerMetre(value: Numeric) -> Magnetization:
    """Construct magnetization from a magnitude in megaamperes per metre."""
    return Magnetization(
        to_exact(value) * MEGAAMPERE_PER_METRE.scale, MEGAAMPERE_PER_METRE
    )


MAGNETIZATION_UNITS: UnitTable[Magnetization] = unit_table(
    "MAGNETIZATION_UNITS",
    {
        MICROAMPERE_PER_METRE: MicroamperePerMetre,
        MILLIAMPERE_PER_METRE: MilliamperePerMetre,
        AMPERE_PER_METRE: AmperePerMetre,
        KILOAMPERE_PER_METRE: KiloamperePerMetre,
        MEGAAMPERE_PER_METRE: MegaamperePerMetre,
    },
)

__all__ = [
    "AMPERE_PER_METRE",
    "KILOAMPERE_PER_METRE",
    "MAGNETIZATION_UNITS",
    "MEGAAMPERE_PER_METRE",
    "MICROAMPERE_PER_METRE",
    "MILLIAMPERE_PER_METRE",
    "AmperePerMetre",
    "KiloamperePerMetre",
    "MegaamperePerMetre",
    "MicroamperePerMetre",
    "MilliamperePerMetre",
]
