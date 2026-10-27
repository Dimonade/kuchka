"""Inductance unit constructors: Nanohenry, Microhenry, Millihenry, Henry, ...

The henry is the SI unit of inductance: `1 H = 1 Wb/A`.

`INDUCTANCE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import INDUCTANCE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Inductance

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

HENRY_NAME = "henry"
HENRY_SYMBOL = "H"
HENRY_WORDS = ("henries",)
"""The plural, which prefixed names follow: `millihenries`."""

PICOHENRY = prefixed_unit(
    prefixes.PICO, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)
NANOHENRY = prefixed_unit(
    prefixes.NANO, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)
MICROHENRY = prefixed_unit(
    prefixes.MICRO, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)
MILLIHENRY = prefixed_unit(
    prefixes.MILLI, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)
HENRY = prefixed_unit(
    prefixes.UNIT, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)
KILOHENRY = prefixed_unit(
    prefixes.KILO, HENRY_NAME, HENRY_SYMBOL, INDUCTANCE, base_words=HENRY_WORDS
)

Inductance._canonical_unit = HENRY  # noqa: SLF001 -- this module owns Inductance's canonical unit


def Picohenry(value: Numeric) -> Inductance:
    """Construct a Inductance from a magnitude expressed in picohenrys."""
    return Inductance(to_exact(value) * PICOHENRY.scale, PICOHENRY)


def Nanohenry(value: Numeric) -> Inductance:
    """Construct a Inductance from a magnitude expressed in nanohenrys."""
    return Inductance(to_exact(value) * NANOHENRY.scale, NANOHENRY)


def Microhenry(value: Numeric) -> Inductance:
    """Construct a Inductance from a magnitude expressed in microhenrys."""
    return Inductance(to_exact(value) * MICROHENRY.scale, MICROHENRY)


def Millihenry(value: Numeric) -> Inductance:
    """Construct a Inductance from a magnitude expressed in millihenrys."""
    return Inductance(to_exact(value) * MILLIHENRY.scale, MILLIHENRY)


def Henry(value: Numeric) -> Inductance:
    """Construct a Inductance from a magnitude expressed in henrys."""
    return Inductance(to_exact(value) * HENRY.scale, HENRY)


def Kilohenry(value: Numeric) -> Inductance:
    """Construct a Inductance from a magnitude expressed in kilohenrys."""
    return Inductance(to_exact(value) * KILOHENRY.scale, KILOHENRY)


INDUCTANCE_UNITS: Mapping[str, Callable[[Numeric], Inductance]] = unit_table(
    "INDUCTANCE_UNITS",
    {
        PICOHENRY: Picohenry,
        NANOHENRY: Nanohenry,
        MICROHENRY: Microhenry,
        MILLIHENRY: Millihenry,
        HENRY: Henry,
        KILOHENRY: Kilohenry,
    },
)

__all__ = [
    "HENRY",
    "INDUCTANCE_UNITS",
    "KILOHENRY",
    "MICROHENRY",
    "MILLIHENRY",
    "NANOHENRY",
    "PICOHENRY",
    "Henry",
    "Kilohenry",
    "Microhenry",
    "Millihenry",
    "Nanohenry",
    "Picohenry",
]
