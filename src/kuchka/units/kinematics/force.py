"""Unit constructors for Force.

    from kuchka import Newton

    push = Newton(10)


`FORCE_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import FORCE
from kuchka.internal import prefixes
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Force
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


NEWTON_NAME = "newton"
NEWTON_SYMBOL = "N"

MILLINEWTON = prefixed_unit(prefixes.MILLI, NEWTON_NAME, NEWTON_SYMBOL, FORCE)
NEWTON = prefixed_unit(prefixes.UNIT, NEWTON_NAME, NEWTON_SYMBOL, FORCE)
KILONEWTON = prefixed_unit(prefixes.KILO, NEWTON_NAME, NEWTON_SYMBOL, FORCE)

Force._canonical_unit = NEWTON  # noqa: SLF001 -- this module owns Force's canonical unit


def Millinewton(value: Numeric) -> Force:
    """Construct a Force from a magnitude expressed in millinewtons."""
    return Force(to_exact(value) * MILLINEWTON.scale, MILLINEWTON)


def Newton(value: Numeric) -> Force:
    """Construct a Force from a magnitude expressed in newtons."""
    return Force(to_exact(value) * NEWTON.scale, NEWTON)


def Kilonewton(value: Numeric) -> Force:
    """Construct a Force from a magnitude expressed in kilonewtons."""
    return Force(to_exact(value) * KILONEWTON.scale, KILONEWTON)


# Non-SI units.

DYNE = UnitDef("dyne", "dyn", Decimal("0.00001"), FORCE)
"""The CGS unit of force: exactly `1e-5` newtons, by definition of the CGS system."""

POUND_FORCE = UnitDef("pound_force", "lbf", Decimal("4.4482216152605"), FORCE)
"""The imperial unit of force.

Exact: a pound-force is, by definition, one avoirdupois pound (exactly `0.45359237`
kg since 1959) accelerated at the standard acceleration of gravity (exactly
`9.80665` m/s^2), and both of those are themselves exact -- the product carries no
rounding error.
"""


def Dyne(value: Numeric) -> Force:
    """Construct a Force from a magnitude expressed in dynes."""
    return Force(to_exact(value) * DYNE.scale, DYNE)


def PoundForce(value: Numeric) -> Force:
    """Construct a Force from a magnitude expressed in pound-force.

    Exact, not approximate: see `POUND_FORCE`'s own docstring.
    """
    return Force(to_exact(value) * POUND_FORCE.scale, POUND_FORCE)


FORCE_UNITS: Mapping[str, Callable[[Numeric], Force]] = MappingProxyType(
    {
        MILLINEWTON.symbol: Millinewton,
        NEWTON.symbol: Newton,
        KILONEWTON.symbol: Kilonewton,
        DYNE.symbol: Dyne,
        POUND_FORCE.symbol: PoundForce,
    }
)

__all__ = [
    "DYNE",
    "FORCE_UNITS",
    "KILONEWTON",
    "MILLINEWTON",
    "NEWTON",
    "POUND_FORCE",
    "Dyne",
    "Kilonewton",
    "Millinewton",
    "Newton",
    "PoundForce",
]
