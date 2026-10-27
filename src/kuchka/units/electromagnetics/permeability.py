"""Permeability unit constructors: NanohenryPerMetre, ..., HenryPerMetre.

Permeability is inductance per unit length: `1 H/m = 1 H / 1 m`.

`PERMEABILITY_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import PERMEABILITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Permeability

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

HENRY_PER_METRE_NAME = "henry_per_metre"
HENRY_PER_METRE_SYMBOL = "H/m"
HENRY_PER_METRE_WORDS = ("henry per metre", "henry per meter")
"""Spoken forms, which prefixed names follow: `nanohenry per metre`."""

NANOHENRY_PER_METRE = prefixed_unit(
    prefixes.NANO,
    HENRY_PER_METRE_NAME,
    HENRY_PER_METRE_SYMBOL,
    PERMEABILITY,
    base_words=HENRY_PER_METRE_WORDS,
)
MICROHENRY_PER_METRE = prefixed_unit(
    prefixes.MICRO,
    HENRY_PER_METRE_NAME,
    HENRY_PER_METRE_SYMBOL,
    PERMEABILITY,
    base_words=HENRY_PER_METRE_WORDS,
)
MILLIHENRY_PER_METRE = prefixed_unit(
    prefixes.MILLI,
    HENRY_PER_METRE_NAME,
    HENRY_PER_METRE_SYMBOL,
    PERMEABILITY,
    base_words=HENRY_PER_METRE_WORDS,
)
HENRY_PER_METRE = prefixed_unit(
    prefixes.UNIT,
    HENRY_PER_METRE_NAME,
    HENRY_PER_METRE_SYMBOL,
    PERMEABILITY,
    base_words=HENRY_PER_METRE_WORDS,
)

Permeability._canonical_unit = HENRY_PER_METRE  # noqa: SLF001 -- this module owns Permeability's canonical unit


def NanohenryPerMetre(value: Numeric) -> Permeability:
    """Construct a Permeability from a magnitude expressed in nanohenrys per metre."""
    return Permeability(
        to_exact(value) * NANOHENRY_PER_METRE.scale, NANOHENRY_PER_METRE
    )


def MicrohenryPerMetre(value: Numeric) -> Permeability:
    """Construct a Permeability from a magnitude expressed in microhenrys per metre."""
    return Permeability(
        to_exact(value) * MICROHENRY_PER_METRE.scale, MICROHENRY_PER_METRE
    )


def MillihenryPerMetre(value: Numeric) -> Permeability:
    """Construct a Permeability from a magnitude expressed in millihenrys per metre."""
    return Permeability(
        to_exact(value) * MILLIHENRY_PER_METRE.scale, MILLIHENRY_PER_METRE
    )


def HenryPerMetre(value: Numeric) -> Permeability:
    """Construct a Permeability from a magnitude expressed in henrys per metre."""
    return Permeability(to_exact(value) * HENRY_PER_METRE.scale, HENRY_PER_METRE)


PERMEABILITY_UNITS: Mapping[str, Callable[[Numeric], Permeability]] = unit_table(
    "PERMEABILITY_UNITS",
    {
        NANOHENRY_PER_METRE: NanohenryPerMetre,
        MICROHENRY_PER_METRE: MicrohenryPerMetre,
        MILLIHENRY_PER_METRE: MillihenryPerMetre,
        HENRY_PER_METRE: HenryPerMetre,
    },
)

__all__ = [
    "HENRY_PER_METRE",
    "MICROHENRY_PER_METRE",
    "MILLIHENRY_PER_METRE",
    "NANOHENRY_PER_METRE",
    "PERMEABILITY_UNITS",
    "HenryPerMetre",
    "MicrohenryPerMetre",
    "MillihenryPerMetre",
    "NanohenryPerMetre",
]
