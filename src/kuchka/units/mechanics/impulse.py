"""Impulse constructors for force integrated over time.

Impulse is the time integral of force and equals the change in momentum:
J = ∫F dt = Δp.
Its coherent SI unit is the newton second (N·s), exactly equivalent in scale to the
kilogram metre per second (kg·m/s).

`kuchka` represents `Impulse` and `Momentum` as distinct quantity kinds with the same
dimension.
A force multiplied by a time produces an `Impulse`; converting that impulse to momentum
requires the explicit `Impulse.to_momentum()` operation.
`Impulse.from_momentum(momentum)` performs the reverse quantity-kind conversion.

The available units cover short and weak impulses in millinewton seconds, ordinary
engineering impulses in newton seconds, large thrust and impact events in
kilonewton seconds, CGS laboratory measurements in dyne seconds, and
pound-force seconds in FPS engineering records.

Examples
--------
During an impact test, a 0.45 kg ball initially at rest experiences an average force of
300 N for 15 ms.
Calculate the impulse and the resulting change in velocity along the force direction:

>>> from kuchka import Kilogram, Millisecond, Newton
>>> ball_mass = Kilogram(0.45)
>>> impact_force = Newton(300)
>>> contact_duration = Millisecond(15)
>>> impact_impulse = impact_force * contact_duration
>>> impact_impulse
4.5 N·s
>>> impact_impulse.to_momentum() / ball_mass
10 m/s

The force is an average over the contact interval.
The calculation gives the velocity change for the stated mass, assuming the impulse
acts along the selected axis and the ball begins at rest.

Notes
-----
Impulse represents a change in momentum, not necessarily the object's total momentum.
For a moving object, its final momentum is the initial momentum plus the impulse, with
signs representing direction along the chosen axis.

`IMPULSE_UNITS` maps symbols such as ``"mN·s"``, ``"N·s"``, ``"kN·s"``, ``"dyn·s"``,
and ``"lbf·s"`` to their constructors.
It is intended for boundary code that reads impulse values from force-time
measurements, test reports, propulsion data, or external simulation records.

See Also
--------
~kuchka.quantities.Momentum
    Linear momentum, equal in magnitude to the corresponding impulse change.
~kuchka.quantities.Force
    The quantity integrated over time to obtain impulse.
~kuchka.quantities.Time
    The duration over which the force acts.

"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from kuchka.dimensions import IMPULSE
from kuchka.internal import symbols
from kuchka.internal.unit_table import unit_table
from kuchka.numeric import Numeric
from kuchka.numeric import to_exact
from kuchka.quantities import Impulse
from kuchka.quantities import UnitDef
from kuchka.units.mechanics.force import POUND_FORCE

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Mapping

NEWTON_SECOND = UnitDef(
    "newton_second",
    f"N{symbols.MIDDLE_DOT}s",
    Decimal(1),
    IMPULSE,
    aliases=(
        "N*s",
        "N s",
    ),
    words=("newton seconds", "newton-seconds"),
)
MILLINEWTON_SECOND = UnitDef(
    "millinewton_second",
    f"mN{symbols.MIDDLE_DOT}s",
    Decimal("0.001"),
    IMPULSE,
    aliases=(
        "mN*s",
        "mN s",
    ),
    words=("millinewton seconds",),
)
KILONEWTON_SECOND = UnitDef(
    "kilonewton_second",
    f"kN{symbols.MIDDLE_DOT}s",
    Decimal(1000),
    IMPULSE,
    aliases=(
        "kN*s",
        "kN s",
    ),
    words=("kilonewton seconds",),
)
DYNE_SECOND = UnitDef(
    "dyne_second",
    f"dyn{symbols.MIDDLE_DOT}s",
    Decimal("0.00001"),
    IMPULSE,
    aliases=(
        "dyn*s",
        "dyn s",
    ),
    words=("dyne seconds", "dyne-seconds"),
)
POUND_FORCE_SECOND = UnitDef(
    "pound_force_second",
    f"lbf{symbols.MIDDLE_DOT}s",
    POUND_FORCE.scale,
    IMPULSE,
    aliases=(
        "lbf*s",
        "lbf s",
    ),
    words=("pound-force seconds",),
)

Impulse._canonical_unit = NEWTON_SECOND  # noqa: SLF001 -- this module owns Impulse's canonical unit


def MillinewtonSecond(value: Numeric) -> Impulse:
    """Construct impulse from millinewton seconds.

    Parameters
    ----------
    value : Numeric
        Impulse in mN·s.

    Returns
    -------
    Impulse
        Impulse represented in millinewton seconds.

    Examples
    --------
    A 12 g calibration slug receives a measured impulse of 2.4 mN·s during a short
    impact.
    Calculate its change in velocity:

    >>> from kuchka import Gram, MillinewtonSecond
    >>> test_mass = Gram(12)
    >>> measured_impulse = MillinewtonSecond(2.4)
    >>> measured_impulse.to_momentum() / test_mass
    0.2 m/s
    """
    return Impulse(
        to_exact(value) * MILLINEWTON_SECOND.scale,
        MILLINEWTON_SECOND,
    )


def NewtonSecond(value: Numeric) -> Impulse:
    """Construct impulse from newton seconds.

    Parameters
    ----------
    value : Numeric
        Impulse in N·s.

    Returns
    -------
    Impulse
        Impulse represented in newton seconds.

    Examples
    --------
    A robotic gripper collision imparts an impulse of 30 N·s to a 15 kg payload.
    Estimate the payload's velocity change along the collision axis:

    >>> from kuchka import Kilogram, NewtonSecond
    >>> collision_impulse = NewtonSecond(30)
    >>> payload_mass = Kilogram(15)
    >>> collision_impulse.to_momentum() / payload_mass
    2 m/s
    """
    return Impulse(to_exact(value) * NEWTON_SECOND.scale, NEWTON_SECOND)


def KilonewtonSecond(value: Numeric) -> Impulse:
    """Construct impulse from kilonewton seconds.

    Parameters
    ----------
    value : Numeric
        Impulse in kN·s.

    Returns
    -------
    Impulse
        Impulse represented in kilonewton seconds.

    Examples
    --------
    A spacecraft propulsion system delivers a total impulse of 45 kN·s to a vehicle
    whose mass during the manoeuvre is 15,000 kg.
    Estimate the velocity change, neglecting external forces and mass variation:

    >>> from kuchka import Kilogram, KilonewtonSecond
    >>> propulsion_impulse = KilonewtonSecond(45)
    >>> vehicle_mass = Kilogram(15_000)
    >>> propulsion_impulse.to_momentum() / vehicle_mass
    3 m/s
    """
    return Impulse(
        to_exact(value) * KILONEWTON_SECOND.scale,
        KILONEWTON_SECOND,
    )


def DyneSecond(value: Numeric) -> Impulse:
    """Construct impulse from dyne seconds.

    Parameters
    ----------
    value : Numeric
        Impulse in dyn·s.

    Returns
    -------
    Impulse
        Impulse represented in dyne seconds.

    Examples
    --------
    A 1 g test particle receives an impulse of 200 dyn·s in a microscale impact
    experiment.
    Calculate its change in velocity:

    >>> from kuchka import DyneSecond, Gram
    >>> test_particle = Gram(1)
    >>> impact_impulse = DyneSecond(200)
    >>> impact_impulse.to_momentum() / test_particle
    2 m/s

    The CGS unit is useful when the force measurements and specimen mass are recorded
    in the centimetre-gram-second system.
    """
    return Impulse(to_exact(value) * DYNE_SECOND.scale, DYNE_SECOND)


def PoundForceSecond(value: Numeric) -> Impulse:
    """Construct impulse from pound-force seconds.

    Parameters
    ----------
    value : Numeric
        Impulse in lbf·s.

    Returns
    -------
    Impulse
        Impulse represented in pound-force seconds.

    Examples
    --------
    A test sled receives an impulse of 13.5 lbf·s during a launcher test.
    For a 10 kg sled, calculate the resulting velocity change in SI units:

    >>> from kuchka import Kilogram, PoundForceSecond
    >>> launch_impulse = PoundForceSecond(13.5)
    >>> sled_mass = Kilogram(10)
    >>> f"{launch_impulse.to_momentum() / sled_mass:.2f}"
    '6.01 m/s'

    The calculation neglects friction, aerodynamic drag, and any impulse delivered by
    external constraints during the launch.
    """
    return Impulse(
        to_exact(value) * POUND_FORCE_SECOND.scale,
        POUND_FORCE_SECOND,
    )


IMPULSE_UNITS: Mapping[str, Callable[[Numeric], Impulse]] = unit_table(
    "IMPULSE_UNITS",
    {
        NEWTON_SECOND: NewtonSecond,
        MILLINEWTON_SECOND: MillinewtonSecond,
        KILONEWTON_SECOND: KilonewtonSecond,
        DYNE_SECOND: DyneSecond,
        POUND_FORCE_SECOND: PoundForceSecond,
    },
)

__all__ = [
    "DYNE_SECOND",
    "IMPULSE_UNITS",
    "KILONEWTON_SECOND",
    "MILLINEWTON_SECOND",
    "NEWTON_SECOND",
    "POUND_FORCE_SECOND",
    "DyneSecond",
    "KilonewtonSecond",
    "MillinewtonSecond",
    "NewtonSecond",
    "PoundForceSecond",
]
