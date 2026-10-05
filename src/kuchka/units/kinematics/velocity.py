"""Velocity quantities and constructors for everyday motion, engineering, and space.

`Velocity` represents the rate of change of position with respect to time:

    v = dx / dt

The SI coherent unit is the metre per second.

This module also provides kilometres per hour and miles per hour for terrestrial
transport, and the knot for navigation and aviation.
All conversions implemented here are exact.

Examples
--------
Velocity covers an enormous range of everyday motion.
A comfortable walking pace of 1.5 m/s is approximately 5.4 km/h:

>>> walking_speed = MetrePerSecond(Decimal("1.5"))
>>> walking_speed.to(KILOMETRE_PER_HOUR)
5.4 km/h

A cyclist travelling at 20 km/h is moving at exactly 125/18 m/s:

>>> cycling_speed = KilometrePerHour(25)
>>> cycling_speed.to(METRE_PER_SECOND)  # doctest: +ELLIPSIS
6.94444... m/s

Motorway speeds are naturally expressed in kilometres per hour.
A vehicle travelling at 130 km/h moves at exactly 36.111... m/s:

>>> motorway_speed = KilometrePerHour(130)
>>> motorway_speed.to(METRE_PER_SECOND)  # doctest: +ELLIPSIS
36.11... m/s

Miles per hour remain common in countries using customary units.
The conversion is exact because the international mile is exactly 1609.344 metres:

>>> highway_speed = MilePerHour(60)
>>> highway_speed.to(METRE_PER_SECOND)
26.8224 m/s

The knot is defined from the international nautical mile.
One knot is exactly one nautical mile per hour, or 1852/3600 m/s:

>>> nautical_speed = Knot(1)
>>> nautical_speed.to(METRE_PER_SECOND)  # doctest: +ELLIPSIS
0.5144... m/s

A vessel travelling at 20 knots therefore moves at exactly:

>>> Knot(20).to(METRE_PER_SECOND)  # doctest: +ELLIPSIS
10.288... m/s

Velocity also connects directly to distance and time.
At 10 m/s, an object travels 600 metres in one minute:

>>> from kuchka import Metre
>>> from kuchka import Minute
>>> speed = MetrePerSecond(10)
>>> distance = speed * Minute(1)
>>> distance
600 m

The same relationship can be used to estimate travel time.
At 90 km/h, a 100 km journey takes 4000 seconds:

>>> from kuchka import Kilometre
>>> journey = Kilometre(100)
>>> travel_time = journey / KilometrePerHour(90)
>>> travel_time
4000 s

Velocity is not limited to vehicles on Earth.
Voyager 1 is travelling through interstellar space at roughly 16.95 km/s relative to
the Sun.
As of 2025 it was roughly 162.8 astronomical units from Earth and about 167.7
astronomical units from the Sun.
These are observational values and change continuously;
the two distances are different because Earth is itself moving around the Sun.

At roughly 17 km/s, Voyager 1 covers about 525 million kilometres per year:

>>> from kuchka import JulianYear
>>> voyager_speed = MetrePerSecond(17_000)
>>> voyager_distance_per_year = voyager_speed * JulianYear(1)
>>> voyager_distance_per_year
536479200000 m

The same velocity expressed in kilometres per hour is:

>>> voyager_speed.to(KILOMETRE_PER_HOUR)
61200 km/h

The difference between terrestrial and interstellar scales does not change the quantity
being represented.
A walking person, an aircraft, and a spacecraft all have `Velocity`.
Only their magnitudes and reference frames differ.

Velocity also participates directly in kinematics.
The change in velocity over time is acceleration:

    a = dv / dt

Conversely, constant acceleration changes velocity according to:

    Δv = a t

`VELOCITY_UNITS` maps symbols such as ``"m/s"``, ``"km/h"``, ``"mph"``, and ``"kn"`` to
their constructors for boundary code that receives units as external data.

Notes
-----
The SI coherent unit is

    1 m/s

The kilometre per hour is exactly

    1 km/h = 5/18 m/s

because one kilometre is exactly 1000 metres and one hour is exactly 3600 seconds.

The international mile is exactly 1609.344 metres, giving

    1 mph = 0.44704 m/s

This conversion is a terminating decimal and therefore preserves exact `Decimal`
arithmetic.

The knot is exactly one international nautical mile per hour:

    1 kn = 1852/3600 m/s = 463/900 m/s

`km/h` and `kn` therefore have exact definitions even though their reciprocal
conversion factors do not necessarily have finite decimal representations.

Velocity is a vector quantity physically, but this type represents a signed
one-dimensional magnitude.
A negative value therefore represents motion in the opposite direction along the chosen
axis.

Metric and American spellings are aliases:

`MetrePerSecond` and `MeterPerSecond` are the same constructor, and
`METRE_PER_SECOND` and `METER_PER_SECOND` are the same unit definition.

Likewise, `KilometrePerHour` and `KilometerPerHour` are the same constructor,
and `KILOMETRE_PER_HOUR` and `KILOMETER_PER_HOUR` are the same unit definition.

See Also
--------
~kuchka.quantities.Length
    Distance travelled by an object.
~kuchka.quantities.Time
    Time interval over which velocity acts.
~kuchka.quantities.Acceleration
    Rate of change of velocity.

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
    "metre_per_second",
    "m/s",
    Decimal(1),
    VELOCITY,
    aliases=("mps", "m/sec"),
    words=("meter per second", "meters per second", "metres per second"),
)
KILOMETRE_PER_HOUR = UnitDef(
    "kilometre_per_hour",
    "km/h",
    Fraction(1000, 3600),
    VELOCITY,
    aliases=("kph", "kmh", "kmph", "km/hr"),
    words=("kilometer per hour", "kilometers per hour", "kilometres per hour"),
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

MILE_PER_HOUR = UnitDef(
    "mile_per_hour",
    "mph",
    Decimal("0.44704"),
    VELOCITY,
    aliases=("mi/h", "mi/hr"),
    words=("miles per hour",),
)


def MilePerHour(value: Numeric) -> Velocity:
    """Construct a Velocity from a magnitude expressed in miles per hour.

    Exact: a mile has been exactly `1609.344` m, so a mile per hour is exactly
    `0.44704` m/s.
    """
    return Velocity(to_exact(value) * MILE_PER_HOUR.scale, MILE_PER_HOUR)


# Misc. units.

KNOT = UnitDef(
    "knot",
    "kn",
    Fraction(1852, 3600),
    VELOCITY,
)


def Knot(value: Numeric) -> Velocity:
    """Construct a Velocity from a magnitude expressed in knots.

    Parameters
    ----------
    value : Numeric
        Velocity magnitude in knots.

    Returns
    -------
    Velocity
        Velocity represented in knots.

    Examples
    --------
    A vessel travelling at 20 knots has a velocity of exactly 926/90 m/s:

    >>> Knot(20).to(METRE_PER_SECOND)  # doctest: +ELLIPSIS
    10.288... m/s

    """
    return Velocity(to_exact(value) * KNOT.scale, KNOT)


VELOCITY_UNITS: Mapping[str, Callable[[Numeric], Velocity]] = unit_table(
    "VELOCITY_UNITS",
    {
        METRE_PER_SECOND: MetrePerSecond,
        KILOMETRE_PER_HOUR: KilometrePerHour,
        MILE_PER_HOUR: MilePerHour,
        KNOT: Knot,
    },
)

__all__ = [
    "KILOMETRE_PER_HOUR",
    "KNOT",
    "METER_PER_SECOND",
    "METRE_PER_SECOND",
    "MILE_PER_HOUR",
    "VELOCITY_UNITS",
    "KilometerPerHour",
    "KilometrePerHour",
    "Knot",
    "MeterPerSecond",
    "MetrePerSecond",
    "MilePerHour",
]
