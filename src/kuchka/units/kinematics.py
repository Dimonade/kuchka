"""Unit constructors for Velocity, Acceleration, and Force.

    from kuchka import MetrePerSecond, MetrePerSecondSquared, Newton

    speed = MetrePerSecond(3)
    rate_of_change = MetrePerSecondSquared(9.81)
    push = Newton(10)

`KilometrePerHour` scales to metres per second by an exact `Fraction` (`5/18`).

`MilePerHour` scales exactly too (`0.44704`, a terminating decimal, since a mile has
been exactly `1609.344` m and an hour exactly `3600` s.

`VELOCITY_UNITS`, `ACCELERATION_UNITS`, and `FORCE_UNITS` each map a symbol to its
constructor, for boundary code that reads a unit as a string from outside the
application.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from types import MappingProxyType
from typing import TYPE_CHECKING

from kuchka.dimensions import ACCELERATION
from kuchka.dimensions import FORCE
from kuchka.dimensions import VELOCITY
from kuchka.internal import prefixes
from kuchka.internal import symbols
from kuchka.internal.prefixes import prefixed_unit
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Acceleration
from kuchka.quantities import Force
from kuchka.quantities import UnitDef
from kuchka.quantities import Velocity

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

# Velocity

METRE_PER_SECOND = UnitDef("metre_per_second", "m/s", Decimal(1), VELOCITY)
KILOMETRE_PER_HOUR = UnitDef(
    "kilometre_per_hour",
    "km/h",
    Fraction(1000, 3600),
    VELOCITY,
)

METER_PER_SECOND = METRE_PER_SECOND
KILOMETER_PER_HOUR = KILOMETRE_PER_HOUR

Velocity._canonical_unit = METRE_PER_SECOND  # noqa: SLF001 -- this module owns Velocity's canonical unit


def MetrePerSecond(value: Numeric) -> Velocity:
    """Construct a Velocity from a magnitude expressed in metres per second."""
    return Velocity(to_exact(value) * METRE_PER_SECOND.scale, METRE_PER_SECOND)


def KilometrePerHour(value: Numeric) -> Velocity:
    """Construct a Velocity from a magnitude expressed in kilometres per hour.

    Exact: `1000 / 3600` is stored as the `Fraction` `5/18`.
    """
    return Velocity(to_exact(value) * KILOMETRE_PER_HOUR.scale, KILOMETRE_PER_HOUR)


MeterPerSecond = MetrePerSecond
"""American spelling, aliasing `MetrePerSecond`: the same function object."""

KilometerPerHour = KilometrePerHour
"""American spelling, aliasing `KilometrePerHour`: the same function object."""


# Mile per hour.

MILE_PER_HOUR = UnitDef("mile_per_hour", "mph", Decimal("0.44704"), VELOCITY)


def MilePerHour(value: Numeric) -> Velocity:
    """Construct a Velocity from a magnitude expressed in miles per hour.

    Exact: a mile has been exactly `1609.344` m, so a mile per hour is exactly
    `0.44704` m/s.
    """
    return Velocity(to_exact(value) * MILE_PER_HOUR.scale, MILE_PER_HOUR)


VELOCITY_UNITS: Mapping[str, Callable[[Numeric], Velocity]] = MappingProxyType(
    {
        METRE_PER_SECOND.symbol: MetrePerSecond,
        KILOMETRE_PER_HOUR.symbol: KilometrePerHour,
        MILE_PER_HOUR.symbol: MilePerHour,
    }
)


# Acceleration

METRE_PER_SECOND_SQUARED = UnitDef(
    "metre_per_second_squared",
    f"m/s{symbols.SUPERSCRIPT_TWO}",
    Decimal(1),
    ACCELERATION,
)

METER_PER_SECOND_SQUARED = METRE_PER_SECOND_SQUARED

Acceleration._canonical_unit = METRE_PER_SECOND_SQUARED  # noqa: SLF001 -- this module owns Acceleration's canonical unit


def MetrePerSecondSquared(value: Numeric) -> Acceleration:
    """Construct an Acceleration from a magnitude in metres per second squared."""
    return Acceleration(
        to_exact(value) * METRE_PER_SECOND_SQUARED.scale,
        METRE_PER_SECOND_SQUARED,
    )


MeterPerSecondSquared = MetrePerSecondSquared
"""American spelling, aliasing `MetrePerSecondSquared`: the same function object."""

ACCELERATION_UNITS: Mapping[str, Callable[[Numeric], Acceleration]] = MappingProxyType(
    {
        METRE_PER_SECOND_SQUARED.symbol: MetrePerSecondSquared,
    }
)


# Force

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
    "ACCELERATION_UNITS",
    "DYNE",
    "FORCE_UNITS",
    "KILOMETRE_PER_HOUR",
    "KILONEWTON",
    "METER_PER_SECOND",
    "METER_PER_SECOND_SQUARED",
    "METRE_PER_SECOND",
    "METRE_PER_SECOND_SQUARED",
    "MILE_PER_HOUR",
    "MILLINEWTON",
    "NEWTON",
    "POUND_FORCE",
    "VELOCITY_UNITS",
    "Dyne",
    "KilometerPerHour",
    "KilometrePerHour",
    "Kilonewton",
    "MeterPerSecond",
    "MeterPerSecondSquared",
    "MetrePerSecond",
    "MetrePerSecondSquared",
    "MilePerHour",
    "Millinewton",
    "Newton",
    "PoundForce",
]
