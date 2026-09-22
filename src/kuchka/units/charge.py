"""Charge unit constructors: Microcoulomb, Millicoulomb, Coulomb.

Each function here does the same thing: take a plain number, multiply it by a fixed
scale factor, and wrap it in :class:`~kuchka.quantities.Charge`.

    from kuchka import Coulomb, Milliampere, Second

    dose = Milliampere(2) * Second(5)  # -> Charge, computed and typed automatically.

`CHARGE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import CHARGE
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.prefixes import MICRO
from kuchka.prefixes import MILLI
from kuchka.prefixes import NANO
from kuchka.prefixes import PICO
from kuchka.prefixes import UNIT
from kuchka.prefixes import prefixed_unit
from kuchka.quantities import Charge
from kuchka.quantities import UnitDef

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
    return Charge(to_exact(value) * PICOCOULOMB.scale, PICOCOULOMB)


def Nanocoulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in nanocoulomb."""
    return Charge(to_exact(value) * NANOCOULOMB.scale, NANOCOULOMB)


def Microcoulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in microcoulombs."""
    return Charge(to_exact(value) * MICROCOULOMB.scale, MICROCOULOMB)


def Millicoulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in millicoulombs."""
    return Charge(to_exact(value) * MILLICOULOMB.scale, MILLICOULOMB)


def Coulomb(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in coulombs."""
    return Charge(to_exact(value) * COULOMB.scale, COULOMB)


# Ampere times Time.

MILLIAMPERE_SECOND = UnitDef("milliampere_second", "mAs", Decimal("0.001"), CHARGE)
MILLIAMPERE_HOUR = UnitDef("milliampere_hour", "mAh", Decimal("3.6"), CHARGE)
AMPERE_HOUR = UnitDef("ampere_hour", "Ah", Decimal(3600), CHARGE)
AmpereSecond = Coulomb
"""An ampere-second by definition is a coulomb."""


def MilliampereSecond(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in milliampere-seconds."""
    return Charge(to_exact(value) * MILLIAMPERE_SECOND.scale, MILLIAMPERE_SECOND)


def MilliampereHour(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in milliampere-hours."""
    return Charge(to_exact(value) * MILLIAMPERE_HOUR.scale, MILLIAMPERE_HOUR)


def AmpereHour(value: Numeric) -> Charge:
    """Construct a Charge from a magnitude expressed in ampere-hours."""
    return Charge(to_exact(value) * AMPERE_HOUR.scale, AMPERE_HOUR)


CHARGE_UNITS: Mapping[str, Callable[[Numeric], Charge]] = MappingProxyType(
    {
        PICOCOULOMB.symbol: Picocoulomb,
        NANOCOULOMB.symbol: Nanocoulomb,
        MICROCOULOMB.symbol: Microcoulomb,
        MILLICOULOMB.symbol: Millicoulomb,
        COULOMB.symbol: Coulomb,
        "As": AmpereSecond,
        MILLIAMPERE_SECOND.symbol: MilliampereSecond,
        MILLIAMPERE_HOUR.symbol: MilliampereHour,
        AMPERE_HOUR.symbol: AmpereHour,
    }
)

__all__ = [
    "AMPERE_HOUR",
    "CHARGE_UNITS",
    "COULOMB",
    "MICROCOULOMB",
    "MILLIAMPERE_HOUR",
    "MILLIAMPERE_SECOND",
    "MILLICOULOMB",
    "NANOCOULOMB",
    "PICOCOULOMB",
    "AmpereHour",
    "AmpereSecond",
    "Coulomb",
    "Microcoulomb",
    "MilliampereHour",
    "MilliampereSecond",
    "Millicoulomb",
    "Nanocoulomb",
    "Picocoulomb",
]
