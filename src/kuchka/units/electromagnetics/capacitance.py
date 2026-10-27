"""Capacitance unit constructors: Picofarad, Nanofarad, Microfarad, ...

The farad is the SI unit of capacitance: `1 F = 1 C/V`.

`CAPACITANCE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kuchka.dimensions import CAPACITANCE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Capacitance

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

FARAD_NAME = "farad"
FARAD_SYMBOL = "F"

FEMTOFARAD = prefixed_unit(prefixes.FEMTO, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
PICOFARAD = prefixed_unit(prefixes.PICO, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
NANOFARAD = prefixed_unit(prefixes.NANO, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
MICROFARAD = prefixed_unit(prefixes.MICRO, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
MILLIFARAD = prefixed_unit(prefixes.MILLI, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
FARAD = prefixed_unit(prefixes.UNIT, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)
KILOFARAD = prefixed_unit(prefixes.KILO, FARAD_NAME, FARAD_SYMBOL, CAPACITANCE)

Capacitance._canonical_unit = FARAD  # noqa: SLF001 -- this module owns Capacitance's canonical unit


def Femtofarad(value: Numeric) -> Capacitance:
    """Construct a Capacitance from a magnitude expressed in femtofarads."""
    return Capacitance(to_exact(value) * FEMTOFARAD.scale, FEMTOFARAD)


def Picofarad(value: Numeric) -> Capacitance:
    """Construct a Capacitance from a magnitude expressed in picofarads."""
    return Capacitance(to_exact(value) * PICOFARAD.scale, PICOFARAD)


def Nanofarad(value: Numeric) -> Capacitance:
    """Construct a Capacitance from a magnitude expressed in nanofarads."""
    return Capacitance(to_exact(value) * NANOFARAD.scale, NANOFARAD)


def Microfarad(value: Numeric) -> Capacitance:
    """Construct a Capacitance from a magnitude expressed in microfarads."""
    return Capacitance(to_exact(value) * MICROFARAD.scale, MICROFARAD)


def Millifarad(value: Numeric) -> Capacitance:
    """Construct a Capacitance from a magnitude expressed in millifarads."""
    return Capacitance(to_exact(value) * MILLIFARAD.scale, MILLIFARAD)


def Farad(value: Numeric) -> Capacitance:
    """Construct a Capacitance from a magnitude expressed in farads."""
    return Capacitance(to_exact(value) * FARAD.scale, FARAD)


def Kilofarad(value: Numeric) -> Capacitance:
    """Construct a Capacitance from a magnitude expressed in kilofarads."""
    return Capacitance(to_exact(value) * KILOFARAD.scale, KILOFARAD)


CAPACITANCE_UNITS: Mapping[str, Callable[[Numeric], Capacitance]] = unit_table(
    "CAPACITANCE_UNITS",
    {
        FEMTOFARAD: Femtofarad,
        PICOFARAD: Picofarad,
        NANOFARAD: Nanofarad,
        MICROFARAD: Microfarad,
        MILLIFARAD: Millifarad,
        FARAD: Farad,
        KILOFARAD: Kilofarad,
    },
)

__all__ = [
    "CAPACITANCE_UNITS",
    "FARAD",
    "FEMTOFARAD",
    "KILOFARAD",
    "MICROFARAD",
    "MILLIFARAD",
    "NANOFARAD",
    "PICOFARAD",
    "Farad",
    "Femtofarad",
    "Kilofarad",
    "Microfarad",
    "Millifarad",
    "Nanofarad",
    "Picofarad",
]
