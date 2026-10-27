"""Permittivity unit constructors: PicofaradPerMetre, ..., FaradPerMetre.

Permittivity is capacitance per unit length: `1 F/m = 1 F / 1 m`.

`PERMITTIVITY_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import PERMITTIVITY
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Permittivity

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

FARAD_PER_METRE_NAME = "farad_per_metre"
FARAD_PER_METRE_SYMBOL = "F/m"
FARAD_PER_METRE_WORDS = ("farad per metre", "farad per meter")
"""Spoken forms, which prefixed names follow: `picofarad per metre`."""

PICOFARAD_PER_METRE = prefixed_unit(
    prefixes.PICO,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
NANOFARAD_PER_METRE = prefixed_unit(
    prefixes.NANO,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
MICROFARAD_PER_METRE = prefixed_unit(
    prefixes.MICRO,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
MILLIFARAD_PER_METRE = prefixed_unit(
    prefixes.MILLI,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)
FARAD_PER_METRE = prefixed_unit(
    prefixes.UNIT,
    FARAD_PER_METRE_NAME,
    FARAD_PER_METRE_SYMBOL,
    PERMITTIVITY,
    base_words=FARAD_PER_METRE_WORDS,
)

Permittivity._canonical_unit = FARAD_PER_METRE  # noqa: SLF001 -- this module owns Permittivity's canonical unit


def PicofaradPerMetre(value: Numeric) -> Permittivity:
    """Construct a Permittivity from a magnitude expressed in picofarads per metre."""
    return Permittivity(
        to_exact(value) * PICOFARAD_PER_METRE.scale, PICOFARAD_PER_METRE
    )


def NanofaradPerMetre(value: Numeric) -> Permittivity:
    """Construct a Permittivity from a magnitude expressed in nanofarads per metre."""
    return Permittivity(
        to_exact(value) * NANOFARAD_PER_METRE.scale, NANOFARAD_PER_METRE
    )


def MicrofaradPerMetre(value: Numeric) -> Permittivity:
    """Construct a Permittivity from a magnitude expressed in microfarads per metre."""
    return Permittivity(
        to_exact(value) * MICROFARAD_PER_METRE.scale, MICROFARAD_PER_METRE
    )


def MillifaradPerMetre(value: Numeric) -> Permittivity:
    """Construct a Permittivity from a magnitude expressed in millifarads per metre."""
    return Permittivity(
        to_exact(value) * MILLIFARAD_PER_METRE.scale, MILLIFARAD_PER_METRE
    )


def FaradPerMetre(value: Numeric) -> Permittivity:
    """Construct a Permittivity from a magnitude expressed in farads per metre."""
    return Permittivity(to_exact(value) * FARAD_PER_METRE.scale, FARAD_PER_METRE)


PERMITTIVITY_UNITS: Mapping[str, Callable[[Numeric], Permittivity]] = unit_table(
    "PERMITTIVITY_UNITS",
    {
        PICOFARAD_PER_METRE: PicofaradPerMetre,
        NANOFARAD_PER_METRE: NanofaradPerMetre,
        MICROFARAD_PER_METRE: MicrofaradPerMetre,
        MILLIFARAD_PER_METRE: MillifaradPerMetre,
        FARAD_PER_METRE: FaradPerMetre,
    },
)

__all__ = [
    "FARAD_PER_METRE",
    "MICROFARAD_PER_METRE",
    "MILLIFARAD_PER_METRE",
    "NANOFARAD_PER_METRE",
    "PERMITTIVITY_UNITS",
    "PICOFARAD_PER_METRE",
    "FaradPerMetre",
    "MicrofaradPerMetre",
    "MillifaradPerMetre",
    "NanofaradPerMetre",
    "PicofaradPerMetre",
]
