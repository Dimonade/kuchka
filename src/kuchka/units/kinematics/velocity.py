"""Unit constructors for Velocity.

    from kuchka import MetrePerSecond

    walk_speed = MetrePerSecond(1.5)


`KilometrePerHour` scales to metres per second by an exact `Fraction` (`5/18`).

`MilePerHour` scales exactly too (`0.44704`, a terminating decimal, since a mile has
been exactly `1609.344` m and an hour exactly `3600` s.

`VELOCITY_UNITS` maps each symbol to its constructor, for boundary code that reads a
unit as a string from outside the application.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

from kuchka.dimensions import VELOCITY
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import UnitDef
from kuchka.quantities import Velocity

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


METRE_PER_SECOND = UnitDef(
    "metre_per_second", "m/s", Decimal(1), VELOCITY, aliases=("mps", "m/sec")
)
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


VELOCITY_UNITS: Mapping[str, Callable[[Numeric], Velocity]] = unit_table(
    "VELOCITY_UNITS",
    {
        METRE_PER_SECOND.symbol: MetrePerSecond,
        KILOMETRE_PER_HOUR.symbol: KilometrePerHour,
        MILE_PER_HOUR.symbol: MilePerHour,
    },
)

__all__ = [
    "KILOMETRE_PER_HOUR",
    "METER_PER_SECOND",
    "METRE_PER_SECOND",
    "MILE_PER_HOUR",
    "VELOCITY_UNITS",
    "KilometerPerHour",
    "KilometrePerHour",
    "MeterPerSecond",
    "MetrePerSecond",
    "MilePerHour",
]
