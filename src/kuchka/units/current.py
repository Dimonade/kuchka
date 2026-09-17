"""Current unit constructors: Microampere, Milliampere, Ampere, Kiloampere.

Each function here does the same thing: take a plain number, multiply it
by a fixed scale factor, and wrap it in :class:`~kuchka.quantities.Current`.

    from kuchka import Ampere, Milliampere

    current = Ampere(1) - Milliampere(250)

`CURRENT_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import CURRENT
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.prefixes import KILO
from kuchka.prefixes import MICRO
from kuchka.prefixes import MILLI
from kuchka.prefixes import UNIT
from kuchka.prefixes import prefixed_unit
from kuchka.quantities import Current

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


AMPERE_NAME = "ampere"
AMPERE_SYMBOL = "A"

MICROAMPERE = prefixed_unit(MICRO, AMPERE_NAME, AMPERE_SYMBOL, CURRENT)
MILLIAMPERE = prefixed_unit(MILLI, AMPERE_NAME, AMPERE_SYMBOL, CURRENT)
AMPERE = prefixed_unit(UNIT, AMPERE_NAME, AMPERE_SYMBOL, CURRENT)
KILOAMPERE = prefixed_unit(KILO, AMPERE_NAME, AMPERE_SYMBOL, CURRENT)

Current._canonical_unit = AMPERE  # noqa: SLF001 -- this module owns Current's canonical unit


def Microampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in microamperes."""
    return Current(to_exact(value) * MICROAMPERE.scale, MICROAMPERE)


def Milliampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in milliamperes."""
    return Current(to_exact(value) * MILLIAMPERE.scale, MILLIAMPERE)


def Ampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in amperes."""
    return Current(to_exact(value) * AMPERE.scale, AMPERE)


def Kiloampere(value: Numeric) -> Current:
    """Construct a Current from a magnitude expressed in kiloamperes."""
    return Current(to_exact(value) * KILOAMPERE.scale, KILOAMPERE)


CURRENT_UNITS: Mapping[str, Callable[[Numeric], Current]] = MappingProxyType(
    {
        MICROAMPERE.symbol: Microampere,
        MILLIAMPERE.symbol: Milliampere,
        AMPERE.symbol: Ampere,
        KILOAMPERE.symbol: Kiloampere,
    }
)

__all__ = [
    "AMPERE",
    "CURRENT_UNITS",
    "KILOAMPERE",
    "MICROAMPERE",
    "MILLIAMPERE",
    "Ampere",
    "Kiloampere",
    "Microampere",
    "Milliampere",
]
