"""Charge unit constructors: Microcoulomb, Millicoulomb, Coulomb.

Each function here does the same thing: take a plain number, multiply it by a fixed
scale factor, and wrap it in :class:`~kuchka.quantities.Charge`.

    from kuchka import Coulomb, Milliampere, Second

    dose = Milliampere(2) * Second(5)  # -> Charge, computed and typed automatically.

`CHARGE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import CHARGE
from kuchka.numeric import Numeric
from kuchka.numeric import to_decimal
from kuchka.prefixes import MICRO
from kuchka.prefixes import MILLI
from kuchka.prefixes import NANO
from kuchka.prefixes import PICO
from kuchka.prefixes import UNIT
from kuchka.prefixes import prefixed_unit
from kuchka.quantities import Charge

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

COULOMB_NAME = "coulomb"
COULOMB_SYMBOL = "C"

PICOCOULOMB = prefixed_unit(PICO, COULOMB_NAME, COULOMB_SYMBOL, CHARGE)
NANOCOULOMB = prefixed_unit(NANO, COULOMB_NAME, COULOMB_SYMBOL, CHARGE)
MICROCOULOMB = prefixed_unit(MICRO, COULOMB_NAME, COULOMB_SYMBOL, CHARGE)
MILLICOULOMB = prefixed_unit(MILLI, COULOMB_NAME, COULOMB_SYMBOL, CHARGE)
COULOMB = prefixed_unit(UNIT, COULOMB_NAME, COULOMB_SYMBOL, CHARGE)

Charge._canonical_unit = COULOMB  # noqa: SLF001 -- this module owns Charge's canonical unit


def Picocoulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in picocoulomb."""
    return Charge(to_decimal(value) * PICOCOULOMB.scale, PICOCOULOMB)


def Nanocoulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in nanocoulomb."""
    return Charge(to_decimal(value) * NANOCOULOMB.scale, NANOCOULOMB)


def Microcoulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in microcoulombs."""
    return Charge(to_decimal(value) * MICROCOULOMB.scale, MICROCOULOMB)


def Millicoulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in millicoulombs."""
    return Charge(to_decimal(value) * MILLICOULOMB.scale, MILLICOULOMB)


def Coulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in coulombs."""
    return Charge(to_decimal(value) * COULOMB.scale, COULOMB)


CHARGE_UNITS: Mapping[str, Callable[[Numeric], Charge]] = MappingProxyType(
    {
        PICOCOULOMB.symbol: Picocoulomb,
        NANOCOULOMB.symbol: Nanocoulomb,
        MICROCOULOMB.symbol: Microcoulomb,
        MILLICOULOMB.symbol: Millicoulomb,
        COULOMB.symbol: Coulomb,
    }
)

__all__ = [
    "CHARGE_UNITS",
    "COULOMB",
    "MICROCOULOMB",
    "MILLICOULOMB",
    "NANOCOULOMB",
    "PICOCOULOMB",
    "Coulomb",
    "Microcoulomb",
    "Millicoulomb",
    "Nanocoulomb",
    "Picocoulomb",
]
