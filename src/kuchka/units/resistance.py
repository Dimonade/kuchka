"""Resistance unit constructors: Milliohm, Ohm, Kiloohm, Megaohm.

Each function here does the same thing: take a plain number, multiply it
by a fixed scale factor, and wrap it in :class:`~kuchka.quantities.Resistance`.

    from kuchka import Ohm

    resistance = Ohm(100)

`RESISTANCE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import RESISTANCE
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Resistance

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


OHM_NAME = "Ohm"
OHM_SYMBOL = symbols.OMEGA


MILLIOHM = prefixed_unit(prefixes.MILLI, OHM_NAME, OHM_SYMBOL, RESISTANCE)
OHM = prefixed_unit(prefixes.UNIT, OHM_NAME, OHM_SYMBOL, RESISTANCE)
KILOOHM = prefixed_unit(prefixes.KILO, OHM_NAME, OHM_SYMBOL, RESISTANCE)
MEGAOHM = prefixed_unit(prefixes.MEGA, OHM_NAME, OHM_SYMBOL, RESISTANCE)


Resistance._canonical_unit = OHM  # noqa: SLF001 -- this module owns Resistance's canonical unit


def Milliohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in milliohms."""
    return Resistance(to_exact(value) * MILLIOHM.scale, MILLIOHM)


def Ohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in ohms."""
    return Resistance(to_exact(value) * OHM.scale, OHM)


def Kiloohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in kiloohms."""
    return Resistance(to_exact(value) * KILOOHM.scale, KILOOHM)


def Megaohm(value: Numeric) -> Resistance:
    """Construct a Resistance from a magnitude expressed in megaohms."""
    return Resistance(to_exact(value) * MEGAOHM.scale, MEGAOHM)


RESISTANCE_UNITS: Mapping[str, Callable[[Numeric], Resistance]] = MappingProxyType(
    {
        MILLIOHM.symbol: Milliohm,
        OHM.symbol: Ohm,
        KILOOHM.symbol: Kiloohm,
        MEGAOHM.symbol: Megaohm,
    }
)

__all__ = [
    "KILOOHM",
    "MEGAOHM",
    "MILLIOHM",
    "OHM",
    "RESISTANCE_UNITS",
    "Kiloohm",
    "Megaohm",
    "Milliohm",
    "Ohm",
]
