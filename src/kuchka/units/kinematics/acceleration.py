"""Acceleration constructors: metres per second squared and the gal.

`Acceleration` represents the rate of change of velocity with respect to time:

    a = dv / dt

The SI coherent unit is the metre per second squared.

This module also provides the gal and its commonly used submultiples for gravimetry:

    1 Gal = 0.01 m/s²
    1 mGal = 1e-5 m/s²
    1 µGal = 1e-8 m/s²

The gal is a non-SI unit of acceleration particularly associated with gravitational
measurements.
Milligals are common in gravity surveys, while microgals are used for higher-precision
gravity measurements.

Examples
--------
Acceleration becomes useful immediately when combined with time.
A vehicle accelerating at 3 m/s² gains 3 m/s of velocity every second:

>>> from kuchka import Second
>>> acceleration = MetrePerSecondSquared(3)
>>> acceleration * Second(1)
3 m/s

The same relationship gives the velocity change over a longer interval:

>>> acceleration * Second(4)
12 m/s

Acceleration also determines how long a uniformly braking vehicle takes to stop.
Starting at 90 km/h and decelerating at exactly 5 m/s²:

>>> from kuchka import KilometrePerHour
>>> initial_speed = KilometrePerHour(90)
>>> braking = MetrePerSecondSquared(-5)
>>> stopping_time = -initial_speed / braking
>>> stopping_time
5 s

The same constant-acceleration model gives the stopping distance:

>>> stopping_distance = initial_speed * stopping_time + braking * stopping_time**2 / 2
>>> stopping_distance
62.5 m

Acceleration can also be derived from force and mass.
A 1500 kg vehicle subjected to a 3 kN net force accelerates at exactly 2 m/s²:

>>> from kuchka import Kilogram
>>> from kuchka import Kilonewton
>>> net_force = Kilonewton(3)
>>> vehicle_mass = Kilogram(1500)
>>> net_force / vehicle_mass
2 m/s²

The same relationship is Newton's second law:

    F = m a

and `kuchka` can use either direction of that relationship.

The gal is particularly useful when expressing small variations in the gravitational
field.
Fifty gals correspond to exactly 0.5 m/s²:

>>> local_gravity_difference = Gal(50)
>>> local_gravity_difference == MetrePerSecondSquared(Decimal("0.5"))
True

Gravity surveys commonly work at much smaller scales.
A 2.5 milligal anomaly is exactly 0.000025 m/s²:

>>> anomaly = Milligal(2.5)
>>> anomaly
2.5 mGal
>>> anomaly == MetrePerSecondSquared(Decimal("0.000025"))
True

High-precision gravity measurements can reach the microgal scale:

>>> microgravity_change = Microgal(40)
>>> microgravity_change
40 µGal
>>> microgravity_change == MetrePerSecondSquared(Decimal("0.0000004"))
True

Acceleration also matters far outside terrestrial mechanics.
A spacecraft maintaining a constant 0.01 m/s² acceleration for one hour changes its
velocity by exactly 36 m/s:

>>> from kuchka import Hour
>>> low_thrust = MetrePerSecondSquared(Decimal("0.01"))
>>> velocity_change = low_thrust * Hour(1)
>>> velocity_change
36 m/s

The physical quantity is the same in every case: rate of change of velocity.
Only the scale and application change.

`ACCELERATION_UNITS` maps symbols such as ``"m/s²"``, ``"Gal"``, ``"mGal"``,
and ``"µGal"`` to their constructors for boundary code that receives units as external
data.

Notes
-----
The SI coherent unit is

    1 m/s²

The gal is exactly

    1 Gal = 0.01 m/s²

Milligal and microgal are exact decimal submultiples:

    1 mGal = 1e-5 m/s²
    1 µGal = 1e-8 m/s²

These units are all linear units of the same `Acceleration` quantity.

Metric and American spellings are aliases:

`MetrePerSecondSquared` and `MeterPerSecondSquared` are the same constructor, and
`METRE_PER_SECOND_SQUARED` and `METER_PER_SECOND_SQUARED` are the same unit definition.

See Also
--------
~kuchka.quantities.Velocity
    Acceleration changes velocity over time.
~kuchka.quantities.Force
    Force, mass, and acceleration are related by Newton's second law.
~kuchka.quantities.Time
    Time over which acceleration acts.
~kuchka.quantities.Length
    Distance travelled during accelerated motion.

"""  # NOTE: This is due the doctest: +SKIP that will be removed later.

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import ACCELERATION
from kuchka.internal import symbols
from kuchka.internal.spelling import powered
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Acceleration
from kuchka.quantities import UnitDef

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping


METRE_PER_SECOND_SQUARED = UnitDef(
    "metre_per_second_squared",
    f"m/s{symbols.SUPERSCRIPT_TWO}",
    Decimal(1),
    ACCELERATION,
    aliases=powered("m/s", 2),
    words=(
        "meter per second squared",
        "meters per second squared",
        "metres per second squared",
    ),
)

METER_PER_SECOND_SQUARED = METRE_PER_SECOND_SQUARED

Acceleration._canonical_unit = METRE_PER_SECOND_SQUARED  # noqa: SLF001 -- this module owns Acceleration's canonical unit


def MetrePerSecondSquared(value: Numeric) -> Acceleration:
    """Construct acceleration from a magnitude in metres per second squared.

    Parameters
    ----------
    value : Numeric
        Acceleration magnitude in metres per second squared.

    Returns
    -------
    Acceleration
        Acceleration represented in metres per second squared.

    Examples
    --------
    A vehicle accelerating at 5 m/s² gains exactly 10 m/s over two seconds:

    >>> from kuchka import Second
    >>> acceleration = MetrePerSecondSquared(5)
    >>> acceleration * Second(2)
    10 m/s

    """
    return Acceleration(
        to_exact(value) * METRE_PER_SECOND_SQUARED.scale,
        METRE_PER_SECOND_SQUARED,
    )


MeterPerSecondSquared = MetrePerSecondSquared
"""American spelling, aliasing `MetrePerSecondSquared`: the same function object."""

# Non-SI.

GAL = UnitDef("gal", "Gal", Decimal("0.01"), ACCELERATION)
MILLIGAL = UnitDef(
    "milligal", "mGal", Decimal("0.00001"), ACCELERATION, aliases=("mgal",)
)
MICROGAL = UnitDef(
    "microgal",
    f"{symbols.MICRO}Gal",
    Decimal("0.00000001"),
    ACCELERATION,
    aliases=("uGal", "ugal", f"{symbols.MICRO}gal"),
)


def Gal(value: Numeric) -> Acceleration:
    """Construct acceleration from a magnitude expressed in gals.

    Parameters
    ----------
    value : Numeric
        Acceleration magnitude in gals.

    Returns
    -------
    Acceleration
        Acceleration represented in gals.

    Examples
    --------
    One gal is exactly one centimetre per second squared:

    >>> Gal(1) == MetrePerSecondSquared(Decimal("0.01"))
    True

    """
    return Acceleration(to_exact(value) * GAL.scale, GAL)


def Milligal(value: Numeric) -> Acceleration:
    """Construct acceleration from a magnitude expressed in milligals.

    Parameters
    ----------
    value : Numeric
        Acceleration magnitude in milligals.

    Returns
    -------
    Acceleration
        Acceleration represented in milligals.

    Examples
    --------
    A 2.5 milligal gravity anomaly corresponds to exactly 0.000025 m/s²:

    >>> anomaly = Milligal(2.5)
    >>> anomaly
    2.5 mGal
    >>> anomaly == MetrePerSecondSquared(Decimal("0.000025"))
    True

    """
    return Acceleration(to_exact(value) * MILLIGAL.scale, MILLIGAL)


def Microgal(value: Numeric) -> Acceleration:
    """Construct acceleration from a magnitude expressed in microgals.

    Parameters
    ----------
    value : Numeric
        Acceleration magnitude in microgals.

    Returns
    -------
    Acceleration
        Acceleration represented in microgals.

    Examples
    --------
    High-precision gravity measurements can use microgal-scale changes:

    >>> change = Microgal(40)
    >>> change
    40 µGal
    >>> change == MetrePerSecondSquared(Decimal("0.0000004"))
    True

    """
    return Acceleration(to_exact(value) * MICROGAL.scale, MICROGAL)


ACCELERATION_UNITS: Mapping[str, Callable[[Numeric], Acceleration]] = unit_table(
    "ACCELERATION_UNITS",
    {
        METRE_PER_SECOND_SQUARED: MetrePerSecondSquared,
        GAL: Gal,
        MILLIGAL: Milligal,
        MICROGAL: Microgal,
    },
)

__all__ = [
    "ACCELERATION_UNITS",
    "GAL",
    "METER_PER_SECOND_SQUARED",
    "METRE_PER_SECOND_SQUARED",
    "MICROGAL",
    "MILLIGAL",
    "Gal",
    "MeterPerSecondSquared",
    "MetrePerSecondSquared",
    "Microgal",
    "Milligal",
]
